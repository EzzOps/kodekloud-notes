# main.tf
resource "azurerm_resource_group" "rg" {
  name     = var.rg
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet" {
  name                 = var.subnet
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "nsg" {
  name                = var.nsg
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

resource "azurerm_subnet_network_security_group_association" "subnet_nsg_assoc" {
  subnet_id                 = azurerm_subnet.subnet.id
  network_security_group_id = azurerm_network_security_group.nsg.id

  # Optional: ensure the subnet and NSG are fully provisioned before making the association
  depends_on = [
    azurerm_subnet.subnet,
    azurerm_network_security_group.nsg
  ]
}
```

Provider and variables files

<Frame>
  /images/Python\_Basics/section-name/Comments/frame\_100.jpg
</Frame>

Minimal `provider.tf` and `variables.tf` for the example:

```hcl theme={null}
# provider.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

```hcl theme={null}
# variables.tf
variable "rg" {
  type        = string
  description = "Resource group name"
}

variable "location" {
  type        = string
  description = "Azure location"
}

variable "vnet" {
  type        = string
  description = "Virtual network name"
}

variable "subnet" {
  type        = string
  description = "Subnet name"
}

variable "nsg" {
  type        = string
  description = "Network Security Group name"
}
```

Example `terraform.tfvars` used to pass values:

```hcl theme={null}
# terraform.tfvars
rg       = "rg-tf-dependencies-01"
location = "eastus"
vnet     = "vnet-tf-dependencies-01"
subnet   = "subnet-tf-dependencies-01"
nsg      = "nsg-tf-dependencies-01"
```

Commands: init, plan, apply

<Frame>
  /images/Python\_Basics/section-name/Comments/frame\_100.jpg
</Frame>

From the directory with your Terraform files:

```bash theme={null}
terraform init
terraform plan -out tfplan
terraform apply --auto-approve tfplan
```

Example (cleaned) output showing correct ordering:

```plaintext theme={null}
azurerm_resource_group.rg: Creating...
azurerm_resource_group.rg: Creation complete after 25s [id=/subscriptions/.../resourceGroups/rg-tf-dependencies-01]
azurerm_virtual_network.vnet: Creating...
azurerm_network_security_group.nsg: Creating...
azurerm_virtual_network.vnet: Creation complete after 4s [id=/subscriptions/.../virtualNetworks/vnet-tf-dependencies-01]
azurerm_network_security_group.nsg: Creation complete after 6s [id=/subscriptions/.../networkSecurityGroups/nsg-tf-dependencies-01]
azurerm_subnet.subnet: Creating...
azurerm_subnet.subnet: Creation complete after 7s [id=/subscriptions/.../subnets/subnet-tf-dependencies-01]
azurerm_subnet_network_security_group_association.subnet_nsg_assoc: Creating...
azurerm_subnet_network_security_group_association.subnet_nsg_assoc: Creation complete after 5s
Apply complete! Resources: 5 added, 0 changed, 0 destroyed.
```

Explanation of the observed order

* The resource group is created first because other resources reference it.
* The VNet and NSG were created in parallel after the resource group because both depend only on the resource group (implicit dependency).
* The subnet waited for the VNet to be created (implicit dependency via `virtual_network_name`).
* The subnet-to-NSG association was applied last; even with attribute references, a `depends_on` can be used to guard against Azure timing issues.

Quick reference table: dependency discovery

| Resource(s)                      | Example attribute reference                                |                                Dependency discovered? | Notes                                                                          |
| -------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------: | ------------------------------------------------------------------------------ |
| Resource Group → Storage Account | `resource_group_name = azurerm_resource_group.rg.name`     |                                        Yes (implicit) | Attribute reference creates ordering.                                          |
| VNet → Subnet                    | `virtual_network_name = azurerm_virtual_network.vnet.name` |                                        Yes (implicit) | Standard pattern for network resources.                                        |
| Subnet NSG Association           | `subnet_id = azurerm_subnet.subnet.id`                     | Often yes (implicit), but may still need `depends_on` | Use `depends_on` when Azure returns IDs before the resource is actually ready. |
| Role or Policy Assignments       | `principal_id = ...` (no direct attribute linking)         |                            No (requires `depends_on`) | Provider-specific eventual consistency can require explicit ordering.          |

<Callout icon="warning">
  Do not overuse `depends_on`. Using it everywhere defeats Terraform’s automatic dependency tracking, reduces parallelism, and makes configurations harder to maintain. Use `depends_on` only when you observe failures caused by provider eventual consistency or when there is no attribute reference to express the relationship.
</Callout>

Summary

* Attribute references (for example `azurerm_resource_group.rg.name` or `azurerm_virtual_network.vnet.id`) allow values to flow between resources and automatically create implicit dependencies.
* Terraform builds a dependency graph from those references and uses it to determine the correct creation order.
* Use `depends_on` only when Terraform cannot infer a dependency from attribute references (for example, associations or operations that require a resource to be fully provisioned even when an ID is already available).
* Avoid overusing `depends_on` to keep configurations readable, maintainable, and parallel where possible.

Understanding these mechanisms prevents race conditions and broken deployments in real production environments.

Links and references

* [Terraform CLI Docs](https://www.terraform.io/docs/cli)
* [Terraform Dependency Graph](https://www.terraform.io/docs/internals/graph.html)
* [Azure Provider (azurerm) on Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
* [Azure Resource Manager documentation](https://learn.microsoft.com/azure/azure-resource-manager/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/866718d2-695e-4ee4-b25d-1aab3b014e85/lesson/70d3a770-63fb-430a-8bbc-278664ed87b1" />
</CardGroup>


# Resource Targeting

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Outputs-and-Dependencies/Resource-Targeting/page

Explains Terraform resource targeting using -target, its use cases for recovery, debugging, and drift fixes, risks of inconsistent state, examples, and best practice guidance.

Resource targeting in Terraform lets you limit an operation (plan or apply) to specific resource(s) instead of evaluating the entire configuration. This is an advanced feature intended for exceptional situations such as recovery, debugging, or fixing drift. Misusing it can leave your infrastructure in an inconsistent or unsafe state, so read carefully.

What resource targeting does:

* Runs Terraform only against the targeted resource(s) and their dependency chain.
* Is invoked with the `-target` flag on `terraform plan` or `terraform apply`.
* Is not a performance optimization; it skips evaluating unrelated parts of the configuration and can therefore produce incomplete results.

Example command:

```bash theme={null}
terraform apply -target=azurerm_storage_container.container
```

<Frame>
  <img alt="The image is an infographic titled &#x22;Resource Targeting,&#x22; featuring three sections: &#x22;Targeting,&#x22; &#x22;Recovery or Debugging,&#x22; and &#x22;Skip Checks,&#x22; each with a brief description of their purpose." />
</Frame>

Call out the risk: if you skip evaluation of other configuration parts, ensure you are not skipping anything critical that could affect the overall deployment.

When to use resource targeting

Use resource targeting only in narrow scenarios where you understand the consequences. Common valid use cases include:

| Use case                | When to use                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Retry a failed resource | A transient API error caused a single resource to fail during apply; you want to retry only that resource.       |
| Debugging               | A resource repeatedly fails; target it to iterate quickly without evaluating the rest of the configuration.      |
| Drift correction        | You know exactly which resource drifted from its Terraform-managed state and want to reapply only that resource. |

<Frame>
  <img alt="The image describes &#x22;Resource Targeting&#x22; with three options: Retry, Debug, and Drift, each with a brief explanation about when to use them." />
</Frame>

Example: resource group, storage account, and container

Below is a minimal example showing a resource group, a storage account that depends on the group, and a container that depends on the storage account.

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "target-demo-rg"
  location = "East US"
}

resource "azurerm_storage_account" "sa" {
  name                     = "targetstoragedemo"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                  = "tfcontainer"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}
```

Under normal operation Terraform evaluates the full dependency graph and creates or updates resources in the correct order. If you run:

```bash theme={null}
terraform apply -target=azurerm_storage_container.container
```

Terraform will plan and apply only the container resource and any resources required to create it (in this example, the storage account and resource group if they do not already exist). This can be useful when the container creation previously failed and you want to retry only that resource.

Why resource targeting is dangerous

Resource targeting may skip planned changes to related resources such as account configuration, policy assignments, network rules, or security settings. Even if the targeted resource is created or updated successfully, the overall infrastructure might become inconsistent.

<Callout icon="warning">
  Resource targeting is intended for recovery, debugging, or drift-fix scenarios only. Do not use it for initial deployments, CI/CD pipelines, or regular day-to-day applies. If you care about correctness and safety, run a normal `terraform apply` (or `terraform apply` on a saved plan).
</Callout>

Practical scenario: retrying or fixing a single resource after a runtime error

Case: you create a storage account, but the chosen account name is globally unique and already taken by another subscription. The plan phase can succeed, because Terraform does not detect the global uniqueness constraint; the failure occurs during apply when Azure rejects the creation.

Example HCL that will fail during apply (name intentionally invalid for demonstration):

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "kodekloud-tf-target-rg"
  location = "eastus"
}

resource "azurerm_storage_account" "sa" {
  name                     = "storage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

Typical workflow:

1. Initialize:

```bash theme={null}
terraform init
```

2. Create a plan:

```bash theme={null}
terraform plan -out=tfplan
```

3. Apply the plan:

```bash theme={null}
terraform apply "tfplan"
```

You might see an apply-time error like:

```plaintext theme={null}
Error: creating Storage Account (Subscription: "1b228746-75fd-46ed-8a6b-6a9066d6d3a3"
Resource Group Name: "kodekloud-tf-target-rg"
Storage Account Name: "storage"): performing Create: unexpected status 409 (409 Conflict) with error: StorageAccountAlreadyTaken: The storage account named storage is already taken.

  with azurerm_storage_account.sa,
  on main.tf line 6, in resource "azurerm_storage_account" "sa":
   6: resource "azurerm_storage_account" "sa" {
```

Fix the configuration by choosing a unique storage account name:

```hcl theme={null}
resource "azurerm_storage_account" "sa" {
  name                     = "storagedrt6673623"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

Then apply only the storage account (Terraform will also include any dependencies required to create it):

```bash theme={null}
terraform apply -target=azurerm_storage_account.sa
```

When you run the targeted apply, Terraform shows a concise plan covering just the targeted resource (and required dependencies). It will also display a warning that the plan was created with `-target`, for example:

```plaintext theme={null}
Plan: 1 to add, 0 to change, 0 to destroy.

Warning: Resource targeting is in effect
You are creating a plan with the -target option, which means that the result of this plan may not represent all of the changes requested by the current configuration.
...
Do you want to perform these actions?
Only 'yes' will be accepted to approve.
```

Best practices and final rules

* Use `-target` only for recovery, debugging, or drift correction—and only when you understand the implications.
* Never use resource targeting for:
  * Initial provisioning
  * CI/CD pipelines
  * Regular operations as a performance shortcut
* Prefer creating and applying a full plan (`terraform plan` + `terraform apply`) when correctness matters.
* If you must target, document the action and follow up with a full plan/apply afterward to ensure consistency.

Additional references

* HashiCorp: Resource Targeting documentation — [https://www.terraform.io/cli/commands/plan#target](https://www.terraform.io/cli/commands/plan#target)
* Azure naming rules and storage account limitations — [https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview#naming-rules](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview#naming-rules)

If you fully understand the impact and need to recover or debug, targeting can be a useful, narrowly scoped tool. Otherwise, rely on Terraform to manage the full dependency graph so your infrastructure remains consistent.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/866718d2-695e-4ee4-b25d-1aab3b014e85/lesson/3e959249-df4f-49eb-b294-78bc63c77a63" />
</CardGroup>
