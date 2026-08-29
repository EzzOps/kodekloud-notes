# Local Values

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Modules/Local-Values/page

Learn to use local values in OpenTofu to reduce duplication, enhance readability, and maintain a DRY configuration.

In this lesson, you’ll discover how to use **local values** (locals) in OpenTofu to eliminate duplication, improve readability, and keep your configuration DRY (Don’t Repeat Yourself).

## The Problem: Repeated Tag Definitions

Imagine you have two AWS EC2 instances—`web` and `db`—that share identical tags. Without locals, your HCL might look like this:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-06178cf087598769c"
  instance_type = "t2.medium"

  tags = {
    Department = "finance"
    Project    = "cerberus"
  }
}

resource "aws_instance" "db" {
  ami           = "ami-0567cf08759818b"
  instance_type = "m5.large"

  tags = {
    Department = "finance"
    Project    = "cerberus"
  }
}
```

> **lightbulb** Defining the same tags in multiple resources increases maintenance overhead. Locals allow you to declare shared values in one place.

## Step 1: Define a `locals` Block

Create a `locals` block to hold your common tag set:

```hcl theme={null}
locals {
  common_tags = {
    Department = "finance"
    Project    = "cerberus"
  }
}
```

## Step 2: Reference the Local Value

Use `local.common_tags` within each resource:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-06178cf087598769c"
  instance_type = "t2.medium"

  tags = local.common_tags
}

resource "aws_instance" "db" {
  ami           = "ami-0567cf08759818b"
  instance_type = "m5.large"

  tags = local.common_tags
}
```

## Step 3: Preview and Apply

Running `tofu plan` or `tofu apply` now shows both instances using the shared tags:

```console theme={null}
$ tofu apply
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

OpenTofu will perform the following actions:
