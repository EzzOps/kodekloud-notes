# Using the for each Meta Argument

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Marking-Code-Reusable/Using-the-for-each-Meta-Argument/page

Explains Terraform's for_each meta-argument for creating uniquely configured resources, how it differs from count, usage of each.key and each.value, and addressing instances by key.

In this lesson you'll learn how to use Terraform's `for_each` meta-argument to create multiple, uniquely configured resources from a single resource block. `for_each` is a more flexible alternative to `count` when you need per-resource uniqueness rather than many identical instances.

Why use `for_each` (versus `count`)

* `for_each` iterates over a map or set, allowing unique configuration per instance.
* Each instance receives a stable key (the map key or set element) instead of an index. This stability reduces accidental recreation of unrelated resources when items are added or removed.
* Use `for_each` when resources need different names, sizes, tags, networks, or other unique attributes.
* Inside the resource block you can reference `each.key` and `each.value` to access the current item.

Example: map of VM names to sizes

```hcl theme={null}
variable "vms" {
  type    = map(string)
  default = {
    "vm1" = "Standard_D2s_v3"
    "vm2" = "Standard_D4s_v3"
    "vm3" = "Standard_B2ms"
  }
}

resource "azurerm_virtual_machine" "example" {
  for_each            = var.vms
  name                = each.key
  location            = "East US"
  resource_group_name = "my-resource-group"
  vm_size             = each.value

  os_profile {
    computer_name  = each.key
    admin_username = "adminuser"
  }

  # Additional required blocks (networking, storage, etc.) omitted for brevity.
}
```

Because `var.vms` contains three key/value pairs, Terraform creates three VMs: `vm1`, `vm2`, and `vm3`, each with its configured size.

Referencing resources created with `for_each`

* Address an individual instance by its key in square brackets:
  * `azurerm_virtual_machine.example["vm1"]`
  * `azurerm_virtual_machine.example["vm2"]`
  * `azurerm_virtual_machine.example["vm3"]`
* Use these keyed references when wiring resources together (for example, passing an instance ID or IP to another resource).

Using `each.key` and `each.value` inside the block

* `each.key` is the map key (here, the VM name).
* `each.value` is the map value (here, the VM size).
* You can reference `each.key`/`each.value` multiple times to configure name, tags, hostnames, and more.
* Combine them in interpolations. For example, to add a suffix to the computer name:

```hcl theme={null}
os_profile {
  computer_name  = "${each.key}-web"
  admin_username = "adminuser"
}
```

Use cases and recommendations

* Prefer `for_each` when instances require distinct attributes or when you want stable addressing that won’t shift as you add or remove items.
* `count` is still useful when creating many identical resources where uniqueness is not needed.
* Map values can be primitive (strings, numbers) or nested objects to carry richer per-resource configuration (regions, tags, disk sizes, network IDs, etc.).

Comparison: `for_each` vs `count`

| Feature           | `for_each`                                  | `count`                             |
| ----------------- | ------------------------------------------- | ----------------------------------- |
| Iterates over     | `map` or `set`                              | integer range                       |
| Stable addressing | Yes — keyed by map/set element (`each.key`) | No — indexed by position (`0..n-1`) |
| Best for          | Resources with unique attributes            | Repeated identical resources        |
| Example           | `for_each = var.vms`                        | `count = var.instance_count`        |

<Callout icon="lightbulb">
  Prefer `for_each` when your instances have unique attributes or when you want stable instance addressing that won't shift as items are added or removed.
</Callout>

<Callout icon="warning">
  When converting existing resources from `count` to `for_each` (or vice versa), resource addresses change. This can cause Terraform to plan to recreate resources unless you import or manipulate state appropriately. Always review the plan and consider state migration steps.
</Callout>

Links and references

* [Terraform: for\_each Meta-Argument](https://www.terraform.io/docs/language/meta-arguments/for_each.html)
* [Terraform: count Meta-Argument](https://www.terraform.io/docs/language/meta-arguments/count.html)

That covers the `for_each` meta-argument and how it compares to `count`. Use `for_each` to keep your configuration DRY while enabling per-resource uniqueness and stable addressing.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/461404b6-76bc-41c3-84cf-bbe67b90f70d" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/e6c5a742-8d30-4cb2-992e-9fa70f66cb0e" />
</CardGroup>
