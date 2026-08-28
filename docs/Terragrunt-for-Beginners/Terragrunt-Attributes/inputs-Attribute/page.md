# inputs Attribute

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Attributes/inputs-Attribute/page

Terragrunt’s inputs attribute is essential for passing configuration values into Terraform modules using key-value pairs for modular and maintainable infrastructure code.

Terragrunt’s `inputs` attribute is essential for passing configuration values into Terraform modules. By specifying key-value pairs, you can easily feed outputs from dependencies or define custom variables for your current module, keeping your infrastructure code modular and maintainable.

## How `inputs` Works

<Frame>
  ![The image shows a diagram of key-value pairs, labeled "Inputs Attribute" and "Attributes," with a gradient color bar at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752884276/notes-assets/images/Terragrunt-for-Beginners-inputs-Attribute/key-value-pairs-attributes-diagram.jpg)
</Frame>

In Terragrunt, the `inputs` block maps each variable name to the desired value:

* You can reference outputs from other modules using Terragrunt’s dependency blocks.
* Values defined here correspond directly to the Terraform variables declared in `variables.tf`.

## Key Benefits

<Frame>
  ![The image features a puzzle piece icon with the text "Enables modularization" below it, and a "Benefits" button at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752884277/notes-assets/images/Terragrunt-for-Beginners-inputs-Attribute/puzzle-piece-enables-modularization-benefits.jpg)
</Frame>

* **Modularization**: Share data between modules without duplicating configuration.
* **Reusability**: Centralize common settings (e.g., VPC CIDR ranges) across environments.
* **Maintainability**: Change inputs in a single Terragrunt file rather than multiple Terraform modules.

## Important Considerations

<Callout icon="lightbulb">
  Terragrunt’s `inputs` block does not enforce Terraform variable type constraints. Always verify that the values you provide match the expected type (e.g., `string`, `number`, `list`, `map`).
</Callout>

## Example: AWS VPC Module

Below is a Terragrunt configuration that passes the VPC `name` and `cidr` into the [Terraform AWS VPC module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest):

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
```

### Input Parameters Table

| Input Key | Description                | Example           |
| --------- | -------------------------- | ----------------- |
| name      | VPC resource name          | `"KodeKloud-VPC"` |
| cidr      | CIDR block for the new VPC | `"10.100.0.0/16"` |

## Links and References

* [Terragrunt Inputs Documentation](https://terragrunt.gruntwork.io/docs/features/inputs/)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)
* [Terragrunt Official Site](https://terragrunt.gruntwork.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/1a2a45b4-e7d1-4af2-a897-7ebf83a4350e/lesson/b33fd9c4-044f-4368-bc20-78be07212d51" />
</CardGroup>
