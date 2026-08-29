# azurerm_storage_account.example:
resource "azurerm_storage_account" "example" {
  access_tier                       = "Hot"
  account_kind                      = "StorageV2"
  account_replication_type          = "LRS"
  account_tier                      = "Standard"
  allow_nested_items_to_be_public   = true
  cross_tenant_replication_enabled  = false
  default_to_oauth_authentication   = false
  dns_endpoint_type                 = "Standard"
  https_traffic_only_enabled        = true
  id                                 = "/subscriptions/548f7d26-b5b1-4b45-ad45-6ee12accf7e7/resourceGroups/my-workshop-eus-rg/providers/Microsoft.Storage/storageAccounts/sadx98rgffe"
  infrastructure_encryption_enabled = false
}
```

Key points:

* The HCL configuration expresses your declarative intent: attributes you explicitly set.
* The state (what `terraform show` renders) contains computed values, provider defaults, and full resource identifiers—the actual recorded state after `terraform apply`.
* `terraform show` can also render saved plan files (for example, `terraform show plan.tfplan`) so you can inspect a planned change in the same human-readable format.
* For programmatic consumption, use `terraform show -json` to obtain a machine-readable JSON representation of the state or plan.

> **lightbulb** `terraform show` reads the state or a saved plan file and formats it for humans. It reports what is recorded in state or plan—it does not actively query the provider for live resource properties.

In production and enterprise environments, `terraform show` is essential for auditing deployed resource properties, debugging drift against known configuration, and validating that applied infrastructure matches expectations.

## terraform output

`terraform output` retrieves values declared in `output` blocks from the state. Outputs are state-level metadata used to export important values (for example, IP addresses, resource IDs, or endpoints) so they can be consumed by external systems or downstream automation.

Example `output` block in `main.tf`:

```hcl theme={null}
# ----- main.tf -----
output "public_ip_address" {
  description = "The public IP address of the deployed resource"
  value       = azurerm_public_ip.public_ip_address
}
```

Run `terraform output` to display exported values:

```bash theme={null}
$ terraform output
public_ip_address = "13.92.100.148"
```

Useful flags and variations:

* `terraform output -json` — produces machine-readable JSON suitable for CI/CD pipelines and scripts.
* `terraform output <NAME>` — prints a single output value by name.
* Sensitive outputs: mark outputs with `sensitive = true` in your configuration to avoid displaying secrets in interactive output. Note how you handle sensitive outputs in automation and logs.

> **lightbulb** Use `terraform output` (and `terraform output -json`) in CI/CD pipelines to retrieve values from state (for example, IPs or resource IDs) and pass them to downstream steps like configuration management, DNS updates, or deployment scripts.

## Command quick reference

|                     Command | Purpose                                             | Common Flags / Notes                                                           |
| --------------------------: | --------------------------------------------------- | ------------------------------------------------------------------------------ |
|            `terraform show` | Render a state or saved plan in human-readable form | Use `terraform show -json` for machine-readable output; can read `plan.tfplan` |
| `terraform show <planfile>` | Inspect a saved plan file                           | Great for reviewing a planned change before apply                              |
|          `terraform output` | List exported output values from state              | Shows all non-sensitive outputs in readable format                             |
|    `terraform output -json` | Machine-readable outputs                            | Ideal for automation scripts and CI/CD systems                                 |
|   `terraform output <name>` | Print a single output value                         | Useful in shell scripts when you only need one value                           |

## Best practices

* Keep `output` blocks minimal and purposeful—export only what downstream consumers require.
* Avoid exporting secrets; if you must, mark them as `sensitive = true` and secure access to state.
* Use `terraform show -json` or `terraform output -json` when integrating with automation to avoid brittle parsing of human-readable output.
* Rely on these commands for auditing and debugging; remember they reflect Terraform's recorded state (or saved plan), not necessarily the current live provider state.

## Summary

* `terraform show` provides full visibility into the state or a saved plan in a human-readable format, including computed attributes and provider defaults.
* `terraform output` returns a controlled set of exported values defined by `output` blocks in your configuration—these are the stable interface between Terraform and external systems or modules.
* Both are read-only inspection tools that are essential for auditing, debugging, and integrating Terraform into automation workflows.

Links and references:

* [Terraform CLI docs — show](https://www.terraform.io/cli/commands/show)
* [Terraform CLI docs — output](https://www.terraform.io/cli/commands/output)
* [Terraform State](https://www.terraform.io/language/state)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/40bbea76-b88f-4725-b14f-e1fe5d46b8d4)


# Terraform State and Refresh

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-CLI/Terraform-State-and-Refresh/page

Explains Terraform state concepts, inspection and management commands, and how to refresh state to reconcile drift without changing infrastructure.

In this lesson we'll examine Terraform state: what it contains, how to inspect it, and how to refresh it when infrastructure changes outside of Terraform. We previously wrote configuration and applied it — Terraform's true power comes from how it tracks resources in state. Here we'll learn how to view that state, perform safe state maintenance, and reconcile Terraform's view with the actual provider.

## What is Terraform state?

Terraform stores a state file that serves as the authoritative record of resources Terraform manages. This file contains the mapping between resource addresses in your configuration and the actual provider-managed resources (IDs, computed attributes, metadata). Terraform relies on state to plan changes and detect drift.

## Inspecting state

Use the `terraform state` family of commands to inspect and manage the state. To see all tracked resources:

```bash theme={null}
$ terraform state list
azurerm_storage_account.example
```

To view detailed attributes for a single tracked resource:

```bash theme={null}
$ terraform state show azurerm_storage_account.example
