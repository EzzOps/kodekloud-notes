# Install GPG key for the HashiCorp repository
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Add the HashiCorp repo for your distribution
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Update package lists and install Terraform
sudo apt-get update
sudo apt-get install -y terraform
```

For RHEL/CentOS, Fedora, SUSE, or other distributions, follow the corresponding steps in the official Terraform installation docs or use the generic ZIP binary to place `terraform` on your `PATH`.

Verify installation (common to all platforms)

```bash theme={null}
terraform version
```

You can also run:

```bash theme={null}
terraform --help
```

This displays common commands such as `init`, `validate`, `plan`, `apply`, and `destroy`.

Using Terraform from Azure Cloud Shell
If you need a quick environment without local installation, use Terraform from Azure Cloud Shell. Cloud Shell is a browser-based shell with Terraform pre-installed—ideal for demos, learning, and quick experiments.

<Frame>
  <img alt="The image is a three-step flowchart showing how to use Terraform via Azure Cloud Shell: Open Azure Cloud Shell, use pre-installed Terraform, and start using Terraform." />
</Frame>

To use Cloud Shell:

* Open the Azure portal and click the Cloud Shell icon in the top bar.
* If this is your first time, Cloud Shell prompts you to create or select a storage account (the portal can create one).
* When provisioned, a terminal session appears and Terraform is available immediately—no local install required.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface with options for Azure services and resources, along with a Cloud Shell terminal being connected at the bottom." />
</Frame>

<Callout icon="lightbulb">
  Azure Cloud Shell is great for quick tests, demos, or when you're away from your usual workstation. It is not recommended as the primary environment for production Terraform workflows—use CI/CD pipelines or local development environments for reproducible, auditable runs.
</Callout>

Common Terraform commands (summary)

| Command     |                                                            Purpose | Example                    |
| ----------- | -----------------------------------------------------------------: | -------------------------- |
| `init`      | Prepare working directory (download providers, initialize backend) | `terraform init`           |
| `validate`  |                        Validate configuration syntax and structure | `terraform validate`       |
| `plan`      |                      Show the proposed changes Terraform will make | `terraform plan`           |
| `apply`     |                      Apply changes to create/update infrastructure | `terraform apply`          |
| `destroy`   |                           Remove previously created infrastructure | `terraform destroy`        |
| `fmt`       |                                         Format configuration files | `terraform fmt`            |
| `output`    |                                            Read outputs from state | `terraform output`         |
| `state`     |                                 Advanced state management commands | `terraform state list`     |
| `workspace` |                                                  Manage workspaces | `terraform workspace list` |
| `version`   |                                             Show Terraform version | `terraform version`        |

Where to find the official instructions

* Terraform installation guide (HashiCorp): [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)
* Azure-specific Terraform docs: [https://learn.microsoft.com/azure/developer/terraform](https://learn.microsoft.com/azure/developer/terraform)

Next steps

* After installing Terraform, authenticate Terraform to Azure so you can manage Azure resources. Common authentication methods include:
  * Azure CLI (`az login`) for interactive sessions
  * Service principals for automation
  * Managed identities for Azure-hosted agents

Recommended workflows for Terraform in production (CI/CD, state backends, workspaces, and governance) are covered in separate guidance and best-practice documents.

Links and References

* [Terraform documentation — Install Terraform](https://developer.hashicorp.com/terraform/install)
* [Azure Cloud Shell documentation](https://learn.microsoft.com/azure/cloud-shell/overview)
* [Azure Terraform Provider docs](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/db2adc19-fa48-4b03-9d9a-8ef71c4c28db/lesson/33827f9f-94da-434d-b60b-fc4433c3925a" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Setting-up-environment/Introduction/page

Guides setting up a local environment, tools, and authentication to develop, validate, and deploy Terraform configurations for provisioning Azure resources.

Setting up the environment

Before writing any Terraform code, prepare a consistent local environment. This section outlines the essential tools and steps to develop, validate, and apply Terraform configurations for Azure.

An IDE such as Visual Studio Code improves productivity by providing HCL syntax highlighting, validation, auto-completion, and formatting. These features help reduce errors and make it easier to maintain Terraform code as projects grow.

Terraform relies on external tools to authenticate and communicate with Azure—most importantly, the Azure CLI.

<Frame>
  <img alt="The image is an introduction slide detailing steps for developing Terraform configurations, including selecting an IDE and installing dependencies for Azure." />
</Frame>

Installing these dependencies enables Terraform to securely connect to Azure subscriptions and manage resources without manual intervention.

Finally, the Terraform CLI is the primary tool used to initialize configurations, validate HCL, generate execution plans, and apply changes. Verify the CLI installation before proceeding with hands-on exercises.

## Required tools and quick checks

Use the table below to confirm the primary tools and common verification commands:

| Tool                              | Purpose                                              | Verify                      |
| --------------------------------- | ---------------------------------------------------- | --------------------------- |
| Visual Studio Code (or other IDE) | Edit HCL, linting, formatting                        | `code --version`            |
| Azure CLI                         | Authenticate and manage Azure subscriptions          | `az --version`              |
| Terraform CLI                     | Initialize, plan, and apply infrastructure           | `terraform version`         |
| Optional extensions               | VS Code Terraform extension, Azure Account extension | Check VS Code extensions UI |

Install links:

* [Terraform downloads](https://www.terraform.io/downloads)
* [Azure CLI installation](https://learn.microsoft.com/cli/azure/install-azure-cli)
* [Visual Studio Code](https://code.visualstudio.com/)

## Install and verify

Install the Azure CLI and Terraform CLI, then confirm they are available in your PATH:

```bash theme={null}
