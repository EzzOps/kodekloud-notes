# Create a new Key Vault
az keyvault create \
  --name MyVault \
  --resource-group MyResourceGroup \
  --location eastus

# Store a secret
az keyvault secret set \
  --vault-name MyVault \
  --name AppSecret \
  --value s3cr3tValue

# Retrieve the secret
az keyvault secret show \
  --vault-name MyVault \
  --name AppSecret
```

> **lightbulb** Ensure your user or service principal has the `Key Vault Contributor` role or an equivalent access policy.

![The image is a slide titled "Implementing and Managing Secrets, Keys, and Certificates by Using Azure Key Vault," listing three topics: Exploring Azure Key Vault, Understanding Secrets, and Working With Keys.](https://kodekloud.com/kk-media/image/upload/v1752867973/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/implementing-managing-secrets-azure-key-vault.jpg)

### Access Control, Monitoring, and Best Practices

Secure your vault by defining access policies, enabling logging with Azure Monitor, and rotating keys regularly.

| Feature            | Description                                        |
| ------------------ | -------------------------------------------------- |
| Access Policies    | Grant or deny permissions at object level          |
| Diagnostic Logging | Capture read/write operations for audit and alerts |
| Key Rotation       | Automate renewal of keys and certificates          |

![The image is a slide titled "Implementing and Managing Secrets, Keys, and Certificates by Using Azure Key Vault," listing topics such as Access Policies, Monitoring and Logging, and Best Practices.](https://kodekloud.com/kk-media/image/upload/v1752867974/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/implementing-managing-secrets-azure-key-vault-2.jpg)

***

## Secrets in CI/CD Pipelines

Managing secrets in your build and release workflows is critical. Below is a quick comparison of GitHub Actions and Azure Pipelines secret stores:

| CI/CD Platform  | Secret Store                     | Reference in Pipeline |
| --------------- | -------------------------------- | --------------------- |
| GitHub Actions  | GitHub Encrypted Secrets         | `secrets.MY_SECRET`   |
| Azure Pipelines | Variable Groups & Key Vault Task | `$(MY_SECRET)`        |

### GitHub Actions Example

```yaml theme={null}
# .github/workflows/deploy.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Use GitHub Secret
        run: echo "API key is ${{ secrets.API_KEY }}"
```

### Azure Pipelines Example

```yaml theme={null}
# azure-pipelines.yml
variables:
  - group: KeyVaultVariables

steps:
  - task: AzureKeyVault@1
    inputs:
      azureSubscription: 'MyServiceConnection'
      KeyVaultName: 'MyVault'
      SecretsFilter: '*'
      RunAsPreJob: true
  - script: echo "Fetched secret: $(AppSecret)"
```

> **lightbulb** Use the Azure Key Vault task in Azure Pipelines to pull secrets at runtime rather than storing them statically.

![The image is a slide titled "Implementing and Managing Secrets in GitHub Actions and Azure Pipelines," listing four topics: understanding secrets in DevOps, managing secrets in GitHub Actions, secrets in Azure Pipelines, and best practices in GitHub Actions.](https://kodekloud.com/kk-media/image/upload/v1752867976/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/implementing-managing-secrets-github-azure.jpg)

***

## Service Connections in Azure Pipelines

Service connections let your pipelines authenticate to external systems such as Azure, GitHub, or container registries.

### Types of Service Connections

| Connection Type        | Use Case                                |
| ---------------------- | --------------------------------------- |
| Azure Resource Manager | Deploy to Azure subscriptions           |
| GitHub                 | Checkout or trigger workflows on GitHub |
| Docker Registry        | Push/pull container images              |

![The image is a slide titled "Using Service Connections in Pipeline," listing two topics: "Introduction to Service Connections in Azure Pipelines" and "Types of Service Connections."](https://kodekloud.com/kk-media/image/upload/v1752867977/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/using-service-connections-azure-pipelines.jpg)

### Configuring and Using Service Connections

```yaml theme={null}
# azure-pipelines.yml
resources:
  connections:
    - connection: MyAzureSubscription
      type: azureResourceManager
    - connection: MyGitHubConnection
      type: github

steps:
  - checkout: self
  - script: |
      az account show
      echo "Cloning via $(MyGitHubConnection)"
```

![The image is a slide titled "Using Service Connections in Pipeline," listing three topics: configuring GitHub service connections, using service connections in pipelines, and best practices for managing service connections.](https://kodekloud.com/kk-media/image/upload/v1752867978/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/using-service-connections-pipeline-slide.jpg)

***

## Conclusion

By centralizing your secrets in Azure Key Vault, integrating vault access into your CI/CD pipelines, and configuring secure service connections, you’ll build robust, compliant DevOps workflows. Implement these patterns to reduce risk and maintain operational excellence.

## Links and References

* [Azure Key Vault Documentation](https://docs.microsoft.com/azure/key-vault/)
* [GitHub Actions Encrypted Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)
* [Azure Pipelines Service Connections](https://docs.microsoft.com/azure/devops/pipelines/library/service-endpoints)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/2f8974b7-9aa9-46b8-a562-d7ed568269af/lesson/c13e0d3f-3eb8-4943-be34-eedbcb7e7f36)


# Summary

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Strategy-for-Managing-Sensitive-Information-in-Automation/Summary/page

This article reviews best practices for managing secrets, keys, and certificates in Azure DevOps, including Azure Key Vault and DevSecOps integration.

This article reviews the core concepts and best practices for managing secrets, keys, and certificates in Azure DevOps—covering Azure Key Vault essentials, DevSecOps secret integration, and Azure Pipelines service connections. These techniques align with AZ-400 exam objectives and real-world security requirements.

## Azure Key Vault Essentials

Azure Key Vault provides a secure, centralized store for secrets, keys, and certificates.

* **Purpose**\
  Securely store API keys, passwords, certificates, and cryptographic keys.

* **Access Policies**\
  Configure who can read, write, or manage vault objects.

* **Monitoring & Logging**\
  Integrate with Azure Monitor and Azure Activity Logs to audit access and changes.

* **Best Practices**
  * Enable **soft-delete** and **purge protection**
  * Enforce **role-based access control (RBAC)**
  * Regularly **rotate** and **audit** secrets

```bash theme={null}
