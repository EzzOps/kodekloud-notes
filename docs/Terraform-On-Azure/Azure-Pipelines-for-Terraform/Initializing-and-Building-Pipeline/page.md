# Initializing and Building Pipeline

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Pipelines-for-Terraform/Initializing-and-Building-Pipeline/page

Guide to building a production-grade Azure DevOps pipeline for Terraform using init, plan, and apply with separation, artifact plans, and gated approvals to enforce safe CI/CD practices

This lesson moves from concepts to implementation by building a production-grade Azure DevOps pipeline for Terraform. The pipeline follows CI/CD best practices: initialize the workspace, produce a safe reviewable plan, and gate destructive changes behind approvals before applying.

## Why `terraform init` runs first

`terraform init` prepares the working directory for all subsequent Terraform commands. It configures the backend, authenticates via the Azure DevOps service connection, downloads provider plugins, and sets up any required modules. Because hosted Azure DevOps agents are ephemeral, this initialization must run on every pipeline job unless you use a self-hosted agent with preinstalled providers and tooling.

Typical Azure DevOps task to run `init`:

```yaml theme={null}
- task: TerraformTask@5
  inputs:
    provider: 'azurerm'
    command: 'init'
    backendServiceArm: 'tf-01'
    backendAzureRmResourceGroupName: 'rg-kodekloud-demo-01'
    backendAzureRmStorageAccountName: 'sakodeklouddemotf'
    backendAzureRmContainerName: 'tfstate'
    backendAzureRmKey: 'demo.tfstate'
```

Important operational points:

* `backendServiceArm` should reference the Azure DevOps service connection with the appropriate permissions.
* The resource group, storage account, container, and key determine where the state file is stored. Remote state provides centralized state storage, state locking, and consistent execution across runs.
* Run `init` at the start of every pipeline job — before `plan` or `apply`.

## Terraform `plan` — the safe review step

`terraform plan` compares your configuration against the remote state, computes proposed changes, and outputs an execution plan without applying changes. In CI/CD, `plan` is the reviewable artifact that tells reviewers and automation exactly what will change.

Example `plan` task:

```yaml theme={null}
- task: TerraformTask@5
  inputs:
    provider: 'azurerm'
    command: 'plan'
    environmentServiceNameAzureRM: 'tf-01'
```

Best practices for `plan` in pipelines:

* Run `plan` automatically on every commit or PR to maintain visibility over intended changes.
* Persist the produced plan as an artifact so the exact plan can be consumed by the `apply` stage.
* Always run `plan` before any `apply`.

<Callout icon="lightbulb">
  Best practice: Run plans automatically (on every commit or PR) but gate `apply` with explicit approvals for non-development environments. This preserves visibility while limiting destructive actions.
</Callout>

## Plan vs Apply separation and approvals

Separation of `plan` and `apply` is an enterprise pattern that improves safety and governance:

* Automatically run `plan` for every pipeline execution (development, feature branches, PRs).
* Gate `apply` for test/UAT/production with human approvals or environment checks.
* Use Azure DevOps stage approvals, environments, and gates to enforce these controls.

<Frame>
  <img alt="The image displays a presentation slide about &#x22;Plan vs Apply Separation&#x22; with best practices, and an approvals settings panel from a software interface." />
</Frame>

## When to use plan separation

Implement plan/apply separation for:

* Test, UAT, and production environments — always require review/approval.
* Development environments — you may allow automated `apply` for rapid iteration, but track changes and revert controls.

## Terraform `apply` — execution phase

`terraform apply` executes the plan (or computes and applies changes), updates remote state, and uses state locking to prevent concurrent modifications. In pipelines, `apply` is typically run only after the plan has been reviewed and approved.

Example `apply` task:

```yaml theme={null}
- task: TerraformTask@5
  inputs:
    provider: 'azurerm'
    command: 'apply'
    commandOptions: '--auto-approve'
    environmentServiceNameAzureRM: 'tf-01'
```

Notes:

* `--auto-approve` is required for non-interactive pipelines but should only be used after an explicit approval gate.
* `apply` is production-impacting — restrict it to authorized runs and environments.

<Callout icon="warning">
  Warning: Never enable automated `apply` in production pipelines without a gated approval. `--auto-approve` will apply changes immediately and cannot prompt for interactive confirmation.
</Callout>

## Quick reference: init, plan, apply

| Command |                                                         Purpose | Typical pipeline inputs                             | Best practice                                       |
| ------- | --------------------------------------------------------------: | --------------------------------------------------- | --------------------------------------------------- |
| `init`  |               Prepare backend, download providers, authenticate | `backendServiceArm`, storage account/container/key  | Run at the start of every pipeline job              |
| `plan`  | Compare configuration to remote state and output execution plan | `environmentServiceNameAzureRM`, save plan artifact | Run on every commit/PR; produce artifact for review |
| `apply` |                         Execute changes and update remote state | `commandOptions: '--auto-approve'`, gated approvals | Require approvals for test/UAT/prod environments    |

## Conclusion

A robust Terraform pipeline follows a consistent sequence:

1. `terraform init` — initialize backend and providers.
2. `terraform plan` — produce a reviewable plan and persist it as an artifact.
3. `terraform apply` — execute the reviewed plan, only after approvals for protected environments.

By separating plan and apply and leveraging Azure DevOps approvals and environments, you maintain visibility, enforce governance, and reduce risk for infrastructure changes.

## Links and references

* [Terraform: Getting Started](https://www.terraform.io/intro)
* [Terraform CLI Documentation](https://developer.hashicorp.com/terraform/cli)
* [Azure DevOps Pipelines documentation](https://learn.microsoft.com/azure/devops/pipelines/)
* [Azure Provider for Terraform](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/66c0006d-c716-4381-8b15-e4edb4f4fbe5/lesson/1b6f2b55-57ac-447e-ae59-b23ae44e74a6" />
</CardGroup>
