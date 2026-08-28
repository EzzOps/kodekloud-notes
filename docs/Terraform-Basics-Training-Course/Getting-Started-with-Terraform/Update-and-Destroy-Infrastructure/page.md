# Update and Destroy Infrastructure

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Getting-Started-with-Terraform/Update-and-Destroy-Infrastructure/page

This guide explains how to update and destroy infrastructure using Terraform, including changing resource configurations and executing destruction commands.

This guide will walk you through updating and destroying infrastructure using Terraform. In previous tutorials, we covered how to create a local file resource. Today, we will update its configuration and then completely destroy it.

## Updating the Resource

In this section, we update the local file resource by changing its file permissions from the default (0777) to a more secure permission (0700). This update restricts file access exclusively to the owner.

Below is the updated Terraform configuration:

```hcl theme={null}
resource "local_file" "pet" {
  filename        = "/root/pets.txt"
  content         = "We love pets!"
  file_permission = "0700"
}
```

Updating this configuration marks the current resource as needing replacement. When you run the Terraform plan, you will see that Terraform plans to replace the resource. The output indicates the replacement using the symbol "-/+" to show that Terraform will destroy the existing file and create a new one with the updated permissions.

Below is an example of the Terraform plan output:

```bash theme={null}
$ terraform plan
local_file.pet: Refreshing state...
[id=5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
   -/+ destroy and then create replacement

Terraform will perform the following actions:
