# Enter a value: yes
# random_string.string: Creating...
# random_string.string: Creation complete [id=...]
# local_file.file: Creating...
# local_file.file: Creation complete [id=...]
```

<Callout icon="lightbulb">
  Because `local_file.file` references `random_string.string.id`, OpenTofu automatically creates the string resource first.
</Callout>

## 2. Forcing Replacement by Changing `keepers`

Open `variables.tf` and adjust the default length:

```hcl theme={null}
variable "length" {
  default = 12
}
```

Run another plan:

```bash theme={null}
tofu plan
# Plan: 2 to add, 0 to change, 2 to destroy.
```

Changing anything in the `keepers` map forces the `random_string.string` resource—and thus `local_file.file`—to be replaced on the next apply.

## 3. Ensuring Continuity with `create_before_destroy`

To create the replacement before destroying the old resource, add a lifecycle block:

```hcl theme={null}
resource "random_string" "string" {
  length  = var.length
  keepers = { length = var.length }

  lifecycle {
    create_before_destroy = true
  }
}
```

Apply the update:

```bash theme={null}
tofu apply
# New string is created first, then the old one is removed.
```

You can apply the same pattern to the file resource:

```hcl theme={null}
resource "local_file" "file" {
  filename        = var.filename
  file_permission = var.permission
  content         = random_string.string.id

  lifecycle {
    create_before_destroy = true
  }
}
```

<Callout icon="triangle-alert">
  On disk, you cannot have two files with the same name simultaneously. The old file is destroyed immediately after the new one appears.
</Callout>

## 4. Inspecting Resource State with `tofu show`

To view the details of your current resources, run:

```bash theme={null}
tofu show
# or
tofu state show local_file.file
```

<Frame>
  ![The image shows a code editor with a Terraform configuration file open, displaying resource definitions and lifecycle rules. Below, a terminal window shows the output of a Terraform apply command, indicating resource creation and destruction.](https://kodekloud.com/kk-media/image/upload/v1752882902/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-Lifecycle-Rules/terraform-configuration-code-editor-terminal-output.jpg)
</Frame>

Look for the `id` attribute under the `local_file.file` block.

## 5. Protecting Critical Resources with `prevent_destroy`

First, destroy or clean up existing resources. Then replace your configuration in `main.tf`:

```hcl theme={null}
resource "random_pet" "super_pet" {
  length = var.length
  prefix = var.prefix

  lifecycle {
    prevent_destroy = true
  }
}
```

Define the variables:

```hcl theme={null}
variable "length" {
  default = 12
}

variable "prefix" {
  default = "Mrs"
}
```

Apply:

```bash theme={null}
tofu plan
tofu apply
# Creates the pet resource.
```

Now modify `length` or `prefix`, then run:

```bash theme={null}
tofu apply
```

You’ll encounter:

```plaintext theme={null}
Error: Instance cannot be destroyed

  on main.tf line 1:
   1: resource "random_pet" "super_pet" {

Resource random_pet.super_pet has lifecycle.prevent_destroy set, but the plan calls for this resource to be destroyed. ...
```

The `prevent_destroy` rule blocks any deletion, protecting must-keep resources from accidental removal.

## Lifecycle Arguments Comparison

| Lifecycle Argument      | Purpose                                       | Use Case                                  |
| ----------------------- | --------------------------------------------- | ----------------------------------------- |
| create\_before\_destroy | Create the new resource before destroying old | Zero-downtime upgrades                    |
| prevent\_destroy        | Block any resource deletion                   | Safeguard critical data or infrastructure |

***

You’ve now mastered:

1. How OpenTofu orders resource creation via dependencies
2. Why changing `keepers` forces replacement
3. Using `create_before_destroy` for seamless updates
4. Applying `prevent_destroy` to protect vital resources

***

## Links and References

* [OpenTofu Documentation](https://opentofu.io/docs/)
* [Terraform Fork Overview](https://opentofu.io/)
* [Resource Lifecycle Meta-Arguments](https://www.terraform.io/language/meta-arguments/lifecycle)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/2cab39b9-fcfa-4df5-af2c-0b23c8c8549b" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/a9d4f393-bb13-4fe3-97be-6ce61e655506" />
</CardGroup>


# Demo OpenTofu Commands

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/Demo-OpenTofu-Commands/page

This article provides a hands-on guide to using OpenTofu commands for managing infrastructure-as-code configurations.

Welcome to this hands-on lab on OpenTofu commands. Here, you’ll learn how to visualize, validate, plan, and apply your infrastructure-as-code (IaC) configurations using the `tofu` CLI. By the end of this guide, you’ll be comfortable generating dependency graphs, troubleshooting HCL errors, and managing provider plugins.

## 1. Visualizing Resources

To inspect resource dependencies, generate a DOT graph:

```bash theme={null}
tofu graph > graph.dot
```

You can then render `graph.dot` with [Graphviz](https://graphviz.org/) to visualize your IaC topology.

| Subcommand     | Purpose                              | Example                               |
| -------------- | ------------------------------------ | ------------------------------------- |
| tofu graph     | Generate DOT-format dependency graph | `tofu graph > graph.dot`              |
| tofu validate  | Validate HCL configuration           | `tofu validate`                       |
| tofu plan      | Create an execution plan             | `tofu plan`                           |
| tofu apply     | Apply the planned changes            | `tofu apply`                          |
| tofu fmt       | Format Terraform/OpenTofu files      | `tofu fmt`                            |
| tofu state     | Inspect or modify the state file     | `tofu state show local_file.key_data` |
| tofu providers | Manage provider plugins              | `tofu providers --help`               |

## 2. Validating Configuration

Before creating any resources, validate your HCL syntax and catch typos:

1. Change into your project directory:
   ```bash theme={null}
   cd /root/opentofu-projects/project-shazam
   ```
2. Run the validator:
   ```bash theme={null}
   tofu validate
   ```

<Frame>
  ![The image shows a Visual Studio Code interface with a task description on the left about fixing configuration errors using the tofu validate command. On the right, there's a terminal and file explorer open, displaying a project directory structure.](https://kodekloud.com/kk-media/image/upload/v1752882904/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-Commands/visual-studio-code-task-terminal-explorer.jpg)
</Frame>

If you see:

```text theme={null}
Error: An argument named "dsa_bits" is not expected here.
  on main.tf line 8, in resource "tls_private_key" "private_key":
   8:   dsa_bits = 2048

Did you mean "rsa_bits"?
```

<Callout icon="triangle-alert">
  Always match algorithm-specific arguments. In this case, replace `dsa_bits` with `rsa_bits` for an RSA key.
</Callout>

Correct the block in **main.tf**:

```hcl theme={null}
resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}
```

Re-run `tofu validate` until no errors remain.

## 3. Planning and Applying

### 3.1 Generating a Plan

Create an execution plan to preview changes:

```bash theme={null}
tofu plan
```

You’ll see which resources will be added, changed, or destroyed.

### 3.2 First Apply Attempt

Apply the plan:

```bash theme={null}
tofu apply
```

If you encounter:

```text theme={null}
Error: Provider produced inconsistent final plan
...
inconsistent values for sensitive attribute
```

it means the syntax was valid but some resource arguments are incompatible.

## 4. Fixing the TLS Resource Block

Ensure your `main.tf` includes only RSA-compatible settings and the local file resource:

```hcl theme={null}
resource "local_file" "key_data" {
  filename        = "/tmp/.pki/private_key.pem"
  content         = tls_private_key.private_key.pem
  file_permission = "0400"
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_cert_request" "csr" {
  private_key_pem = file("/tmp/.pki/private_key.pem")
  depends_on      = [local_file.key_data]

  subject {
    common_name  = "flexit.com"
    organization = "FlexIT Consulting Services"
  }
}
```

Re-initialize, plan, and apply:

```bash theme={null}
tofu init
tofu plan
tofu apply
```

If `tofu apply` completes without errors, your configuration is now correct.

## 5. Formatting Code

Keep your files consistent:

```bash theme={null}
tofu fmt
```

This enforces HCL canonical style across all `.tf` files.

## 6. Inspecting State

Query the state for a specific resource:

```bash theme={null}
cd ~/opentofu-projects/project-shazam
tofu state show local_file.key_data
```

Check the `filename` attribute (e.g., `/tmp/.pki/private_key.pem`) to confirm it matches expectations.

## 7. Providers Subcommands

OpenTofu uses providers to interact with external APIs. To list available provider commands:

```bash theme={null}
tofu providers --help
```

Common subcommands include:

* mirror
* list
* install
* remove

## 8. Reviewing Downloaded Providers

Without browsing the directory directly, list installed plugins:

```bash theme={null}
tofu providers
```

<Frame>
  ![The image shows a coding environment with a file explorer and a code editor displaying a JSON file related to Terraform configuration. There is also a terminal at the bottom with commands related to navigating directories and managing provider plugins.](https://kodekloud.com/kk-media/image/upload/v1752882905/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-Commands/coding-environment-json-terraform-terminal.jpg)
</Frame>

You should see entries like:

* `registry.opentofu.org/hashicorp/aws`
* `registry.opentofu.org/hashicorp/local`

***

## Links and References

* [OpenTofu GitHub Repository](https://github.com/opentofu/opentofu)
* [Terraform Concepts](https://www.terraform.io/docs/concepts/index.html)
* [Graphviz Overview](https://graphviz.org/documentation/)
* [TLS Provider Documentation](https://registry.terraform.io/providers/hashicorp/tls/latest/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/d1e2cf32-919d-448c-b8e0-2abdaaa25a01" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/fa965784-46aa-4503-a227-6a5096c4890a" />
</CardGroup>
