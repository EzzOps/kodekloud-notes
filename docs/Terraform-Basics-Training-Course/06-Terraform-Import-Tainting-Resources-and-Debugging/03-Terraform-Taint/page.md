# terraform import <resource_type>.<resource_name> <attribute>
$ terraform import aws_instance.webserver-2 i-026e13be10d5326f7
```

<Callout icon="triangle-alert">
  Before running the import command, ensure that the corresponding configuration exists. If the resource block isn't defined, Terraform will return an error.
</Callout>

If the resource configuration hasn’t been created, you might see an error like:

```plaintext theme={null}
Error: resource address "aws_instance.webserver-2" does not exist in the configuration.

Before importing this resource, please create its configuration in the root module. For example:
resource "aws_instance" "webserver-2" {
  # (resource arguments)
}
```

Terraform import only updates the state file and does not alter configuration files. Hence, ensure that you create an appropriate resource block beforehand.

### Step 1: Create an Empty Resource Block

Begin by defining an empty resource block in your configuration file:

```hcl theme={null}
resource "aws_instance" "webserver-2" {
  # (resource arguments)
}
```

### Step 2: Run the Import Command

After the empty block is defined, run the import command again. It should output something similar to:

```bash theme={null}
$ terraform import aws_instance.webserver-2 i-026e13be10d5326f7
aws_instance.webserver-2: Importing from ID "i-026e13be10d5326f7"...
aws_instance.webserver-2: Import prepared!
Prepared aws_instance for import
aws_instance.webserver-2: Refreshing state... [id=i-026e13be10d5326f7]

Import successful!
```

The command imports the resource into your Terraform state file, allowing Terraform to manage it moving forward.

### Step 3: Complete the Resource Configuration

Next, update the resource block with the necessary configurations. You can retrieve the required attribute values from the AWS Management Console or by inspecting the state file. For example, update the resource configuration as follows:

```hcl theme={null}
resource "aws_instance" "webserver-2" {
  ami                    = "ami-0edab43b6fa892279"
  instance_type          = "t2.micro"
  key_name               = "ws"
  vpc_security_group_ids = ["sg-8064fdeee"]
}
```

Running a Terraform plan now ensures that your configuration matches the imported infrastructure:

```bash theme={null}
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be persisted to local or remote state storage.

aws_instance.webserver-2: Refreshing state... [id=i-0d7c0088069819ff8]
-------------------------------------------------------------------------------
No changes. Infrastructure is up-to-date.
```

<Callout icon="lightbulb">
  This output confirms that Terraform has successfully imported the resource. Any future changes to the infrastructure can be managed by modifying this configuration and following the standard Terraform workflow: init, plan, and apply.
</Callout>

## Next Steps

Proceed to the hands-on labs to practice using the Terraform import command, and continue streamlining your infrastructure management by bringing all resources under Terraform control.

For further information, check out:

* [Terraform Documentation](https://www.terraform.io/docs/)
* [AWS Documentation](https://docs.aws.amazon.com/)
* [Terraform Import Guide](https://www.terraform.io/cli/import)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/29825b4d-c0d3-4732-a4e0-ec3a2988e2a3/lesson/bcdec6a0-4ac8-4995-8374-2e6af2aaf68a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/29825b4d-c0d3-4732-a4e0-ec3a2988e2a3/lesson/2ad6df8d-66d1-41e1-be9d-b78f0c1065e6" />
</CardGroup>


# Terraform Taint

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Import-Tainting-Resources-and-Debugging/Terraform-Taint/page

This article explains how to use Terraform’s taint and untaint commands for effective resource recreation management.

In this article, we explain how to use Terraform’s taint and untaint commands to manage resource recreation effectively. These commands are especially useful when a resource fails during creation or when manual changes occur that necessitate a fresh deployment.

## Overview

Terraform marks a resource as tainted when it encounters errors during creation, such as a failed provisioner command. A tainted resource is scheduled for replacement during the next apply. Conversely, you can use the untaint command to clear this status and prevent a replacement.

<Callout icon="lightbulb">
  Using taint and untaint commands allows for efficient control of resource lifecycle without a complete destroy and reapply cycle.
</Callout>

## Scenario: Tainted Resource due to Provisioner Failure

Consider a scenario where an AWS EC2 instance is provisioned using a local provisioner to store its public IP address in a file. If the provisioner command fails—perhaps because the file path is incorrect—the resource is marked as tainted, triggering its replacement on the next apply.

### Resource Definition Example

```hcl theme={null}
resource "aws_instance" "webserver-3" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  key_name      = "ws"

  provisioner "local-exec" {
    command = "echo ${aws_instance.webserver-3.public_ip} > /temp/pub_ip.txt"
  }
}
```

### Applying the Configuration

When executing the apply command, you might see output indicating that the provisioner has failed:

```bash theme={null}
$ terraform apply
Plan: 1 to add, 0 to change, 0 to destroy.

aws_instance.webserver: Creating...
aws_instance.webserver: Still creating... [10s elapsed]
aws_instance.webserver: Still creating... [20s elapsed]
aws_instance.webserver: Still creating... [30s elapsed]
aws_instance.webserver: Provisioning with 'local-exec'...
aws_instance.webserver (local-exec): Executing: ["cmd" "/C" "echo 35.183.14.192 > /temp/pub_ip.txt"]
aws_instance.webserver (local-exec): The system cannot find the path specified.

Error: Error running command 'echo 35.183.14.192 > /temp/pub_ip.txt': exit status 1. Output: The system
```

At this point, Terraform marks the "webserver" resource as tainted.

### Verifying the Tainted Resource

Running the terraform plan command confirms that the tainted resource is scheduled for replacement:

```bash theme={null}
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

aws_instance.webserver: Refreshing state... [id=i-0dba2d5dc22a9a904]
------------------------------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:
