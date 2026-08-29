# Create a new Key Vault with soft-delete enabled
az keyvault create \
  --name MyKeyVault \
  --resource-group MyResourceGroup \
  --location eastus \
  --enable-soft-delete true

# Add a secret to Key Vault
az keyvault secret set \
  --vault-name MyKeyVault \
  --name MySecret \
  --value "MySecretValue"
```

> **lightbulb** Enable **purge protection** to prevent accidental or malicious deletion of vault contents.

***

## Integrating Secret Management in DevSecOps Pipelines

Implement automated, secure retrieval of secrets in CI/CD workflows.

### 1. GitHub Actions

* Use the [Azure/login action](https://github.com/Azure/login) to authenticate.
* Fetch secrets from Key Vault at runtime.
* Apply [environment protection rules](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment).
* Rotate credentials on a regular schedule.

```yaml theme={null}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Fetch secret from Key Vault
        run: |
          az keyvault secret show \
            --vault-name MyKeyVault \
            --name MySecret
```

### 2. Azure Pipelines

* Link Key Vault as a **Variable Group**.
* Reference secrets in YAML or classic pipelines without exposing them in code.
* Turn on diagnostic logging for Key Vault access.

```yaml theme={null}
variables:
- group: KV-Secrets-Group

steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'MyServiceConnection'
    KeyVaultName: 'MyKeyVault'
    SecretsFilter: '*'
```

### 3. General Best Practices

* Enforce **least-privilege** for all identities and service principals.
* Rotate secrets, keys, and certificates at least every 90 days.
* Monitor access logs and trigger alerts on anomalous patterns.

> **triangle-alert** Always restrict service principal permissions to only the required Azure scopes. Overprivileged identities increase security risk.

***

## Azure Pipelines Service Connections

Service connections allow pipelines to authenticate with external systems without embedding credentials in code.

### Overview

Securely connect to Azure, GitHub, container registries, and third-party services.

### Types of Service Connections

| Service Connection Type          | Use Case                          | Example CLI Command                             |
| -------------------------------- | --------------------------------- | ----------------------------------------------- |
| Azure Resource Manager           | Deploy and manage Azure resources | `az devops service-endpoint azurerm create ...` |
| GitHub                           | Access GitHub repositories        | `az devops service-endpoint github create ...`  |
| Docker Registry / ACR            | Push/pull container images        | —                                               |
| Third-Party (SonarQube, Jenkins) | Integrate analysis and CI tools   | —                                               |

### Configuration Steps

1. In Azure DevOps, go to **Project Settings > Service connections**.
2. Click **New service connection** and select the type.
3. Provide authentication details (service principal, token, or PAT).
4. Assign the minimal required scope and permissions.
5. Validate and save the connection.

```bash theme={null}
# Example: Create a service connection via Azure CLI (ARM)
az devops service-endpoint create \
  --service-endpoint-configuration azurerm.json
```

### ARM Service Connection

* Use an existing or new service principal with a Contributor or custom role.
* Specify subscription ID, resource group, and scope.
* Test the connection before saving.

### GitHub Service Connection

* Authorize Azure DevOps via OAuth or provide a Personal Access Token (PAT).
* Limit repository permissions to only those needed for your pipelines.

![The image is a slide titled "Using Service Connections in Pipeline," listing topics related to Azure Pipelines and service connections, each marked with a colored dot.](https://kodekloud.com/kk-media/image/upload/v1752867979/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Summary/using-service-connections-pipeline-slide.jpg)

### Usage in Pipelines

Reference service connections in YAML tasks or classic releases:

```yaml theme={null}
steps:
- task: AzureCLI@2
  inputs:
    azureSubscription: 'MyServiceConnection'
    scriptType: bash
    scriptLocation: inlineScript
    inlineScript: az group list
```

### Best Practices

* Audit service connection permissions regularly.
* Adopt custom roles with just-enough permissions.
* Rotate service principal credentials and tokens on a scheduled basis.

***

## Links and References

* [Azure Key Vault Documentation](https://docs.microsoft.com/azure/key-vault/)
* [Azure DevOps Service Connections](https://docs.microsoft.com/azure/devops/pipelines/library/service-endpoints)
* [GitHub Actions for Azure](https://docs.github.com/actions/deployment/deploying-to-your-cloud-provider/deploying-to-azure)
* [AZ-400 Exam Guide](https://query.prod.cms.rt.microsoft.com/cms/api/am/binary/RE4vjQ0)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/2f8974b7-9aa9-46b8-a562-d7ed568269af/lesson/8153439c-3754-4c66-b4c9-f7cdb2bb1fc4)


# Using Service Connections in Pipeline

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Strategy-for-Managing-Sensitive-Information-in-Automation/Using-Service-Connections-in-Pipeline/page

Service connections in Azure DevOps enable secure authentication and interaction with external systems for CI/CD pipelines without exposing secrets.

Service connections in Azure DevOps enable your CI/CD pipelines to securely authenticate and interact with external systems—such as Azure subscriptions, GitHub repos, and container registries—without exposing secrets in your code. Mastering service connections is essential for both the AZ-400 exam and practical DevOps workflows.

![The image illustrates the flow of service connections in Azure Pipelines, showing the sequence from Azure Pipeline to Azure Resource Manager Service Connection, Service Principal, and Resource Group, with a role associated with the Service Principal.](https://kodekloud.com/kk-media/image/upload/v1752867980/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/azure-pipelines-service-connections-flow.jpg)

> **lightbulb** Service connections act like secure bridges, letting your pipelines authenticate against external services without hard-coding credentials.

## What Are Service Connections?

Service connections are configuration entries in Azure DevOps that store authentication details for external resources. Instead of embedding passwords, tokens, or keys in your scripts, you reference a service connection in your pipeline YAML or Classic definitions, and Azure DevOps handles the secure login.

![The image is an introduction to service connections in Azure Pipelines, showing a diagram with "Credentials," "Authentication Details," and "Service Connections" linked to "External services," along with the Azure DevOps logo.](https://kodekloud.com/kk-media/image/upload/v1752867981/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/azure-pipelines-service-connections-diagram.jpg)

## Benefits of Service Connections

* **Security**: Credentials are encrypted and stored centrally.
* **Maintainability**: Rotate or update credentials in one place.
* **Least Privilege**: Grant each connection only the permissions it needs.
* **Scalability**: Reuse connections across multiple pipelines and projects.

## Types of Service Connections

| Connection Type              | Use Case                                      | Example                               |
| ---------------------------- | --------------------------------------------- | ------------------------------------- |
| Azure Resource Manager (ARM) | Automate Azure resource deployments           | Deploy ARM templates via `AzureCLI@2` |
| GitHub                       | Pull code or trigger builds from GitHub repos | Clone with `checkout: self`           |
| Docker Registry              | Push and pull container images                | `docker push myrepo/myimage:latest`   |
| Kubernetes                   | Deploy to Kubernetes using kubeconfig or SA   | `kubectl apply -f deployment.yaml`    |
| Other (Bitbucket, Jenkins)   | Integrate with additional DevOps services     | Varies by service                     |

### Docker Connection

Enables pipelines to authenticate with Docker Hub or private registries for pulling base images and pushing built artifacts.

![The image describes a type of service connection, specifically Docker, which connects to Docker Hub or private Docker registries to pull and push container images.](https://kodekloud.com/kk-media/image/upload/v1752867982/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/docker-service-connection-hub-registries.jpg)

### Kubernetes Connection

Lets you deploy applications to Kubernetes clusters by providing a kubeconfig file or a service account token.

![The image describes a type of service connection involving Kubernetes, highlighting its ability to enable deployments to Kubernetes clusters using kubeconfig files or service accounts.](https://kodekloud.com/kk-media/image/upload/v1752867983/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/kubernetes-service-connection-deployments.jpg)

Azure DevOps supports many more connection types—always pick the one best aligned with your service.

## Creating a Service Connection

1. In Azure DevOps, select the **gear icon** (Project Settings) in the lower-left corner.
2. Under **Pipelines**, click **Service Connections**.
3. Hit **New Service Connection** and choose the desired type.

![The image is a step in a guide titled "Creating a Service Connection," instructing users to go to the project settings in their Azure DevOps project.](https://kodekloud.com/kk-media/image/upload/v1752867984/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/creating-service-connection-azure-devops.jpg)

4. Complete the authentication form with credentials or OAuth details.

![The image shows a step in creating a service connection, specifically providing details like authentication method and credentials, with a form for a new NuGet service connection.](https://kodekloud.com/kk-media/image/upload/v1752867986/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/nuget-service-connection-authentication-form.jpg)

5. Test the connection and save it under a clear, descriptive name for use in your pipeline definitions.

## Setting Up an Azure Resource Manager Connection

1. Select **Azure Resource Manager** as the connection type.
2. Choose **Service Principal** authentication to enforce least-privilege access.
3. Enter your Service Principal ID, Key, and Tenant ID from Azure AD.

![The image shows a configuration screen for setting up an Azure Resource Manager (ARM) connection, with options for selecting an authentication method such as service principal or workload identity federation.](https://kodekloud.com/kk-media/image/upload/v1752867987/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/azure-arm-connection-configuration-screen.jpg)

4. Pick the target Azure subscription and optionally scope down to a specific resource group.

![The image shows a step in configuring an Azure Resource Manager (ARM) connection, specifically selecting the Azure subscription and optionally the resource group. It includes a screenshot of the "New Azure service connection" dialog box with options for scope level and fields for service connection name and description.](https://kodekloud.com/kk-media/image/upload/v1752867988/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/azure-arm-connection-configuration-screenshot.jpg)

5. Confirm that the Service Principal has only the permissions required for your deployment tasks.

## Setting Up a GitHub Connection

* Choose **GitHub** from the service connection list.
* Authenticate via **OAuth** or **Personal Access Token (PAT)**:
  * OAuth automatically grants permission through a consent screen.
  * PAT lets you configure fine-grained scopes—create it in GitHub and paste the token into Azure DevOps.
* Test and save the integration under a memorable name.

## Using Service Connections in Pipelines

Reference service connections in YAML or Classic pipelines. Below is an example using the Azure CLI task in YAML:

```yaml theme={null}
jobs:
- job: deploy
  pool:
    vmImage: 'ubuntu-latest'
  steps:
    - task: AzureCLI@2
      inputs:
        azureSubscription: 'My-ARM-Service-Connection'
        scriptType: 'bash'
        scriptLocation: 'inlineScript'
        inlineScript: |
          az login --service-principal \
                   -u $(clientId) \
                   -p $(clientSecret) \
                   --tenant $(tenantId)
```

### Deploying an ARM Template

```yaml theme={null}
trigger:
  branches:
    include:
      - main
pool:
  vmImage: 'ubuntu-latest'
steps:
  - task: AzureResourceManagerTemplateDeployment@3
    inputs:
      azureSubscription: 'ARM-Service-Connection'
      resourceGroupName: 'myResourceGroup'
      location: 'West US'
      templateLocation: 'Linked artifact'
      csmFile: 'templates/template.json'
      csmParametersFile: 'templates/parameters.json'
```

This task uses your ARM service connection to deploy resources defined in your template and parameters files without exposing credentials.

## Best Practices for Managing Service Connections

1. Audit connections periodically and remove unused entries.
2. Follow the **least privilege** principle—grant only necessary permissions.
3. Rotate credentials on a regular schedule.
4. Document each connection’s purpose and scope for team transparency.

![The image outlines best practices for managing service connections, including regular audits, least privilege principle, documentation, and rotation of credentials. It features a central icon with a thumbs-up and ribbon, surrounded by these four practices.](https://kodekloud.com/kk-media/image/upload/v1752867989/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Using-Service-Connections-in-Pipeline/service-connections-best-practices-diagram.jpg)

> **triangle-alert** Failing to rotate or audit credentials may lead to unauthorized access and compliance risks. Schedule regular reviews.

## Links and References

* [Azure Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
* [AZ-400 Exam Guide](https://learn.microsoft.com/certifications/exams/az-400)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/2f8974b7-9aa9-46b8-a562-d7ed568269af/lesson/67bffc6c-030b-444f-8f8e-9ecfd23b49d4)
