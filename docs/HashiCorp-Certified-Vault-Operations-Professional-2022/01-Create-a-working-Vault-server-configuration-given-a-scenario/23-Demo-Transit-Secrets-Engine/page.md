# Enter Unseal Key (hidden)
```

Repeat until `Rekey Progress: 3/3`:

```text theme={null}
Key 1: C+YlFuzh0ds9hXmnbTs4QOy1cPvyTCKx8M4iklLDcu6D
Key 2: c07ohvE7H53xFAYxrzl8xTTXGEUcQH39d9HdIcrdaj
Key 3: gvxsl00uJKIwfq0h71sQRKHyC4fcI7svl9gdJ0DPNGp
Key 4: AOJ5LJvl/bhyV+MF/9FBdZB/j0YGRdNi1kpEel7i3Vjt
Key 5: KfHwPR7KVx4eDk4ZlaA2QoZ5IXVdXs1wQKOcY0cxpn

Vault rekeyed with 5 key shares and a key threshold of 3.
Please securely distribute the key shares printed above.
```

You now have a fresh set of recovery keys.

## 4. Rotate the Encryption Key

Periodic encryption key rotation keeps your data encryption strong by refreshing the master key.

### 4.1 Configure Environment Variables

```bash theme={null}
export VAULT_TOKEN=hvs.Wxqk6kDX3fAko3LoCCfczQ3D
export VAULT_ADDR=http://127.0.0.1:8200
```

### 4.2 Check Current Key Status

```bash theme={null}
vault operator key-status
```

Example:

```text theme={null}
Key Term         1
Install Time     09 May 22 14:22 UTC
Encryption Count 199
```

### 4.3 Rotate to a New Key

```bash theme={null}
vault operator rotate
```

```text theme={null}
Success! Rotated key
Key Term         2
Install Time     09 May 22 14:31 UTC
Encryption Count 0
```

Verify:

```bash theme={null}
vault operator key-status
```

## Vault Key Management Commands

| Command                               | Description                                 |
| ------------------------------------- | ------------------------------------------- |
| vault operator init                   | Initialize Vault and generate recovery keys |
| vault operator rekey -init            | Start rekey process                         |
| vault operator rekey -target=recovery | Submit recovery keys to complete rekey      |
| vault operator key-status             | Display current encryption key metadata     |
| vault operator rotate                 | Rotate the Vault encryption key             |

## References

* [Vault CLI Documentation](https://developer.hashicorp.com/vault/docs/commands/operator)
* [Vault Security Concepts](https://www.vaultproject.io/docs/concepts)
* [AWS KMS Auto-Unseal](https://www.vaultproject.io/docs/secrets/aws/kms)

Practice these steps in a non-production environment to master Vault’s key management workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/d7006525-2ee1-4eac-a91a-2bb1e16ba570" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/df72d3c4-15e6-4055-b47e-ab53e0a0aa8c" />
</CardGroup>


# Demo Transit Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Transit-Secrets-Engine/page

This tutorial covers enabling and configuring the Vault Transit Secrets Engine for managing encryption keys and performing cryptographic operations.

Welcome to this tutorial on the Vault Transit Secrets Engine. In this guide, you'll learn how to enable and configure the Transit engine, manage encryption keys, and perform encrypt, decrypt, and rewrap operations.

## Table of Contents

* [Overview](#overview)
* [Verify Enabled Secrets Engines](#verify-enabled-secrets-engines)
* [Enable the Transit Engine](#enable-the-transit-engine)
* [Create and Inspect an Encryption Key](#create-and-inspect-an-encryption-key)
* [Rotate an Encryption Key](#rotate-an-encryption-key)
* [Encrypt Data](#encrypt-data)
* [Rewrap Data After Rotation](#rewrap-data-after-rotation)
* [Decrypt Ciphertexts](#decrypt-ciphertexts)
* [Enforce Minimum Decryption Version](#enforce-minimum-decryption-version)
* [Conclusion](#conclusion)

## Overview

The Transit Secrets Engine provides cryptographic functions as a service. It allows you to offload encryption, decryption, key management, and more to Vault without storing raw data.

Learn more in the official docs: [Transit Secrets Engine](https://www.vaultproject.io/docs/secrets/transit).

## Verify Enabled Secrets Engines

First, check which secrets engines are active on your Vault dev server:

```bash theme={null}
vault secrets list
```

Expected output in dev mode:

| Path       | Type      | Description                              |
| ---------- | --------- | ---------------------------------------- |
| cubbyhole/ | cubbyhole | per-token private secret storage         |
| identity/  | identity  | identity store                           |
| secret/    | kv (v2)   | key/value secret storage                 |
| sys/       | system    | system endpoints for control & debugging |

<Callout icon="lightbulb">
  In Vault dev mode, the `cubbyhole/`, `identity/`, `secret/` (KV v2), and `sys/` engines are enabled by default.
</Callout>

## Enable the Transit Engine

Enable the Transit engine at the default path `transit/`:

```bash theme={null}
vault secrets enable transit
```

Verify it was added:

```bash theme={null}
vault secrets list
```

| Path     | Type    | Description |
| -------- | ------- | ----------- |
| transit/ | transit | n/a         |

You can also add a description when enabling:

```bash theme={null}
vault secrets disable transit
vault secrets enable -description="My transit engine" transit
vault secrets list
```

## Create and Inspect an Encryption Key

Create a new key named `training`:

```bash theme={null}
vault write -f transit/keys/training
```

Then read its configuration:

```bash theme={null}
vault read transit/keys/training
```

Key configuration highlights:

| Field                | Value        |
| -------------------- | ------------ |
| name                 | training     |
| type                 | aes256-gcm96 |
| latest\_version      | 1            |
| supports\_encryption | true         |
| supports\_decryption | true         |

## Rotate an Encryption Key

Rotate `training` to generate a new version:

```bash theme={null}
vault write -f transit/keys/training/rotate
```

Verify the version bump:

```bash theme={null}
vault read transit/keys/training | grep latest_version
