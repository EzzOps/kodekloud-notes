# KeyValue Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-and-Configure-Secrets-Engines/KeyValue-Secrets-Engine/page

Vaults Key/Value Secrets Engine securely stores static secrets and integrates with various tools for retrieval and management.

Vault's Key/Value (KV) Secrets Engine securely stores static secrets—API keys, certificates, credentials—that Vault doesn’t generate dynamically. You can retrieve these secrets via UI, CLI, or API and integrate with tools like Terraform, Jenkins, or GitLab CI/CD.

> **lightbulb** Almost every Vault deployment uses at least one KV mount. You can enable multiple KV instances at different paths to isolate secrets by team, environment, or application.

## Why Use KV for Static Secrets

* Centralized management of non-rotating secrets
* Integration with CI/CD and automation tools
* Granular access control through Vault policies
* 256-bit AES encryption at rest

| Tool         | Use Case                    | Example                                    |
| ------------ | --------------------------- | ------------------------------------------ |
| Terraform    | Infrastructure provisioning | `terraform apply`                          |
| Jenkins      | CI/CD pipelines             | Vault CLI plugin for secret injection      |
| GitLab CI/CD | Pipeline secret storage     | Store Vault token and KV path in variables |

![The image is a slide explaining the Key/Value Secrets Engine, detailing how secrets are stored as key-value pairs at defined paths and the capabilities required for writing and updating secrets.](https://kodekloud.com/kk-media/image/upload/v1752878108/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/key-value-secrets-engine-explanation.jpg)

## KV Engine Versions: v1 vs. v2

| Feature           | KV v1                | KV v2 (Versioned)                      |
| ----------------- | -------------------- | -------------------------------------- |
| Versioning        | No history           | Full version history                   |
| Read behavior     | Overwrites on update | Latest by default, can request version |
| Rollback/Undelete | Not supported        | Supported                              |
| Metadata support  | No                   | Yes                                    |

> Reading from v2 returns the latest version unless you specify another version.

## Enabling the KV Engine

KV v2 is not enabled by default in production.

### Via UI

1. Go to **Secrets > Enable new engine**
2. Select **Key/Value**
3. Set **Mount path** (default `kv`) and choose version
4. (Optional) Add description, tune max versions or CAS, configure deletion

![The image shows a user interface for enabling a Key/Value Secrets Engine, with options for selecting different types of secrets and configuring settings. It includes sections for generic, cloud, and infrastructure options.](https://kodekloud.com/kk-media/image/upload/v1752878109/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/key-value-secrets-engine-ui-options.jpg)

### Via CLI

Enable KV v1 at `kv/` (default):

```bash theme={null}
vault secrets enable kv
