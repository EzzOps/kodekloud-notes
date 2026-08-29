# Demo Batch Tokens

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Scale-Vault-for-Performance/Demo-Batch-Tokens/page

This guide covers managing HashiCorp Vault Batch Tokens, including creation, revocation, inspection, and authentication.

In this guide, we’ll cover how to work with HashiCorp Vault Batch Tokens. You’ll learn how to inspect existing tokens, create and revoke service tokens, generate batch tokens (including orphaned ones), and understand their key characteristics. Finally, you’ll see how to authenticate using a batch token.

## Inspecting Existing Tokens

First, verify your current root token accessor:

```bash theme={null}
vault token lookup
```

Example output:

```text theme={null}
Key               Value
---               -----
accessor          HMqNT7nOPAsreghAyixLeRks
creation_time     1655409760
display_name      root
policies          [root]
type              service
```

List all token accessors in Vault:

```bash theme={null}
vault list auth/token/accessors
```

```text theme={null}
Keys
----
HMqNT7nOPAsreghAyixLeRks
```

Since only the root token exists, that accessor is the one you see.

## Creating and Revoking a Service Token

To create a standard service token with a specific policy:

```bash theme={null}
vault token create -policy=cloud-policy
```

Sample response:

```text theme={null}
Key                Value
---                -----
token              hvs.CAESIJBJBIUD...
token_accessor     3hwz8fd5p5U108UGxbeDb3D
token_duration     768h
renewable          true
policies           ["cloud-policy" "default"]
```

Now list accessors again:

```bash theme={null}
vault list auth/token/accessors
```

```text theme={null}
Keys
----
3hwz8fd5p5U108UGxbeDb3D
HMqNT7nOPAsreghAyixLeRks
```

Revoke the new service token by its accessor:

```bash theme={null}
vault token revoke -accessor 3hwz8fd5p5U108UGxbeDb3D
```

```text theme={null}
Success! Revoked token (if it existed)
```

Any login attempt with the revoked token fails:

```bash theme={null}
vault login hvs.CAESIJBJBIUD...
```

```text theme={null}
Error authenticating: permission denied
```

> **lightbulb** Granting `list` and `revoke` permissions on `auth/token/accessors` lets users revoke any token by accessor. Assign this capability with care.

## Creating a Batch Token

Batch tokens are designed for high-performance use cases. They are longer, non-renewable, and have no accessor.

```bash theme={null}
vault token create \
  -policy=cloud-policy \
  -type=batch \
  -ttl=24h
```

```text theme={null}
Key                Value
---                -----
token              hvb.AAAAAQJIifEa...
token_accessor     n/a
token_duration     24h
renewable          false
policies           ["cloud-policy" "default"]
```

* Prefix `hvb.` indicates a HashiCorp Vault Batch Token.
* No accessor means it won’t appear in `auth/token/accessors`.

### Inspecting the Batch Token

Retrieve its metadata:

```bash theme={null}
vault token lookup hvb.AAAAAQJIifEa...
```

```text theme={null}
Key               Value
---               -----
accessor          n/a
creation_ttl      24h
expire_time       2022-06-22T08:49:50Z
orphan            false
policies          [cloud-policy default]
renewable         false
type              batch
```

Because `orphan: false`, this token has a parent and cannot be used across performance-replicated clusters.

### Creating an Orphaned Batch Token

An orphaned batch token has no parent, making it usable across performance clusters:

```bash theme={null}
vault token create \
  -policy=cloud-policy \
  -type=batch \
  -ttl=24h \
  -orphan=true
```

Verify the orphan status:

```bash theme={null}
vault token lookup hvb.AAAAQL7ypVnQ...
```

```text theme={null}
Key               Value
---               -----
orphan            true
