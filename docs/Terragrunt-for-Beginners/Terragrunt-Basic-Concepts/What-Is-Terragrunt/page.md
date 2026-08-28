# live/prod/app/terragrunt.hcl
include {
  path = find_in_parent_folders()
}

terraform {
  source = "git::ssh://git@github.com/your-org/terraform-modules.git//app?ref=v1.2.0"
}

inputs = {
  instance_count = 3
  instance_type  = "t3.medium"
}
```

<Frame>
  ![The image illustrates the "Don't Repeat Yourself" (DRY) principle, highlighting modular configuration, modular and reusable components, and reduced redundancy.](https://kodekloud.com/kk-media/image/upload/v1752884288/notes-assets/images/Terragrunt-for-Beginners-The-DRY-Principle/dry-principle-modular-configuration-diagram.jpg)
</Frame>

***

## 2. Variable Abstraction

Terragrunt centralizes variable definitions into shared files, preventing hard-coded values and scattered overrides. Reuse a single `variables.hcl` across modules:

```hcl theme={null}
# live/common/variables.hcl
locals {
  project_name = "MyApp"
  region       = "us-east-1"
  tags = {
    Environment = read_terragrunt_config(find_in_parent_folders("env.hcl")).inputs.environment
    Project     = local.project_name
  }
}
```

Then reference it:

```hcl theme={null}
# live/prod/app/terragrunt.hcl
dependency "vars" {
  config_path = find_in_parent_folders("common")
}

inputs = merge(dependency.vars.outputs, {
  service_port = 8080
})
```

<Frame>
  ![The image explains the "Don't Repeat Yourself" (DRY) principle, highlighting variable abstraction to avoid code repetition and enable centralized variable management.](https://kodekloud.com/kk-media/image/upload/v1752884288/notes-assets/images/Terragrunt-for-Beginners-The-DRY-Principle/dry-principle-variable-abstraction-diagram.jpg)
</Frame>

***

## 3. Hierarchical Configuration Inheritance

Terragrunt’s directory structure supports inheritance of configuration blocks. Define global settings at the root, then override or extend them in child folders:

```hcl theme={null}
# live/terragrunt.hcl (root)
remote_state {
  backend = "s3"
  config = {
    bucket = "my-tf-state"
    key    = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
  }
}
```

```hcl theme={null}
# live/prod/terragrunt.hcl
include {
  path = find_in_parent_folders()
}

inputs = {
  environment = "production"
}
```

<Frame>
  ![The image explains the "Don't Repeat Yourself" (DRY) principle, highlighting hierarchical configuration, enabling inheritance of settings, reducing duplicate configurations, and facilitating reuse of configuration settings.](https://kodekloud.com/kk-media/image/upload/v1752884289/notes-assets/images/Terragrunt-for-Beginners-The-DRY-Principle/dry-principle-configuration-inheritance-reuse.jpg)
</Frame>

***

## 4. Simplified Maintenance and Promotion

With DRY in place, updating modules or variables in one location propagates changes everywhere they’re used. This reduces configuration drift, lowers the risk of errors, and accelerates promotions across dev, staging, and prod.

| Benefit                     | Description                                               | Example Change                          |
| --------------------------- | --------------------------------------------------------- | --------------------------------------- |
| Single Source of Truth      | One module or file manages multiple environments          | Bump AMI ID in module repository        |
| Consistent Environment Tags | Central tags applied automatically across all deployments | Add `CostCenter` tag in `variables.hcl` |
| Rapid Rollout               | Apply changes once and run `terragrunt apply-all`         | Security patch update                   |
| Reduced Human Error         | Fewer manual edits across multiple HCL files              | Fix input typo in shared file           |

<Frame>
  ![The image illustrates the "Don't Repeat Yourself" (DRY) principle, highlighting benefits like simplified maintenance, more maintainable code, and uniform updates across code.](https://kodekloud.com/kk-media/image/upload/v1752884290/notes-assets/images/Terragrunt-for-Beginners-The-DRY-Principle/dry-principle-benefits-code-maintenance.jpg)
</Frame>

***

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/)
* [Terraform Registry](https://registry.terraform.io/)
* [Infrastructure as Code Best Practices](https://docs.microsoft.com/azure/devops/learn/what-is-infrastructure-as-code)
* [HCL Language Reference](https://github.com/hashicorp/hcl)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/9618155f-f613-4c7b-92c7-9be9ddfa22b5/lesson/ac9182c8-4e96-4d29-b3eb-630496944ac8" />
</CardGroup>


# What Is Terragrunt

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Basic-Concepts/What-Is-Terragrunt/page

Terragrunt is a wrapper for Terraform that enhances Infrastructure as Code workflows by improving management of complex infrastructures with less repetition.

Terragrunt is a lightweight wrapper for [Terraform](https://www.terraform.io/), built by Gruntwork to bring structure and automation to Infrastructure as Code (IaC) workflows. Rather than replacing Terraform, Terragrunt enhances it—making it easier to manage complex, multi-environment infrastructures with less repetition and more consistency.

<Callout icon="lightbulb">
  Terragrunt works *on top* of Terraform. You still write your IaC in Terraform language and benefit from the Terraform CLI.
</Callout>

## Why Terragrunt?

* Enforces best practices for Terraform configurations
* Simplifies remote state configuration and locking
* Promotes reuse of variables and modules
* Reduces code duplication with parent–child inheritance

## Key Features

| Feature                      | Description                                                                                          |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| Hierarchical Configuration   | Organize Terraform code in directories that reflect environments and regions.                        |
| Remote State Management      | Automate backend setup (e.g., S3, Azure Blob, GCS) and enable state locking with DynamoDB or Consul. |
| Modular Variable Definitions | Define shared variables in one place and reference them across multiple modules and environments.    |
| DRY (Don't Repeat Yourself)  | Inherit and override configurations in a parent–child folder structure to minimize duplication.      |

<Callout icon="triangle-alert">
  Always enable state locking and encryption for your remote backend to prevent concurrent writes and protect sensitive data.
</Callout>

<Frame>
  ![The image lists four key features: Hierarchical Configuration, Remote Management, Modular Variable Definitions, and DRY Approach, each with an icon.](https://kodekloud.com/kk-media/image/upload/v1752884291/notes-assets/images/Terragrunt-for-Beginners-What-Is-Terragrunt/key-features-hierarchical-remote-modular-dry.jpg)
</Frame>

## Common Use Cases

Terragrunt shines in scenarios where Terraform alone can become unwieldy:

| Use Case                        | Benefit                                                                                        |
| ------------------------------- | ---------------------------------------------------------------------------------------------- |
| Complex Infrastructure Projects | Simplifies management of interdependent modules, networks, and cloud resources.                |
| Multi-Environment Deployments   | Maintains consistency across dev, staging, and prod through shared remote state and variables. |

<Frame>
  ![The image illustrates use cases for Terragrunt, highlighting its application in managing complex infrastructure and deployments.](https://kodekloud.com/kk-media/image/upload/v1752884293/notes-assets/images/Terragrunt-for-Beginners-What-Is-Terragrunt/terragrunt-use-cases-infrastructure-deployments.jpg)
</Frame>

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/)
* [Terraform Documentation](https://www.terraform.io/docs/)
* [Gruntwork Blog on Terragrunt](https://blog.gruntwork.io/introducing-terragrunt-9f9d2c2bdb34)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/9618155f-f613-4c7b-92c7-9be9ddfa22b5/lesson/48d37272-f19b-4ae3-a51f-01a1c269e483" />
</CardGroup>
