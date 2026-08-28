# Introduction

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Strategy-for-Managing-Sensitive-Information-in-Automation/Introduction/page

Learn to secure sensitive data in DevOps pipelines using Azure Key Vault, GitHub Actions, and Azure Pipelines best practices.

In this module, you’ll learn how to secure sensitive data—secrets, keys, and certificates—in your DevOps automation pipelines. We’ll focus on best practices for Azure Key Vault, GitHub Actions, and Azure Pipelines so you can confidently manage credentials and cryptographic materials in production environments.

<Callout icon="triangle-alert">
  Never store secrets or certificates in plaintext within your code repositories. Always leverage a secure vault or secrets store.
</Callout>

***

## Azure Key Vault

Azure Key Vault is a cloud-hosted service that centralizes the storage and management of secrets, keys, and certificates. You can apply fine-grained access policies, enable detailed logging, and integrate with other Azure services.

### Key Vault Components

| Component   | Description                                   | Example                          |
| ----------- | --------------------------------------------- | -------------------------------- |
| Secret      | Passwords, API keys, connection strings       | `az keyvault secret set …`       |
| Key         | Cryptographic keys for encryption and signing | `az keyvault key create …`       |
| Certificate | Managed X.509 certificates                    | `az keyvault certificate create` |

### Quickstart with Azure CLI

```bash theme={null}
