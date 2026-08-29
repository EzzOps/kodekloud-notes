# Terragrunt Function Overview

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Functions/Terragrunt-Function-Overview/page

Overview of core Terragrunt functions to enhance modularity, maintainability, and dynamic configuration in infrastructure design.

As you design your infrastructure with Terragrunt, leveraging its built-in functions can greatly enhance modularity, maintainability, and dynamic configuration. Below, we present a concise overview of core Terragrunt functions, along with practical examples and links to further resources.

## Core Terragrunt Functions

| Function                    | Description                                                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `read_terragrunt_config`    | Read and parse another Terragrunt configuration file, giving you access to its inputs, dependencies, and locals.        |
| `find_in_parent_folders`    | Recursively search parent directories to locate specific files (e.g., `terragrunt.hcl`), enabling shared configs.       |
| `path_relative_to_include`  | Compute the relative path from the current file to an included configuration, promoting modular directory layouts.      |
| `get_terragrunt_dir`        | Return the full path of the directory containing the current `terragrunt.hcl` file, useful for dynamic file references. |
| `get_parent_terragrunt_dir` | Retrieve the directory path of the parent Terragrunt configuration, supporting hierarchical inheritance.                |
| `run_cmd`                   | Execute a shell command directly within Terragrunt, allowing automation of external tools or scripts.                   |

> **triangle-alert** Use `run_cmd` with caution. Executing shell commands can expose sensitive information or introduce security risks. Always validate inputs and avoid hardcoding credentials.

<Frame>
  <img alt="The image lists Terragrunt functions in a vertical flowchart format, including functions like read_terragrunt_config and run_cmd." />
</Frame>

## Combining Terragrunt with Terraform Functions

Terragrunt functions become even more powerful when combined with Terraform’s native functions. For example, to extract just the directory name of your current Terragrunt configuration, you can use Terraform’s `basename` together with `get_terragrunt_dir`:

```hcl theme={null}
