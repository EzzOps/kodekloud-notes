# Verify Terraform installation
terraform -version
```

You should see Terraform's version and the installed provider plugin versions. If you see "command not found", confirm the binary is on your `PATH`.

## Editor: Visual Studio Code (recommended)

I recommend Visual Studio Code as a lightweight, extensible editor for Terraform HCL files.

Suggested extensions and formatting

* HashiCorp Terraform extension for syntax highlighting, snippets, and formatting: [https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
* EditorConfig and/or Prettier for consistent formatting (if your team uses them)
* Configure VS Code to run `terraform fmt` on save, or run formatting manually:

```bash theme={null}
terraform fmt
```

## Setting up cloud provider credentials

Terraform uses provider plugins to interact with cloud APIs. Before executing Terraform code that targets a cloud provider, configure credentials on the machine where you run Terraform.

Credential patterns and examples

| Provider | Typical local auth method                                                 | Environment variables / files                                                                                  |
| -------: | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
|      AWS | Configure AWS CLI or set env vars                                         | `~/.aws/credentials` via `aws configure`, or `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` |
|    Azure | Use `az login` for interactive sessions; service principal for automation | Service principal vars: `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`           |
|   GitHub | Create a Personal Access Token (PAT)                                      | Set `GITHUB_TOKEN` or `GH_TOKEN` in the environment, or use provider block config                              |

Examples and notes

* AWS: Run `aws configure` to create `~/.aws/credentials`. The Terraform AWS provider reads the default profile automatically; you can also specify a `profile` in the provider block.
* Azure: Run `az login` for interactive work. For CI/CD, create a service principal and export `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, and `ARM_TENANT_ID`.
* GitHub: Create a PAT with the minimum scopes required (for example, `repo` and `workflow`) and export it as `GITHUB_TOKEN` for use by the GitHub Terraform provider.

<Callout icon="lightbulb">
  When possible, prefer using CLI tools (for example `aws`, `az`) to authenticate locally and use environment variables or credential files for automation. This avoids hard-coding secrets in your Terraform configuration.
</Callout>

## Basic Terraform workflow checks

Once Terraform is installed and credentials are configured, validate your environment by running these commands inside an empty working directory (or a directory with your Terraform configurations).

1. Initialize the working directory (downloads providers and configures the backend):

```bash theme={null}
terraform init
```

2. Format and validate your configuration files:

```bash theme={null}
terraform fmt
terraform validate
```

3. Preview changes:

```bash theme={null}
terraform plan
```

4. Apply changes (prompts for confirmation by default):

```bash theme={null}
terraform apply
```

Quick verification checklist

| Command              | Purpose                                   | Expected result                                      |
| -------------------- | ----------------------------------------- | ---------------------------------------------------- |
| `terraform -version` | Confirms Terraform binary is installed    | Displays Terraform and provider plugin versions      |
| `terraform init`     | Fetches providers and initializes backend | Completed initialization without errors              |
| `terraform fmt`      | Formats HCL files                         | Files are formatted (or no changes)                  |
| `terraform validate` | Static validation of configs              | No errors reported                                   |
| `terraform plan`     | Shows proposed changes                    | Plan output lists resources to create/update/destroy |

<Callout icon="warning">
  Never commit provider credentials, personal access tokens, or other secrets to version control. Use environment variables, CLI-authenticated sessions, or a secrets manager for automation.
</Callout>

## Wrapping up

This lesson covered the essentials to prepare your machine for Terraform exercises:

1. Install Terraform (package manager or HashiCorp binary)
2. Configure a code editor (Visual Studio Code + extensions)
3. Set up cloud provider credentials (AWS, Azure, GitHub)
4. Verify the basic Terraform workflow (`init`, `fmt`, `validate`, `plan`, `apply`)

You're now ready to start the lab exercises. Begin by installing Terraform on your platform, then configure your editor and authenticate to your target cloud provider.

## Links and references

* Terraform downloads: [https://developer.hashicorp.com/terraform/downloads](https://developer.hashicorp.com/terraform/downloads)
* Visual Studio Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)
* HashiCorp Terraform VS Code extension: [https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
* AWS CLI configuration quickstart: [https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
* Azure CLI authentication: [https://learn.microsoft.com/cli/azure/authenticate-azure-cli](https://learn.microsoft.com/cli/azure/authenticate-azure-cli)
* GitHub PATs: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/df5b5815-c1ea-45f5-ba18-7a5c53ded28a/lesson/c15b7a1b-a0b7-40ab-982a-d1a3c660b57f" />
</CardGroup>


# Setting Up AWS Credentials for Terraform

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Preparing-Your-Environment/Setting-Up-AWS-Credentials-for-Terraform/page

Guide to creating an AWS IAM user, generating access keys, and configuring credentials for Terraform with example configuration and security best practices.

This guide walks through creating an IAM user in the AWS Management Console, generating programmatic credentials, and configuring those credentials so Terraform can authenticate to your AWS account.

Prerequisites:

* An AWS account and a user with permission to create IAM users and access keys.
* Terraform installed locally.
* (Optional) AWS CLI installed for managed credential storage.

1. Open the AWS Management Console

<Frame>
  <img alt="The image shows an AWS Console Home page, displaying a list of recently visited services and application management options, as well as sections for AWS Health, cost and usage, and getting started resources." />
</Frame>

2. Navigate to IAM

Open IAM from Recently visited services or type “IAM” in the top search box and open the IAM console.

<Frame>
  <img alt="The image shows an AWS Identity and Access Management (IAM) user interface with a list of users and details like last activity, password age, and console last sign-in times. There are navigation options for managing groups, roles, policies, and access reports on the left side." />
</Frame>

3. Create a new IAM user for Terraform

* Click “Users” in the left navigation, then “Create user”.
* Give the user a name (for example, `terraform`) — you can choose any naming convention you prefer.
* Enable programmatic access so AWS generates an access key ID and secret access key for the user.

<Frame>
  <img alt="The image displays the AWS IAM console where a user named &#x22;terraform&#x22; is being specified in the &#x22;Create user&#x22; process, within the &#x22;Specify user details&#x22; step. There are options for providing AWS Management Console access and generating programmatic access credentials." />
</Frame>

4. Attach permissions (least privilege recommended)

You can attach policies directly to the user on the permissions step. For the purposes of provisioning VPC resources (which typically do not incur charges), attach a managed policy that grants VPC permissions.

<Frame>
  <img alt="The image shows the AWS IAM (Identity and Access Management) console where a user is setting permissions by selecting policy options. There's a section for permission policies with various listed policies that can be attached to a new user." />
</Frame>

Search for “VPC” and choose **AmazonVPCFullAccess** (or attach `AdministratorAccess` only if you truly need full administrative scope). Limiting permissions to what Terraform requires is a best practice.

<Frame>
  <img alt="The image shows the AWS IAM console with a list of permission policies related to &#x22;VPC&#x22; being displayed. The policies are AWS managed, and none are currently attached to any entities." />
</Frame>

After creating the user, verify the policy is attached on the user’s permissions page.

<Frame>
  <img alt="The image shows an AWS Identity and Access Management (IAM) interface, specifically the user permissions page where &#x22;AmazonVPCFullAccess&#x22; is attached as a policy." />
</Frame>

5. Create an access key for programmatic access

Open the user’s “Security credentials” tab and create a new access key. You will receive an Access Key ID and a Secret Access Key. Copy and store them immediately — the Secret Access Key is shown only once.

<Frame>
  <img alt="The image shows the AWS Identity and Access Management (IAM) dashboard focused on security credentials, including options for multi-factor authentication, access keys, and SSH public keys." />
</Frame>

You may add a description or tags for the access key during creation.

<Frame>
  <img alt="The image shows a screen from the AWS console where a user can set a description tag for creating an access key, with instructions and options to proceed or cancel." />
</Frame>

6. Example Terraform configuration

If you don’t yet have any .tf files, save a minimal example (for instance `main.tf`) in your working directory before running `terraform plan`:

```hcl theme={null}
provider "aws" {}

resource "aws_vpc" "production" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "production"
  }
}

resource "aws_vpc" "dev" {
  cidr_block = "10.10.0.0/16"

  tags = {
    Name = "dev"
  }
}

resource "aws_subnet" "workloads" {
  vpc_id     = aws_vpc.production.id
  cidr_block = "10.1.0.0/24"

  tags = {
    Name = "workloads"
  }
}
```

<Callout icon="lightbulb">
  By default the empty `provider "aws" {}` block lets Terraform pick up credentials and the region from environment variables or the AWS shared credentials file. To set a region explicitly, add `region = "us-east-1"` inside the provider block (or configure `required_providers` if your Terraform workflow requires it).
</Callout>

7. Configure AWS credentials for Terraform

You can provide the Access Key ID and Secret Access Key to Terraform in multiple ways. Below are common approaches:

| Platform / Method                        |                                                                                                                                            Command / File | Notes                                                                                                              |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------ |
| macOS / Linux (bash, zsh) — session-only |       `bash export AWS_ACCESS_KEY_ID="AKIAEXAMPLEACCESSKEY" export AWS_SECRET_ACCESS_KEY="examplesecretKEY+chars" export AWS_DEFAULT_REGION="us-east-1" ` | Exports apply only to the current shell session. Persist in `~/.bashrc` or `~/.zshrc` if needed (beware security). |
| Windows PowerShell — session-only        | `powershell $Env:AWS_ACCESS_KEY_ID = "AKIAEXAMPLEACCESSKEY" $Env:AWS_SECRET_ACCESS_KEY = "examplesecretKEY+chars" $Env:AWS_DEFAULT_REGION = "us-east-1" ` | Session-only — values disappear when the shell closes.                                                             |
| AWS CLI (recommended for persistence)    |                                                                       Run `aws configure` and follow prompts (stores credentials in `~/.aws/credentials`) | Cross-platform managed file — safer than repeatedly exporting keys in shells. See AWS CLI docs below.              |

If you use the AWS CLI, run:

* `aws configure` — then enter Access Key ID, Secret Access Key, default region, and output format when prompted.

8. Verify Terraform and credentials

With credentials set and your `.tf` files in the working directory, run Terraform commands:

* `terraform init` to initialize providers.
* `terraform plan` to see what Terraform intends to create.

If you run `terraform plan` with no configuration files you will see the familiar message:

```bash theme={null}
$ terraform plan
Error: No configuration files

Plan requires configuration to be present. Planning without a configuration would mark everything for destruction, which is normally not what is desired. If you would like to destroy everything, run plan with the -destroy option. Otherwise, create a Terraform configuration file (.tf file) and try again.
```

Security best practices

* Use the principle of least privilege when attaching IAM policies.
* Prefer short-lived credentials or managed profiles when possible.
* Rotate or delete access keys when they are no longer required.

<Callout icon="warning">
  After you finish using these credentials, delete the access key in the IAM console (or rotate it). Treat access keys like passwords and follow the principle of least privilege.
</Callout>

Links and references

* [AWS IAM documentation](https://docs.aws.amazon.com/iam/)
* [AWS CLI configure quickstart](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
* [Terraform AWS Provider documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

This completes the setup for creating an IAM user and configuring AWS credentials for Terraform. Use `export` on macOS/Linux, `$Env:` for Windows PowerShell, or the AWS CLI `aws configure` command for persistent credentials.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/df5b5815-c1ea-45f5-ba18-7a5c53ded28a/lesson/885c3bca-859c-4ac9-8836-ecb3e10c9a70" />
</CardGroup>
