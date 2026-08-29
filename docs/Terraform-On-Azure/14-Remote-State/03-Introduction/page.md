# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Remote-State/Introduction/page

Guide to using Azure Blob Storage as a Terraform remote backend, covering initialization, state migration, locking, common failures, recovery steps, and best practices for teams and CI pipelines.

In this lesson we cover Terraform remote state: what it is, why you need it when multiple people or automated pipelines manage the same infrastructure, how to use Azure Storage as a centralized backend, how `terraform init` configures and migrates state, and common remote-state failure scenarios with recovery steps.

> **lightbulb** This guide focuses on Azure Blob Storage as a Terraform backend, explains initialization and migration behavior, and summarizes common failure modes and mitigation steps. Use it as an operational checklist when configuring remote state for team and CI/CD workflows.

What you'll learn in this lesson/article:

* Why remote state is essential for collaboration and CI/CD.
* How a backend (Azure Storage) stores Terraform state and provides locking and durability.
* What `terraform init` does: backend configuration, state creation, and migration behavior.
* Common failure modes (permissions, locking, networking, corrupted state) and remediation steps.

***

## Why remote state matters

Terraform keeps the current representation of managed infrastructure in a state file. When multiple users or automation systems modify the same resources, storing state locally leads to:

* Conflicts and race conditions during concurrent operations.
* Diverging views of infrastructure and drift between environments.
* Increased risk of accidental resource deletion or duplication.

A remote backend centralizes state to provide:

* A single authoritative source-of-truth for resource state.
* Locking to prevent concurrent writes that corrupt state.
* Centralized access control, audit logs, and encryption when supported by the cloud provider.

***

## Benefits of using a remote backend

| Benefit                         | Description                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------ |
| Centralized storage and history | State file stored in one place with versioning and history for recoverability. |
| State locking                   | Prevents concurrent writes and reduces the chance of corruption.               |
| Access control & auditing       | Leverage cloud provider IAM and logging for centralized governance.            |
| Encryption                      | Backend providers often offer encryption at rest and in transit.               |
| Team and CI/CD collaboration    | Consistent state for developers and automation pipelines.                      |

***

## Using Azure Storage as a Terraform backend

Azure Blob Storage is a common, supported backend for Terraform. When using Azure as a backend, the typical components you provision are:

| Component       | Purpose                                                                              |
| --------------- | ------------------------------------------------------------------------------------ |
| Storage account | Holds the blob container where the state file is stored.                             |
| Blob container  | Container to store the Terraform state file(s).                                      |
| Access control  | Use storage keys, `SAS` tokens, or managed identities to authenticate access.        |
| Blob leases     | Azure blob leases are used to implement state locking and prevent concurrent writes. |

Useful links:

* Azure Blob Storage overview: [https://learn.microsoft.com/en-us/azure/storage/blobs/](https://learn.microsoft.com/en-us/azure/storage/blobs/)
* SAS tokens: [https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview)
* Managed identities: [https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
* Blob leases (locking): [https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-lease](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-lease)

Example backend configuration for Azure (place this in your Terraform configuration):

```hcl theme={null}
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

Notes:

* `key` is the path/name of the state file inside the container; use environment/branch naming conventions to isolate environments (e.g., `dev/terraform.tfstate`, `prod/terraform.tfstate`).
* Choose authentication that fits your automation: storage account keys or SAS for CI pipelines, and managed identities for Azure-hosted automation or interactive Azure CLI sessions.

***

## Initializing and migrating state with `terraform init`

`terraform init` performs backend configuration and prepares local working directory components (modules, providers). When you add or change a backend configuration, `terraform init` is the command that reconciles local and remote state.

Behavior to expect:

* If local state exists and your configuration specifies a remote backend, Terraform will prompt to migrate local state to the remote backend.
* If remote state already exists at the configured backend key, Terraform uses that remote state as authoritative.
* To change backend configuration without accepting migration prompts, use `terraform init -reconfigure`.

Typical usage:

```bash theme={null}
