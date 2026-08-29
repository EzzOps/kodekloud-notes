# Conceptual expansion of the dynamic block
security_rule {
  name                       = "allow-80"
  priority                   = 100
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = 80
  source_address_prefix      = "*"
  destination_address_prefix = "*"
}

security_rule {
  name                       = "allow-443"
  priority                   = 101
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = 443
  source_address_prefix      = "*"
  destination_address_prefix = "*"
}

security_rule {
  name                       = "allow-22"
  priority                   = 102
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = 22
  source_address_prefix      = "*"
  destination_address_prefix = "*"
}
```

This eliminates copy-paste and keeps the configuration compact and easy to maintain.

> **warning** Azure NSG `priority` values must be unique per security group and are typically in the range 100–4096. When generating priorities programmatically, ensure the computation yields unique values and stays within Azure's allowed range.

## Alternatives and notes

There are two common ways to define NSG rules in Terraform:

* Use nested `security_rule` blocks (inside the `azurerm_network_security_group`) — good when you want grouped rules defined with the resource and simpler configuration grouping.
* Use the separate `azurerm_network_security_rule` resource with a `for_each` — useful if you prefer each rule as its own top-level resource with independent lifecycle and state addressing.

> **lightbulb** You can define NSG rules either as nested `security_rule` blocks (using `dynamic`) or as separate `azurerm_network_security_rule` resources with `for_each`. Choose the style that best fits your lifecycle, referencing needs, and state management preferences.

Comparison (quick reference):

|                                            Approach | When to use                                                                          | Example                                                                                   |
| --------------------------------------------------: | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
|                               Nested dynamic blocks | Rules are tightly coupled to the NSG and should be managed together                  | Use `dynamic "security_rule"` inside `azurerm_network_security_group`                     |
| Separate resource (`azurerm_network_security_rule`) | Need fine-grained lifecycle control, separate addressing, or independent referencing | Use `resource "azurerm_network_security_rule" "rule" { for_each = toset(var.ports) ... }` |

Example of the separate-resource approach (using `for_each`):

```hcl theme={null}
variable "ports" {
  type    = list(number)
  default = [80, 443, 22]
}

resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-demo"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "rule" {
  for_each = toset(var.ports)

  name                         = "allow-${each.value}"
  priority                     = 100 + index(var.ports, each.value)
  direction                    = "Inbound"
  access                       = "Allow"
  protocol                     = "Tcp"
  source_port_range            = "*"
  destination_port_range       = tostring(each.value)
  source_address_prefix        = "*"
  destination_address_prefix   = "*"
  resource_group_name          = azurerm_resource_group.rg.name
  network_security_group_name  = azurerm_network_security_group.nsg.name
}
```

Both approaches are valid — nested `dynamic` is often cleaner when rules are tightly coupled to the NSG, while separate resources can offer different lifecycle semantics and easier targeting in state.

## Example: VS Code / local iteration demo

The dynamic-block pattern is also useful when iterating to create many top-level resources. Below is a concise example that builds combinations of environment + app and creates resource groups with `for_each`.

```hcl theme={null}
variable "environment" {
  default = "dev"
}

locals {
  location     = var.environment == "prod" ? "East US" : "West US"
  environments = ["dev", "prod"]
  apps         = ["api", "web", "db"]

  # build all combinations of environment + app, then flatten
  rg = flatten([
    for env in local.environments : [
      for app in local.apps : "rg-${env}-${app}"
    ]
  ])
}

resource "azurerm_resource_group" "rg" {
  for_each = toset(local.rg)
  name     = each.value
  location = local.location
}
```

Example plan output (abbreviated):

```plaintext theme={null}
# azurerm_resource_group.rg["rg-prod-web"] will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "West US"
    + name     = "rg-prod-web"
  }

Plan: 6 to add, 0 to change, 0 to destroy.
```

## FQDN / Firewall rules example

The dynamic-block pattern fits other Azure features where repeated nested blocks occur, such as:

* Azure Firewall application rules (FQDNs)
* Firewall network rules
* Any resource with repeated nested block types

Replace the `for_each` collection and nested block content appropriately — the pattern remains the same: iterate over a collection and produce one nested block per item.

## Full working example (provider + variable + RG + NSG + dynamic rules)

A complete HCL example, ready to use:

```hcl theme={null}
provider "azurerm" {
  features {}
}

variable "ports" {
  type    = list(number)
  default = [80, 443, 22]
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-nsg-demo"
  location = "West Europe"
}

resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-demo"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  dynamic "security_rule" {
    for_each = var.ports
    content {
      name                       = "allow-${security_rule.value}"
      priority                   = 100 + security_rule.key
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = tostring(security_rule.value)
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
  }
}
```

Summary

* Use dynamic blocks when nested block structure is constant but the number of blocks varies.
* Consider separate resources if you need independent lifecycle control.
* Always ensure generated values (like NSG priorities) comply with Azure constraints.

Further reading and references:

* [Terraform documentation: dynamic blocks](https://www.terraform.io/docs/language/expressions/dynamic-blocks.html)
* [Azure Provider — Network Security Group](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_group)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4fafc188-5a1a-4dbf-8fa0-50e3f00a270d/lesson/eceab11e-90ed-49a4-8453-0320aed507c0)


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Advanced-Constructs/Introduction/page

Explains Terraform advanced constructs like locals, dynamic blocks, built-in functions, and best practices for building scalable, maintainable, production ready modules

Welcome to the next module: Advanced Constructs in Terraform.

So far you’ve learned variables, resources, simple expressions, and basic iterations. This lesson introduces constructs that make Terraform scalable, maintainable, and production-ready. We’ll cover how to compute reusable values, generate nested blocks programmatically, use built-in functions to transform data safely, and make practical decisions about when and how to apply these features.

This module focuses on four key concepts:

| Concept                          | Purpose                                                                                                 | Quick example                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Locals                           | Define derived, reusable values inside a module to reduce duplication and centralize naming/formatting. | `locals { env = "${var.project}-${var.environment}" }` |
| Dynamic blocks                   | Programmatically generate repeated nested configuration blocks (e.g., multiple ingress rules).          | See dynamic block example below                        |
| Built-in functions               | Transform and validate data safely (`join`, `concat`, `coalesce`, `lookup`, `jsonencode`, etc.).        | `join(", ", var.subnets)`                              |
| Decision-making & best practices | When to compute locally, how to design module boundaries, and how to keep code readable and testable.   | Guidance in the Best practices section                 |

1. Locals\
   Locals let you define computed, reusable values inside a module. Treat them as module-level constants derived from inputs. Use locals to:

* Consolidate repeated logic (formatting, naming, derived IDs).
* Simplify complex expressions (combinations of `for` expressions and conditional logic).
* Reduce duplication to make HCL easier to read and maintain.

Example: simple local for an environment-based name

```hcl theme={null}
locals {
  env_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project = var.project
    Env     = var.environment
  }
}
```

> **lightbulb** Use locals when a value is derived from inputs and reused in multiple places. Locals are evaluated per-module and do not create additional state or resources.

2. Dynamic blocks\
   Dynamic blocks generate repeated nested blocks inside resources or modules, based on input collections. They prevent copy-pasting when the number of nested blocks varies.

Example: generating multiple `ingress` rules from a variable list

```hcl theme={null}
resource "aws_security_group" "example" {
  name = "${local.env_prefix}-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from
      to_port     = ingress.value.to
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

<Frame>
  <img alt="The image shows an introduction slide with two points about Terraform configurations: using locals for reusable values and applying dynamic blocks for nested resource configurations." />
</Frame>

> **warning** Avoid overusing dynamic blocks to hide complex logic. If dynamic generation makes the configuration hard to read, prefer an explicit approach or refactor into a smaller module with clear inputs.

3. Built-in functions\
   Terraform’s built-in functions help you inspect and transform data safely. Common ones include:

* `join(separator, list)` — join list elements
* `concat(list1, list2)` — concatenate lists
* `coalesce(val1, val2, ...)` — return the first non-empty value
* `lookup(map, key, default)` — safe map lookup
* `jsonencode(value)` — encode an HCL value as JSON

Examples:

```hcl theme={null}
output "subnets_csv" {
  value = join(", ", var.subnet_ids)
}

locals {
  instance_name = coalesce(var.instance_name, "default-${var.environment}")
  policy_json   = jsonencode(local.policy_map)
}
```

4. Decision-making and best practices\
   Apply these constructs to improve readability and maintainability, not to obscure intent. Key guidelines:

* Compute values locally when they’re derived from module inputs and used in several places.
* Keep module APIs (inputs/outputs) explicit; avoid hiding important behavior inside complex locals or dynamic generation.
* Favor small, focused modules that are easy to test and reason about.
* Use built-in functions to write defensive expressions that tolerate optional or missing inputs.

Quick checklist:

* Are derived values used more than once? Use `locals`.
* Is the nested block count variable (and simple)? Use `dynamic`.
* Does complexity harm readability? Consider refactoring into a module.
* Can you write expressions that survive missing inputs? Use functions like `coalesce` and `lookup`.

Further reading and references

* [Terraform: Locals](https://www.terraform.io/language/values/locals)
* [Terraform: Dynamic Blocks](https://www.terraform.io/language/expressions/dynamic-blocks)
* [Terraform: Functions](https://www.terraform.io/language/functions)
* [Terraform best practices and module design patterns](https://www.terraform.io/docs/extend/best-practices/index.html)

In the following sections we’ll explore each concept with detailed examples and patterns that are proven in real-world Terraform projects.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4fafc188-5a1a-4dbf-8fa0-50e3f00a270d/lesson/aedc3cda-5080-4389-a97f-f4aa99ff8905)
