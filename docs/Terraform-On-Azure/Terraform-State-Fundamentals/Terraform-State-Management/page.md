# Terraform State Management

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-State-Fundamentals/Terraform-State-Management/page

Explains Terraform state management, its contents, local versus remote backends, security and collaboration considerations, and using remote storage for team workflows.

Now that we understand what Terraform state is, let’s examine how Terraform manages state in practice and why it matters for collaboration, safety, and incremental updates.

<Frame>
  <img alt="The image features the text &#x22;Terraform State Management&#x22; with a minimalist design, including a gradient blue shape on a white background." />
</Frame>

## Example: A simple Azure Storage Account

Here is a minimal `azurerm_storage_account` resource using a `variable` for the storage account name:

```hcl theme={null}
resource "azurerm_storage_account" "sa" {
  name                      = var.storage_account_name
  location                  = "East US"
  resource_group_name       = "my-workshop-eus-rg"
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}

variable "storage_account_name" {
  type        = string
  description = "Name of the Azure Storage Account"
}
```

When you run `terraform apply` and pass the storage account name, Terraform does two things:

* Creates (or updates) the resource in Azure.
* Writes a local state file called `terraform.tfstate` (by default).

You do not create this file manually—Terraform manages it automatically.

Example apply and local state output:

```bash theme={null}
$ terraform apply -var "storage_account_name=sfx097674"
