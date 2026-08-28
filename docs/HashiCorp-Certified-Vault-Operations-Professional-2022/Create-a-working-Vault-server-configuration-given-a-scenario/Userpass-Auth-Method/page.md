# Success! Enabled the transit secrets engine at: transit/
```

Create an encryption key named `training`:

```bash theme={null}
vault write -f transit/keys/training
# Success! Data written to: transit/keys/training
```

Encrypt Base64-encoded data:

```bash theme={null}
vault write transit/encrypt/training \
  plaintext=$(base64 <<< "Getting Started with HashiCorp Vault")
# Key         Value
# ---         -----
# ciphertext  vault:v1:FYpph6C7r5MUILIiEiFhCoJBxelQbsGe...
# key_version 1
```

Decrypt ciphertext:

```bash theme={null}
vault write transit/decrypt/training \
  ciphertext="vault:v1:FYpph6C7r5MUILIiEiFhCoJBxelQbsGe..."
# Key       Value
# ---       -----
# plaintext R2V0dGluZyBTdGFydGVkIHdpdGggSGFzaGlDb3JwIFZhdWx0Cg==
```

***

## Rotating & Configuring Keys

Rotate a key (manual or via `auto_rotate_period`):

```bash theme={null}
vault write -f transit/keys/training/rotate
# Success! Data written to: transit/keys/training/rotate
```

Inspect key metadata:

```bash theme={null}
vault read transit/keys/training
# Key                   Value
# ---                   -----
# keys                  map[1:1647960245 2:1647960257 3:1647961177]
# latest_version        3
# min_decryption_version 1
# ...
```

Set the minimum decryptable version:

```bash theme={null}
vault write transit/keys/training/config \
  min_decryption_version=4
# Success! Data written to: transit/keys/training/config
```

Applications using ciphertext from versions below this threshold will be refused decryption.

<Frame>
  ![The image is a slide about key rotation in Vault, explaining the simplified process of rotating keys manually or automatically, and maintaining a versioned keyring for encryption keys. It includes details about setting rotation periods and limiting key versions for decryption.](https://kodekloud.com/kk-media/image/upload/v1752878512/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Transit-Secrets-Engine/key-rotation-vault-process-diagram.jpg)
</Frame>

## Rewrapping Ciphertexts

To upgrade existing ciphertext to the latest key version—without exposing plaintext—use `rewrap`:

```bash theme={null}
vault write transit/rewrap/training \
  ciphertext="vault:v1:FYpph6C7r5MUILIiEiFhCoJBxelQbsGe..."
# Key         Value
# ---         -----
# ciphertext  vault:v4:RPzp1kMpjtUIis+6qxrNjIE...
# key_version 4
```

Rewrap operations keep data protected entirely within Vault.

***

## Policy Example

Grant an application the ability to encrypt and decrypt using `training`:

```hcl theme={null}
# Encrypt capability
path "transit/encrypt/training" {
  capabilities = ["update"]
}

# Decrypt capability
path "transit/decrypt/training" {
  capabilities = ["update"]
}
```

***

## Links and References

* [HashiCorp Vault Transit Secrets Engine](https://www.vaultproject.io/docs/secrets/transit)
* [Vault HTTP API](https://www.vaultproject.io/api-docs)
* [Vault Tokens and Policies](https://www.vaultproject.io/docs/concepts/policies)
* [HashiCorp Certified: Vault Associate](https://www.hashicorp.com/certification/vault-associate)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/68f18ac2-9d11-4ca2-bd93-3e30f0cfdc37" />
</CardGroup>


# Userpass Auth Method

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Userpass-Auth-Method/page

The Userpass authentication method allows Vault clients to log in using a username and password stored in Vault for basic credential management.

The Userpass authentication method enables Vault clients to log in using a username and password stored in Vault itself. Since it doesn’t depend on an external identity provider, Userpass is perfect for quick labs, testing environments, and simple use cases where you need basic credential management without added complexity.

<Callout icon="triangle-alert">
  Userpass does not enforce password complexity, expiration, or rotation by default. For production workloads, consider integrating Vault with [external identity providers][vault-oidc] or LDAP.
</Callout>

## How It Works

<Frame>
  ![The image illustrates a "Userpass – Auth Workflow," showing a Vault user sending an authentication request with a username and password to a vault using the UserPass authentication method.](https://kodekloud.com/kk-media/image/upload/v1752878513/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Userpass-Auth-Method/userpass-auth-workflow-vault-diagram.jpg)
</Frame>

1. User provides **username** (e.g., `hcvop-engineer`) and **password**.
2. Vault validates credentials and issues a **token**.
3. The token is used to interact with Vault’s API and secrets engines.

## Configuration Workflow

<Frame>
  ![The image illustrates a "Userpass – Configuration Workflow" showing the steps for a Vault Admin to create a user, provide credentials, and authenticate, with an optional password change for a developer.](https://kodekloud.com/kk-media/image/upload/v1752878514/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Userpass-Auth-Method/userpass-configuration-workflow-vault-admin.jpg)
</Frame>

1. Vault Admin **enables** the `userpass` auth method.
2. Admin **creates** a user with policies and token settings.
3. Admin hands off credentials to the Developer.
4. Developer **logs in** and obtains a token.
5. Developer may **update** their password if allowed by policy.

## Enabling Userpass

```bash theme={null}
