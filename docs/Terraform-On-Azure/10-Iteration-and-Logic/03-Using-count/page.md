# Using count

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Iteration-and-Logic/Using-count/page

Explains Terraform's count meta-argument for creating indexed resource instances, discusses identity, lifecycle pitfalls, and when to prefer for_each for stable, key based resource identities.

In this lesson we cover one of Terraform's earliest and simplest iteration mechanisms: the `count` meta-argument. `count` is useful for creating multiple copies of a resource from a single block, but it has important implications for identity, indexing, and lifecycle behavior. Read on for concise examples, common pitfalls, and guidance on when to prefer alternatives like `for_each`.

What `count` does

* Adding `count = N` transforms a single resource block into a collection (a list) of `N` instances rather than a single instance.
* Inside such a resource block you can reference `count.index` to get the current instance’s numeric index (starting at `0`).
* Each instance’s identity is positional and based on its numeric index — Terraform tracks `resource.name[0]`, `resource.name[1]`, etc., not by any human-readable name you assign.

Example: two resource groups

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  count    = 2
  name     = "rg-${count.index}"
  location = "eastus"
}
```

This creates:

* `azurerm_resource_group.rg[0]` with name `rg-0`
* `azurerm_resource_group.rg[1]` with name `rg-1`

`count.index` exists only inside resource blocks that use `count` and increments from `0` to `count - 1`.

<Callout icon="lightbulb">
  Use `count` when instance identity is strictly positional (index-based) and you only need simple duplication with small index-driven differences (for example, suffixes or offsets). For long-lived infrastructure that requires stable identities, prefer `for_each`.
</Callout>

When `count` is a poor fit

* Identity is numeric and positional. If you change `count`, Terraform will add or remove instances based on indices (it removes the highest indices first), not by any name or metadata you supply.
* Non-index-based mappings between configuration and logical entities can result in surprising destroys and recreates when indexes shift.

Practical examples

1. Minimal provider + counted resource groups

```hcl theme={null}
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

variable "subscription_id" {
  type = string
}

variable "text" {
  default = "rg"
}

resource "azurerm_resource_group" "rg" {
  count    = 3
  name     = "${var.text}-resources-${count.index}"
  location = "westeurope"
}
```

Terraform plan (simplified):

```bash theme={null}
