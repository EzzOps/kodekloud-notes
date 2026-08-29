# Self Hosted vs Terraform cloud

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Cloud/Self-Hosted-vs-Terraform-cloud/page

Comparing self-hosted Terraform and Terraform Cloud, outlining trade-offs, operational gaps, governance differences, and reasons for using self-hosted in this course.

This lesson compares running Terraform locally—commonly called self-hosted Terraform—with using [Terraform Cloud](https://www.terraform.io/cloud), the managed SaaS offering. The goal is not to declare one approach universally right or wrong, but to clarify trade-offs and explain why this course intentionally sets up a self-hosted environment so you can learn the underlying concepts.

## Key limitations of running Terraform locally

When Terraform runs from a developer laptop or a custom CI pipeline, many capabilities that [Terraform Cloud](https://www.terraform.io/cloud) provides out of the box must instead be implemented, operated, and maintained by your team. That transfers platform responsibilities to your organization.

Primary operational gaps to consider:

* State management and durability are manual. By default Terraform stores state locally; to share state you must configure and operate a remote backend such as `Azure Storage Account` or `AWS S3` (usually with `DynamoDB` for locking) or run a self-hosted state server. This adds operational overhead and increases the risk of misconfiguration and state corruption.
* No built-in collaboration model. There’s no native concept of shared workspaces, RBAC, or coordinated concurrent-run handling. Teams must enforce collaboration via processes, CI pipelines, and documentation.
* No native VCS-triggered workflows. Git-triggered plan/apply workflows, gated approvals, and rollbacks must be implemented with custom CI/CD systems.
* Additional integration work. Features like remote runs, shared variables, secure secret storage, and audit trails must be integrated or built.

These limitations don’t make local Terraform unusable, but they shift responsibility from a managed platform to your engineering and ops teams.

<Frame>
  <img alt="The image highlights the limitations of using Terraform locally, including lack of built-in remote state management, no team collaboration features, and absence of VCS-driven automation." />
</Frame>

## Governance, visibility, and operational features also differ

Beyond collaboration and state, local Terraform lacks many governance and visibility features typically provided by a managed platform. Adding them requires additional tooling or custom automation.

Common platform features absent from local setups:

* No built-in policy-as-code enforcement prior to apply. Policy checks (for example, enforcing tag rules, required approvals, or network restrictions) must be plugged in externally.
* No centralized run logs or unified UI. Plans, applies, and audit logs live across developers’ machines and CI systems, making troubleshooting and compliance reporting harder.
* No automatic cost estimation or continuous drift detection. You’ll need separate tools to estimate cost impacts of changes and to detect drift between code and live infrastructure.
* Limited secrets and credentials management unless integrated with secure stores and CI secrets management.

These capabilities can be implemented with third-party tools or bespoke automation, but they require additional design, operational effort, and maintenance.

<Frame>
  <img alt="The image outlines the limitations of using Terraform locally, highlighting issues like the lack of policy as code (Sentinel), no centralized run logs and UI, and no cost estimation or drift detection capabilities." />
</Frame>

> **lightbulb** This lesson intentionally uses a self-hosted Terraform setup so you can see how state, backends, locking, security controls, and CI integrations are designed and operated—concepts that are often abstracted away by SaaS platforms.

## Why we chose self-hosted for this course

Choosing a self-hosted approach in a learning environment helps you acquire practical skills that apply whether you later migrate to Terraform Cloud or stay self-hosted.

Reasons for using self-hosted Terraform here:

* Maximum learning exposure: You will configure backends, enable state locking, and troubleshoot state issues—skills that deepen your understanding of Terraform execution.
* Clearer integration visibility: You’ll build the CI/CD flows, secrets integrations, and policy enforcement points so you understand where and how platform features fit together.
* Applicability to restrictive environments: Organizations with regulatory, security, or data residency constraints often cannot use SaaS platforms. Self-hosted knowledge is essential for those cases.

## Quick comparison: Self-hosted vs Terraform Cloud

| Area                    | Self-hosted Terraform                                                                  | Terraform Cloud                              |
| ----------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------- |
| State management        | You configure and operate remote backends (e.g., `AWS S3 + DynamoDB`, `Azure Storage`) | Managed remote state with locking            |
| Policy enforcement      | Requires external tools or custom CI checks                                            | Built-in policy-as-code (e.g., Sentinel)     |
| Collaboration & RBAC    | Implemented via CI, VCS, and process                                                   | Native workspaces, RBAC, and access controls |
| Run orchestration       | Uses custom CI pipelines and runners                                                   | Built-in VCS-triggered runs and UI           |
| Logs & auditing         | Distributed across machines and CI systems                                             | Centralized runs, logs, and UI               |
| Cost estimation & drift | Requires third-party tools                                                             | Often included or easier to integrate        |

## Next steps

Now that you understand the trade-offs between [Terraform Cloud](https://www.terraform.io/cloud) and self-hosted Terraform—and why this lesson adopts a self-hosted path—proceed to the next module to start configuring a remote backend, enable state locking, and create your CI-driven plan/apply pipeline.

## Links and references

* [Terraform Cloud](https://www.terraform.io/cloud)
* [Terraform Backends](https://www.terraform.io/language/settings/backends)
* [Terraform State](https://www.terraform.io/language/state)
* [Terraform Sentinel (policy as code)](https://developer.hashicorp.com/sentinel)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ca386519-4725-417d-a46f-642d0a683a01/lesson/19de60fb-4742-4fab-8f5a-a8daae2abf36)
