# Switched to workspace "us-payroll".
```

***

## 4. Understand Workspace State Location

OpenTofu stores each workspace’s state under `terraform.tfstate.d/<workspace-name>`. For example:

```text theme={null}
terraform.tfstate.d/india-payroll/terraform.tfstate
```

> **triangle-alert** Do not manually edit files in the `terraform.tfstate.d/` directory—always use OpenTofu commands to manage state.

***

## 5. Review the Configuration Files

Your `project-sapphire` folder should include:

* **variables.tf**
* **provider.tf**

### variables.tf

```hcl theme={null}
variable "region" {
  type = map(string)
  default = {
    "us-payroll"    = "us-east-1"
    "uk-payroll"    = "eu-west-2"
    "india-payroll" = "ap-south-1"
  }
}

variable "ami" {
  type = map(string)
  default = {
    "us-payroll"    = "ami-24e140119877avm"
    "uk-payroll"    = "ami-351e40119877avm"
    "india-payroll" = "ami-55140119877avm"
  }
}
```

Quiz:

* **Type of `region`?** A `map(string)`.
* **`region["india-payroll"]` default?** `"ap-south-1"`.
* **`ami["india-payroll"]` default?** `"ami-55140119877avm"`.

### provider.tf

```hcl theme={null}
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.38.0"
    }
  }
}

provider "aws" {
  region                      = lookup(var.region, terraform.workspace)
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    ec2      = "http://aws:4566"
    dynamodb = "http://aws:4566"
    s3       = "http://aws:4566"
  }
}
```

***

## 6. Update `main.tf` to Invoke the Module

Add a module block in `main.tf` that points to your shared payroll application:

```hcl theme={null}
module "payroll_app" {
  source     = "/root/opentofu-projects/modules/payroll-app"
  app_region = lookup(var.region, terraform.workspace)
  ami        = lookup(var.ami, terraform.workspace)
}
```

***

## 7. Initialize OpenTofu

Download providers and modules:

```bash theme={null}
tofu init
```

***

## 8. Apply Configuration Across All Workspaces

Deploy the payroll app in each region:

1. US Payroll
   ```bash theme={null}
   tofu workspace select us-payroll
   tofu apply
   # Enter "yes" to confirm
   ```

2. UK Payroll
   ```bash theme={null}
   tofu workspace select uk-payroll
   tofu apply
   # Enter "yes" to confirm
   ```

3. India Payroll
   ```bash theme={null}
   tofu workspace select india-payroll
   tofu apply
   # Enter "yes" to confirm
   ```

***

### Workspace-State Mapping

| Workspace     | AWS Region | AMI ID              | State File Location                                 |
| ------------- | ---------- | ------------------- | --------------------------------------------------- |
| us-payroll    | us-east-1  | ami-24e140119877avm | terraform.tfstate.d/us-payroll/terraform.tfstate    |
| uk-payroll    | eu-west-2  | ami-351e40119877avm | terraform.tfstate.d/uk-payroll/terraform.tfstate    |
| india-payroll | ap-south-1 | ami-55140119877avm  | terraform.tfstate.d/india-payroll/terraform.tfstate |

***

## References

* [OpenTofu Documentation](https://github.com/opentofu/opentofu)
* [Terraform Workspaces](https://www.terraform.io/language/state/workspaces)
* [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/042e7b27-75d9-46fc-8f8c-7357d81923c1/lesson/0161ce1c-5d2a-477f-9d21-9f3056f9859a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/042e7b27-75d9-46fc-8f8c-7357d81923c1/lesson/9197d359-40fc-4167-993e-e951dff69ff9)


# Dynamic Blocks and Splat Expressions

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Functions-and-Conditional-Expressions/Dynamic-Blocks-and-Splat-Expressions/page

This guide explores streamlining Terraform configurations in OpenTofu using dynamic blocks and splat expressions for efficient resource management.

In this guide, we’ll explore how to streamline repetitive Terraform configurations in OpenTofu using **dynamic blocks** and **splat expressions**. You’ll learn to replace verbose nested blocks with a DRY, scalable approach, and extract attributes efficiently from generated resources.

## Looping with `count` and `for_each`

Traditionally, you can create multiple resources by using the `count` or `for_each` arguments:

```hcl theme={null}
resource "aws_instance" "backend" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = length(var.backend_servers)

  tags = {
    Name = var.backend_servers[count.index]
  }
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}

variable "backend_servers" {
  type    = list(string)
  default = ["server1", "server2"]
}
```

Here, two EC2 instances (`server1` and `server2`) are instantiated by leveraging `count`.

***

## Building a VPC, Subnet, and Security Group

Let’s set up:

1. A new VPC
2. A private subnet
3. A security group allowing SSH (port 22) and HTTP (port 8080)

A VPC provides an isolated network (`10.0.0.0/16`), and the subnet uses `10.0.2.0/24`. The security group acts as a virtual firewall.

![The image is a diagram of an Amazon VPC setup, showing a private subnet with two servers (server1 and server2) and a security group allowing inbound traffic on ports 8080 and 22.](https://kodekloud.com/kk-media/image/upload/v1752882867/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Dynamic-Blocks-and-Splat-Expressions/amazon-vpc-private-subnet-diagram.jpg)

First, declare the VPC and subnet:

```hcl theme={null}
resource "aws_vpc" "backend_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "backend-vpc"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.backend_vpc.id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "private-subnet"
  }
}
```

Next, define a security group with two hard-coded `ingress` blocks:

```hcl theme={null}
resource "aws_security_group" "backend_sg" {
  name   = "backend-sg"
  vpc_id = aws_vpc.backend_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

Adding more ports would require additional nested `ingress` blocks, quickly becoming repetitive.

***

## Simplifying with Dynamic Blocks

With a **dynamic block**, you can loop over a list of ports and generate as many `ingress` entries as needed.

Declare an input variable for ports:

```hcl theme={null}
variable "ingress_ports" {
  type    = list(number)
  default = [22, 8080]
}
```

Replace the static blocks with one dynamic block:

```hcl theme={null}
resource "aws_security_group" "backend_sg" {
  name   = "backend-sg"
  vpc_id = aws_vpc.backend_vpc.id

  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

> **lightbulb** You can rename the default iterator (`ingress`) to anything meaningful.\
  Example:

  ```hcl theme={null}
  dynamic "ingress" {
    iterator = port
    for_each = var.ingress_ports
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  ```

## Splat Expressions

After generating multiple ingress rules, you might want to output all `to_port` values at once. Use a splat expression:

```hcl theme={null}
output "to_ports" {
  value = aws_security_group.backend_sg.ingress[*].to_port
}
```

> **triangle-alert** Be aware that splat expressions return a list. If your security group has no `ingress` rules, you’ll get an empty list rather than a single value.

## Compare Approaches

| Approach          | Description                                | Pros                 |
| ----------------- | ------------------------------------------ | -------------------- |
| Static Blocks     | Individual `ingress` blocks for each port  | Simple for few ports |
| Dynamic Blocks    | One block looping over `var.ingress_ports` | DRY, maintainable    |
| Splat Expressions | Extracts list of attributes from resources | Concise outputs      |

***

## Apply and Inspect

Execute your plan:

```bash theme={null}
$ tofu apply --auto-approve
aws_vpc.backend_vpc: Creating...
aws_vpc.backend_vpc: Creation complete after 0s [id=vpc-593470c0]
aws_subnet.private_subnet: Creating...
aws_security_group.backend_sg: Creating...
aws_subnet.private_subnet: Creation complete after 1s [id=subnet-fdd6b762]
aws_security_group.backend_sg: Creation complete after 1s [id=sg-a5aa3b711157d4a2b]
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

Retrieve the generated ports:

```bash theme={null}
$ tofu output
to_ports = [
  22,
  8080,
]
```

By leveraging dynamic blocks and splat expressions, your OpenTofu configurations become more **expressive**, **concise**, and **easier to maintain**.

## References

* [OpenTofu Documentation](https://docs.opentofu.org/)
* [Terraform Dynamic Blocks](https://www.terraform.io/language/expressions/dynamic-blocks)
* [Terraform Splat Expressions](https://www.terraform.io/language/expressions/splat)

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/042e7b27-75d9-46fc-8f8c-7357d81923c1/lesson/aeb39e04-a7c3-4edd-970b-f65401dac59e)
