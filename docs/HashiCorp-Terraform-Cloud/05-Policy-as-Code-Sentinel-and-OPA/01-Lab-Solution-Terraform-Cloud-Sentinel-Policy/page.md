# Lab Solution Terraform Cloud Sentinel Policy

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Policy-as-Code-Sentinel-and-OPA/Lab-Solution-Terraform-Cloud-Sentinel-Policy/page

This guide covers implementing Policy as Code in Terraform Cloud using Sentinel to enforce organizational policies for infrastructure compliance.

In this lab, we’ll implement **Policy as Code** in Terraform Cloud with **Sentinel**. Sentinel enforces organizational policies between the `terraform plan` and `terraform apply` stages, ensuring your infrastructure remains compliant before changes are applied.

<Frame>
  ![The image shows a KodeKloud lab interface for Terraform Cloud Sentinel Policy, featuring a diagram explaining how Sentinel works with Terraform Cloud and a Visual Studio Code editor with instructions for opening a terminal.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878768/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-Cloud-Sentinel-Policy/kodekloud-terraform-cloud-sentinel-diagram.jpg)
</Frame>

## Prerequisites: Teams & Governance Tier

Sentinel policies require the **Teams & Governance** tier in Terraform Cloud. In **Settings → Plan & Billing**, activate your free trial or subscription for this tier to unlock Policy as Code, cost estimation, and run tasks.

<Callout icon="lightbulb">
  You must have an active Teams & Governance plan in Terraform Cloud before you can enforce Sentinel policies.
</Callout>

<Frame>
  ![The image shows a KodeKloud lab interface for Terraform Cloud Sentinel Policy, with instructions on activating the "Team and Governance" plan and a Visual Studio Code editor on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878769/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-Cloud-Sentinel-Policy/kodekloud-terraform-cloud-sentinel-policy.jpg)
</Frame>

In **Plan & Billing** you’ll see your current plan:

<Frame>
  ![The image shows a pricing plan page for a service, detailing options for Free, Trial, and Team plans, with features and pricing information. The sidebar includes navigation options like Workspaces, Plan & Billing, and Integrations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878770/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-Cloud-Sentinel-Policy/pricing-plan-page-free-trial-team.jpg)
</Frame>

The Teams & Governance tier includes all Team features plus Policy as Code and additional run capabilities:

<Frame>
  ![The image shows a pricing and feature comparison for different plans in a software application, with options for "Team & Governance" and "Business" plans. The sidebar includes navigation options like "Plan & billing" and "Integrations."](../../../../images/kodekloud.com/kk-media/image/upload/v1752878771/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-Cloud-Sentinel-Policy/pricing-feature-comparison-software-plans.jpg)
</Frame>

## Fork the Sentinel Policy Repository

Start by forking the HashiCorp Sentinel policy repository into your GitHub account. This gives you a local copy to customize and connect to Terraform Cloud.

<Frame>
  ![The image shows a KodeKloud lab interface for Terraform Cloud Sentinel Policy, with instructions to create a fork of a HashiCorp repository on GitHub. On the right, there's a Visual Studio Code editor with a terminal open.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878773/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-Cloud-Sentinel-Policy/kodekloud-terraform-sentinel-policy-lab.jpg)
</Frame>

## Review Sentinel Policies

Below are two example policies from the repository.

### 1. Enforce Mandatory Tags

This policy uses the `tfplan-functions` import to require that every AWS EC2 instance in the plan has a `Name` tag. The `main` rule fails if any instance is missing this tag.

```sentinel theme={null}
import "tfplan-functions" as plan
