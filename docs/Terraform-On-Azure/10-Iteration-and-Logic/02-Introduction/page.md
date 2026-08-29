# Initialize (example)
terraform init
```

```bash theme={null}
terraform plan
```

```plaintext theme={null}
Error: Invalid for_each set argument

  on main.tf line 18, in resource "azurerm_resource_group" "rg":
  18:   for_each = toset(local.rg_nested)

local.rg_nested is tuple with 2 elements

The given "for_each" argument value is unsuitable: "for_each" supports maps and sets of strings, but you have provided a set containing type tuple.
```

This error occurs because the nested `for` expression produced a list that contains inner lists. `flatten()` converts a nested list into a single flat list, which `toset()` can then convert into a set of strings acceptable to `for_each`.

<Callout icon="warning">
  If you produce nested lists, call `flatten()` before `toset()` when using `for_each`. Otherwise Terraform will complain that the argument type is not a set of strings.
</Callout>

Plan output and environment overrides

With the default `environment = "dev"`, `local.location` will compute to `"westus"`, so all resource groups are planned for West US. Example plan (after using `flatten` or `rg_flat`):

```plaintext theme={null}
Plan: 6 to add, 0 to change, 0 to destroy.

# azurerm_resource_group.rg["rg-dev-api"] will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "westus"
    + name     = "rg-dev-api"
}
# ... other RGs omitted for brevity
```

Override the environment at plan time to change locations:

```bash theme={null}
terraform plan -var='environment=prod'
```

Now `local.location` evaluates to `"eastus"` and the plan shows East US locations:

```plaintext theme={null}
Plan: 6 to add, 0 to change, 0 to destroy.

# azurerm_resource_group.rg["rg-prod-api"] will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "eastus"
    + name     = "rg-prod-api"
}
# ... other RGs omitted for brevity
```

Quick reference

| Topic                    | When to use                                              | Example / Notes                                                     |
| ------------------------ | -------------------------------------------------------- | ------------------------------------------------------------------- |
| Conditional expressions  | Choose between two values (regions, SKUs, toggles)       | `condition ? true_val : false_val`                                  |
| For expressions (nested) | When you want grouped lists per iterator                 | `local.rg_nested = [ for env in ... : [ for app in ... : "..." ] ]` |
| For expressions (flat)   | When you want a single list of combinations              | `local.rg_flat = [ for env in ... : for app in ... : "..." ]`       |
| Flatten + toset          | Required when converting nested lists to `for_each` sets | `for_each = toset(flatten(local.rg_nested))`                        |

Summary

* Conditional expressions are Terraform's ternary operator — useful for environment-specific values and small toggles.
* `for` expressions build lists. Use a double `for` to produce a flat list directly, or nest `for` expressions to create grouped lists.
* If you have nested lists, use `flatten()` before `toset()` so `for_each` receives a set of strings.
* Override variables at `plan`/`apply` time (e.g., `-var='environment=prod'`) to affect computed locals like `local.location`.

Links and references

* [Terraform Expressions](https://www.terraform.io/docs/language/expressions/index.html)
* [Terraform for Expressions](https://www.terraform.io/docs/language/expressions/for.html)
* [Azure Provider (azurerm) Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/fda91ce8-39e6-4206-b1bb-9491f1b1753e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/5e9c2799-c739-4d2a-a547-bca4eebb7eee" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Iteration-and-Logic/Introduction/page

Guide to Terraform iteration and logic using count, for_each, for expressions and conditional expressions for scalable maintainable resources and predictable state management

In this lesson we'll explore how Terraform handles repetition and decision-making so your infrastructure code can scale without duplication. You'll learn when to use `count` and when to prefer `for_each`, how to reshape data with `for` expressions, and how to apply conditional expressions for environment-specific or optional logic.

* Understand `count` and its limits for predictable resource addresses.
* Master `for_each` for stable identities and safer state management.
* Compare `count` vs `for_each` to choose the right approach for long-term maintenance.
* Use `for` expressions to transform collections.
* Use conditional expressions to implement environment or optional logic.

<Frame>
  <img alt="The image displays an agenda with five numbered points related to resource management and expressions in Terraform, each point having a different color." />
</Frame>

All of these patterns let your configurations adapt programmatically, reducing repetition and making modules easier to maintain and evolve.

<Callout icon="lightbulb">
  Use `count` when you need simple repetition of identical resources. Prefer `for_each` for collections where each instance needs a stable address or when keys/identities matter for the Terraform state.
</Callout>

## Quick overview: when to use each pattern

|                 Pattern | Best for                                                            | Example                                                                                    |
| ----------------------: | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
|                 `count` | Creating N identical resources with a numeric index                 | `count = 3`                                                                                |
|              `for_each` | Creating resources from a collection with stable keys (`set`/`map`) | `for_each = toset(["a","b"])` or `for_each = { "app1" = "10.0.1.0", "app2" = "10.0.2.0" }` |
|       `for` expressions | Transforming or mapping collections before use                      | `local.subnets = [for s in var.azs : "${s}-subnet"]`                                       |
| Conditional expressions | Environment-specific or optional behavior                           | `count = var.enabled ? 1 : 0`                                                              |

## What you'll learn in this lesson

1. `count` — how it creates multiple instances and where it becomes limiting.
2. `for_each` — why it provides stable resource identities and predictable state addresses.
3. Side-by-side comparison — how changing between patterns affects state and resource replacement.
4. `for` expressions — reshaping data for use in resources.
5. Conditional expressions — gating resources and settings by environment or flags.

<Callout icon="warning">
  Changing between `count` and `for_each` (or changing keys used by `for_each`) can force Terraform to recreate resources. Test changes in a safe environment and plan before apply to avoid unexpected replacements.
</Callout>

## Links and references

* [Terraform documentation: count](https://www.terraform.io/docs/language/meta-arguments/count.html)
* [Terraform documentation: for\_each](https://www.terraform.io/docs/language/meta-arguments/for_each.html)
* [Terraform documentation: for expressions](https://www.terraform.io/docs/language/expressions/for.html)
* [Terraform documentation: conditional expressions](https://www.terraform.io/docs/language/expressions/conditionals.html)

These topics will help you write Terraform configurations that are both concise and resilient as your infrastructure grows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/ee652b86-0e33-48f1-bea5-f99104adddd3" />
</CardGroup>
