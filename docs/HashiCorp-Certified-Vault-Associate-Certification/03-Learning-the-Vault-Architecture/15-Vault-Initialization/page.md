# Top-level settings
api_addr     = "<address>"
ui           = true
cluster_name = "<name>"
```

* **listener**: Defines the API port, cluster port, and TLS options.
* **storage**: Configures where Vault persists its data.
* **seal**: Sets up the auto-unseal provider (e.g., KMS).
* **telemetry**: Controls metrics export.

Top-level parameters include:

* `api_addr`
* `cluster_addr`
* `ui`
* `cluster_name`
* `log_level`

### Basic Stanza Examples

```hcl theme={null}
listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = true    # Do NOT disable TLS in production
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "12345678-abcd-1234-abcd-123456789101"
}
```

* **listener**: Binds Vault to all interfaces on ports 8200 (API) and 8201 (cluster).
* **seal**: Configures AWS KMS for automatic unseal.

<Callout icon="triangle-alert">
  Disabling TLS (`tls_disable = true`) is insecure. Always enable TLS (`tls_disable = false`) in production and provide valid certificates.
</Callout>

## Production-Ready Configuration Example

Use this HCL template as a starting point for a highly available, production-grade Vault cluster:

```hcl theme={null}
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
  token   = "1a2b3c4d-1234-abdc-1234-1a2b3c4d5e6a"
}

listener "tcp" {
  address                  = "0.0.0.0:8200"
  cluster_address          = "0.0.0.0:8201"
  tls_disable              = false
  tls_cert_file            = "/etc/vault.d/client.pem"
  tls_key_file             = "/etc/vault.d/cert.key"
  tls_disable_client_certs = true
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "12345678-abcd-1234-abcd-123456789101"
  endpoint   = "example.kms.us-east-1.vpce.amazonaws.com"
}

api_addr     = "https://vault-us-east-1.example.com:8200"
cluster_addr = "https://node-us-east-1.example.com:8201"
cluster_name = "vault-prod-us-east-1"
ui           = true
log_level    = "INFO"
```

* **storage.consul**: Persists Vault data to a local Consul agent.
* **tls\_disable = false**: Enforces TLS; certificates must be valid.
* **seal.awskms.endpoint**: Uses a VPC endpoint for secure AWS KMS access.

## Vault Contents vs. Config File

The Vault configuration file does *not* manage:

* Secrets Engines
* Auth Methods
* Audit Devices (beyond file/device declaration)
* Vault Policies, Entities, and Groups

These resources are created **inside** Vault after initialization and unseal, using the CLI or API.

## Summary of Stanzas

| Stanza    | Required | Description                            |
| --------- | -------- | -------------------------------------- |
| listener  | Yes      | API and cluster bindings, TLS settings |
| storage   | Yes      | Backend for storing Vault data         |
| seal      | No\*     | Auto-unseal provider                   |
| telemetry | No       | Metrics publishing settings            |
| audit     | No       | Audit device declarations              |
| database  | No       | Database credentials rotation          |

\*Vault can run without an auto-unseal seal stanza, but manual unseal is required at each startup.

## Links & References

* [Vault Configuration Docs](https://www.vaultproject.io/docs/configuration)
* [HashiCorp Vault Getting Started](https://learn.hashicorp.com/vault)
* [Consul Storage Backend](https://www.vaultproject.io/docs/configuration/storage/consul)
* [AWS KMS Auto-Unseal](https://www.vaultproject.io/docs/secrets/aws)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/0ba0097f-db0a-4b08-9ddf-434cabaa2dc2" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/b4b46309-766d-4d7e-99f7-604811d3d563" />
</CardGroup>


# Vault Initialization

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Learning-the-Vault-Architecture/Vault-Initialization/page

Vault initialization prepares the storage backend to securely manage secrets by generating keys and issuing an initial root token.

Vault initialization is a one-time operation that prepares your storage backend to securely store and manage secrets. During this step, Vault generates encryption keys, shards them, and issues an initial root token. Initialization must be performed exactly once per Vault cluster—never re-initialize after a restore or node failure.

## What Happens During Initialization

When you run:

```bash theme={null}
$ vault operator init <options>
```

Vault will:

1. Generate a **master key** that encrypts the data-encryption key.
2. Create a **data-encryption key** for all subsequent operations.
3. Split the master key into key shares (using Shamir’s Secret Sharing) or generate recovery keys if an auto-unseal mechanism is enabled.
4. Issue the **initial root token** for first-time authentication.

<Callout icon="lightbulb">
  Initialization writes to your storage backend only once. If your cluster is lost or restored from backup, you skip initialization and go straight to unsealing.
</Callout>

## Key Shares, Thresholds, and Recovery Keys

By default:

* **Key shares**: 5
* **Threshold**: 3 (number of shares needed to unseal)

Customize these values:

```bash theme={null}
$ vault operator init \
    -key-shares=10 \
    -key-threshold=6
```

If you use a cloud KMS or HSM for auto-unseal, Vault generates **recovery keys** instead of traditional unseal keys. These recovery keys are only needed for manual recovery or re-sealing.

## Encrypting Unseal Keys and Root Token

Protect your unseal/recovery keys and root token with PGP encryption. Supply one or more public keys during initialization:

```bash theme={null}
$ vault operator init \
    -pgp-keys="alice_pubkey.pem" \
    -pgp-keys="bob_pubkey.pem"
```

Each key share (and the root token, optionally) is encrypted to the corresponding PGP public key. Only private key holders can decrypt them.

## Initialization Methods

Vault supports three initialization interfaces:

| Method | Use Case                                     | Example                                 |
| ------ | -------------------------------------------- | --------------------------------------- |
| CLI    | Stand up a new cluster or quick manual setup | `vault operator init`                   |
| API    | Automation workflows, CI/CD pipelines        | HTTP `PUT /v1/sys/init`                 |
| UI     | Interactive setup via Vault Web UI           | Navigate to **System → Initialization** |

### CLI Examples

Default initialization:

```bash theme={null}
$ vault operator init
```

Custom shares, threshold, and PGP encryption:

```bash theme={null}
$ vault operator init \
    -key-shares=7 \
    -key-threshold=4 \
    -pgp-keys="team1_pub.pem" \
    -pgp-keys="team2_pub.pem"
```

## Post-Initialization Steps

1. **Auto-Unseal**\
   Vault contacts the configured KMS/HSM and unseals automatically.
2. **Manual Unseal**\
   Supply unseal key shares on a single Vault node:
   ```bash theme={null}
   $ vault operator unseal <key-share-1>
   $ vault operator unseal <key-share-2>
   $ vault operator unseal <key-share-3>
   ```
3. **Authenticate**\
   Log in with the initial root token:
   ```bash theme={null}
   $ vault login <initial-root-token>
   ```

Once unsealed and authenticated, you can configure policies, enable secrets engines, and onboard applications.

***

## Links and References

* [Vault Initialization API](https://www.vaultproject.io/api-docs/system/init)
* [Shamir’s Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing)
* [Auto-Unseal with AWS KMS](https://www.vaultproject.io/docs/secrets/aws#auto-unseal)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/3c10741c-af07-473d-8249-ea46d0c22664" />
</CardGroup>
