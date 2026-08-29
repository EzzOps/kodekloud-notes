# include Block

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Blocks/include-Block/page

The Include Block in Terragrunt allows integration of external HCL files, enhancing reusability and consistency in infrastructure configurations.

The **Include Block** in Terragrunt enables you to integrate external HCL files or entire directories into your configuration, promoting reusability, reducing duplication, and ensuring consistency across your infrastructure.

## Include Block Attributes

| Attribute                  | Description                                                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| `path`                     | Relative or absolute filesystem path to the Terragrunt configuration file or directory.            |
| `find_in_parent_folders()` | Searches parent directories for a matching configuration when set to `true` or used as a function. |

![The image is an infographic titled "Include Block" showing two attributes: "Path," which defines the location of external config, and "Find\_in\_parent," which searches for included config in parent folders.](https://kodekloud.com/kk-media/image/upload/v1752884304/notes-assets/images/Terragrunt-for-Beginners-include-Block/include-block-infographic-path-find-in-parent.jpg)

## Key Benefits

1. Reusability\
   Integrate shared HCL files to avoid rewriting the same remote-state or provider settings.
2. Consistency\
   Enforce uniform patterns (naming conventions, tags, backends) across modules.
3. Efficiency\
   Follow the DRY principle by centralizing common logic in one place.

![The image is an infographic titled "Include Block" that outlines three benefits: promoting reusability through external config, reducing duplication, and ensuring consistency across infrastructure.](https://kodekloud.com/kk-media/image/upload/v1752884305/notes-assets/images/Terragrunt-for-Beginners-include-Block/include-block-infographic-benefits.jpg)

## Considerations

* **Override Conflicts**\
  Understand how included blocks inherit or override values in child configurations.
* **Directory Hierarchy**\
  Deep folder structures with multiple includes may become hard to trace without clear naming.

> **triangle-alert** Avoid overly complex include hierarchies. Always document your folder layout and include points to prevent configuration drift.

![The image is an informational graphic titled "Include Block," highlighting considerations such as being mindful of potential conflicts and how configurations inherit and override settings.](https://kodekloud.com/kk-media/image/upload/v1752884306/notes-assets/images/Terragrunt-for-Beginners-include-Block/include-block-configuration-graphic.jpg)

## Best Practices

* Extract shared logic (remote-state, provider blocks, common locals) into dedicated HCL files.
* Use `expose = true` to make outputs or locals from an included file available to child modules.
* Leverage `find_in_parent_folders()` to avoid hard-coding relative paths.

> **lightbulb** Place a `common.hcl` at your repo root for project-wide settings (e.g., tags, metadata) so that every module can `include` it.

![The image features a graphic with a puzzle piece icon, labeled "Include Block," and text stating it is used for organizing and modularizing configs, along with a "Best Practices" button.](https://kodekloud.com/kk-media/image/upload/v1752884307/notes-assets/images/Terragrunt-for-Beginners-include-Block/include-block-puzzle-best-practices.jpg)

***

## Example: Centralizing Remote State

In your root `terragrunt.hcl`, define the S3 backend:

```hcl theme={null}
