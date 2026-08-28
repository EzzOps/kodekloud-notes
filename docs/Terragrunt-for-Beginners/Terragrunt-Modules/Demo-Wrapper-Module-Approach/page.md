# terragrunt.hcl
terraform {
  source = "tfr:///terraform-aws-modules/s3-bucket/aws?version=4.1.2"
}

inputs = {
  bucket = "my-unique-bucket-name"
  acl    = "private"

  public_access_block = {
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }
}
```

The syntax breakdown:

* `tfr:///` — Registry prefix (two slashes for delimiter + one slash to start address).
* `namespace/module_name/provider` — Module path on the Terraform Registry.
* `?version=x.y.z` — Query parameter to lock the module version.

## Initialize and Apply with Terragrunt

Run the following commands to download the module and provision your S3 bucket:

```bash theme={null}
$ terragrunt init
[terragrunt]  INFO: Downloading module...
...

$ terragrunt apply --auto-approve
...
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

## Verify the S3 Bucket

Use the AWS CLI to confirm that your bucket exists:

```bash theme={null}
$ aws s3 ls
2023-08-15 12:34:56 my-unique-bucket-name
```

<Callout icon="triangle-alert">
  Bucket names must be globally unique. If you encounter an error about the bucket already existing, choose a different name.
</Callout>

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform Registry: S3 Bucket Module](https://registry.terraform.io/modules/terraform-aws-modules/s3-bucket/aws/latest)
* [AWS CLI S3 Commands](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/4d4cda50-7d42-4622-b0d4-fa6e6ce0a16d/lesson/10f295f9-2ab3-4c55-8c4a-2f26863db598" />
</CardGroup>


# Demo Wrapper Module Approach

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Demo-Wrapper-Module-Approach/page

This article explains how to create a wrapper module for the Terraform S3 bucket module to enforce naming conventions and configuration rules.

In this example, we'll create a **wrapper module** around the official Terraform S3 bucket community module. This lets you inherit all best practices while enforcing your own naming conventions and configuration rules.

## Why Use a Wrapper Module?

A wrapper module allows you to:

* Leverage community-tested code.
* Enforce company-specific policies (e.g., naming standards).
* Extend or override default settings without modifying upstream code.

| Module                              | Description                                                   | Key Inputs                     |
| ----------------------------------- | ------------------------------------------------------------- | ------------------------------ |
| terraform-aws-modules/s3-bucket/aws | Official S3 bucket module on the Terraform Registry           | `source`, `version`, `bucket`  |
| local wrapper module                | Wraps the community module to append a random suffix to names | `bucket_name`, `suffix_length` |

***

## 1. Define the Wrapper Module

In your local `modules/s3-bucket` directory, replace the direct resource blocks with a call to the community module:

```hcl theme={null}
terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }
  }
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.0.0"

  bucket = local.full_bucket_name
  acl    = "private"

  # …any other inputs you normally pass…
}
```

## 2. Add a Random Suffix

Generate a unique suffix automatically so that bucket names remain globally unique:

```hcl theme={null}
resource "random_string" "suffix" {
  length           = 8
  special          = false
  upper            = false
}

locals {
  full_bucket_name = "${var.bucket_name}-${random_string.suffix.result}"
}
```

<Callout icon="lightbulb">
  We set `special = false` and `upper = false` to keep the suffix alphanumeric and lowercase only.
</Callout>

## 3. Update Module Outputs

Since the wrapper no longer defines the bucket resource directly, forward the community module outputs:

```hcl theme={null}
output "bucket_id" {
  value = module.s3_bucket.bucket_id
}

output "bucket_arn" {
  value = module.s3_bucket.bucket_arn
}
```

## 4. Configure Terragrunt

In your Terragrunt live configuration, reference the local wrapper module. Notice we no longer supply a suffix manually:

```hcl theme={null}
terraform {
  source = "../modules/s3-bucket"
}

inputs = {
  bucket_name = "testing-bucket-for-terragrunt"
}
```

<Callout icon="triangle-alert">
  The final bucket name is not known until apply time since it depends on the random suffix.
</Callout>

## 5. Deploy with Terragrunt

Run:

```bash theme={null}
terragrunt init
terragrunt apply
```

Terragrunt will:

1. Download the S3 bucket community module.
2. Generate a random suffix.
3. Create the bucket with your base name plus suffix.
4. Apply default public-access-block settings from the module.

Confirm the bucket exists:

```bash theme={null}
aws s3 ls
