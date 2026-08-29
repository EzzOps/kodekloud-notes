# Environment Separation in Azure

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Context-for-Terraform/Environment-Separation-in-Azure/page

Guidance on separating Azure environments when using Terraform by isolating state, backends, subscriptions, resource groups and pipelines to prevent accidental cross-environment changes and limit blast radius.

Environment separation in Azure is a critical architectural decision that prevents accidental cross-environment changes, reduces blast radius, and enforces correct ownership. Terraform itself is context-blind: it only understands configuration files, providers, backends, and state. Terms like "development", "test", or "production" are human labels — Terraform treats resources according to the state and backend you point it at.

If two environments use the same backend and the same state file, Terraform will treat them as the same environment no matter what you call them. Proper environment separation must be implemented using Azure constructs (subscriptions, resource groups, storage accounts, etc.) and by designing Terraform state and execution contexts correctly.

Terraform is context-blind. Use isolation to control ownership and blast radius.

<Callout icon="lightbulb">
  Terraform’s state file is the source of truth and therefore represents ownership. Proper isolation of state and execution context prevents accidental cross-environment changes.
</Callout>

## Core strategies for environment separation

Below are the practical, production-ready methods to achieve environment separation in Azure with Terraform. These reduce the chance of destructive mistakes and make CI/CD safe and auditable.

1. Separate state files

* A Terraform state file represents the authoritative view of a set of resources. If two environments share one state file, they share ownership.
* Use one state file per environment so Terraform tracks resources independently. This prevents accidental updates, deletes, or drift across environments.
* Separate state files are the foundational step for logical separation.

2. Configure separate backends

<Frame>
  <img alt="The image is a diagram explaining environment separation in Terraform, highlighting two methods: using separate Terraform state files and configuring separate backends." />
</Frame>

* Isolate backends by using separate storage accounts, containers, or distinct state keys (object names) per environment.
* Ensure state locking and concurrency control are scoped to each environment. Shared backends can lead to one environment locking or overwriting another environment’s state.
* Azure remote backends (e.g., Azure Storage with state locking via Cosmos/Blob leases) should be configured per environment to avoid cross-environment interference.

3. Run Terraform from separate workflows/pipelines

* Execution context matters as much as state. Each environment should have its own CI/CD pipeline, credentials, and approval flow.
* Treat pipelines as security and governance boundaries: production pipelines typically require stricter approvals and more restrictive service principals or managed identities.
* Keep non-production pipelines faster and more flexible but still isolated to prevent accidental promotion of changes across environments.

## Azure isolation primitives: subscriptions and resource groups

Azure enforces isolation mainly using subscriptions and resource groups. Use them deliberately to align with organizational ownership, billing, and lifecycle requirements.

* Subscriptions: outer boundary for billing, RBAC, policies, quotas, and limits.
* Resource groups: define lifecycle boundaries — resources that are created, updated, or deleted together.

<Frame>
  <img alt="The image illustrates &#x22;Environment Separation and Terraform State,&#x22; showing how subscriptions and resource groups contribute to enforcing isolation in a technical context." />
</Frame>

Use resource groups and subscriptions intentionally; Terraform will not protect you from misusing them. If you put multiple environments in the same subscription or reuse resource groups inappropriately, Terraform will faithfully apply your configuration — including destructive changes.

## How Terraform evaluates infrastructure changes

Terraform calculates a plan by comparing three sources:

* The current Terraform state file (what Terraform thinks exists).
* The desired configuration (your .tf files).
* The actual resources and lifecycle rules in Azure.

<Frame>
  <img alt="The image explains how Terraform evaluates infrastructure changes by considering the current state and Azure's resource hierarchy and lifecycle rules to achieve the desired configuration." />
</Frame>

If any part of the context is wrong — wrong subscription, wrong resource group, or wrong state — the plan may look valid but will not produce the intended outcome. Misaligned assumptions commonly lead to unexpected destroys or failed plans. Azure also enforces cascading deletes: deleting a resource group deletes everything inside it regardless of Terraform’s intent.

## Risks: unexpected destroys, hard rollbacks, and loss of data

Terraform is not a backup system. Once Azure has destroyed a resource or data, Terraform cannot restore it unless you have external backups or recovery procedures. Rollbacks after destructive changes can be complex or impossible without separate backups or state snapshots.

<Frame>
  <img alt="The image explains the importance of understanding context in Terraform projects, highlighting risks like unexpected destroys, difficult rollbacks, and failed plans due to misaligned assumptions about Azure constructs." />
</Frame>

<Callout icon="warning">
  Terraform will apply the actions it calculates based on state and configuration. If the context is wrong, those actions may be destructive and irreversible without backups.
</Callout>

## Recommended patterns and examples

Below are recommended patterns for different levels of isolation. Choose the pattern that matches your organization’s governance, risk tolerance, and team ownership model.

| Pattern                                        | Isolation scope                            | Use case                                                                                  |
| ---------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| One subscription per environment               | Subscription-level isolation               | Suitable for strict separation: billing, policies, quotas are separated for dev/test/prod |
| Multiple subscriptions, per team + environment | Subscription + resource group segmentation | Good for larger orgs where teams manage environments independently                        |
| Single subscription, multiple resource groups  | Resource-group-level isolation             | Simpler setups or small teams; use strict RBAC and state separation to mitigate risk      |
| Backend per environment                        | Isolate state storage and locking          | Use separate storage account/container or distinct state keys for each environment        |

Operational recommendations

* Use distinct service principals or managed identities for each environment with least privilege.
* Use separate backend configurations per environment and distinct state keys.
* Implement pipeline approvals for production and audit logging for state changes.
* Back up your Terraform state (and Azure data) regularly. Consider automated snapshots for critical resources.

## Benefits of correct environment separation

When context and isolation are implemented correctly:

* Plans become predictable — you can trust that the plan targets the intended environment.
* Changes are safer — the blast radius is limited to a single environment.
* Teams can refactor and evolve infrastructure independently, reducing technical debt and enabling safer migrations.

<Frame>
  <img alt="The image is an infographic discussing why context matters in Terraform projects, highlighting benefits such as predictable execution, safer changes, and cleaner infrastructure evolution." />
</Frame>

## Key takeaway

Terraform is powerful but context-blind. It will do exactly what your configuration and state tell it to do. Enforce environment separation with Azure primitives (subscriptions, resource groups), isolated backends, distinct pipelines, and least-privilege credentials. When those boundaries are correct, Terraform is predictable and safe; when they’re not, Terraform can quickly make mistakes irreversible.

Following this conceptual grounding, the next step is to transition to practical examples and start writing real Terraform modules and backend configurations for each environment.

## Links and references

* [Azure subscriptions and management groups](https://learn.microsoft.com/azure/overview-what-is-azure)
* [Terraform remote state](https://www.terraform.io/language/state/remote)
* [Terraform backend configuration for Azure](https://www.terraform.io/language/settings/backends/azurerm)
* [Azure RBAC documentation](https://learn.microsoft.com/azure/role-based-access-control/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/7fc76e5f-e1e7-4c53-8940-57761020744e/lesson/92193847-5b93-4c3f-abcb-11ca45bb93e1" />
</CardGroup>
