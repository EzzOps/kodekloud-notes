# Enable KV v2 at mount path "crds"
vault secrets enable -path=crds kv-v2

# Upload the "app" policy from your HCL file
vault policy write app /home/vault/app-policy.hcl

# List all policies to confirm
vault policy list
```

You should see:

```text theme={null}
app
default
root
```

Inspect the rules in the `app` policy:

```bash theme={null}
vault policy read app
```

<Callout icon="triangle-alert">
  Avoid using the root token for routine operations. Instead, generate scoped tokens for applications and users.
</Callout>

## 3. Generate a Token Bound to the `app` Policy

Create a new token that attaches only the `app` policy. Store it in the `VAULT_TOKEN` environment variable:

```bash theme={null}
export VAULT_TOKEN="$(vault token create -field token -policy=app)"
echo $VAULT_TOKEN
# Example output: s.1S3rgiveIvhIn2gBe9RwUc2cf
```

All subsequent Vault CLI commands will automatically use this token.

## 4. Test Policy Enforcement

1. **Allowed Operation**\
   Read MongoDB credentials:
   ```bash theme={null}
   vault kv get crds/data/mongodb
   ```

2. **Denied Operation**\
   Attempt to write MySQL credentials (not permitted by the `app` policy):
   ```bash theme={null}
   vault kv put crds/data/mysql username=siddharth
   ```
   You will see a **403 permission denied** error:
   ```text theme={null}
   Error writing data to crds/data/mysql: Error making API request.

   URL: PUT http://127.0.0.1:8200/v1/crds/data/mysql
   Code: 403. Errors:
   * 1 error occurred:
   * permission denied
   ```

This confirms that the `app` policy correctly restricts write access to the MySQL path.

## Next Steps

After defining and testing policies, integrate them with an authentication method:

* Kubernetes Auth
* AppRole Auth
* LDAP Auth

These methods use **roles** to assign policies to authenticated entities, enabling seamless integration with external identity systems.

## Links and References

* [Vault Policies](https://www.vaultproject.io/docs/concepts/policies)
* [KV Secrets Engine (v2)](https://www.vaultproject.io/docs/secrets/kv/kv-v2)
* [Vault Authentication Methods](https://www.vaultproject.io/docs/auth)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/98b0333a-cf76-48a9-b662-5c6165cdb414" />
</CardGroup>


# Demo Vault Helm Installation

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Demo-Vault-Helm-Installation/page

This tutorial covers installing HashiCorp Vault on Kubernetes using Helm, including prerequisites, deployment steps, and accessing the Vault UI.

In this tutorial, you’ll learn what HashiCorp Vault is, explore various installation methods, and perform a hands-on deployment of Vault in a Kubernetes cluster using the official Helm chart.

## What Is Vault?

Vault is a centralized secrets management tool designed for securely storing and accessing sensitive data such as:

* **Credentials** for authenticating users or services
* **Encryption keys** for data encryption and decryption
* **API tokens**, TLS certificates, and other secret types

Vault offers:

* A unified REST API for secret management
* Fine-grained access control with policies
* Detailed audit logging of all operations

For more, visit the [HashiCorp Vault Documentation](https://www.vaultproject.io/docs).

## Installation Methods

You can install Vault using one of the following approaches:

| Method                | Description                                 | Example Command                             |
| --------------------- | ------------------------------------------- | ------------------------------------------- |
| Linux Package Manager | Install via APT or Yum on supported distros | `sudo apt-get install vault`                |
| Precompiled Binary    | Download and place in your `PATH`           | `wget https://releases.hashicorp.com/vault` |
| Build from Source     | Clone the repo and compile yourself         | `go build github.com/hashicorp/vault`       |

<Callout icon="triangle-alert">
  For production, run Vault in a highly available configuration across multiple hosts. Use a durable storage backend like Consul or AWS S3.
</Callout>

### Installing via APT (Ubuntu/Debian)

```bash theme={null}
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```

## Deploying Vault with Helm

We’ll deploy Vault into Kubernetes using the official Helm chart. Ensure you have:

* Kubernetes ≥1.14
* Helm 3.x installed
* `kubectl` configured to access your cluster

### 1. Add the HashiCorp Helm Repository

```bash theme={null}
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
```

### 2. Review the Vault Helm Chart

Check the chart’s prerequisites and usage on GitHub:

<Frame>
  ![The image shows a GitHub page for the "Vault Helm Chart" repository by HashiCorp, detailing installation and configuration instructions for using Vault on Kubernetes. It includes sections on prerequisites and usage, with a sidebar showing language statistics.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873731/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Vault-Helm-Installation/github-vault-helm-chart-repo.jpg)
</Frame>

### 3. Inspect Default Configuration

View the excerpt from `values.yaml`:

```yaml theme={null}
