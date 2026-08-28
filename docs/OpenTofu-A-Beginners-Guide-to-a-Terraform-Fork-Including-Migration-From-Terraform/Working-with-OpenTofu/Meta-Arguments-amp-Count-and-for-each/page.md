# Meta Arguments amp Count and for each

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/Meta-Arguments-amp-Count-and-for-each/page

This guide explains provisioning multiple EC2 instances using `count` and `for_each` meta-arguments in OpenTofu, highlighting their differences in indexing and lifecycle behavior.

In this guide, you’ll learn how to provision multiple EC2 instances with the `count` and `for_each` meta-arguments in OpenTofu. Both approaches let you duplicate a single resource block, but differ in indexing and lifecycle behavior.

| Meta-Argument | Key Characteristic                     | Best Use Case                                |
| ------------- | -------------------------------------- | -------------------------------------------- |
| count         | Integer-based, zero-indexed            | Create a fixed number of identical resources |
| for\_each     | Key-based, uses a set or map of values | Stable addressing of dynamic or named items  |

***

## 1. Using `count`

The `count` meta-argument accepts an integer and creates that many instances of a resource.

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = 3
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}
```

Run:

```bash theme={null}
tofu apply
```

Then verify:

```bash theme={null}
tofu state list
