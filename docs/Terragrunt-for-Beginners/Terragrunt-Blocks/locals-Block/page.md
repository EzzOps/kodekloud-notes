# root terragrunt.hcl
remote_state {
  backend = "s3"
  config = {
    encrypt        = true
    bucket         = "kodekloud-terragrunt-remote-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "terraform-locks"
  }

  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}
```

In `vpc/terragrunt.hcl`, include the root remote state:

```hcl theme={null}
# vpc/terragrunt.hcl
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}
```

When running `terragrunt apply` in `vpc/`, Terragrunt will:

1. Locate and include the root `remote_state` block.
2. Generate `backend.tf` with the S3 backend settings.
3. Deploy the VPC module using the shared backend configuration.

## Example: Sharing Common Configuration

Create a `common.hcl` at the repository root:

```hcl theme={null}
# common.hcl
locals {
  project = "KodeKloud"
  owner   = "DevOps Team"
}
```

Then in each module (e.g., `vpc2/terragrunt.hcl`):

```hcl theme={null}
# vpc2/terragrunt.hcl
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

include "common" {
  path   = find_in_parent_folders()
  expose = true
}

inputs = {
  project = local.project
  owner   = local.owner
}
```

This approach ensures both remote-state settings and shared locals (like `project` and `owner`) are available across modules without repetition.

***

## Links and References

* [Terragrunt Include Block Documentation](https://terragrunt.gruntwork.io/docs/features/include-block/)
* [Terragrunt Remote State](https://terragrunt.gruntwork.io/docs/features/remote-state/)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/bab279d4-de1d-4e8d-8376-ea420c71c9e1/lesson/8dea68bf-2d0d-4db6-996e-6c0bf277226e" />
</CardGroup>


# locals Block

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Blocks/locals-Block/page

Learn to use the locals block in Terragrunt for defining reusable variables and expressions to simplify configuration and improve maintainability.

In this lesson, you’ll learn how to leverage the `locals` block in Terragrunt to define reusable variables and expressions directly within your configuration. By centralizing complex values, you can simplify your HCL, reduce duplication, and improve maintainability.

## Benefits of the locals Block

Encapsulating expressions or static values into named local variables offers clear advantages:

| Benefit          | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| Code readability | Improves comprehension by giving meaningful names to expressions         |
| Code reusability | Follows DRY (Don’t Repeat Yourself) by reusing values in multiple places |

<Frame>
  ![The image is a diagram titled "Locals Block" highlighting two benefits: "Code readability" and "Code reusability."](https://kodekloud.com/kk-media/image/upload/v1752884308/notes-assets/images/Terragrunt-for-Beginners-locals-Block/locals-block-code-readability-reusability-diagram.jpg)
</Frame>

## Considerations

Local variables are strictly confined to the configuration where they’re declared. They won’t be shared across sibling or parent Terragrunt files.

<Callout icon="triangle-alert">
  `locals` in Terragrunt are not global. You cannot reference a local variable defined in one directory from another unless explicitly passed through inputs or shared via a common config.
</Callout>

<Frame>
  ![The image is a diagram titled "Locals Block" with two points: "Limited to the scope" and "Cannot be shared across configs," accompanied by icons. At the bottom, there's a label "Considerations."](https://kodekloud.com/kk-media/image/upload/v1752884308/notes-assets/images/Terragrunt-for-Beginners-locals-Block/locals-block-scope-considerations-diagram.jpg)
</Frame>

## Best Practices

* Group related expressions under a single `locals` block to keep your configuration tidy.
* Name variables clearly to convey their purpose (e.g., `project_name`, `environment_cidr`).
* Avoid overusing locals for trivial values; reserve them for expressions or values reused multiple times.
* Document complex locals with inline comments for future maintainers.

<Frame>
  ![The image is a slide titled "Locals Block" with a purple icon and text explaining it is used to reduce complexity by defining variables. It also includes a "Best Practices" button.](https://kodekloud.com/kk-media/image/upload/v1752884309/notes-assets/images/Terragrunt-for-Beginners-locals-Block/locals-block-reduce-complexity-best-practices.jpg)
</Frame>

## Example Usage

### 1. Defining a local variable

```hcl theme={null}
locals {
  project = "KodeKloud"
}
```

### 2. Referencing locals from a shared config (`common.hcl`)

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

include "common" {
  path   = find_in_parent_folders("common.hcl")
  expose = true
}

inputs = {
  name = include.common.locals.project
}
```

### 3. Adding file-specific locals

You can define additional `locals` in any Terragrunt file for values unique to that directory.

```hcl theme={null}
locals {
  cidr = "10.100.0.0/16"
}

inputs = {
  name     = include.common.locals.project
  vpc_cidr = local.cidr
}
```

This `cidr` variable is available only within the current VPC configuration, ensuring isolation from other modules.

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/bab279d4-de1d-4e8d-8376-ea420c71c9e1/lesson/1c5c1958-10fe-4912-964d-5478cecc3b1f" />
</CardGroup>
