# Terraform Destroy

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Terraform-Destroy/page

Explains how to safely remove Terraform-managed infrastructure using terraform destroy, targeted destroys, and configuration-first workflows while highlighting best practices and warnings.

After applying your Terraform configurations and managing infrastructure with Terraform, you'll eventually need to remove that infrastructure. This article explains how to safely and predictably remove Terraform-managed resources using `terraform destroy` and alternative workflows.

Quick overview:

* `terraform destroy` removes resources managed in the current workspace.
* You can also remove resources by deleting resource blocks from your configuration and running `terraform apply`.
* Targeted destruction (`-target`) destroys specific resources but can cause drift if not accompanied by configuration changes.

## What `terraform destroy` does

`terraform destroy` builds a destruction plan (similar to `terraform plan`) and then, after you confirm, it destroys resources in dependency-aware order. This ensures that resources that depend on others are destroyed before their dependencies (for example, VMs are destroyed before the subnets they use).

Example:

```bash theme={null}
