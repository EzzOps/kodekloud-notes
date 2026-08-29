# Cloud IAM Role Type Details

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Cloud-IAM-Role-Type-Details/page

Explains Google Cloud IAM role types—basic, predefined, and custom—and best practices for granting least privilege to reduce blast radius and manage permissions

Hello and welcome back.

In this lesson we continue our Google Cloud IAM deep dive and focus on IAM role types: basic (primitive), predefined (service) roles, and custom roles. Understanding these will help you grant the right permissions, reduce blast radius, and apply the principle of least privilege.

To ground this, imagine granting a "VM instance editor" capability to an operator who manages Compute Engine instances. That capability is represented by an IAM role — a collection of permissions — and every Google Cloud role belongs to one of three categories described below.

## Overview: role assignment and permissions

An IAM role is a named collection of permissions you grant to a principal (user, group, or service account) on a resource. Roles are attached to policy bindings and evaluated at request time to authorize actions.

Key distinctions between role types:

* Basic (primitive) roles: Owner, Editor, Viewer — very broad and apply across a project, folder, or organization.
* Predefined roles: Service-specific, finer-grained roles provided and maintained by Google Cloud.
* Custom roles: User-defined roles that combine explicit permissions to meet organizational requirements.

Why role choice matters:

* Granting overly broad roles increases blast radius when credentials are compromised.
* Apply least privilege: grant only the permissions required for the job.

> **warning** Avoid using basic (Owner/Editor/Viewer) roles in production. They grant broad access across resources and increase risk. Prefer predefined or custom roles tailored to the task.

***

## Quick comparison

| Role type            | Scope                         | Typical use cases                                    | Examples                                                       |
| -------------------- | ----------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| Basic (primitive)    | Project, folder, organization | Quick experiments, short-lived test projects         | `roles/owner`, `roles/editor`, `roles/viewer`                  |
| Predefined (service) | Project, folder, organization | Production access to a specific Google Cloud service | `roles/compute.instanceAdmin.v1`, `roles/storage.objectViewer` |
| Custom               | Project or Organization level | Fine-grained, organization-specific permission sets  | `projects/PROJECT_ID/roles/CustomInstanceOperator`             |

***

## 1) Basic (primitive) roles

Basic roles are coarse-grained and classic:

* Owner (`roles/owner`)
* Editor (`roles/editor`)
* Viewer (`roles/viewer`)

Pros:

* Simple to assign and understand.

Cons:

* Extremely broad; often grant more permissions than necessary.
* Not recommended for production environments due to elevated risk.

Use cases:

* Quick experimentation, learning labs, or non-production short-lived projects.

Inspecting who has basic roles on a project:

```bash theme={null}
