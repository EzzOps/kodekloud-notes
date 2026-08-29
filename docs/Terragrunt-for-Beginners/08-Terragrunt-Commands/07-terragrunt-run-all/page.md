# aws_vpc.this[0] will be created
resource "aws_vpc" "this" {
  + arn                                  = (known after apply)
  + cidr_block                           = "10.0.0.0/16"
  + default_network_acl_id               = (known after apply)
  + default_route_table_id               = (known after apply)
  + default_security_group_id            = (known after apply)
  + dhcp_options_id                      = (known after apply)
  + enable_dns_hostnames                 = true
  + enable_dns_support                   = true
  + enable_network_address_usage_metrics = (known after apply)
  + id                                   = (known after apply)
  + instance_tenancy                     = "default"
  + owner_id                             = (known after apply)
  + tags                                 = {
      + "Name" = "KodeKloud-VPC"
    }
  + tags_all                             = {
      + "Name" = "KodeKloud-VPC"
    }
}

Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + azs                                  = []
  + cgw_arns                             = []
  + cgw_ids                              = []
  + database_nat_gateway_route_ids       = []
  + database_route_table_association_ids = []
  + database_route_table_ids             = []
  + database_subnet_arns                 = []
  + database_subnets_cidr_blocks         = []
```

Always inspect the plan output to confirm that resource additions and deletions match your expectations before proceeding to `terragrunt apply`.

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform CLI: plan](https://www.terraform.io/cli/plan)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws)

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/e42961fc-4288-4cc2-8db8-3882b884c0b1/lesson/570bbde7-cba7-4868-ad01-2c24e82e6e7f)


# terragrunt run all

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Commands/terragrunt-run-all/page

The command enables bulk Terraform operations across all project modules, automating workflows and ensuring consistency in large-scale deployments.

The `terragrunt run-all` command lets you perform bulk Terraform operations—such as `init`, `plan`, `apply`, and `destroy`—across every module in your project. By automating multi-module workflows, it reduces manual effort and ensures consistency in large-scale Terraform deployments.

![The image is an infographic about "Terragrunt run-all," highlighting its support for Terragrunt commands like init, plan, apply, and destroy, and its capability for bulk execution.](https://kodekloud.com/kk-media/image/upload/v1752884336/notes-assets/images/Terragrunt-for-Beginners-terragrunt-run-all/terragrunt-run-all-infographic-commands.jpg)

## Key Features

| Feature               | Description                                              |
| --------------------- | -------------------------------------------------------- |
| Bulk Commands         | Run `init`, `plan`, `apply`, or `destroy` on all modules |
| Workflow Streamlining | Standardize operations and eliminate repetitive steps    |
| Parallel Execution    | Execute commands concurrently to speed up large projects |

![The image illustrates the concept of "Terragrunt run-all" with colorful puzzle piece icons and emphasizes workflow streamlining by reducing manual command execution.](https://kodekloud.com/kk-media/image/upload/v1752884337/notes-assets/images/Terragrunt-for-Beginners-terragrunt-run-all/terragrunt-run-all-puzzle-workflow.jpg)

![The image illustrates the concept of "Terragrunt run-all" with icons representing parallel execution of tasks. It features colorful puzzle piece icons and a label indicating "Parallel Execution."](https://kodekloud.com/kk-media/image/upload/v1752884338/notes-assets/images/Terragrunt-for-Beginners-terragrunt-run-all/terragrunt-run-all-parallel-execution.jpg)

## Common Use Cases

* Apply changes across all modules with a single command
* Destroy resources uniformly in every module
* Automate routine Terraform tasks in CI/CD pipelines

![The image is a presentation slide about "Terragrunt run-all," highlighting benefits such as performing the same operations across modules and saving time and effort. It includes icons and a "Use Cases" button.](https://kodekloud.com/kk-media/image/upload/v1752884340/notes-assets/images/Terragrunt-for-Beginners-terragrunt-run-all/terragrunt-run-all-benefits-presentation.jpg)

## Best Practices

* Review your Terraform plans before applying changes.
* Use targeted execution (`--terragrunt-include-dir` / `--terragrunt-exclude-dir`) to scope large projects.
* Remember that `run-all apply` and `run-all destroy` add `--auto-approve` by default.

> **triangle-alert** When running `terragrunt run-all apply` or `terragrunt run-all destroy`, Terragrunt automatically appends `--auto-approve`. Ensure you understand the full impact before executing these commands.

![The image is an infographic about "Terragrunt run-all," highlighting its use for consistent and automated operations and its ability to reduce human error, with a "Best Practices" label.](https://kodekloud.com/kk-media/image/upload/v1752884341/notes-assets/images/Terragrunt-for-Beginners-terragrunt-run-all/terragrunt-run-all-infographic-best-practices.jpg)

***

## Example: Applying Multiple VPC Modules

Assume you have two directories—`vpc-1` and `vpc-2`—each containing a `terragrunt.hcl` that sources the AWS VPC module:

```hcl theme={null}
