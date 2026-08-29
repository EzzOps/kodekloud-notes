# count
count = length(var.items)

# for_each
for_each = toset(var.items)
```

How Terraform tracks identity

* count: Terraform tracks instances by numeric index. If the order of the input list changes, instances shift indices and Terraform may plan to destroy and recreate resources to match new indices.
* for\_each: Terraform tracks instances by key derived from the collection (element value for sets or keys for maps). As long as keys stay the same, resources remain stable even if the collection is reordered.

Concrete resource examples

Using `count` (index-based):

```hcl theme={null}
variable "items" {
  type    = list(string)
  default = ["rg-dev", "rg-prod"]
}

resource "aws_resource" "example_count" {
  count = length(var.items)

  name = var.items[count.index]
  # other configuration...
}
```

Using `for_each` (key-based):

```hcl theme={null}
variable "items" {
  type    = list(string)
  default = ["rg-dev", "rg-prod"]
}

resource "aws_resource" "example_each" {
  for_each = toset(var.items)

  name = each.key
  # other configuration...
}
```

Referencing created resources

* With `count`:
  * Inside the resource: `count.index`
  * Outside the resource: `aws_resource.example_count[0].id`, `aws_resource.example_count[1].id`

* With `for_each`:
  * Inside the resource: `each.key` (or `each.value` when iterating maps)
  * Outside the resource: `aws_resource.example_each["rg-dev"].id`, `aws_resource.example_each["rg-prod"].id`

Comparison table

|                 Feature |                      `count`                     |                   `for_each`                   |
| ----------------------: | :----------------------------------------------: | :--------------------------------------------: |
|       Identity tracking |           Numeric index (`0`, `1`, `2`)          |      Stable key (element value or map key)     |
|                Best for | Simple numeric repetition or ephemeral resources | Long-lived resources that need stable identity |
|     Behavior on reorder |  Risk of destroy/recreate due to index shifting  |     No recreation if keys remain unchanged     |
| Example state addresses |             `aws_resource.example[0]`            |        `aws_resource.example["rg-dev"]`        |
|          Recommendation |         Use when identity doesn't matter         |     Use as default for production resources    |

Behavior when inputs change

* count: Because instances are index-driven, inserting, removing, or reordering items in a list can change indices. Terraform will view shifted indices as different resources and may destroy/create instances to reconcile state.
* for\_each: Because instances are key-driven, reordering a collection does not affect existing resources. Adding or removing keys only adds or removes the specific instances affected.

Example scenario

Initial variable:

```hcl theme={null}
variable "items" {
  default = ["a", "b", "c"]
}
```

* With `count`, Terraform creates: `resource[0]` -> "a", `resource[1]` -> "b", `resource[2]` -> "c". If the list becomes `["b","a","c"]`, indices change and Terraform may recreate resources.
* With `for_each` (e.g., `for_each = toset(var.items)`), Terraform creates keys `"a"`, `"b"`, `"c"`. Reordering the list does not change keys or result in recreation.

Stable keys and metadata

When you need stable identifiers plus per-item attributes, prefer a map for `for_each`. Example:

```hcl theme={null}
variable "items_map" {
  type = map(object({
    cidr = string
  }))

  default = {
    "rg-dev"  = { cidr = "10.0.0.0/24" }
    "rg-prod" = { cidr = "10.0.1.0/24" }
  }
}

resource "aws_resource" "example_map" {
  for_each = var.items_map

  name = each.key
  cidr = each.value.cidr
}
```

Important nuances and gotchas

* `toset()` deduplicates and loses order. If duplicates in your list matter, do not convert to a set. Use a map keyed by a stable identifier or create explicit keys with `zipmap`.
* If you must use `count` with a list, keep the list ordering stable (for example, sort it explicitly) to avoid index shifts.
* `for_each` requires keys to be unique. For lists use `toset()` only when duplicates aren’t significant; otherwise, map elements to unique keys.
* When converting a list to a map for stable keys, you can use `zipmap()` to build explicit keys.

Best practices

* Default to `for_each` for long-lived, production resources where stable identity matters.
* Use `count` for simple numeric repetition (like creating N identical test resources) or when you intentionally want index semantics.
* Use maps with `for_each` for predictable keys and to attach metadata per item.
* Be deliberate when changing the input collection for an existing resource block; plan and review `terraform plan` to avoid accidental destruction.

Reference links

* [Terraform docs: count](https://www.terraform.io/language/meta-arguments/count)
* [Terraform docs: for\_each](https://www.terraform.io/language/meta-arguments/for_each)
* [Terraform docs: zipmap](https://www.terraform.io/language/functions/zipmap)

<Callout icon="lightbulb">
  Prefer `for_each` for stable, long-lived resources and `count` for simple numeric repetition. Remember that `toset()` removes duplicates and discards order—use maps or `zipmap()` to create deterministic keys when you need stable identities and per-item metadata.
</Callout>

With this, the comparison between `count` and `for_each` is complete.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/f4c88663-77b9-419e-8725-5389e3e7e2fa" />
</CardGroup>


# for Expressions

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Iteration-and-Logic/for-Expressions/page

Explains Terraform for expressions for transforming collections into lists, sets, or maps to prepare inputs for for_each and resources with examples and best practices.

For expressions in Terraform are a data-transformation feature, distinct from `count` and `for_each`. While `count` and `for_each` control how many resources Terraform creates, for expressions are used to reshape or derive new data structures (lists, sets, maps, strings) from existing inputs. Think of them as a preprocessing step: transform the input data with a for expression, then feed the result into `for_each`, module inputs, or other resource arguments.

Below is a compact example followed by a step‑by‑step explanation.

```hcl theme={null}
variable "environments" {
  type    = list(string)
  default = ["prod", "dev", "test"]
}

locals {
  # For expression: transform a list of environment names into resource group names
  resource_group_names = [for env in var.environments : "rg-${env}"]
}

resource "azurerm_resource_group" "rg" {
  # for_each expects a set or map; convert the list into a set to ensure uniqueness and stable keys
  for_each = toset(local.resource_group_names)

  # each.value represents the current element from the collection (here, the resource group name)
  name     = each.value
  location = "eastus"
}
```

<Callout icon="lightbulb">
  For expressions only produce data—they do not create resources. Use them to prepare or reshape values (lists, sets, maps, strings) that you then pass into `for_each`, resource arguments, modules, or other expressions. They keep configurations DRY and easier to maintain.
</Callout>

Line-by-line explanation

* variable block
  * `variable "environments"` defines a simple list: `["prod", "dev", "test"]`. These are input values only; no resources are created here.
* locals block and the for expression
  * `resource_group_names = [for env in var.environments : "rg-${env}"]`
  * This iterates each element in `var.environments`, transforms the value by prefixing `rg-`, and produces a new list: `["rg-prod", "rg-dev", "rg-test"]`.
* resource block and `for_each`
  * `for_each = toset(local.resource_group_names)` converts the list into a set. `for_each` requires either a set or a map (not a plain list). Converting to a set ensures uniqueness and establishes stable keys that Terraform uses to track resources between runs.
  * Inside the resource block, `each.value` represents the current element from the collection (here, the resource group name) and is used as the `name`.

Why choose a for expression?

* DRY configuration: Add or remove environment names in a single place and derived values update automatically.
* Flexible transformations: Build formatted names, filter elements, or generate complex maps used later in resources or modules.
* Separation of concerns: Locals act as a preprocessing layer—shape inputs exactly the way resources expect them.

Best practices and behavior notes

* For expressions return a collection type (list, set, or map) depending on the syntax and context; they do not create resources.
* Use `toset()` or `tomap()` when required by consumers like `for_each` so Terraform can use stable keys to track resources across runs.
* When using a map with `for_each`, the map keys become resource instance keys and `each.value` is the corresponding value. For sets of primitive values, the element itself becomes the stable identifier used by `for_each`.

<Callout icon="warning">
  Do not pass a plain list directly into `for_each`. Always convert lists into `toset()` or build a map to ensure deterministic resource keys and avoid unexpected resource recreation.
</Callout>

Quick reference table

| Topic                                            | When to use                                      | Example / Note                                                  |
| ------------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------- |
| Transform a list of strings into formatted names | When you need consistent naming across resources | Use a for expression in `locals` then `toset()` for `for_each`  |
| Filter elements                                  | Exclude items before resource creation           | `[for e in var.list : e if startswith(e,"prod")]`               |
| Build maps for complex resources                 | When resources need keyed inputs                 | Use `[for k, v in var.map : k => v]` or `merge()` patterns      |
| Ensure stable keys for `for_each`                | Always when creating resources from collections  | Convert list → `toset()` or produce a map with predictable keys |

When to use for expressions

* Any time you need to prepare or transform input data before passing it into `for_each`, module inputs, or resource arguments.
* Useful for consistent naming, filtering unwanted elements, or composing more complex structures from simple variables.

Summary

* For expressions transform data structures—they do not create resources.
* Locals commonly host for expressions to prepare data for resource creation.
* `for_each` consumes transformed data (often after conversion to a set or map), and resources are created based on those values.

Links and references

* [Terraform documentation: For expressions](https://www.terraform.io/docs/language/expressions/for.html)
* [Terraform documentation: for\_each meta-argument](https://www.terraform.io/docs/language/meta-arguments/for_each.html)
* [Terraform locals documentation](https://www.terraform.io/docs/language/values/locals.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/94612c9a-84fb-4096-bdac-b5765470e478" />
</CardGroup>
