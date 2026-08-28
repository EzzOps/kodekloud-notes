# ignore changes

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Lifecycle-Meta-Arguments/ignore-changes/page

Explains Terraform lifecycle ignore_changes to prevent reconciliation of externally managed resource attributes such as tags, avoiding noisy plans while still detecting drift.

In this lesson we examine Terraform's lifecycle meta-argument `ignore_changes` and how it controls drift handling between your configuration and real infrastructure.

Unlike `prevent_destroy`, `ignore_changes` does not block deletion. Unlike `create_before_destroy`, it does not change replacement ordering. Instead, `ignore_changes` tells Terraform to tolerate specific differences between the resource configuration and the actual infrastructure — effectively controlling which attribute drift Terraform should not reconcile.

Key behaviors

* `ignore_changes` causes Terraform to detect differences but deliberately avoid acting on them for the specified attributes.
* Terraform will still refresh state and show the differences; it just won’t include those attributes in planned changes.
* This is most useful when an attribute is managed outside Terraform (for example by Azure Policy or another automation tool) and you want to avoid continual, unnecessary diffs.

<Frame>
  <img alt="The image describes two functions of a Terraform feature: ignoring drift on certain attributes and managing attributes outside Terraform." />
</Frame>

When to use `ignore_changes`

A common scenario is platform-level governance applying tags or other properties to resources. For example, Azure Policy may automatically apply or mutate tags. If Terraform also declares tags in the configuration, Terraform will detect those policy-applied tags as drift and will attempt to reconcile them back to the configuration, causing constant diffs and noisy plans. Using `ignore_changes` for the `tags` attribute prevents Terraform from trying to overwrite values that are intentionally controlled by an external system.

<Frame>
  <img alt="The image illustrates a scenario about ensuring that an Azure Policy for automatically tagging resources isn't overridden by Terraform, accompanied by the logos for Azure and Terraform." />
</Frame>

Example — storage account

1. Without `ignore_changes`

This resource config declares tags in Terraform. If Azure Policy or another process applies different tags, Terraform will plan an in-place update to match the configuration:

```hcl theme={null}
resource "azurerm_storage_account" "example" {
  name                     = var.storage_account_name
  location                 = "East US"
  resource_group_name      = "rg-workshop-riskaria"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  public_network_access_enabled = true

  tags = {
    "Added from" = "Terraform"
  }
}
```

Example abbreviated plan output showing a tags diff:

```bash theme={null}
