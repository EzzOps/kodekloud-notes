# Understanding Variable Scope in Modules

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Modules/Understanding-Variable-Scope-in-Modules/page

Explains Terraform module variable scoping, how to pass inputs to child modules, expose outputs to callers, and manage defaults for reusable, isolated modules.

Variable scope in Terraform modules is a common stumbling block for beginners. Once you understand how variables are scoped and passed between modules, working with reusable modules becomes predictable and safe. This guide covers the essentials — how variables are declared, how to pass values into child modules, and how to expose values back to the caller. If you're preparing for the [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004) exam, this topic frequently appears on practice questions.

Overview of the setup

* The root (parent) module is the top-level configuration that invokes other modules.
* A child module is a reusable unit of configuration — for example, a networking module or a compute module.
* Typical module files:
  * `main.tf` — resources and module invocations
  * `variables.tf` — input variable declarations
  * `outputs.tf` — exported values for callers

What "module scope" means

* Each module has its own variable namespace (scope).
* Variables declared in one module are not visible to other modules unless explicitly passed or exported as outputs.
* This isolation makes modules more reusable and less prone to accidental coupling.

Variables are defined per-module

Below is an example where the root module defines its own variables and the child module defines different variables. These definitions are independent; naming collisions do not create implicit connections.

```hcl theme={null}
