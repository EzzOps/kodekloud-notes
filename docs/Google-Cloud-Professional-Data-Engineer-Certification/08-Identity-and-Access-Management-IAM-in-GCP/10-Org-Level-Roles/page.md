# Org Level Roles

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Org-Level-Roles/page

Explains Google Cloud organization-level IAM roles, inheritance across org folder project, and guidance on Viewer Editor Owner permissions and least privilege

Hello and welcome back.

In this lesson we’ll cover organization-level IAM roles in Google Cloud — a foundational part of access management for companies and large teams. Organization-level roles let you control who can view, modify, or administer resources across your entire Google Cloud organization. We’ll review the Google Cloud resource hierarchy, explain how IAM inheritance works, and describe the three basic predefined roles — Viewer, Editor, and Owner — including guidance on when and where to assign them.

For more details, see the Google Cloud documentation on [Understanding roles](https://cloud.google.com/iam/docs/understanding-roles) and [Resource hierarchy](https://cloud.google.com/resource-manager/docs/organization-resource).

## Organization hierarchy

At the top of the Google Cloud resource hierarchy sits the organization node. This is the root for all your resources and the most common place to apply organization-wide policies, IAM bindings, and identity management.

Beneath the organization node you can create folders to logically group related projects. For example:

* Marketing
* Data Engineering
* Finance

Folders make it easy to apply the same permissions or policies across multiple projects at once.

Projects live under folders (or directly under the organization) and contain actual cloud resources — Compute Engine VMs, BigQuery datasets, Cloud Storage buckets, Cloud Functions, etc.

Because IAM bindings inherit downward, any permissions granted at a higher level automatically apply to the nodes below.

<Callout icon="lightbulb">
  The organization node is the most powerful scope. Apply permissions there only when you want the role to affect every folder, project, and resource in the organization.
</Callout>

## How IAM inheritance works

* Organization-level bindings apply to all folders, projects, and resources under that organization node.
* Folder-level bindings apply to projects and resources contained in that folder.
* Project-level bindings apply only to resources inside that project.

Always verify the scope (organization, folder, or project) before assigning a role — granting a role at a higher level increases the effective scope of that role.

| Scope        |                           Applies to | Typical use                                                 |
| ------------ | -----------------------------------: | ----------------------------------------------------------- |
| Organization | All folders, projects, and resources | Global policies, org-wide auditors, central admins          |
| Folder       | Projects and resources in the folder | Departmental teams, shared infrastructure groups            |
| Project      |        Resources in the project only | Application owners, CI/CD pipelines, project-specific roles |

## Org-level roles: Viewer, Editor, Owner

There are three primitive predefined roles in Google Cloud that are commonly used at the organization level. They grant increasing levels of access:

* Viewer
  * Read-only access to view resources and configuration.
  * Useful for monitoring logs, reviewing configurations, or auditing usage.
  * Cannot make changes or modify configuration.

* Editor
  * Can create, modify, and delete resources (Compute Engine, BigQuery, Cloud Storage, Cloud Functions, etc.).
  * Cannot manage IAM policies (cannot grant or revoke roles).

* Owner
  * Full administrative control, including the ability to manage IAM.
  * Can grant/revoke roles, invite/remove principals, and delete projects and resources.

When assigning these roles, always ask: "At what level am I applying this role?" For example, a user with Owner at the organization level has full control across all projects and folders within the organization.

| Role   |                     Typical permissions | When to use                                               |
| ------ | --------------------------------------: | --------------------------------------------------------- |
| Viewer |              Read-only across the scope | Reporters, auditors, non-admin stakeholders               |
| Editor | Modify/create/delete resources (no IAM) | Developers, operators who manage resources but not IAM    |
| Owner  | All Editor permissions + IAM management | Trusted administrators who manage org policies and access |

<Frame>
  <img alt="A slide titled &#x22;Org-Level Roles&#x22; showing three GCP IAM roles — Viewer, Editor, and Owner — with icons and checkmarks indicating increasing permissions from read-only to full control. A caption notes these roles apply at the organization node across all projects, folders, and resources." />
</Frame>

## Practical guidance

* Follow least privilege: grant the most restrictive role that still allows the user to perform their tasks.
* Prefer assigning roles at the project or folder level rather than the organization level to reduce blast radius.
* Limit organization-level Owner assignments to a very small group of trusted administrators.
* Use predefined and custom roles appropriately — predefined primitive roles are broad; consider fine-grained predefined or custom roles for production use.

<Callout icon="warning">
  Be careful granting Owner at the organization level — that role can change IAM policies across the entire organization, including deleting projects and revoking other admins.
</Callout>

## Summary

Organization-level roles in GCP are IAM roles applied at the organization node and cascade down to folders, projects, and resources. Viewer provides read-only access, Editor allows resource changes but not IAM management, and Owner has full control including IAM. Always verify the assignment scope and follow least-privilege principles to keep your environment secure.

End of lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/6163aa95-39c6-4611-b5cd-524f41e32b22" />
</CardGroup>
