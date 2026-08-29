# After apply, listing the directory shows terraform.tfstate
$ ls -lah
total 56
drwxr-xr-x  8 rithinskarla staff 256B May 13 06:31  .
drwxr-xr-x  8 rithinskarla staff 256B May 12 19:50  ..
drwxr-xr-x  3 rithinskarla staff 96B May 12 16:27  .terraform
-rw-r--r--  1 rithinskarla staff 1.1K May 12 16:27  .terraform.lock.hcl
-rw-r--r--  1 rithinskarla staff 415B May 13 06:28  main.tf
-rw-r--r--  1 rithinskarla staff 159B May 12 16:27  providers.tf
-rw-r--r--  1 rithinskarla staff 8.4K May 13 06:31  terraform.tfstate
-rw-r--r--  1 rithinskarla staff 861B May 12 16:27  variables.tf
```

This `terraform.tfstate` file represents the current infrastructure as Terraform knows it.

## What is inside the state file?

Terraform state acts as the authoritative mapping between your configuration and the real-world infrastructure. Think of it as Terraform’s memory: without it, Terraform cannot determine which resources exist, their IDs, or which attributes have changed.

A simplified excerpt of a Terraform state file (JSON):

```json theme={null}
{
  "version": 4,
  "terraform_version": "1.5.7",
  "serial": 1,
  "lineage": "62f9521-2fc2-a699-211f-e1f306c99896",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "azurerm_storage_account",
      "name": "example",
      "provider": "provider[\"registry.terraform.io/hashicorp/azurerm\"]",
      "instances": [
        {
          "schema_version": 4,
          "attributes": {
            "access_tier": "Hot",
            "account_kind": "StorageV2",
            "account_replication_type": "LRS",
            "account_tier": "Standard",
            "allow_nested_items_to_be_public": true,
            "allowed_copy_scope": "",
            "azure_files_authentication": [],
            "blob_properties": []
          }
        }
      ]
    }
  ]
}
```

This JSON includes provider info, resource types and names, and all recorded attributes (SKU, replication type, access tier, etc.). Because the state can contain sensitive or critical information (resource IDs, endpoints, sometimes secrets), protecting state is essential.

> **lightbulb** Protect your state: state files can contain sensitive values (resource IDs, endpoints, and occasionally secrets). When storing state remotely, enable encryption and strict access controls to prevent unauthorized access.

## Where is state stored?

* By default: `terraform.tfstate` stored locally in your working directory. This is fine for learning, demos, or single-user scenarios.
* For teams and automation: use a remote backend (Azure Storage, Amazon S3, Terraform Cloud, etc.) to centralize state, provide locking, and improve access control.

> **warning** Warning: Local state lacks concurrency protection. Multiple users or CI jobs operating on the same local state can cause conflicts or corruption. Use a remote backend for team workflows.

## Remote backends — why and when to use them

Remote backends provide several advantages:

* Centralized storage so all team members and CI pipelines use the same state.
* Locking support (depending on backend) to prevent concurrent operations.
* Access control, auditability, and encryption at rest.
* Integration with remote runs and workspace concepts (e.g., Terraform Cloud).

Popular backend options:

* Azure Storage Account: reliable for Azure-native workflows.
* Amazon S3 (with DynamoDB locking): common for AWS and cross-cloud setups.
* Terraform Cloud: managed state, remote runs, and policy enforcement.

References:

* [Azure Storage Account overview](https://learn.microsoft.com/azure/storage/common/storage-account-overview)
* [Amazon S3](https://aws.amazon.com/s3/)
* [Terraform Cloud](https://www.terraform.io/cloud)

## Quick comparison: local vs remote state

| Aspect                 | Local state (`terraform.tfstate`) | Remote backend                     |
| ---------------------- | --------------------------------: | ---------------------------------- |
| Best for               |      Single user, experimentation | Teams, CI/CD, production           |
| Concurrency protection |                                No | Usually yes (depending on backend) |
| Access control         |          OS/file permissions only | Fine-grained RBAC, cloud IAM       |
| Encryption at rest     |                            Manual | Typically provided by backend      |
| Recovery / backups     |                  Manual snapshots | Backend-managed/versioned          |

## Why state matters (summary)

* Maps Terraform configuration to real resources (IDs, attributes).
* Enables incremental updates — Terraform only modifies what changed.
* Prevents duplicate resource creation and is required for plan/apply/destroy/import.
* Serves as the source of truth for Terraform operations.

Check your working directory for `terraform.tfstate` to confirm the resources you’ve deployed.

Now that you understand Terraform state and why it’s important, the next step is to configure a remote backend suited to your team and automation needs.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/d0fef6dd-c271-403d-b4ac-ee1f20c1839b/lesson/130cadb8-31f6-42e0-8ef0-4686ad423a81)


# Considerations

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Workspaces/Considerations/page

Guidance comparing Terraform workspaces and separate state files, evaluating isolation, risk, complexity, and recommended patterns for governance, teams, and environment separation

Pause to review the key design trade-offs before adopting Terraform workspaces versus maintaining separate state files. Each approach has implications for isolation, risk, operational complexity, and suitability for enterprise governance. Use the guidance below to align your choice with team structure, compliance needs, and blast-radius tolerance.

## At a glance

* Workspaces share the same configuration across environments and keep separate state per workspace.
* Separate state files (backends) decouple environments, allowing independent configuration, pipelines, and ownership.
* The right pattern depends on your need for simplicity versus strict isolation and governance.

## Comparison: workspaces vs separate state files

| Criteria               |                                                                                   Terraform Workspaces | Separate state files / backends                                                               |
| ---------------------- | -----------------------------------------------------------------------------------------------------: | --------------------------------------------------------------------------------------------- |
| Configuration          | Shared across environments; differences handled via variables, conditionals, or workspace-aware logic. | Each environment can have its own configuration, enabling independent evolution.              |
| State isolation        |                                                  Each workspace maps to its own state file (isolated). | State files are explicitly separated in different backends or directories (strong isolation). |
| Blast radius & risk    |                        Medium: shared config and CI/CD pipelines can produce cross-environment impact. | Smaller: decoupled backends/pipelines confine failures to a single environment.               |
| Complexity             |                                   Lower: less duplication and simpler for small, single-team projects. | Higher: multiple repos/directories/pipelines add overhead but provide finer control.          |
| Enterprise suitability |   Limited: may struggle with strict compliance, fine-grained access control, and multi-team ownership. | Better: aligns with security boundaries, audit requirements, and organizational ownership.    |

Key takeaway: workspaces optimize simplicity and reduced duplication; separate state files prioritize safety, scalability, and governance.

## When not to use workspaces

Avoid workspaces when any of the following apply:

* Your environment requires strong isolation between environments (security, compliance, or data separation).
* Different teams own different environments and need independent lifecycles or deployment control.
* Each environment must have its own pipeline lifecycle (plan/apply/approve) or separate audit trails.
* Organizational governance demands explicit boundaries and limited blast radius.

<Frame>
  <img alt="The image illustrates when not to use Terraform Workspaces, featuring a figure navigating a path with four numbered steps and corresponding reasons listed on the side." />
</Frame>

In these scenarios, using workspaces can increase operational risk by introducing hidden coupling between environments.

## Recommended alternatives

When you need stronger separation, consider these patterns. They trade some convenience for predictability, safety, and governance:

* Separate backends
  * Use distinct remote backends (e.g., different state storage containers, buckets, or workspaces in a supported backend) to enforce state isolation and manage access controls independently.
* Separate directories or repositories per environment
  * Put environment-specific configuration in different folders or repos so teams can evolve independently and apply different lifecycle rules.
* Independent pipelines per environment
  * Create dedicated CI/CD pipelines per environment to enforce approvals, reduce accidental cross-environment changes, and provide auditable runs.

These patterns align well with large organizations, regulated industries, or multi-team ownership models where isolation and governance are paramount.

<Frame>
  <img alt="The image outlines a decision-making flow for using separate backends or directories/repositories based on different cases such as strong isolation, different team management, separate pipelines, and compliance needs." />
</Frame>

## Practical guidance

* Start by mapping ownership, compliance requirements, and acceptable blast radius for your systems. This will guide whether simplicity (workspaces) or strong boundaries (separate backends/repos) is the better fit.
* For small teams and non-critical workloads, workspaces can reduce duplication and speed onboarding.
* For production-critical or regulated systems, prefer separate backends/repositories and distinct pipelines to avoid accidental cross-environment impacts.

> **lightbulb** If you are unsure which approach to choose, map ownership, compliance requirements, and blast-radius tolerance. For small teams with simple requirements, workspaces may be acceptable. For multi-team, compliant, or production-critical environments, prefer separate backends and repositories.

## Links and references

* [Terraform Workspaces — HashiCorp Documentation](https://www.terraform.io/docs/state/workspaces.html)
* [Terraform Backends — HashiCorp Documentation](https://www.terraform.io/docs/language/settings/backends/index.html)
* [Best practices for managing Terraform state](https://www.terraform.io/docs/cloud/guides/recommended-practices/state.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/0eb3275a-a37d-45a5-86b5-4920e2e44e7c/lesson/7441dbfe-cfd4-4775-8c72-630bf79a51ab)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/0eb3275a-a37d-45a5-86b5-4920e2e44e7c/lesson/c8ca3a25-469d-4405-b2fe-da02e518a033)
