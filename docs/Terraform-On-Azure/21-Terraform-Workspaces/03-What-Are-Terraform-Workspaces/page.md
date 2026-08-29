# Show the currently selected workspace
terraform workspace show

# List workspaces
terraform workspace list

# Create a new workspace (and switch to it)
terraform workspace new dev

# Select an existing workspace
terraform workspace select prod

# Delete a workspace (cannot delete the current workspace)
terraform workspace delete staging
```

Quick comparison: when to use workspaces vs separate backends

| Use case                                                              | Prefer Terraform CLI workspaces                                     | Prefer separate state files / backends or separate configurations               |
| --------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Multiple lightweight states from the same code                        | Yes — when environments differ mainly by variables or name prefixes | No                                                                              |
| Different provider accounts or credentials                            | No — workspaces do not switch providers or credentials              | Yes — use separate backends or configurations                                   |
| Strict isolation for billing, compliance, or RBAC                     | No — state isolation alone is insufficient                          | Yes — use separate backends, accounts, or Terraform Cloud/Enterprise workspaces |
| Substantially different infrastructure (different modules/lifecycles) | No — hard to manage within one configuration                        | Yes — maintain separate configurations or directories                           |

When not to use workspaces

* Do not rely on CLI workspaces for isolation across cloud accounts, subscriptions, or provider credentials — they do not change provider endpoints or authentication.
* Avoid workspaces if environments require significant configuration differences, distinct lifecycles, or unique module compositions.
* If you need independent CI/CD pipelines, strict access control per environment, or separate backends, prefer separate state backends or Terraform Cloud/Enterprise workspaces (these are different from CLI workspaces).

Practical tips and best practices

* Make resource names workspace-aware to prevent collisions: `\`${local.prefix}-$\`\`.
* Always confirm the active workspace before applying changes: `terraform workspace show`.
* Keep variable values and small differences parameterized via variables, locals, or input files when using workspaces.
* Use separate backends or completely separate configurations when you need account-level isolation, different provider blocks, or strict compliance controls.
* Consider naming conventions and CI workflows that explicitly select or set the workspace before planning/applying to avoid accidental operations in the wrong state.

Additional links and references

* [Terraform: State & Backends](https://developer.hashicorp.com/terraform/language/state/backends)
* [Terraform Cloud: Workspaces](https://developer.hashicorp.com/terraform/cloud/workspaces)
* [Terraform CLI workspaces documentation](https://developer.hashicorp.com/terraform/cli/commands/workspace)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/0eb3275a-a37d-45a5-86b5-4920e2e44e7c/lesson/ce4e59eb-f32b-4d99-a3c4-20aedd6aa377" />
</CardGroup>


# What Are Terraform Workspaces

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Workspaces/What-Are-Terraform-Workspaces/page

Explains Terraform workspaces and how they isolate state per environment to reuse one configuration for multiple identical infrastructure environments like dev test and prod.

Terraform workspaces let a single Terraform configuration manage multiple independent environments by switching which state file is active. The configuration — providers, resources, modules, and variables — is authored once and reused. Terraform acts as the execution engine; the only thing that changes between environments is the active workspace.

Each workspace (for example: `dev`, `test`, `prod`) has its own isolated state file while evaluating the same configuration. This enables Terraform to track separate infrastructure lifecycles per environment without duplicating configuration. The core concept is state isolation, not configuration duplication.

<Frame>
  <img alt="The image is a diagram showing Terraform workspaces managing different environments (PROD, TEST, DEV), each with its own state while sharing configuration files. It includes icons for environments, workspaces, and tools like Visual Studio Code, highlighting isolation and state management in infrastructure configuration." />
</Frame>

Overview and characteristics

Workspaces are a lightweight mechanism to manage multiple state files from one Terraform configuration. They are particularly useful when the same infrastructure topology needs to exist in multiple logical environments. Key characteristics:

| Characteristic       | Details                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| State isolation      | Each workspace has its own state file; resources in one workspace are invisible to others.                   |
| Single configuration | Providers, resources, modules, and variables are defined once and shared across workspaces.                  |
| Safety by design     | Operations in one workspace cannot modify resources tracked by another workspace because state is separated. |
| Default workspace    | Terraform provides a `default` workspace. If you don’t create/select another, you operate in `default`.      |

<Callout icon="lightbulb">
  Workspaces provide lightweight state isolation for identical infrastructure topologies. Use them when you need separate state files for multiple environments without duplicating configuration.
</Callout>

What workspaces are designed to support

Workspaces are intended for scenarios where multiple environments share the same architecture and resource definitions. They are ideal for experimentation, testing, ephemeral feature branches, and short-lived sandboxes that should mirror production topology without requiring separate repositories or duplicated configurations.

<Frame>
  <img alt="The image is a diagram illustrating Terraform workspaces with environments for production, testing, and development, highlighting features such as multiple environment support, lightweight isolation, and simplified testing. It shows the relationship between tfvars, tfstate files, and workspace configuration." />
</Frame>

Typical use cases and recommendations

* Standard environment separation (development, testing, staging, production) when all environments follow the same architecture.
* Feature branches or ephemeral environments for validating changes without impacting other states.
* Short-lived sandboxes for experimentation or demos.

If environments diverge significantly (different resources, providers, or modules), prefer separate configurations or dedicated backends rather than forcing divergence through workspaces.

<Frame>
  <img alt="The image illustrates a Terraform workflow with environments for development, testing, and production, using workspaces with tfvars and tfstate files. It also highlights typical use cases like feature testing and temporary environments." />
</Frame>

How switching workspaces works

Terraform maintains one state file per workspace. When you switch workspaces, Terraform changes which state file is active but does not alter the configuration, providers, or resource definitions. From Terraform’s perspective, the same code is being applied against a different isolated state.

Workspaces are effective when environments are structurally identical. They are not a replacement for fully separate configurations or backends if environments have diverged in design or lifecycle requirements.

Common Terraform workspace commands

Use these commands to manage workspaces locally.

| Command                             | Purpose                                                |
| ----------------------------------- | ------------------------------------------------------ |
| `terraform workspace list`          | List all workspaces                                    |
| `terraform workspace new <name>`    | Create and switch to a new workspace                   |
| `terraform workspace select <name>` | Switch to an existing workspace                        |
| `terraform workspace show`          | Display the current workspace                          |
| `terraform workspace delete <name>` | Delete a workspace (must not be the current workspace) |

Examples:

```bash theme={null}
