# terragrunt.hcl
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

inputs = {
  name = "KodeKloud-VPC"
}
```

Initialize and validate in the same folder:

```bash theme={null}
$ terragrunt init
Initializing the backend...
Initializing provider plugins...
- Reusing previous version of hashicorp/aws from the dependency lock file
- Using previously-installed hashicorp/aws v5.51.1

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure. All Terraform commands should now work.

If you ever set or change modules or backend configuration for Terraform, rerun this command to reinitialize your working directory. If you forget, other commands will detect it and remind you to do so if necessary.
```

```bash theme={null}
$ terragrunt validate
Success! The configuration is valid.
```

That concludes our overview of `terragrunt init` and `terragrunt validate`. By initializing early and validating frequently, you ensure reliable, maintainable infrastructure as code.

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/e42961fc-4288-4cc2-8db8-3882b884c0b1/lesson/2a6db1e8-f513-4eff-adf0-a077efb3b815)


# terragrunt plan

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Commands/terragrunt-plan/page

Generates and reviews execution plans for Terraform infrastructure changes, enhancing visibility and efficiency across configurations.

`terragrunt plan` produces a detailed execution plan that shows exactly which resources Terraform will create, update, or destroy. Reviewing this plan before applying changes helps you:

* Validate the intended modifications
* Catch configuration errors early
* Ensure alignment with stakeholder requirements

Terragrunt enhances Terraform’s native `plan` command by recursively applying it across your entire configuration hierarchy. This provides a unified, end-to-end view of changes across all modules.

> **lightbulb** Terragrunt delegates to [`terraform plan`](https://www.terraform.io/cli/plan) under the hood, orchestrating plans across multiple modules and directories.

![The image illustrates a Terragrunt plan process, showing how it generates an execution plan and applies it across a configuration hierarchy, with integration with Terraform.](https://kodekloud.com/kk-media/image/upload/v1752884333/notes-assets/images/Terragrunt-for-Beginners-terragrunt-plan/terragrunt-plan-process-terraform-diagram.jpg)

## Key Features of Terragrunt Plan

| Feature               | Description                                             | Benefit                                         |
| --------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| Hierarchical Planning | Executes `terraform plan` across all Terragrunt modules | Consistent visibility across environments       |
| Parallel Execution    | Plans multiple modules concurrently                     | Significant reduction in planning time          |
| Execution Summaries   | Aggregates and summarizes results from each module      | Quick, consolidated view of all pending changes |

### Parallel Planning Across Modules

In a modular project structure, `terragrunt plan` can run in parallel, speeding up the planning phase by generating multiple execution plans simultaneously.

![The image illustrates a "Terragrunt plan" with a central icon connected to two puzzle piece icons, representing parallel execution.](https://kodekloud.com/kk-media/image/upload/v1752884334/notes-assets/images/Terragrunt-for-Beginners-terragrunt-plan/terragrunt-plan-parallel-execution-diagram.jpg)

## Best Practices for `terragrunt plan`

* Always **review** the complete execution plan before applying changes.
* **Seek approval** from relevant stakeholders to prevent unintended infrastructure modifications.
* Use version control to track and audit plan outputs.

![The image is a slide titled "Terragrunt plan" with icons and text for "Review plan" and "Seek approval," along with a "Best Practices" button.](https://kodekloud.com/kk-media/image/upload/v1752884334/notes-assets/images/Terragrunt-for-Beginners-terragrunt-plan/terragrunt-plan-review-approval-best-practices.jpg)

> **triangle-alert** Never run `terragrunt apply` without first validating the execution plan. Unreviewed plans can lead to unexpected downtime or resource drift.

## Example: Planning an AWS VPC Module

Below is a sample Terragrunt configuration that references the official Terraform AWS VPC module. Adjust the `name` input to fit your naming conventions:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

inputs = {
  name = "KodeKloud-VPC"
}
```

To generate the plan, simply run:

```bash theme={null}
$ terragrunt plan
```

After Terragrunt prepares the consolidated configuration, you’ll see an execution plan similar to this:

```hcl theme={null}
