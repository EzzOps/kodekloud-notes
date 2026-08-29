# ---- variables.tf ----
variable "resource_group_name" {
}

variable "location" {
}
```

Running `terraform plan` without supplying values triggers an interactive prompt:

```bash theme={null}
$ terraform plan
var.location
  Enter a value: eastus

var.resource_group_name
  Enter a value: my-workshop-rg
```

Pros:

* Simple and immediate for ad-hoc runs or demos.

Cons:

* Requires human input.
* Not suitable for automated pipelines.

## 2) Command-line flags (-var)

You can provide variable values at runtime with the `-var` flag, which overrides values from files and defaults and bypasses interactive prompts.

Example:

```bash theme={null}
$ terraform plan -var "location=eastus" -var "resource_group_name=my-workshop-rg"
```

Terraform will then generate a plan immediately:

```plaintext theme={null}
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_storage_account.storage will be created
  + resource "azurerm_storage_account" "storage" {
      + access_tier                = (known after apply)
      + account_kind               = "StorageV2"
      + account_replication_type   = "LRS"
    }
```

Pros:

* Quick for testing and one-off overrides.

Cons:

* Values appear in shell history.
* Commands become long and error-prone.
* Not ideal for secrets or repeatable workflows.

## 3) Variable definition files (tfvars)

Separating variable declarations from variable values is a common best practice. Place values in a `.tfvars` file:

```hcl theme={null}
# ---- variables.tf ----
variable "resource_group_name" {}
variable "location" {}

# ---- terraform.tfvars ----
resource_group_name = "my-workshop-rg"
location            = "eastus"
```

Behavior:

* `terraform.tfvars` is loaded automatically when you run `terraform plan` or `terraform apply`.
* Any file ending in `.auto.tfvars` is also auto-loaded.
* JSON equivalents (`terraform.tfvars.json`, `*.auto.tfvars.json`) are supported when valid JSON.

If you prefer explicit loading, use `-var-file`:

```bash theme={null}
$ terraform plan -var-file="variable.tfvars"
```

This is useful when switching environments manually (e.g., `dev.tfvars`, `staging.tfvars`, `prod.tfvars`).

Example plan output when using a var file:

```plaintext theme={null}
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_storage_account.storage will be created
  + resource "azurerm_storage_account" "storage" {
      + access_tier              = (known after apply)
      + account_kind             = "StorageV2"
      + account_replication_type = "LRS"
      + account_tier             = "Standard"
    }
```

Pros:

* Keeps values out of Terraform source files.
* Easy to version-control non-sensitive defaults (but don't commit secrets).
* Convenient for single primary environments.

Cons:

* Requires care to avoid committing secrets to VCS.

## 4) Environment variables (TF\_VAR\_\*)

Environment variables are widely used in CI/CD to inject secrets and other runtime values without checking them into source control. Terraform maps any environment variable named `TF_VAR_<variable_name>` to the corresponding input variable.

Example:

```bash theme={null}
$ export TF_VAR_resource_group_name="rg-01"
$ export TF_VAR_location="eastus"
$ terraform plan -var-file="variable.tfvars"
```

Notes:

* Environment variables are often used for sensitive values because CI/CD systems provide secure ways to store them.
* Treat any mechanism that exposes environment variables with care—environment values can leak into logs or process listings in some cases.

Pros:

* Good for CI/CD secrets when your pipeline manager stores secrets securely.
* Not persisted in project files.

Cons:

* Potential exposure in logs or process listings if misused.

## Variable precedence (lowest → highest)

Understanding precedence ensures you know which value Terraform will use when the same variable is defined in multiple places.

Precedence (lowest to highest):

1. Default value in `variable` declaration.
2. `terraform.tfvars` (auto-loaded).
3. `terraform.tfvars.json` (auto-loaded).
4. Auto-loaded files ending in `.auto.tfvars` or `.auto.tfvars.json` (alphabetical order; later files override earlier ones).
5. Environment variables: `TF_VAR_*`.
6. Command-line flags: `-var` and `-var-file` (last flag wins if multiple).

For readability, here’s the same precedence in a compact table:

| Priority    | Source                                                                         |
| ----------- | ------------------------------------------------------------------------------ |
| 1 (lowest)  | Default in `variable` block                                                    |
| 2           | `terraform.tfvars` (auto-loaded)                                               |
| 3           | `terraform.tfvars.json` (auto-loaded)                                          |
| 4           | `*.auto.tfvars` / `*.auto.tfvars.json` (auto-loaded; processed alphabetically) |
| 5           | Environment variables: `TF_VAR_*`                                              |
| 6 (highest) | Command-line: `-var` / `-var-file`                                             |

Note: If a variable has no default and hasn't been set by any of the above, Terraform will prompt you interactively as a last resort—unsuitable for automation.

<Callout icon="lightbulb">
  Organize variables according to this hierarchy. Use environment variables for secrets in CI/CD, `terraform.tfvars` for project defaults, `.auto.tfvars` for per-environment variables, and `-var`/`-var-file` for temporary or manual overrides.
</Callout>

## When to use each method

Use this quick reference to choose the right approach for your workflow:

| Method                 | Best for                                                 | Notes                                                                 |
| ---------------------- | -------------------------------------------------------- | --------------------------------------------------------------------- |
| `terraform.tfvars`     | Default reusable variables for a project                 | Auto-loaded and simple for a primary environment                      |
| `.auto.tfvars`         | Per-environment values where you want auto-load behavior | Files are processed alphabetically; later files override earlier ones |
| `-var` / `-var-file`   | One-off overrides or scripted runs                       | Highest precedence; avoid for long-term secret management             |
| Environment `TF_VAR_*` | CI/CD secrets and runtime injection                      | Store securely in pipeline secret stores; avoid logging them          |
| JSON (`*.tfvars.json`) | Machine-generated variable files                         | Useful when values are produced by scripts or external systems        |

Terraform gives you flexible options; apply consistent conventions to scale and secure your deployments.

## Example: prompts, env vars, and tfvars combined

This example demonstrates variable declarations with `description` and `validation`—helpful for interactive prompts and improving UX for other contributors.

```hcl theme={null}
variable "rg" {
  description = "Name of the resource group"
  type        = string

  validation {
    condition     = length(var.rg) >= 10
    error_message = "The resource group name cannot be less than 10 characters."
  }
}

variable "region" {
  description = "Azure region to deploy the resources"
  type        = string

  validation {
    condition     = contains(["eastus", "westus", "centralus"], var.region)
    error_message = "The region must be one of the following: eastus, westus, centralus."
  }
}
```

Interactive prompt example:

```plaintext theme={null}
variables
variables terraform plan
Azure region to deploy the resources
Enter a value: eastus

var.rg
Name of the resource group
Enter a value: rg-kodekloud-tf-01
```

Environment variable example:

```bash theme={null}
$ export TF_VAR_region="eastus"
$ terraform plan
```

Output (excerpt):

```plaintext theme={null}
  + id       = (known after apply)
  + location = "eastus"
  + name     = "rg-kodekloud-tf-01"

Plan: 1 to add, 0 to change, 0 to destroy.
```

Using a `terraform.tfvars` file (one variable from tfvars, one from environment):

```terraform theme={null}
# terraform.tfvars
rg = "rg-kodekloud-tf-01"
```

With `TF_VAR_region` set in the environment and `rg` in `terraform.tfvars`, Terraform will use values from both sources:

```bash theme={null}
$ export TF_VAR_region="eastus"
$ terraform plan
```

Plan output (excerpt):

```plaintext theme={null}
Terraform will perform the following actions:

# azurerm_resource_group.rg will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "eastus"
    + name     = "rg-kodekloud-tf-01"
}

Plan: 1 to add, 0 to change, 0 to destroy.
```

Always remember the precedence rules when values are defined in multiple places. Use the simplest method that still scales and follow security best practices for secrets.

## Links and References

* Terraform: Variables documentation — [https://www.terraform.io/language/values/variables](https://www.terraform.io/language/values/variables)
* Terraform: Input variable precedence — [https://www.terraform.io/cli/config/variables](https://www.terraform.io/cli/config/variables)
* Terraform: Variable files and JSON syntax — [https://www.terraform.io/language/values/variables#variable-definitions-files](https://www.terraform.io/language/values/variables#variable-definitions-files)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/6909fa70-4ccc-40c3-a918-1188673d8985/lesson/6b9783d9-2590-4e55-a0ae-2fcc7db50537" />
</CardGroup>


# Understanding Variable Block

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Variables/Understanding-Variable-Block/page

Explains Terraform variable blocks, covering types, defaults, validation, sensitivity, and value sources to enforce input rules, document intent, and secure reusable infrastructure modules.

In this lesson we examine the Terraform `variable` block — a foundational building block for creating reusable, well‑documented, and robust infrastructure code. A clearly defined `variable` block becomes a contract: it documents intent, enforces rules, and improves reuse across teams and automation pipelines.

A minimal variable declaration looks like:

```hcl theme={null}
