# main.tf
output "public_ip_address" {
  description = "The public IP address of the deployed resource"
  value       = azurerm_public_ip.public_ip.ip_address
}

# outputs.tf
output "publicip_address" {
  description = "The public IP address of the deployed resource"
  value       = azurerm_public_ip.public_ip.ip_address
}
```

## Plan and apply behavior

During `terraform plan`, attributes that Terraform cannot compute until apply are shown as `(known after apply)`. Outputs referencing such attributes will also be reported as `(known after apply)` in the plan.

Example (condensed):

```plaintext theme={null}
$ terraform apply -auto-approve

Plan: 2 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + public_ip_address = (known after apply)

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:
public_ip_address = "13.92.100.148"
```

## Retrieve outputs

After `apply` you can fetch outputs at any time:

* `terraform output` — lists all outputs
* `terraform output <name>` — shows a single output value
* `terraform show` — displays the full state; outputs appear in the Outputs section

Examples:

```bash theme={null}
$ terraform output
public_ip_address = "13.92.100.148"
```

```bash theme={null}
$ terraform show
Outputs:
public_ip_address = "13.92.100.148"
```

Note: Outputs are stored in the Terraform state. Terraform prints them after `apply`, and subsequent `terraform output` reads values from state (not by re-querying the provider).

<Callout icon="lightbulb">
  Outputs are stored in the Terraform state file. If an output contains sensitive information, mark it with `sensitive = true` to avoid printing it to the CLI by default.
</Callout>

<Callout icon="warning">
  Do not expose secrets via outputs unless absolutely necessary. Use `sensitive = true` and restrict access to your remote state backend.
</Callout>

## Output arguments reference (quick)

|      Argument | Purpose                                           | Example                                |
| ------------: | ------------------------------------------------- | -------------------------------------- |
|       `value` | Expression to evaluate and store as the output    | `azurerm_public_ip.pip.ip_address`     |
| `description` | Human-readable description                        | `"Public IP for demo"`                 |
|   `sensitive` | Hides output from CLI unless explicitly requested | `sensitive = true`                     |
|  `depends_on` | (Rare) Force output evaluation order              | `depends_on = [azurerm_public_ip.pip]` |

## Using outputs in a workflow — step-by-step demo

Below is a concise walkthrough to create resources and outputs in a workspace.

1. Create a new folder (for example, `outputs`) and add your Terraform configuration.

Example resources: a resource group and a storage account:

```hcl theme={null}
# main.tf
resource "azurerm_resource_group" "rg" {
  name     = "kodekloud-tf-output-rg"
  location = "eastus"
}

resource "azurerm_storage_account" "sa" {
  name                = "storagedrt6673623"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  sku {
    name = "Standard_LRS"
  }

  kind = "StorageV2"
}
```

2. (Optional) Target a specific resource for exceptional cases (recovery, incremental testing). Use `-target` with care — Terraform will warn that the plan may be incomplete.

```bash theme={null}
terraform apply --target="azurerm_storage_account.sa"
```

Example warning the CLI shows when using `-target`:

```plaintext theme={null}
Warning: Applied changes may be incomplete

The plan was created with the -target option in effect, so some changes requested in the configuration may have been ignored and the output values may not be fully updated. Run `terraform plan` to verify.
```

3. Add a public IP resource and create an output for the IP address.

```hcl theme={null}
# main.tf (continued)
resource "azurerm_public_ip" "pip" {
  name                = "kodekloud-tf-pip"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  allocation_method   = "Static"
}
```

4. Consult the provider/resource documentation to learn which attributes are exported. For AzureRM `azurerm_public_ip` the exported attributes include `id`, `ip_address`, and (if applicable) `fqdn`. See the AzureRM docs for details: [https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]/resources/public\_ip](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]/resources/public_ip)

<Frame>
  <img alt="This is a screenshot of the AzureRM documentation for Terraform, focusing on the configuration of a public IP resource. It includes parameter options, notes, and attribute references related to the setup." />
</Frame>

5. Create `outputs.tf` and define the output using the attribute discovered in the docs:

```hcl theme={null}
# outputs.tf
output "pip" {
  description = "The public IP address for the public IP resource"
  value       = azurerm_public_ip.pip.ip_address
}
```

If the output must not be printed to the console (for example, a connection string), mark it as sensitive:

```hcl theme={null}
output "storage_connection_string" {
  description = "Primary connection string for storage account (sensitive)"
  value       = azurerm_storage_account.sa.primary_connection_string
  sensitive   = true
}
```

6. Initialize, plan, and apply:

```bash theme={null}
$ terraform init
$ terraform plan -out tfplan
# Plan will show pip = (known after apply)
$ terraform apply "tfplan"
```

Condensed apply output:

```plaintext theme={null}
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:
pip = "52.188.13.188"
```

## Common CLI commands

|                      Command | Purpose                                    |
| ---------------------------: | ------------------------------------------ |
|             `terraform init` | Initialize working directory and providers |
| `terraform plan -out=tfplan` | Generate a plan and save it to a file      |
|   `terraform apply "tfplan"` | Apply a saved plan                         |
|           `terraform output` | Display all outputs from state             |
|    `terraform output <name>` | Display a specific output value            |
|             `terraform show` | Display entire state and outputs           |

## Verification

Cross-check the printed public IP in the Azure Portal: [https://portal.azure.com](https://portal.azure.com) — navigate to the resource group and the `Public IP` resource to confirm the allocation matches the Terraform output.

## Summary

Terraform outputs let you expose runtime values for humans and automation. Use outputs to:

* Export values only known after creation (IP addresses, IDs, FQDNs).
* Provide connection details or metadata to scripts and CI/CD pipelines.
* Keep outputs organized in `outputs.tf` for clarity.

Always mark secrets with `sensitive = true` and protect access to your state backend. For more provider-specific exported attributes, consult the provider docs such as the AzureRM `azurerm_public_ip` resource: [https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]/resources/public\_ip](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]/resources/public_ip).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/866718d2-695e-4ee4-b25d-1aab3b014e85/lesson/4f867dbb-d2bf-4977-9131-29ea7d316d0a" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/866718d2-695e-4ee4-b25d-1aab3b014e85/lesson/cae027d8-660f-43d0-9f8a-2f517abe92a8" />
</CardGroup>


# Resource Attributes and Dependencies

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Outputs-and-Dependencies/Resource-Attributes-and-Dependencies/page

Explains how Terraform uses resource attribute references and depends_on to build dependency graphs and control Azure resource creation order, avoiding race conditions

This article explains how Terraform resources relate to each other, how values flow between resources, and how Terraform decides the order in which resources are created. Understanding these concepts is essential for reliable Azure deployments: most resources are not standalone—a subnet belongs to a VNet, a storage account lives in a resource group, and VMs depend on networking, disks, and identities.

After reading this article you will clearly understand:

* How Terraform builds its dependency graph.
* When dependencies are discovered implicitly (via attribute references).
* When you must be explicit using `depends_on`.

Basic VNet + Subnet example

<Frame>
  /images/Python\_Basics/section-name/Comments/frame\_100.jpg
</Frame>

A virtual network (VNet) exposes attributes such as `name`, `address_space`, `location`, and `resource_group_name`. A subnet that belongs to that VNet should reference the VNet resource rather than hard-coding values. Referencing resource attributes lets Terraform both pass values and infer the ordering between resources (an implicit dependency).

Example — VNet and Subnet with attribute references (implicit dependency):

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = var.rg
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location   # implicit dependency on resource group
  resource_group_name = azurerm_resource_group.rg.name       # implicit dependency on resource group
}

resource "azurerm_subnet" "subnet" {
  name                 = var.subnet
  resource_group_name  = azurerm_resource_group.rg.name      # implicit dependency on resource group
  virtual_network_name = azurerm_virtual_network.vnet.name  # implicit dependency on vnet
  address_prefixes     = ["10.0.1.0/24"]
}
```

Key points

* When the `azurerm_subnet` block references `azurerm_virtual_network.vnet.name`, Terraform obtains that attribute value and also infers that the subnet depends on the VNet. This is an implicit dependency.
* Attribute references both pass configuration values and create ordering information in Terraform’s dependency graph.
* If you hard-code values or rely only on variables (for example `resource_group_name = var.rg`), Terraform cannot infer a dependency between the resources and may attempt parallel creation.

Why reference the resource group in each resource?

* Terraform can create independent-looking resources in parallel. If a resource must be created inside a resource group but you supply only a variable (which is known at plan time), Terraform has no relationship to infer and may run creations concurrently. Referencing the resource group's attributes (for example `azurerm_resource_group.rg.name`) makes the dependency explicit to Terraform (implicitly).

Implicit dependencies are sufficient in most scenarios

<Frame>
  /images/Python\_Basics/section-name/Comments/frame\_100.jpg
</Frame>

Consider a resource group and a storage account; because the storage account references attributes from the resource group, Terraform ensures the resource group is created first.

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "my-workshop-rg-wus"
  location = "West US"
}

resource "azurerm_storage_account" "sa" {
  name                     = "saworkshopazuretf098"
  resource_group_name      = azurerm_resource_group.rg.name   # implicit dependency on rg
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

When depends\_on is required (explicit dependency)

* Use `depends_on` when a logical dependency exists but Terraform cannot infer it through attribute references.
* Common cases requiring `depends_on`: role assignments, policy assignments, diagnostic settings, private endpoints, resource associations, or provider behaviors where an ID is returned but the resource is not fully ready for dependent operations.

Example: NSG-to-subnet association that needs `depends_on` to handle Azure eventual consistency:

```hcl theme={null}
resource "azurerm_network_security_group" "nsg" {
  name                = var.nsg
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

resource "azurerm_subnet" "subnet" {
  name                 = var.subnet
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet_network_security_group_association" "subnet_nsg_assoc" {
  subnet_id                 = azurerm_subnet.subnet.id
  network_security_group_id = azurerm_network_security_group.nsg.id

  # Force ordering when Azure's eventual consistency requires both resources to be fully ready
  depends_on = [
    azurerm_subnet.subnet,
    azurerm_network_security_group.nsg,
  ]
}
```

<Callout icon="lightbulb">
  Use `depends_on` sparingly — only when Terraform cannot infer the dependency. Overusing `depends_on` makes configurations harder to read and less flexible. Always ask: is an attribute reference already providing the dependency?
</Callout>

A typical example configuration (main.tf)

<Frame>
  /images/Python\_Basics/section-name/Comments/frame\_100.jpg
</Frame>

A compact main configuration that creates a resource group, virtual network, subnet, network security group (NSG), and the subnet-to-NSG association. This demonstrates implicit references plus a `depends_on` used for the association.

```hcl theme={null}
