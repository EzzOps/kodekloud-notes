# Initialize backend, download providers and modules, and configure state backend
terraform init

# Reinitialize backend configuration (useful when backend settings changed)
terraform init -reconfigure
```

Authentication notes:

* Ensure credentials for the backend (storage account key, SAS token, or appropriate managed identity) are available in your environment before running `terraform init`.
* For Azure, authentication methods include `az login` (CLI), environment variables for a Service Principal (`ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`), or managed identities when running inside Azure.

***

## Handling locks and stuck state

Terraform relies on backend-supported locking to avoid concurrent state writes. With Azure Blob Storage, locking uses blob leases. When a lock is active, operations that require write access will fail with a lock acquisition error.

Recovery options:

* Before forcing anything, determine whether the lock holder is still actively working. Killing a valid operation can lead to corruption.
* If the lock is stale (e.g., caused by a crashed process), you can use `terraform force-unlock` to remove the lock.

```bash theme={null}
terraform force-unlock LOCK_ID
```

> **warning** Use `terraform force-unlock` only after confirming the lock holder is not active. Forcibly removing a valid lock can cause concurrent writes and lead to state corruption. Investigate the origin of the lock and prefer coordination or waiting over forcing when possible.

***

## Common remote-state failure scenarios and their effects

* Permission issues
  * Symptom: `terraform init`, `terraform plan`, or `terraform apply` fails with authorization or access denied errors.
  * Cause: Insufficient permissions to read or write the blob/container.
  * Remedy: Grant the necessary storage permissions (storage account keys, properly-scoped SAS tokens, or Azure role assignments) and verify with blob access tests.

* Lock acquisition failures
  * Symptom: Operations fail due to a lock or lease held by another process.
  * Cause: Parallel `apply` or a crashed process still holding a lease.
  * Remedy: Confirm the lock owner and, if safe, run `terraform force-unlock` to clear a stale lock.

* Network or availability issues
  * Symptom: Reads/writes to state fail intermittently; CI runs fail or stall.
  * Cause: Transient network problems, DNS, or cloud service disruptions.
  * Remedy: Improve CI network reliability, add retries in automation, and configure retry/backoff policies where supported.

* Corrupted or incompatible state
  * Symptom: Terraform errors when reading state or resource addresses no longer match; plans behave unexpectedly.
  * Cause: Manual edits of state, failed migrations, or incompatible backend transitions.
  * Remedy: Restore state from backups/version history or run targeted state manipulation commands (`terraform state rm` / `terraform import`) carefully. Avoid manual state edits unless you fully understand implications.

* Secrets exposure
  * Symptom: Sensitive values appear in state or logs.
  * Cause: Terraform providers output secrets into state or use outputs with sensitive=false.
  * Remedy: Restrict access to the storage account/container, enable encryption and access logging, and follow provider best practices to prevent secrets from appearing in state. Rotate secrets if exposure is suspected.

***

## Best practices summary

* Always use a remote backend for team or CI/CD workflows—never rely on local state for shared infrastructure.
* Protect backend access with least-privilege authentication (managed identities, scoped SAS, or minimal role assignments).
* Enable versioning or automatic backups on the storage account/container to enable state recovery.
* Use backend locking and avoid keeping locks held for long periods; design CI to run short-lived Terraform operations.
* Test backend initialization and state migration in a pre-production environment before applying in production.
* Use `terraform force-unlock` sparingly and only after verifying the lock holder is not active.

***

## Links and References

* Terraform init documentation: [https://developer.hashicorp.com/terraform/cli/commands/init](https://developer.hashicorp.com/terraform/cli/commands/init)
* Azure Blob Storage: [https://learn.microsoft.com/en-us/azure/storage/blobs/](https://learn.microsoft.com/en-us/azure/storage/blobs/)
* SAS tokens overview: [https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview)
* Managed identities overview: [https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
* Blob leases (locking): [https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-lease](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-lease)

This article includes Azure-specific configuration examples and practical recovery advice to help teams set up reliable Terraform remote state workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4693ec96-f075-4e4f-922b-1f1e27202120/lesson/5dffda35-1d74-457b-99bb-cd8d46b8e333)


# Remote State Failure Modes

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Remote-State/Remote-State-Failure-Modes/page

Terraform remote state failure modes on Azure with impacts, recovery steps, and best practices to prevent and mitigate lost backend access, deleted state blobs, stale locks, and credential issues

In this lesson we cover what can go wrong when Terraform uses a remote state backend, why these failures are operationally critical, and how to mitigate them. Remote state is the single source of truth for Terraform's view of your infrastructure; when it becomes unavailable or corrupted, Terraform operations halt for everyone.

We’ll review the common failure scenarios, their immediate impact, and practical operational best practices and recovery steps.

## Common failure scenarios

The most frequent remote-state failure modes include:

* Loss of access to the backend storage account
  * Causes: revoked or changed RBAC roles, expired/rotated credentials, Conditional Access policies blocking automation, or identity misconfiguration.
  * Effect: Terraform can no longer authenticate to read/write the state.
* Deleted, renamed, or moved state container/blob
  * Causes: accidental human action or overly-broad automation that modifies storage resources.
  * Effect: Terraform cannot locate the expected state file; operations fail with “state not found”/“backend error”.
* Stale lock (broken or abandoned state lock)
  * Causes: an interrupted or crashed Terraform operation left a lease/lock on the state blob.
  * Effect: Subsequent `terraform plan`/`apply` are blocked until the stale lease is broken or allowed to expire.
* Credential drift or identity mismatch
  * Causes: secret rotation, switching service principals, or CI/CD pipelines not updated after identity changes.
  * Effect: Authentication failures across all consumers of the backend.

<Frame>
  <img alt="The image illustrates common failure scenarios with a man scratching his head, missed darts near a target, and three listed scenarios: loss of access to the storage account, deleted or renamed state container, and broken state lock (stale lease)." />
</Frame>

## What breaks first — and why it matters

When remote state access fails, the effects are immediate and broad:

* Terraform cannot plan or apply changes. Without access to the state, Terraform cannot compute diffs, so both `terraform plan` and `terraform apply` will fail with backend/state errors.
* All users and automation pipelines are blocked. Because the backend is shared, a backend failure prevents engineers and CI/CD jobs from progressing.
* Infrastructure becomes unmanaged until state access is restored. The live infrastructure continues running, but Terraform cannot make coordinated updates or safely change resources until the state is recovered.

<Frame>
  <img alt="The image outlines the impacts of remote state failure modes in a workflow, including Terraform's inability to plan or apply changes, infrastructure becoming unmanaged, and users and automation pipelines being blocked." />
</Frame>

Summary table: failure -> cause -> immediate mitigation

| Failure mode                | Typical cause                                        | Short-term mitigation                                                                       |
| --------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Loss of backend access      | RBAC change, conditional access, rotated credentials | Re-enable identity/pipeline credentials, check Conditional Access; restore role assignments |
| Deleted or moved state blob | Human error or automation                            | Use blob soft-delete/versioning to restore; recover from backups                            |
| Stale state lock (lease)    | Crashed Terraform or interrupted operation           | Break the stale lease via Azure CLI or Portal (see example below)                           |
| Credential mismatch         | Secret rotation or identity swap                     | Update pipeline credentials and re-run authenticated actions                                |

## Operational best practices (preventive and detective controls)

Adopt these practices to reduce both the likelihood of remote-state failures and their blast radius:

* Apply least-privilege access to the backend
  * Grant only the identities and automation accounts that truly need read/write state access.
  * Avoid overly broad roles that also allow resource deletion.
* Make the backend storage “hands-off”
  * Avoid manual edits to the state container or blob. Treat backend storage as a critical system that humans and unapproved automation must not touch.
* Protect against accidental deletion
  * Use resource locks, deny assignments, and strict role constraints for the storage account.
* Enable built-in storage protections
  * Turn on blob soft-delete and blob versioning in Azure Storage to enable point-in-time recovery of state blobs.
* Monitor and alert
  * Treat the backend as a dependency: capture storage account metrics, authentication failures, audit logs, and alert on access errors or failed reads/writes.
* Prepare recovery runbooks
  * Document how to break stale leases and recover state from versioning or soft-delete. Keep these runbooks accessible to SRE/DevOps on-call teams.
* Plan for credential rotation
  * Keep a short documented path to update CI/CD pipelines and automation when secrets or service principals rotate.

<Frame>
  <img alt="The image shows a person working on a laptop at a desk with coding icons around, alongside a list of best practices: restrict backend access, monitor availability, and avoid manual storage changes." />
</Frame>

> **lightbulb** Treat the remote state backend as a critical, highly-available system: restrict direct human access, monitor it closely, enable storage protections (soft-delete/versioning), and document recovery steps for stale locks and credential failures.

## Actionable recovery steps

Here are practical steps to recover common failure modes.

Breaking a stale lease (example using Azure CLI)

* If a previous operation left a lease on the blob, break it so Terraform can continue:

```bash theme={null}
az storage blob lease break \
  --container-name <container-name> \
  --name <state-blob-name> \
  --account-name <storage-account-name>
```

* After breaking the lease, re-run `terraform plan` (in a safe environment) to confirm state access.

Recovering a deleted or moved state blob

* If you enabled soft-delete or versioning, recover the state blob from the portal or via the Azure CLI. The exact restore steps depend on whether you enabled soft-delete or blob versioning—see Azure Storage docs linked below.
* If you maintain external backups of the state (recommended), copy the backup file back to the expected blob location and re-run Terraform operations to verify state integrity.

Handling authentication/identity failures

* If credentials were rotated, update service principal secrets or managed identity configurations in CI/CD pipelines and automation.
* Verify the identity has the required RBAC role to access the storage account and the specific container/blob.

Dealing with corrupted state

* If the state file is corrupt, restore from the most recent good backup or blob version. Validate the recovered state with `terraform plan` before making changes.
* Consider creating an isolated environment to validate recovery steps before applying changes to production resources.

## Example troubleshooting checklist (quick reference)

1. Confirm storage account and container exist and the blob name matches Terraform backend configuration.
2. Verify identity and credentials:
   * Test authentication from the same agent/pipeline that failed.
3. Check for stale lease:
   * Use Azure CLI to inspect or break the lease.
4. Check storage protections:
   * Are soft-delete or versioning enabled? If so, recover a previous version.
5. Restore from a known-good backup if necessary.
6. Validate recovered state with `terraform plan` in a safe workspace/environment.

## Final takeaway

Remote state is the coordination point for Terraform and a single point of failure if not managed carefully. Reduce risk by applying least-privilege access, protecting state storage with locks/versioning, monitoring access, and documenting recovery playbooks. With the right controls and runbooks, you can significantly reduce downtime and safely recover from the majority of remote-state failures.

## Links and references

* [Terraform CLI: plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
* [Terraform CLI: apply](https://developer.hashicorp.com/terraform/cli/commands/apply)
* [Azure RBAC overview](https://learn.microsoft.com/azure/role-based-access-control/overview)
* [Azure Conditional Access overview](https://learn.microsoft.com/azure/active-directory/conditional-access/overview)
* Azure CLI: break blob lease — [https://learn.microsoft.com/cli/azure/storage/blob/lease](https://learn.microsoft.com/cli/azure/storage/blob/lease)
* Azure Storage: soft-delete — [https://learn.microsoft.com/azure/storage/blobs/storage-blob-soft-delete](https://learn.microsoft.com/azure/storage/blobs/storage-blob-soft-delete)
* Azure Storage: blob versioning — [https://learn.microsoft.com/azure/storage/blobs/storage-blob-versioning](https://learn.microsoft.com/azure/storage/blobs/storage-blob-versioning)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4693ec96-f075-4e4f-922b-1f1e27202120/lesson/75acf611-6fbb-420f-b9b1-26a0798a178e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4693ec96-f075-4e4f-922b-1f1e27202120/lesson/0fec8bcd-42a1-4009-8e31-997641e4fa83)
