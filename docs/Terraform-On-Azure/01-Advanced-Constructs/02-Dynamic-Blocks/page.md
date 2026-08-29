# Dynamic Blocks

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Advanced-Constructs/Dynamic-Blocks/page

Explains Terraform dynamic blocks to generate repeated nested Azure resource blocks like NSG rules, with examples, usage scenarios, and alternatives for lifecycle control.

Let's move on to the next advanced Terraform construct: dynamic blocks.

Dynamic blocks let Terraform feel more programmable while staying declarative. They generate repeated nested blocks dynamically from input data, so you avoid copy-pasting identical nested blocks with only small variations.

What dynamic blocks do:

* Dynamically create nested blocks (useful when a resource expects multiple child blocks of the same type, like rules, routes, or settings).
* Avoid repeating identical nested configuration with only small variations.

<Frame>
  <img alt="The image explains what dynamic blocks do, highlighting their functions to dynamically create nested blocks and avoid repeating identical nested configurations." />
</Frame>

Why use dynamic blocks?

* When a resource contains repeated nested blocks (for example, NSG rules, firewall application rules, or multiple network rules), dynamic blocks keep your code concise and maintainable.
* They are common across Azure networking and security resources and help reduce duplication and human error.

<Frame>
  <img alt="The image outlines when to use dynamic blocks, listing NSG rules, firewall rules, and any resource with repeated nested blocks." />
</Frame>

## Simple NSG example

Start by defining a variable for the ports you want to allow:

```hcl theme={null}
variable "ports" {
  type    = list(number)
  default = [80, 443, 22]
}
```

Then use a dynamic block inside `azurerm_network_security_group` to generate one nested `security_rule` block per port. The `security_rule` iterator gives you `.key` (index) and `.value` (the item):

```hcl theme={null}
provider "azurerm" {
  features {}
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
      priority                   = 100 + security_rule.key   # security_rule.key is the index (0,1,2...)
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

How this works, step by step:

* `for_each = var.ports` iterates over the list of ports.
* For each item, Terraform emits one nested `security_rule` block.
* `security_rule.value` is the current port (e.g., `80`, `443`, `22`).
* `security_rule.key` is the iteration index (`0`, `1`, `2`...), which we used to create unique priorities like `100`, `101`, `102` (via `100 + security_rule.key`).
* Other fields (direction, access, protocol) remain constant for each generated block.

Result (conceptual expansion): for three ports, Terraform will create three nested `security_rule` blocks similar to these:

```hcl theme={null}
