# Targeting Resource for Replacement with Terraform Cloud

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Advanced-Topics/Targeting-Resource-for-Replacement-with-Terraform-Cloud/page

Learn to replace a resource in Terraform Cloud without modifying code or Git history using the `-replace` flag and environment variables.

In this guide, you'll learn how to replace a single resource in a Terraform Cloud workspace—connected to a Version Control System (VCS)—without touching your code or Git history. We demonstrate how to inject the `-replace` flag into Terraform Cloud runs by using workspace environment variables.

***

## Overview of the Terraform Cloud Workspace

You have multiple workspaces—**DevOps**, **AWS MyApp Dev**, **Prod**, and **Staging**—all linked to their respective Git branches. The screenshot below shows the Terraform Cloud dashboard with workspace names, run statuses, linked repositories, and last update times.

<Frame>
  ![The image shows a Terraform Cloud dashboard displaying a list of workspaces with their names, run statuses, repositories, and the latest change timestamps. The sidebar includes options for managing workspaces, registry, and settings.](https://kodekloud.com/kk-media/image/upload/v1752878714/notes-assets/images/HashiCorp-Terraform-Cloud-Targeting-Resource-for-Replacement-with-Terraform-Cloud/terraform-cloud-dashboard-workspaces-list.jpg)
</Frame>

***

## Configuring Terraform CLI for Terraform Cloud

Even with a VCS-connected workspace, you can run `terraform init` and `terraform plan` locally by pointing your CLI to Terraform Cloud:

```hcl theme={null}
terraform {
  cloud {
    organization = "Mastering-Terraform-Cloud"
    workspaces {
      name = "devops-aws-myapp-dev"
    }
  }
}
```

After cloning the `clumsy_bird` repo and checking out the `development` branch (tied to the MyApp Dev workspace), initialize and plan:

```bash theme={null}
$ terraform init
$ terraform plan
