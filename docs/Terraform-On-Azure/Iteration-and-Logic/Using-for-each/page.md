# azurerm_resource_group.rg[0] will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "westeurope"
    + name     = "rg-resources-0"
  }

# azurerm_resource_group.rg[1] will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "westeurope"
    + name     = "rg-resources-1"
  }

# azurerm_resource_group.rg[2] will be created
+ resource "azurerm_resource_group" "rg" {
    + id       = (known after apply)
    + location = "westeurope"
    + name     = "rg-resources-2"
  }

Plan: 3 to add, 0 to change, 0 to destroy.
```

2. Creating a related resource per index

To create one storage account per resource group when both use `count`, use the same index so instances map 1:1:

```hcl theme={null}
resource "azurerm_storage_account" "sa" {
  count                     = 3
  name                      = "stfx${count.index}"
  resource_group_name       = azurerm_resource_group.rg[count.index].name
  location                  = azurerm_resource_group.rg[count.index].location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}
```

This maps `sa[0]` → `rg[0]`, `sa[1]` → `rg[1]`, and so on. Using matching indexes is a straightforward approach when instances should be paired by position.

3. Binding all instances to a single (first) resource group

If instead you reference a single index explicitly, all of your resources can be tied to that specific instance:

```hcl theme={null}
resource "azurerm_storage_account" "sa" {
  name                = "stfx0"
  resource_group_name = azurerm_resource_group.rg[0].name
  location            = azurerm_resource_group.rg[0].location
  account_tier        = "Standard"
  account_replication_type = "LRS"
}
```

If `sa` uses `count`, every `sa[i]` will be bound to `rg[0]`. If `sa` does not use `count`, this resource is simply created once in `rg[0]`.

Reducing `count` and the destroy behavior

* Decreasing `count` from `3` to `2` on `azurerm_resource_group.rg` causes Terraform to plan to destroy `rg[2]` (the highest index), because identities are positional. Example plan when decreasing:

```bash theme={null}
# azurerm_resource_group.rg[2] will be destroyed
- resource "azurerm_resource_group" "rg" {
    - id       = "/subscriptions/.../resourceGroups/rg-resources-2" -> null
    - location = "westeurope" -> null
    - name     = "rg-resources-2" -> null
  }

Plan: 0 to add, 0 to change, 1 to destroy.
```

Targeting and dependent resources

* Removing a middle index (for example `rg[1]`) is non-trivial. A targeted destroy like:

```bash theme={null}
terraform destroy --target 'azurerm_resource_group.rg[1]'
```

may still affect other resources. Terraform recalculates dependencies and the collection-level state, so dependent resources can be refreshed, recreated, or destroyed if their references or the collection’s structure change.

Important takeaway: targeted operations on counted collections can trigger complex cascades because Terraform maintains collection-level identity and dependency relationships. Removing a middle item often results in recomputations or recreations to keep indices consistent.

Why `for_each` is often better

* `count` uses numeric, positional identity.
* `for_each` uses stable keys (map keys or set elements) to give each instance a stable identity. With `for_each`, reordering, partial removals, or additions are less likely to cause unintended resource recreations.

Comparison at a glance

| Feature        |                                                    `count` | `for_each`                                                             |
| -------------- | ---------------------------------------------------------: | ---------------------------------------------------------------------- |
| Identity model |                                 Numeric index (positional) | Stable key (map/set element)                                           |
| Good for       |            Simple duplication with index-based differences | Stable, key-based instances that survive reordering/removal            |
| Changing size  | Removes highest indices first; middle removals are complex | Removing a key removes that specific instance without shifting others  |
| Best use case  |       Short-lived or ephemeral infrastructure, quick demos | Long-lived infra where individual resource identity must remain stable |

<Callout icon="warning">
  Avoid using `count` for resources where instance identity must remain stable across reorders, removals, or updates. Prefer `for_each` when you need deterministic, key-based identities for individual instances.
</Callout>

Summary

* `count` is a simple and effective way to duplicate resources when instance identity is purely positional.
* Instances are identified by `index` (0..N-1). Changes to `count` add or remove instances at the end of the list.
* Removing a middle instance can lead to unintended destroys or recreations because identity is positional.
* For stable identities and safer updates, use `for_each`.

Links and references

* Official Terraform docs: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* `for_each` vs `count` guidance: [https://www.terraform.io/docs/language/meta-arguments/count.html](https://www.terraform.io/docs/language/meta-arguments/count.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/fb5019bb-df21-4583-818e-6dae40fde2ec/lesson/7200843c-0c99-4508-95e2-14e9dac71d63" />
</CardGroup>


# Using for each

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Iteration-and-Logic/Using-for-each/page

Explains Terraform's for_each to create stable keyed resources, preventing index shifting versus count, with Azure examples and best practices for safe resource management.

In this lesson we cover Terraform's `for_each` meta-argument — the recommended way to create multiple resources when instance identity and lifecycle stability matter. Unlike `count`, `for_each` ties each resource instance to a meaningful key, which prevents index-shifting and makes changes safer and more predictable for production workloads.

<Frame>
  <img alt="The image has a gradient blue background with the text &#x22;Using for_each&#x22; in white in the center." />
</Frame>

Why use `for_each`? When resources are keyed by meaningful identifiers (names, subnet IDs, DNS names, etc.), Terraform can track each resource independently. This prevents accidental destruction and recreation caused by reordering or changing collections that are tracked only by numeric indexes.

<Frame>
  <img alt="The image has a blue gradient background with the text &#x22;Using for_each&#x22; in the center. In the bottom left corner, it says &#x22;Copyright KodeKloud&#x22;." />
</Frame>

Example: create a resource group for every element in a set

```hcl theme={null}
variable "resource_groups" {
  type    = set(string)
  default = ["rg-dev", "rg-prod"]
}

resource "azurerm_resource_group" "rg" {
  for_each = var.resource_groups
  name     = each.key
  location = "eastus"
}
```

Key notes about this example:

* `variable.resource_groups` is declared as `set(string)`: a collection of unique values without a guaranteed order.
* `for_each = var.resource_groups` creates one resource instance per element in the set.
* When iterating a set, both `each.key` and `each.value` refer to the element value (e.g., `"rg-dev"` and `"rg-prod"`). When iterating a map, `each.key` is the map key and `each.value` is the map value.

Because `for_each` uses meaningful keys rather than numeric indexes, Terraform state does not shift when you add or remove other items. This makes `for_each` far safer than `count` in many production scenarios.

<Callout icon="lightbulb">
  Prefer `for_each` when each resource has a meaningful identifier (name, subnet ID, DNS name, etc.). Use `count` only for N identical resources where individual identity or lifecycle does not matter.
</Callout>

Why index-based `count` is brittle

With `count`, Terraform identifies resources by their numeric index (0, 1, 2, ...). Reordering or removing elements can change those indexes and cause Terraform to destroy and recreate resources unnecessarily.

count-style example (index-based):

```hcl theme={null}
variable "text" {
  default = "rg"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  count    = 3
  name     = "${var.text}-resources-${count.index}"
  location = "westeurope"
}

resource "azurerm_storage_account" "sa" {
  count                     = 3
  resource_group_name       = azurerm_resource_group.rg[0].name
  location                  = azurerm_resource_group.rg[0].location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}
```

A truncated plan showing index-based change:

```plaintext theme={null}
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create
  - destroy

Terraform will perform the following actions:
