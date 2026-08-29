# Demo Cubbyhole Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Cubbyhole-Secrets-Engine/page

Learn to use Vault’s Cubbyhole Secrets Engine for data isolation and Response Wrapping for secure, one-time secret delivery.

In this tutorial, you’ll learn how to leverage Vault’s **Cubbyhole Secrets Engine** for per-token data isolation and use **Response Wrapping** for secure, one-time delivery of secrets. We’ll cover:

* Writing and reading token-specific cubbyhole data
* Proving isolation between tokens
* Populating and protecting a KV secret
* Generating and unwrapping a wrapped secret both via CLI and UI

## Prerequisites

* Vault 1.10.0 Enterprise installed locally (initialized & unsealed)
* Environment variable: `VAULT_ADDR=http://127.0.0.1:8200`
* Familiarity with basic Vault concepts ([Vault Overview][vault-overview])

## 1. Verify Vault Status

```bash theme={null}
vault status
```

Expected output:

```text theme={null}
Key                         Value
---                         -----
Recovery Seal Type          shamir
Initialized                 true
Sealed                      false
Version                     1.10.0+ent
Storage Type                raft
HA Enabled                  true
```

## 2. Authenticate as Root

```bash theme={null}
vault login <root_token>
```

> Success! You are now authenticated as the root user.

## 3. Create an Unprivileged Token

Create a token with only the `default` policy:

```bash theme={null}
vault token create -policy=default
```

Output:

```text theme={null}
Key             Value
---             -----
token           hv.s.XXXXXXXXXXXXXX
token_accessor  NuBg8k455X2yQERKgRxV3134
token_policies  ["default"]
```

Save the token value and log in with it:

```bash theme={null}
vault login hv.s.XXXXXXXXXXXXXX
```

> Success! You are now authenticated with limited permissions.

## 4. Working with Cubbyhole

Every token receives a private cubbyhole path. Only the token owner can write/read its own cubbyhole.

### 4.1 Write to Cubbyhole

```bash theme={null}
vault write cubbyhole/training certification=hcvop
```

### 4.2 Read from Cubbyhole

```bash theme={null}
vault read cubbyhole/training
```

```text theme={null}
Key             Value
---             -----
certification   hcvop
```

### 4.3 Proving Token Isolation

<Callout icon="lightbulb">
  Cubbyhole paths are isolated per token. No token can access another token’s cubbyhole.
</Callout>

1. **Switch back to root**
   ```bash theme={null}
   vault login <root_token>
   ```
2. **Attempt to read the unprivileged token’s cubbyhole**
   ```bash theme={null}
   vault read cubbyhole/training
   ```
   Output: `No value found at cubbyhole/training`
3. **Confirm unprivileged token can still read its own data**
   ```bash theme={null}
   vault login hv.s.XXXXXXXXXXXXXX
   vault read cubbyhole/training
   ```

## 5. KV Secrets Engine & Access Control

Next, we’ll show how an unprivileged token is denied access to KV secrets written by root.

| Token Type         | Accessible Path | Permissions          |
| ------------------ | --------------- | -------------------- |
| Root Token         | secret/data/\*  | read, write, delete  |
| Unprivileged Token | cubbyhole/\*    | read, write own only |

### 5.1 As Root: Write a KV Secret

```bash theme={null}
vault kv put secret/training goal=hcvop
```

### 5.2 As Root: Read the KV Secret

```bash theme={null}
vault kv get secret/training
```

```text theme={null}
====== Secret Path ======
secret/data/training

=== Data ===
Key    Value
---    -----
goal   hcvop
```

### 5.3 Denied Access for Unprivileged Token

```bash theme={null}
vault login hv.s.XXXXXXXXXXXXXX
vault kv get secret/training
```

```text theme={null}
Error making API request.
Code: 403. Errors:
* permission denied on path "secret/data/training"
```

## 6. Response Wrapping

Response wrapping provides a one-time-use, time-limited wrapping token for secure secret transfer.

### 6.1 Generate a Wrapping Token

As root, request a 60-minute wrapped response:

```bash theme={null}
vault kv get -wrap-ttl=60m secret/training
```

```text theme={null}
Key                           Value
---                           -----
wrapping_token                hvs.CAESIHHiPSBDnG75y4hN...  
wrapping_token_ttl            1h
wrapping_token_creation_path  secret/data/training
```

### 6.2 Inspect the Wrapping Token

```bash theme={null}
vault token lookup hvs.CAESIHHiPSBDnG75y4hN...
```

```text theme={null}
Key        Value
---        -----
path       secret/data/training
policies   [response-wrapping]
ttl        59m30s
num_uses   1
```

### 6.3 Unwrap as Unprivileged User

1. Log in with the limited token:
   ```bash theme={null}
   vault login hv.s.XXXXXXXXXXXXXX
   ```
2. Unwrap the secret:
   ```bash theme={null}
   vault unwrap hvs.CAESIHHiPSBDnG75y4hN...
   ```
   ```text theme={null}
   Key      Value
   ---      -----
   data     map[goal:hcvop]
   metadata map[created_time:... version:1]
   ```

### 6.4 TTL & One-Time Use Demonstration

```bash theme={null}
vault kv get -wrap-ttl=5s secret/training
