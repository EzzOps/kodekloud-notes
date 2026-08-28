# Promote a Secondary Cluster

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Build-Fault-Tolerant-Vault-Environments/Promote-a-Secondary-Cluster/page

This tutorial explains how to promote a DR secondary cluster to primary in HashiCorp Vault to minimize downtime during primary cluster failure.

When your primary Vault cluster becomes unavailable, you can promote its Disaster Recovery (DR) secondary cluster to primary to minimize downtime. This tutorial walks through the steps and best practices for DR replication failover in HashiCorp Vault.

The typical topology consists of:

* A primary cluster
* A performance replica in another data center
* DR replicas for each cluster

If any cluster fails, its DR replica can assume the primary role in that region.

<Callout icon="lightbulb">
  You need a **DR operation token** to promote a DR secondary. You can generate this token on the DR cluster using unseal or recovery keys, or pre-create a **DR operation batch token** on the primary to have it automatically replicate to the secondary.
</Callout>

<Frame>
  ![The image is a slide explaining how to promote a secondary to a primary in a DR cluster, detailing the use of a DR Operation Token and the option to create a DR Operation Batch Token beforehand.](https://kodekloud.com/kk-media/image/upload/v1752878319/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Promote-a-Secondary-Cluster/dr-cluster-promote-secondary-primary-slide.jpg)
</Frame>

## Comparison: Batch Token vs. Generated DR Operation Token

| Token Type               | Creation Location | Replication Behavior     | Use Case                                           |
| ------------------------ | ----------------- | ------------------------ | -------------------------------------------------- |
| DR Operation Batch Token | Primary           | Automatically replicates | Pre-shift preparation; minimal downtime on failure |
| DR Operation Token       | Secondary         | Generated on demand      | When no pre-created batch token is available       |

## DR Operation Batch Token

A **batch token** is an orphan token created on the primary with permissions to promote a DR cluster. It automatically replicates to the DR secondary.

1. Generate at the start of each shift (valid only for that period).
2. Store securely (e.g., in an HSM or secure vault).
3. On failure, use it immediately—no need for unseal or recovery key collection.

## Generating a DR Operation Token

If you don’t have a valid batch token, follow these steps on the DR secondary:

<Frame>
  ![The image is a flowchart explaining the process of obtaining a DR Operation Token, involving steps like initializing token generation, key holders providing keys, decoding with OTP, and promoting a cluster.](https://kodekloud.com/kk-media/image/upload/v1752878321/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Promote-a-Secondary-Cluster/dr-operation-token-flowchart.jpg)
</Frame>

### Step 1: Initialize DR Token Generation

Run `vault operator generate-root` with the `-dr-token` flag and `-init` to receive a `nonce`, an OTP, and progress status:

```bash theme={null}
vault operator generate-root -dr-token -init
```

Example output:

```text theme={null}
Nonce       0ccf03cd-33b3-96db-577c-d5492c4cf909
Started     true
Progress    0/3
Complete    false
OTP         Frq1lTtFmZp1iSD4VwNlRH8ccGm46
OTP Length  28
```

### Step 2: Collect Key Shares

Each key holder submits their key:

```bash theme={null}
vault operator generate-root -dr-token
```

They verify the `Operation nonce: 0ccf03cd-33b3-96db-577c-d5492c4cf909` and enter a unseal or recovery key. After collecting the threshold (e.g., 3 of 5), Vault returns an encoded token:

```text theme={null}
Operation nonce: 0ccf03cd-33b3-96db-577c-d5492c4cf909
Unseal Key (will be hidden): [key input]
Progress    3/3
Complete    true
Encoded Token LgQCHzFBByMRNUYeFgcBHT0KJxN+WwEnIyFIdA
```

### Step 3: Decode the Encoded Token

Use the OTP from step 1 and the encoded token to retrieve the DR operation token:

```bash theme={null}
vault operator generate-root -dr-token \
  -decode="LgQCHzFBByMRNUYeFgcBHT0KJxN+WwEnIyFIdA" \
  -otp="Frq1lTtFmZp1iSD4VwNlRH8ccGm46"
```

Output:

```text theme={null}
hvs.e5ANKEwwEC5KJDKA6cbDdLAB
```

This string is your DR operation token.

## Promote the DR Secondary

With either the batch token or generated DR operation token, run:

```bash theme={null}
vault write sys/replication/dr/secondary/promote \
  dr_operation_token="hvs.e5ANKEwwEC5KJDKA6cbDdLAB"
```

Example warning:

```text theme={null}
WARNING! The following warnings were returned from Vault:
* This cluster is being promoted to a replication primary. Vault will be unavailable for a brief period and will resume service shortly.
```

After promotion, the DR cluster will become the new primary in its data center.

<Callout icon="triangle-alert">
  During promotion, Vault will be temporarily unavailable. Plan for a brief service interruption.
</Callout>

***

## Links and References

* [Vault DR Replication](https://www.vaultproject.io/docs/concepts/replication/dr)
* [vault operator generate-root](https://www.vaultproject.io/docs/commands/operator/generate-root)
* [Vault Best Practices for Disaster Recovery](https://learn.hashicorp.com/collections/vault/high-availability)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/c1dd23ce-c7fd-4564-84d8-4ff14b115bd7/lesson/6ff98f2c-2248-4453-80d2-d2d324adf3d9" />
</CardGroup>
