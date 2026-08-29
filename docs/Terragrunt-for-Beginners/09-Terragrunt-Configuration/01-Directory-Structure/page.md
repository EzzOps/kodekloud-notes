# vpc-1/terragrunt.hcl
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

inputs = {
  name = "KodeKloud-VPC-1"
}
```

```hcl theme={null}
# vpc-2/terragrunt.hcl
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

inputs = {
  name = "KodeKloud-VPC-2"
}
```

From the parent directory, list modules:

```bash theme={null}
$ ls
vpc-1  vpc-2
```

1. Initialize all modules
   ```bash theme={null}
   $ terragrunt run-all init
   ```
   Downloads providers, creates cache folders, and writes lock files in each module.

2. Plan and apply changes
   ```bash theme={null}
   $ terragrunt run-all apply
   ```
   Prompts once, then creates VPCs in both modules:
   ```bash theme={null}
   aws_vpc.this[0]: Creating...
   aws_vpc.this[0]: Creation complete after 13s [id=vpc-00a01fbbed0f8a50]
   aws_vpc.this[1]: Creating...
   aws_vpc.this[1]: Creation complete after 12s [id=vpc-033ed68948da3c48]
   ```

3. Destroy all resources
   ```bash theme={null}
   $ terragrunt run-all destroy
   ```
   Confirm with `yes` to tear down everything:
   ```bash theme={null}
   aws_vpc.this[0]: Destroying... [id=vpc-00a01fbbed0f8a50]
   aws_vpc.this[0]: Destruction complete after 1s
   aws_vpc.this[1]: Destroying... [id=vpc-033ed68948da3c48]
   aws_vpc.this[1]: Destruction complete after 1s
   ```

## References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/e42961fc-4288-4cc2-8db8-3882b884c0b1/lesson/d273febc-2f10-4542-9f8e-b40385b9e299" />
</CardGroup>


# Directory Structure

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Configuration/Directory-Structure/page

A well-organized directory layout simplifies management of Terraform configurations with Terragrunt, promotes reuse, and makes environment-specific customizations straightforward.

A well-organized directory layout simplifies management of Terraform configurations with Terragrunt, promotes reuse, and makes environment-specific customizations straightforward.

## Key Components

| Component             | Purpose                                                  | Location                              |
| --------------------- | -------------------------------------------------------- | ------------------------------------- |
| Root `terragrunt.hcl` | Defines global settings (remote state, providers, hooks) | `/terragrunt.hcl`                     |
| **Modules**           | Reusable Terraform logic (resources, variables)          | `/modules/<module-name>/`             |
| **Environments**      | Environment-specific configurations                      | `/envs/<environment>/`                |
| Shared Variables      | Centralizes common variable values per environment       | `/envs/<environment>/common-vars.hcl` |

## Example Directory Tree

```bash theme={null}
.
├── terragrunt.hcl              # Global Terragrunt configuration
├── modules                     # Reusable Terraform modules
│   ├── app
│   │   ├── main.tf
│   │   └── variables.tf
│   └── mysql
│       ├── main.tf
│       └── variables.tf
└── envs                        # Environment-specific configurations
    ├── dev
    │   ├── account.hcl         # Dev account ID, region, etc.
    │   ├── common-vars.hcl     # Shared dev variables
    │   ├── app
    │   │   └── terragrunt.hcl  # Inherits root, adds app settings
    │   └── mysql
    │       └── terragrunt.hcl  # Inherits root, adds MySQL settings
    └── prod
        ├── account.hcl         # Prod account ID, region, etc.
        ├── common-vars.hcl     # Shared prod variables
        ├── app
        │   └── terragrunt.hcl
        └── mysql
            └── terragrunt.hcl
```

## How It Works

1. **Global Settings**\
   The root `terragrunt.hcl` provides defaults for all modules and environments:
   * Remote state backend configuration
   * Shared providers
   * Pre/post hooks for automation

<Callout icon="lightbulb">
  Define secure and centralized remote state backends in your root file to maintain state consistency across teams.
</Callout>

2. **Environment Overrides**\
   Each environment directory (`envs/dev`, `envs/prod`) contains:
   * `account.hcl` for environment-specific parameters (account IDs, AWS region, etc.)
   * `common-vars.hcl` to share variable values among all components

3. **Component-Specific Configuration**\
   Inside `envs/<environment>/<component>/terragrunt.hcl` you:
   * Include both the root configuration and the environment’s `account.hcl`
   * Reference the corresponding module from `modules/<component>`
   * Override or supplement module inputs as needed

4. **Shared Variables**\
   Use `common-vars.hcl` to avoid repetition:
   ```hcl theme={null}
   inputs = {
     project_name = "example"
     tags = {
       owner = "team-infra"
     }
   }
   ```

<Callout icon="triangle-alert">
  Avoid duplicating variables across component configs. Centralize values in `common-vars.hcl` to prevent drift.
</Callout>

## Benefits

* **Modularity**: Break infrastructure into reusable modules.
* **Clarity**: Isolate environment-specific settings from shared defaults.
* **Scalability**: Easily add new environments or components without refactoring existing code.

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform Modules](https://www.terraform.io/language/modules)
* [Terraform Remote State](https://www.terraform.io/language/state/remote)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/52cf8076-030b-430e-9a8b-273697ad3399/lesson/99e9124e-f13b-4227-a093-422b9447bfb9" />
</CardGroup>
