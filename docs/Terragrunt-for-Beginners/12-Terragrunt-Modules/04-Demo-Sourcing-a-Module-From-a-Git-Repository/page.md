# terragrunt.hcl
terraform {
  source = "./modules/s3"
}

inputs = {
  bucket_name = "your-unique-s3-bucket-name-123"
}
```

<Callout icon="lightbulb">
  Terragrunt lets you keep your Terraform code DRY by abstracting common configurations.\
  Learn more in the [Terragrunt documentation](https://terragrunt.gruntwork.io/).
</Callout>

***

## 4. Initialize, Plan, and Apply

Run these commands from the directory containing `terragrunt.hcl`:

```bash theme={null}
terragrunt init
terragrunt plan
```

Sample plan output:

```plaintext theme={null}
Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + bucket_arn  = (known after apply)
  + bucket_name = "your-unique-s3-bucket-name-123"
```

Apply your changes:

```bash theme={null}
terragrunt apply
```

Confirm with `yes` when prompted:

```plaintext theme={null}
aws_s3_bucket.this: Creating...
aws_s3_bucket.this: Creation complete after 3s [id=your-unique-s3-bucket-name-123]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
bucket_arn  = "arn:aws:s3:::your-unique-s3-bucket-name-123"
bucket_name = "your-unique-s3-bucket-name-123"
```

***

## 5. Verifying the S3 Bucket

Use the AWS CLI to confirm that your bucket exists:

```bash theme={null}
aws s3 ls
```

Example:

```plaintext theme={null}
2024-06-23 15:41:52 your-unique-s3-bucket-name-123
```

***

## Next Steps

* Store your module in a Git repository (e.g., GitHub or GitLab).
* Pin module versions in `terragrunt.hcl` using a Git URL and tag.
* Expand the module with features like versioning, lifecycle rules, or encryption.

***

## Links and References

* [Terraform Modules](https://www.terraform.io/language/modules)
* [AWS S3 Bucket Resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
* [Terragrunt Documentation](https://terragrunt.gruntwork.io/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/4d4cda50-7d42-4622-b0d4-fa6e6ce0a16d/lesson/89935bb9-9e3b-4621-9c7d-7fe0a1f32f16" />
</CardGroup>


# Demo Sourcing a Module From a Git Repository

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Demo-Sourcing-a-Module-From-a-Git-Repository/page

This tutorial teaches how to source a Terraform module from GitHub using Terragrunt for consistent deployments.

In this tutorial, you’ll learn how to source the official [Terraform AWS S3 Bucket Module](https://github.com/terraform-aws-modules/terraform-aws-s3-bucket) directly from GitHub using Terragrunt. By pinning to a specific release tag, you can guarantee consistent deployments across environments.

## Prerequisites

* Terragrunt installed (v0.XX+).
* [AWS CLI](https://aws.amazon.com/cli/) configured with valid credentials.
* Git installed and reachable from your environment.

## terragrunt.hcl

Create or update your `terragrunt.hcl` file:

```hcl theme={null}
terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-s3-bucket.git?ref=v4.1.2"
}

inputs = {
  # This module expects "bucket" (not "bucket_name")
  bucket = "terragrunt-demo-bucket"
}
```

<Callout icon="lightbulb">
  Appending `?ref=v4.1.2` to the Git URL locks the module to version 4.1.2. This prevents unexpected changes due to upstream updates.
</Callout>

## Module Inputs

| Input  | Description            | Required | Default |
| ------ | ---------------------- | -------- | ------- |
| bucket | Name of the S3 bucket. | yes      | —       |

## Apply the Configuration

Run the following command in the directory containing your `terragrunt.hcl`:

```bash theme={null}
terragrunt apply
```

You should see a plan similar to:

```HCL theme={null}
  # module.s3_bucket.aws_s3_bucket.this will be created
  + resource "aws_s3_bucket" "this" {
      + bucket = "terragrunt-demo-bucket"
      …
    }

  # module.s3_bucket.aws_s3_bucket_public_access_block.this will be created
  + resource "aws_s3_bucket_public_access_block" "this" {
      …
    }
```

Confirm by typing `yes` and wait for provisioning to complete.

## Verify the Bucket

After Terragrunt finishes, list your S3 buckets:

```bash theme={null}
aws s3 ls
```

Expected output:

```text theme={null}
2023-06-01 12:34:56 terragrunt-demo-bucket
```

You should see `terragrunt-demo-bucket` in the list.

## Sourcing from Private Repositories

If your module resides in a private Git repo, update the `source` URL to point to your private repository (HTTPS or SSH) and ensure authentication is set up:

* **SSH**: Configure SSH keys and add them to your Git provider.
* **HTTPS**: Use `git-credential-helper` or environment variables for credentials.

<Callout icon="triangle-alert">
  Do not store credentials in version control. Use secure credential helpers or environment variables to manage access.
</Callout>

## Links and References

| Resource                 | URL                                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Terraform AWS S3 Module  | [https://github.com/terraform-aws-modules/terraform-aws-s3-bucket](https://github.com/terraform-aws-modules/terraform-aws-s3-bucket) |
| Terragrunt Documentation | [https://terragrunt.gruntwork.io/docs/](https://terragrunt.gruntwork.io/docs/)                                                       |
| Terraform Documentation  | [https://www.terraform.io/docs/](https://www.terraform.io/docs/)                                                                     |
| AWS CLI                  | [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)                                                                           |

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/4d4cda50-7d42-4622-b0d4-fa6e6ce0a16d/lesson/8a3a7434-c751-49b0-8ff8-4d5e3f342d3c" />
</CardGroup>
