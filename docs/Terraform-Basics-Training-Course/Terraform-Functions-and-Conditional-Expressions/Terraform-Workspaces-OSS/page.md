# Terraform Workspaces OSS

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Functions-and-Conditional-Expressions/Terraform-Workspaces-OSS/page

This lesson explores using Terraform workspaces to manage multiple environments and streamline infrastructure as code projects.

In this lesson, we will explore how to use Terraform workspaces effectively to manage multiple environments and streamline your infrastructure as code (IaC) projects. By leveraging workspaces, you can eliminate repetitive tasks and maintain a single configuration directory while handling different projects or environments. This approach not only improves efficiency but also supports best practices for managing Terraform state files.

Terraform state is a critical component during IaC operations. Whether stored locally or on remote backends like [Amazon Simple Storage Service (Amazon S3)](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3), state files map your real-world infrastructure and help Terraform determine the necessary changes based on your configurations. In our examples, we've kept a one-to-one relationship between configuration directories and state files—one state file per configuration directory.

Consider a scenario where you need to create an [EC2 instance](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) in the AWS CA Central 1 region for an initial project, Project A. You can start with a simple configuration file located in a directory named Project A inside your Terraform Projects folder. For example:

```hcl theme={null}
resource "aws_instance" "projectA" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name = "ProjectA"
  }
}
```

Running `terraform apply` in the Project A directory creates the EC2 instance and generates its corresponding state file.

Now, suppose you want to replicate this setup for a new project (Project B) with a different AMI ID and server name. The straightforward approach might involve creating a new directory for Project B, copying Project A’s configuration, and updating the AMI ID and tags. An example configuration combining both projects might look like this:

```hcl theme={null}
resource "aws_instance" "projectA" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name = "ProjectA"
  }
}

resource "aws_instance" "projectB" {
  ami           = "ami-0c2f25c1f66a1ff4d"
  instance_type = "t2.micro"
  tags = {
    Name = "ProjectB"
  }
}
```

<Callout icon="lightbulb">
  Terraform workspaces allow you to use one configuration directory to manage multiple projects (or environments) without duplicating files. This improves maintainability and prevents configuration drift.
</Callout>

## Using Workspaces to Manage Environments

Terraform workspaces isolate state within the same configuration directory. To create a workspace for Project A, run:

```bash theme={null}
$ terraform workspace new ProjectA
Created and switched to workspace "ProjectA"!

You're now on a new, empty workspace. Workspaces isolate their state, so if you run "terraform plan" Terraform will not see any existing state for this configuration.
```

To list all available workspaces, use:

```bash theme={null}
$ terraform workspace list
default
* ProjectA
```

In the output, the default workspace is shown along with Project A (marked by an asterisk to indicate the active workspace).

## Parameterizing Your Configuration for Workspaces

To maintain a single configuration that dynamically adjusts for different projects in the `ca-central-1` region, create a `variables.tf` file. This file will define the region, instance type, and a map variable for AMI IDs—differentiating between Project A and Project B.

```hcl theme={null}
// variables.tf
variable "region" {
  default = "ca-central-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami" {
  type = map(string)
  default = {
    "ProjectA" = "ami-0edab43b6fa892279"
    "ProjectB" = "ami-0c2f25c1f66a1ff4d"
  }
}
```

Next, update your main configuration file (`main.tf`) to dynamically select values based on the current workspace. Here, the AMI is chosen using Terraform's `lookup` function combined with the `terraform.workspace` variable, and the instance tag is automatically set to the workspace name:

```hcl theme={null}
// main.tf
resource "aws_instance" "project" {
  ami           = lookup(var.ami, terraform.workspace)
  instance_type = var.instance_type
  tags = {
    Name = terraform.workspace
  }
}
```

You can verify that the configuration adapts to the current workspace using the Terraform console:

```bash theme={null}
$ terraform console
> terraform.workspace
ProjectA
> lookup(var.ami, terraform.workspace)
"ami-0edab43b6fa892279"
```

This confirms that when you are in the ProjectA workspace, Terraform selects the correct AMI ID.

## Switching Workspaces and Applying Configuration Changes

After setting up your configuration files, run `terraform plan` to preview changes for the current workspace (for example, ProjectA):

```bash theme={null}
$ terraform plan
Terraform will perform the following actions:
