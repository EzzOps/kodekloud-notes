# Lab Solution Terraform to GitHub

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Workflows/Lab-Solution-Terraform-to-GitHub/page

This tutorial explains how to integrate Terraform Cloud with GitHub for automated infrastructure provisioning through version control.

In this tutorial, you’ll learn how to integrate **Terraform Cloud** with your **GitHub** account to enable the Version Control Workflow. By registering GitHub as a VCS provider, any commit to your repository automatically triggers `terraform init`, `plan`, and `apply` in Terraform Cloud.

**Prerequisite**: A GitHub account.

***

## 1. Create a GitHub Repository

1. Log in to GitHub and click **New** repository.
2. Configure the repository as follows:

| Setting             | Value                      |
| ------------------- | -------------------------- |
| Repository name     | `clumsy_bird`              |
| Description         | *Your project description* |
| Visibility          | Private                    |
| Initialize with     | README                     |
| .gitignore template | Terraform                  |

3. Click **Create repository**.

***

## 2. Generate a GitHub Personal Access Token

You need a **Personal Access Token (PAT)** with `repo` scope to allow Terraform Cloud to read your repository.

1. In GitHub, go to **Settings > Developer settings > Personal access tokens**.
2. Click **Generate new token**, select **repo** scope, then **Generate token**.
3. Copy the token now—you won’t be able to see it again.

<Frame>
  ![The image shows a GitHub settings page for personal access tokens, displaying generated tokens with options to delete or generate new ones.](https://kodekloud.com/kk-media/image/upload/v1752878900/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/github-settings-personal-access-tokens.jpg)
</Frame>

<Callout icon="triangle-alert">
  Keep your PAT secure. Do not commit it to any repository or share it publicly.
</Callout>

***

## 3. Clone the Repository Locally

In your local or lab environment, clone and push the initial commit:

```bash theme={null}
cd ~/VCS
git clone https://github.com/<your-org>/clumsy_bird.git
cd clumsy_bird
