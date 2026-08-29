# main.tf
resource "aws_instance" "webserver" {
  # configuration here
}
```

```hcl theme={null}
# key_pair.tf
resource "aws_key_pair" "web" {
  # configuration here
}
```

```hcl theme={null}
# dynamodb_table.tf
resource "aws_dynamodb_table" "state-locking" {
  # configuration here
}
```

```hcl theme={null}
# security_group.tf
resource "aws_security_group" "ssh-access" {
  # configuration here
}
```

```hcl theme={null}
# ec2_instance.tf
resource "aws_instance" "webserver-2" {
  # configuration here
}
```

```hcl theme={null}
# s3_bucket.tf
resource "aws_s3_bucket" "terraform-state" {
  # configuration here
}
```

While breaking configurations into separate files can improve organization, it does not fully solve two common challenges:

* Increasing complexity and code duplication within the configuration directory.
* The risk of unintended changes affecting resources in different parts of the configuration.

Additionally, sharing parts of the configuration with teammates involves copying and pasting code, which can introduce errors.

Consider the following directory listing for a typical Terraform project:

```bash theme={null}
$ ls
provider.tf
id_rsa
id_rsa.pub
main.tf
pub_ip.txt
terraform.tfstate.backup
terraform.tfstate
iam_roles.tf
iam_users.tf
security_groups.tf
variables.tf
outputs.tf
s3_buckets.tf
dynamo_db.tf
local.tf
```

<Callout icon="lightbulb">
  Using modules in Terraform allows you to manage complexity, reduce code duplication, and enhance reusability across projects and environments.
</Callout>

## What Is a Terraform Module?

A Terraform module is any directory that contains a set of `.tf` files. Essentially, every Terraform configuration directory is a module. For example, consider a configuration directory named `aws-instance` located under `/root/terraform-projects`. This directory contains the Terraform files required to create a simple EC2 instance in AWS. Since it has valid Terraform configuration files, it qualifies as a module.

Here is the directory listing for the `aws-instance` module:

```bash theme={null}
$ ls /root/terraform-projects/aws-instance
main.tf
variables.tf
```

The contents of `main.tf` might look like this:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = var.key
}
```

And the corresponding `variables.tf` defines the variables:

```hcl theme={null}
variable "ami" {
  type        = string
  default     = "ami-0edab43b6fa892279"
  description = "Ubuntu AMI ID in the ca-central-1 region"
}
```

When you run Terraform commands from within the `aws-instance` directory, it is considered the root module.

## Reusing Modules for Different Environments

Now, imagine you want to reuse the `aws-instance` module to create a new development web server instance without duplicating code. Follow these steps to create a development environment:

1. Create a new directory named `development` under the `terraform-projects` directory:

   ```bash theme={null}
   $ mkdir /root/terraform-projects/development
   ```

2. Inside the `development` directory, create a configuration file (for example, `main.tf`) that references the `aws-instance` module:

   ```hcl theme={null}
   module "dev-webserver" {
     source = "../aws-instance"
   }
   ```

In this setup, the `development` directory serves as the root module (because you run Terraform commands from here), while the `aws-instance` directory is referenced as a child module.

Let’s review the module block again:

```bash theme={null}
$ mkdir /root/terraform-projects/development
```

```hcl theme={null}
module "dev-webserver" {
  source = "../aws-instance"
}
```

The `module` keyword is followed by a logical name, in this case, `dev-webserver`. Within the block, the required argument is `source`, which specifies the relative or absolute path to the child module containing the Terraform configuration for the EC2 instance. Here, we use a relative path `"../aws-instance"`, pointing to the corresponding directory next to our development directory.

This modular approach effectively addresses earlier challenges by reducing code duplication, simplifying updates, and boosting reusability. It encapsulates specific infrastructure logic in a module that can be reused across different environments or projects.

<Callout icon="lightbulb">
  Modules not only help in organizing your Terraform configurations but also promote best practices by isolating infrastructure components. This makes your configurations easier to manage and share.
</Callout>

That concludes this article. In the next section, we will dive deeper into creating custom modules and harnessing their full potential with Terraform.

Learn more about related topics in the following links:

* [Terraform Modules](https://www.terraform.io/language/modules)
* [Terraform Configuration Language](https://www.terraform.io/language)

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e6838c6b-3208-4396-a744-34b0ed2cd292/lesson/e5a998ed-cd36-48db-81a4-95b1235ebb7f" />
</CardGroup>


# AWS EC2 with Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Provisioners/AWS-EC2-with-Terraform/page

Learn to deploy an AWS EC2 instance running Ubuntu using Terraform, covering configuration, SSH access, and security group setup.

In this lesson, you'll learn how to deploy an AWS EC2 instance running Ubuntu using Terraform. This guide covers instance configuration, provisioning with a startup script, setting up key-based SSH access, and configuring a security group for secure SSH connections.

## Deploying an EC2 Instance with Terraform

We begin by defining an AWS instance resource in Terraform. The configuration includes two mandatory arguments for our instance resource (named "webserver"):

1. **AMI ID:** We use the AMI for an Ubuntu instance in the US West 1 region.
2. **Instance Type:** We select a `t2.micro` instance, a low-spec option with one CPU and 1 GB of RAM.

Optionally, tags are added to identify the instance, including a name ("webserver") and a description ("An NGINX WebServer on Ubuntu"). A Bash shell script is provided via the `user_data` argument using the here-doc syntax. This script updates the package list, installs NGINX, enables it, and starts the service when the instance launches.

After configuring Terraform, run the following commands to preview and apply your changes:

```bash theme={null}
terraform plan
terraform apply
```

Below is a sample output after running `terraform apply`:

```bash theme={null}
$ terraform apply
