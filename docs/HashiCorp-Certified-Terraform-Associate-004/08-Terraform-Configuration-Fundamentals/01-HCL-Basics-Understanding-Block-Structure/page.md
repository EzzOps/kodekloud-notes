# Azure resource examples
resource "azurerm_resource_group" "prd" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_virtual_network" "dv" {
  name                = "example-network"
  resource_group_name = azurerm_resource_group.prd.name
  location            = azurerm_resource_group.prd.location
  address_space       = ["10.0.0.0/16"]
}
```

Use outputs to export values that are consumed outside this configuration—root modules, CI pipelines, or manual testers.

## Basic output examples (AWS resources)

Below are typical outputs you might declare for an EC2 instance and a load balancer. These show simple attribute exposure, composed values, and how to produce a ready-to-use URL.

```hcl theme={null}
# Output Instance IP Address
output "instance_public_ip" {
  description = "Public IP of Server"
  value       = aws_instance.web.public_ip
}

# Output DNS Name for Load Balancer
output "website_dns" {
  description = "Website DNS Record"
  value       = aws_elb.web_app.dns_name
}

# Output Friendly URL of Website
output "website_url" {
  description = "Friendly URL for the website"
  value       = "https://${aws_alb.web.dns_name}"
}
```

* `instance_public_ip`: exposes a single resource attribute.
* `website_dns`: exports the load balancer's DNS name.
* `website_url`: composes a click-ready HTTPS URL around a resource attribute.

## Dissecting an `output` block

Each output block typically contains a few common elements:

| Field         | Purpose                                                                                | Example                      |
| ------------- | -------------------------------------------------------------------------------------- | ---------------------------- |
| `name`        | Identifier used to reference the output                                                | `instance_public_ip`         |
| `description` | Optional human-readable explanation                                                    | `"Public IP of Server"`      |
| `value`       | Expression that computes the output (resource attributes, maps, lists, or expressions) | `aws_instance.web.public_ip` |
| `sensitive`   | Hides the value in CLI and logs when set to `true`                                     | `sensitive = true`           |

Use `description` to document intent and `sensitive` to prevent accidental exposure in terminal output.

## Common `terraform output` commands

Use these commands locally or in automation:

| Command                        | What it does                                             |
| ------------------------------ | -------------------------------------------------------- |
| `terraform output`             | Show all outputs (non-sensitive values hidden if marked) |
| `terraform output website_url` | Show a single output by name                             |
| `terraform output -json`       | Emit all outputs in JSON for scripts and CI              |

## Sensitive outputs

Mark outputs that contain secrets so Terraform hides them in interactive CLI output and most logs.

```hcl theme={null}
output "db_password" {
  description = "RDS master password"
  value       = aws_db_instance.default.password
  sensitive   = true
}
```

> **lightbulb** Mark outputs as `sensitive = true` for any secret or credential. Sensitive outputs are still recorded in the Terraform state (so secure your backend accordingly). Treat your state file as sensitive data.

## Best practices and important considerations

* Remember outputs are stored in state: protect your state backend and access control.
* Limit outputs to values that are useful externally (URLs, IPs, IDs required by other systems).
* Prefer secret managers for long-term secret storage; do not rely solely on outputs for sensitive secrets.
* Use outputs to pass data between modules: a child module declares outputs that the parent (or other modules) can read.
* Avoid exposing low-value or noisy attributes that are not consumed by other systems.

> **warning** Do not store highly sensitive secrets only in outputs unless your state backend is secured and access is tightly controlled. Consider using dedicated secret management solutions for production secrets.

## Quick reference table

| Use case                  | Example output                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| Expose a single attribute | `output "instance_public_ip" { value = aws_instance.web.public_ip }`                           |
| Compose a URL             | `output "website_url" { value = "https://${aws_alb.web.dns_name}" }`                           |
| Return structured data    | `output "subnet_map" { value = { public = aws_subnet.pub.id, private = aws_subnet.priv.id } }` |
| Mark sensitive values     | `output "db_password" { value = var.db_password, sensitive = true }`                           |

## Summary

* `output` blocks provide a structured way to expose information from Terraform configurations.
* Outputs appear after `terraform apply`, are stored in state, and can be consumed by scripts, CI pipelines, and other modules.
* Use `description` and `sensitive` to make outputs easier and safer to use.
* Keep outputs focused on externally useful values and secure your state backend.

Further reading and references:

* [Terraform Outputs Documentation](https://www.terraform.io/docs/cli/commands/output.html)
* [Terraform State Concepts](https://www.terraform.io/docs/state/index.html)
* [Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/b170a16c-2fe0-4561-aca0-c37474762dce)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/c8f283e2-b2d4-4ad5-a340-3d2ab32ab665)


# HCL Basics Understanding Block Structure

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Configuration-Fundamentals/HCL-Basics-Understanding-Block-Structure/page

Overview of Terraform HCL block structure, explaining block anatomy, common block types, meta-arguments, examples, modules, and import workflow for infrastructure as code

In this lesson you’ll learn why Terraform’s block-oriented syntax (HCL — HashiCorp Configuration Language) makes infrastructure-as-code easier to author, maintain, and reuse. HCL was designed to be both human-readable and machine-friendly, and Terraform’s block structure provides clear semantics, modularity, and composability for real-world infrastructure.

Terraform language reference: [https://developer.hashicorp.com/terraform/language](https://developer.hashicorp.com/terraform/language)

## Why the block structure matters

* Clear intent: Each block type has an explicit role (for example, `provider` vs `resource`), which makes configurations easier to read and reason about.
* Modularity: Blocks compose naturally — use the right block types for discrete concerns and group them into modules.
* Reusability: Consistent block patterns enable shareable modules, predictable behavior, and cleaner team collaboration.
* Predictability: Meta-arguments and nested/dynamic blocks let you express common patterns (scaling, dependencies, lifecycle) declaratively.

## Block anatomy (high level)

A Terraform block usually has three parts:

1. Block type — e.g., `resource`, `provider`, `module`, `variable`.
2. Optional labels — resource blocks often include a type and a name: `resource "<TYPE>" "<NAME>"`.
3. Block body — arguments and nested blocks inside `{ ... }`.

Minimal example of a generic block:

```hcl theme={null}
<block_type> "<label1>" "<label2>" {
  # arguments and nested blocks
}
```

Blocks can also include meta-arguments such as `count`, `for_each`, `depends_on`, and `lifecycle`. Use nested blocks and `dynamic` blocks when you need to generate block content programmatically from data structures.

## Quick reference: common block types

| Block type | Purpose                                                                                | Example                                                                                                                                       |
| ---------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Provider   | Connects Terraform to an external platform and configures credentials, region, etc.    | `provider "aws" { region = "us-west-2" }`                                                                                                     |
| Resource   | Declares infrastructure objects Terraform manages (VMs, networks, storage, DNS, etc.). | `resource "aws_instance" "web" { ami = "ami-123" instance_type = "t3.micro" }`                                                                |
| Data       | Reads information about existing resources or external sources without creating them.  | `data "aws_ami" "ubuntu" { most_recent = true }`                                                                                              |
| Variable   | Declares input variables to parameterize configurations.                               | `variable "instance_type" { type = string; default = "t3.micro" }`                                                                            |
| Output     | Exposes values from the applied configuration for other systems or users.              | `output "instance_ip" { value = aws_instance.web.public_ip }`                                                                                 |
| Terraform  | Configures Terraform itself (`required_providers`, backend settings, etc.).            | `terraform { required_providers { aws = { source = "hashicorp/aws"; version = "~> 4.0" } }; backend "s3" { bucket = "my-terraform-state" } }` |
| Module     | Groups related resources and references reusable configurations via `source`.          | `module "network" { source = "./modules/network"; cidr = "10.0.0.0/16" }`                                                                     |

## Examples and common patterns

Provider block (configure a cloud provider):

```hcl theme={null}
provider "aws" {
  region = "us-west-2"
  profile = "team-account"
}
```

Resource block (create an EC2 instance):

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-0abcd1234efgh5678"
  instance_type = var.instance_type

  tags = {
    Name = "web-server"
  }
}
```

Data block (read the most recent Ubuntu AMI):

```hcl theme={null}
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
```

Variable and output blocks (parameterize and expose values):

```hcl theme={null}
variable "instance_type" {
  type    = string
  default = "t3.micro"
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

Terraform settings block (required providers + backend):

```hcl theme={null}
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "project/terraform.tfstate"
    region = "us-west-2"
  }
}
```

Module usage (reuse a network module):

```hcl theme={null}
module "network" {
  source = "git::https://github.com/example/terraform-modules.git//network"
  cidr   = "10.0.0.0/16"
}
```

## Meta-arguments and advanced nesting

Common meta-arguments:

* `count` — create multiple instances of a block.
* `for_each` — iterate across maps/sets to create multiple resources with unique keys.
* `depends_on` — explicitly express ordering dependencies.
* `lifecycle` — fine-tune creation/update/delete behavior.

Example with `for_each` and `lifecycle`:

```hcl theme={null}
resource "aws_security_group" "sg" {
  for_each = toset(var.environments)

  name = "sg-${each.key}"

  lifecycle {
    prevent_destroy = true
  }
}
```

Dynamic blocks let you conditionally create nested blocks based on input data:

```hcl theme={null}
resource "aws_lb_listener" "http" {
  dynamic "default_action" {
    for_each = var.create_redirect ? [1] : []
    content {
      type = "redirect"
      redirect {
        protocol = "HTTPS"
        port     = "443"
      }
    }
  }
}
```

## Importing existing resources into state

Terraform does not have an “import block.” The import workflow is:

1. Add a matching `resource` block to your configuration that reflects the existing external object.
2. Run:
   `terraform import <resource_address> <external_id>`
3. Run `terraform plan` and update your configuration fields to match the imported resource attributes.

See the official docs for details: [https://developer.hashicorp.com/terraform/cli/import](https://developer.hashicorp.com/terraform/cli/import)

## Scope and next steps

This overview covers the most commonly used block types and patterns. Terraform also includes other constructs such as `locals`, provisioners, provider-specific nested blocks, and advanced patterns for module composition. Explore individual reference pages and tutorials for in-depth examples and best practices.

> **lightbulb** This lesson provided a conceptual overview of Terraform’s block structure and the primary block types you'll use. For hands-on examples, syntax rules, and advanced patterns for each block type, consult the official Terraform language documentation and provider-specific guides.

## Links and references

* Terraform language docs: [https://developer.hashicorp.com/terraform/language](https://developer.hashicorp.com/terraform/language)
* Terraform CLI import docs: [https://developer.hashicorp.com/terraform/cli/import](https://developer.hashicorp.com/terraform/cli/import)
* Module registry and examples: [https://registry.terraform.io/](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/0313a316-274a-47d7-b188-471f6d4bcf1b)
