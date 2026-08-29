# Define shared values in locals
locals {
  environment = "dev"
  prefix      = "myorg"
}

resource "github_repository" "dev_repo" {
  name        = "${local.prefix}-${local.environment}-repo"
  visibility  = "private"
  description = "Terraform-managed repo for dev environment"
}

resource "github_team" "awesome_people" {
  name        = "${local.prefix}-${local.environment}-team"
  description = "My Awesome Team"
  privacy     = "closed"
}
```

Now `local.prefix` and `local.environment` are the single source of truth for these names. Change them once to propagate updates.

## Grouping locals and referencing locals from locals

You can have multiple `locals` blocks for readability. Locals may reference other locals (avoid circular references).

Example: group common tags and reference a local inside another locals block:

```hcl theme={null}
locals {
  app_team = "customer-experience"
}

locals {
  # Common tags to be applied to resources
  common_tags = {
    Name      = var.app_name
    Owner     = var.owner
    App       = var.app
    Service   = "${var.team}-${var.app}-${var.environment}"
    AppTeam   = local.app_team
    CreatedBy = data.aws_caller_identity.current.account_id
    Image     = data.aws_ami.ubuntu.name
  }
}
```

Then apply the `local.common_tags` map to any resource that supports tags:

```hcl theme={null}
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = var.aws_subnet.public_subnets[0]
  tags          = local.common_tags
}
```

All resources referencing `local.common_tags` will receive the same tag set; updating the tags in one place affects every resource.

<Frame>
  <img alt="The image outlines the benefits of using locals in HashiCorp Terraform, highlighting centralized logic, clearer code, and less risk." />
</Frame>

## When to use locals

Locals are particularly useful for:

* Computed or derived values — combine variables, data sources, or inputs into a consistent format (naming conventions, tag values).
* Reusing constants — store project prefixes, environment names, or common tag maps so you only update one place.
* Complex expressions — move long or nested Terraform functions into named locals to keep resource blocks readable.

Use the following table to decide where locals can provide the most value:

| Use case            | Why use locals                                  | Example                                                       |
| ------------------- | ----------------------------------------------- | ------------------------------------------------------------- |
| Naming conventions  | Ensures consistent names across resources       | `local.prefix = "acme"`                                       |
| Tag standardization | Apply consistent tags to many resources         | `local.common_tags = { Owner = var.owner }`                   |
| Derived values      | Combine multiple inputs into one expression     | `local.service = "${var.team}-${var.app}-${var.environment}"` |
| Complex expressions | Shorten resource blocks and improve readability | `local.subnet_ids = compact(var.subnets)`                     |

<Callout icon="lightbulb">
  Use locals to centralize logic and keep resources focused on resource-specific configuration. Avoid placing heavy computation directly inside resource arguments; compute it once in a local and reference it.
</Callout>

## Practical considerations and best practices

* Locals can reference variables, data sources, and other locals — but do not create circular references.
* Locals are evaluated during plan/apply and are not stored in state.
* Give locals descriptive names and group related locals together to make them discoverable.
* Prefer maps or objects (e.g., a `common_tags` map) for shared sets of attributes rather than repeating keys across resources.
* Use locals to hide complexity, but don’t overuse them to obscure obvious values.

<Frame>
  <img alt="The image is a presentation slide explaining when to use local values in code, highlighting their role in maintaining readability and consistency, and features a photo of a laptop on a purple background." />
</Frame>

## Summary

Locals reduce repetition, centralize logic, and make complex expressions easier to manage. They serve as a single source of truth for commonly repeated values—change once, and every reference updates.

Hands-on exercise: refactor a small module by extracting duplicated names, tag maps, and repeated computed expressions into `locals`, then run `terraform plan` to verify the consolidated changes.

## Links and references

* [Terraform Language: Locals](https://developer.hashicorp.com/terraform/language/values/locals)
* [Terraform Best Practices](https://www.terraform.io/docs/configuration/index.html)
* [HashiCorp Learn - Terraform](https://learn.hashicorp.com/terraform)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/6c9d4950-5cea-4fbf-bad4-ef75a8d8ef5b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/a08f0c74-20c7-4741-88df-6f8b07745ae9" />
</CardGroup>


# Using the count Meta Argument

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Marking-Code-Reusable/Using-the-count-Meta-Argument/page

Explains Terraform's count meta-argument for creating multiple resource instances using count.index, differences from for_each, and tips to manage indexing and identity stability.

The `count` meta-argument in Terraform lets you create multiple instances of the same resource from a single resource block. It uses a zero-based numeric index (`count.index`) that you can reference inside the resource to produce unique names, tags, or other per-instance values. This makes `count` ideal when you need several identical or nearly-identical resources, or when the number of instances should be driven by a variable.

<Callout icon="lightbulb">
  Use `count` when you want to scale identical resources by number. For stable identities or keyed collections, consider `for_each` instead (see the comparison below).
</Callout>

<Frame>
  <img alt="The image explains the count meta-argument in Terraform, which allows creating multiple instances of a resource using a single block, assigns an index to each instance, and describes how to reference the resource." />
</Frame>

## How `count` works

* Set `count` to a number or a numeric variable (for example, `var.vm_count`).
* Terraform creates that many instances and assigns each a numeric index starting at `0`.
* Inside the resource you can reference `count.index` to create unique values per instance.
* To address an individual instance from another resource or an output, use an index on the resource address (for example: `aws_instance.example[1]`).

Example: create multiple Azure VMs driven by a variable and use `count.index` to generate unique names.

```hcl theme={null}
variable "vm_count" {
  type    = number
  default = 3
}

resource "azurerm_virtual_machine" "example" {
  count               = var.vm_count
  name                = "vm-${count.index}"
  location            = "East US"
  resource_group_name = "my-resource-group"
  vm_size             = "Standard_D2s_v3"

  os_profile {
    computer_name  = "vm-${count.index}"
    admin_username = "adminuser"
  }
}
```

With `vm_count = 3`, Terraform will create VMs named `vm-0`, `vm-1`, and `vm-2`.

## Referencing instances

* Address the first instance: `azurerm_virtual_machine.example[0]`
* Get the name of the second instance: `azurerm_virtual_machine.example[1].name`
* Collect all names into an output:

```hcl theme={null}
output "vm_names" {
  value = azurerm_virtual_machine.example[*].name
}
```

## Common uses and tips

* Use `count.index` inside `name`, `tags`, or properties that accept strings to ensure uniqueness.
* Combine `count` with other functions (for example, `count = var.vm_count > 0 ? var.vm_count : 0`) to handle conditional creation.
* Avoid using `count` with resources that require stable identity across changes if individual items will be added/removed frequently — the numeric indexing can shift.

## count vs for\_each

| Feature         | `count`                                          | `for_each`                                             |
| --------------- | ------------------------------------------------ | ------------------------------------------------------ |
| Indexing        | Numeric, zero-based `count.index`                | Keyed by element value or map keys                     |
| Stable identity | No — indices shift if items are inserted/removed | Yes — each key maps to a stable instance               |
| Use-case        | Create N identical instances, scale by a number  | Create instances from a set/map where identity matters |
| Example         | `count = var.vm_count`                           | `for_each = toset(["a","b","c"])`                      |

## When to prefer for\_each

If you need stable, predictable identities for each instance (for example, when adding/removing single items), `for_each` is usually safer because it keys resources by a set or map value instead of a shifting numeric index.

<Callout icon="warning">
  Because `count` is index-based, changing the number or ordering of instances can shift indices and cause Terraform to delete and recreate resources. If you need stable identities for resources, prefer `for_each`.
</Callout>

## References

* [Terraform: Resource Meta-Arguments — count](https://www.terraform.io/language/meta-arguments/count)
* [Terraform: for\_each vs count](https://www.terraform.io/docs/language/meta-arguments/for_each.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/ceb1f393-8428-4839-928b-f3e24e477ff8" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/3d337c54-316c-4031-8293-2f2a107fd591" />
</CardGroup>
