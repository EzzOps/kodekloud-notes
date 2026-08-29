# Remote Backend Usage in Pipelines

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-DevOps-Integration/Remote-Backend-Usage-in-Pipelines/page

Explains configuring Terraform remote state in Azure DevOps pipelines using Azure Blob Storage backend with RBAC and locking to secure and persist Terraform state across ephemeral CI/CD agents

In CI/CD pipelines, Terraform must store its state remotely. Local state files (for example, `terraform.tfstate`) cannot persist across ephemeral build agents such as `ubuntu-latest`, because each pipeline run creates and then destroys a fresh VM or container. If state were stored locally, subsequent pipeline runs would not see the existing infrastructure state — leading Terraform to recreate resources or fail with inconsistent state. This is risky for production environments and teams collaborating on the same infrastructure.

Below is a representative Azure DevOps pipeline snippet showing how to initialize Terraform with an Azure Storage backend. The task configures the AzureRM provider, runs the `init` command, and passes the service connection together with the storage account, container, and key to use for remote state:

```yaml theme={null}
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
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

This configuration instructs Terraform to store state in Azure Blob Storage rather than on the agent disk. The pipeline authenticates using the configured service connection (`backendServiceArm`) and connects to the storage account to read, write, and lock the remote state file. When [`terraform init`](https://www.terraform.io/cli/commands/init) runs in the pipeline:

* The pipeline authenticates using Entra ID / Azure AD (typically via a service principal or managed identity) associated with the service connection. See Azure AD docs: [https://learn.microsoft.com/en-us/azure/active-directory/](https://learn.microsoft.com/en-us/azure/active-directory/)
* Terraform reads the existing state from the specified blob container and key.
* Terraform attempts to acquire a state lock before modifications. The Azure Storage backend uses blob leases for locking: [https://learn.microsoft.com/en-us/rest/api/storageservices/lease-container](https://learn.microsoft.com/en-us/rest/api/storageservices/lease-container)

Why state locking matters

* CI/CD pipelines are ephemeral and multiple runs (or multiple engineers) can trigger concurrent Terraform applies.
* Without locking, simultaneous applies can corrupt state or leave resources in an inconsistent state.
* The Azure Storage backend leverages blob leasing so only one apply can modify the state at any time.

<Callout icon="warning">
  Never rely on ephemeral build agent disks to persist your Terraform state. Use a remote backend with locking to avoid state corruption and accidental resource recreation.
</Callout>

Typical backend setup in Azure

* Create a dedicated storage account for Terraform state and a private blob container (no public access).
* Limit access with RBAC so only the pipeline identity (service connection) or specific service principals have permissions.
* Enable blob versioning on the storage account to help recover from accidental or corrupted state updates.
* For multiple environments (dev/test/prod), isolate state by using separate containers, keys, or storage accounts — consider one backend per environment/workspace.

Recommended RBAC roles

| Role name                       | Purpose                                                                                                    |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `Storage Blob Data Contributor` | Grant to the pipeline identity to allow read/write/delete of blobs (typical minimum for state management). |
| `Storage Blob Data Reader`      | Read-only access for auditing or read-only operations.                                                     |
| `Contributor` / `Owner`         | Broad permissions — avoid unless strictly necessary. Prefer least privilege.                               |

Authentication approaches

* Avoid sharing storage account access keys. Historically some pipelines used `ARM_ACCESS_KEY` or similar environments, but this increases blast radius.
* Prefer Entra ID (Azure AD) authentication so the pipeline identity accesses the storage account via RBAC instead of a shared key: [https://learn.microsoft.com/en-us/azure/active-directory/](https://learn.microsoft.com/en-us/azure/active-directory/)
* Assign the pipeline identity the least-privilege role required. For state operations, granting `Storage Blob Data Contributor` on the storage account or the specific container is typical: [https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor)

Configuring access in the Azure portal

* Identify the storage account you want to use as the Terraform backend.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying a storage account named &#x22;lifecyclestorage75636&#x22; with an open blob container titled &#x22;reports.&#x22; The container has a private anonymous access level and is available for lease." />
</Frame>

* Verify the identity that the pipeline will use (for example, an application registration / service principal or managed identity).

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying the overview of an application registration. It includes details such as application IDs, client credentials, and options to manage the application setup." />
</Frame>

* In the storage account, open Access control (IAM), add a role assignment, and grant `Storage Blob Data Contributor` to the pipeline identity (the service principal or managed identity used by your Azure DevOps service connection).

<Frame>
  <img alt="This image shows a Microsoft Azure portal interface for adding a role assignment in Access Control (IAM) for blob storage. It includes sections for selecting roles, members, and conditions, with a searchable list of available roles." />
</Frame>

After assigning the role, the pipeline can authenticate via Entra ID and perform remote state operations (read, write, lock) against the blob container without requiring storage access keys.

Next steps and recommendations

* Configure the Terraform backend in the pipeline `init` step (example shown above) and confirm the service connection has the required RBAC role on the storage account or container.
* Structure environments to isolate state: use dedicated containers, distinct keys (for example: `dev.tfstate`, `prod.tfstate`), or separate storage accounts per environment.
* Enable storage blob versioning and consider a backup/retention policy to improve recovery options in case the state becomes corrupted.
* Audit access and rotate credentials for service principals; consider using managed identities where feasible to reduce secret management.

References and further reading

* Terraform CLI: init — [https://www.terraform.io/cli/commands/init](https://www.terraform.io/cli/commands/init)
* Azure Active Directory — [https://learn.microsoft.com/en-us/azure/active-directory/](https://learn.microsoft.com/en-us/azure/active-directory/)
* Storage Blob Data Contributor role — [https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor)
* Azure Blob leases for locking — [https://learn.microsoft.com/en-us/rest/api/storageservices/lease-container](https://learn.microsoft.com/en-us/rest/api/storageservices/lease-container)

<Callout icon="lightbulb">
  Using a dedicated, RBAC-protected storage account with Azure Blob versioning and Entra ID authentication gives you secure, durable, and recoverable Terraform state for CI/CD pipelines.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/70677d20-46be-4257-9a02-34aa382b3b05/lesson/cafab432-987d-4070-913b-0dfb01721aa3" />
</CardGroup>
