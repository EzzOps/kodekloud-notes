# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Workspaces/Introduction/page

Explains Terraform CLI workspaces, how to manage multiple state instances, workspace commands, comparisons with separate backends, limitations, and best practices.

Terraform workspaces

This lesson introduces Terraform workspaces and shows how a single set of Terraform configuration files can manage multiple isolated state instances. You will learn the workspace commands to create, list, select, and delete workspaces, compare CLI workspaces with separate state files/backends, and identify when workspaces are not appropriate so you can choose alternative approaches.

<Frame>
  <img alt="The image outlines an introduction to Terraform workspaces, detailing four key learning objectives: explaining workspaces, using workspace commands, comparing workspaces with separate state files, and identifying scenarios where workspaces are inappropriate." />
</Frame>

Terraform CLI workspaces provide a lightweight way to maintain multiple state snapshots from the same configuration files. Each workspace stores its own Terraform state, enabling you to reuse a single codebase to manage multiple environments (for example: `dev`, `staging`, `prod`) without copying or duplicating the configuration.

What workspaces do and do not do:

* They isolate Terraform state only. They do not automatically create separate cloud accounts, provider configurations, or change resource identifiers.
* Resource naming collisions can occur when different workspaces deploy resources with identical names to the same provider account. Avoid collisions by making resource names workspace-aware (for example: `\`${local.prefix}-$\`\`).
* The default workspace is named `default`. Creating a new workspace does not modify your configuration files.

> **lightbulb** Terraform CLI workspaces are a state-scoping mechanism only. If you need stronger isolation (different accounts, different backends, or different provider configurations), consider separate state files/backends or separate configurations.

Common workspace commands

```bash theme={null}
