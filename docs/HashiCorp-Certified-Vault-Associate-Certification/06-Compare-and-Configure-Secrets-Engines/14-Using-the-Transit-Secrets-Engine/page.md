# Using the Transit Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-and-Configure-Secrets-Engines/Using-the-Transit-Secrets-Engine/page

This guide explains how to enable and use the Transit Secrets Engine in HashiCorp Vault for secure data encryption workflows.

In this guide, you’ll learn how to enable and use the Transit Secrets Engine in HashiCorp Vault for secure data encryption workflows. We’ll cover:

* Enabling the engine
* Creating and managing encryption keys
* Encrypting and decrypting data
* Rotating keys and setting decryption constraints
* Rewrapping ciphertext to the latest key version

***

## Prerequisites

> **lightbulb** Make sure you have:

  * Vault CLI installed and authenticated (`VAULT_ADDR` & token configured).
  * A running Vault server (Dev mode or Production).

***

## 1. Enable the Transit Secrets Engine

By default, the Transit engine mounts at `transit/`. To enable it:

```bash theme={null}
vault secrets enable transit
