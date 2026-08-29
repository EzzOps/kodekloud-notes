# The DRY Principle

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Basic-Concepts/The-DRY-Principle/page

This article explains the DRY principle in Terragrunt for Terraform, focusing on modular configurations, variable abstraction, and hierarchical inheritance.

In Infrastructure as Code (IaC), the DRY (Don’t Repeat Yourself) principle is essential for creating modular, maintainable, and scalable configurations. Terragrunt extends Terraform by enforcing DRY across your codebase. In this guide, you’ll learn how to:

* Structure reusable modules to eliminate redundancy
* Centralize and abstract variables for consistency
* Inherit shared settings through a hierarchical layout
* Streamline maintenance and promote changes safely

<Callout icon="lightbulb">
  This article assumes basic familiarity with Terraform and HCL. For a Terraform refresher, see [Terraform Overview](https://www.terraform.io/intro).
</Callout>

***

## 1. Modular Configuration

By encapsulating common resources in Terragrunt modules, you define infrastructure blocks once and reuse them across environments. This approach reduces code duplication and speeds up delivery.

Example module call in your environment folder:

```hcl theme={null}
