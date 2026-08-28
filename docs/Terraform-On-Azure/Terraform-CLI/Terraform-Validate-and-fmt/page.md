# azurerm_storage_account.example:
resource "azurerm_storage_account" "example" {
  access_tier                      = "Hot"
  account_kind                     = "StorageV2"
  account_replication_type         = "LRS"
  account_tier                     = "Standard"
  allow_nested_items_to_be_public  = true
  cross_tenant_replication_enabled = false
  default_to_oauth_authentication  = false
  dns_endpoint_type                = "Standard"
  https_traffic_only_enabled       = true

  id = "/subscriptions/548f7d26-b5b1-468e-ad45-6ee12accf7e7/resourceGroups/my-workshop-eus-rg/providers/Microsoft.Storage/storageAccounts/sadx98rgffe"
}
```

The `state show` output includes both configuration-declared attributes and provider-populated fields (IDs, defaults, and runtime properties). This detailed view is essential for debugging, auditing, and preparing precise state changes.

## State management subcommands

The `terraform state` command exposes subcommands for advanced state maintenance. Terraform automatically creates a timestamped backup of state before any operation that modifies it. Below is a concise reference:

| Subcommand         | Purpose                                                               | Example                                                                                                  |
| ------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `list`             | List resources recorded in state                                      | `terraform state list`                                                                                   |
| `show`             | Print detailed state for a single resource                            | `terraform state show azurerm_storage_account.example`                                                   |
| `mv`               | Move a resource address within state (useful when refactoring)        | `terraform state mv old.resource new.resource`                                                           |
| `rm`               | Remove instances from state without destroying remote resources       | `terraform state rm module.foo.azurerm_resource.bar`                                                     |
| `replace-provider` | Replace provider references in state (for provider namespace changes) | `terraform state replace-provider registry.terraform.io/old/provider registry.terraform.io/new/provider` |
| `pull`             | Pull the current state and output to stdout (for manual inspection)   | `terraform state pull`                                                                                   |
| `push`             | Update remote state from a local state file (special workflows)       | `terraform state push terraform.tfstate`                                                                 |

The commands are intentionally simple and script-friendly (work well with grep, awk, etc.) for advanced automation and auditing.

<Callout icon="warning">
  State modification commands can cause drift between Terraform and your real infrastructure if used incorrectly. Always work against a backup and prefer non-destructive commands unless you fully understand the implications.
</Callout>

## Refreshing state

<Frame>
  <img alt="The image contains the text &#x22;Terraform Refresh&#x22; with a copyright notice for KodeKloud at the bottom left." />
</Frame>

Terraform expects the state file to reflect reality. When resources are modified outside Terraform (console edits, manual CLI/API actions, other orchestration tools), the stored state can diverge — this is configuration drift.

Use `terraform refresh` to reconcile Terraform's state with the provider by re-querying resource attributes and updating the state file. Important: `terraform refresh` updates only the state file; it does not change infrastructure.

Example configuration using a variable for the storage account name:

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

Running a refresh (supplying the variable):

```bash theme={null}
$ terraform refresh -var "storage_account_name=sadx98rgffe"
azurerm_storage_account.example: Refreshing state...
  [id=/subscriptions/548f7d26-b5b1-468e-ad45-6ee12accf7e7/resourceGroups/my-workshop-eus-rg/providers/Microsoft.Storage/storageAccounts/sadx98rgffe]
```

After running, Terraform has fetched the current resource attributes from Azure and updated the local state to match — no remote changes are made.

<Callout icon="lightbulb">
  Modern Terraform performs an automatic refresh during operations like `terraform plan` and `terraform apply`, so manually running `terraform refresh` is less common. Still, it's valuable when resolving drift or preparing for direct state edits.
</Callout>

## Key takeaways

* The Terraform state file is the authoritative record of managed infrastructure.
* Inspect state with `terraform state list` and `terraform state show`.
* Use `terraform state` subcommands for advanced maintenance — Terraform creates backups automatically for safety.
* Run `terraform refresh` to update the state from provider data; it updates only the state file and does not alter resources.
* Be cautious with state-modifying commands; test on non-production state or use backups to recover if needed.

## Links and references

* [Terraform State | HashiCorp Documentation](https://www.terraform.io/docs/state/index.html)
* [Terraform CLI Commands](https://www.terraform.io/docs/commands/index.html)
* [Azure Provider for Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/b55fe31e-bb64-4e13-8a58-102864b8b5a5" />
</CardGroup>


# Terraform Validate and fmt

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-CLI/Terraform-Validate-and-fmt/page

Explains using terraform validate to catch HCL syntax and provider-schema errors and terraform fmt to enforce consistent HCL formatting for local development and CI

This lesson explains how to use `terraform validate` and `terraform fmt` to catch configuration errors early and enforce consistent HCL (HashiCorp Configuration Language) formatting.

## Overview

* `terraform validate` performs static validation of Terraform configuration files. When run after `terraform init`, it loads provider schemas and checks configuration structure and types against those schemas.
* `terraform fmt` reformats HCL files to the canonical style defined by HashiCorp. It changes only formatting (whitespace, indentation) and does not alter any configuration logic.

Both commands are fast and lightweight and are ideal for local development checks and CI pipelines.

## terraform validate — static validation (syntax + provider schema)

`terraform validate` parses your configuration, checks HCL syntax, and — if you previously ran `terraform init` — uses provider schemas to validate resource and argument names and types.

Important: run `terraform init` first so Terraform can download provider plugins and schema information. Without initialization, `terraform validate` still checks basic HCL syntax but may not catch provider-specific schema errors.

Example: an Azure Storage Account resource with a subtle argument-name typo

```hcl theme={null}
resource "azurerm_storage_account" "example" {
  name                          = var.storage_account_name
  location                      = "East US"
  resource_group_name           = "my-workshop-eus-rg"
  account_tier                  = "Standard"
  account_replication_types     = "LRS"
  public_network_access_enabled = false
}
```

At a glance the block looks valid, but the correct argument name is `account_replication_type` (singular). The typo results in a missing required argument plus an unsupported unexpected argument. After running `terraform init` and `terraform validate`, Terraform will detect both issues and report file/line numbers with suggestions:

```bash theme={null}
$ terraform validate
Error: Missing required argument

  on main.tf line 1, in resource "azurerm_storage_account" "example":
   1: resource "azurerm_storage_account" "example" {

The argument "account_replication_type" is required, but no definition was found.

Error: Unsupported argument

  on main.tf line 6, in resource "azurerm_storage_account" "example":
   6:   account_replication_types     = "LRS"

An argument named "account_replication_types" is not expected here.
Did you mean "account_replication_type"?
```

Key characteristics of `terraform validate`:

* Validates HCL syntax and configuration structure.
* When initialized, validates against provider schemas (argument names, types, required fields).
* Does not make API calls to create or modify cloud resources — no infrastructure changes.
* Excellent to use in pre-commit hooks and CI pipelines to catch schema and syntax problems early.

<Callout icon="lightbulb">
  Run `terraform init` before `terraform validate` to ensure provider schemas are available for full validation.
</Callout>

## terraform fmt — enforce consistent HCL formatting

`terraform fmt` reformats your Terraform configuration files to the canonical HCL style. This improves readability and reduces noisy diffs in version control. It does not check correctness or change resource semantics.

Example of a poorly formatted file:

```hcl theme={null}
resource "azurerm_storage_account" "example" {
  name                        = var.storage_account_name
  location                    = "East US"
  resource_group_name         = "my-workshop-eus-rg"
  account_tier                = "Standard"
  account_replication_type    = "LRS"
  public_network_access_enabled = false
}
```

Format the file with:

```bash theme={null}
$ terraform fmt main.tf
```

For CI pipelines, use `terraform fmt -check` to verify that files are already formatted and fail the build if they are not:

```bash theme={null}
$ terraform fmt -check
```

Notes about `terraform fmt`:

* Only modifies whitespace/indentation and formatting.
* Does not validate argument names, types, or provider schemas.
* Useful as an automatic pre-commit hook step or CI gate to enforce a consistent code style.

<Callout icon="warning">
  `terraform validate` does not check runtime constraints or whether a given resource name is already taken by the cloud provider. Those checks require interacting with the provider (for example via `terraform plan`/`apply` or provider APIs).
</Callout>

## Quick reference

| Command              | Purpose                                                           | CI usage                                                |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------- |
| `terraform init`     | Download provider plugins and initialize the working directory.   | Always run before `validate` in CI.                     |
| `terraform validate` | Static validation of HCL and (after init) provider-schema checks. | Run to catch schema/syntax errors early.                |
| `terraform fmt`      | Reformat files to canonical HCL style.                            | Use `terraform fmt -check` to enforce formatting in CI. |

## Best practices

* Always run `terraform init` once per working directory (or in your CI job) before `terraform validate`.
* Add `terraform fmt -check` and `terraform validate` to CI pipelines to block malformed or invalid configs.
* Use `terraform fmt` as a pre-commit hook to keep repository diffs clean and consistent.
* Remember that `terraform validate` is static — to confirm resource creation and runtime constraints, use `terraform plan` and `terraform apply` in a safe environment.

## Links and references

* [Terraform CLI Commands — validate](https://www.terraform.io/docs/cli/commands/validate)
* [Terraform CLI Commands — fmt](https://www.terraform.io/docs/cli/commands/fmt)
* [azurerm provider documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

Summary:

* Use `terraform validate` to catch syntax and provider-schema issues before planning/applying.
* Use `terraform fmt` to enforce consistent HCL formatting across your team.
* Both commands are quick and should be part of your standard Terraform workflow (locally and in CI) before running `terraform plan` or `terraform apply`.

We'll now cover another Terraform command.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/8c459611-f77e-4c1f-95e1-7dc4d9ae312a" />
</CardGroup>
