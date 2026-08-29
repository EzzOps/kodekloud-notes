# Initialize backend and providers
terraform init

# Check formatting
terraform fmt -check

# Validate configurations
terraform validate

# Create a plan file that can be reviewed and applied by the pipeline
terraform plan -out=tfplan

# (Locally) inspect the plan
terraform show -no-color tfplan

# Apply an existing plan file
terraform apply -input=false tfplan
```

## Example Azure DevOps pipeline (simplified)

This YAML demonstrates separation of Validate, Plan, and Apply stages. The Plan stage publishes the `tfplan` artifact and the Apply stage uses an environment (which can be protected with approvals in Azure DevOps).

```yaml theme={null}
trigger:
  branches:
    include:
      - main

stages:
  - stage: Validate
    jobs:
      - job: Validate
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - script: |
              terraform init -backend-config="storage_account_name=${{ variables.storageAccount }}" -backend-config="container_name=${{ variables.container }}" -backend-config="key=${{ variables.key }}"
              terraform fmt -check
              terraform validate
            displayName: 'Terraform Init, Fmt, Validate'

  - stage: Plan
    dependsOn: Validate
    jobs:
      - job: Plan
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - script: |
              terraform init -backend-config="storage_account_name=${{ variables.storageAccount }}" -backend-config="container_name=${{ variables.container }}" -backend-config="key=${{ variables.key }}"
              terraform plan -out=tfplan
            displayName: 'Terraform Init and Plan'
          - publish: tfplan
            artifact: terraform-plan

  - stage: Apply
    dependsOn: Plan
    condition: succeeded()
    jobs:
      - deployment: Apply
        displayName: 'Apply to Production (requires approval)'
        environment: 'production' # Protect this environment with approval gates in Azure DevOps
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: terraform-plan
                - script: |
                    terraform init -backend-config="storage_account_name=${{ variables.storageAccount }}" -backend-config="container_name=${{ variables.container }}" -backend-config="key=${{ variables.key }}"
                    terraform apply -input=false tfplan
                  displayName: 'Terraform Apply (using saved plan)'
```

> **lightbulb** Always save and publish the exact `tfplan` produced by the plan stage and use that saved plan in the apply stage. This ensures reviewers are approving the exact changes that will be applied, preventing drift between review and execution.

<Frame>
  <img alt="The image depicts a DevOps workflow involving a user creating infrastructure as code, storing it in Azure Repos, and passing it through a CI/CD pipeline with approvers, leading to testing, production, planning, and application stages." />
</Frame>

## Summary

Running Terraform in CI/CD with remote state, state locking, controlled service identities, saved plan artifacts, and approval gates delivers a robust, auditable, and repeatable IaC workflow. This reduces risk, enforces review and compliance, and provides a reliable promotion path from development to production.

## Links and references

* [Terraform documentation](https://www.terraform.io/docs)
* [Azure DevOps pipelines](https://docs.microsoft.com/azure/devops/pipelines/)
* [Azure Storage as Terraform backend](https://www.terraform.io/language/settings/backends/azurerm)
* [Best practices for Terraform in CI/CD](https://www.terraform.io/docs/cloud/vs/cli.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/70677d20-46be-4257-9a02-34aa382b3b05/lesson/d3fe959a-9563-4929-8faa-74d7128732ea)


# Why CICD for Terraform

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-DevOps-Integration/Why-CICD-for-Terraform/page

Explains why CI/CD is essential for running Terraform in team and production environments, detailing pipeline stages, governance, secrets management, approvals, and auditability.

Before diving into pipelines, let’s clarify the problem CI/CD solves.

Terraform can be run locally, but production infrastructure requires more than a developer running `terraform apply` on their laptop. In a team or enterprise setting you need consistent execution, traceability, and governance. The diagram below shows a typical enterprise workflow and why CI/CD is essential.

At the bottom is an engineer working in a local Git repository. They author Terraform code, commit it, and push to a centralized repo (for example, Azure DevOps). Pushing code triggers the CI pipeline, which prepares and validates the changes; after CI succeeds, the CD pipeline applies approved changes to the cloud provider (Azure in this example).

<Frame>
  <img alt="The image is a diagram illustrating a CI/CD workflow using Terraform and Azure, highlighting the importance of consistency, auditability, controlled changes, and team collaboration in production infrastructure. It shows a process from local git repo code commit to the deployment of resources in Azure." />
</Frame>

> **lightbulb** CI/CD provides consistency, repeatability, and an auditable trail—turning ad-hoc infrastructure changes into governed, reviewable, and reproducible operations.

What does CI do for Terraform?

CI automates the preparation and verification steps so every commit is treated uniformly. Typical CI stages for Terraform include:

* `terraform init` — configures backend, downloads providers and modules.
* `terraform validate` — checks syntax and internal consistency.
* `terraform plan` — produces an execution plan that shows proposed changes.

These steps ensure plugins and modules are initialized, configuration is validated, and a clear plan is produced that reviewers can inspect before any changes reach production.

CI tasks and their purpose:

| CI Task                          | Purpose                                           | Typical Command      |
| -------------------------------- | ------------------------------------------------- | -------------------- |
| Initialize backend and providers | Ensures consistent provider and module resolution | `terraform init`     |
| Validate configuration           | Catches syntax and structural issues early        | `terraform validate` |
| Produce an execution plan        | Shows exactly what will change for review         | `terraform plan`     |

Once CI finishes and reviewers approve the plan, CD performs the guarded `terraform apply`. The result is a separation of responsibilities:

* Developers write and version infrastructure code,
* Pipelines execute and enforce the delivery process,
* Azure (or another cloud) receives the validated deployment.

This removes the need for developers to have direct production access from their local machines.

Why CI/CD matters (short list):

* Consistency: Pipelines fix the Terraform version, provider versions, and command order so results are repeatable.
* Auditability: Runs, logs, and archived plans provide a searchable history of what changed, when, and by whom.
* Change governance: PRs, automated plan generation, and approval gates enforce review workflows before apply.
* Team collaboration: Infrastructure becomes part of the normal code review and delivery lifecycle.

Without CI/CD, an engineer could bypass gates and run `terraform apply` locally, creating risk and reducing traceability. Pipelines transform changes into controlled, auditable events.

Credentials and secrets

Store credentials centrally in your CI/CD system—use Azure DevOps service connections or service principals with secrets kept in the pipeline secret store. Where possible prefer managed identities to avoid long-lived credentials on machines.

> **warning** Do not embed secrets in code or store long-lived credentials on developer machines. Centralize secrets in your pipeline or use managed identities to minimize operational risk.

Before the CD stage performs `terraform apply`, require approvals (manager, security, or change board) as appropriate. The recommended sequence is: plan → review → approve → apply. This preserves automation benefits while maintaining control.

<Frame>
  <img alt="The image is a diagram illustrating CI/CD pipelines, highlighting features like repeatable execution, centralized credentials, approval gates, and safe automation, alongside a CI/CD process involving code repositories, builds, and releases using Terraform and Azure." />
</Frame>

When should you use CI/CD for Terraform?

Use CI/CD when the environment or organizational needs demand consistency, traceability, and governance. Common scenarios:

| Scenario                   | Why CI/CD is recommended                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| Team environments          | Standardizes execution, reduces merge conflicts, and provides shared visibility            |
| Production environments    | Ensures stability, traceability, and approval workflows for safe deployments               |
| Regulated/audited settings | Provides demonstrable change control required by ISO, SOC, HIPAA, or financial regulations |

<Frame>
  <img alt="The image illustrates a continuous integration and continuous deployment (CI/CD) pipeline using a local Git repository, Azure, and Terraform, indicating environments suitable for team collaboration, production, and regulated or audited settings." />
</Frame>

CI/CD pipelines give you reproducible runs, centralized secrets, approval gates, and audit logs—everything needed for production-grade infrastructure delivery. Running Terraform locally remains useful for learning and experimentation, but for any shared, production, or audited environment, CI/CD is not optional—it’s mandatory for safe, repeatable infrastructure operations.

Links and references

* [Terraform](https://www.terraform.io/)
* [Azure DevOps](https://azure.microsoft.com/services/devops/)
* Azure DevOps service connections: `https://learn.microsoft.com/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml`
* Service principals: `https://learn.microsoft.com/azure/active-directory/develop/app-objects-and-service-principals`
* Managed identities: `https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview`
* Compliance references: [ISO](https://www.iso.org/), [SOC](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/soc-for-service-organizations.html), [HIPAA](https://www.hhs.gov/hipaa/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/70677d20-46be-4257-9a02-34aa382b3b05/lesson/58a7527e-8714-4d90-a8d8-4e6bb3c8ef93)
