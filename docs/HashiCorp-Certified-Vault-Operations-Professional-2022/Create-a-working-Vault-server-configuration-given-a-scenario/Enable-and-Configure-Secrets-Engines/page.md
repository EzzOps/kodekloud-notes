# Output: bar
```

This is useful for automation and CI pipelines.

***

## 10. Cleanup: Delete All Metadata

To remove both data and metadata for a secret path:

```bash theme={null}
vault kv metadata delete kvv2/apps/circleci
```

Running `vault kv list kvv2/apps` now returns nothing.

***

## 11. KV v2 Prefixes in ACL Policies

When you write ACL policies for KV v2, include both `data/` and `metadata/` paths:

```hcl theme={null}
path "kvv2/data/apps/artifactory" {
  capabilities = ["read"]
}

path "kvv2/metadata/apps/artifactory" {
  capabilities = ["read", "list"]
}
```

***

## 12. Managing Secrets via the Web UI

Vault’s UI offers point-and-click management for KV v2 secrets:

**Browse secrets and create a new entry**\
Click **Secrets > kvv2** and select **Create secret**.

<Frame>
  ![The image shows a web interface for managing secrets in HashiCorp Vault, with options for "azuredevops" and "jenkins" under the "training" section. The interface includes a search bar and a "Create secret" button."](https://kodekloud.com/kk-media/image/upload/v1752878427/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-KeyValue-Secrets-Engine-Version-2/hashicorp-vault-secrets-management-interface.jpg)
</Frame>

**Enter secret data**\
Provide `artifact = "jenkins"` or other key-value pairs, then save.

<Frame>
  ![The image shows a web interface for creating a secret in HashiCorp Vault, with fields for specifying the secret path and data. There are options to save or cancel the entry."](https://kodekloud.com/kk-media/image/upload/v1752878427/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-KeyValue-Secrets-Engine-Version-2/hashicorp-vault-secret-creation-interface.jpg)
</Frame>

**View stored JSON**\
Select the secret to see its JSON key-value data.

<Frame>
  ![The image shows a web interface for HashiCorp Vault, displaying a secret stored under the path "apps/artifactory" with a JSON key-value pair. The secret's value is obscured for security."](https://kodekloud.com/kk-media/image/upload/v1752878428/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-KeyValue-Secrets-Engine-Version-2/hashicorp-vault-web-interface-secret-json.jpg)
</Frame>

**Create an ACL policy**\
Under **Policies**, click **Create policy**, enter a name and HCL, then save.

<Frame>
  ![The image shows a user interface for creating an ACL policy, with fields for entering a name and policy details, and options to create or cancel the policy."](https://kodekloud.com/kk-media/image/upload/v1752878429/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-KeyValue-Secrets-Engine-Version-2/acl-policy-creation-user-interface.jpg)
</Frame>

***

## 13. Accessing KV v2 via the HTTP API

To retrieve secret data over HTTP, include `/data/` in the path:

```bash theme={null}
curl --header "X-Vault-Token: $VAULT_TOKEN" \
     http://127.0.0.1:8200/v1/kvv2/data/apps/artifactory \
  | jq
```

Response:

```json theme={null}
{
  "request_id": "...",
  "data": {
    "data": {
      "artifact": "jenkins"
    },
    "metadata": {
      "created_time": "...",
      "version": 1
    }
  }
}
```

For KV v1 mounts, omit the `/data/` prefix.

***

## References

* [Vault KV Secrets Engine v2](https://www.vaultproject.io/docs/secrets/kv/kv-v2)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)
* [Vault HTTP API](https://www.vaultproject.io/api-docs)

That wraps up our deep dive into the KV v2 engine. Enjoy secure, versioned secret management with HashiCorp Vault!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/778922e5-1ae1-4bbf-accb-b2bb7d08bee5" />
</CardGroup>


# Enable and Configure Secrets Engines

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Enable-and-Configure-Secrets-Engines/page

This guide explores enabling, configuring, and managing HashiCorp Vault’s Secrets Engines using the CLI, API, and UI.

Secrets Engines are the heart of HashiCorp Vault, providing dynamic secrets, encryption, identity management, and more. In this guide, we’ll explore how to enable, configure, and manage Vault’s Secrets Engines—both generic and cloud-integrated—using the Vault CLI, API, and UI.

* What are Vault Secrets Engines?
* Generic vs. Cloud-Integrated Engines
* Enabling Engines with CLI
* Enabling Engines via UI
* Next Steps

## What Are Secrets Engines?

Vault Secrets Engines enable integration with external platforms and back-end systems by generating dynamic secrets, certificates, encryption, and identity data. While Vault supports a wide range of cloud providers and services, this tutorial focuses on the core generic engines tested in the HashiCorp Certified Vault Operations Professional exam.

<Frame>
  ![The image lists various "Available Secrets Engines" related to Vault, including services like AWS, Google Cloud, and MongoDB Atlas. It also features a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878445/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Secrets-Engines/available-secrets-engines-vault-services.jpg)
</Frame>

## Generic Secrets Engines

Vault’s generic Secrets Engines do not require deep expertise in external platforms. These are commonly used across environments and covered in Vault certification:

<Frame>
  ![The image is a slide about "Generic Secrets Engines," detailing features like database support, Key/Value versions, PKI certificates, and data encryption with Transit. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878446/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Secrets-Engines/generic-secrets-engines-features-slide.jpg)
</Frame>

| Engine     | Function                          | Key Features                                    |
| ---------- | --------------------------------- | ----------------------------------------------- |
| Database   | Dynamic database credentials      | 13+ platforms (MySQL, PostgreSQL, Oracle, etc.) |
| KV (v1/v2) | Key/Value storage                 | v1 (simple) & v2 (versioned, metadata)          |
| PKI        | Certificate issuance & management | X.509/TLS certificates                          |
| Transit    | Encryption-as-a-Service           | Data encryption, auto-unseal                    |
| Cubbyhole  | Per-token private secret storage  | Enabled by default                              |
| Identity   | Identity data storage             | Enabled by default                              |

## Enabling Secrets Engines

Engines can be enabled at a custom mount path using the Vault CLI, API, or UI. The UI offers a simple way to enable common engines, but some advanced configurations require CLI or API.

<Frame>
  ![The image is a slide about enabling secrets engines, detailing default settings, enabling methods, and path configurations. It includes a Vault certification badge and a cartoon character illustration.](https://kodekloud.com/kk-media/image/upload/v1752878447/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Secrets-Engines/enabling-secrets-engines-vault-slide.jpg)
</Frame>

<Callout icon="lightbulb">
  Use meaningful mount paths (e.g., `prod-db/` or `teams/cloud-kv/`) to simplify management and auditing.
</Callout>

### Enable with Vault CLI

The `vault secrets` command suite manages engine lifecycle:

* `enable`: Mount a new engine
* `disable`: Unmount an engine
* `list`: View enabled engines
* `move`: Rename or relocate a mount path
* `tune`: Adjust engine settings (TTLs, descriptions)

```bash theme={null}
