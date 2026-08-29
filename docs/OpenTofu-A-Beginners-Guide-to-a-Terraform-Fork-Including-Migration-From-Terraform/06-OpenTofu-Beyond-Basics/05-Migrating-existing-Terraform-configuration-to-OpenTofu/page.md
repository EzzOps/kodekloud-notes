# Migrating existing Terraform configuration to OpenTofu

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Beyond-Basics/Migrating-existing-Terraform-configuration-to-OpenTofu/page

This guide provides a step-by-step process for migrating Terraform configurations to OpenTofu, including rollback and troubleshooting tips.

OpenTofu 1.6 is fully compatible with Terraform 1.6, making it easy to switch your existing infrastructure-as-code workflows. This guide walks you through a safe, step-by-step migration and provides tips for rollback and troubleshooting.

## Prerequisites

* Terraform 1.6.x installed
* Access to your Terraform state file (`terraform.tfstate`)
* A version-control backup or snapshot of your configuration

## Step-by-Step Migration

1. **Document a disaster recovery plan**\
   Outline rollback procedures and how to restore state in case of unexpected issues.

2. **Apply any pending Terraform changes**
   ```bash theme={null}
   terraform init
   terraform plan
   terraform apply
   ```

3. **Install OpenTofu**\
   Follow the official installation guide for your OS: [OpenTofu Installation](/docs/installation).

4. **Backup your Terraform state file**

> **lightbulb** Always version-control or copy your `terraform.tfstate` before you begin.

```bash theme={null}
cp terraform.tfstate terraform.tfstate.backup
```

5. **Initialize OpenTofu and preview the plan**
   ```bash theme={null}
   tofu init
   tofu plan
   ```

6. **Test a non-critical change**\
   Modify a minor resource to verify compatibility:
   ```bash theme={null}
   # Example: Update a tag on a test resource
   tofu apply
   ```
   Confirm that resources apply without drift before proceeding to production.

![The image outlines a six-step process for migrating existing Terraform configurations to OpenTofu, including preparing a disaster recovery plan, applying changes, installing OpenTofu, backing up state files, initializing OpenTofu, inspecting the plan, and testing changes.](https://kodekloud.com/kk-media/image/upload/v1752882841/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Migrating-existing-Terraform-configuration-to-OpenTofu/terraform-to-opentofu-migration-process.jpg)

## Getting Community Support

If you encounter issues during migration, leverage the OpenTofu community:

* Join the [OpenTofu Slack](https://slack.opentofu.io) for real-time assistance.
* Post in [GitHub Discussions](https://github.com/opentofu/opentofu/discussions) under “Q\&A.”

![The image is a diagram titled "Migrating Existing Terraform Configuration to OpenTofu," showing two options for support: OpenTofu Slack and GitHub Discussions.](https://kodekloud.com/kk-media/image/upload/v1752882843/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Migrating-existing-Terraform-configuration-to-OpenTofu/migrating-terraform-configuration-opentofu-diagram.jpg)

***

If you need to revert to Terraform—whether due to workflow preference or compatibility issues—follow these steps:

1. **Backup your OpenTofu state**

> **triangle-alert** Skipping this step may lead to state loss. Always keep a backup.

```bash theme={null}
cp terraform.tfstate terraform.tfstate.backup
```

2. **Re-initialize Terraform**
   ```bash theme={null}
   terraform init
   ```

3. **Review the execution plan**
   ```bash theme={null}
   terraform plan
   ```

4. **Apply a test change**
   ```bash theme={null}
   terraform apply
   ```
   Ensure the rollback completes successfully before normal operations.

![The image outlines four steps for migrating back from OpenTofu to Terraform, including creating a backup, running terraform init, verifying the plan, and testing the rollback.](https://kodekloud.com/kk-media/image/upload/v1752882843/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Migrating-existing-Terraform-configuration-to-OpenTofu/migrate-opentofu-to-terraform-steps.jpg)

***

When you discover a bug in OpenTofu—during migration or rollback—please file a report on [OpenTofu GitHub Issues](https://github.com/opentofu/opentofu/issues). Include:

| Report Type            | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| Bug report             | Steps to reproduce, expected vs. actual behavior        |
| Feature request (RFC)  | Rationale, proposed API changes                         |
| Security vulnerability | Version details, impact analysis (use private channels) |

> **lightbulb** Search existing issues first and follow the [issue templates](https://github.com/opentofu/opentofu/issues/new/choose).

![The image illustrates a migration from OpenTofu to Terraform due to a bug, featuring icons of both platforms and a screenshot of the OpenTofu GitHub issues page.](https://kodekloud.com/kk-media/image/upload/v1752882845/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Migrating-existing-Terraform-configuration-to-OpenTofu/opentofu-terraform-migration-illustration.jpg)

***

## Links and References

* [OpenTofu Documentation](https://docs.opentofu.io/)
* [Terraform 1.6 Release Notes](https://github.com/hashicorp/terraform/releases/tag/v1.6.0)
* [OpenTofu GitHub Repository](https://github.com/opentofu/opentofu)
* [Terraform Configuration Language](https://www.terraform.io/language)

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/5a06d90f-8a8a-49a9-99d6-30b70e37bc83/lesson/0317d56d-311e-4001-9698-4f5157f54210)
