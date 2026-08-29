# Terraform Show and Output

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-CLI/Terraform-Show-and-Output/page

Explains Terraform's show and output commands for inspecting state and plans, usage patterns, JSON flags, and best practices for automation, debugging, and exporting values.

In this lesson we focus on two practical Terraform CLI inspection commands: `terraform show` and `terraform output`.

You have likely encountered these commands during day-to-day Terraform usage. Here we formalize their roles from a state-inspection perspective, show common usage patterns, and explain how they fit into automation and debugging workflows.

## terraform show

`terraform show` reads a Terraform state file (local or remote) or a saved plan file and renders its contents in a human-readable format. Because Terraform stores state as JSON, `terraform show` is the convenient way to inspect what Terraform knows about resources without parsing raw JSON yourself.

Example resource declaration (the declared intent in HCL):

```hcl theme={null}
resource "azurerm_storage_account" "example" {
  name                          = var.storage_account_name
  location                      = "East US"
  resource_group_name           = "my-workshop-eus-rg"
  account_tier                  = "Standard"
  account_replication_type      = "LRS"
  public_network_access_enabled = false
}
```

When you run `terraform show` against the applied state, Terraform renders the resource including computed attributes, provider defaults, and the full resource ID that were not explicitly declared in configuration. For example:

```bash theme={null}
$ terraform show
