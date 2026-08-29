# aws_instance.project will be created
+ resource "aws_instance" "project" {
    + ami           = "ami-0edab43b6fa892279"
    + instance_type = "t2.micro"
    + tags = {
        + "Name" = "ProjectA"
    }
}
```

To configure Project B, create a new workspace:

```bash theme={null}
$ terraform workspace new ProjectB
Created and switched to workspace "ProjectB"!

You're now on a new, empty workspace. Workspaces isolate their state, so if you run "terraform plan" Terraform will not see any existing state for this configuration.
```

When you run `terraform plan` in the ProjectB workspace, Terraform will use the AMI and tag assigned to Project B:

```bash theme={null}
$ terraform plan
Terraform will perform the following actions:

# aws_instance.project will be created
+ resource "aws_instance" "project" {
    + ami           = "ami-0c2f25c1f66a1ff4d"
    + instance_type = "t2.micro"
    + tags = {
        + "Name" = "ProjectB"
    }
}
```

To switch between workspaces, use the `terraform workspace select` command. For example, to switch back to ProjectA:

```bash theme={null}
$ terraform workspace select ProjectA
Switched to workspace "ProjectA".
```

When you run `terraform apply` in each workspace, Terraform stores each workspace's state in a separate subdirectory within the `terraform.tfstate.d` directory. For example:

```bash theme={null}
$ ls
main.tf  provider.tf  terraform.tfstate  variables.tf

$ tree terraform.tfstate.d/
terraform.tfstate.d/
├── ProjectA
│   └── terraform.tfstate
└── ProjectB
    └── terraform.tfstate

2 directories, 2 files
```

> **lightbulb** Using workspaces ensures that changes in one environment (e.g., ProjectA) do not impact another (e.g., ProjectB), thanks to the isolated state files.

That concludes this lesson on Terraform workspaces. Practice managing multiple environments using a single configuration directory to maximize efficiency and maintainability in your Terraform projects.

For further insights:

* [Terraform Documentation](https://www.terraform.io/docs)
* [AWS EC2 Instance Guide](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [Amazon S3 Overview](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/cdfc2941-5d41-4d7c-b701-cddd299de4c5/lesson/d805227d-3dc1-4d85-80d5-968bbfa12958)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/cdfc2941-5d41-4d7c-b701-cddd299de4c5/lesson/efca6a14-da3b-4bb6-a9fe-1d83d47101f7)


# Using Modules from the Registry

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Modules/Using-Modules-from-the-Registry/page

Learn to leverage Terraform Registry modules for simplified infrastructure provisioning and reusable configurations across projects.

In this lesson, you will learn how to leverage modules from the Terraform Registry to simplify your infrastructure provisioning. Terraform modules allow you to reuse and share configurations across projects, streamlining your workflow. While a local module resides on the same machine as Terraform, modules from the Registry offer the added benefit of being easily shared with the community.

## Local Module Example

A typical local module configuration might look like this:

```hcl theme={null}
module "dev-webserver" {
  source = "../aws-instance/"
  key    = "webserver"
}
```

## Terraform Registry Modules

Modules in the Terraform Registry are organized by the provider they support. They come in two categories:

* **Verified Modules:** Tested and maintained by HashiCorp, these modules are marked with a blue tick. For example, AWS security group modules often appear as verified solutions.
* **Community Modules:** Created by users, these modules are not validated by HashiCorp.

When searching for a module—say, to create AWS security groups—you might encounter multiple options. Each module in the Registry includes detailed information such as the publisher, available versions, and helpful usage instructions with examples.

## Referencing a Security Group Module

The following example demonstrates how to reference an AWS security group module from the Terraform Registry:

```hcl theme={null}
module "security-group" {
  source  = "terraform-aws-modules/security-group"
  version = "3.16.0"
  # insert the 2 required variables here
}
```

## Creating an SSH Security Group

A common use case is to create a security group that permits inbound SSH access. The SSH module requires three mandatory inputs:

* The name of the security group.
* The VPC in which it will be created.
* A list of ingress CIDR blocks allowed access for SSH.

Below is the configuration for the SSH sub-module:

```hcl theme={null}
module "security-group_ssh" {
  source              = "terraform-aws-modules/security-group/aws/modules/ssh"
  version             = "3.16.0"
  vpc_id              = "vpc-7d8d215"
  ingress_cidr_blocks = [ "10.10.0.0/16" ]
  name                = "ssh-access"
}
```

> **lightbulb** It is highly recommended to specify the module version to ensure consistency and prevent unintended updates. Omitting the version may cause Terraform to download the latest module revision, potentially introducing changes that could disrupt your environment.

## Initializing and Downloading Modules

To use a module from the Terraform Registry, start by initializing your Terraform configuration. If the provider plugins are already downloaded, you can simply run the command to fetch the module:

```bash theme={null}
$ terraform get
Downloading terraform-aws-modules/security-group/aws 3.16.0 for security-group_ssh...
- security-group_ssh in .terraform/modules/security-group_ssh/modules/ssh
```

Following the download, create the security group by executing:

1. `terraform plan` – to view the changes.
2. `terraform apply` – to apply the configuration.

## Conclusion

This lesson covered how to utilize modules from the Terraform Registry, from local module examples to referencing public modules for building robust and reusable infrastructure components. Practice working with these modules to reinforce your learning and improve your Terraform configurations.

For more detailed information, explore these resources:

* [Terraform Documentation](https://www.terraform.io/docs/)
* [Terraform Registry](https://registry.terraform.io/)
* [AWS Provider Documentation](https://docs.aws.amazon.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e6838c6b-3208-4396-a744-34b0ed2cd292/lesson/1ad02134-86c6-4f1d-b8c9-ab4a53e08cf5)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e6838c6b-3208-4396-a744-34b0ed2cd292/lesson/ec3d12ee-9a6a-42b6-a26b-1e8bcd88ce3f)
