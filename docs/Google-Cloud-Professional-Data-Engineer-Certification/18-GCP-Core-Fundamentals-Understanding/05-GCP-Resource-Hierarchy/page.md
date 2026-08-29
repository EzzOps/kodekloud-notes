# GCP Resource Hierarchy

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Core-Fundamentals-Understanding/GCP-Resource-Hierarchy/page

Explains Google Cloud's resource hierarchy and how organization, folders, projects, and resources determine IAM, policies, inheritance, and billing for centralized governance.

Welcome back.

In this lesson we cover an essential concept every Google Cloud engineer should master: the GCP resource hierarchy. Understanding this hierarchy is key to applying consistent access control, governance, and billing across your organization.

## Why this matters

* The resource hierarchy defines how Google Cloud organizes everything from your entire organization down to individual resources like VMs and buckets.
* It determines how IAM, organization policies, and billing are applied and inherited across your cloud estate.
* If you manage projects inside an organization, each project is a node in this hierarchy. Knowing the structure helps you standardize permissions, enforce policies, and simplify auditing.

## Overview: the layers of the hierarchy

1. Organization node

   * The organization node is the root for your company inside Google Cloud. It typically represents your domain (for example, `kodekloud.com`) and requires Cloud Identity or Google Workspace to be established.
   * Policies and IAM bindings applied at the organization level affect every child below it—folders, projects, and resources—making it the highest point for central enforcement.

   > **lightbulb** The organization node is created when you set up Cloud Identity or Google Workspace for your domain. Without it, projects are created without a shared organizational root.

2. Folders
   * Folders are optional grouping containers that help you structure projects and subfolders. Use folders to represent departments, environments (e.g., dev, staging, prod), or business units.
   * They simplify applying consistent IAM and organization policies across many projects without configuring each project individually.

3. Projects
   * Projects are the primary boundary for resources, billing, APIs, and IAM. Every Google Cloud resource belongs to a project.
   * A project contains configuration, quota, enabled APIs, and a link to a billing account. Teams typically own projects to isolate environments and responsibilities. (Billing accounts are separate resources that can be attached to multiple projects.)

4. Resources
   * Resources are concrete services and objects such as Compute Engine VMs, Cloud Storage buckets, BigQuery datasets, Pub/Sub topics, etc.
   * Resources live inside projects and inherit policies and IAM bindings from their parent project, folder (if any), and organization node.

## Inheritance and scope

* Permissions and organization policies flow downward: a policy set at the organization node applies to folders, projects, and all resources beneath it.
* You can add more specific IAM bindings or policies at lower levels (folders, projects, or individual resources). The effective permissions for an identity are the union of all applicable bindings across the hierarchy.
* Organization Policy constraints let you restrict resource creation and configuration across the organization (for example, limiting regions, disallowing external IPs, or blocking certain APIs).

> **warning** Be careful when assigning broad roles at high levels (organization or folder). A single overly-permissive binding can grant access across many projects and resources. Prefer least privilege and use predefined/custom IAM roles where possible.

## Quick mental model

* Organization node → Folders (optional) → Projects → Resources
* Each layer can have many children and inherits controls from its parent. This enables centralized management while allowing targeted exceptions or additional controls at lower levels.

## Summary table

| Layer             | Purpose                                            | Typical examples / use                                             |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| Organization node | Top-level administrative root for a company domain | Central IAM, org policies, billing linkage                         |
| Folders           | Optional groupings for logical structure           | Departments, environments (dev/prod), business units               |
| Projects          | Boundary for resources, APIs, quotas, and billing  | Team-owned environments, application stacks                        |
| Resources         | Concrete cloud services and objects                | `Compute Engine` VMs, `Cloud Storage` buckets, `BigQuery` datasets |

## Next steps

A related topic is the project identification framework: naming conventions, labels, and tags to manage projects efficiently within this hierarchy. Consider documenting a naming and labeling standard (for example: `proj-<team>-<app>-<env>`) and enforcing it with organization policies and automation.

## Links and references

* [GCP Resource hierarchy](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
* [Organizations resource](https://cloud.google.com/resource-manager/docs/organizations)
* [IAM concepts](https://cloud.google.com/iam/docs/overview)
* [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

<Frame>
  <img alt="A slide titled &#x22;GCP Resource Hierarchy&#x22; showing a colorful four-level stacked diagram and labels describing Organization Node, Folders, Projects, and Resources with brief explanations of each." />
</Frame>

That is it for this lesson. Speak with you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/54d4f17c-56da-41a4-b998-2a2c63f0ee3f/lesson/2e747fa7-6cab-4637-a4c1-3fdde02dd1f1)
