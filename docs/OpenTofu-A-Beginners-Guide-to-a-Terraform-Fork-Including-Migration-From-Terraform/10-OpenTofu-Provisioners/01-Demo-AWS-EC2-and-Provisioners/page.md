# /root/opentofu-projects/aws-instance/main.tf
resource "aws_instance" "webserver" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = var.key
}
```

– **variables.tf**

```hcl theme={null}
# /root/opentofu-projects/aws-instance/variables.tf
variable "ami" {
  type        = string
  default     = "ami-0edab43b6fa892279"
  description = "Ubuntu AMI ID in the ca-central-1 region"
}
```

> **lightbulb** Running `tofu init`, `tofu plan`, or `tofu apply` inside `aws-instance` treats it as the **root module**.

## Calling Child Modules

To avoid duplicating infrastructure code, package a directory as a **child module** and invoke it:

```bash theme={null}
$ mkdir -p /root/opentofu-projects/development
```

Create a `main.tf` in `development`:

```hcl theme={null}
# /root/opentofu-projects/development/main.tf
module "dev-webserver" {
  source = "../aws-instance"
}
```

* `module "dev-webserver"` assigns a logical name.
* `source = "../aws-instance"` points to the child module’s path.

Now `development` is the **root module**, calling the `../aws-instance` **child module**.

***

## Building a Reusable Payroll App Module

FlexIT Consulting needs the same payroll stack in multiple regions. The architecture uses:

* One EC2 instance (custom AMI)
* One DynamoDB table
* One S3 bucket

All resources live in the default VPC:

![The image is a diagram of a simplified AWS architecture for FlexIT Consulting's payroll software, showing components like an AWS instance, S3 bucket, and DynamoDB table within a default VPC. It highlights aspects such as no IAM role considerations and default VPC and subnet usage.](https://kodekloud.com/kk-media/image/upload/v1752882878/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-What-are-Modules/aws-architecture-flexit-payroll-diagram.jpg)

### Define the Module

Organize reusable code under `modules/payroll-app`:

```bash theme={null}
$ mkdir -p /root/opentofu-projects/modules/payroll-app
$ ls /root/opentofu-projects/modules/payroll-app
app_server.tf  dynamodb_table.tf  s3_bucket.tf  variables.tf
```

#### app\_server.tf

```hcl theme={null}
# modules/payroll-app/app_server.tf
resource "aws_instance" "app_server" {
  ami           = var.ami
  instance_type = "t2.medium"
  tags = {
    Name = "${var.app_region}-app-server"
  }
  depends_on = [
    aws_dynamodb_table.payroll_db,
    aws_s3_bucket.payroll_data
  ]
}
```

#### s3\_bucket.tf

```hcl theme={null}
# modules/payroll-app/s3_bucket.tf
resource "aws_s3_bucket" "payroll_data" {
  bucket = "${var.app_region}-${var.bucket}"
}
```

#### dynamodb\_table.tf

```hcl theme={null}
# modules/payroll-app/dynamodb_table.tf
resource "aws_dynamodb_table" "payroll_db" {
  name         = "user_data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "EmployeeID"

  attribute {
    name = "EmployeeID"
    type = "S"
  }
}
```

#### variables.tf

```hcl theme={null}
# modules/payroll-app/variables.tf
variable "app_region" {
  type = string
}

variable "bucket" {
  type    = string
  default = "flexit-payroll-alpha-22001c"
}

variable "ami" {
  type = string
}
```

* **Hardcoded**: instance type, DynamoDB table name, and hash key.
* **Configurable**: AMI, region, bucket via variables.

***

## Deploy in US East (us-east-1)

Create a root module for the US deployment:

```bash theme={null}
$ mkdir /root/opentofu-projects/us-payroll-app
```

– **provider.tf**

```hcl theme={null}
# /root/opentofu-projects/us-payroll-app/provider.tf
provider "aws" {
  region = "us-east-1"
}
```

– **main.tf**

```hcl theme={null}
# /root/opentofu-projects/us-payroll-app/main.tf
module "us_payroll" {
  source     = "../modules/payroll-app"
  app_region = "us-east-1"
  ami        = "ami-24e140119877avm"
}
```

Initialize and apply:

```bash theme={null}
$ cd /root/opentofu-projects/us-payroll-app
$ tofu init
```

```bash theme={null}
$ tofu apply
```

You’ll see:

```HCL theme={null}
module.us_payroll.aws_dynamodb_table.payroll_db will be created
module.us_payroll.aws_instance.app_server     will be created
module.us_payroll.aws_s3_bucket.payroll_data will be created
```

> **lightbulb** The S3 bucket name combines the region prefix with the default bucket variable.

***

## Deploy in London (eu-west-2)

Repeat for the UK region:

```bash theme={null}
$ mkdir /root/opentofu-projects/uk-payroll-app
```

– **provider.tf**

```hcl theme={null}
# /root/opentofu-projects/uk-payroll-app/provider.tf
provider "aws" {
  region = "eu-west-2"
}
```

– **main.tf**

```hcl theme={null}
# /root/opentofu-projects/uk-payroll-app/main.tf
module "uk_payroll" {
  source     = "../modules/payroll-app"
  app_region = "eu-west-2"
  ami        = "ami-35e140119877avm"
}
```

```bash theme={null}
$ cd /root/opentofu-projects/uk-payroll-app
$ tofu init && tofu apply
```

Resources provisioned under:

```HCL theme={null}
module.uk_payroll.aws_instance.app_server
module.uk_payroll.aws_s3_bucket.payroll_data
module.uk_payroll.aws_dynamodb_table.payroll_db
```

***

OpenTofu can source community or verified modules from the registry, just like Terraform. For example, to provision a security group:

![The image shows a search interface from the OpenTofu Registry, displaying results for "security-group" modules, including details about a Terraform module for creating EC2-VPC security groups on AWS.](https://kodekloud.com/kk-media/image/upload/v1752882880/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-What-are-Modules/opentofu-registry-security-group-module.jpg)

```hcl theme={null}
module "security_group_ssh" {
  source              = "terraform-aws-modules/security-group/aws/modules/ssh"
  version             = "3.16.0"
  vpc_id              = "vpc-7d8d215"
  ingress_cidr_blocks = ["10.10.0.0/16"]
  name                = "ssh-access"
}
```

> **triangle-alert** Always pin the `version` to prevent unexpected module changes. Use `tofu get` or `tofu init` to fetch registry modules.

***

![The image is an infographic titled "OpenTofu Module" highlighting the benefits of using modules, including simpler configuration files, lower risk, and reusability.](https://kodekloud.com/kk-media/image/upload/v1752882880/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-What-are-Modules/opentofu-module-benefits-infographic.jpg)

| Benefit         | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| Simpler configs | Keep root modules concise for easier maintenance                 |
| Reusability     | Share the same module across multiple projects                   |
| Stability       | Enforce default settings and reduce configuration drift          |
| Reduced errors  | Leverage tested modules from your team or the community registry |

***

## Links and References

* [OpenTofu Documentation](https://github.com/opentofu)
* [Terraform Module Registry](https://registry.terraform.io/)
* [AWS Provider for Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest)

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/d4c286c6-b8ee-47b1-bea3-abcf408b00ed/lesson/9d09c96a-4d2d-4f7c-81a1-5d46b790dd99)


# Demo AWS EC2 and Provisioners

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Provisioners/Demo-AWS-EC2-and-Provisioners/page

This tutorial covers provisioning an AWS EC2 instance using OpenTofu, including configuration, SSH key management, user data scripts, and automation with provisioners.

Welcome to this hands-on tutorial on provisioning an AWS EC2 instance using OpenTofu (a community-driven fork of Terraform). You’ll learn how to:

* Create and configure an EC2 instance
* Manage SSH keys
* Apply user data scripts
* Use provisioners for automation
* Allocate and associate an Elastic IP
* Understand Terraform’s dependency graph

This guide assumes you have AWS credentials configured and the OpenTofu CLI installed.

## Prerequisites

* OpenTofu CLI installed (`tofu version`)
* AWS CLI configured (`aws configure`)
* An SSH key pair (we’ll generate one in step 2)

***

## 1. Provision a Simple EC2 Instance

1. Change to your project directory and open `main.tf`:

   ```bash theme={null}
   cd /root/OpenTofu/projects/project-cerberus/
   touch main.tf
   ```

2. Define the EC2 resource and variables:

   ```hcl theme={null}
   resource "aws_instance" "cerberus" {
     ami           = var.ami
     instance_type = var.instance_type
   }

   variable "ami" {
     default = "ami-06178c7f087598769c"
   }

   variable "region" {
     default = "eu-west-2"
   }

   variable "instance_type" {
     default = "m5.large"
   }
   ```

3. Initialize and apply:

   ```bash theme={null}
   tofu init
   tofu apply
   ```

   Example output:

   ```plaintext theme={null}
   Plan: 1 to add, 0 to change, 0 to destroy.
   aws_instance.cerberus: Creating...
   aws_instance.cerberus: Creation complete after 12s [id=i-3f85199c9711d152f]
   Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
   ```

Inspect your instance attributes:

```bash theme={null}
tofu show
```

***

## 2. Create an SSH Key Pair

Generate an SSH key pair on your local machine:

```bash theme={null}
ssh-keygen -t rsa -b 4096 -f ~/.ssh/cerberus -N ""
```

Then add this to `main.tf`:

```hcl theme={null}
resource "aws_key_pair" "cerberus_key" {
  key_name   = "cerberus"
  public_key = file("~/.ssh/cerberus.pub")
}
```

Apply the change:

```bash theme={null}
tofu init
tofu apply
```

You should see:

```plaintext theme={null}
aws_key_pair.cerberus_key: Creating...
aws_key_pair.cerberus_key: Creation complete after 0s [id=cerberus]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

***

## 3. Attach the Key to the EC2 Instance

Update the `aws_instance` block to reference the key:

```hcl theme={null}
resource "aws_instance" "cerberus" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = "cerberus"
}
```

Re-apply:

```bash theme={null}
tofu apply
```

```plaintext theme={null}
aws_instance.cerberus: Modifying... [id=i-3f85199c9711d152f]
aws_instance.cerberus: Destruction complete after 10s
aws_instance.cerberus: Creation complete after 11s [id=i-2386285c5705afa5071]
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

***

## 4. Install Nginx via User Data

Provision your instance to install Nginx at launch:

1. Create `install-nginx.sh`:

   ```bash theme={null}
   #!/bin/bash
   apt-get update
   apt-get install -y nginx
   ```

2. Reference it in your EC2 resource:

   ```hcl theme={null}
   resource "aws_instance" "cerberus" {
     ami           = var.ami
     instance_type = var.instance_type
     key_name      = "cerberus"
     user_data     = file("./install-nginx.sh")
   }
   ```

> **lightbulb** User data scripts run only on the first instance launch. Future `tofu apply` runs will not re-execute `user_data`.

Attempt to apply:

```bash theme={null}
tofu apply
```

You’ll see no changes if the instance already exists.

***

## 5. Provisioners and Connection Blocks

Terraform supports three built-in provisioners. Only **local-exec** does **not** require a `connection` block.

| Provisioner | Connection Required? | Use Case                                       |
| ----------- | -------------------- | ---------------------------------------------- |
| local-exec  | No                   | Run commands on the machine executing OpenTofu |
| remote-exec | Yes                  | Execute SSH/WinRM commands on the remote host  |
| file        | Yes                  | Upload/download files to/from the resource     |

Remember: provisioners must be nested inside the resource block they target.

***

## 6. Retrieve the Public IPv4 Address

After creating your EC2 instance, run:

```bash theme={null}
tofu show aws_instance.cerberus
```

Look for the `public_ip` attribute (for example, `54.214.169.15`).

***

## 7. Reserve and Associate an Elastic IP

An Elastic IP (EIP) is a static public IPv4 address. Add this resource:

```hcl theme={null}
resource "aws_eip" "eip" {
  vpc      = true
  instance = aws_instance.cerberus.id
}
```

To save the public DNS to a file, use a `local-exec` provisioner:

```hcl theme={null}
resource "aws_eip" "eip" {
  vpc      = true
  instance = aws_instance.cerberus.id

  provisioner "local-exec" {
    command = <<EOT
echo "${self.public_dns}" > /root/serverless_publicDNS.txt
EOT
  }
}
```

> **lightbulb** This block allocates and associates an Elastic IP, then writes the instance’s public DNS to `/root/serverless_publicDNS.txt`.

![The image shows a split-screen view with a task description on the left about creating an Elastic IP in Terraform, and a code editor on the right displaying a Terraform configuration file with AWS resources.](https://kodekloud.com/kk-media/image/upload/v1752882882/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-AWS-EC2-and-Provisioners/elastic-ip-terraform-configuration-editor.jpg)

Apply your changes:

```bash theme={null}
tofu apply
```

Inspect the EIP:

```bash theme={null}
tofu show aws_eip.eip
```

Note the `public_ip` (e.g., `52.47.169.195`).

***

## 8. Understanding Dependency Direction

Because `aws_eip.eip` references `aws_instance.cerberus.id`, Terraform automatically creates the EC2 instance before allocating the EIP. There’s no reverse dependency.

> **lightbulb** Terraform’s graph engine infers resource creation order by scanning references. No explicit `depends_on` is needed here.

![The image shows a split screen with a multiple-choice question on the left and a code editor on the right displaying Terraform configuration files. The terminal at the bottom shows the output of a Terraform apply command.](https://kodekloud.com/kk-media/image/upload/v1752882884/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-AWS-EC2-and-Provisioners/terraform-multiple-choice-code-editor.jpg)

***

That completes this lab. Thank you for following along!

## Links and References

* [OpenTofu CLI Repository](https://github.com/opentofu/opentofu)
* [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)
* [Terraform Provisioners](https://www.terraform.io/docs/language/resources/provisioners/syntax.html)
* [SSH Key Management](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/98011198-b847-4ee1-a7bd-7593bfe5576c/lesson/f86348a1-e5b4-41e1-9265-34c3fa2dc375)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/98011198-b847-4ee1-a7bd-7593bfe5576c/lesson/67b0b9cc-3146-41a2-8b4f-7a0762841f04)
