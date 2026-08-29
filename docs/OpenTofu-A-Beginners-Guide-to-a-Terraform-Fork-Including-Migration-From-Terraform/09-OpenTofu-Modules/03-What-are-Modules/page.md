# aws_instance.db will be created
+ resource "aws_instance" "db" {
    + tags = {
        + "Department" = "finance"
        + "Project"    = "cerberus"
    }
}

# aws_instance.web will be created
+ resource "aws_instance" "web" {
    + tags = {
        + "Department" = "finance"
        + "Project"    = "cerberus"
    }
}

Plan: 2 to add, 0 to change, 0 to destroy.
```

***

## Advanced Example: Combining Variables and Resource Attributes

Locals aren’t limited to static maps—they can also concatenate variables, resource attributes, and more. For instance, to generate a globally unique S3 bucket name:

```hcl theme={null}
variable "project" {
  description = "Name of the project"
  type        = string
  default     = "cerberus"
}

resource "random_string" "random_suffix" {
  length  = 6
  special = false
  upper   = false
}

locals {
  bucket_prefix = "${var.project}-${random_string.random_suffix.id}-bucket"
}

resource "aws_s3_bucket" "finance_bucket" {
  acl    = "private"
  bucket = local.bucket_prefix
}
```

When you run `tofu apply`, you’ll see:

```console theme={null}
$ tofu apply --auto-approve
random_string.random_suffix: Creating...
random_string.random_suffix: Creation complete after 0s [id=dhiabk]
aws_s3_bucket.finance_bucket: Creating...
aws_s3_bucket.finance_bucket: Creation complete after 0s [id=cerberus-dhiabk-bucket]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

> **lightbulb** HCL supports both legacy interpolation (`"${...}"`) and the newer direct syntax (`var.project`). Both work in locals, but be consistent across your codebase.

***

## When to Use Local Values

| Use Case                                    | Local Value Example          |
| ------------------------------------------- | ---------------------------- |
| Share common configuration across resources | `local.common_tags`          |
| Build dynamic names or identifiers          | `local.bucket_prefix`        |
| Simplify complex expressions                | Intermediate computed values |

***

## Further Reading and References

* [OpenTofu Locals Documentation](https://developer.hashicorp.com/openTofu/docs/configuration/locals)
* [Terraform Best Practices](https://developer.hashicorp.com/terraform/best-practices)
* [Random Provider on Terraform Registry](https://registry.terraform.io/providers/hashicorp/random/latest)
* [AWS Provider on Terraform Registry](https://registry.terraform.io/providers/hashicorp/aws/latest)

That’s it for this lesson on local values! In the next lesson, we’ll explore modules and how they can further modularize your infrastructure code.

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/d4c286c6-b8ee-47b1-bea3-abcf408b00ed/lesson/f6ea91e0-bcaa-49fb-9878-b1c58476acaa)


# What are Modules

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Modules/What-are-Modules/page

This article explains modules in OpenTofu, detailing their structure, usage, and benefits for organizing infrastructure code.

A **module** in OpenTofu (a Terraform fork) is any directory that contains configuration files. When you run OpenTofu commands inside that directory, it becomes the **root module**, orchestrating resources defined within.

## Root Module Example

Suppose your workspace looks like this:

```bash theme={null}
$ ls /root/opentofu-projects/aws-instance
main.tf  variables.tf
```

– **main.tf**

```hcl theme={null}
