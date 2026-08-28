# main.tf (root)
module "backup_storage" {
  source           = "../storage-module"
  storage_name     = "backupupsa321"
  rg_name          = "my-workshop-rg"
  location         = "East US"
  account_tier     = "Standard"
  replication_type = "ZRS"
}
```

* The left-hand identifier (`backup_storage`) is a logical name for the module block inside your configuration — it is not the name of any Azure resource.
* `source` tells Terraform where to find the module code. In this example it's a local path (`../storage-module`). You can also reference Git repositories, the [Terraform Registry](https://registry.terraform.io/), or private registries.
* The attributes inside the module block (for example, `storage_name`, `rg_name`, `location`) must match the variable names declared in the module (see its `variables.tf`). These bind values from the calling configuration into the module.

Think of a module like a function: you define inputs (variables) and the module returns outputs. When Terraform evaluates the configuration, it injects the passed input values into the module and evaluates the resources inside as part of the calling configuration's graph.

<Callout icon="lightbulb">
  Module block names are local identifiers only. They do not automatically set Azure resource names — pass explicit values through variables for resource naming.
</Callout>

## Module sources: local and remote

Common module `source` formats:

| Source type        | Description                         | Example                                                      |
| ------------------ | ----------------------------------- | ------------------------------------------------------------ |
| Local path         | Modules kept in your repo.          | `./modules/resource_group`                                   |
| Relative path      | Referencing adjacent folders.       | `../modules/storage_account`                                 |
| Git / VCS          | Fetch module from a Git repository. | `git::https://github.com/you/terraform-modules.git//storage` |
| Terraform Registry | Public or private registry modules. | `azure/storage/azurerm`                                      |

The Terraform Registry includes curated modules that often follow provider-specific best practices — useful for production.

## Example walkthrough — root configuration and module calls

Below is a typical sequence used in a root configuration that consumes multiple local modules (resource group and storage account).

1. Provider configuration (root/main.tf or provider.tf)

```hcl theme={null}
# provider.tf
variable "subscription_id" {
  type = string
}

provider "azurerm" {
  features        = {}
  subscription_id = var.subscription_id
}
```

You can obtain the subscription ID with `az account show` and assign it in `terraform.tfvars` or use environment variables.

2. Calling the resource group module from the root

```hcl theme={null}
# main.tf (root)
module "rg" {
  source = "./modules/resource_group"
  rg     = var.rg_name
  region = var.location
}
```

Assume the module defines an Azure Resource Group using variables `rg` and `region`:

```hcl theme={null}
# modules/resource_group/main.tf (module)
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

3. Expose values from the resource group module via outputs so other modules can reference them

```hcl theme={null}
# modules/resource_group/outputs.tf
output "rg_id" {
  value = azurerm_resource_group.main.id
}

output "rg_name" {
  value = azurerm_resource_group.main.name
}

output "rg_location" {
  value = azurerm_resource_group.main.location
}
```

4. Calling the storage-account module and referencing resource group outputs

```hcl theme={null}
# main.tf (root)
module "storage" {
  source  = "./modules/storage_account"
  storage = "stmodstorage56535"
  rg      = module.rg.rg_name
  region  = module.rg.rg_location
  rep     = "LRS"
}
```

The `storage_account` module should accept inputs such as `storage`, `rg`, `region`, and `rep`, and may expose outputs like the storage blob endpoint.

5. Example storage-account module output (so the root can retrieve the blob endpoint)

```hcl theme={null}
# modules/storage_account/outputs.tf
output "endpoint" {
  value = azurerm_storage_account.this.primary_blob_endpoint
}
```

6. Declaring the root variables and tfvars

```hcl theme={null}
# variables.tf (root)
variable "rg_name" {
  type = string
}

variable "location" {
  type = string
}
```

```hcl theme={null}
# terraform.tfvars
rg_name        = "rg-modules-demo"
location       = "East US"
subscription_id = "1b228746-75fd-46ed-8a6b-6a9066d6d3a"
```

## Practical notes on evaluation and execution flow

* `terraform init`: downloads provider plugins and initializes module source code (including remote module sources).
* `terraform plan`: reads the calling configuration (root), loads referenced modules, injects input values, evaluates resources inside the modules, and produces an execution plan. Modules are evaluated as part of the root dependency graph — they are not separate deployments.
* `terraform apply`: executes the plan and creates/manages resources described across the root and module code.
* Reuse: call the same module multiple times with different inputs (e.g., `module "rg2" { ... }`) to create multiple resource instances without duplicating resource blocks.

Below is a quick reference table for common commands and their purpose:

| Command                          | Purpose                                                      |
| -------------------------------- | ------------------------------------------------------------ |
| `terraform init`                 | Initialize working directory, download providers and modules |
| `terraform validate`             | Validate configuration syntax and internal consistency       |
| `terraform plan`                 | Produce an execution plan showing changes                    |
| `terraform apply --auto-approve` | Apply the plan and create/upate resources                    |
| `terraform destroy`              | Remove managed resources                                     |

Visual Studio Code context

<Frame>
  <img alt="The image shows a Visual Studio Code interface with Terraform configuration files open, displaying code related to Azure storage account resources. The terminal at the bottom has some Azure account information displayed." />
</Frame>

## Commands and a sample run

Initialize Terraform (this also initializes modules):

```bash theme={null}
terraform init
```

Typical `terraform init` output will indicate initialized modules:

```bash theme={null}
Initializing the backend...
Initializing modules...
  - rg in modules/resource_group
  - storage in modules/storage_account

Initializing provider plugins...
- Finding latest version of hashicorp/azurerm...
- Installing hashicorp/azurerm v4.60.0...
```

Validate, plan, and apply:

```bash theme={null}
terraform validate
terraform plan
terraform apply --auto-approve
```

A successful apply might show:

```terraform theme={null}
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

endpoint = "https://stmodstorage56535.blob.core.windows.net/"
```

You can verify the resource group and its tags using the Azure CLI:

```bash theme={null}
az group show -n rg-modules-demo
```

A trimmed JSON snippet from `az group show` might include the tags created by the module:

```json theme={null}
{
  "id": "/subscriptions/1b228746-75fd-46ed-8a6b-6a9066d6d3a/resourceGroups/rg-modules-demo",
  "location": "eastus",
  "name": "rg-modules-demo",
  "properties": { "provisioningState": "Succeeded" },
  "tags": {
    "Created": "Terraform",
    "CreatedBy": "Module",
    "Location": "East US"
  },
  "type": "Microsoft.Resources/resourceGroups"
}
```

## Reusing the same module to create additional resource groups

To create multiple resource groups using the same module, call it multiple times with different inputs:

```hcl theme={null}
module "rg" {
  source = "../modules/resource_group"
  rg     = var.rg_name
  region = var.location
}

module "rg2" {
  source = "../modules/resource_group"
  rg     = var.rg_name2
  region = var.location
}
```

Then add `rg_name2` to `variables.tf` / `terraform.tfvars` to provide the second resource group name.

<Callout icon="warning">
  Keep module variable names and the calling attributes aligned. A mismatch (for example, passing `rg` to a module that expects `resource_group_name`) will cause validation or planning errors.
</Callout>

## Summary

* Define reusable resources inside a module directory and expose inputs (`variables.tf`) and outputs (`outputs.tf`).
* Call that module from the root using a `module` block and pass inputs that match the module's variables.
* Export values from modules using outputs so other modules or the root can reference them.
* Initialize with `terraform init`, then `terraform plan` and `terraform apply`. Modules are evaluated as part of the root execution graph and support scalable, DRY Terraform configurations.

Links and references

* [Terraform Registry](https://registry.terraform.io/)
* [Azure Provider (azurerm) documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* [Azure CLI docs](https://learn.microsoft.com/cli/azure/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/e38de693-04a0-45e9-b67a-9f8d26ac03ee/lesson/ad9c5d69-215a-492c-a468-1c9257bbce9b" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Modules/Introduction/page

Overview of Terraform modules explaining structure usage and best practices for reusable Azure infrastructure including root versus child modules inputs outputs and module composition

Welcome to the lesson on Terraform modules.

As infrastructure grows—especially in Azure environments—Terraform configurations often become repetitive and harder to manage. Terraform modules solve this by grouping related resources into reusable, composable units. This lesson builds both conceptual and practical understanding of modules: what they are, how they’re structured, how to call them, and when to use them.

Learning objectives

* Explain what a Terraform module is and why modules are used.
* Distinguish the root module (your working directory) from child modules called by the root module.
* Describe a module’s typical structure and the roles of `main.tf`, `variables.tf`, and `outputs.tf`.
* Call and consume a module using inputs and outputs.
* Compare configurations with and without modules and reason about trade-offs for reusability, consistency, and maintainability in enterprise Azure deployments.

<Callout icon="lightbulb">
  A Terraform module is simply a folder containing Terraform configuration files. The root module is the configuration in your current working directory; any other folder referenced with a `module` block is a child (or remote) module.
</Callout>

This overview introduces core concepts with minimal, focused examples to make ideas concrete and actionable.

## Root module vs child modules

* Root module: The Terraform configuration in the directory where you run `terraform init` and `terraform apply`. It can call other modules and orchestrate resources.
* Child module: Any module invoked by the root module using a `module` block. Child modules can be local folders, Git repositories, or modules published to the Terraform Registry.

Example: a root module that calls a child module named `storage`:

```hcl theme={null}
