# Defining Variable Types

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Configuration-Fundamentals/Defining-Variable-Types/page

Explains Terraform variable types including primitives string number bool and collections list map set with examples, usage, validation, and best practices for safe configurable infrastructure.

In this lesson we cover Terraform variable types — the primitive and collection types you use to make configurations flexible, predictable, and safe. Terraform exposes three primitive types: `string`, `number`, and `bool`. You then combine those primitives with collection types (`list`, `map`, `set`) to model complex inputs like network lists, resource tags, or unique identifiers.

## Primitive types

* String: free-form text for names, tags, DNS names, and other textual values.
* Number: integers or floating-point values for counts, sizes, timeouts, etc.
* Boolean: `true`/`false` switches for toggles (e.g., enabling or disabling features).

Example declaring each primitive type:

```hcl theme={null}
variable "region" {
  type    = string
  default = "us-east-2"
}

variable "num_of_vms" {
  type    = number
  default = 3
}

variable "enable_ha" {
  type    = bool
  default = true
}
```

Using explicit types creates a contract for your configuration. Terraform validates incoming values and prevents accidental type mismatches (for example, passing `"three"` for a `number` variable).

<Callout icon="lightbulb">
  Declaring explicit types helps catch errors early. For example, if someone supplies the word `three` instead of the numeric value `3` for a `number` variable, Terraform will report a type validation error before any infrastructure changes occur.
</Callout>

## Lists

Lists store an ordered sequence of values. Use lists when order matters or when you need indexed access to a sequence of similar items (availability zones, instance sizes, subnet CIDRs, etc.).

Example list variable:

```hcl theme={null}
variable "permitted_size" {
  type    = list(string)
  default = ["t3.small", "t4g.micro"]
}
```

Key points about lists:

* Values are accessed by index, starting at zero (e.g., `var.permitted_size[0]`).
* Lists preserve order — use them when sequence matters.
* Accessing an out-of-range index will cause an error, so validate or guard your indexing.

## Maps

Maps are unordered key-value collections and are useful when you prefer name-based access rather than positional indexing.

Example map variable:

```hcl theme={null}
variable "course_details" {
  description = "Course details"
  type        = map(string)
  default     = {
    instructor = "Bryan Krausen"
    course     = "Terraform"
  }
}
```

Advantages of maps:

* Readable, self-documenting keys (e.g., `var.course_details.instructor`).
* Add or modify keys without affecting others.
* Unordered by design — do not rely on entry order.

## Sets

Sets are unordered collections that enforce uniqueness. Use sets when duplicates must be avoided (subnet IDs, IP addresses, domain names).

Example set variable:

```hcl theme={null}
variable "pub_subnet_ids" {
  type    = set(string)
  default = toset(["subnet-12345", "subnet-67890"])
}
```

Important notes about sets:

* Values are unique; duplicates are automatically deduplicated.
* Sets are unordered; you cannot index into a set (no `set[0]`).
* Convert a set to a list with `tolist()` when you need deterministic ordering and indexed access.
* Use `toset()` in literals to ensure Terraform treats the default as a set rather than a list.

<Callout icon="lightbulb">
  Sets are ideal when uniqueness matters. If you later need ordered access, convert a set to a list with `tolist()` and handle the ordering explicitly.
</Callout>

## Referencing variables

Terraform variable values are referenced using the `var` namespace followed by the variable name. This distinguishes variables from literal values inside your configuration.

Example variable definitions (vSphere):

```hcl theme={null}
variable "vsphere_datacenter" {
  description = "Name of datacenter"
  type        = string
  default     = "prd-workload-dc"
}

variable "vsphere_networks" {
  description = "List of networks"
  type        = list(string)
  default     = [
    "VM Network",
    "Management Network"
  ]
}
```

Referencing these variables:

```plaintext theme={null}
1. var.vsphere_datacenter
2. var.vsphere_networks[0]
```

* `var.vsphere_datacenter` returns the string value `"prd-workload-dc"`.
* `var.vsphere_networks[0]` returns the first element of the list (`"VM Network"`). Remember lists are zero-indexed.

## Table: Terraform variable types at a glance

| Type                  | Purpose                         | Example HCL                                         |
| --------------------- | ------------------------------- | --------------------------------------------------- |
| Primitive: `string`   | Names, tags, DNS                | `variable "region" { type = string }`               |
| Primitive: `number`   | Counts, sizes, timeouts         | `variable "num_of_vms" { type = number }`           |
| Primitive: `bool`     | Feature toggles                 | `variable "enable_ha" { type = bool }`              |
| Collection: `list(T)` | Ordered sequences, indexing     | `variable "permitted_size" { type = list(string) }` |
| Collection: `map(T)`  | Named lookups, self-documenting | `variable "course_details" { type = map(string) }`  |
| Collection: `set(T)`  | Unordered unique values         | `variable "pub_subnet_ids" { type = set(string) }`  |

## Best practices and tips

* Prefer explicit `type` declarations to avoid accidental values and to enable early validation.
* Use `list` when order matters and you need indexed access.
* Use `map` for named lookups and to make intent clear in your inputs.
* Use `set` when you need uniqueness; convert with `tolist()` when deterministic ordering is required.
* Validate indexes or use helper functions (e.g., `length()`, `lookup()`) to avoid runtime errors.
* Consider `variable` `validation` blocks (Terraform 0.13+) for enforcing constraints beyond type (e.g., allowed values, regex checks).

## Summary

* The three primitive types (`string`, `number`, `bool`) form the foundation of Terraform variables.
* Lists, maps, and sets are the primary collection types; choose based on order, naming, and uniqueness requirements.
* Always reference variables as `var.<name>` and validate indexes and types before runtime.

Next, we'll combine these types and add `validation` rules to enforce more complex constraints and business rules in your variable definitions.

## Links and References

* [Terraform: Input Variables](https://developer.hashicorp.com/terraform/language/values/variables)
* [Terraform: Type Constraints](https://developer.hashicorp.com/terraform/language/expressions/type-constraints)
* [Terraform: Functions - toset, tolist](https://developer.hashicorp.com/terraform/language/functions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/aeb08bd6-fa0b-40bb-8555-0ece4ee7b9fc" />
</CardGroup>
