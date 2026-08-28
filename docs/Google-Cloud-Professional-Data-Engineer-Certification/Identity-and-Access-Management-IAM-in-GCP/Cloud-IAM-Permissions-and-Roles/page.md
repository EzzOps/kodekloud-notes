# Cloud IAM Permissions and Roles

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Cloud-IAM-Permissions-and-Roles/page

Explains Google Cloud IAM permissions, roles, policy structure, best practices and tooling to enforce least privilege across BigQuery, Cloud Storage, Compute Engine and other resources.

Hello and welcome back.

Cloud IAM and the principle of least privilege — the idea that identities should have only the access they truly need — are foundational to secure Google Cloud operations. This lesson goes deeper into IAM permissions and roles to answer the core question: who can do what on which resource?

Understanding these concepts is critical for data engineers and cloud operators because they determine how securely you interact with BigQuery datasets and tables, Cloud Storage buckets and objects, Compute Engine instances, and other Google Cloud resources.

## Permissions

Permissions are the atomic unit of access control in IAM. A permission authorizes a specific action on a resource type. Examples:

* `bigquery.tables.get` — read metadata for a BigQuery table
* `bigquery.tables.update` — modify a table
* `storage.objects.create` — upload an object to a Cloud Storage bucket
* `compute.instances.start` — start a Compute Engine VM

Permissions follow a structured naming scheme: `service.resource.action` (or `service.action`). Note that you cannot grant individual permissions directly to a member; you grant roles that bundle permissions.

## Roles

A role is a collection of permissions. When you bind a role to a member on a resource, that member receives every permission included in the role.

| Role type         | What it is                                             | When to use (examples)                                                                                                          |
| ----------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Primitive (basic) | Broad legacy roles                                     | `roles/owner`, `roles/editor`, `roles/viewer`. Avoid for fine-grained access.                                                   |
| Predefined        | Curated by Google per product                          | `roles/bigquery.dataViewer`, `roles/storage.objectAdmin`. Prefer these for common workflows.                                    |
| Custom            | Organization/project-defined with specific permissions | Use when predefined roles are too broad; e.g., a custom ETL role containing `bigquery.tables.get` and `bigquery.tables.update`. |

Best practices:

* Prefer predefined roles over primitive roles.
* Use custom roles only when predefined roles do not meet your needs.
* Apply the principle of least privilege: grant the minimum set of permissions required, and scope them as narrowly as possible.

## IAM Policy Structure

Permissions are granted through IAM policies attached to resources. A policy is a collection of bindings. Each binding associates a role to one or more members and can include an optional condition.

Example policy (JSON):

```json theme={null}
{
  "bindings": [
    {
      "role": "roles/storage.objectViewer",
      "members": [
        "user:alice@example.com"
      ]
    },
    {
      "role": "roles/bigquery.dataEditor",
      "members": [
        "serviceAccount:etl-sa@my-project.iam.gserviceaccount.com"
      ]
    }
  ],
  "etag": "BwWWja0YfJA=",
  "version": 3
}
```

Key fields:

* `role`: the role being granted (e.g., `roles/storage.objectViewer`).
* `members`: identities receiving the role, e.g., `user:`, `group:`, `serviceAccount:`, `domain:`.
* `condition` (optional): an expression to restrict when or how the role applies (by time, resource, or request attributes).

## Common gcloud Commands

Use gcloud to inspect and modify policies, describe roles, and create custom roles.

| Purpose                                  | Command                                                                                                                                                                                                                | Notes                                        |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Get the IAM policy for a project         | `gcloud projects get-iam-policy PROJECT_ID`                                                                                                                                                                            | Replace `PROJECT_ID`.                        |
| Add a binding to a project's IAM policy  | `gcloud projects add-iam-policy-binding PROJECT_ID --member='user:alice@example.com' --role='roles/storage.objectViewer'`                                                                                              | Adds a role binding for a user.              |
| Describe a predefined role's permissions | `gcloud iam roles describe roles/bigquery.dataViewer --format="yaml(includedPermissions)"`                                                                                                                             | Shows included permissions.                  |
| Create a project-scoped custom role      | `gcloud iam roles create myCustomRole --project=PROJECT_ID --title="My Custom Role" --description="Custom role for ETL tasks" --permissions=bigquery.tables.get,bigquery.tables.update,storage.objects.get --stage=GA` | Replace `PROJECT_ID` and adjust permissions. |

Use the Policy Troubleshooter and IAM Policy Simulator in the Cloud Console to validate whether a member has a specific permission on a resource.

<Callout icon="lightbulb">
  Always follow the principle of least privilege: grant only the roles and permissions required. Prefer predefined roles for common tasks, and create custom roles only when necessary.
</Callout>

## How Permissions Map to Resources

Roles can be granted at different resource levels. Permissions granted at a higher level are inherited by resources under that scope.

| Scope                            | What it affects                                | Typical use cases                                             |
| -------------------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| Organization                     | All projects and resources in the organization | Broad administrative roles for security or compliance teams   |
| Folder                           | Projects under the folder                      | Cross-project teams grouped by department                     |
| Project                          | All resources in the project                   | Standard practice for most application workloads              |
| Resource (e.g., bucket, dataset) | Only the specific resource                     | Tightest-scoped access for specific buckets, datasets, or VMs |

Examples:

* Granting `roles/bigquery.dataViewer` at the project level allows viewing datasets and tables across that project.
* Granting `roles/storage.objectAdmin` on a specific bucket allows full object management only for that bucket.

## Example: BigQuery and Cloud Storage Patterns

* Analyst who needs read-only access across datasets: grant `roles/bigquery.dataViewer` at the project or dataset level.
* ETL service account that loads data into BigQuery and writes to Cloud Storage: grant a combination such as `roles/bigquery.dataEditor` (or a narrower custom role) plus `roles/storage.objectCreator` on the target bucket(s).
* When cross-project access is required, consider granting roles at the project level of the target project (not the source) or using IAM service account impersonation with limited roles.

## Troubleshooting and Validation

* Use the Policy Troubleshooter to answer "Does member X have permission Y on resource Z?" in the console.
* Use the IAM Policy Analyzer / Simulator to test changes before applying custom roles or complex conditional bindings.
* When debugging access errors, check:
  * The effective permissions (including inherited roles).
  * Whether a deny policy exists that overrides allow bindings.
  * Any IAM conditions that might restrict access by time or attributes.

## Summary

* Permissions (e.g., `bigquery.tables.get`) are the atomic units of authorization.
* Roles are collections of permissions that are granted to members.
* Use predefined roles where possible; create custom roles only when needed.
* Scope roles at the narrowest resource level that still supports your workflow, and leverage IAM conditions for finer control.
* Use gcloud and Console tools (Policy Troubleshooter, IAM Simulator) to inspect, validate, and test policies.

## Links and References

* [IAM Overview — Google Cloud](https://cloud.google.com/iam/docs)
* [IAM Roles — Google Cloud](https://cloud.google.com/iam/docs/understanding-roles)
* [BigQuery Access Control](https://cloud.google.com/bigquery/docs/access-control)
* [Cloud Storage IAM](https://cloud.google.com/storage/docs/access-control/iam)
* [gcloud reference — projects](https://cloud.google.com/sdk/gcloud/reference/projects)

This lesson covers the core IAM concepts you need to manage access securely across Google Cloud services. Apply these patterns to your BigQuery, Cloud Storage, and Compute Engine workflows for secure, least-privilege access.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/9a31792f-a30f-4dfa-bf98-6a21b8769afc" />
</CardGroup>
