# Secure Vault Initialization

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Secure-Vault-Initialization/page

This article explains the secure initialization process of a HashiCorp Vault cluster, including key generation, distribution, and best practices for security.

Initializing a new HashiCorp Vault cluster securely is critical. This process:

1. Generates a master key and splits it into key shares (unseal or recovery keys).
2. Creates the initial root token.

Depending on your setup—default unseal or auto unseal (Transit, AWS KMS, GCP KMS, Azure Key Vault)—Vault will produce the appropriate key shares. Once initialized, you use these shares (or the auto-unseal mechanism) to make Vault operational, then log in with the root token to configure your secrets engine.

```bash theme={null}
vault operator init [options]
```

Next, we’ll explore what happens during initialization, how to protect those critical keys, and best practices for secure distribution.

## Vault Initialization Process

When you run `vault operator init`, Vault:

1. Creates an encryption key for the storage backend.
2. Generates a master key to encrypt that storage key.
3. Splits the master key into shards (unseal or recovery keys).
4. Outputs the shards along with the initial root token.

<Frame>
  ![The image illustrates the process of Vault Initialization, showing how key shards (unseal keys) combine to form a master key, which then protects an encryption key that secures vault data.](https://kodekloud.com/kk-media/image/upload/v1752878497/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Secure-Vault-Initialization/vault-initialization-key-shards-diagram.jpg)
</Frame>

By default, Vault displays all key shards and the root token to the operator. To adhere to Vault’s security model, you should split custody of those shards across multiple trusted parties.

## Distributing Key Shares

A common security practice is to distribute unseal (or recovery) keys to separate, trusted employees. For example, if you configure 5 key shares with a threshold of 3, you give each of five employees one share—any three can reconstruct the master key.

<Frame>
  ![The image shows five people, each with a colored key above their head, under the text "Provide Keys to Trusted Employees." There's also a certification badge in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752878498/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Secure-Vault-Initialization/provide-keys-trusted-employees-image.jpg)
</Frame>

<Callout icon="triangle-alert">
  If a single operator runs `vault operator init` without encryption, they receive all keys in plaintext. Always encrypt shards when splitting custody.
</Callout>

## Basic Initialization Options

Customize the number of shares and the reconstruction threshold:

| Option                | Description                             | Example                 |
| --------------------- | --------------------------------------- | ----------------------- |
| `-key-shares`         | Total unseal key shards                 | `-key-shares=5`         |
| `-key-threshold`      | Shards required to unseal               | `-key-threshold=3`      |
| `-recovery-shares`    | Total recovery key shards (auto-unseal) | `-recovery-shares=5`    |
| `-recovery-threshold` | Shards required for recovery            | `-recovery-threshold=3` |

```bash theme={null}
vault operator init \
  -key-shares=5 \
  -key-threshold=3

vault operator init \
  -recovery-shares=5 \
  -recovery-threshold=3
```

<Callout icon="lightbulb">
  These flags adjust only the share count and threshold. They do **not** encrypt the output.
</Callout>

## Encrypting Shares with PGP

To prevent a single operator from holding all key material, encrypt each shard with the recipient’s PGP public key. Provide Vault with each user’s `.pub` file during initialization.

<Frame>
  ![The image illustrates "Secure Vault Initialization" with cartoon and real people, each associated with pairs of public and private keys. A logo and certification badge are also present.](https://kodekloud.com/kk-media/image/upload/v1752878499/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Secure-Vault-Initialization/secure-vault-initialization-keys-illustration.jpg)
</Frame>

### Unseal Keys with PGP Encryption

Assume five users—Bob, Steve, Stacy, Katie, and Dani—have shared their public PGP keys:

```bash theme={null}
ls /opt
