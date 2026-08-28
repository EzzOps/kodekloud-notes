# Returns the base name of the directory containing this Terragrunt configuration
locals {
  current_module = basename(get_terragrunt_dir())
}
```

This pattern helps you dynamically name resources or output modules based on directory structure—ideal for large, multi-environment projects.

## Links and References

* Terragrunt Documentation: [https://terragrunt.gruntwork.io/docs/](https://terragrunt.gruntwork.io/docs/)
* Terraform Language Functions: [https://developer.hashicorp.com/terraform/language/functions](https://developer.hashicorp.com/terraform/language/functions)
* Terragrunt GitHub Repository: [https://github.com/gruntwork-io/terragrunt](https://github.com/gruntwork-io/terragrunt)
* Best Practices for Infrastructure as Code: [https://www.hashicorp.com/resources/series/infrastructure-as-code-guide](https://www.hashicorp.com/resources/series/infrastructure-as-code-guide)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/5775621f-5504-4da8-835d-661cda37a852/lesson/de16959f-d86c-4a43-8b10-8dd6f3934411" />
</CardGroup>


# find in parent folders

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Functions/find-in-parent-folders/page

This article explains how to use Terragrunt’s `find_in_parent_folders` function for recursive file searches in project directories.

Terragrunt’s built-in function `find_in_parent_folders` enables recursive searches up your directory tree to locate a specific file or folder. This approach is invaluable when you need to reference shared configurations or modules in a multi-layered project, removing the brittleness of hardcoded relative paths.

<Frame>
  ![The image shows a hierarchical arrangement of folder icons with the label "find\_in\_parent\_folders" at the top and "Functionality" at the bottom. It appears to represent a file system structure or search functionality within parent folders.](https://kodekloud.com/kk-media/image/upload/v1752884349/notes-assets/images/Terragrunt-for-Beginners-find-in-parent-folders/find-in-parent-folders-hierarchy.jpg)
</Frame>

## Why Use `find_in_parent_folders`?

By leveraging this function, you can:

* Dynamically adapt configuration based on files located higher in the hierarchy
* Inherit and override settings across environments without manual path tweaks
* Maintain cleaner, DRY (Don’t Repeat Yourself) configurations

<Frame>
  ![The image is a presentation slide titled "find\_in\_parent\_folders," highlighting two benefits: adapting based on configurations from parent folders and flexible configuration inheritance.](https://kodekloud.com/kk-media/image/upload/v1752884350/notes-assets/images/Terragrunt-for-Beginners-find-in-parent-folders/find-in-parent-folders-benefits-slide.jpg)
</Frame>

## Best Practices

* Organize projects into clear, modular, hierarchical folders
* Use `find_in_parent_folders` inside `include` blocks to locate root-level `terragrunt.hcl`
* Avoid embedding static paths; let Terragrunt resolve them dynamically

<Frame>
  ![The image is a diagram titled "find\_in\_parent\_folders" with icons and text explaining its use in modular environments and include blocks, along with a "Best Practices" button.](https://kodekloud.com/kk-media/image/upload/v1752884351/notes-assets/images/Terragrunt-for-Beginners-find-in-parent-folders/find-in-parent-folders-diagram-best-practices.jpg)
</Frame>

<Callout icon="lightbulb">
  `find_in_parent_folders` stops when it hits the filesystem root or finds the target file. If the file isn’t present, Terragrunt throws an error.
</Callout>

## Real-World Example

Imagine a VPC module that relies on common variables from `common.hcl`.

Before (hardcoded path):

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

locals {
  common_vars = read_terragrunt_config("../common.hcl")
}

inputs = {
  name = "${local.common_vars.inputs.project}-${local.common_vars.inputs.environment}-VPC"
}
```

After (dynamic lookup):

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

locals {
  common_vars = read_terragrunt_config(find_in_parent_folders("common.hcl"))
}

inputs = {
  name = "${local.common_vars.inputs.project}-${local.common_vars.inputs.environment}-VPC"
}
```

Now, no matter how deep your `vpc/` folder is nested, Terragrunt will climb up until it finds `common.hcl`.

### Verify with Terragrunt

Run:

```bash theme={null}
~/workspace/vpc
> terragrunt plan
```

You should see the VPC name generated using values from `common.hcl`, for example:

```text theme={null}
KodeKloudDevVPC
```

### common.hcl

```hcl theme={null}
inputs = {
  project     = "KodeKloud"
  environment = "dev"
}
```

## References

* [Terragrunt Documentation: find\_in\_parent\_folders](https://terragrunt.gruntwork.io/docs/reference/functions/#find_in_parent_folders)
* [Terragrunt Official Site](https://terragrunt.gruntwork.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/5775621f-5504-4da8-835d-661cda37a852/lesson/0fa40a93-2c92-4fb1-9ef6-5477ac7d9604" />
</CardGroup>
