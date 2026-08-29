# Authenticating to Azure

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Setting-up-environment/Authenticating-to-Azure/page

Explains how Terraform authenticates to Azure using Azure CLI, service principals, and managed identities with setup steps and best practices for secure, least privilege access

Terraform does not manage Azure resources directly; it talks to the Azure Resource Manager (ARM) API to create, update, and delete resources. Every call to ARM must be authenticated (who is making the request) and authorized (what the identity is allowed to do). Azure validates identities using Microsoft Entra ID and issues access tokens that Terraform’s Azure Provider uses for each API call.

Terraform supports multiple authentication methods because it can run in different environments. All methods ultimately use Microsoft Entra ID, but the way credentials or tokens are acquired differs:

* Azure CLI (best for local development)
* Service Principal (typical for CI/CD automation)
* Managed Identity (recommended for workloads running inside Azure)

Below we walk through each authentication method with example commands and recommended practices.

<Frame>
  <img alt="The image outlines three ways of authenticating to Azure: using Azure CLI, using Service Principal, and using managed identity." />
</Frame>

## How authentication works (quick overview)

* Terraform requests an access token from Microsoft Entra ID.
* The Provider includes that token in API calls to ARM.
* ARM validates the token and enforces RBAC permissions assigned to that identity.

Choose an authentication method based on where Terraform runs:

* Local machine or laptop → Azure CLI
* CI/CD pipelines → Service principal
* Azure-hosted VMs, App Services, or other resources → Managed identity

## Quick comparison

| Method            | Best for                  | Credentials stored where    | Typical setup                                      |
| ----------------- | ------------------------- | --------------------------- | -------------------------------------------------- |
| Azure CLI         | Local development & demos | Local Azure CLI token cache | `az login`                                         |
| Service Principal | CI/CD and automation      | Client secret / certificate | `az ad sp create-for-rbac` + environment variables |
| Managed Identity  | Azure-hosted workloads    | No customer-managed secrets | Assign identity and RBAC to the Azure resource     |

## 1) Azure CLI (az login)

The Azure CLI authenticates a user via Microsoft Entra ID and caches an access token locally. The Terraform Azure Provider detects the cached session and reuses the token for ARM API calls. The permissions used by Terraform are the role assignments of the signed-in user.

Example: authenticate locally

```bash theme={null}
az login
```

<Callout icon="lightbulb">
  Use `az login` for interactive development, learning, and demos. Avoid using it for production automation because it uses your user identity, which may have broader permissions than necessary.
</Callout>

Notes:

* If you use multiple subscriptions, set the active subscription with `az account set -s <SUBSCRIPTION_ID>`.
* For headless CI scenarios, prefer a service principal instead of `az login`.

## 2) Service Principal

A service principal is an application identity in Microsoft Entra ID and is commonly used for automation and CI/CD. It provides a dedicated identity with scoped RBAC permissions.

Create a service principal and assign it an RBAC role scoped to a subscription or resource group:

```bash theme={null}
az ad sp create-for-rbac \
  --name tf-kodekloud \
  --role Contributor \
  --scopes "/subscriptions/d1e69bd8-2fe1-42bc-a3a7-ca4469cb5167/resourceGroups/echovisa-rg-7u9uby"
```

The command prints credentials (example output, sanitized):

```json theme={null}
{
  "appId": "5eaaf6c4-d542-4eb6-bd8d-24c0e5986f90",
  "displayName": "tf-kodekloud",
  "password": "REDACTED_SECRET",
  "tenant": "a8dab4a7-9027-461c-97ab-b022f15917a4"
}
```

Set environment variables so the Terraform Provider can authenticate:

```bash theme={null}
export ARM_SUBSCRIPTION_ID="d1e69bd8-2fe1-42bc-a3a7-ca4469cb5167"
export ARM_TENANT_ID="a8dab4a7-9027-461c-97ab-b022f15917a4"
export ARM_CLIENT_ID="5eaaf6c4-d542-4eb6-bd8d-24c0e5986f90"
export ARM_CLIENT_SECRET="REDACTED_SECRET"
```

<Callout icon="warning">
  Do not commit service principal credentials to source control. Store secrets securely (for example, in [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)) and rotate them regularly.
</Callout>

Why use service principals:

* Suitable for non-interactive automation.
* Allows least-privilege RBAC scoping to limit Terraform actions.
* Can use client secret or certificate-based authentication.

Terraform will use these environment variables to acquire tokens from Microsoft Entra ID and call ARM on your behalf.

## 3) Managed Identity

Managed identities (formerly MSI) are Azure-managed service principals attached to an Azure resource (for example, a VM, Virtual Machine Scale Set, App Service, or Azure Function). They provide a secretless way for Azure resources to authenticate to Azure services.

To use a managed identity with Terraform:

1. Enable a system-assigned or user-assigned managed identity on your Azure resource.
2. Assign the managed identity the necessary RBAC role at the appropriate scope.
3. Configure Terraform (or the environment) so the Azure Provider uses the managed identity. Example environment variables:

```bash theme={null}
export ARM_USE_MSI=true
export ARM_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
export ARM_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

How it works:

* The Azure resource requests tokens from the Instance Metadata Service (IMDS).
* No client secrets are stored or shared.
* Terraform running on that resource will acquire tokens transparently.

Managed identities are the recommended approach for Terraform running inside Azure because they remove credential management and reduce risk.

## Best practices

* Principle of least privilege: scope RBAC roles to the minimal required scope (resource group, resource, or custom roles).
* Avoid embedding secrets in source control. Use secret stores like Azure Key Vault.
* Prefer Managed Identity for Azure-hosted automation. Use service principals for external CI/CD systems.
* For local development use `az login`, but ensure CI/CD uses explicit, auditable identities (service principals or managed identities).

## Links and references

* Microsoft Entra ID (Azure AD): [https://learn.microsoft.com/azure/active-directory/](https://learn.microsoft.com/azure/active-directory/)
* Azure Resource Manager (ARM): [https://learn.microsoft.com/azure/azure-resource-manager/](https://learn.microsoft.com/azure/azure-resource-manager/)
* Azure CLI: [https://learn.microsoft.com/cli/azure/](https://learn.microsoft.com/cli/azure/)
* Managed identities for Azure resources: [https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/)
* Create a service principal with Azure CLI: [https://learn.microsoft.com/cli/azure/ad/sp#create-for-rbac](https://learn.microsoft.com/cli/azure/ad/sp#create-for-rbac)

Summary:

* Azure CLI (`az login`) is convenient for local work.
* Service principals are ideal for CI/CD automation; secure secrets properly.
* Managed identities are the recommended, secretless option for resources running inside Azure.

With these patterns you can authenticate Terraform to Azure in a secure and auditable way.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/db2adc19-fa48-4b03-9d9a-8ef71c4c28db/lesson/c140ef67-4b6d-49ab-bfca-d2c449d2ab3a" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/db2adc19-fa48-4b03-9d9a-8ef71c4c28db/lesson/3df81667-731b-4456-8751-9e6f680a6e9d" />
</CardGroup>
