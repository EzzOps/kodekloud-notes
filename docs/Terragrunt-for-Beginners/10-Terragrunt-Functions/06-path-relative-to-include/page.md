# terragrunt.hcl (initial version)
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws/?version=5.8.1"

  extra_arguments "custom_vars" {
    commands  = ["plan"]
    arguments = ["-var-file=../common.tfvars"]
  }
}
```

Your `common.tfvars`:

```hcl theme={null}
name = "KodeKloud-VPC"
cidr = "10.100.0.0/24"
```

When you run:

```bash theme={null}
cd workspace/vpc
terragrunt plan
```

You’ll see:

```bash theme={null}
Error: Failed to read variables file
  Given variables file ../common.tfvars does not exist.
```

Terragrunt is running Terraform inside its cache folder, so the relative path breaks.

### Applying `get_terragrunt_dir()`

Update your `terragrunt.hcl` to compute the correct path:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//"

  extra_arguments "custom_vars" {
    commands  = ["plan"]
    arguments = ["-var-file=${get_terragrunt_dir()}/../common.tfvars"]
  }
}
```

Now `terragrunt plan` correctly locates `common.tfvars`, and the VPC module receives the desired inputs. After a successful apply, your AWS VPC resource might look like this:

```hcl theme={null}
resource "aws_vpc" "this" {
  cidr_block = "10.100.0.0/24"
  tags = {
    Name = "KodeKloud-VPC"
  }
  # ...other attributes omitted for brevity
}
```

***

## Summary

Using `get_terragrunt_dir()` ensures that:

* File references are always relative to your `terragrunt.hcl` location
* Your configurations remain portable and modular
* Terragrunt’s cache directory behavior won’t break your paths

Leverage this function to build more robust and maintainable infrastructure code.

***

## Links and References

* [Terragrunt Official Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)
* [Working with Extra Arguments in Terragrunt](https://terragrunt.gruntwork.io/docs/features/extra-arguments/)

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/5775621f-5504-4da8-835d-661cda37a852/lesson/f36ff662-3b0c-44cd-8d3e-a8ae00a04013)


# path relative to include

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Functions/path-relative-to-include/page

This lesson explores Terragrunt’s `path_relative_to_include` function for calculating relative paths in configuration files.

In this lesson, we’ll dive into Terragrunt’s `path_relative_to_include` function. This built-in helper calculates the relative path between the current `.hcl` file and the file specified in its `include` block. Use it to:

* Organize and modularize your configuration files
* Construct dynamic file paths
* Segregate remote state keys per module

## Why Use `path_relative_to_include`?

| Benefit                  | Description                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| Dynamic Configuration    | Adjust resource definitions based on their position in the directory hierarchy. |
| Modular Structures       | Build reusable, adaptable modules that survive folder reorganizations.          |
| Remote State Segregation | Generate unique backend keys for each module, keeping your state isolated.      |

> **lightbulb** When used without arguments, `path_relative_to_include()` returns the relative path from the current folder to where `common.hcl` (or your included file) lives.

## Typical Terragrunt Setup

Imagine you have a shared `common.hcl` in a parent directory and multiple child modules that include it. You can tag each module’s remote state with its relative path:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

locals {
  common_vars = read_terragrunt_config(
    find_in_parent_folders("common.hcl")
  )
}

include "common" {
  path = find_in_parent_folders("common.hcl")
}

inputs = {
  name = "${local.common_vars.inputs.project}-${local.common_vars.inputs.environment}"
  tags = {
    Path = path_relative_to_include()
  }
}
```

Here’s what happens when you run `terragrunt plan`:

```plaintext theme={null}
Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + azs                                  = []
  + cgw_arns                             = []
  + cgw_ids                              = []
  + database_nat_gateway_route_ids       = []
  + database_route_table_association_ids = []
  + database_route_table_ids             = []
  + database_subnet_arns                 = []
  + database_subnets                     = []
  + database_subnets_cidr_blocks         = []
  + default_network_acl_id               = (known after apply)
  + default_route_table_id               = (known after apply)
  + default_security_group_id            = (known after apply)
  + elasticache_route_table_association_ids = []
  + elasticache_route_table_ids         = []
  + elasticache_subnet_arns             = []
  + elasticache_subnets                 = []
```

Notice how the `Path` tag reflects this module’s folder relative to `common.hcl`. By doing so, each module’s Terraform state is stored under a unique key in your remote backend, enhancing clarity and maintainability.

## Further Reading

* [Terragrunt Documentation on `path_relative_to_include`](https://terragrunt.gruntwork.io/docs/reference/functions/#path_relative_to_include)
* [Terragrunt Remote State Configuration](https://terragrunt.gruntwork.io/docs/features/keep-your-backend-configuration-dry/)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/5775621f-5504-4da8-835d-661cda37a852/lesson/02079dcb-1fa9-4d49-aaf4-187525423e7c)
