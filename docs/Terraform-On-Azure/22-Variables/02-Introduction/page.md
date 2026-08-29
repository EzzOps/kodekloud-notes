# ---- variables.tf ----
variable "resource_group_name" {
  type        = string
  default     = "my-workshop-eus-rg"
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  default     = "East US"
  description = "Azure region"
}
```

Use the variables in your resource (`main.tf`):

```hcl theme={null}
# ---- main.tf ----
resource "azurerm_storage_account" "storage" {
  name                      = "satfworshop46536"
  location                  = var.location
  resource_group_name       = var.resource_group_name
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}

resource "azurerm_storage_account" "storage2" {
  name                      = "satfworshop48835"
  location                  = var.location
  resource_group_name       = var.resource_group_name
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}
```

Referencing `var.location` and `var.resource_group_name` allows multiple resources to reuse the same inputs. If the region or resource group needs to change, update the variable defaults or supply different values at runtime in one place instead of editing every resource block.

> **lightbulb** Variables can be provided by default values, environment variables, a `.tfvars` file, or via CLI flags when you run Terraform. This makes configurations portable and easier to manage across environments.

Common ways to provide variable values

| Source                    | Usage                                                  | Example                                                          |
| ------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- |
| Default in `variables.tf` | Automatically used when no other value provided        | `default = "eastus"`                                             |
| Environment variable      | Prefix `TF_VAR_` to variable name                      | `export TF_VAR_region="eastus"`                                  |
| `*.tfvars` file           | Create a `terraform.tfvars` or custom file and pass it | `region = "eastus"` or `terraform apply -var-file="prod.tfvars"` |
| CLI `-var` flag           | Pass a value directly when running Terraform           | `terraform apply -var 'region=westus'`                           |

Demonstration: creating variables and resources in a project directory

* We'll create a small Terraform project that defines a provider, variables, and a single resource group resource.
* For brevity, this demo uses simpler variable names (`rg` and `region`) to illustrate the same concept.

Provider configuration (`provider.tf`):

```hcl theme={null}
provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-8a6b-6a90666d6d3a"
}
```

Declare variables (`variables.tf`):

```hcl theme={null}
variable "rg" {
  default = "kodekloud-tf-var-rg"
}

variable "region" {
  default = "eastus"
}
```

Use variables in the resource group resource (`main.tf`):

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = var.rg
  location = var.region
  tags     = {
    environment = "testing"
  }
}
```

Initialize the working directory and inspect the plan:

```bash theme={null}
terraform init
terraform plan
```

Sample `terraform init` output:

```plaintext theme={null}
Terraform has been successfully initialized!
```

Sample `terraform plan` output:

```plaintext theme={null}
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

# azurerm_resource_group.rg will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "eastus"
    + name     = "kodekloud-tf-var-rg"
    + tags     = {
        + "environment" = "testing"
      }
  }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Note that the plan shows the resolved values (for example, `eastus` and `kodekloud-tf-var-rg`) rather than `var.rg` or `var.region`. This makes it easy to review what Terraform will deploy.

> **warning** Do not store sensitive secrets (API keys, passwords) in plaintext `variables.tf` defaults or checked-in `.tfvars` files. Use environment variables, Terraform Cloud/Enterprise workspace variables, or secret management integrations to protect sensitive data.

Quick reference: variable block essentials

| Argument      | Description                                                                         | Example                        |
| ------------- | ----------------------------------------------------------------------------------- | ------------------------------ |
| `type`        | Optional: enforce a data type (`string`, `number`, `bool`, `list`, `map`, `object`) | `type = string`                |
| `default`     | Optional: value used when no other value supplied                                   | `default = "eastus"`           |
| `description` | Optional: helpful text for maintainers                                              | `description = "Azure region"` |
| `sensitive`   | Optional: mark value as sensitive to hide in output                                 | `sensitive = true`             |

Summary

* Declaring variables decouples configuration values from resource blocks, improving reusability and maintainability.
* Use `var.<name>` in resource blocks to reference declared variables.
* Variable values can be supplied via defaults, environment variables (`TF_VAR_`), `.tfvars` files, or CLI `-var` flags.
* For secrets, avoid checked-in defaults and prefer secure secret mechanisms.

Further reading and references

* [Terraform Input Variables](https://www.terraform.io/language/values/variables)
* [Terraform CLI - var files](https://www.terraform.io/cli/commands#apply)
* [Azure Provider (azurerm) on Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

A deeper dive into the `variable` block would cover advanced topics such as type constraints, `validation` blocks, `sensitive` attributes, and multiple ways to provide variable values across CI/CD and team workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/6909fa70-4ccc-40c3-a918-1188673d8985/lesson/4499ac01-c650-4fa8-b55c-f75a90691478)


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Variables/Introduction/page

Guide to Terraform input variables explaining declaration, types, value provisioning methods, and best practices for reusable environment-agnostic configurations and secure handling of sensitive data

In this lesson we cover Terraform variables: how to declare them, how they make configurations reusable and environment-agnostic, and the common patterns for supplying values.

Variables let you parameterize your Terraform configuration instead of hard-coding values. This makes code easier to reuse across environments (dev, staging, prod), simplifies CI/CD automation, and reduces duplication.

Agenda for this lesson:

1. Define input variables in Terraform
   * Externalize values such as region, resource names, SKUs, subscriptions, and environment-specific settings.

2. Understand the `variable` block
   * Learn the structure and purpose of the `variable` block, including metadata such as `type`, `default`, and `description`. Note that the variable's `name` is declared in the block header (e.g., `variable "name" { ... }`) rather than as a field inside the block.

3. Supply values to variables
   * Explore ways to provide variable values: `.tfvars` files, command-line arguments (`-var` and `-var-file`), environment variables, and interactive prompts.

4. Work with Terraform variable types
   * Review primitive types (`string`, `number`, `bool`) and complex types (`list`, `map`, `object`) with usage examples.

<Frame>
  <img alt="The image presents an agenda with four points about using input variables in Terraform configurations, including defining variables, understanding variable blocks, setting variable values, and identifying data types. The agenda is visually organized with numbered markers and a gradient background." />
</Frame>

> **lightbulb** Use variables to decouple environment-specific data from configuration. This enables the same Terraform codebase to provision different environments by supplying different variable values.

We will now start by looking at how to declare input variables and the structure of a `variable` block.

## Declaring input variables

A `variable` block defines an input variable for a module or root module. The block header contains the variable name; attributes inside define metadata and constraints.

Basic example:

```hcl theme={null}
variable "location" {
  description = "Azure region where resources will be deployed"
  type        = string
  default     = "eastus"
}
```

Key attributes:

* `description` — human-readable context for the variable
* `type` — the data type (e.g., `string`, `number`, `bool`, `list(string)`, `map(string)`, `object({...})`)
* `default` — optional value used if none is supplied
* `sensitive` — optional boolean to mark values as sensitive (prevents them from being shown in CLI output)

Example showing a mix of types, including `map` and `object`:

```hcl theme={null}
variable "tags" {
  description = "Tags applied to resources"
  type        = map(string)
  default = {
    environment = "dev"
    owner       = "team-a"
  }
}

variable "vm_sizes" {
  description = "Allowed VM SKUs for this environment"
  type        = list(string)
  default     = ["Standard_B1s", "Standard_B2s"]
}

variable "service_config" {
  description = "Configuration object for the service"
  type = object({
    sku               = string
    capacity          = number
    enable_monitoring = bool
  })
  default = {
    sku               = "standard"
    capacity          = 2
    enable_monitoring = true
  }
}
```

Referencing variables inside your configuration uses the `var` namespace:

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.service_config.sku}"
  location = var.location
  tags     = var.tags
}
```

## Variable types — quick reference

| Type            | Description                             | Example                                       |
| --------------- | --------------------------------------- | --------------------------------------------- |
| `string`        | Simple text                             | `variable "name" { type = string }`           |
| `number`        | Numeric values                          | `variable "replicas" { type = number }`       |
| `bool`          | True / false                            | `variable "enabled" { type = bool }`          |
| `list(...)`     | Ordered list                            | `list(string)` — `["a", "b"]`                 |
| `map(...)`      | Key/value collection                    | `map(string)` — `{ env = "dev" }`             |
| `object({...})` | Structured object with typed attributes | `object({ sku = string, capacity = number })` |

When providing examples or inline values that include braces (`{}`) or double-curly syntax, wrap them in backticks to avoid MDX parsing issues. For example: `` `[{ "object": "person", "bbox": [0,0,10,10] }]` ``.

## Ways to supply variable values

Terraform supports multiple ways to provide values for input variables. Choose the method that fits your workflow (local testing, automation, CI/CD, or secret management).

| Method                | Use case                                                       | Example                                          |
| --------------------- | -------------------------------------------------------------- | ------------------------------------------------ |
| `.tfvars` file        | Grouped values per environment (recommended for repeated runs) | `terraform.tfvars` or `prod.tfvars`              |
| `-var-file`           | Explicitly pass a tfvars file on the CLI                       | `terraform apply -var-file="prod.tfvars"`        |
| `-var`                | Quick one-off values                                           | `terraform apply -var='location=westus2'`        |
| Environment variables | CI/CD or secrets via env vars                                  | `export TF_VAR_location="westus2"`               |
| Interactive prompt    | When no default is provided and automation isn't used          | Terraform prompts for missing required variables |

Example `terraform.tfvars`:

```hcl theme={null}
resource_name = "my-rg"
location      = "westus2"
```

Environment variable example:

```bash theme={null}
export TF_VAR_location="westus2"
terraform apply
```

CLI example:

```bash theme={null}
terraform apply -var='location=westus2' -var='resource_name=my-rg'
```

> **warning** Do not commit secrets (passwords, API keys) into `.tfvars` files stored in version control. Use a secrets manager or mark variables `sensitive = true` and supply values via secure pipelines or Terraform Cloud/Enterprise variable sets.

## Best practices

* Prefer `tfvars` files for environment-level defaults and `-var-file` to select them at runtime.
* Use typed variables (`list(...)`, `map(...)`, `object(...)`) to validate inputs and catch mistakes early.
* Document variable `description` values to aid collaborators and automation.
* Avoid hard-coding environment-specific values inside modules—pass them as inputs to keep modules reusable.

## Links and references

* [Terraform Input Variables — HashiCorp Documentation](https://developer.hashicorp.com/terraform/language/values/variables)
* [Best practices for using Terraform variables](https://developer.hashicorp.com/terraform/tutorials/local-development/terraform-modules)

We will next walk through concrete examples of using variables in modules and how to organize `tfvars` files per environment.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/6909fa70-4ccc-40c3-a918-1188673d8985/lesson/fb6658ce-0f7a-4c42-b3a7-9cdd5dd21331)
