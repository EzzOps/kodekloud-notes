# Service Token (96 bytes)
hvs.CAESIA4CZQisJNn9eq3g5TS5xP0-DPkFDsshli_jb5UH28AuGiAKHGh2cy5wZjPU1NsVlpWaTQxSFUyczFuQk9DOFgQHQ

# Batch Token (128 bytes)
hvb.AAAAAQKskxnAqTz0Ah3qu5Hc4Q3lYdqCocdDZjLXhyLAjuhhBJktOCrBaJVbKwE6AVsxD6WAFvlZ2UHs2MUb1gcpqYvro-kfVv10x7tKZ9GqUObUwKnn5341sU
```

## Batch Token Replication

Vault supports two replication modes for batch tokens:

### Non-Orphan Tokens

Batch tokens created with a parent token remain bound to the original cluster. Performance secondaries cannot validate the parent, so these tokens do **not** replicate.

<Frame>
  ![The image illustrates the process of replicating batch tokens in a non-orphan token scenario, showing that batch tokens are only valid on the primary cluster where they were created and are not replicated to the secondary performance cluster.](https://kodekloud.com/kk-media/image/upload/v1752878625/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/replicating-batch-tokens-primary-cluster.jpg)
</Frame>

### Orphan Tokens

Orphan batch tokens have no parent and are automatically replicated to all performance and DR clusters. Use these when you need a single token valid across multiple clusters.

<Frame>
  ![The image illustrates the replication of orphaned batch tokens between a primary cluster and a secondary performance cluster, highlighting that these tokens have no parent and are valid on any cluster in the replica set.](https://kodekloud.com/kk-media/image/upload/v1752878626/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/orphaned-batch-tokens-replication-diagram.jpg)
</Frame>

## Creating Batch Tokens

### Direct Token Creation

Use the `vault token create` command:

```bash theme={null}
vault token create -type=batch -orphan=true -policy=hcvop
```

Example output:

```console theme={null}
Key                  Value
---                  -----
Token                hvb.AAAAAQKsxnAqTz0Ah3qu5Hc4Q31YdqCocdDZjLXhyLAjuhhBJktOCrBaIJVbKwE6AVsxD6WAFvlI2ZUHs2MUb1gcpqYvro-kfVv
token_accessor       n/a
token_duration       768h
token_renewable      false
token_policies       ["default" "hcvop"]
```

<Callout icon="lightbulb">
  The `-orphan=true` flag ensures this token replicates across performance and DR clusters.
</Callout>

### Via AppRole

Configure an AppRole to issue batch tokens:

```bash theme={null}
vault write auth/approle/role/hcvop \
  policies=devops \
  token_type="batch" \
  token_ttl="60s"
```

## DR Operations Batch Token

A DR operations batch token lets you promote a DR secondary without needing unseal or recovery keys. Grant it the following permissions:

<Frame>
  ![The image is a slide about "DR Operation Batch Token," explaining its use in promoting a DR secondary cluster without needing unseal/recovery keys, and emphasizing the importance of proper permissions. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878627/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/dr-operation-batch-token-slide.jpg)
</Frame>

```hcl theme={null}
path "sys/replication/dr/secondary/promote" {
  capabilities = ["update"]
}

path "sys/replication/dr/secondary/update-primary" {
  capabilities = ["update"]
}

path "sys/storage/raft/autopilot/state" {
  capabilities = ["update", "read"]
}
```

1. Create an orphan batch token with the `dr-ops` policy:
   ```bash theme={null}
   vault token create -type=batch -orphan=true -policy=dr-ops
   ```
2. Use it to promote the DR secondary:
   ```bash theme={null}
   vault write sys/replication/dr/secondary/promote
   ```

## Summary

* Batch tokens are lightweight, non-persistent tokens for high-throughput workloads.
* Only **orphan** batch tokens replicate to performance and DR clusters.
* Token prefixes (`hvs.`, `hvb.`, `hvr.`) and lengths help identify types.
* Create batch tokens directly or via auth methods like AppRole.
* Use DR operations batch tokens to streamline disaster recovery promotions.

## Links and References

* [Vault Token Authentication](https://www.vaultproject.io/docs/concepts/tokens)
* [Transit Secrets Engine](https://www.vaultproject.io/docs/secrets/transit)
* [Replication Overview](https://www.vaultproject.io/docs/enterprise/replication)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b6a41fdb-447c-43b2-9489-6c8459821fab/lesson/b61adae2-2ce4-42e7-ac3b-85dcb723150b" />
</CardGroup>


# Benefits and Use Cases of Seal Wrapping

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Understand-the-Hardware-Security-Module-HSM-Integration/Benefits-and-Use-Cases-of-Seal-Wrapping/page

This article discusses seal wrapping in HashiCorp Vault, highlighting its benefits for double encryption and FIPS 140-2 compliance in high-security environments.

HashiCorp Vault encrypts data at rest with AES-256, but seal wrapping adds a second layer of encryption using an HSM for FIPS 140-2 compliance. This “double encryption” ensures data is encrypted first by Vault’s master key, then again by the HSM’s key.

<Callout icon="lightbulb">
  As of Vault 1.10.3, HashiCorp publishes FIPS-certified binaries suffixed with `-fips` that do not require an HSM.
</Callout>

<Frame>
  ![The image explains "Seal Wrapping," a method for providing double encryption and FIPS 140-2 compliance by integrating with an HSM, allowing Vault to be used in high-security environments. It also notes that HashiCorp offers Vault binaries for FIPS compliance without HSM integration starting from version 1.10.3.](https://kodekloud.com/kk-media/image/upload/v1752878630/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Benefits-and-Use-Cases-of-Seal-Wrapping/seal-wrapping-double-encryption-fips.jpg)
</Frame>

## What Is Seal Wrapping?

Seal wrapping encrypts Vault’s ciphertext a second time with HSM-managed keys, enabling Vault in high-security environments (PCI, HIPAA, DoD, NATO).

By combining:

* AES-256 encryption by Vault’s master key
* Secondary HSM encryption

Vault achieves FIPS 140-2 Level 3 compliance when paired with a Level 3 HSM.

### Default Seal-Wrapped Data

Vault seal-wraps the most sensitive assets by default:

<Frame>
  ![The image is a slide titled "What is Seal Wrapped by Default?" listing items such as Recovery Key, Any stored key shares, The root key, and The keyring. It includes a Vault certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878630/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Benefits-and-Use-Cases-of-Seal-Wrapping/what-is-seal-wrapped-default-slide.jpg)
</Frame>

| Resource      | Description                    |
| ------------- | ------------------------------ |
| Recovery Key  | Master recovery key shares     |
| Stored Shares | All encrypted key shares       |
| Root Key      | Primary root token key         |
| Keyring       | Internal cryptographic keyring |

## Configuring Seal Wrapping

Seal wrapping is on by default for supported HSM seals. To disable it (trading security for a slight performance boost):

```hcl theme={null}
