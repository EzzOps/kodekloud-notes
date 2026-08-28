# Demo Running Vault Dev Server

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Installing-Vault/Demo-Running-Vault-Dev-Server/page

This tutorial demonstrates launching HashiCorp Vault in development mode on a local machine for demos, testing, or learning purposes.

In this tutorial, we’ll demonstrate how to launch HashiCorp Vault in **development mode** on your local machine. Dev mode is perfect for demos, testing integrations, or learning Vault—it runs entirely in-memory, starts unsealed, and provides a single unseal key and root token.

<Callout icon="triangle-alert">
  **Dev mode is not secure.** Do **not** use it in production environments.
</Callout>

***

## Prerequisites

Before you begin:

* Vault CLI installed and in your `PATH`.
* Windows PowerShell or Command Prompt (for Windows users).

Verify your installation:

```powershell theme={null}
PS C:\> vault version
Vault v1.7.0 ([SECRET_REDACTED])
```

***

## 1. Starting Vault in Dev Mode

In a new shell (PowerShell or cmd), start Vault:

```powershell theme={null}
vault server -dev
```

You should see output similar to:

```text theme={null}
WARNING! Dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variable:

PowerShell:
  $env:VAULT_ADDR="http://127.0.0.1:8200"
cmd.exe:
  set VAULT_ADDR=http://127.0.0.1:8200

Unseal Key: [SECRET_REDACTED]=
Root Token: s.d6931rVSdkpBINnnRvMHBRXR

Development mode should NOT be used in production installations!
```

<Callout icon="lightbulb">
  This command runs Vault in the foreground. Open a **second** terminal window to interact with Vault without stopping the server.
</Callout>

***

## 2. Configuring Your Environment

By default, Vault listens on `https://127.0.0.1:8200`, but dev mode uses HTTP. Configure the `VAULT_ADDR` variable accordingly:

PowerShell:

```powershell theme={null}
PS C:\> $env:VAULT_ADDR = "http://127.0.0.1:8200"
```

Command Prompt:

```cmd theme={null}
C:\> set VAULT_ADDR=http://127.0.0.1:8200
```

***

## 3. Checking Vault Status

Confirm Vault is unsealed and running in-memory:

```bash theme={null}
vault status
```

Example output:

```text theme={null}
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.7.0
Storage Type    inmem
Cluster Name    vault-cluster-48151c3a
HA Enabled      false
```

Notice `Storage Type: inmem`—all data resides in memory.

***

## 4. Listing Enabled Secrets Engines

Dev mode automatically enables several secrets engines. View them with:

```bash theme={null}
vault secrets list
```

| Path       | Type      | Description                                |
| ---------- | --------- | ------------------------------------------ |
| cubbyhole/ | cubbyhole | Per-token private secret storage           |
| identity/  | identity  | Identity store                             |
| secret/    | kv        | Versioned key/value secret storage (KV v2) |
| sys/       | system    | System endpoints for control and debugging |

***

## 5. Writing and Reading KV Secrets

The KV (Key/Value) engine is mounted at `secret/`.

1. **Write** a secret:

   ```bash theme={null}
   vault kv put secret/vaultcourse/bryan bryan=bryan
   ```

   Sample response:

   ```text theme={null}
   Key            Value
   ---            -----
   created_time   2021-05-12T12:27:09.504562727Z
   deletion_time  n/a
   destroyed      false
   version        1
   ```

2. **Read** the secret back:

   ```bash theme={null}
   vault kv get secret/vaultcourse/bryan
   ```

   Example output:

   ```text theme={null}
   === Metadata ===
   Key            Value
   ---            -----
   created_time   2021-05-12T12:27:09.504562727Z
   deletion_time  n/a
   destroyed      false
   version        1

   === Data ===
   Key    Value
   ---    -----
   bryan  bryan
   ```

***

## 6. Cleaning Up

When you stop the dev server (e.g., `Ctrl+C`), all in-memory data is lost—ideal for ephemeral testing.

<Callout icon="lightbulb">
  Every restart returns Vault to a clean slate.
</Callout>

***

## Next Steps

* Explore additional [Vault Dev Mode capabilities](https://www.vaultproject.io/docs/commands/server#dev-server).
* Integrate with the [AWS Secrets Engine](https://www.vaultproject.io/docs/secrets/aws) for dynamic credentials.
* Practice writing policies and managing access control in dev mode.

***

## Links and References

* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands)
* [Vault Secrets Engines](https://www.vaultproject.io/docs/secrets)
* [Getting Started with Vault](https://learn.hashicorp.com/vault)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/a5a3d715-00ac-4573-aa63-061912aafce2/lesson/ff6a4647-f0d0-4128-adc1-234a4cf0e060" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/a5a3d715-00ac-4573-aa63-061912aafce2/lesson/1570bd34-be02-4233-a742-17dc75862e3d" />
</CardGroup>
