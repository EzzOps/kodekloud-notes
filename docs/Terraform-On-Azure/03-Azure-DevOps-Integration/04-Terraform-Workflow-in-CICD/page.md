# Terraform Workflow in CICD

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-DevOps-Integration/Terraform-Workflow-in-CICD/page

Guide to running Terraform in Azure DevOps CI/CD, covering plan review, approvals, remote state, secure service identities, and applying saved plans for auditable infrastructure deployments

This guide explains how Terraform is executed inside a CI/CD pipeline—covering the path from a developer commit to a production deployment. It describes the enterprise-grade workflow for Infrastructure as Code (IaC) using Terraform and Azure DevOps, including state management, plan review, approval gates, and secure execution.

## Why run Terraform in CI/CD?

Running Terraform inside CI/CD (instead of locally) ensures changes are:

* Auditable and versioned via Git.
* Consistently validated and formatted.
* Reviewed using the exact execution plan that will be applied.
* Applied by controlled service identities with least-privilege access.
* Safe from state corruption by using a shared remote backend and locking.

This approach reduces human error, prevents configuration drift, and provides a clear audit trail of what changed, when, and why.

## Developer workflow (high level)

1. Developers write Terraform code locally (resources, modules, variables).
2. They commit changes to a version-controlled repository (e.g., Azure Repos), which becomes the source of truth.
3. A CI/CD pipeline is triggered by the commit or a pull request.
4. The pipeline runs standardized validation, formatting, and planning steps, then publishes the generated plan as an artifact for reviewers.
5. After review and approval, the pipeline applies the saved plan using the pipeline agent and service connection (not from developer laptops).
6. Optionally promote using staged environments (dev → staging → production) with gates and automated tests between promotions.

## Typical pipeline stages and their purpose

| Stage     | Purpose                                                                 | Example commands                                               |
| --------- | ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| Validate  | Check init, formatting, and basic configuration correctness             | `terraform init`, `terraform fmt -check`, `terraform validate` |
| Plan      | Produce an execution plan and save it as an artifact for review         | `terraform plan -out=tfplan`                                   |
| Approvals | Manual or automated gates to review the plan artifact before applying   | Review `tfplan` artifact in Azure DevOps                       |
| Apply     | Use the saved plan to make changes in cloud using a controlled identity | `terraform apply -input=false tfplan`                          |

## Recommended production practices

| Practice                                                   | Benefit                                                  |
| ---------------------------------------------------------- | -------------------------------------------------------- |
| Remote backend (e.g., Azure Storage)                       | Shared persisted state outside agent machines            |
| State locking and concurrency controls                     | Prevent race conditions and state corruption             |
| Service principal or managed identity with least privilege | Secure, auditable pipeline permissions                   |
| Save and publish the `tfplan` artifact                     | Ensures reviewers can inspect the exact proposed changes |

> **warning** Enforce least-privilege on the service connection used by your pipeline. Avoid using broad contributor permissions; scope the identity to only the required resource groups and actions.

## Approval gates and plan review

Before applying changes to sensitive environments, require a plan review step. This is commonly implemented as:

* The Plan stage publishes the `tfplan` artifact.
* A reviewer (senior engineer or platform team) inspects the plan using `terraform show -no-color tfplan` or Azure DevOps artifact viewer.
* A manual approval gate (or an automated policy) allows or blocks the Apply stage.
* The Apply stage downloads the exact saved plan artifact and executes `terraform apply -input=false tfplan`.

This guarantees the pipeline applies exactly what was reviewed—no surprises or drift between review and execution.

## Local commands (for context)

Use these locally for development, formatting, and quick validation. Note: production changes should be applied through CI/CD.

```bash theme={null}
