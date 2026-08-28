# Using Batch Tokens

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Scale-Vault-for-Performance/Using-Batch-Tokens/page

Learn to work with batch tokens in Vault, designed for high-throughput operations and seamless replication without persistence.

In this lesson, you’ll learn how to work with **batch tokens** in Vault—lightweight, non-persistent tokens designed for high-throughput operations and seamless replication.

## What Are Batch Tokens?

Batch tokens are encrypted binary large objects (BLOBs) that Vault issues directly to clients without persisting them to storage. They excel in scenarios requiring:

* High-volume cryptographic operations (e.g., Transit encrypt/decrypt)
* Frequent KV reads and writes
* Replication to performance and DR clusters

<Frame>
  ![The image is a slide titled "Introduction to Batch Tokens," describing batch tokens as encrypted binary large objects designed to be lightweight, scalable, and ideal for high-volume operations. It also mentions their use in DR Replication cluster promotion.](https://kodekloud.com/kk-media/image/upload/v1752878620/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/introduction-to-batch-tokens-slide.jpg)
</Frame>

<Callout icon="lightbulb">
  Batch tokens are never written to the storage backend. This makes them faster to create and cheaper to replicate across performance clusters.
</Callout>

## Service Tokens vs. Batch Tokens

Batch tokens trade off some features for speed and replication agility. Key differences include:

* **Renewability & Revocation**: Batch tokens are not renewable, listable, or manually revocable.
* **Accessors & Cubbyholes**: They lack token accessors and cubbyholes.
* **Child Tokens**: You cannot create child tokens from batch tokens.
* **TTL Configuration**: No periodic issuance or explicit max TTL.
* **Replication**: Orphan batch tokens replicate to performance and DR clusters; non-orphans do not.

<Frame>
  ![The image is a comparison table between service tokens and batch tokens, highlighting their differences in features such as renewability, revocability, and TTL settings. It emphasizes the importance of understanding these differences.](https://kodekloud.com/kk-media/image/upload/v1752878621/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/service-tokens-vs-batch-tokens-table.jpg)
</Frame>

<Frame>
  ![The image is a comparison table between Service Tokens and Batch Tokens, highlighting differences in usage across performance replication clusters, creation scalability, and cost. It emphasizes the importance of understanding these differences.](https://kodekloud.com/kk-media/image/upload/v1752878622/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/service-tokens-vs-batch-tokens-table-2.jpg)
</Frame>

## Identifying Token Types

Starting with Vault 1.10, tokens are prefixed to indicate their type:

| Prefix | Token Type     |
| ------ | -------------- |
| hvs.   | Service Token  |
| hvb.   | Batch Token    |
| hvr.   | Recovery Token |

Batch tokens tend to be longer (≈128 bytes) than service tokens (≈96 bytes). Always plan for tokens up to 255 bytes in length.

<Frame>
  ![The image explains how to identify token types in Vault using prefixes: "hvs." for Service Token, "hvb." for Batch Token, and "hvr." for Recovery Token. It also features a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878623/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/vault-token-types-identification-guide.jpg)
</Frame>

<Frame>
  ![The image explains token size changes in HashiCorp Vault, noting the initial root token size and recommending planning for a maximum length of 255 bytes. It includes a certification badge and a character illustration.](https://kodekloud.com/kk-media/image/upload/v1752878624/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Using-Batch-Tokens/hashicorp-vault-token-size-changes.jpg)
</Frame>

```console theme={null}
