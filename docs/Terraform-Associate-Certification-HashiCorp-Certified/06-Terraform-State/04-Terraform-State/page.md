# Terraform State

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Terraform-State/Terraform-State/page

This article reviews Terraform state, its purpose, and best practices for managing it effectively.

In this lesson, we'll review Terraform state, its purpose, and best practices for managing it. Terraform state is a JSON file that records your infrastructure's current configuration and serves as a single source of truth for Terraform operations like plan and apply.

When you create a resource for the first time by running the Terraform apply command, Terraform generates a state file named terraform.tfstate in the same directory as your configuration files. Additionally, a backup file called terraform.tfstate.backup is created.

## Initial Resource Creation

Consider the following Terraform configuration:

```hcl theme={null}
