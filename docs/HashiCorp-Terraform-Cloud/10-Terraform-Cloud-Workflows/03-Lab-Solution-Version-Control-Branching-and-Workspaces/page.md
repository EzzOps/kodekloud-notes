# Add your Terraform code or update README
git add .
git commit -m "Initial Terraform configuration"
git push origin main
```

Verify the three files (`README.md`, `.gitignore`, your Terraform code) in GitHub:

![The image shows a GitHub repository named "clumsy\_bird" with several files related to Terraform configuration. It includes details like commit messages and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752878901/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/clumsy-bird-github-repo-terraform.jpg)

***

## 4. Configure GitHub as a VCS Provider in Terraform Cloud

1. In Terraform Cloud, navigate to **Settings > VCS Providers**.
2. Click **Connect new provider** → **GitHub**.
3. Follow the instructions to register a new OAuth application on GitHub:

![The image shows a setup page for connecting a version control system (VCS) provider to Terraform Cloud, with instructions for registering a new OAuth application on GitHub. The sidebar includes options like Plan & Billing, Security, and Version Control.](https://kodekloud.com/kk-media/image/upload/v1752878903/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/vcs-connection-setup-terraform-cloud.jpg)

![The image shows a setup guide for connecting GitHub to Terraform Cloud, including instructions for registering a new OAuth application and entering details like application name, homepage URL, and authorization callback URL.](https://kodekloud.com/kk-media/image/upload/v1752878904/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/github-terraform-cloud-setup-guide.jpg)

4. After registering the app, copy the **Client ID** and **Client Secret**:

![The image shows a settings page for a Terraform Cloud application on GitHub, displaying details like the client ID and client secrets, with options to manage user tokens and generate new secrets.](https://kodekloud.com/kk-media/image/upload/v1752878905/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/terraform-cloud-github-settings-page.jpg)

5. Back in Terraform Cloud, enter the **Client ID**, **Client Secret**, and click **Connect and continue**. Then authorize the OAuth app.

> **lightbulb** If you prefer SSH-based access instead of HTTPS, generate an SSH key pair and upload the public key in your GitHub OAuth settings:

  ```bash theme={null}
  ssh-keygen -t rsa -m PEM -f "~/.ssh/service_terraform" -C "service_terraform_enterprise"
  ```

Once connected, GitHub appears as a VCS provider:

![The image shows a VCS Providers settings page for GitHub in Terraform Cloud, displaying details like callback URL, HTTP URL, API URL, creation date, and OAuth token ID. There are options to edit or delete the client and add a VCS provider.](https://kodekloud.com/kk-media/image/upload/v1752878906/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/github-vcs-providers-settings-terraform.jpg)

***

## 5. Associate the Workspace with Your GitHub Repository

1. In your Terraform Cloud workspace, go to **Settings > Version Control Workflow**.
2. Select the GitHub provider and choose your repository (`<your-org>/clumsy_bird`).

![The image shows a Terraform Cloud interface where a user is choosing a repository for version control. The selected repository is "gmaentz/clumsy\_bird" from a list of available repositories.](https://kodekloud.com/kk-media/image/upload/v1752878908/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/terraform-cloud-repository-selection-gmaentz.jpg)

3. Enable the following options:

| Option                 | Description                                     |
| ---------------------- | ----------------------------------------------- |
| Auto Apply             | Automatically apply approved plans              |
| Automatic Run Triggers | Trigger runs on VCS events                      |
| Speculative Plans      | Create a plan on pull requests without applying |

4. Click **Save settings**.

![The image shows a settings page for a workspace in Terraform Cloud, focusing on run triggers, version control, and pull request options. It includes options for automatic run triggering and other settings related to version control and submodules.](https://kodekloud.com/kk-media/image/upload/v1752878909/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/terraform-cloud-workspace-settings-page.jpg)

***

## 6. Verify the Connection and Trigger a Run

After saving, Terraform Cloud will detect the latest commit and automatically start a run. In the workspace overview, you’ll see the plan and apply details:

![The image shows a Terraform Cloud workspace overview for "devops-aws-myapp-dev," displaying details of the latest run, including resource changes and configuration updates.](https://kodekloud.com/kk-media/image/upload/v1752878910/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/terraform-cloud-workspace-devops-aws.jpg)

You can inspect the commit that triggered the run. For example, this simple deployment script runs as part of a Terraform provisioner:

```bash theme={null}
#!/bin/bash
sudo apt -y update
sudo apt -y install cowsay unzip git build-essential nodejs curl npm node-grunt-cli

# Clone Clumsy Bird application
mkdir -p /src
git clone https://github.com/ellisonleao/clumsy-bird /src/clumsy-bird
```

Once connected, any future commit to `clumsy_bird` will kick off `terraform init`, `plan`, and `apply` in Terraform Cloud:

![The image shows a Terraform Cloud interface displaying a successful run of a Terraform configuration upload from GitHub, with details about the commit and execution. The plan and apply processes have finished, adding 23 resources.](https://kodekloud.com/kk-media/image/upload/v1752878911/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Terraform-to-GitHub/terraform-cloud-successful-run-github.jpg)

***

## Conclusion

You have successfully linked **Terraform Cloud** with **GitHub** using the Version Control Workflow. Every code change now triggers automated infrastructure provisioning.

***

## Links and References

* [Terraform Cloud Version Control Workflow](https://developer.hashicorp.com/terraform/cloud/vcs)
* [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
* [Terraform Cloud](https://www.terraform.io/cloud)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/8dc830bd-1e70-4a76-bc45-b417ff7c1771/lesson/f7384291-f095-4935-94ff-f4409dc44fbd)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/8dc830bd-1e70-4a76-bc45-b417ff7c1771/lesson/2126326e-6db6-4ed8-b2ab-03b910147f90)


# Lab Solution Version Control Branching and Workspaces

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Workflows/Lab-Solution-Version-Control-Branching-and-Workspaces/page

This guide explains integrating Terraform Cloud with GitHub for managing infrastructure across development, staging, and production environments.

In this guide, you’ll learn how to integrate Terraform Cloud with GitHub to manage infrastructure across **development**, **staging**, and **production** environments. You will:

1. Create `development` and `staging` branches in GitHub
2. Configure a shared Terraform Cloud variable set for AWS credentials
3. Point the development workspace to the `development` branch
4. Provision a staging workspace on the `staging` branch
5. Trigger and verify runs in each workspace
6. Create a production workspace on the `main` branch
7. Confirm all workspaces and their run statuses

> **lightbulb** * A Terraform Cloud organization and [Terraform CLI installed](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).
  * A GitHub repository (`clumsy_bird`) containing your Terraform configurations.

***

## 1. Create Development and Staging Branches

Clone your GitHub repository, then create and push the feature branches:

```bash theme={null}
git clone https://github.com/your-org/clumsy_bird.git
cd clumsy_bird
git checkout -b development
git push -u origin development
git checkout main
git checkout -b staging
git push -u origin staging
```

Alternatively, use the GitHub UI to add the `development` and `staging` branches.

![The image shows a GitHub repository page with a branch selection dropdown open, displaying branches "main" and "development." The repository is named "clumsy\_bird" and contains several Terraform configuration files.](https://kodekloud.com/kk-media/image/upload/v1752878912/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/github-repo-clumsy-bird-branches-dropdown.jpg)

***

## 2. Configure a Terraform Cloud Variable Set

In Terraform Cloud, navigate to **Organization Settings → Variable Sets** and create or verify a set containing:

| Variable Name           | Category             | Description         |
| ----------------------- | -------------------- | ------------------- |
| `AWS_ACCESS_KEY_ID`     | Environment Variable | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Environment Variable | Your AWS secret key |

This centralizes AWS credentials for all workspaces in your organization.

> **triangle-alert** Never commit AWS credentials to Git. Always use Terraform Cloud variable sets or [Vault](https://www.vaultproject.io/) for secret management.

***

## 3. Update the Development Workspace

1. Open the **devops-aws-myapp-dev** workspace in Terraform Cloud.
2. Go to **Settings → Version Control**.
3. Change **VCS Branch** to `development` and **Save**.

Terraform Cloud will automatically queue and apply a run on the `development` branch:

![The image shows a KodeKloud lab interface for version control branching and workspaces, with instructions to navigate a workspace on Terraform Cloud. The left side displays task steps, while the right side features a terminal window.](https://kodekloud.com/kk-media/image/upload/v1752878914/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/kodekloud-lab-version-control-terraform.jpg)

![The image shows a Terraform Cloud workspace settings page, specifically the Version Control section, indicating a connection to a GitHub repository named "gmaentz/clumsy\_bird."](https://kodekloud.com/kk-media/image/upload/v1752878914/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-workspace-github-connection.jpg)

![The image shows a version control settings page for a Terraform Cloud workspace, with options for configuring VCS branch, pull requests, and other settings like including submodules on clone.](https://kodekloud.com/kk-media/image/upload/v1752878916/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-vcs-settings-page.jpg)

![The image shows a Terraform Cloud interface with a workspace named "devops-aws-myapp-dev" that is currently in the "Applying" status. The interface includes options for managing workspaces, registry, and settings.](https://kodekloud.com/kk-media/image/upload/v1752878916/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-devops-aws-app-applying.jpg)

***

## 4. Create the Staging Workspace

1. In Terraform Cloud, select **Workspaces → New Workspace**.
2. Choose **Version Control Workflow** and connect to `gmaentz/clumsy_bird`.
3. Configure the workspace:

| Setting                     | Value                    |
| --------------------------- | ------------------------ |
| Name                        | devops-aws-myapp-staging |
| VCS Branch                  | staging                  |
| Auto Apply                  | Enabled                  |
| Automatic Speculative Plans | Enabled                  |

4. (Optional) Add Terraform variables for environment context:

```hcl theme={null}
prefix      = "clumsy"
project     = "Clumsy Bird"
environment = "staging"
```

![The image shows a Terraform Cloud interface for creating a new workspace, with options to choose a workflow type such as version control, CLI-driven, or API-driven. The sidebar includes navigation options like Workspaces, Registry, and Settings.](https://kodekloud.com/kk-media/image/upload/v1752878918/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-workspace-creation-interface.jpg)

![The image shows a Terraform Cloud interface where a user is choosing a repository from a list, with "gmaentz/clumsy\_bird" highlighted. The interface includes navigation options and a filter for repositories.](https://kodekloud.com/kk-media/image/upload/v1752878919/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-repository-selection-interface.jpg)

![The image shows a Terraform Cloud interface for creating a workspace, with options for triggering runs, specifying a VCS branch, and configuring pull requests and other settings. A "Create workspace" button is highlighted.](https://kodekloud.com/kk-media/image/upload/v1752878920/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-workspace-creation-interface-2.jpg)

![The image shows a HashiCorp Cloud Platform interface where a workspace has been created, prompting the user to configure Terraform variables such as prefix, project, and environment.](https://kodekloud.com/kk-media/image/upload/v1752878922/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/hashicorp-cloud-platform-terraform-variables.jpg)

Save and monitor the initial plan/apply run.

***

## 5. Trigger Manual Runs

To validate both environments:

* **Development**: Open **devops-aws-myapp-dev** and click **Start new run**.
* **Staging**: Open **devops-aws-myapp-staging** and click **Start new run**.

> **lightbulb** Auto Apply simplifies continuous delivery, but manual runs offer more control for production-critical changes.

***

## 6. Create the Production Workspace

Repeat the workspace creation steps for production:

| Setting             | Value                          |
| ------------------- | ------------------------------ |
| Name                | devops-aws-myapp-prod          |
| VCS Branch          | main                           |
| Auto Apply          | Enabled (or Manual per policy) |
| Always Trigger Runs | Enabled                        |

1. **Workspaces → New Workspace → Version Control**
2. Select `gmaentz/clumsy_bird` and set **VCS Branch** to `main`.
3. Add the same Terraform variables (`prefix`, `project`, `environment = "production"`).

![The image shows a GitHub repository page for a project named "clumsy\_bird," with a dropdown menu for switching branches, displaying "main," "development," and "staging" branches. The repository contains files related to Terraform configuration.](https://kodekloud.com/kk-media/image/upload/v1752878923/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/github-repo-clumsy-bird-branches.jpg)

Save the workspace to kick off the initial production run.

***

## 7. Verify All Workspaces

Head to **Workspaces** overview. You should see all three environments configured:

| Workspace Name           | Branch      | Status            |
| ------------------------ | ----------- | ----------------- |
| devops-aws-myapp-dev     | development | Applied           |
| devops-aws-myapp-staging | staging     | Applied           |
| devops-aws-myapp-prod    | main        | Pending / Applied |

![The image shows a Terraform Cloud interface displaying a list of workspaces with their names, run statuses, repositories, and the time of the latest changes. Two workspaces have the status "Applied."](https://kodekloud.com/kk-media/image/upload/v1752878925/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Version-Control-Branching-and-Workspaces/terraform-cloud-workspaces-status-list.jpg)

Congratulations! You’ve successfully implemented version control branching strategies and workspace management in Terraform Cloud. Next, explore GitOps-native workflows with Terraform Enterprise or integrate policy as code using Sentinel.

***

## References

* [Terraform Cloud Version Control Workflow](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/vcs)
* [Git Branching Strategies](https://www.atlassian.com/git/tutorials/using-branches)
* [Managing Variables in Terraform Cloud](https://developer.hashicorp.com/terraform/cloud-docs/variables)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/8dc830bd-1e70-4a76-bc45-b417ff7c1771/lesson/b2e16417-4958-4667-87d2-c13d808a04d0)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/8dc830bd-1e70-4a76-bc45-b417ff7c1771/lesson/90da0b84-dc16-4c28-84c0-7606196e8151)
