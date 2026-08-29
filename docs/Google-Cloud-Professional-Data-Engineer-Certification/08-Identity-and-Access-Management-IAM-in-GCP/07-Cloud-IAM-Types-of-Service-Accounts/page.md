# Retrieve the IAM policy for a project
gcloud projects get-iam-policy PROJECT_ID --format=json
```

Sample (shortened) output showing bindings:

```json theme={null}
[
  {
    "role": "roles/editor",
    "members": [
      "user:alice@example.com"
    ]
  },
  {
    "role": "roles/viewer",
    "members": [
      "group:eng@example.com"
    ]
  }
]
```

***

## 2) Predefined (service) roles

Predefined roles (service roles) are published and maintained by Google Cloud. They provide narrower permission sets specific to individual services.

Benefits:

* Granularity: restricts access to required APIs and actions for a service.
* Maintained by Google Cloud: roles evolve with service features.

Examples:

* `roles/compute.instanceAdmin.v1` — manage Compute Engine instances
* `roles/storage.objectViewer` — read objects in Cloud Storage

Inspect a predefined role's permissions:

```bash theme={null}
# Describe a predefined role
gcloud iam roles describe roles/compute.instanceAdmin.v1 --format="yaml(name,includedPermissions)"
```

Example output (abridged):

```yaml theme={null}
name: roles/compute.instanceAdmin.v1
includedPermissions:
- compute.instances.create
- compute.instances.delete
- compute.instances.get
- compute.instances.setMetadata
# ...
```

Best practice:

* When granting VM instance management privileges, prefer a relevant predefined role such as `roles/compute.instanceAdmin.v1` or an even narrower predefined role if available, instead of a basic Editor.

<Callout icon="lightbulb">
  Prefer predefined roles for most production scenarios. They provide service-focused permission sets that are more secure than basic roles while remaining easy to manage.
</Callout>

***

## 3) Custom roles

Custom roles let you define exactly which permissions a role contains. They can be created at the organization or project level and are ideal when predefined roles are too broad or don't cover your required combination of permissions.

When to use custom roles:

* You need a role more restrictive than available predefined roles.
* You need to combine permissions from multiple services into one role.
* You require strict separation of duties tailored to your organization.

Create a project-level custom role example:

```bash theme={null}
gcloud iam roles create customInstanceOperator \
  --project=PROJECT_ID \
  --title="Instance Operator" \
  --description="Manage Compute Engine instances without billing or org administration permissions" \
  --permissions="compute.instances.get,compute.instances.list,compute.instances.start,compute.instances.stop"
```

Describe a custom role:

```bash theme={null}
gcloud iam roles describe customInstanceOperator --project=PROJECT_ID --format="yaml(name,stage,includedPermissions)"
```

Notes:

* Custom roles have a lifecycle stage (e.g., `ALPHA`, `BETA`, `GA`, `DISABLED`) and can be updated over time.
* Track changes and test custom roles before wide adoption to avoid accidental permission gaps.

***

## Practical tips and commands

* See which roles a principal has on a project:

```bash theme={null}
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:alice@example.com" \
  --format="table(bindings.role)"
```

* Find role definitions and included permissions:
  * Use `gcloud iam roles describe roles/ROLE_NAME` for predefined roles.
  * Use `gcloud iam roles describe ROLE_ID --project=PROJECT_ID` for project-level custom roles.

* For permission-level troubleshooting:
  * Use the IAM Policy Troubleshooter in the Cloud Console: [https://cloud.google.com/iam/docs/policy-troubleshooter](https://cloud.google.com/iam/docs/policy-troubleshooter)
  * Or the gcloud reference for policy-troubleshooter: [https://cloud.google.com/sdk/gcloud/reference/policy-troubleshooter](https://cloud.google.com/sdk/gcloud/reference/policy-troubleshooter)

* Use IAM Recommender to get suggestions for tightening permissions:
  * [https://cloud.google.com/iam/docs/recommender](https://cloud.google.com/iam/docs/recommender)

* Audit changes and review bindings regularly to detect drift and over-privileged principals.

***

## Summary

* Basic (Owner/Editor/Viewer) roles are broad, simple, and not recommended for production due to increased risk.
* Predefined roles are Google-provided, service-specific roles that offer better granularity and are suitable for most production needs.
* Custom roles let you compose precise permission sets and are optimal when predefined roles are too permissive or incomplete.

Always apply the principle of least privilege: choose the most restrictive role that still allows principals to perform their job.

## Links and references

* [IAM documentation — Google Cloud](https://cloud.google.com/iam/docs/)
* [IAM Policy Troubleshooter](https://cloud.google.com/iam/docs/policy-troubleshooter)
* [IAM Recommender](https://cloud.google.com/iam/docs/recommender)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/d0d0759e-e3e6-46e0-85d2-726c31147987" />
</CardGroup>


# Cloud IAM Types of Service Accounts

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Cloud-IAM-Types-of-Service-Accounts/page

Explains Google Cloud service accounts, their types, usage differences, and production best practices for secure least privileged identity management.

Hello and welcome back.

In this lesson we cover service accounts: what they are, why you need them, how they differ, and safe production practices for using them.

## What is a service account and why use one?

IAM grants identities (users or service accounts) roles that permit specific actions. A human Google account receives a role and a person signs in to the Cloud Console to act. For non-human identities—Compute Engine VMs, Cloud Run services, Cloud Composer workers, or other GCP services—you need a programmatic identity: a service account.

When you attach a service account to a resource (for example, a Compute Engine VM), applications running on that resource can call Google Cloud APIs with the service account identity and the permissions you granted. This avoids impersonating individual users and enables automated tasks to act securely.

<Frame>
  <img alt="A slide titled &#x22;Cloud IAM – Types of Service Accounts&#x22; showing a diagram where a Compute Engine instance uses a service account (Role: VPN Editor) to access a Cloud VPN inside a project/zone. The graphic illustrates how applications/VMs authenticate to Google Cloud services." />
</Frame>

Example scenarios:

* A VM needs to change network settings (Compute Network Admin). Attach a service account with the appropriate role and the VM can make those changes programmatically.
* Cloud Composer needs to write to Cloud Storage. Assign a dedicated service account to Composer and grant the required Storage permissions so Composer writes without a human credential.

Quick CLI examples:

* Grant a role to a service account:

```bash theme={null}
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/compute.networkAdmin"
```

* Create a VM with a service account attached:

```bash theme={null}
gcloud compute instances create INSTANCE_NAME \
  --zone=ZONE \
  --service-account=SA_EMAIL \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

* Replace the service account on an existing VM:

```bash theme={null}
gcloud compute instances set-service-account INSTANCE_NAME \
  --service-account=SA_EMAIL --zone=ZONE
```

## Types of service accounts

Google Cloud provides three main types of service accounts. The table below summarizes who manages each type, typical use cases, privilege patterns, and how they are created or deleted.

| Type                            | Who manages                                        | Typical use cases                                                                                 | Privileges                                                             | Creation / Deletion                                                    |
| ------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| User-managed service accounts   | You (project admins/dev teams)                     | Custom applications, ETL pipelines, CI/CD, VM workloads — any workload identity you control       | You define roles and permissions; best for least-privilege enforcement | Created and deleted by your team (manual or IaC)                       |
| Default service accounts        | Auto-created by GCP when certain services are used | Used by Google Cloud services that need a service identity (e.g., Compute Engine default account) | Often granted broad permissions by default — can be overprivileged     | Created automatically; deleting may break services that depend on them |
| Google-managed service accounts | Fully managed by Google                            | Internal support for Google-managed services (e.g., App Engine internal accounts)                 | Permissions are fixed by Google and not configurable by project admins | Creation and deletion controlled by Google                             |

<Frame>
  <img alt="A slide titled &#x22;Comparing Service Account Types&#x22; showing a table that compares User‑Managed, Default, and Google‑Managed service accounts across characteristics like management, use cases, privilege, and creation/deletion. A short certification tip appears at the bottom." />
</Frame>

Certification tip: Know which service account type to use for each scenario and which supports least privilege. Always ask: does this workload need broad roles like `Editor`, or can you grant a narrowly scoped role?

<Callout icon="lightbulb">
  Prefer user-managed service accounts for workloads. They provide ownership and let you grant only required permissions (least privilege).
</Callout>

## Recommended production practices

Follow these practices to maintain good IAM hygiene and reduce risk:

| Best practice                                                     | Why it matters                                                                     |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Use user-managed service accounts per workload                    | Easier auditing, clearer ownership, and tighter permission scoping                 |
| Disable automatic default service account creation where feasible | Prevents unexpected over-privileged accounts and forces explicit identity creation |
| Grant the minimal permissions required                            | Limits blast radius from bugs or compromise (principle of least privilege)         |
| Use structured naming and ownership                               | One account per app/environment simplifies incident response and audits            |
| Enable audit logs and monitoring                                  | Detect and attribute automated activity; correlate Cloud Audit Logs and app logs   |

Additional operational tips:

* Rotate credentials and keys for any service account keys you create.
* Prefer Workload Identity Federation or short-lived tokens over long-lived service account keys where possible.
* Use IAM Conditions for more granular access (e.g., restrict by request time or resource attributes).

<Frame>
  <img alt="A presentation slide titled &#x22;Managing Service Accounts in Production&#x22; showing three colored arrows recommending: Use User-Managed Accounts, Disable Default Creation, and Understand Permissions. Each recommendation is briefly annotated (least privilege/better security, enforcing user-managed accounts, and preventing over-permissive access)." />
</Frame>

<Callout icon="warning">
  Do NOT reuse a single service account across unrelated services or environments. Reuse increases the blast radius of a compromise and makes it hard to determine which workload performed an action.
</Callout>

## Summary

* Service accounts are non-human identities used by applications and services to call Google Cloud APIs.
* Prefer user-managed service accounts for production workloads and enforce least-privilege permissions.
* Avoid default account reuse, create explicit service identities with clear ownership, and monitor their activity.

## Links and references

* [Cloud IAM overview — Google Cloud](https://cloud.google.com/iam)
* [Understand service accounts — Google Cloud](https://cloud.google.com/iam/docs/service-accounts)
* [Principle of least privilege — Google Cloud security guidance](https://cloud.google.com/architecture/security-design-principles#least_privilege)

That is it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/49028fb3-a958-472e-b8e3-cb2ab831d5a3" />
</CardGroup>
