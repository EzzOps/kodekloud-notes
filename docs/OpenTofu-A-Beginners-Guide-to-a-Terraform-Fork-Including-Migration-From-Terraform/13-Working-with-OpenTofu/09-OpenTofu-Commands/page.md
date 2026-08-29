# aws_instance.web[0]
# aws_instance.web[1]
# aws_instance.web[2]
```

### Dynamic `count` with `length()`

Instead of hardcoding an integer, drive `count` from a list:

```hcl theme={null}
variable "webservers" {
  type    = list(string)
  default = ["web1", "web2", "web3"]
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = length(var.webservers)

  tags = {
    Name = var.webservers[count.index]
  }
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}
```

Here, each instance tag is assigned by its `count.index`:

* `count.index = 0` → `Name = "web1"`
* `count.index = 1` → `Name = "web2"`
* `count.index = 2` → `Name = "web3"`

<Callout icon="triangle-alert">
  Removing or reordering items in the `webservers` list causes all subsequent resources to be reindexed. This can lead to unintended in-place updates instead of only removing the orphaned resource.
</Callout>

Example plan when deleting `"web1"`:

```plaintext theme={null}
# aws_instance.web[0] will be updated (web1 → web2)
# aws_instance.web[1] will be updated (web2 → web3)
# aws_instance.web[2] will be destroyed (web3)
```

***

## 2. Using `for_each`

The `for_each` meta-argument uses a set or map, giving each resource a stable key based on its value.

```hcl theme={null}
variable "webservers" {
  type    = set(string)
  default = ["web1", "web2", "web3"]
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  for_each      = var.webservers

  tags = {
    Name = each.value
  }
}
```

Run and list state:

```bash theme={null}
tofu apply
tofu state list
# aws_instance.web["web1"]
# aws_instance.web["web2"]
# aws_instance.web["web3"]
```

If you remove `"web1"` from the set and run `tofu plan`, only that resource is destroyed:

```plaintext theme={null}
# aws_instance.web["web1"] will be destroyed
Plan: 0 to add, 0 to change, 1 to destroy.
```

This ensures stable resource addressing and prevents unnecessary updates.

***

## Links and References

* [OpenTofu Documentation](https://docs.opentofu.org)
* [AWS EC2 Instance Resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)
* [Terraform `count` Meta-Argument](https://developer.hashicorp.com/terraform/meta-arguments/count)
* [Terraform `for_each` Meta-Argument](https://developer.hashicorp.com/terraform/meta-arguments/for_each)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/c0fe2879-c597-4c61-857d-cc2debd2f337" />
</CardGroup>


# OpenTofu Commands

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/OpenTofu-Commands/page

OpenTofu CLI helps manage infrastructure with HCL files, covering commands for validation, formatting, visualization, and applying configurations.

OpenTofu provides a powerful CLI for managing infrastructure with HCL files. In this guide, we'll cover the essential `tofu` commands to validate, format, visualize, and apply your configurations.

## OpenTofu Command Overview

| Command          | Purpose                                                  | Example                  |
| ---------------- | -------------------------------------------------------- | ------------------------ |
| `tofu validate`  | Validate HCL syntax and internal consistency             | `tofu validate`          |
| `tofu fmt`       | Reformat HCL files to canonical style                    | `tofu fmt`               |
| `tofu show`      | Display current infrastructure state                     | `tofu show --json`       |
| `tofu providers` | List providers required by configuration and state       | `tofu providers`         |
| `tofu output`    | Read defined outputs or a specific output value          | `tofu output pet-name`   |
| `tofu refresh`   | Refresh state without planning or applying changes       | `tofu refresh`           |
| `tofu plan`      | Show execution plan after refreshing state               | `tofu plan`              |
| `tofu graph`     | Generate a DOT-format dependency graph for visualization | `tofu graph > graph.dot` |

## 1. Validate Configuration

Use `tofu validate` to check your HCL files for syntax errors and internal consistency. It flags errors with precise file and line numbers.

```bash theme={null}
$ tofu validate
Success! The configuration is valid.
```

<Callout icon="lightbulb">
  When validation fails, OpenTofu highlights the incorrect attribute. For example, replace `file permission` with `file_permission` to match HCL naming conventions.
</Callout>

```hcl theme={null}
resource "local_file" "pet" {
  filename        = "/root/pets.txt"
  content         = "We love pets!"
  file_permission = "0700"  # Corrected attribute name
}
```

## 2. Format HCL Files

The `tofu fmt` command enforces a consistent style across all `.tf` files in the current directory, handling indentation, alignment, and spacing automatically.

```bash theme={null}
$ tofu fmt
main.tf
```

## 3. Show Infrastructure State

`tofu show` prints the current state stored by OpenTofu. Add `--json` for a machine-readable output.

```bash theme={null}
$ tofu show --json
{
  "values": { … }
}
```

## 4. Providers

`tofu providers` lists providers declared in your configuration versus those recorded in the state file.

```hcl theme={null}
resource "aws_instance" "db" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

```plaintext theme={null}
$ tofu providers
Providers required by configuration:
.
└── provider[registry.opentofu.org/hashicorp/aws] 4.15.0

Providers required by state:
provider[registry.opentofu.org/hashicorp/aws] 4.15.0
```

## 5. Outputs

Use `tofu output` to inspect all declared outputs or fetch a single output by name.

```hcl theme={null}
resource "local_file" "pet" {
  filename        = "/root/pets.txt"
  content         = "We love pets!"
  file_permission = "0777"
}

resource "random_pet" "cat" {
  length    = 2
  separator = "-"
}

output "content" {
  description = "Print the content of the file"
  value       = local_file.pet.content
}

output "pet-name" {
  description = "Print the name of the pet"
  value       = random_pet.cat.id
}
```

```bash theme={null}
$ tofu output
content  = We love pets!
pet-name = huge-owl

$ tofu output pet-name
pet-name = huge-owl
```

## 6. Refresh and Plan

By default, `tofu plan` and `tofu apply` refresh the state before execution. To update only the state file without planning or applying, run:

```bash theme={null}
$ tofu refresh
random_pet.cat: Refreshing state… [id=bold-coyote]
local_file.pet: Refreshing state… [id=cba595b7d9f94ba1107a46f3f731912d95fb3d2c]
```

This syncs your state with external changes. Then check for drift or planned changes:

```bash theme={null}
$ tofu plan
random_pet.cat: Refreshing state… [id=bold-coyote]
local_file.pet: Refreshing state… [id=cba595b7d9f94ba1107a46f3f731912d95fb3d2c]
No changes. Your infrastructure matches the configuration.
```

## 7. Dependency Graph

Generate a dependency graph in [DOT format](https://graphviz.org/doc/info/lang.html) using `tofu graph`. You can then visualize it with [GraphViz](https://graphviz.org):

```bash theme={null}
$ tofu graph > graph.dot
```

```dot theme={null}
digraph {
  compound = "true"
  newrank = "true"
  subgraph "root" {
    "[root] aws_instance.cerberus (expand)" [label = "aws_instance.cerberus", shape = "box"]
    "[root] provider[\"registry.opentofu.org/hashicorp/aws/\"]" [label = "provider[\"registry.opentofu.org/hashicorp/aws/\"]", shape = "diamond"]
    /* … additional nodes and edges … */
  }
}
```

<Callout icon="lightbulb">
  Save the DOT output (e.g., `graph.dot`) and render it with:

  ```bash theme={null}
  dot -Tpng graph.dot -o graph.png
  ```
</Callout>

## References

* [OpenTofu Documentation](https://opentofu.org/docs)
* [HCL Language Guide](https://github.com/hashicorp/hcl)
* [GraphViz](https://graphviz.org)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/4cf2f489-9c9f-4ede-99d6-5cdfa7df908e" />
</CardGroup>
