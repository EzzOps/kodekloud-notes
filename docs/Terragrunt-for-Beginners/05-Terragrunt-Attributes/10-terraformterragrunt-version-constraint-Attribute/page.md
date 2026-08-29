# terraformterragrunt version constraint Attribute

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Attributes/terraformterragrunt-version-constraint-Attribute/page

Learn to enforce Terraform and Terragrunt version constraints in your configuration to ensure consistency and avoid unexpected upgrades.

In this guide, you’ll learn how to enforce Terraform and Terragrunt version constraints directly within your Terragrunt configuration. By pinning approved versions of the binaries, you’ll avoid unexpected upgrades and ensure consistency across your infrastructure deployments.

![The image illustrates the benefits and considerations of using terraform\_version\_constraint and terragrunt\_version\_constraint attributes, highlighting version limitations and compatibility with setting constraints.](https://kodekloud.com/kk-media/image/upload/v1752884283/notes-assets/images/Terragrunt-for-Beginners-terraformterragrunt-version-constraint-Attribute/terraform-terragrunt-version-constraints-benefits.jpg)

## Why Version Constraints?

Use version constraints to:

* Guarantee compatibility with existing state and modules
* Prevent accidental upgrades during CI/CD runs
* Enforce organizational compliance on approved tool versions

> **lightbulb** Always review your infrastructure modules and provider versions before updating constraints to avoid breaking changes.

## Key Attributes

| Attribute                       | Purpose                                               | Example                |
| ------------------------------- | ----------------------------------------------------- | ---------------------- |
| terraform\_version\_constraint  | Locks the Terraform binary to a specific semver range | `= 1.8.4`              |
| terragrunt\_version\_constraint | Restricts the Terragrunt binary to a given range      | `> 0.58.0, <= 0.58.11` |

## Terraform Version Constraint Example

Below is a `terragrunt.hcl` snippet that requires Terraform `1.8.4`:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

inputs = {
  name = "KodeKloud-VPC"
  cidr = "10.100.0.0/16"
}

download_dir                 = "../.terragrunt-kodekloud"
prevent_destroy              = false
skip                         = false
iam_role                     = "arn:aws:iam::654654587009:role/terragrunt-role"
terraform_version_constraint = "= 1.8.4"
```

When a non-matching Terraform binary is detected, Terragrunt exits with an error:

```bash theme={null}
~/workspace/vpc > terragrunt plan
ERROR[0000] The currently installed version of Terraform (1.9.0) is not compatible with the version Terragrunt requires (= 1.8.4).
ERROR[0000] Unable to determine underlying exit code, so Terragrunt will exit with error code 1
```

To proceed, you can update or comment out the constraint to match your installed version:

```hcl theme={null}
