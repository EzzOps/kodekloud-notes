# Add HashiCorp GPG key and repository, then install Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform -y

# Verify installation
terraform version

# Enable shell autocomplete (optional)
terraform --install-autocomplete
exec bash
```

<Callout icon="lightbulb">
  If you are using macOS, Windows, or another Linux distribution, follow the platform-specific installation instructions on the official Terraform documentation: [https://developer.hashicorp.com/terraform/tutorials](https://developer.hashicorp.com/terraform/tutorials).
</Callout>

## What you'll learn — Course roadmap

| Module            | Focus                                         | Example outcome                                |
| ----------------- | --------------------------------------------- | ---------------------------------------------- |
| Foundations       | IaC principles, Azure basics, provider setup  | Authenticate Terraform to Azure                |
| HCL & Providers   | Resources, providers, configuration syntax    | `provider "azurerm" { ... }`                   |
| Logic & Reuse     | `count`, `for_each`, `locals`, dynamic blocks | Create multiple resources from one config      |
| State Management  | Remote state with Azure Storage, locking      | Reliable team collaboration with state backend |
| Modules & Outputs | Organize infrastructure, share modules        | Reusable resource modules and outputs          |
| CI/CD             | Azure DevOps pipelines, plan/apply automation | CI/CD pipeline for Terraform changes           |

## Provider and a simple resource example

A minimal Azure provider and resource written in HCL:

```hcl theme={null}
provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-8a6b-6a9066d6d3a3"
}

resource "azurerm_resource_group" "rg" {
  name     = "kodekloud-tf-rg"
  location = "East US"
}
```

This config declares the AzureRM provider and creates a resource group in East US.

## Typical Terraform workflow — plan and apply

When you run Terraform, the common interaction is `terraform plan` followed by `terraform apply`. Example console output:

```plaintext theme={null}
$ terraform plan
Note: You didn't use the --out option to save this plan, so Terraform can't guarantee to take exactly these actions when you run "terraform apply" now.

$ terraform apply
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_resource_group.rg will be created
  + resource "azurerm_resource_group" "rg" {
      + id       = (known after apply)
      + location = "East US"
      + name     = "kodekloud-tf-rg"
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.

Enter a value: yes
```

## Iteration, logic, and modular patterns

You’ll learn to make configurations dynamic with `count`, `for_each`, conditionals, `locals`, and built-in functions. Example network security rule resource in HCL:

```hcl theme={null}
resource "azurerm_network_security_rule" "rule2" {
  name                        = "allow-https"
  priority                    = 200
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.nsg.name
}
```

Use `locals` and `dynamic` blocks where patterns repeat to reduce duplication and improve maintainability.

## Terraform state (why it matters)

State is the source of truth Terraform uses to map real-world resources to your configuration. In team environments, store state remotely (e.g., Azure Storage account with locking). Terraform state files are JSON; here’s a truncated example showing structure:

```json theme={null}
{
  "version": 4,
  "terraform_version": "1.5.7",
  "serial": 1,
  "lineage": "c62f9521-2fc2-a699-211f-ef1306c99896",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "azurerm_storage_account",
      "name": "example",
      "provider": "provider[\"registry.terraform.io/hashicorp/azurerm\"]",
      "instances": [
        {
          "schema_version": 4,
          "attributes": {
            "access_tier": "Hot",
            "account_kind": "StorageV2",
            "account_replication_type": "LRS",
            "account_tier": "Standard",
            "allow_nested_items_to_be_public": true,
            "allowed_copy_scope": "",
            "azure_files_authentication": [],
            "blob_properties": {}
          }
        }
      ]
    }
  ]
}
```

## Outputs and modules

Outputs expose computed values from modules or root configurations. Modules enable reuse and separation of concerns.

Example output:

```hcl theme={null}
output "endpoint" {
  value = module.storage.endpoint
}
```

Example module usage:

```hcl theme={null}
module "rg" {
  source = "../modules/resource_group"
  rg     = var.rg_name
  region = var.location
}

module "storage" {
  source  = "../modules/storage_account"
  storage = "stdmstorager56535"
  rg      = module.rg.rg_name
  region  = module.rg.rg_location
  rep     = "LRS"
}
```

Sample apply output for modules:

```plaintext theme={null}
$ terraform apply -auto-approve
module.rg.azurerm_resource_group.main: Still creating... [20s elapsed]
module.rg.azurerm_resource_group.main: Creation complete after 27s [id=/subscriptions/1b282746-75fd-46ed-8a6b-6a90666dd3a3/resourceGroups/kodekloud-tf-rg]
module.storage.azurerm_storage_account.this: Creating...
module.storage.azurerm_storage_account.this: Still creating... [10s elapsed]
module.storage.azurerm_storage_account.this: Still creating... [20s elapsed]
module.storage.azurerm_storage_account.this: Still creating... [30s elapsed]
module.storage.azurerm_storage_account.this: Still creating... [40s elapsed]
module.storage.azurerm_storage_account.this: Still creating... [50s elapsed]
module.storage.azurerm_storage_account.this: Creation complete after 1m5s [id=/subscriptions/1b282746-75fd-46ed-8a6b-6a90666dd3a3/resourceGroups/kodekloud-tf-rg/providers/Microsoft.Storage/storageAccounts/stdmstorager56535]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
Outputs:
```

## CI/CD with Terraform and Azure DevOps

We finish the course by integrating Terraform into CI/CD pipelines (Azure DevOps, GitHub Actions, or other CI systems). You’ll learn to automate:

* terraform fmt, init, validate, plan
* plan approval gates and manual checks
* controlled terraform apply in production

This approach lets teams ship infrastructure changes safely and repeatedly.

By the end of this module, you will be able to design,

<Frame>
  <img alt="The image shows an Azure DevOps interface with a repository named &#x22;Terraform on Azure&#x22; containing several files. In the bottom right corner, there's an overlay of a person from KodeKloud." />
</Frame>

deploy, and automate Azure infrastructure with Terraform from your machine all the way to a production pipeline.

## Community and next steps

At KodeKloud we value community learning. Join our forums to ask questions, share labs, and collaborate with peers. Build real projects, contribute modules, and iterate with feedback.

Additional references

* Terraform: [https://www.terraform.io/](https://www.terraform.io/)
* Terraform Azure Provider (azurerm): [https://registry.terraform.io/providers/hashicorp/azurerm](https://registry.terraform.io/providers/hashicorp/azurerm)
* Azure Documentation: [https://docs.microsoft.com/azure](https://docs.microsoft.com/azure)

Ready to master Infrastructure-as-Code on Azure and accelerate your cloud career? Let's get started.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ab5ee49b-38b0-43bc-929b-f230cde10d90/lesson/a3ba353d-6d04-405a-8c36-01ef6db361e8" />
</CardGroup>


# Conditional Expressions

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Iteration-and-Logic/Conditional-Expressions/page

Explains Terraform conditional and for expressions, using ternary operators, nested versus flat lists, flatten and toset for for_each, and environment-based configuration examples

Conditional expressions in Terraform let you choose one value or another based on a boolean condition — essentially Terraform's ternary operator. This is useful for selecting regions, SKUs, sizes, or toggling small feature differences without duplicating resources or maintaining separate files per environment.

Example — choose region based on environment:

```hcl theme={null}
variable "environment" {
  type = string
  default = "dev"
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-demo"
  location = var.environment == "prod" ? "eastus" : "westus"
}
```

The syntax is: `condition ? value_if_true : value_if_false`.

Use conditional expressions to keep configuration DRY and to decide values dynamically during `terraform plan` and `terraform apply`.

<Callout icon="lightbulb">
  Use conditional expressions to keep code clean and let Terraform compute configuration values (regions, SKUs, toggles) at plan/apply time.
</Callout>

This article also covers `for` expressions and how they interact with conditional expressions and `for_each`.

Example showing provider, variable, and locals with a conditional:

```hcl theme={null}
provider "azurerm" {
  features {}
}

variable "environment" {
  type    = string
  default = "dev"
}

locals {
  location     = var.environment == "prod" ? "eastus" : "westus"
  environments = ["dev", "prod"]
  apps         = ["api", "web", "db"]
}
```

Generating resource-group names with for expressions

Two common patterns generate combinations (environments × apps):

1. Nested `for` expression that returns a list of lists (nested list)

```hcl theme={null}
locals {
  rg_nested = [
    for env in local.environments :
      [ for app in local.apps : "rg-${env}-${app}" ]
  ]
}
```

`local.rg_nested` becomes a list with inner lists (one per environment), for example:
`[["rg-dev-api","rg-dev-web","rg-dev-db"], ["rg-prod-api","rg-prod-web","rg-prod-db"]]`.

2. Single `for` expression with two iterators that returns a flat list

```hcl theme={null}
locals {
  rg_flat = [ for env in local.environments : for app in local.apps : "rg-${env}-${app}" ]
}
```

`local.rg_flat` produces a flat list:
`["rg-dev-api","rg-dev-web","rg-dev-db","rg-prod-api","rg-prod-web","rg-prod-db"]`.

Using the generated names as resources

Terraform `for_each` supports maps and sets of strings. If you have a nested list (`rg_nested`), flatten it before converting to a set. Example using the nested list:

```hcl theme={null}
locals {
  rg_nested = [
    for env in local.environments :
      [ for app in local.apps : "rg-${env}-${app}" ]
  ]
}

resource "azurerm_resource_group" "rg" {
  for_each = toset(flatten(local.rg_nested))
  name     = each.value
  location = local.location
}
```

If you produce a flat list (`rg_flat`), you can use it directly:

```hcl theme={null}
locals {
  rg_flat = [ for env in local.environments : for app in local.apps : "rg-${env}-${app}" ]
}

resource "azurerm_resource_group" "rg" {
  for_each = toset(local.rg_flat)
  name     = each.value
  location = local.location
}
```

Why flatten? Example error when using a nested list directly

If you use the nested list without `flatten`, `for_each` will fail during `terraform plan`:

```bash theme={null}
