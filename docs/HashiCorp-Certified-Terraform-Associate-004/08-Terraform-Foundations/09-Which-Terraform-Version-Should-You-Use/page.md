# Which Terraform Version Should You Use

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Which-Terraform-Version-Should-You-Use/page

Guide comparing Terraform CLI, Terraform Cloud, and Terraform Enterprise to help choose the right edition for learning, team collaboration, or enterprise governance.

Choosing the right Terraform edition depends on team size, collaboration needs, governance requirements, and whether you want HashiCorp to manage the service or host it yourself. This guide compares the three primary Terraform distributions and provides practical recommendations to help you select the best fit for learning, small teams, and enterprise deployments.

## Terraform Editions Overview

Terraform is available in three primary flavors:

* Terraform CLI (Open Source / Community)
* Terraform Cloud (HashiCorp’s SaaS)
* Terraform Enterprise (self-hosted)

Each edition builds on the core Terraform engine but targets different operational and organizational needs.

### Terraform CLI (Open Source / Community)

This is the free command-line client you install locally. It’s ideal for:

* Individual practitioners learning Infrastructure as Code
* Developers experimenting with infrastructure
* Small teams or ad-hoc automation where centralized collaboration and governance are not required

Most hands-on learning materials and examples assume the open-source Terraform CLI. It’s what you’ll run locally for authoring, planning, and applying infrastructure changes.

Key characteristics:

* Local execution of `terraform plan` and `terraform apply`
* Local state by default (can be backed by remote state backends)
* No built-in team collaboration features

### Terraform Cloud (HashiCorp’s SaaS)

Terraform Cloud extends the CLI with hosted collaboration, remote execution, and governance features. It’s well suited for teams that want managed services without operating additional infrastructure.

Notable features:

* Remote state management
* Remote runs (shared plan and apply workflows)
* Private module registry for sharing modules across teams
* Policy-as-code (e.g., Sentinel or OPA-based governance)
* Integrations with VCS providers for VCS-driven workflows

Think of Terraform Cloud as the Terraform CLI plus hosted collaboration and governance features. It’s a common choice for teams that want centralized state, consistent remote runs, and policy enforcement without self-managing the platform.

Recommended reading:

* HashiCorp Terraform Cloud: [https://www.hashicorp.com/products/terraform](https://www.hashicorp.com/products/terraform)

### Terraform Enterprise (Self-Managed)

Terraform Enterprise provides the same collaboration and governance capabilities as Terraform Cloud but is deployed and managed within your organization’s network or cloud account. Choose this when strict control, compliance, or isolation is required.

Typical enterprise features:

* Role-based access control (RBAC)
* Single sign-on (SSO) integrations
* Detailed audit logging
* Private networking and isolated deployment options
* Full administrative control over updates and infrastructure

Terraform Enterprise fits larger organizations that must host their Terraform platform internally for compliance, security, or organizational policy reasons. Functionally similar to Terraform Cloud, the primary difference is responsibility for hosting and operations.

## Quick Comparison

| Edition                     |                                   Best for | Key features                                                                | Management model                          |
| --------------------------- | -----------------------------------------: | --------------------------------------------------------------------------- | ----------------------------------------- |
| Terraform CLI (Open Source) |         Learners, individuals, small teams | Local execution, local state (or remote backend), no built-in collaboration | Community-managed client; you run locally |
| Terraform Cloud             | Small-to-large teams needing collaboration | Remote state, remote runs, private module registry, policy-as-code          | Hosted by HashiCorp (SaaS)                |
| Terraform Enterprise        |  Large orgs with strict control/compliance | RBAC, SSO, audit logging, private networking                                | Self-managed in your environment          |

## Guidance: Which to Use When

* Use Terraform CLI (Open Source) to learn Terraform, author configurations, and develop locally.
* Use Terraform Cloud when your team needs managed remote state, shared module registries, remote runs, and centralized policy enforcement without operating infrastructure.
* Use Terraform Enterprise when your organization requires complete control over the Terraform platform, including RBAC, audit logging, private networking, and self-hosted operations.

<Callout icon="lightbulb">
  For exam and course focus: Terraform Cloud (the SaaS offering) is covered as part of the [Terraform Associate Certification: HashiCorp Certified](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified) exam objectives (specifically the section on collaboration and governance). Terraform Enterprise is typically not emphasized on the [Terraform Associate Certification: HashiCorp Certified](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified) exam — most course content and exam items assume the open-source Terraform CLI or Terraform Cloud features.
</Callout>

## Additional resources

* HashiCorp Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* Terraform Cloud product pages and docs: [https://www.hashicorp.com/products/terraform](https://www.hashicorp.com/products/terraform)
* Terraform best practices and state management guides: [https://www.terraform.io/docs/state/index.html](https://www.terraform.io/docs/state/index.html)

Summary: Start with the open-source CLI to learn and prototype. Move to Terraform Cloud for team collaboration without operational overhead. Choose Terraform Enterprise when you must host and control the full platform inside your organization.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/5ea9d027-63c2-4873-b88d-c1df207f1649" />
</CardGroup>
