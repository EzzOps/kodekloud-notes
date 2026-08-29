# Cloud IAM Introduction

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Cloud-IAM-Introduction/page

Introduction to Google Cloud IAM explaining identities, roles, policies, least privilege best practices, service accounts, policy inheritance, auditing, and permission troubleshooting

Welcome — in this lesson you'll learn the fundamentals of Cloud IAM (Identity and Access Management) in Google Cloud.

Every cloud environment needs a consistent way to decide who can do what and where. Google Cloud IAM provides that control: it verifies identities, evaluates their permissions (roles), and enforces which resources those permissions apply to. This three-part model (identity, role/permission, resource) is central to secure cloud operations.

* Identity — who is making the request: users, groups, or service accounts.
* Role — what actions that identity can perform: a collection of permissions.
* Resource — which Google Cloud resource the role applies to: projects, buckets, datasets, VMs, etc.

<Frame>
  <img alt="A three-column diagram titled &#x22;Cloud IAM – Introduction&#x22; showing Identity (users, groups, service accounts), Role (viewer, editor, admin, custom roles) and Resource (compute, storage, network, projects). It illustrates that Google Cloud IAM controls who (identity) can do what (role/permission) on which resource." />
</Frame>

Always ask: why does this identity need the permission? That question drives secure designs and helps you grant the minimal access required.

## Key IAM elements

1. Identities

* Users: individual people with Google accounts.
* Groups: logical collections of users that simplify team-level access management.
* Service accounts: machine identities for applications, VMs, CI/CD pipelines, or workloads that act programmatically.

2. Roles
   Roles are collections of permissions. Google Cloud provides three role types:

| Role type         | Scope & use case                                              | Example                                       |
| ----------------- | ------------------------------------------------------------- | --------------------------------------------- |
| Basic (primitive) | Broad, project-wide; not recommended for fine-grained control | `roles/owner`, `roles/editor`, `roles/viewer` |
| Predefined        | Service-specific, fine-grained permissions for common tasks   | `roles/bigquery.dataViewer`                   |
| Custom            | You define an exact permission set for least-privilege access | Create with a tailored set of permissions     |

Use the principle of least privilege: grant only the permissions required for a task. Prefer predefined or custom roles over broad basic roles.

3. Policies
   An IAM policy binds one or more identities (members) to roles on a resource. Policies are attached to resources in the Google Cloud resource hierarchy:

organization → folder → project → resource

Policies are additive and inherited down the hierarchy; a role granted at the project level applies to all resources in that project unless overridden.

A minimal IAM policy (JSON) that grants a user the Viewer role on a project:

```json theme={null}
{
  "bindings": [
    {
      "role": "roles/viewer",
      "members": [
        "user:alice@example.com"
      ]
    }
  ]
}
```

* `bindings` is a list of  entries.
* `role` is the IAM role identifier.
* `members` lists identities in the form `user:`, `group:`, `serviceAccount:`, or `domain:`.

You can apply the same binding with gcloud:

```bash theme={null}
gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="user:alice@example.com" \
  --role="roles/viewer"
```

## Why IAM matters for data engineers

IAM regulates every read/write action on datasets, start/stop operations on Compute Engine instances, and deployments of workflows like Dataflow or Dataproc. When you see a "permission denied" error, check these components:

* Identity: is the caller (user or service account) the expected identity?
* Role: does the role assigned include the specific permission required?
* Policy/resource: is the policy attached at the correct level (project vs. resource) or inherited as expected?

Troubleshooting checklist:

* Validate the caller identity (audit logs or `whoami` behavior).
* Inspect the effective permissions using IAM Recommender or `gcloud iam roles describe`.
* Confirm policy inheritance and overrides at organization/folder/project/resource levels.

<Callout icon="lightbulb">
  Always apply the principle of least privilege: grant the minimal roles required, prefer predefined or custom roles over broad basic roles, and manage access with groups and service accounts to keep policies consistent and auditable.
</Callout>

## Practical tips and next steps

* Use groups to manage team access and avoid per-user bindings.
* Use service accounts for non-human access; rotate keys and use workload identity when possible.
* Audit IAM changes with Cloud Audit Logs and use IAM Recommender to identify overly broad permissions.
* Consider automation (Terraform, Deployment Manager) to enforce consistent IAM policies across environments.

## Links and references

* [Google Cloud IAM overview](https://cloud.google.com/iam/docs/overview)
* [IAM best practices](https://cloud.google.com/iam/docs/best-practices)
* [Roles and permissions documentation](https://cloud.google.com/iam/docs/understanding-roles)

This is a compact introduction to Google Cloud IAM — how Google Cloud decides who can do what on which resource. Explore applying least-privilege patterns, service-account management, and IAM auditing for secure and maintainable cloud access control.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/7a14d12b-0d02-459c-9702-a2b2c915600e" />
</CardGroup>
