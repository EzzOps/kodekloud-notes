# instance_type = t2.2xlarge
```

This completes our walkthrough of OpenTofu functions and conditional expressions. Great job!

<Frame>
  ![The image shows a coding environment with instructions to create an EC2 instance using Terraform, alongside a code editor displaying Terraform configuration files and a terminal with output messages.](https://kodekloud.com/kk-media/image/upload/v1752882866/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-Functions-and-Conditional-Expressions/ec2-instance-terraform-coding-environment.jpg)
</Frame>

***

## Links and References

* [OpenTofu Documentation](https://docs.opentofu.org)
* [Terraform Language - Expressions](https://www.terraform.io/language/expressions)
* [AWS IAM User Resource](https://registry.terraform.[SECRET_REDACTED]iam_user)
* [AWS S3 Bucket & Object](https://registry.terraform.[SECRET_REDACTED]s3_bucket)
* [AWS EC2 Instance](https://registry.terraform.[SECRET_REDACTED])

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/042e7b27-75d9-46fc-8f8c-7357d81923c1/lesson/72ecd9c1-c9d4-4bc2-9687-a54a126a5d00" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/042e7b27-75d9-46fc-8f8c-7357d81923c1/lesson/eb423b69-3251-4c0a-86dc-463214648609" />
</CardGroup>


# Demo OpenTofu Workspaces

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Functions-and-Conditional-Expressions/Demo-OpenTofu-Workspaces/page

This guide explains how to create and manage OpenTofu workspaces for separate state files in multiple deployments.

In this guide, you'll learn how to create, select, and manage OpenTofu workspaces to maintain separate state files for multiple deployments of the same configuration. By the end, you'll deploy a payroll application across three regions—US, UK, and India—using a single Terraform-compatible codebase.

## Prerequisites

<Callout icon="lightbulb">
  * OpenTofu CLI installed and available in your `PATH`.
  * A sample project directory named `project-sapphire`.
  * Access to an S3-like backend (e.g., LocalStack) for state storage.
</Callout>

***

## 1. List the Default Workspace

Navigate to your project directory and list available workspaces. By default, OpenTofu starts with the `default` workspace.

```bash theme={null}
cd ~/opentofu-projects/project-sapphire/
tofu workspace list
```

Expected output:

```bash theme={null}
* default
```

***

## 2. Create New Workspaces

Isolate state per region by creating three workspaces: `us-payroll`, `uk-payroll`, and `india-payroll`.

```bash theme={null}
tofu workspace new us-payroll
tofu workspace new uk-payroll
tofu workspace new india-payroll
```

Verify:

```bash theme={null}
tofu workspace list
```

| Workspace     | Description                        |
| ------------- | ---------------------------------- |
| default       | Default environment                |
| us-payroll    | State for US payroll deployment    |
| uk-payroll    | State for UK payroll deployment    |
| india-payroll | State for India payroll deployment |

***

## 3. Select a Workspace

Switch to the `us-payroll` workspace before running any commands:

```bash theme={null}
tofu workspace select us-payroll
