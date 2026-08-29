# Demo Sourcing a Module From the Terraform Registry

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Demo-Sourcing-a-Module-From-the-Terraform-Registry/page

This guide demonstrates sourcing an S3 bucket module from the Terraform Registry using Terragrunt for simplified version management.

In this guide, we’ll demonstrate how to source the same S3 bucket module from the Terraform Registry using Terragrunt. Instead of pulling the module from GitHub, we switch to the `tfr:///` prefix and pin a specific version. This approach simplifies version management and leverages the official [Terraform Registry](https://registry.terraform.io/) distribution.

## Why Use the Terraform Registry?

| Source Type        | Prefix                        | Example Address                                                             |
| ------------------ | ----------------------------- | --------------------------------------------------------------------------- |
| GitHub             | `git::https://github.com/...` | `git::https://github.com/terraform-aws-modules/terraform-aws-s3-bucket.git` |
| Terraform Registry | `tfr:///`                     | `tfr:///terraform-aws-modules/s3-bucket/aws?version=4.1.2`                  |

<Callout icon="lightbulb">
  Pinning module versions (e.g. `?version=4.1.2`) ensures reproducible builds and prevents unexpected changes when upstream modules are updated.
</Callout>

## terragrunt.hcl Configuration

Create or update your `terragrunt.hcl` file with the registry source and input variables:

```hcl theme={null}
