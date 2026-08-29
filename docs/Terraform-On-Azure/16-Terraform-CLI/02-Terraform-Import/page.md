# Terraform Import

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-CLI/Terraform-Import/page

Guide on using terraform import to bring existing cloud resources into Terraform state, including Azure ID formats, workflow, examples, and best practices

This guide explains how to bring existing infrastructure under Terraform management using the `terraform import` command. It covers the required arguments, Azure-specific ID formats, example usage, a recommended import workflow, and best practices to avoid surprises after importing resources.

## What `terraform import` does (and does not do)

* `terraform import` connects an existing real resource to a declared resource block in your Terraform state.
* It does not generate HCL configuration, nor does it create, modify, or destroy the remote resource.
* After a successful import, the resource's attributes are recorded in the Terraform state and Terraform will manage it going forward.

## Required arguments

The import command expects two positional arguments:

1. ADDR — the resource address in your Terraform configuration (must already exist in your `.tf` files). Example: `azurerm_storage_account.example`.
2. ID — the provider-specific identifier of the real resource (format depends on provider).

Example syntax:

```bash theme={null}
terraform import ADDR ID
```

## ADDR vs ID — quick comparison

| Item | Description                                                              | Example                                                                                                                         |
| ---- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| ADDR | Terraform resource address declared in HCL                               | `azurerm_storage_account.example`                                                                                               |
| ID   | Provider-specific identifier used by the provider to locate the resource | `/subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/STORAGE_ACCOUNT_NAME` |

For Azure resources the ID is typically the full Azure Resource Manager (ARM) ID shown above.

## Example: import an Azure Storage Account

Run the import using the HCL resource address and the ARM resource ID:

```bash theme={null}
terraform import azurerm_storage_account.example /subscriptions/SUBSCRIPTION_ID/resourceGroups/rg1/providers/Microsoft.Storage/storageAccounts/stacct1
```

## Trimmed help text (reference)

```bash theme={null}
$ terraform import
The import command expects two arguments.
Usage: terraform [global options] import [options] ADDR ID

Import existing infrastructure into your Terraform state.

This will find and import the specified resource into your Terraform
state, allowing existing infrastructure to come under Terraform
management without having to be initially created by Terraform.

The ADDR specified is the address to import the resource to. Please
see the documentation online for resource addresses. The ID is a
resource-specific ID to identify that resource being imported. Please
reference the documentation for the resource type you're importing to
determine the ID syntax to use. It typically matches directly to the ID
that the provider uses.

This command will not modify your infrastructure, but it will make
network requests to inspect parts of your infrastructure relevant to
the resource being imported.
```

## Recommended import workflow (step-by-step)

1. Ensure the Terraform configuration contains a resource block that matches the resource type you intend to import. `terraform import` does not create this block for you.
2. Confirm the correct provider-specific ID format from provider docs (for Azure, use the ARM resource ID).
3. Run `terraform import ADDR ID`.
4. Immediately run `terraform plan` to detect any differences (drift) between the imported state and your HCL.
5. Reconcile your HCL: update default values, add missing attributes, or change values to reflect the desired configuration.
6. Run `terraform plan` again until the plan shows only intended changes, then `terraform apply` to persist any HCL-driven changes (if required).

> **lightbulb** Note: `terraform import` is especially useful when adopting Terraform in a brownfield environment, recovering a lost state file, or migrating manually created resources into infrastructure-as-code without causing downtime or recreation.

## Best practices and important clarifications

* The resource block must exist in the configuration before importing. Terraform will not generate HCL for you.
* After import, the imported resource's state attributes may differ from the configuration; always run `terraform plan` and reconcile differences.
* Import only affects the state file; it does not change configuration files or the remote resource.
* Use provider documentation to determine the correct ID format for imports. For Azure, this is usually the ARM resource ID.
* Consider using separate branches and state backups when importing multiple resources to reduce risk.

## Tools and further resources

* Azure: Microsoft maintains a tool called `aztfexport` which can help convert existing Azure infrastructure into HCL and assist in generating Terraform configuration for larger migrations: [https://github.com/Azure/aztfexport](https://github.com/Azure/aztfexport)
* Terraform docs: [https://www.terraform.io/docs/cli/commands/import.html](https://www.terraform.io/docs/cli/commands/import.html)
* Azure Resource Manager ID docs: [https://learn.microsoft.com/azure/azure-resource-manager/management/resource-name-rules](https://learn.microsoft.com/azure/azure-resource-manager/management/resource-name-rules)

> **lightbulb** Note: After importing, reconcile your configuration with the imported state and run `terraform plan` and `terraform apply` only when you have verified the intended changes.

This completes the coverage of `terraform import`. It is the primary CLI command for bringing existing resources into Terraform state when adopting infrastructure-as-code in environments that already have resources provisioned.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/ac123bd0-ef89-44d6-a213-ab8d3f0b9d90)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/0582c65c-d487-4819-b7c5-9aafe16ba6d7)
