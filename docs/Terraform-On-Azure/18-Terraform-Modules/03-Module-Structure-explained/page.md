# root/main.tf
module "storage" {
  source       = "./modules/storage"
  storage_name = "mystorageacct"
  location     = "eastus"
}
```

## Typical module structure

Modules are usually organized with a small set of well-known files. Following this convention improves clarity, reuse, and versioning.

Directory layout example:

```text theme={null}
modules/
  storage/
    main.tf
    variables.tf
    outputs.tf
    providers.tf       # optional, for provider configuration
    versions.tf        # optional, for Terraform and provider version constraints
```

Common file responsibilities:

| File                           | Purpose                                                                                             |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| `main.tf`                      | Define the module’s resources and primary configuration.                                            |
| `variables.tf`                 | Declare input variables the module accepts and their defaults.                                      |
| `outputs.tf`                   | Expose values from the module to the caller.                                                        |
| `providers.tf` / `versions.tf` | Optional: pin provider/terraform versions and provider requirements (useful for published modules). |

Minimal example variables for a storage module:

```hcl theme={null}
# modules/storage/variables.tf
variable "storage_name" {
  description = "Name of the storage account"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}
```

Example module resources:

```hcl theme={null}
# modules/storage/main.tf
resource "azurerm_storage_account" "this" {
  name                     = var.storage_name
  location                 = var.location
  resource_group_name      = azurerm_resource_group.rg.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.storage_name}-rg"
  location = var.location
}
```

Example outputs:

```hcl theme={null}
# modules/storage/outputs.tf
output "storage_account_id" {
  description = "The ID of the storage account"
  value       = azurerm_storage_account.this.id
}
```

## Calling and consuming a module

In your root module, use a `module` block to call a child module and map inputs. Then reference module outputs with `module.<NAME>.<OUTPUT>`.

Example root invocation and output consumption:

```hcl theme={null}
# root/main.tf
provider "azurerm" {
  features = {}
}

module "storage" {
  source       = "./modules/storage"
  storage_name = "mystorageacct"
  location     = "eastus"
}

output "storage_id" {
  value = module.storage.storage_account_id
}
```

Common commands to execute from the root module directory:

```bash theme={null}
terraform init
terraform plan
terraform apply
```

## Why use modules?

Modules provide several concrete benefits for teams and enterprise Azure deployments:

| Benefit         | Description                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| Reusability     | Encapsulate repeatable infrastructure patterns (networking, storage, compute) into callable units.         |
| Consistency     | Enforce standardized configurations and naming conventions across environments and teams.                  |
| Maintainability | Smaller focused modules are easier to test, reason about, and update than one large configuration.         |
| Composition     | Build complex architectures by composing smaller modules, simplifying dependency management and lifecycle. |

Design guidance: aim for small, single-responsibility modules with clear input/output contracts. Use inputs to parameterize behavior and outputs to expose only what callers need.

## Comparing configurations: with vs without modules

| Characteristic       | Without modules                            | With modules                                            |
| -------------------- | ------------------------------------------ | ------------------------------------------------------- |
| Code duplication     | High — repeated blocks across environments | Low — reuse module multiple times with different inputs |
| Consistency          | Harder to enforce                          | Easier to enforce standardized patterns                 |
| Testing & validation | More manual across many files              | Test modules once, reuse confidently                    |
| Onboarding           | New contributors face bigger monoliths     | Easier to understand small focused modules              |
| Complexity           | Single large file can be complex           | Complexity managed via composition                      |

## Best practices and considerations

* Keep modules focused (single responsibility) and parameterized through clear inputs.
* Avoid hardcoding environment-specific values in modules; supply them from the root module or environment variables.
* When publishing modules, include `versions.tf` and clear README documentation.
* Be deliberate about provider configuration: prefer configuring providers in the root module and passing provider aliases to child modules when needed.
* Use remote state or workspaces appropriately to manage state separation between environments.

## Related topics and references

* [Terraform Modules Documentation](https://www.terraform.io/docs/language/modules/index.html)
* [Azure Provider for Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* [Terraform Registry](https://registry.terraform.io/)
* [Best practices for module design](https://www.terraform.io/docs/language/modules/develop/index.html)

Further exploration

* Structuring module inputs and sensible defaults for flexible reuse.
* Publishing and versioning modules: local vs registry vs Git.
* Provider management and remote state strategies across modules.
* Real-world Azure patterns for enterprise: networking, identity, and security modules.

Now that you understand what Terraform modules are and why they matter, proceed to the hands-on example and step-by-step module build in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/e38de693-04a0-45e9-b67a-9f8d26ac03ee/lesson/4555be4c-7064-4566-bcaa-418117bed43f)


# Module Structure explained

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Modules/Module-Structure-explained/page

Explains Terraform module structure, inputs, outputs, and file conventions with Azure resource group and storage account examples and best practices for reusable composable modules

Understanding Terraform modules starts with a simple truth: a module is not a special language construct — it is a folder organized in a predictable way. When you grasp that pattern, building reusable modules becomes straightforward.

At a high level, a Terraform module:

* Defines resources (the "how").
* Declares inputs (the "what" the caller provides).
* Exposes outputs (values other modules or the root module can consume).

Common files you’ll find in a module:

* `main.tf` — resource definitions (execution layer).
* `variables.tf` — inputs the module expects (module interface/contract).
* `outputs.tf` — values the module exposes to callers.

Separating the "how" (module logic) from the "what" (caller-provided values) makes modules composable and reusable.

| File           | Purpose                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `main.tf`      | Resource definitions and implementation details. Prefer referencing variables rather than hard-coding values so the module stays flexible. |
| `variables.tf` | Declares inputs: names, types, defaults, and validations. This is the module's contract with callers.                                      |
| `outputs.tf`   | Exposes useful data (IDs, endpoints, connection strings) consumers need to wire modules together.                                          |

<Frame>
  <img alt="The image shows the file structure of a &#x22;Storage Module&#x22; with files named main.tf, variables.tf, and outputs.tf, highlighting that outputs.tf provides useful information like an endpoint URL." />
</Frame>

Outputs are the communication channel between modules. Without outputs, modules cannot hand useful runtime values back to the root module or other modules that depend on them.

Below are practical examples showing how to implement this pattern. The examples keep module implementation minimal while demonstrating inputs and outputs clearly.

Example: a storage account resource implemented so every configurable attribute references a variable (caller decides name, location, SKU):

```hcl theme={null}
resource "azurerm_storage_account" "this" {
  name                     = var.storage_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.replication_type

  tags = var.tags
}
```

If your organization requires a specific configuration (for example, always use the `Standard` account tier), the module may enforce it by hard-coding that property:

```hcl theme={null}
resource "azurerm_storage_account" "this" {
  name                     = var.storage_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = var.replication_type

  tags = var.tags
}
```

> **lightbulb** Hard-coding an argument inside a module (e.g., `account_tier = "Standard"`) is a valid way to enforce organizational policies. Do this only for properties you intend to make non-configurable for consumers.

Now we’ll walk through creating two simple modules in Visual Studio Code: a `resource_group` module and a `storage_account` module. These examples illustrate a clean module structure and how to wire modules together from a root module.

Create the modules directory and subfolders:

```bash theme={null}
mkdir -p modules/resource_group
mkdir -p modules/storage_account
```

***

## Resource Group module

Path: `modules/resource_group`

main.tf

```hcl theme={null}
resource "azurerm_resource_group" "main" {
  name     = var.rg
  location = var.region

  tags = {
    Created   = "Terraform"
    Location  = var.region
    CreatedBy = "Module"
  }
}
```

variables.tf

```hcl theme={null}
variable "rg" {
  type        = string
  description = "Name of the resource group"
}

variable "region" {
  type        = string
  description = "Azure region for the resource group"
}
```

outputs.tf

```hcl theme={null}
output "rg_id" {
  description = "The ID of the resource group"
  value       = azurerm_resource_group.main.id
}
```

This module defines a resource group, declares the inputs it needs, and exposes the resource group's ID so other modules or the root module can consume it.

***

## Storage Account module

Path: `modules/storage_account`

main.tf

```hcl theme={null}
resource "azurerm_storage_account" "this" {
  name                     = var.storage
  resource_group_name      = var.rg
  location                 = var.region
  account_tier             = "Standard"            # enforced by module (organization standard)
  account_replication_type = var.rep

  tags = var.tags
}
```

variables.tf

```hcl theme={null}
variable "storage" {
  type        = string
  description = "Storage account name"
}

variable "rg" {
  type        = string
  description = "Name of the resource group to create the storage account in"
}

variable "region" {
  type        = string
  description = "Azure region for the storage account"
}

variable "rep" {
  type        = string
  description = "Replication type for the storage account (e.g., LRS, GRS)"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to the storage account"
  default     = {}
}
```

outputs.tf

```hcl theme={null}
output "primary_blob_endpoint" {
  description = "Primary Blob Endpoint for the storage account"
  value       = azurerm_storage_account.this.primary_blob_endpoint
}
```

In this example the `account_tier` is enforced to `Standard` by the module. All other attributes are configurable, which keeps the module reusable while still meeting organizational constraints.

***

## Using these modules from a root module

Once you have `modules/resource_group` and `modules/storage_account`, call them from your root module and wire outputs to inputs.

Example minimal root module usage:

```hcl theme={null}
module "rg" {
  source = "./modules/resource_group"

  rg     = "my-rg"
  region = "eastus"
}

module "storage" {
  source = "./modules/storage_account"

  storage = "mystorageacct"
  rg      = module.rg.rg_id         # or use the resource group name if exposed
  region  = "eastus"
  rep     = "LRS"
  tags    = { Environment = "dev" }
}

output "storage_blob_endpoint" {
  value = module.storage.primary_blob_endpoint
}
```

This pattern demonstrates:

* Modules encapsulate implementation details.
* Inputs (`variables.tf`) define the contract with callers.
* Outputs (`outputs.tf`) enable composition between modules.

***

## Best practices and tips

* Keep modules focused and small: one module per logical resource or closely related set of resources.
* Prefer variables over hard-coded values unless enforcing a policy.
* Document variables and outputs with `description` fields so consumers know how to use the module.
* Use semantic names for outputs (e.g., `primary_blob_endpoint`) so their intent is clear.
* Version modules if you publish them to a registry or share across teams.

## Links and references

* Terraform Modules: [https://www.terraform.io/docs/language/modules/index.html](https://www.terraform.io/docs/language/modules/index.html)
* Azure Provider for Terraform: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* Azure Resource Manager documentation: [https://docs.microsoft.com/azure/azure-resource-manager/](https://docs.microsoft.com/azure/azure-resource-manager/)

These resources will help deepen your understanding of modules and provider-specific resources.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/e38de693-04a0-45e9-b67a-9f8d26ac03ee/lesson/3d3a0851-93fc-4968-8ab1-0ee0cfb90463)
