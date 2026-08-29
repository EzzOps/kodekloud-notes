# Transit Cluster
ssh ec2-user@10.0.1.209

# Target Cluster
ssh ec2-user@10.0.1.37
```

> **triangle-alert** Ensure that both nodes can communicate over port `8200` and that the Vault CLI is installed and in your `PATH`.

***

## 1. Configure the Transit Cluster

### 1.1 Enable the Transit Secrets Engine

Verify existing engines and enable `transit`:

```bash theme={null}
vault secrets list
vault secrets enable transit
```

### 1.2 Create an Encryption Key

Create a new key named `unseal-key`:

```bash theme={null}
vault write -f transit/keys/unseal-key
vault list transit/keys
```

### 1.3 Define an Unseal Policy

Create a file named `policy.hcl` with the following content:

```hcl theme={null}
path "transit/encrypt/unseal-key" {
  capabilities = ["update"]
}

path "transit/decrypt/unseal-key" {
  capabilities = ["update"]
}
```

Upload the policy:

```bash theme={null}
vault policy write unseal policy.hcl
```

### 1.4 Create a Token for Auto Unseal

Generate a token scoped to the `unseal` policy:

```bash theme={null}
vault token create -policy=unseal
```

> **lightbulb** Save the `token` output securely. You will reference it in the target cluster’s configuration (for example, by exporting it as `VAULT_SEAL_TOKEN`).

***

## 2. Configure the Target Cluster

### 2.1 Verify Vault Status

On the target node, check that Vault is initialized and sealed:

```bash theme={null}
vault status
```

### 2.2 Update Vault Configuration

Edit `/etc/vault.d/vault.hcl` to include your Raft storage and the transit seal stanza:

```hcl theme={null}
storage "raft" {
  path    = "/opt/vault3/data"
  node_id = "node-us-east-1"

  retry_join {
    auto_join = "provider=aws region=us-east-1 tag_key=vault tag_value=us-east-1"
  }
}

seal "transit" {
  address    = "http://10.0.1.209:8200"
  token      = "s.v9hDNIycSM8ZL7wsFo9vD0i"
  key_name   = "unseal-key"
  mount_path = "transit"
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = true
}

api_addr     = "http://10.0.1.37:8200"
cluster_addr = "http://10.0.1.37:8201"
cluster_name = "vault-prod-us-east-1"
ui           = true
log_level    = "INFO"
```

### 2.3 Restart Vault

Restart and verify that the seal type is now Transit:

```bash theme={null}
sudo systemctl restart vault
vault status
```

***

## 3. Initialize and Verify Auto Unseal

Initialize the target cluster:

```bash theme={null}
vault operator init
```

You should see your recovery keys and root token. Immediately after, Vault will auto-unseal:

```bash theme={null}
vault status
```

The `Sealed` field should read `false`, and `Recovery Seal Type` will switch to `shamir`.

***

## 4. Post-Unseal Operations

Log in with the initial root token:

```bash theme={null}
vault login <initial-root-token>
```

Enable additional engines and store sample data:

```bash theme={null}
vault secrets enable azure
vault secrets enable -path=vaultcourse kv

vault kv put vaultcourse/bryan bryan=bryan
vault kv get vaultcourse/bryan
```

Restarting Vault will now preserve the unsealed state:

```bash theme={null}
sudo systemctl restart vault
vault status
```

***

## Conclusion

You’ve successfully set up a centralized Transit Secrets Engine to auto-unseal a Raft-backed Vault cluster. This setup automates unsealing, streamlines recovery, and maintains best practices for security and operations.

***

## Links and References

* [Vault Transit Secrets Engine][transit-doc]
* [Vault Auto Unseal with Transit][auto-unseal]
* [Vault Raft Storage Backend][raft-doc]

[transit-doc]: https://www.vaultproject.io/docs/secrets/transit

[auto-unseal]: https://www.vaultproject.io/docs/seal/transit-auto-unseal

[raft-doc]: https://www.vaultproject.io/docs/storage/raft

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/66d6b1c0-e689-444c-8d5f-a30aa4c84101)


# Pros and Cons of Unseal Options

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Learning-the-Vault-Architecture/Pros-and-Cons-of-Unseal-Options/page

This guide compares HashiCorp Vault’s three primary unseal methods to help you choose the right option for your team.

Unlocking HashiCorp Vault requires an unseal mechanism that fits your security posture and operational model. In this guide, we compare Vault’s three primary unseal methods—Key Shards, Cloud Auto-Unseal, and Transit Auto-Unseal—to help you choose the right option for your team.

| Unseal Method       | Key Advantages                                                         | Key Drawbacks                                                                 |
| ------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Key Shards          | • Platform-agnostic<br />• Customizable share count & threshold        | • Manual process<br />• Human-error risk<br />• Requires key rotation         |
| Cloud Auto-Unseal   | • Fully automated at startup<br />• Integrates with cloud HSM services | • Vendor lock-in potential<br />• Regional service limitations                |
| Transit Auto-Unseal | • Centralized unseal for multiple clusters<br />• Cloud-agnostic       | • Requires highly available transit cluster<br />• Added operational overhead |

![The image is a comparison chart of unseal options, highlighting the pros of "Keys Shards," "Auto Unseal," and "Transit Unseal" with a colorful design and a cartoon character in the corner.](https://kodekloud.com/kk-media/image/upload/v1752878213/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Pros-and-Cons-of-Unseal-Options/unseal-options-comparison-chart-colorful.jpg)

## 1. Key Shards

Vault’s original unseal approach splits the master key into multiple shards. A subset of these shards must be provided to unseal the vault.

### Pros

* Simplest to configure—works on any OS or platform.
* You decide the total number of shares and threshold (e.g., 5 of 10).
* No external dependencies; zero cloud lock-in.

### Cons

* Manual unseal with `vault operator unseal` can be slow during restarts.
* High risk of lost or exposed shards if not managed properly.
* Shards must be rotated when custodians leave or keys are compromised.

> **triangle-alert** Always store unseal shards in secure, separate locations. Consider encrypted hardware tokens or HSM-protected backups to reduce human-error risk.

## 2. Cloud Auto-Unseal

Vault can integrate directly with cloud Key Management Services to decrypt its master key automatically.

### Pros

* Fully automated unseal on startup—no manual steps.
* Seamless integration with cloud HSM offerings such as [AWS KMS](https://aws.amazon.com/kms/), [Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/), or [GCP KMS](https://cloud.google.com/kms).
* Master key never exposed in plaintext to your infrastructure.

### Cons

* Tied to a specific cloud provider—potential for vendor lock-in.
* Service availability and region limits may affect startup times.

> **lightbulb** Review your cloud provider’s HSM SLAs to ensure they meet your uptime and latency requirements.

## 3. Transit Auto-Unseal

By leveraging Vault’s Transit secrets engine on a dedicated cluster, you can offload unseal operations centrally for multiple Vault servers.

### Pros

* Platform- and cloud-agnostic solution—works across AWS, Azure, GCP, or on-prem.
* One transit cluster can service unseal requests for many Vault clusters.
* Simplifies multi-region and hybrid-cloud deployments.

### Cons

* Introduces a critical dependency on a highly available transit cluster—misconfiguration can lead to outages.
* Increases operational overhead to secure, monitor, and scale the transit cluster.

> **triangle-alert** Ensure your transit cluster is deployed with replication or clustering enabled. A single Transit node failure could prevent all downstream Vault instances from unsealing.

## Further Reading

* [Vault Auto Unseal Documentation](https://www.vaultproject.io/docs/configuration/seal)
* [AWS KMS Integration](https://www.vaultproject.io/docs/secrets/aws)
* [Vault Transit Secrets Engine](https://www.vaultproject.io/docs/secrets/transit)
* [Best Practices for Vault High Availability](https://www.vaultproject.io/docs/enterprise/haz)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/a201f459-d4bb-4332-a603-55b72ab566ab)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/e222f1f9-db60-4d34-a0d3-12f9b0312710)
