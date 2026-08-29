# Securing Azure AI Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Using-Azure-AI-Services-for-Enterprise-Applications/Securing-Azure-AI-Services/page

Guide on securing Azure AI services by using key rotation, Azure Key Vault, and Managed Identity to prevent credential leakage, enforce least privilege, and simplify secret rotation.

Protecting Azure AI resources from unauthorized access requires a layered approach. This guide covers three essential methods you can use together to reduce key leakage and operational risk: key rotation, storing secrets in Azure Key Vault, and using Managed Identity to avoid hardcoded credentials.

* Key rotation
* Key Vault storage
* Managed Identity

<Frame>
  <img alt="A slide titled &#x22;Securing Azure AI Services&#x22; showing three colored panels for Key Rotation, Key Vault Storage, and Managed Identity with matching icons. Each panel gives brief guidance about regularly regenerating keys, storing keys in Azure Key Vault, and using a Service Principal to avoid hardcoding credentials." />
</Frame>

Why these controls matter

* Keys embedded in code or logs are easy to leak and can be used by an attacker to call your AI service, incur costs, or exfiltrate data.
* Combining centralized secret storage (Key Vault), automated identity (Managed Identity), and regular key rotation makes exposure less likely and limits the blast radius if a secret is compromised.

Comparison at a glance

| Resource Type    | Primary Purpose                                        | When to use                                                                                    |
| ---------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Key rotation     | Limit exposure of compromised keys                     | Use for any long-lived secret; schedule per policy (monthly, quarterly)                        |
| Azure Key Vault  | Centralize secrets, versioning, access control         | Use to store API keys, connection strings, certificates                                        |
| Managed Identity | Eliminate credentials in code by using Azure AD tokens | Use for Azure-hosted apps (App Service, VMs, Functions) to access Key Vault and other services |

## 1. Key rotation

Regularly regenerate (rotate) your access keys to reduce the time window an exposed key remains valid.

Zero-downtime rotation pattern (applies where resources provide two keys):

1. Configure your application to use the secondary key.
2. Regenerate the primary key.
3. Verify operation using the new primary key, then switch the application to use the primary key.
4. Regenerate the secondary key according to your rotation policy.

Best practices

* Select rotation frequency based on your compliance and risk posture (e.g., monthly, quarterly).
* Automate rotation and validation where possible to avoid human error.
* Never embed keys in source code, container images, or logs.

## 2. Key Vault storage

Use Azure Key Vault to centrally store keys, secrets, and certificates. Key Vault supports access control, auditing, and secret versioning.

Benefits

* Centralized management reduces accidental exposure via source control.
* Secret versioning lets you rotate without changing application code (if the app retrieves the latest version).
* Access to secrets can be audited and restricted via RBAC or Key Vault access policies.

How it works in practice

* Store your AI service API key as a secret in Key Vault.
* Applications fetch the secret at runtime (see Managed Identity below).
* When you rotate the secret in Key Vault, retrieving by name without a version returns the latest value, enabling seamless updates.

## 3. Managed Identity

Managed Identity eliminates credential handling in code by giving Azure resources an identity in Azure AD.

Typical flow

1. Your app authenticates using its Managed Identity.
2. The app requests the secret (API key) from Key Vault.
3. Key Vault returns the secret value.
4. The app uses the secret to call Azure AI Services.

<Callout icon="lightbulb">
  Use Managed Identity wherever possible for Azure-hosted applications. It avoids hard-coded secrets and simplifies rotation and access control.
</Callout>

Example: retrieving a secret from Key Vault using Managed Identity (Python)

* Prerequisites: The Azure resource (e.g., App Service, VM, or Function) must have its Managed Identity enabled and be granted the Key Vault "get" permission. Install azure-identity and azure-keyvault-secrets packages.

```python theme={null}
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
