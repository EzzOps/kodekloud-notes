# resource example — Terraform will create and manage this VNet
resource "azurerm_virtual_network" "example_vnet" {
  name                = "example-vnet"
  location            = "eastus"
  resource_group_name = "example-rg"
  address_space       = ["10.0.0.0/16"]
}
```

data source example — Terraform will look up an existing virtual network but will not manage it:

```hcl theme={null}
# data source example — Terraform reads an existing VNet's attributes without managing it
data "azurerm_virtual_network" "existing_vnet" {
  name                = "existing-vnet"
  resource_group_name = "existing-rg"
}
```

## When to use each

* Use `resource` when:
  * Terraform should create, update, or delete the object.
  * You want the object tracked in Terraform state.
  * You need full lifecycle management and drift detection.

* Use `data` when:
  * The object is managed outside this Terraform configuration (or by another team).
  * You need to reference attributes (IDs, names, subnet lists, AMI IDs).
  * You want to avoid Terraform creating duplicate or conflicting infrastructure.

## Practical tips

* Prefer data sources for shared resources (e.g., centrally managed networks, shared subnets).
* Avoid using data sources as a workaround to hide unmanaged drift — if you need to manage something consistently, convert it into a resource.
* Remember that data lookups may introduce dependency ordering; reference them explicitly to ensure correct evaluation.

## References

* [Terraform: Resources](https://www.terraform.io/docs/language/resources/index.html)
* [Terraform: Data Sources](https://www.terraform.io/docs/language/data-sources/index.html)
* [Azure Provider — azurerm Virtual Network](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network)

Summary: resources manage lifecycle and are tracked in state; data sources read and expose attributes from existing infrastructure without taking ownership.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/5e64ee11-c3c3-4d9c-be0c-53989a38ae8f/lesson/b8bbdea5-fe8a-4bd7-9dc9-404608a1ee45)


# What are data sources

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Data-Sources/What-are-data-sources/page

Explains using Terraform data sources to read existing Azure resources, reference attributes in configurations, avoid duplication, and create compatible resources with examples, errors, and best practices.

In this lesson we introduce Terraform data sources — a read-only mechanism that lets Terraform query existing infrastructure and expose attributes you can reference in your configuration. Data sources are ideal when you need to reference resources that are managed outside your current Terraform run (for example, an IT-managed resource group or storage account) without importing or recreating them.

Why use data sources?

* Reuse attributes (location, id, name) from existing resources.
* Avoid duplicating configuration values across stacks or pipelines.
* Keep Terraform operations non-destructive for resources managed elsewhere.

General data source structure

```hcl theme={null}
data "azurerm_<type>" "<name>" {
  # lookup filters or required parameters
}
```

Reference attributes from a data source using:

```hcl theme={null}
data.azurerm_<type>.<name>.<attribute>
```

Common example: read an existing Resource Group and reference its attributes

```hcl theme={null}
provider "azurerm" {
  features {}
  # Optionally set subscription_id here or via environment variables (AZURE_SUBSCRIPTION_ID)
}

data "azurerm_resource_group" "rg" {
  name = "rg-qe-workshop-riskaria"
}

resource "azurerm_storage_account" "example" {
  name                        = var.storage_account_name
  location                    = data.azurerm_resource_group.rg.location
  resource_group_name         = data.azurerm_resource_group.rg.name
  account_tier                = "Standard"
  account_replication_type    = "LRS"
  public_network_access_enabled = true
}
```

In this example Terraform creates the storage account, but it derives the location and resource group from an existing resource group via the data source. This ensures consistency and prevents duplicating values.

Scenario: Deploying into IT-managed resources

Imagine your IT team manages a resource group and a storage account. You want to deploy additional resources into that same resource group from a separate pipeline without modifying or recreating the IT-managed resources. Use data sources to read the existing resources, then create your own resources that reference them.

Step 1 — Read the existing resource group

```hcl theme={null}
data "azurerm_resource_group" "rg" {
  name = "lifecycle-resources"
}
```

Step 2 — Two common approaches

Option A: Create your own storage account inside the existing resource group

```hcl theme={null}
variable "st_name" {
  type = string
}

resource "azurerm_storage_account" "myst" {
  name                = var.st_name
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  account_tier        = "Standard"
  account_replication_type = "LRS"
}
```

Option B: Reference an existing storage account (managed by IT) and create a blob container inside it

```hcl theme={null}
data "azurerm_storage_account" "storage" {
  name                = "lifecyclestorage5836"
  resource_group_name = data.azurerm_resource_group.rg.name
}

resource "azurerm_storage_container" "reports" {
  name                  = "reports"
  # Prefer using storage_account_id (not storage_account_name) to avoid deprecated arguments
  storage_account_id    = data.azurerm_storage_account.storage.id
  container_access_type = "private"
}
```

Common errors and fixes

| Error                                                                   | Typical cause                                                                          | Fix                                                                                                        |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Reference to undeclared input variable                                  | You referenced a variable (e.g., `st_name`) but did not declare it.                    | Declare the variable: <br />`hcl<br>variable "st_name" { type = string }<br>`                              |
| Invalid resource type (e.g., using `azurerm_storage_account_container`) | Wrong resource name for a blob container.                                              | Use the correct resource: `azurerm_storage_container`. See provider docs for resource names.               |
| Using deprecated arguments                                              | Some resource arguments are deprecated and may be removed in future provider versions. | Use provider-recommended attributes (for example, `storage_account_id` instead of `storage_account_name`). |

Running Terraform in the configuration directory

Initialize the working directory:

```bash theme={null}
terraform init
```

Plan with a variable value (if `st_name` is declared):

```bash theme={null}
terraform plan --var="st_name=myst6878766"
```

Apply (with the same variable):

```bash theme={null}
terraform apply --var="st_name=myst6878766"
```

Example plan output (creating an `azurerm_storage_container`):

```plaintext theme={null}
