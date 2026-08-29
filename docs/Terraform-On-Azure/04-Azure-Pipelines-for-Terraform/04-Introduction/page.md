# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Pipelines-for-Terraform/Introduction/page

Guide to building production-ready Terraform CI/CD pipelines in Azure DevOps, using remote state, plan artifacts, separated plan and apply stages, approvals, and best practices for secure automated infrastructure delivery

In this lesson we implement Terraform CI/CD workflows in Azure DevOps using Azure Pipelines. We'll move from concept to a practical, production-ready pipeline pattern that emphasizes safety, control, and automation for infrastructure changes.

By the end of this lesson you will be able to:

* Initialize Terraform in a pipeline using a remote state backend.
* Run `terraform plan` inside CI to validate changes and produce an inspectable plan artifact.
* Separate plan and apply stages to enforce controlled deployments.
* Configure approval gates and environment checks to protect sensitive environments.
* Design and understand an end-to-end Terraform CI/CD pipeline in Azure DevOps that fits organizational governance and security requirements.

This lesson provides a reusable, production-oriented implementation pattern that you can adapt to your organization’s practices.

<Callout icon="lightbulb">
  Prerequisites: an [Azure DevOps project](https://learn.microsoft.com/azure/devops/?view=azure-devops), an [Azure service connection](https://learn.microsoft.com/azure/devops/pipelines/library/service-endpoints?view=azure-devops\&tabs=yaml) (or equivalent cloud provider connection), and a remote state backend such as an Azure Storage account or [Terraform Cloud](https://www.terraform.io/cloud). Ensure build agents have the [Terraform CLI](https://www.terraform.io/cli) available or use pipeline tasks that install Terraform. Keep secrets and backend credentials in secure pipeline variables or variable groups.
</Callout>

## High-level design

A production-ready pipeline separates validation from change. Typical stages are:

| Stage             | Purpose                                                  | Key actions / outputs                                                                       |
| ----------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Init & Format     | Ensure Terraform is initialized and formatted            | `terraform init` (with remote backend), `terraform fmt -check`                              |
| Validate & Plan   | Validate configs and produce an execution plan           | `terraform validate`, `terraform plan -out=tfplan`, publish `tfplan` as a pipeline artifact |
| Review (optional) | Human review of plan                                     | Inspect plan artifact; optionally use checklist or PR comments                              |
| Approvals         | Gate apply to protect critical environments              | Azure DevOps environment approvals or stage approvals                                       |
| Apply             | Execute the approved plan against the target environment | `terraform apply "tfplan"` using the previously generated plan artifact                     |

## Example Azure Pipelines YAML

Below is a concise example that demonstrates the recommended flow: init, plan (produces an artifact), and apply (deployed to an environment so approvals can be attached). Adapt paths, service connections, and backend configuration to your repository.

```yaml theme={null}
trigger:
  branches:
    include:
      - main

variables:
  TF_WORKING_DIR: infra
  TF_PLAN_FILE: tfplan

pool:
  vmImage: ubuntu-latest

stages:
  - stage: Plan
    displayName: 'Terraform Plan'
    jobs:
      - job: TerraformPlan
        displayName: 'Init, Validate, Plan'
        steps:
          - checkout: self

          # Authenticate to cloud provider using a service connection
          # For Azure: use AzureCLI@2 with a service connection or add cloud-specific login steps.
          - task: AzureCLI@2
            displayName: 'Login to Azure'
            inputs:
              azureSubscription: 'My-Azure-Service-Connection'
              scriptType: bash
              scriptLocation: inlineScript
              inlineScript: |
                echo "Logged into Azure for Terraform operations"

          - script: |
              cd $(TF_WORKING_DIR)
              # Initialize Terraform with backend config values provided via secure pipeline variables
              terraform init -input=false -backend-config="storage_account_name=$(TF_STATE_STORAGE)" -backend-config="container_name=$(TF_STATE_CONTAINER)" -backend-config="key=$(Build.BuildId).tfstate"
            displayName: 'terraform init (remote backend)'

          - script: |
              cd $(TF_WORKING_DIR)
              terraform fmt -check
              terraform validate
            displayName: 'terraform fmt & validate'

          - script: |
              cd $(TF_WORKING_DIR)
              terraform plan -input=false -out=$(TF_PLAN_FILE)
            displayName: 'terraform plan (output to tfplan)'

          - publish: $(TF_WORKING_DIR)/$(TF_PLAN_FILE)
            artifact: terraform-plan
            displayName: 'Publish terraform plan artifact'

  - stage: Apply
    displayName: 'Terraform Apply (requires approval)'
    dependsOn: Plan
    jobs:
      - deployment: TerraformApply
        displayName: 'Apply approved plan'
        environment: 'production' # Attach approvals/checks to this environment in DevOps UI
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: terraform-plan
                  displayName: 'Download plan artifact'

                - task: AzureCLI@2
                  displayName: 'Login to Azure for Apply'
                  inputs:
                    azureSubscription: 'My-Azure-Service-Connection'
                    scriptType: bash
                    scriptLocation: inlineScript
                    inlineScript: |
                      echo "Authenticated for apply"

                - script: |
                    cd $(TF_WORKING_DIR)
                    # Apply the exact plan file produced in the Plan stage
                    terraform apply -input=false "tfplan"
                  displayName: 'terraform apply using stored plan'
```

Notes about the example:

* Use secure pipeline variables or variable groups for sensitive values (storage account keys, backend secrets).
* The `environment: 'production'` line enables the use of environment-level approvals and checks in Azure DevOps (configure them in the UI).
* Publishing the plan artifact allows reviewers and auditors to inspect exactly what will change.

<Callout icon="warning">
  Never enable unattended `terraform apply` against production without proper approvals and checks. Always produce an immutable plan artifact (`terraform plan -out=...`) in CI and require either manual approval or an automated policy that validates the plan before applying.
</Callout>

## Implementation tips and recommended practices

* Always use a remote backend for state locking (for example, Azure Storage with blob locking) to avoid concurrent writes.
* Keep state backend credentials and sensitive variables in secure pipeline variable groups or Azure Key Vault.
* Produce and store plan artifacts in CI so changes are reviewable and auditable. You can also convert plans to JSON with `terraform show -json tfplan` for automated validation tooling.
* Prefer `deployment` jobs and `environment` targets in Azure DevOps for apply steps. This enables approvals, resource checks, and traceability.
* Use Terraform workspaces or separate state keys/directories per environment (dev, staging, prod) to isolate state.
* Consider running `terraform fmt -check` and `terraform validate` on pull requests to catch issues early.

## Links and references

* [Terraform CLI commands: plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
* [Azure Pipelines documentation](https://learn.microsoft.com/azure/devops/pipelines/?view=azure-devops)
* [Azure DevOps service connections](https://learn.microsoft.com/azure/devops/pipelines/library/service-endpoints?view=azure-devops\&tabs=yaml)
* [Remote state with Azure Storage](https://learn.microsoft.com/azure/storage/common/storage-account-overview)
* [Terraform Cloud](https://www.terraform.io/cloud)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/66c0006d-c716-4381-8b15-e4edb4f4fbe5/lesson/2b9bf0da-b546-4d65-bbcb-90f429c35100" />
</CardGroup>
