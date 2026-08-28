# What is Terraform Module and why use it

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Modules/What-is-Terraform-Module-and-why-use-it/page

Explains Terraform modules as reusable folders of configuration, their core files, how to use them, and benefits like reuse, organization, scalability, and reduced operational risk.

Now we begin one of the most important concepts in Terraform: modules.

If you truly understand modules, you move from writing small Terraform scripts to engineering reusable infrastructure platforms. A module is simply a folder containing Terraform configuration files that define how to create infrastructure. That's the definition—simple. The power comes from how you use modules to standardize, reuse, and scale infrastructure.

## What is a Terraform module?

A module is a folder that defines *how* to create something. Note the emphasis on "how": a module is not limited to a single resource. It represents a logical unit of infrastructure—this could be a storage account, a virtual machine, or a full environment composed of many resources (Resource Group, VNet, Subnet, NSG, VM, etc.).

Think of a module as a recipe:

* Input variables = ingredients
* Resources = steps to prepare
* Outputs = the finished dish and what you serve

Using modules lets you avoid repeating the same 10–20 lines of Terraform every time you need the same building block. Instead, you call the module and pass different inputs (names, SKUs, locations, tags), while the module encapsulates the creation logic.

## Core files inside a module

A typical Terraform module contains these primary files:

| File           | Purpose                                                                                   | Example contents                                                          |
| -------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `main.tf`      | Resource definitions — the logic that creates infrastructure (storage account, VM, VNet). | Resource blocks and data sources                                          |
| `variables.tf` | Input variable declarations — what the caller must provide to customize the module.       | `variable "location" { type = string }`                                   |
| `outputs.tf`   | Output values — what the module returns to callers (IDs, endpoints, IPs).                 | `output "storage_account_id" { value = azurerm_storage_account.this.id }` |

<Frame>
  <img alt="The image explains the components of a Terraform module, showing main.tf for main resources, variables.tf for input values, and outputs.tf for values to retrieve." />
</Frame>

Structurally: inputs → resources → outputs. That is the typical lifecycle and mental model for module design.

## Why use modules?

Why not write everything directly in the root configuration? Modules provide three concrete advantages:

1. Reuse instead of copy-paste — avoid duplicating resource blocks across environments (dev, test, prod), which reduces human error and configuration drift.
2. Organization and maintainability — split large, monolithic files (e.g., 1,500-line `main.tf`) into focused modules like `network`, `compute`, and `storage`. This makes code easier to read and troubleshoot.
3. Scalability — instantiate the same module across regions or tenants by changing inputs. Infrastructure becomes a configuration task, not a rewrite.

<Frame>
  <img alt="The image explains the benefits of using modules, highlighting points such as reusing code, keeping projects organized, and making infrastructure easier to scale." />
</Frame>

### Operational risk reduction

Without modules, the same configuration parameters (replication type, TLS settings, tagging strategy) are repeated in many places. If you need to change a policy later, you must update every instance, which is error-prone.

With modules, that logic is centralized. Callers only pass inputs. If you update module logic, all callers inherit the change. This is abstraction, and it lets infrastructure teams scale safely. However, be mindful: over-abstracting can push important implementation details out of reach for callers, making debugging harder.

<Callout icon="lightbulb">
  Use modules to standardize and reuse infrastructure logic. Avoid over-abstraction that hides too much implementation detail from callers.
</Callout>

## Example: a storage module and how to call it

Below is a concise example demonstrating the storage resource inside a module and how a root configuration invokes that module.

Resource inside the module (modules/storage/main.tf):

```hcl theme={null}
resource "azurerm_storage_account" "this" {
  name                      = var.storage_name
  resource_group_name       = var.resource_group_name
  location                  = var.location
  account_tier              = var.account_tier
  account_replication_type  = var.account_replication_type
  enable_https_traffic_only = true
  tags                      = var.tags
}
```

A typical `variables.tf` inside the same module might include:

```hcl theme={null}
variable "storage_name" {
  type        = string
  description = "The name of the Storage Account"
}

variable "resource_group_name" {
  type        = string
  description = "The resource group where the storage account will be created"
}

variable "location" {
  type        = string
  description = "Azure region for the storage account"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to the storage account"
  default     = {}
}
```

And `outputs.tf` could expose helpful values:

```hcl theme={null}
output "storage_account_id" {
  value       = azurerm_storage_account.this.id
  description = "The ID of the storage account"
}
```

Calling the module from the root configuration:

```hcl theme={null}
module "storage1" {
  source                   = "../modules/storage"
  storage_name             = "mystorage123"
  resource_group_name      = "rg-example"
  location                 = "eastus"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags = {
    environment = "dev"
  }
}
```

The `source` points to the module folder that contains the `main.tf`, `variables.tf`, and `outputs.tf`. Callers pass inputs; the module contains the creation logic. Update the module to apply improvements across all callers.

## Key takeaways

* A Terraform module is a folder grouping Terraform configuration for a specific unit of infrastructure.
* Modules enable reuse, cleaner structure, and easier scaling.
* Common files: `main.tf`, `variables.tf`, `outputs.tf`.
* Use modules to enforce standards and reduce duplication—while avoiding excessive abstraction that makes debugging harder.

## Next steps and references

* Start by converting repeated resource blocks into modules (one resource type at a time).
* Create clear variable names, sensible defaults, and concise outputs to make modules easy to consume.
* Version and publish reusable modules (e.g., private registry or Git tags) to promote safe upgrades.

Links and references:

* [Terraform Modules - Official Docs](https://www.terraform.io/language/modules)
* [Terraform Registry](https://registry.terraform.io/)
* [Azure Provider for Terraform](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])

Let's take a closer look next at module composition patterns and how to manage inputs/outputs for large projects.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/e38de693-04a0-45e9-b67a-9f8d26ac03ee/lesson/70d6a889-2249-42f2-b3c3-6d2f13b65736" />
</CardGroup>
