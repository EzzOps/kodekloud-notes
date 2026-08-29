# Executing Pipelines

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Pipelines-for-Terraform/Executing-Pipelines/page

Guides running Terraform via Azure DevOps pipelines from code commit to apply, covering agents, backend, YAML, approvals, and governance.

Now that the pipeline is authored, let's follow how it runs in a real-world CI/CD flow. Execution is more than running commands — it’s controlled infrastructure delivery with visibility, validation, and governance. This lesson walks through the lifecycle from code change to infrastructure deployment, showing the typical stages, required prerequisites, and example pipeline configuration for Azure DevOps.

The flow begins when a developer commits Terraform code to the repository — a new resource, a configuration tweak, a variable change, or a module upgrade. Treating infrastructure as code enables the same review, audit, and automation patterns used for application code.

A commit triggers the Azure DevOps pipeline. Triggers can be branch-based (for example, `main` or `dev`), pull-request-based, or manual. Azure DevOps provisions an agent (Microsoft-hosted or self-hosted) to run the pipeline job.

Typical pipeline sequence:

* Terraform init — connects to the remote backend, authenticates via the Azure service connection, downloads providers, and locks/prepares the state. If the backend is unreachable, init fails and the pipeline stops.
* Terraform plan — reads remote state, inspects current infrastructure, and produces an execution plan. This is a read-only validation step; it does not change Azure. In production pipelines, the plan is often saved as a binary artifact using `terraform plan -out=<planfile>` so reviewers apply the exact reviewed artifact.
* Approval — governance checkpoint where the plan is reviewed and risk is assessed. Azure DevOps supports manual approvals, environment checks, and role-based approvers.
* Terraform apply — applies the reviewed plan, updates remote state, and releases the state lock.

<Frame>
  <img alt="The image is a flowchart illustrating an end-to-end CI/CD process, detailing steps from &#x22;Code Commit&#x22; to &#x22;Terraform Apply.&#x22;" />
</Frame>

Prerequisites

Before running the pipeline end-to-end in Azure DevOps ensure you have:

* An Azure DevOps organization and project with a repository to store Terraform code.
* A build agent: Microsoft-hosted or self-hosted (see options below).
* A remote backend for Terraform state (example: Azure Storage account + container).
* An Azure DevOps service connection (Service Principal) with least-privilege permissions for the operations your pipeline will perform.

Repository setup

1. Create an Azure DevOps repository for your Terraform code.
2. If needed, generate Git credentials (Windows Credential Manager often handles this automatically; macOS/Linux can use a personal access token or SSH key).
3. Clone the repo locally, make a test change (for example, update `README.md`), commit and push to verify connectivity and confirm commits are tracked for audit purposes.

<Frame>
  <img alt="The image shows a screenshot of an Azure DevOps repository page titled &#x22;Terraform on Azure,&#x22; including options to clone the repository via HTTPS or SSH and instructions for pushing an existing repository." />
</Frame>

Open the repo in your IDE (e.g., Visual Studio Code), edit files, then commit and push. The repo will show the commit history and support code review workflows.

<Frame>
  <img alt="The image shows a Visual Studio Code interface with a README.md file open, displaying markdown instructions for introducing a Terraform project, including sections for Getting Started, Build and Test, and Contribute. The sidebar shows source control options and changes." />
</Frame>

Build agents

Build agents execute Terraform commands (init, plan, apply) in your pipeline. Choose between:

| Agent type       | Management                                     | When to use                                                                                           |
| ---------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Microsoft-hosted | Microsoft manages VMs and updates              | Low maintenance; prefer when you don't need custom tools or long-lived credentials                    |
| Self-hosted      | You manage a VM or container and install tools | Required if you need specific tooling, persistent credentials, or network access to private resources |

Key self-hosted requirements: Azure CLI, Terraform binary, Git, and any other tooling your pipeline needs.

<Frame>
  <img alt="The image shows an Azure DevOps interface with a repository named &#x22;Terraform on Azure&#x22; featuring a README.md file. The file includes sections for &#x22;Introduction to Terraform,&#x22; &#x22;Getting Started,&#x22; &#x22;Build and Test,&#x22; and &#x22;Contribute.&#x22;" />
</Frame>

Creating a self-hosted agent (example using an Azure VM)

1. Provision an Ubuntu VM in Azure. Configure VM name, resource group, region, size, and authentication (SSH).
2. SSH into the VM:

```bash theme={null}
ssh azureuser@<PUBLIC_IP>
```

3. Install Azure CLI (official Microsoft method for Debian/Ubuntu):

```bash theme={null}
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

4. Install Terraform (HashiCorp APT repository):

```bash theme={null}
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
```

5. Verify installations:

```bash theme={null}
az --version
terraform version
git --version
```

Install and configure the Azure DevOps agent on the VM:

* In Azure DevOps go to Project settings → Agent pools and create a new pool (for example, `Terraform`).
* Register an agent for Linux (or your OS), copy the agent package URL, then download, extract, configure, and run the agent on the VM.

Typical agent setup commands:

```bash theme={null}
mkdir myagent && cd myagent
wget https://vstsagentpackageurl -O ado.tar.gz
tar zxvf ado.tar.gz
./config.sh
./run.sh
```

During `./config.sh` you will:

* Accept license terms
* Enter server URL (e.g., `https://dev.azure.com/<ORG>/`)
* Provide a Personal Access Token (PAT) generated with agent registration scope
* Specify the agent pool name (e.g., `Terraform`)
* Choose an agent name (or accept the default)
* Save and run the agent: `./run.sh` — the agent will poll for jobs and run them when available.

<Frame>
  <img alt="The image shows a browser window with the Azure DevOps settings page, specifically the &#x22;Personal Access Tokens&#x22; section. A modal is open for creating a new personal access token, allowing customization of permissions and expiration settings." />
</Frame>

Marketplace extension

Install the Terraform extension (Terraform Tasks for Azure DevOps) from the Azure DevOps Marketplace to get prebuilt tasks and a tool installer. This simplifies YAML authoring by providing task templates for init/plan/apply.

<Frame>
  <img alt="The image is a screenshot of the Visual Studio Marketplace page for Terraform, an extension by Microsoft DevLabs, with installation details and features listed." />
</Frame>

Pipeline YAML

You can let Azure DevOps generate starter YAML or author your own. Example pipeline using the self-hosted pool `Terraform` and the official Terraform tasks:

```yaml theme={null}
trigger:
  branches:
    include:
      - main

pool: Terraform

steps:
  - task: TerraformTask@5
    displayName: Terraform Init
    inputs:
      provider: 'azurerm'
      command: 'init'
      backendServiceArm: 'tf-svc-01'
      backendAzureRmStorageAccountName: 'lifecyclestorage75636'
      backendAzureRmContainerName: 'pipeline'
      backendAzureRmKey: 'terraform.tfstate'

  - task: TerraformTask@5
    displayName: Terraform Plan
    inputs:
      provider: 'azurerm'
      command: 'plan'
      environmentServiceNameAzureRM: 'tf-svc-01'
      # Add plan-specific arguments here, e.g. -var or -var-file

  - task: TerraformTask@5
    displayName: Terraform Apply
    inputs:
      provider: 'azurerm'
      command: 'apply'
      environmentServiceNameAzureRM: 'tf-svc-01'
      additionalArgs: '-auto-approve'
```

Notes:

* `pool: Terraform` targets the self-hosted agent pool you created.
* `backendServiceArm` (for `init`) and `environmentServiceNameAzureRM` (for `plan`/`apply`) refer to the Azure service connection (example: `tf-svc-01`).
* The backend storage account/container/key are provided to the `init` task so the remote state is configured during pipeline execution.
* Remove the `trigger` block if you prefer to run pipelines manually (useful when approvals are required before execution).

> **warning** Using `-auto-approve` bypasses interactive confirmation. Ensure you have robust approvals and artifact-based plan reviews before enabling automatic apply in production.

Working Terraform files

Add your Terraform configuration to the repo. Example `main.tf` with a single resource group:

```hcl theme={null}
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-pipeline-resources"
  location = "eastus"
}
```

Declare the AzureRM backend in `backend.tf` (backend details will be provided by the pipeline):

```hcl theme={null}
terraform {
  backend "azurerm" {}
}
```

Commit and push these files. When the pipeline runs, Azure Repos will check out the repository into the agent working directory, and the Terraform tasks will run against that workspace.

Pipeline execution and output

When the pipeline runs on the self-hosted agent it performs:

* Checkout
* `terraform init` to configure the remote backend
* `terraform plan` to validate the changes
* Approval gates (if configured)
* `terraform apply` to create/update resources

Example trimmed output from the `apply` step:

```bash theme={null}
/usr/bin/terraform providers

Providers required by configuration:
└── provider[registry.terraform.io/hashicorp/azurerm]

/usr/bin/terraform apply --auto-approve

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_resource_group.example will be created
  + resource "azurerm_resource_group" "example" {
      + id       = (known after apply)
      + location = "eastus"
      + name     = "example-pipeline-resources"
    }

Plan: 1 to add, 0 to change, 0 to destroy.
azurerm_resource_group.example: Creating...
azurerm_resource_group.example: Creation complete after 2s [id=/subscriptions/xxxx/resourceGroups/example-pipeline-resources]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Agent logs show lifecycle activity such as registration, listening for jobs, and job completion:

```plaintext theme={null}
>> Connect:
Enter server URL = https://dev.azure.com/Kodekloud-ADO/
Enter authentication type (press enter for PAT) >
Enter personal access token > ***************
Connecting to server ...
>> Register Agent:
Enter agent pool (press enter for default) > Terraform
Enter agent name (press enter for vm-sha-01) >
Scanning for tool capabilities.
Successfully added the agent
Testing agent connection.
Enter work folder (press enter for _work) >
2026-02-13 21:51:14Z: Settings Saved.
./run.sh
Scanning for tool capabilities.
Connecting to the server.
2026-02-13 21:51:25Z: Listening for Jobs
2026-02-13 22:02:03Z: Running job: Job
2026-02-13 22:02:03Z: Job Job completed with result: Succeeded
```

Once complete, your Azure infrastructure matches the Terraform configuration and the remote state file is updated.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for creating a virtual machine, with options for availability zone, security type, image selection, VM architecture, and size." />
</Frame>

What’s next?

* Save the binary plan as a pipeline artifact and require that the exact plan artifact is applied to ensure auditable, deterministic changes.
* Add approvals, environment checks, and role-based approvers before `apply` to enforce governance.
* Harden self-hosted agents: apply least privilege, automate updates, and restrict network access; use Microsoft-hosted agents when possible to reduce maintenance.
* Extend pipeline tasks with linting (tflint), validation (terraform validate), and automated tests for modules (terratest).

> **lightbulb** Keep Terraform state in a secured remote backend and ensure your Azure service connection has the minimum required permissions for the operations your pipeline performs.

References

* Azure DevOps docs: [https://docs.microsoft.com/azure/devops](https://docs.microsoft.com/azure/devops)
* Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* Install Azure CLI on Linux: [https://learn.microsoft.com/cli/azure/install-azure-cli-linux](https://learn.microsoft.com/cli/azure/install-azure-cli-linux)

This completes an end-to-end example of running Terraform from Azure DevOps using a self-hosted agent. You now have a reproducible CI/CD flow from code commit to infrastructure apply, with checkpoints for visibility and governance.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/66c0006d-c716-4381-8b15-e4edb4f4fbe5/lesson/513335c4-aef9-4800-822e-74e042c9a553)
