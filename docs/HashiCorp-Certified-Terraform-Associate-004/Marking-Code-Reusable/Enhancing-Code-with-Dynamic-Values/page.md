# Enhancing Code with Dynamic Values

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Marking-Code-Reusable/Enhancing-Code-with-Dynamic-Values/page

Using variables, data sources, locals, and interpolation to replace hard-coded values so Terraform configurations are reusable, adaptable, and safe across environments, accounts, and regions

Keeping Terraform code reusable means avoiding hard-coded values. This guide explains how to replace static literals with dynamic values using variables, data sources, locals, and interpolation. These patterns make your configurations adaptable across accounts, regions, and environments, reduce repetition, and lower the risk of errors.

<Callout icon="lightbulb">
  Use variables, data sources, and locals to assemble names, tags, and arguments dynamically so a single set of Terraform files can be reused across environments (dev/stage/prod), accounts, and regions.
</Callout>

Why use dynamic values?

* Reusability: One configuration can handle many environments.
* Maintainability: Update variable defaults or data lookups instead of editing every resource.
* Safety: Avoid accidental drift caused by manually changing literal values.
* Uniqueness: Build unique names (for S3, role names, etc.) programmatically.

Quick recap: variables
Variables let you pass values into Terraform modules and root modules. Terraform supports types like string, number, bool, list, map, and object, and variables can be set using defaults, `-var`/`.tfvars` files, or environment variables.

<Frame>
  <img alt="The image is a recap of Terraform variables, featuring three sections: dynamic inputs, variable types, and keeping code DRY, each with brief explanations." />
</Frame>

Brief reminder: data sources
Data sources (data blocks) allow Terraform to read information from providers—such as the latest AMI, the current account ID, or regions—so you can reference existing infrastructure or provider metadata without creating or managing it.

<Frame>
  <img alt="The image is a graphic titled &#x22;Data Sources - Reap,&#x22; explaining how to use data sources in Terraform to pull external information. It highlights provider-specific information, common use cases, and that data sources do not make changes to infrastructure." />
</Frame>

Static (anti-pattern) vs. dynamic (recommended)
Below is a direct comparison that highlights why dynamic values are preferable.

Static example (what to avoid)

```hcl theme={null}
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}

resource "aws_vpc" "example" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "hardcoded-vpc"
  }
}

resource "github_repository" "example" {
  name        = "my-static-repo"
  description = "A static name"
  visibility  = "public"
}

resource "github_team" "example" {
  name        = "hardcoded-team"
  description = "A team with a name"
}
```

Dynamic example using data sources, locals, variables, and interpolation

```hcl theme={null}
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

locals {
  instance_type = "t3.micro"
  env           = "production"
}

variable "app" {
  type    = string
  default = "xyz"
}

resource "aws_instance" "example" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = local.instance_type

  tags = {
    Name = "${var.app}-${local.env}-server"
  }
}

resource "aws_vpc" "example" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "vpc-${local.env}-${data.aws_region.current.name}-${var.network}"
  }
}
```

What’s happening in the dynamic example:

* The AMI is discovered via `data.aws_ami.ubuntu.id` instead of a literal AMI ID.
* A `local` holds the instance type so the value is defined once and reused.
* Tags and names are assembled with interpolation to include variables, locals, and data source values.

Interpolation (string templating)
Interpolation in Terraform uses the `${...}` syntax to evaluate expressions and embed results into strings.

Simple interpolation examples

```hcl theme={null}
variable "name" {
  type    = string
  default = "Bryan"
}
