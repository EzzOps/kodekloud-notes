# Using locals

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Advanced-Constructs/Using-locals/page

Explains Terraform locals as computed reusable values to centralize derived logic, reduce duplication, and standardize naming, tags, and shared configurations across resources

Let's start with the first advanced construct: locals.

In Terraform, locals are named values evaluated during configuration processing and reused throughout your configuration. Unlike input `variable`s, locals are derived values (computed from variables, expressions, and functions). They centralize repeated logic and computed expressions so you avoid duplicating the same interpolation, concatenation, or function call across multiple resources.

<Frame>
  <img alt="The image illustrates the role of &#x22;locals&#x22; in Terraform. It highlights that locals define computed values and help avoid repeating the same expression." />
</Frame>

Why use locals?

* Define computed values (for example, transform environment names into standardized prefixes).
* Reduce repetition of identical expressions across resources.
* Improve readability and reduce the chance of copy/paste errors.
* Make refactoring easier by centralizing logic in one place.

When should you use locals? Common scenarios include:

* Naming conventions: construct consistent resource names using environment, project, or workload identifiers.
* Tags: define a standard set of tags once and reuse them across resources.
* Derived values used in multiple places: any calculated value referenced more than once should live in a local.

<Frame>
  <img alt="The image is a slide titled &#x22;When to Use Locals&#x22; and lists three points: &#x22;Naming convention,&#x22; &#x22;Tags,&#x22; and &#x22;Derived values used in multiple places.&#x22;" />
</Frame>

Any value that is calculated and reused more than once should be a local.

> **lightbulb** Use locals to centralize computed logic. If you find yourself duplicating the same interpolation, concatenation, or function call across resources, move that expression into a local.

Example

Below is a concise example showing a variable, a computed local, and the local referenced in a resource name:

```hcl theme={null}
variable "environment" {
  type = string
}

locals {
  name_prefix = "demo-${var.environment}"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.name_prefix}-rg"
  location = "eastus"
}
```

Explanation

* `variable "environment"` expects strings like `dev`, `test`, or `prod`.
* `local.name_prefix` derives its value from `var.environment`, producing values such as `demo-dev`, `demo-test`, or `demo-prod`.
* The resource group name is composed as `demo-dev-rg`, `demo-test-rg`, or `demo-prod-rg` depending on `var.environment`.

When to prefer locals (quick reference)

| Resource pattern      | Why use locals                                    | Example                                          |
| --------------------- | ------------------------------------------------- | ------------------------------------------------ |
| Naming conventions    | Keep names consistent and changeable in one place | `local.name_prefix = "demo-${var.environment}"`  |
| Shared tags           | Define tags once and reuse to ensure consistency  | `locals { default_tags = { Owner = "team-a" } }` |
| Reused derived values | Centralize logic used by multiple resources       | `local.az_location = lower(var.location)`        |

Best practices

* Give locals clear, descriptive names (e.g., `name_prefix`, `default_tags`, `subnet_cidrs`).
* Keep locals focused on computation; avoid embedding complex side effects.
* Use locals to simplify dynamic blocks and for\_each expressions by computing maps or lists up front.
* Limit the number of nested computations in a single local—split complex logic into multiple small locals for readability.

References

* Terraform documentation: [locals](https://www.terraform.io/language/values/locals)

Takeaway: locals clarify intent and reduce duplication. As a rule of thumb, if a value is derived and reused anywhere in your configuration, move it into a local.

This pattern is particularly useful when working with dynamic blocks and computed collections—compute the list or map in a local, then iterate over it with `dynamic` or `for_each`.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4fafc188-5a1a-4dbf-8fa0-50e3f00a270d/lesson/2436fd5e-d11f-4e48-8b19-823900f51ec2)
