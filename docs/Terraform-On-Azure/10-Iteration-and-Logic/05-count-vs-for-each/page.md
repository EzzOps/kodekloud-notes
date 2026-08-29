# azurerm_resource_group.rg[1] will be created
+ resource "azurerm_resource_group" "rg" {
  + id       = (known after apply)
  + location = "westeurope"
  + name     = "rg-resources-1"
}

# azurerm_resource_group.rg[2] will be destroyed
- resource "azurerm_resource_group" "rg" {
  - id       = ".../resourceGroups/rg-resources-2" -> null
  - location = "westeurope" -> null
  - name     = "rg-resources-2" -> null
  - tags     = {} -> null
  -/ # etc.
}

Plan: 1 to add, 0 to change, 1 to destroy.
```

Convert the same example to `for_each` to avoid index shifting

```hcl theme={null}
variable "text" {
  default = "rg"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  for_each = toset(["0", "1", "2"])
  name     = "${var.text}-resources-${each.key}"
  location = "West Europe"
}

resource "azurerm_storage_account" "sa" {
  name                      = "stfx0953764"
  resource_group_name       = azurerm_resource_group.rg["0"].name
  location                  = azurerm_resource_group.rg["0"].location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}
```

Notes on referencing `for_each` results:

* A resource using `for_each` becomes a map keyed by the iteration key. Reference an instance with `azurerm_resource_group.rg["0"].name`.
* Avoid mixing index-based references (e.g., `rg[0]`) with map-style lookups from `for_each`. Use map-style lookups consistently.

Quick comparison: `for_each` vs `count`

| Aspect                           | `for_each`                                                      | `count`                                   |
| -------------------------------- | --------------------------------------------------------------- | ----------------------------------------- |
| Identity                         | Stable keys (strings/maps)                                      | Numeric indexes                           |
| Best for                         | Resources with meaningful identifiers (names, IDs, DNS records) | N indistinguishable, ordinal resources    |
| Reference style                  | `resource.name["key"]`                                          | `resource.name[index]`                    |
| Resilience to reordering/removal | High — keyed instances remain stable                            | Low — index shifts cause recreate/destroy |

Typical local workflow

```bash theme={null}
terraform init
terraform plan
terraform apply --auto-approve
```

Example apply output (abridged):

```plaintext theme={null}
Plan: 4 to add, 0 to change, 0 to destroy.

azurerm_resource_group.rg["0"]: Creating...
azurerm_resource_group.rg["0"]: Creation complete after 23s [id=/subscriptions/.../resourceGroups/rg-resources-0]
azurerm_resource_group.rg["1"]: Creating...
azurerm_resource_group.rg["1"]: Creation complete after 23s [id=/subscriptions/.../resourceGroups/rg-resources-1]
azurerm_resource_group.rg["2"]: Creating...
azurerm_resource_group.rg["2"]: Creation complete after 23s [id=/subscriptions/.../resourceGroups/rg-resources-2]
azurerm_storage_account.sa: Creating...
azurerm_storage_account.sa: Creation complete after 1m1s [id=/subscriptions/.../resourceGroups/rg-resources-0/providers/Microsoft.Storage/storageAccounts/stfx0953764]

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
```

Targeting and destroying a single `for_each` instance

* Using `terraform destroy --target 'azurerm_resource_group.rg["0"]'` or `terraform apply -target=...` is possible but generally discouraged for routine operations. Terraform will warn you when targeting because the plan may not represent all configuration changes.

Example warning when using `-target` (abridged):

```plaintext theme={null}
Warning: Resource targeting is in effect

You are creating a plan with the -target option, which means that the result of this plan may not represent all of the changes requested by the current configuration.
The -target option is not for routine use...
```

<Callout icon="warning">
  Avoid relying on `-target` for normal workflows. Targeting can produce incomplete or unsafe plans when resources have dependencies, and may cause unintended changes.
</Callout>

Recommended pattern to remove an instance managed by `for_each`

1. Update the collection used by `for_each` to remove the key you want to delete.
2. Run `terraform plan` and `terraform apply`. Terraform will plan and destroy only the resource whose key was removed and leave other keyed instances intact.

Example: remove the instance with key `"1"`

Before:

```hcl theme={null}
variable "resource_groups" {
  type    = set(string)
  default = ["0", "1", "2"]
}
```

After (removed `"1"`):

```hcl theme={null}
variable "resource_groups" {
  type    = set(string)
  default = ["0", "2"]   # removed "1"
}
```

Then:

```bash theme={null}
terraform plan
terraform apply
```

Resulting plan shows only the removed key scheduled for destruction:

```plaintext theme={null}
# azurerm_resource_group.rg["1"] will be destroyed
- resource "azurerm_resource_group" "rg" {
    id       = "/subscriptions/.../resourceGroups/rg-resources-1"
    name     = "rg-resources-1" -> null
    location = "West Europe" -> null
    tags     = {} -> null
}
Plan: 0 to add, 0 to change, 1 to destroy.
```

Summary and best practices

* Use `for_each` when instances have meaningful identities (names, subnet IDs, DNS records, etc.). It maps instances to stable keys and prevents index-driven recreation.
* Use `count` only when you truly need N indistinguishable, ordinal resources.
* Reference `for_each` instances with `resource.name["key"]`, and avoid mixing indexing styles.
* To remove a single instance, remove its key from the `for_each` collection and `apply` the change. Avoid `-target` unless you fully understand the dependency implications.

Links and references

* [Terraform: Meta-arguments — for\_each and count](https://www.terraform.io/docs/language/meta-arguments/for_each.html)
* [Terraform: Expressions — each object](https://www.terraform.io/docs/language/expressions/each.html)
* [Azure Provider (azurerm) Documentation](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/316db583-71fc-4563-8f19-72bbf9be8a2b" />
</CardGroup>


# count vs for each

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Iteration-and-Logic/count-vs-for-each/page

Explains Terraform's count versus for_each, how they track resource identity, risks of index shifts, and best practices for stable resources.

This article compares Terraform's `count` and `for_each` meta-arguments. Both create multiple instances of a resource from a collection, but they record resource identity differently in the Terraform state. Choosing the wrong one can cause unexpected resource deletion and recreation in production—so understanding the differences is important.

Quick overview

* `count` creates instances indexed by number: `resource.example[0]`, `resource.example[1]`.
* `for_each` creates instances keyed by an element from the collection: `resource.example["key"]`.

Minimal usage examples

```hcl theme={null}
