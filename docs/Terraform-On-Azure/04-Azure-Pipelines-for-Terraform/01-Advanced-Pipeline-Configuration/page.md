# Advanced Pipeline Configuration

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Pipelines-for-Terraform/Advanced-Pipeline-Configuration/page

Configuring an Azure DevOps pipeline for Terraform that separates plan and apply, publishes immutable plan artifacts, and enforces manual approvals for safer auditable deployments.

In this lesson we implement an advanced Azure DevOps pipeline for Terraform that separates Plan and Apply into distinct stages, publishes the immutable plan as a pipeline artifact, and enforces a manual approval before applying that plan. This pattern improves auditability and safety by ensuring the exact plan that was reviewed is what gets applied.

Overview

* Plan stage: run `terraform init` and `terraform plan --out=...`, then publish the generated plan as a pipeline artifact.
* Apply stage: run as a `deployment` job tied to an Azure DevOps environment (with approval checks). The job downloads the plan artifact and runs `terraform apply` against the downloaded plan file.

Pipeline YAML (complete):

```yaml theme={null}
pool: Terraform
trigger: none

stages:
  - stage: Plan
    displayName: Terraform Plan
    jobs:
      - job: TerraformPlan
        displayName: Init & Plan
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
              commandOptions: '--out=$(Build.ArtifactStagingDirectory)/tfplan'
              environmentServiceNameAzureRM: 'tf-svc-01'

          - task: PublishPipelineArtifact@1
            displayName: Publish Plan Artifact
            inputs:
              targetPath: '$(Build.ArtifactStagingDirectory)/tfplan'
              artifactName: 'tfplan'

  - stage: Apply
    displayName: Terraform Apply
    dependsOn: Plan
    condition: succeeded()
    jobs:
      - deployment: TerraformApply
        displayName: Apply
        environment: 'terraform-approval'
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self
                - task: DownloadPipelineArtifact@2
                  displayName: Download Plan Artifact
                  inputs:
                    artifact: 'tfplan'
                    path: '$(Pipeline.Workspace)/tfplan'
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
                  displayName: Terraform Apply
                  inputs:
                    provider: 'azurerm'
                    command: 'apply'
                    commandOptions: '--auto-approve $(Pipeline.Workspace)/tfplan/tfplan'
                    environmentServiceNameAzureRM: 'tf-svc-01'
```

Stages at a glance

| Stage | Purpose                              | Key actions / artifacts                                                                                                                                                                                    |
| ----- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plan  | Produce an executable Terraform plan | `terraform init`, `terraform plan --out=` writes `$(Build.ArtifactStagingDirectory)/tfplan`, then `PublishPipelineArtifact@1` uploads it                                                                   |
| Apply | Apply an approved, immutable plan    | Deployment job to `environment: 'terraform-approval'`, `DownloadPipelineArtifact@2` downloads to `$(Pipeline.Workspace)/tfplan`, then `terraform apply --auto-approve $(Pipeline.Workspace)/tfplan/tfplan` |

Key points explained

* Structure
  * The pipeline uses top-level `stages:` containing `Plan` and `Apply`. Each stage has jobs, and jobs contain steps/tasks. Splitting Plan and Apply allows you to review and approve the exact plan that will be run.

* Plan stage
  * `terraform init` configures the backend and providers so Terraform can calculate changes.
  * `terraform plan` with `--out=$(Build.ArtifactStagingDirectory)/tfplan` produces a binary plan file on the agent. This file is required for deterministic apply and must be preserved beyond the job lifecycle.
  * `PublishPipelineArtifact@1` uploads that plan to Azure DevOps pipeline storage. Uploaded artifacts are associated with the pipeline run and are immutable for traceability.

* Artifact location and download
  * When published, the `tfplan` artifact is stored with the pipeline run and is immutable and traceable.
  * In Apply, `DownloadPipelineArtifact@2` retrieves the artifact into `$(Pipeline.Workspace)/tfplan`. The concrete plan file path becomes `$(Pipeline.Workspace)/tfplan/tfplan`, which is what `terraform apply` consumes.

* Apply stage and approvals
  * The Apply job is a `deployment` job scoped to an Azure DevOps environment `terraform-approval`. Environments support checks such as manual approvals; when configured, the deployment pauses until an approver releases it.
  * After approval, the job downloads the plan, runs `terraform init` again (to ensure backend/provider configuration on the agent), and applies the exact binary plan via `terraform apply --auto-approve <plan-file>`.

<Callout icon="lightbulb">
  Create an Azure DevOps environment named `terraform-approval` (or change the pipeline to reference an existing environment). Configure approvals and checks for that environment to enforce a manual approval gate before the Apply job runs.
</Callout>

The environment creation UI in Azure DevOps looks like this:

<Frame>
  <img alt="The image shows an Azure DevOps interface with a form to create a new environment, offering options for resources like Kubernetes and virtual machines." />
</Frame>

Sample Terraform changes (example HCL)

* Commit an HCL change to trigger Plan stage. Example Terraform configuration creating a resource group and storage account:

```hcl theme={null}
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-pipeline-resources"
  location = "East US"
}

resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacc4765746"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

Example pipeline console output excerpts

* Downloading artifact:

```text theme={null}
Starting: Download Artifact
=================================================================
Task                : Download pipeline artifact
Description         : Download a named artifact from a pipeline to a local path
Version             : 1.230.0
Author              : Microsoft Corporation
Help                : https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/download-pipeline-artifact
=================================================================
Download from the specified build: #7
Download artifact to: /home/azureuser/myagent/_work/1/
Downloading 1 pipeline artifacts...
```

* Terraform apply execution (abridged):

```text theme={null}
/usr/bin/terraform providers

Providers required by configuration:
.
├── provider[registry.terraform.io/hashicorp/azurerm]

/usr/bin/terraform apply --auto-approve /home/azureuser/myagent/_work/1/tfplan
azurerm_resource_group.example: Creating...
azurerm_resource_group.example: Still creating... [00s elapsed]
azurerm_resource_group.example: Still creating... [20s elapsed]
azurerm_resource_group.example: Creation complete after 25s [id=/subscriptions/.../resourceGroups/example-pipeline-resources]
azurerm_storage_account.example: Creating...
azurerm_storage_account.example: Creation complete after 15s [id=/subscriptions/.../storageAccounts/examplestorageacc4765746]
```

Disabling automatic runs

* The example pipeline uses `trigger: none` to disable CI. If you want CI back, adjust the `trigger` section to include branches or paths.

Final notes

* Using pipeline artifacts plus environment approvals provides a safe, auditable, and repeatable process: generate the plan once, keep it immutable, and only apply what was reviewed.
* Keep credentials and service connections minimal. Grant the service connection only the permissions required.

<Callout icon="warning">
  Ensure the Azure DevOps service connection `tf-svc-01` has the required permissions: access to the backend storage account/container and the target subscription/resource group for resource creation. Misconfigured permissions will cause backend init or apply failures.
</Callout>

Links and references

* Azure DevOps Pipelines: [https://docs.microsoft.com/azure/devops/pipelines/](https://docs.microsoft.com/azure/devops/pipelines/)
* Terraform CLI docs: [https://www.terraform.io/docs/cli/index.html](https://www.terraform.io/docs/cli/index.html)
* Azure Provider docs: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* PublishPipelineArtifact: [https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/publish-pipeline-artifact](https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/publish-pipeline-artifact)
* DownloadPipelineArtifact: [https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/download-pipeline-artifact](https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/download-pipeline-artifact)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/66c0006d-c716-4381-8b15-e4edb4f4fbe5/lesson/58e3a969-870c-4bb0-98bd-7ba796c58a54" />
</CardGroup>
