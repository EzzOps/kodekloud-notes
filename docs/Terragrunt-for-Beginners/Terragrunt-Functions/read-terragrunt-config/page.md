# read terragrunt config

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Functions/read-terragrunt-config/page

This lesson explores Terragrunts `read_terragrunt_config` function for reading HCL files and returning their contents as a map.

In this lesson, we’ll dive into Terragrunt’s built-in function `read_terragrunt_config`, which reads a Terragrunt HCL file and returns its contents as a map. This enables you to:

* Dynamically consume inputs, outputs, blocks, and attributes from another configuration.
* Adapt resources for different environments or setups.
* Promote modularity, reusability, and DRY infrastructure code.

When you invoke:

```hcl theme={null}
read_terragrunt_config("<path/to/file.hcl>")
```

Terragrunt will:

1. Parse the specified HCL file.
2. Serialize its contents into a map.
3. Expose all blocks and attributes under that map for referencing in your configuration.

## Key Benefits

* **Dynamic Configuration**: Tailor resources per environment.
* **Modularity**: Reuse shared inputs and outputs.
* **Maintainability**: Avoid duplication across modules.

## Best Practices

| Practice                 | Recommendation                                           |
| ------------------------ | -------------------------------------------------------- |
| Centralize common inputs | Store project-level variables in a root `common.hcl`.    |
| Use `locals` for mapping | Assign descriptive local names to imported values.       |
| Keep shared configs lean | Include only widely used variables to reduce complexity. |
| Verify relative paths    | Ensure the path passed to the function is correct.       |

<Frame>
  ![The image outlines best practices for "read\_terragrunt\_config," highlighting the need for resources to adapt dynamically and access input/output configurations.](https://kodekloud.com/kk-media/image/upload/v1752884356/notes-assets/images/Terragrunt-for-Beginners-read-terragrunt-config/best-practices-read-terragrunt-config.jpg)
</Frame>

<Callout icon="lightbulb">
  Use clear naming conventions in your `common.hcl` to avoid confusion when referencing nested attributes.
</Callout>

***

## Example: Sharing Common Variables

Create a root-level `common.hcl` with project-wide variables:

```hcl theme={null}
