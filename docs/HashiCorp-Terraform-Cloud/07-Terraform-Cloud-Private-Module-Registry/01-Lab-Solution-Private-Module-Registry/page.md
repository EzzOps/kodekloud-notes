# Single variable
terraform plan -var="name=value"

# Load from a file
terraform apply -var-file="env.prod.tfvars"

# Export as environment variable
export TF_VAR_region=us-west-2
terraform apply
```

Terraform 0.10.0+ automatically loads any `*.auto.tfvars` in your working directory:

```bash theme={null}
# Rename your terraform.tfvars
mv terraform.tfvars terraform.auto.tfvars
```

> **lightbulb** Using `terraform.auto.tfvars` lets you track non-sensitive defaults in Git while still overriding them via the CLI or workspace UI.

![The image provides information on setting non-sensitive variables in Terraform using auto.tfvars files, and mentions that workspaces using Terraform v0.10.0 or later can load default values from these files. It also suggests using the Terraform Cloud Provider or variables API for adding multiple variables.](https://kodekloud.com/kk-media/image/upload/v1752878793/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Variables/terraform-auto-tfvars-variables-guide.jpg)

## Variable Precedence

When a variable exists in multiple locations, Terraform applies values based on this hierarchy (highest → lowest):

1. **CLI** flags (`-var` or `-var-file`)
2. **Workspace** UI variables
3. **Organization** Variable Sets
4. **Auto-loaded** `*.auto.tfvars` files

Command-line inputs override workspace settings, which override organizational sets, which in turn override `auto.tfvars` defaults.

![The image illustrates the order of precedence for Terraform Cloud, listing local values, files ending with \*.auto.tfvars, workspace-specific values, and variable sets, with a visual hierarchy on the right.](https://kodekloud.com/kk-media/image/upload/v1752878794/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Variables/terraform-cloud-precedence-order-diagram.jpg)

![The image illustrates the order of precedence for variable settings, showing a hierarchy from command line variables to global variables, with a visual flowchart and priority indicators.](https://kodekloud.com/kk-media/image/upload/v1752878795/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Variables/variable-precedence-flowchart-hierarchy.jpg)

For more details, see the [Terraform Cloud Variable Precedence documentation](https://www.terraform.io/cloud-docs/workspaces/variables#variable-precedence).

## Best Practices & Recommendations

* Store **non-sensitive** defaults in `*.auto.tfvars` files and commit them to Git.
* Keep **sensitive** values in Terraform Cloud—either at the workspace level or via Organization Variable Sets.
* Regularly rotate credentials and audit workspace variable access.

![The image provides recommendations for using Terraform Cloud, advising to use .auto.tfvars files for non-sensitive variables and to set sensitive variables in the Workspace's Variables section. It includes the Terraform Cloud logo and cartoon characters at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878796/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Variables/terraform-cloud-recommendations-auto-tfvars.jpg)

## Links and References

* [Terraform Cloud Variables Guide](https://www.terraform.io/cloud-docs/workspaces/variables)
* [Terraform Input Variables](https://www.terraform.io/language/values/variables)
* [Terraform CLI Docs](https://www.terraform.io/cli)
* [HashiCorp Configuration Language (HCL)](https://www.terraform.io/language)
* [Terraform Cloud Best Practices](https://www.terraform.io/cloud-docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/253ba638-af3c-4403-a517-a7f6f7c7594c/lesson/da8bca14-1731-468e-b5fe-5e115c84be3f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/253ba638-af3c-4403-a517-a7f6f7c7594c/lesson/e2714b1d-22d1-4d62-9da8-70f80c20fa5a)


# Lab Solution Private Module Registry

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Private-Module-Registry/Lab-Solution-Private-Module-Registry/page

Learn to manage private providers and modules in Terraform Cloud using the Private Module Registry for secure storage and sharing within your organization.

Welcome to this hands-on lab where you'll learn to manage private providers and modules in Terraform Cloud. The Private Module Registry enables your team to securely store and share Terraform providers and modules within your organization.

## Prerequisites

> **lightbulb** Ensure you have:

  * A Terraform Cloud account with organization permissions
  * A connected VCS provider (e.g., GitHub)
  * `terraform` CLI installed and authenticated

## 1. Importing Public Providers and Modules

First, import existing public resources into your Private Module Registry:

1. Navigate to **Registry** » **Providers**, search for `hashicorp/aws`, and click **Add to organization**.

![The image shows a dialog box for adding a provider to an organization in Terraform Cloud, specifically adding the "hashicorp/aws" provider. There are options to "Add to organization" or "Cancel."](https://kodekloud.com/kk-media/image/upload/v1752878797/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Private-Module-Registry/terraform-cloud-add-provider-dialog.jpg)

2. Switch to the **Modules** tab, search for the S3 bucket module, and click **Add to organization**.

Once complete, your Private Module Registry will include the AWS provider and the S3 bucket module.

## 2. Forking and Publishing a Private Module

Next, fork a public module repository and publish it privately:

1. On the public Terraform Registry, open the **AWS Security Group** module and click the GitHub repo link.

![The image shows a GitHub repository page for "terraform-aws-security-group," displaying the file structure and repository details such as stars, forks, and recent commits.](https://kodekloud.com/kk-media/image/upload/v1752878798/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Private-Module-Registry/github-repo-terraform-aws-security-group.jpg)

2. Fork the repository into your GitHub account.

![The image shows a GitHub interface for creating a new fork of a repository named "terraform-aws-security-group." It includes options to set the owner, repository name, and description, with a button to create the fork.](https://kodekloud.com/kk-media/image/upload/v1752878800/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Private-Module-Registry/github-fork-terraform-aws-security-group.jpg)

3. In Terraform Cloud, go to **Registry** » **Private Module Registry**, click **Publish**, select your GitHub VCS provider, and choose the forked repo.

![The image shows a user interface for adding a module in Terraform Cloud, where the user can connect to a VCS and choose a repository from a list. The sidebar includes options like Workspaces, Registry, and Settings.](https://kodekloud.com/kk-media/image/upload/v1752878801/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Private-Module-Registry/terraform-cloud-add-module-interface.jpg)

After publishing, Terraform Cloud displays the module README and usage details:

![The image shows a webpage for a Terraform module named "security-group," which creates EC2-VPC security groups on AWS. It includes details like version, publication time, and usage instructions.](https://kodekloud.com/kk-media/image/upload/v1752878802/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Private-Module-Registry/terraform-module-security-group-ec2-vpc.jpg)

You can now source this private module:

```hcl theme={null}
module "security-group" {
  source  = "app.terraform.io/Mastering-Terraform-Cloud/security-group/aws"
  version = "4.13.1"
}
```

## 3. Selecting a Specific Module Version

To use an earlier version (for example, `4.8.0`), update your module block:

```hcl theme={null}
module "security-group" {
  source  = "app.terraform.io/Mastering-Terraform-Cloud/security-group/aws"
  version = "4.8.0"
}
```

## 4. Consuming the Private Module in a Terraform Project

Finally, integrate the private module into your application:

1. Copy the **Clumsy Birds** repo URL.

![The image shows a GitHub repository page for a project named "Clumsy Birds," with details about branches, commits, and files such as .gitignore and README.md. The repository is private and has no stars or forks.](https://kodekloud.com/kk-media/image/upload/v1752878803/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Private-Module-Registry/clumsy-birds-github-repo-details.jpg)

2. Clone and switch to the `development` branch:

   ```bash theme={null}
   git clone https://github.com/your-org/clumsy_bird.git
   cd clumsy_bird
   git checkout development
   ```

3. Create `security_groups.tf` and add:

   ```hcl theme={null}
   module "security-group-http" {
     source              = "app.terraform.io/Mastering-Terraform-Cloud/security-group/aws"
     version             = "4.8.0"
     name                = "http-traffic-${var.env}"
     description         = "Security group for HTTP traffic"
     vpc_id              = module.vpc.vpc_id
     ingress_cidr_blocks = ["10.10.0.0/16"]
   }
   ```

4. Commit and push your changes:

   ```bash theme={null}
   git config --global user.email "your.email@example.com"
   git config --global user.name "Your Name"
   git add security_groups.tf
   git commit -m "Add private security group module for HTTP traffic"
   git push origin development
   ```

Terraform Cloud will trigger a run; upon success, the security group appears in AWS.

> **triangle-alert** Ensure your module’s semantic versioning aligns with your organization’s policy. Misaligned versions may break downstream workflows.

## Summary of Actions

| Step                                | Action                        | Destination                     |
| ----------------------------------- | ----------------------------- | ------------------------------- |
| Import public items                 | Add provider & module         | Terraform Cloud Registry        |
| Fork & publish private module       | GitHub fork & Terraform Cloud | Private Module Registry         |
| Select specific module version      | Update `version` attribute    | Terraform configuration         |
| Consume module in project workspace | Clone repo & add module block | Clumsy Birds development branch |

## Links and References

* [Terraform Cloud Private Module Registry](https://www.terraform.io/cloud/registry/private)
* [Terraform CLI Documentation](https://www.terraform.io/docs/cli/index.html)
* [GitHub Forking Guide](https://docs.github.com/en/forks)

This completes the lab on the Terraform Cloud Private Module Registry. Proceed to the next module for advanced collaboration features.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/55b59425-ff18-4a6b-a521-907542051f03/lesson/89b24aff-c770-428d-96c8-dab273b5433d)
