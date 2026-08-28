# Demo Output Variables

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Demo-Output-Variables/page

Learn to configure, apply, and manage output variables in OpenTofu using the random provider through a hands-on lab experience.

In this hands-on lab, you’ll learn how to configure, apply, and manage output variables in OpenTofu using the `random` provider. By the end, you’ll be able to expose resource attributes and query them on demand.

## 1. Setup and Resource Configuration

1. Change into the sample project directory:
   ```bash theme={null}
   cd /root/OpenTofu-projects/data
   ```

2. Examine the HCL files defining nine resources with the *random* provider:

   ```hcl theme={null}
   # random_integer resources
   resource "random_integer" "order1" {
     min = 1
     max = 99999
   }

   resource "random_integer" "order2" {
     min = 1
     max = 222222
   }

   # random_uuid resources
   resource "random_uuid" "id1" {}
   resource "random_uuid" "id2" {}
   resource "random_uuid" "id3" {}
   resource "random_uuid" "id4" {}
   resource "random_uuid" "id5" {}
   resource "random_uuid" "id6" {}
   resource "random_uuid" "id7" {}
   ```

3. Open the accompanying `output.tf` to see how each resource is exposed as an output variable.

## 2. Initialize, Plan, and Apply

Initialize the working directory, preview the plan, and apply the configuration.

| Command      | Description                                          |
| ------------ | ---------------------------------------------------- |
| `tofu init`  | Download providers and initialize the working folder |
| `tofu plan`  | Generate and display the execution plan              |
| `tofu apply` | Apply changes to create resources                    |

```bash theme={null}
tofu init
tofu plan
tofu apply
