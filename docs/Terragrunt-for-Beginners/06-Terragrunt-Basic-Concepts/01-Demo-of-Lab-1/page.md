# terraform_version_constraint = "= 1.8.4"
```

```bash theme={null}
~/workspace/vpc > terragrunt plan
aws_vpc.this[0]: Refreshing state... [id=vpc-0d98d39c5a645c65f]
aws_default_security_group.this[0]: Refreshing state... [id=sg-0617b0ec3422dbc5]
No changes. Your infrastructure matches the configuration.
```

## Terragrunt Version Constraint Example

To restrict the Terragrunt binary, add `terragrunt_version_constraint`. The following example allows any version greater than `0.58.0` and up to `0.58.11`:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws//?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

inputs = {
  name = "KodeKloud-VPC"
  cidr = "10.100.0.0/16"
}

download_dir                  = "../.terragrunt-kodekloud"
prevent_destroy               = false
skip                          = false
iam_role                      = "arn:aws:iam::654645487009:role/terragrunt-role"
terraform_version_constraint  = "= 1.8.4"
terragrunt_version_constraint = "> 0.58.0, <= 0.58.11"
```

When your local Terragrunt is outside the specified range, all commands will fail:

```bash theme={null}
~/workspace/vpc > terragrunt -version
terragrunt version v0.58.12

~/workspace/vpc > terragrunt plan
ERROR[0000] The currently installed version of Terragrunt (0.58.12) is not compatible with the version Terragrunt requires (> 0.58.0, <= 0.58.11).
ERROR[0000] Unable to determine underlying exit code, so Terragrunt will exit with error code 1
```

> **triangle-alert** Locking to very specific versions can block legitimate upgrades. Plan your version bumps carefully and test in a staging environment.

## Links and References

* [Terraform Version Constraints](https://www.terraform.io/docs/language/expressions/version-constraints.html)
* [Terragrunt Configuration Reference](https://terragrunt.gruntwork.io/docs/reference/config-blocks/)
* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws)

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/1a2a45b4-e7d1-4af2-a897-7ebf83a4350e/lesson/990b6330-6327-4a96-8994-f8f26bce751b)


# Demo of Lab 1

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Basic-Concepts/Demo-of-Lab-1/page

This lesson guides you through installing Terraform 1.8.3 and Terragrunt 0.58.8 in your cloud shell and formatting your code.

Welcome to **Lab 1**! This lesson will guide you through installing Terraform 1.8.3 and Terragrunt 0.58.8 in your cloud shell. You’ll also learn how to format your Terraform and Terragrunt code.

When you open the lab, click **Open in VS Code** to launch the editor in a new browser tab. This allows you to copy and paste commands directly into the integrated terminal. Dismiss any initial prompts to get started.

![The image shows a split-screen view of a Visual Studio Code environment with instructions for opening a terminal and copying text, alongside a task prompt about using VS Code in a browser tab.](https://kodekloud.com/kk-media/image/upload/v1752884284/notes-assets/images/Terragrunt-for-Beginners-Demo-of-Lab-1/vs-code-terminal-instructions-task-prompt.jpg)

***

## Question 1: Install Terraform 1.8.3 and Verify the Version

The lab environment doesn’t include Terraform by default. Let’s confirm:

```bash theme={null}
terraform version
```

You should see:

```plaintext theme={null}
bash: terraform: command not found
```

Follow these steps to install Terraform 1.8.3:

| Step | Command / Action                                                                                                                            |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.   | Download the Terraform 1.8.3 ZIP (linux\_amd64):<br />`wget https://releases.hashicorp.com/terraform/1.8.3/terraform_1.8.3_linux_amd64.zip` |
| 2.   | Ensure `unzip` is installed:<br />`apt update && apt install -y unzip`                                                                      |
| 3.   | Unpack the archive:<br />`unzip terraform_1.8.3_linux_amd64.zip`                                                                            |
| 4.   | Make the binary executable and move it to `/usr/bin`:<br />`chmod +x terraform && mv terraform /usr/bin/`                                   |
| 5.   | Remove the ZIP file:<br />`rm terraform_1.8.3_linux_amd64.zip`                                                                              |
| 6.   | Verify the installation:<br />`terraform version`                                                                                           |

```bash theme={null}
