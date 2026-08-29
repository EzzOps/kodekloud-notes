# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-State-Fundamentals/Introduction/page

Overview of Terraform state, covering its role in tracking resources, plan generation, drift detection, security, backends, and best practices for safe collaborative infrastructure management.

Welcome to this module on Terraform state fundamentals.

So far you've focused on writing clean, reusable Terraform code. In this lesson we’ll examine what powers Terraform behind the scenes: the state file. Understanding state helps you manage infrastructure reliably, collaborate safely, and troubleshoot unexpected changes.

This lesson covers four core areas:

* What Terraform state is and why it matters.
* How Terraform uses state to track resources, detect differences, and produce accurate execution plans.
* Security considerations for storing and sharing state.
* How Terraform refreshes state, detects drift, and how refreshed state affects planning and execution.

Terraform state is more than simple metadata. It is Terraform’s authoritative record for what exists in your environment. By persisting resource IDs, attributes, dependency relationships, and provider-specific details, state enables Terraform to:

* Map resources in your configuration to real-world objects.
* Compute diffs between the desired configuration and current reality.
* Generate a precise execution plan that performs only the necessary changes.

> **lightbulb** State is the authoritative record Terraform relies on to know which resources exist and how they relate. Losing or corrupting state can prevent Terraform from managing infrastructure correctly.

## Quick summary table

| Topic           | Purpose                                               | Key takeaway                                    |
| --------------- | ----------------------------------------------------- | ----------------------------------------------- |
| What is state   | Stores Terraform’s view of real infrastructure        | Source of truth for mapping config to resources |
| Plan & apply    | Uses state to compute diffs and build execution plans | Accurate plans require up-to-date state         |
| Security        | Protects sensitive data inside state                  | Encrypt at rest, restrict access, avoid VCS     |
| Refresh & drift | Detects out-of-band changes                           | Refreshing updates state and can change plans   |

## How Terraform uses state

Terraform keeps a serialized snapshot of the infrastructure it manages. That snapshot contains:

* Resource IDs and attributes needed by providers to reference cloud objects.
* Metadata for dependency graph resolution.
* Provider-specific information (for example, auto-generated names, ARNs, subresource IDs).

At plan time, Terraform compares the desired configuration to the state file (and the provider’s live API during refresh when necessary) to compute a set of operations: create, update, or delete. Because state contains identity and attribute values, Terraform can:

* Determine whether a resource already exists or must be created.
* Compute minimal updates instead of recreating resources unnecessarily.
* Maintain stable resource addresses across runs.

## Security considerations

State files often contain sensitive information such as resource identifiers, network details, and sometimes secrets or tokens. Treat state with the same care you apply to other secrets:

* Never commit state files to source control.
* Use remote backends (for example, S3 with DynamoDB locking, Azure Blob Storage, or Terraform Cloud/Enterprise) for team collaboration.
* Enable server-side encryption and backend-level access controls.
* Use state locking where supported to prevent concurrent modifications.

> **warning** Terraform state can contain secrets and credentials. Never commit state files to source control. Use remote backends with encryption and access controls for team or production use.

## Backends and collaboration (local vs remote)

Choosing the right backend affects collaboration, performance, and safety. Use remote backends for team or production workflows.

| Backend type                             | Use case                          | Notes                                                          |
| ---------------------------------------- | --------------------------------- | -------------------------------------------------------------- |
| Local                                    | Single-user, quick experiments    | State stored on local disk. Not suitable for teams.            |
| Remote (S3, GCS, Azure, Terraform Cloud) | Team workflows, CI/CD, production | Supports locking, encryption, and centralized state management |

Recommended reading:

* [Terraform State](https://www.terraform.io/docs/state) (Terraform docs)
* Backend-specific docs (AWS S3, Google Cloud Storage, Azure Blob, Terraform Cloud)

## Refresh, drift detection, and effects on planning

Terraform can refresh state by querying provider APIs to update the stored attributes before planning. Refresh behavior is central to understanding why plans change:

* Refresh updates state attributes to reflect the current live environment.
* If resources changed outside Terraform (drift), a refresh will reveal differences and update state accordingly.
* After refresh, Terraform re-evaluates diffs and may generate a different plan (for example, to reconcile drift or to make further intended changes).

Common workflow implications:

* Run `terraform plan` frequently in CI to detect drift early.
* Use `terraform refresh` or `terraform plan -refresh=true` when you suspect out-of-band changes.
* Review plan outputs carefully after refresh—some differences may require manual reconciliation or import.

## Best practices

* Use remote backends with locking and encryption for teams.
* Protect access to state storage with fine-grained IAM policies.
* Never store secrets in plain text within state; use secrets management integrations when possible.
* Regularly run plans in CI to detect drift.
* Use `terraform import` to bring unmanaged resources under Terraform control rather than editing state manually.
* Version your Terraform configurations and maintain a clear drift remediation policy.

## Links and references

* [Terraform: State](https://www.terraform.io/docs/state)
* [Terraform: Backends](https://www.terraform.io/docs/backends/index.html)
* [HashiCorp Best Practices for Terraform](https://www.hashicorp.com/best-practices)

This module gives you the conceptual foundation to manage Terraform state safely and predictably. Use the guidance above to design backends, secure state, and manage drift across environments.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/d0fef6dd-c271-403d-b4ac-ee1f20c1839b/lesson/62847658-1969-4115-94a8-0797313137b0)
