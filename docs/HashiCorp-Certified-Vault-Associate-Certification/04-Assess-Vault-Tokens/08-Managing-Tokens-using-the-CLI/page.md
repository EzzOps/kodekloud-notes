# Verify
cat token.txt
# s.dhtIk8VsE3Mj61PuGP3ZfFrg
```

### 2.2 Save to an Environment Variable

```bash theme={null}
OUTPUT=$(curl --request POST \
              --data @payload.json \
              http://127.0.0.1:8200/v1/auth/userpass/login/bryan)

export VAULT_TOKEN=$(echo "$OUTPUT" | jq -r '.auth.client_token')

echo "$VAULT_TOKEN"
# s.dhtIk8VsE3Mj61PuGP3ZfFrg
```

## 3. Use the Token in API Requests

Vault supports two header styles for passing the token. Choose one:

| Header Style  | Example                                   |
| ------------- | ----------------------------------------- |
| X-Vault-Token | `-H "X-Vault-Token: $VAULT_TOKEN"`        |
| Authorization | `-H "Authorization: Bearer $VAULT_TOKEN"` |

> The most common practice is to use **X-Vault-Token**.

### 3.1 Write a Secret

```bash theme={null}
curl --header "X-Vault-Token: $VAULT_TOKEN" \
     --request POST \
     --data '{ "apikey": "3230sc$832d" }' \
     https://vault.example.com:8200/v1/secret/apikey/splunk
```

### 3.2 Read a Secret

```bash theme={null}
curl --header "X-Vault-Token: $VAULT_TOKEN" \
     --request GET \
     https://vault.example.com:8200/v1/secret/data/apikey/splunk
```

That’s it! Authenticate, extract `auth.client_token`, store it securely, and include it in the header for all Vault API calls.

## Links and References

* [Vault HTTP API Documentation](https://www.vaultproject.io/api-docs)
* [jq Tool Documentation](https://stedolan.github.io/jq/)
* [Vault Authentication Methods](https://www.vaultproject.io/docs/auth)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/f641b172-da5d-457d-853a-2080dc00b4f8)


# Managing Tokens using the CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Managing-Tokens-using-the-CLI/page

This article explains how to manage Vault tokens using the CLI for authentication and access control in HashiCorp Vault.

Vault tokens are the primary authentication mechanism for interacting with HashiCorp Vault. Using the Vault CLI, you can create, inspect, renew, revoke, and check capabilities of tokens to tailor access control for your applications and users.

## Table of Contents

1. [Creating a Token](#1-creating-a-token)
2. [Looking Up a Token](#2-looking-up-a-token)
3. [Renewing a Token](#3-renewing-a-token)
4. [Revoking a Token](#4-revoking-a-token)
5. [Checking Token Capabilities](#5-checking-token-capabilities)
6. [References](#6-references)

***

## 1. Creating a Token

Use the `vault token create` command to generate a new token with a specified TTL (time-to-live) and attached policies.

```bash theme={null}
vault token create \
  -ttl=5m \
  -policy=training
```

Example output:

```text theme={null}
Key                  Value
---                  -----
token                s.12VNpg4OA9tTdCd4V60DuDRK
token_accessor       lMIaz4Tn1t57wKXdsfNv7vlm
token_duration       5m
token_renewable      true
policies             ["default" "training"]
```

| Property         | Description                                               |
| ---------------- | --------------------------------------------------------- |
| token            | Authentication token string                               |
| token\_accessor  | String used to renew or revoke without exposing the token |
| token\_duration  | Initial TTL before expiration                             |
| token\_renewable | Indicates if the token can be renewed                     |
| policies         | List of Vault policies attached to the token              |

> **lightbulb** You can further customize a token with `-display_name`, multiple policies, and an explicit maximum TTL.

```bash theme={null}
vault token create \
  -display_name=jenkins \
  -policy=training,certs \
  -ttl=24h \
  -explicit-max-ttl=72h
```

* `-display_name`: Human-friendly identifier
* `-policy`: Comma-separated Vault policies
* `-ttl`: Initial lifetime (e.g., `24h`)
* `-explicit-max-ttl`: Maximum lifetime across renewals

***

## 2. Looking Up a Token

Inspect metadata for any token by running:

```bash theme={null}
vault token lookup <token-or-accessor>
```

Example:

```bash theme={null}
vault token lookup s.12VNpg4OA9tTdCd4V60DuDRK
```

```text theme={null}
Key               Value
---               -----
accessor          lMIaz4Tn1t57wKXdsfNv7vlm
creation_time     1630613718
creation_ttl      5m
display_name      jenkins
expire_time       2021-09-02T16:23:02Z
explicit_max_ttl  72h
id                s.12VNpg4OA9tTd4V60DuDRK
issue_time        2021-09-02T16:15:18Z
last_renewal      2021-09-02T16:18:02Z
num_uses          0
orphan            false
path              auth/token/create
policies          [default training certs]
renewable         true
ttl               3m12s
type              service
```

If you omit the identifier, Vault returns details for the token in your `$VAULT_TOKEN`:

```bash theme={null}
vault token lookup
```

***

## 3. Renewing a Token

Extend a token’s TTL using `vault token renew`. You can renew by token ID or accessor:

```bash theme={null}
