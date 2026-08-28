# get parent terragrunt dir

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Functions/get-parent-terragrunt-dir/page

This article explains the `get_parent_terragrunt_dir()` function for managing hierarchical configurations in Terragrunt by returning the parent directory path.

Terragrunt’s built-in function `get_parent_terragrunt_dir()` simplifies hierarchical configuration management by returning the file path of the parent Terragrunt directory. Use it to construct relative `source` paths, inherit common settings, and keep your infrastructure code modular and maintainable.

## What Is `get_parent_terragrunt_dir()`?

`get_parent_terragrunt_dir()` resolves at runtime to the directory containing the nearest parent `terragrunt.hcl`. This enables:

* Dynamic discovery of module or state backend locations
* Reuse of shared configurations defined in a parent folder
* Cleaner directory structures for multi-environment setups

<Callout icon="lightbulb">
  Ensure your Terragrunt directory layout follows a clear hierarchy—each child folder must reside under a parent that contains a `terragrunt.hcl`.
</Callout>

## Key Benefits

| Feature                       | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| Dynamic Path Construction     | Automatically build paths for Terraform modules relative to parent folders. |
| Hierarchical Inheritance      | Share backend or provider settings from a top-level `terragrunt.hcl`.       |
| Modular & Flexible Structures | Keep each environment or component isolated while reusing common logic.     |

<Frame>
  ![The image describes the benefits of the get\_parent\_terragrunt\_dir function, highlighting its adaptability to parent Terragrunt configs, dynamic path construction, and support for modular and flexible config structures.](https://kodekloud.com/kk-media/image/upload/v1752884353/notes-assets/images/Terragrunt-for-Beginners-get-parent-terragrunt-dir/get-parent-terragrunt-dir-benefits.jpg)
</Frame>

## Example Usage

Place the following in a child environment’s `terragrunt.hcl` to reference a module stored alongside the parent configuration:

```hcl theme={null}
