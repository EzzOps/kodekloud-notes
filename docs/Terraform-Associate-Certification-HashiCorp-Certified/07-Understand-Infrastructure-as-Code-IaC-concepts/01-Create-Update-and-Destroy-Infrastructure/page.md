# main.tf
resource "aws_instance" "cerberus" {
  ami           = var.ami
  instance_type = var.instance_type
}

# variables.tf
variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}
```

When you run the apply command:

```bash theme={null}
$ terraform apply
aws_instance.cerberus: Creating...
aws_instance.cerberus: Still creating... [10s elapsed]
aws_instance.cerberus: Creation complete after 10s [id=i-c791dc46a6639d4a7]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed
```

Terraform generates the state file, which contains all the details about the resources it created. For example, a snippet from the state file may look like this:

```json theme={null}
{
  "version": 4,
  "terraform_version": "0.13.3",
  "serial": 2,
  "lineage": "ccd95cf0-9966-549b-c7d1-1d2683b3119b",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "aws_instance",
      "name": "cerberus",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [
        {
          "schema_version": 1,
          "attributes": {
            "ami": "ami-06178cf087598769c",
            "arn": "arn:aws:ec2:eu-west-2:instance/i-1db6bfe81bd1e3ed7",
            "associate_public_ip_address": true,
            "availability_zone": "eu-west-2a",
            "capacity_reservation_specification": [],
            "cpu_core_count": null,
            "cpu_threads_per_core": null,
            "credit_specification": [],
            "disable_api_termination": false,
            "ebs_block_device": []
          }
        }
      ]
    }
  ]
}
```

This state file holds vital information such as resource IDs, provider details, and all resource attributes that Terraform uses to manage your infrastructure.

## Refreshing State with Terraform Plan

Before generating an execution plan, Terraform refreshes the state by comparing it with the actual state of your external resources. For example, the output of the plan command may look like:

```bash theme={null}
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be persisted to local or remote state storage.

aws_instance.cerberus: Refreshing state... [id=i-1db6bfe81bd1e3ed7]

---------------------------------------------------------------------------
No changes. Infrastructure is up-to-date.
```

If no differences are detected between your configuration and the real-world resources, Terraform indicates that no changes are needed. The apply command also performs a state refresh before proceeding with any updates.

In certain cases, you might want to skip refreshing the state. This can be done using the -refresh=false option:

```bash theme={null}
$ terraform apply -refresh=false
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

> **triangle-alert** Disabling the state refresh is generally not recommended as it may introduce inconsistencies if resources have been manually modified. Use this option with caution, especially in large environments.

## Tracking Configuration Changes with the State File

Terraform continuously monitors the state file to detect changes between your configurations and your provisioned resources. For example, if you change the instance type from m5.large to t3.micro, Terraform will detect the discrepancy during the next plan or apply.

### Original Variable Definitions

```hcl theme={null}
variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}
```

And a sample snippet from the terraform.tfstate file:

```json theme={null}
{
  "version": 4,
  "terraform_version": "0.13.3",
  "serial": 1,
  "lineage": "160ca48f-cd6a-bd64-fc1b-0e2e78c2bc10",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "aws_instance",
      "name": "cerberus",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [
        {
          "schema_version": 1,
          "attributes": {
            "ami": "ami-06178cf087598769c",
            "arn": "arn:aws:ec2:eu-west-2:instance/i-9d394a982f158e887",
            "instance_state": "running",
            "instance_type": "m5.large"
          }
        }
      ]
    }
  ]
}
```

### After Modifying the Configuration

```hcl theme={null}
variable "ami" {
  default = "ami-06178cf087598769"
}

variable "instance_type" {
  default = "t3.micro"
}
```

Terraform’s execution plan will mark the resource for recreation due to the change in instance type.

## Managing Resource Dependencies

Terraform also manages inter-resource dependencies using the state file. Consider a configuration where a web instance depends on a DB instance:

```hcl theme={null}
resource "aws_instance" "db" {
  ami           = var.ami
  instance_type = var.instance_type
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  depends_on    = [aws_instance.db]
}
```

The state file captures this dependency explicitly:

```json theme={null}
{
  "mode": "managed",
  "type": "aws_instance",
  "name": "web",
  "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
  "instances": [
    {
      "schema_version": 1,
      "attributes": {
        "ami": "ami-06178cf087598769c",
        "arn": "arn:aws:ec2:eu-west-2:instance/i-33b55018bd1a8d8ca",
        ...
      },
      ...
      "dependencies": [
        "aws_instance.db"
      ]
    }
  ]
}
```

During provisioning, Terraform creates the DB instance first, followed by the web instance. Conversely, when destroying resources, Terraform will remove the web instance before deleting the DB instance.

## Security and Remote State Management

> **lightbulb** The state file contains sensitive information, including configuration variables and resource attributes like SSH keys or initial passwords. Store your state file securely in remote backends (e.g., Amazon S3 or Terraform Cloud) and never commit it to version control systems.

For illustration, here is a snippet showing sensitive data in a state file:

```json theme={null}
{
  "mode": "managed",
  "type": "aws_instance",
  "name": "web",
  "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
  "instances": [
    {
      "schema_version": 1,
      "attributes": {
        "ami": "ami-0a634ae95e11c6f91",
        ...
        "primary_network_interface_id": "eni-0ccd57b1597e633e0",
        "private_dns": "ip-172-31-7-21.us-west-2.compute.internal",
        "private_ip": "172.31.7.21",
        "public_dns": "ec2-54-71-34-19.us-west-2.compute.amazonaws.com",
        "public_ip": "54.71.34.19",
        "root_block_device": [
          {
            "delete_on_termination": true,
            "device_name": "/dev/sda1",
            "encrypted": false,
            "iops": 100,
            "kms_key_id": "vol-070720a3636979c22"
          }
        ]
      }
    }
  ]
}
```

The configuration for managing dependencies remains the same:

```hcl theme={null}
resource "aws_instance" "db" {
  ami           = var.ami
  instance_type = var.instance_type
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  depends_on    = [aws_instance.db]
}
```

## Final Thoughts on Terraform State

Terraform state is designed exclusively for internal Terraform operations. It is essential to avoid manually editing the state file and to use Terraform commands to manage state. The information contained in the state file is crucial, and any changes to the configuration are reflected through Terraform's plan and apply process.

For example, here is a state file entry for a development EC2 instance:

```json theme={null}
{
  "mode": "managed",
  "type": "aws_instance",
  "name": "dev-ec2",
  "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
  "instances": [
    {
      "schema_version": 1,
      "attributes": {
        "ami": "ami-0a634ae95e11c6f91"
      },
      ...
      "primary_network_interface_id": "eni-0ccd57b1597e633e0",
      "private_dns": "ip-172-31-7-21.us-west-2.compute.internal",
      "private_ip": "172.31.7.21",
      "public_dns": "ec2-54-71-34-19.us-west-2.compute.amazonaws.com",
      "public_ip": "54.71.34.19",
      "root_block_device": [
        {
          "delete_on_termination": true,
          "device_name": "/dev/sda1",
          "encrypted": false,
          "iops": 100,
          ...
        }
      ]
    }
  ]
}
```

Remember, proper management of your Terraform state is key to maintaining the integrity and security of your infrastructure. For more detailed information and advanced state management practices, refer to the [Terraform documentation](https://www.terraform.io/docs).

## Summary

| Topic                      | Description                                                              | Example Command/Resource                         |
| -------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------ |
| Terraform State File       | Tracks infrastructure, resources, and metadata in a JSON format          | terraform.tfstate, terraform.tfstate.backup      |
| Refreshing Terraform State | Ensures state matches external resources before planning and applying    | terraform plan, terraform apply                  |
| Resource Dependencies      | Records dependencies to manage correct resource creation and deletion    | depends\_on attribute in resource configuration  |
| Secure State Management    | Store state in secure remote backends and avoid version control exposure | Using backends like Amazon S3 or Terraform Cloud |

By following these best practices, you can ensure that your Terraform operations are secure, reliable, and accurately reflect your intended infrastructure changes.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/4b6ab52b-4fbb-4a33-9dbc-0fb1c6900c7e/lesson/6a7d2a40-816d-4326-88fe-1431bd17082a)


# Create Update and Destroy Infrastructure

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Understand-Infrastructure-as-Code-IaC-concepts/Create-Update-and-Destroy-Infrastructure/page

This article explains how to update and destroy infrastructure resources using Terraform, including modifying configurations and executing commands.

In this article, we revisit how to update and destroy infrastructure resources managed with Terraform. Using a local file resource as an example, we will walk through updating a resource configuration, previewing the changes, and eventually destroying the resource if needed.

## Updating a Resource

To update a resource in Terraform, simply modify the configuration file. For example, you might add a new argument to update the file permissions of a resource to "0700":

```hcl theme={null}
resource "local_file" "pet" {
  filename        = "/root/pets.txt"
  content         = "We love pets!"
  file_permission = "0700"
}
```

After making your changes, run the Terraform plan to preview the execution changes:

```bash theme={null}
$ terraform plan
```

> **lightbulb** Running `terraform plan` is optional because executing `terraform apply` displays the same execution plan.

In the execution plan, Terraform uses the “-/+” symbol preceding the resource name to indicate that the resource will be destroyed and then recreated. A corresponding line in the output specifies that the change in file permissions is forcing this replacement. Since Terraform adheres to immutable infrastructure principles, any update that alters critical properties results in the resource being destroyed and re-created with the new settings.

Once you have reviewed the changes, apply the updates with:

```bash theme={null}
$ terraform apply
local_file.pet: Refreshing state...
[id=feafccdae259f25533749abfb90e27558256459]

-/+ destroy and then create replacement
...
Plan: 1 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.

Enter a value: yes
local_file.pet: Destroying...
[id=feafccdae259f25533749abfb90e27558256459]
local_file.pet: Destruction complete after 0s
local_file.pet: Creating...
local_file.pet: Creation complete after 0s
[id=feafccdae259f25533749abfb90e27558256459]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

## Destroying a Resource

To remove a resource completely from your infrastructure, use the `terraform destroy` command. This command generates an execution plan that shows a minus symbol next to each resource set for removal. Review the plan carefully before confirming the destruction.

```bash theme={null}
$ terraform destroy
local_file.pet: Refreshing state...
[id=5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # local_file.pet will be destroyed
  - resource "local_file" "pet" {
      - content             = "My favorite pet is a gold fish" -> null
      - directory_permission = "0777" -> null
      - file_permission     = "0700" -> null
      - filename            = "/root/pet.txt" -> null
      - id                  = "5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf" -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
local_file.pet: Destroying... [id=5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf]
local_file.pet: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.
```

You can bypass the confirmation prompt by including the `auto-approve` flag with the `terraform destroy` command. Use this option with caution, as it immediately removes all managed resources.

## Organizing Your Configuration Directory

Terraform treats any file with a `.tf` extension found in the current working directory as part of your configuration. This allows you to split your infrastructure configuration across multiple files for better organization. For instance, if your configuration is stored under `/root/terraform-local-file` with an initial file named `local.tf`, your directory might look like this:

```bash theme={null}
[terraform-local-file]$ ls /root/terraform-local-file
local.tf
```

The `local.tf` file may contain a resource like:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

You can add another configuration file, such as `cat.tf`, to define an additional resource:

```hcl theme={null}
resource "local_file" "cat" {
  filename = "/root/cat.txt"
  content  = "My favorite pet is Mr. Whiskers"
}
```

Both resources will be created when you run `terraform apply` for the first time.

A common best practice is to consolidate resource blocks into a single configuration file (often named `main.tf`) while separating variables and outputs into dedicated files such as `variables.tf` and `outputs.tf`. This modular structure improves manageability, especially as your project grows in complexity.

That concludes our guide on updating and destroying Terraform-managed infrastructure resources. To reinforce your understanding, consider taking the multiple-choice quiz and testing your knowledge of these Terraform operations.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/e27c7cfe-a9f1-4e56-b55b-f908bd92d21c/lesson/98cc4b71-d037-4127-8cef-9e1d463a0017)
