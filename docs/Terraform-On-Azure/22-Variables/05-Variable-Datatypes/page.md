# ---- variables.tf ----
variable "resource_group_name" {
}
```

With no `type`, `default`, or other arguments, Terraform treats the variable as a required input. If a value is not supplied at runtime, Terraform will prompt for it and stop execution until a value is provided. This behavior prevents accidental deployments with missing configuration.

Key arguments supported by the `variable` block

* `default` — A fallback value. When present, the variable becomes optional.
* `type` — Enforces an expected type (for example `string`, `list(string)`, `object({...})`). Terraform performs type checking before planning or applying.
* `description` — Human‑readable documentation that appears in CLI prompts and module docs.
* `validation` — A nested block that allows arbitrary expressions to validate input values (naming standards, allowed values, lengths, etc.). Validation is evaluated during the planning phase.
* `sensitive` — When true, Terraform hides the value in CLI output and logs. Note that sensitive values may still be stored in the state file.
* `nullable` — Controls whether `null` is an allowed value.
* `ephemeral` — Not a Terraform core attribute. For short‑lived or run‑only secrets, prefer passing values via the CLI (`-var`), environment variables, a secrets manager, or using [Terraform Cloud/Enterprise](https://www.terraform.io/cloud) run‑only variables or other secret management integrations to avoid persisting secrets in state.

<Callout icon="lightbulb">
  Use `sensitive = true` together with secure state backends (for example, encrypted [remote state](https://www.terraform.io/language/state/remote)) when handling secrets. `sensitive` masks output but does not prevent values from being stored in state.
</Callout>

Arguments quick reference

| Argument      | Purpose                                                             | Example                                                                                         |
| ------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `type`        | Enforces the expected type; Terraform validates before plan/apply   | `string`, `list(string)`, `object({ internal = number, external = number, protocol = string })` |
| `default`     | Provides a fallback value — variable is optional when present       | `default = ["us-west-1"]`                                                                       |
| `description` | Human-readable text used in prompts and docs                        | `description = "Azure region to deploy the resources"`                                          |
| `validation`  | Nested block with `condition` and `error_message` to validate input | `validation { condition = contains(["eastus"], var.region) error_message = "..." }`             |
| `sensitive`   | Hides values in output and logs (state still may contain value)     | `sensitive = true`                                                                              |
| `nullable`    | Controls whether `null` is permitted                                | `nullable = true`                                                                               |

Example: enforce a naming convention and length

```hcl theme={null}
# ---- variables.tf ----
variable "resource_group_name" {
  description = "Name for the resource group"
  type        = string

  validation {
    condition = (
      substr(var.resource_group_name, 0, 3) == "rg-" &&
      length(var.resource_group_name) <= 20
    )
    error_message = "Value must start with 'rg-' and be at most 20 characters long."
  }
}
```

This `validation` block enforces:

1. The value must start with the prefix `rg-`.
2. The value must not exceed 20 characters.

If a provided value fails validation, Terraform halts at planning and returns a clear error. For example:

```bash theme={null}
terraform plan -var "resource_group_name=demo-rg"
```

Might produce:

```plaintext theme={null}
Planning failed. Terraform encountered an error while generating this plan.

Error: Invalid value for variable "resource_group_name"
var.resource_group_name is "demo-rg"
Value must start with 'rg-' and be at most 20 characters long.
This was checked by the validation rule in variables.tf.
```

Working with variables in an editor — common patterns
Below are concise examples demonstrating typical validations and common types.

1. Enforce non‑empty or minimum length for an `rg` variable:

```hcl theme={null}
variable "rg" {
  description = "Name of the resource group"
  type        = string

  validation {
    condition     = length(var.rg) > 10
    error_message = "The resource group name must be greater than 10 characters."
  }
}
```

2. Restrict `region` to an allowlist using `contains`:

```hcl theme={null}
variable "region" {
  description = "Azure region to deploy the resources"
  type        = string

  validation {
    condition     = contains(["eastus", "westus", "centralus"], var.region)
    error_message = "The region must be one of the following: eastus, westus, centralus."
  }
}
```

Passing values on the CLI:

```bash theme={null}
terraform plan -var "rg=rg-kodekloud-tf-01" -var "region=eastus"
```

Example plan output (truncated):

```plaintext theme={null}
Terraform will perform the following actions:

  # azurerm_resource_group.rg will be created
  + resource "azurerm_resource_group" "rg" {
      + id       = (known after apply)
      + location = "eastus"
      + name     = "rg-kodekloud-tf-01"
      + tags     = {
          + "environment" = "testing"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Complex types and defaults
You can define structured types and defaults for more advanced configurations.

```hcl theme={null}
variable "image_id" {
  type        = string
  description = "The ID of the machine image (AMI) to use for the server."
}

variable "availability_zone_names" {
  type        = list(string)
  description = "List of availability zones where resources will be deployed."
  default     = ["us-west-1"]
}

variable "docker_ports" {
  type = list(object({
    internal = number
    external = number
    protocol = string
  }))
  description = "List of port configurations for Docker containers."
  default = [
    {
      internal = 8320
      external = 8320
      protocol = "tcp"
    }
  ]
}

variable "image_id" {
  description = "The ID of the machine image (AMI) to use for the server."
  validation {
    condition     = length(var.image_id) > 4 && substr(var.image_id, 0, 4) == "ami-"
    error_message = "The image_id must be a valid AMI ID, starting with \"ami-\"."
  }
}
```

Note: These examples are independent snippets. Do not declare the same variable name more than once within the same module — redeclaring a variable name in the same module will cause an error.

Official variable block template
The [official Terraform documentation](https://www.terraform.io/language/values/variables) shows a template like:

```hcl theme={null}
variable "LABEL" {
  type        = string
  default     = "<DEFAULT VALUE>"
  description = "<DESCRIPTION>"
  validation {
    condition     = <EXPRESSION>
    error_message = "<ERROR_MESSAGE>"
  }
  sensitive = false
  nullable  = false
  ephemeral = false
}
```

Ways to set variable values (common methods) and precedence

| Method                                | Description                                                   | Notes                                    |
| ------------------------------------- | ------------------------------------------------------------- | ---------------------------------------- |
| `default` inside the `variable` block | Lowest precedence; used when no other source provides a value | `default` in the block                   |
| `.tfvars` or `.tfvars.json` files     | Common for environment or deployment-specific values          | e.g., `terraform.tfvars`                 |
| `-var-file` on the CLI                | Loads variables from a file at plan/apply time                | `terraform plan -var-file="prod.tfvars"` |
| `-var` on the CLI                     | Highest precedence among non‑environment sources              | `terraform plan -var "rg=..."`           |
| environment variables `TF_VAR_<NAME>` | Useful for automation and CI systems                          | e.g., `TF_VAR_rg="..."`                  |

Note: Precedence can be subtle and may vary between Terraform versions and environments. In general, CLI `-var` and `-var-file` override values from files and environment variables, and defaults in the variable block have the lowest precedence. Consult the [Terraform documentation](https://www.terraform.io/language/values/variables) for exact rules for your version.

Summary

* Use `type`, `description`, and `validation` to make variables self‑documenting and expressive.
* Explicit validations in shared modules and automation catch invalid inputs early.
* Protect secrets with `sensitive = true` and secure state backends; `sensitive` only masks output.
* Choose an appropriate method to supply values (defaults, `tfvars`, CLI, environment) and be aware of precedence for deterministic behavior.

Links and references

* [Terraform Variables — Official Documentation](https://www.terraform.io/language/values/variables)
* [Terraform State — Remote Backends](https://www.terraform.io/language/state/remote)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/6909fa70-4ccc-40c3-a918-1188673d8985/lesson/a9827670-df89-4638-9ee0-7063fc36abc1" />
</CardGroup>


# Variable Datatypes

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Variables/Variable-Datatypes/page

Guide to Terraform variable data types, usage, declaration examples, and best practices for strong typing, validation, and structured inputs like lists, maps, objects, and tuples.

A clear understanding of Terraform variable data types is essential for writing safe, maintainable infrastructure-as-code. Terraform is strongly typed: every input variable can — and usually should — have an explicit type. Picking the correct type improves validation, prevents runtime errors, and makes configurations easier to reason about as your infrastructure grows.

This guide explains the common Terraform variable data types: what each represents, when to use it, and how to declare values in `variables.tf` and `terraform.tfvars`. It also includes a consolidated example showing how several types are used together in an `azurerm_storage_account` resource.

For additional reading, see the Terraform docs on input variables: [https://www.terraform.io/language/values/variables](https://www.terraform.io/language/values/variables)

## Common Terraform variable data types

| Type   | Description                                                                                      | When to use                                                      | Declaration example                                                                                               |
| ------ | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| string | A single line of text.                                                                           | Names, identifiers, regions, environment labels, resource names. | `variable "env" { type = string }`                                                                                |
| number | Numeric values (integer or floating-point).                                                      | Counts, thresholds, sizes, timeouts.                             | `variable "replicas" { type = number }`                                                                           |
| bool   | Boolean: `true` or `false`.                                                                      | Feature toggles, conditionals, enabling/disabling options.       | `variable "enabled" { type = bool }`                                                                              |
| list   | Ordered collection of elements of the same type (order matters).                                 | Ordered subnet CIDRs, ordered AZ lists.                          | `variable "azs" { type = list(string) }`                                                                          |
| set    | Unordered collection of unique elements of the same type (duplicates not allowed).               | Unique values where order is irrelevant.                         | `variable "unique_ids" { type = set(string) }`                                                                    |
| map    | Key-value pairs where all values share the same type. Great for tag maps or environment lookups. | Tagging, SKUs per environment, configuration lookup tables.      | `variable "tags" { type = map(string) }`                                                                          |
| object | A grouping of named attributes, each with its own type. Useful for bundling related settings.    | Complex structured inputs like storage/network configs.          | `variable "storage_config" { type = object({ location = string, account_tier = string, replication = string }) }` |
| tuple  | Ordered, fixed-length collection where each position can have a different type.                  | Positional structures with known length and mixed types.         | `variable "coords" { type = tuple([number, number]) }`                                                            |
| any    | Accepts any value. Disables type validation.                                                     | Only when maximum flexibility is required (use sparingly).       | `variable "flex" { type = any }`                                                                                  |

<Frame>
  <img alt="The image is a table detailing different variable datatypes including their descriptions, declaration methods, and example values. It covers types such as string, number, bool, list, set, map, object, tuple, and any." />
</Frame>

### Short notes on selected types

* map: Use `map(string)` or `map(number)` when values share a single type; access entries via `var.my_map["key"]`.
* object: Use objects to group related attributes and access them with `var.obj.attr`.
* tuple: Useful for fixed-position data such as `[ "log", 30 ]` where positions convey meaning.
* any: Avoid in production code; it defeats type checking and can hide configuration errors.

<Callout icon="lightbulb">
  Prefer specific types (string, number, bool, list, map, object) over `any` whenever possible. Strong typing enables Terraform to validate inputs and catch errors early.
</Callout>

The following diagram shows a concrete example of variable declarations for a storage account and how those variables are intended to be consumed by resources.

<Frame>
  <img alt="The image shows a code snippet from a Terraform configuration file defining variables for a storage account. It includes settings for the storage account name, HTTPS-only toggle, tags, and storage configuration." />
</Frame>

## Consolidated example

The example below demonstrates defining variables in `variables.tf`, consuming them in `main.tf`, and providing runtime values in `terraform.tfvars`.

```hcl theme={null}
