# Managing Tokens using the API

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Managing-Tokens-using-the-API/page

This guide explains how to authenticate to Vault, retrieve and store a client token, and use it for API requests.

In this guide, you’ll learn how to authenticate to Vault using an auth method, extract the client token from the API response, store it securely, and use it for subsequent requests. All examples use [`jq`](https://stedolan.github.io/jq/) to parse JSON.

## 1. Authenticate and Retrieve a Client Token

When you log in (with any method other than token auth), Vault returns a JSON payload containing `auth.client_token`. Use `curl` to send your credentials:

```bash theme={null}
curl --request POST \
     --data @payload.json \
     http://127.0.0.1:8200/v1/auth/userpass/login/bryan | jq
```

Sample response:

```json theme={null}
{
  "request_id": "Ob4181fe-0dec-2261-5231-bb3f033387e5",
  "lease_id": "",
  "renewable": false,
  "auth": {
    "client_token": "s.WN54zL4c4wQJet9KS9KItkHW",
    "accessor": "zsapl3bBo0GzB5xVPZFEu3Th",
    "policies": ["default", "training"],
    "token_policies": ["default", "training"],
    "metadata": { "username": "bryan" },
    "lease_duration": 2764800,
    "renewable": true,
    "entity_id": "88669d54-b405-c27a-d468-410a1185eb0d",
    "token_type": "service",
    "orphan": true
  }
}
```

The value of `auth.client_token` is your Vault token for future API calls.

## 2. Store the Token

You have two common options for storing the token.

| Method      | Command Example                 | Pros & Cons                               |                                                 |
| ----------- | ------------------------------- | ----------------------------------------- | ----------------------------------------------- |
| File        | \`curl …                        | jq -r ".auth.client\_token" > token.txt\` | Easy persistence; file permissions are critical |
| Environment | \`export VAULT\_TOKEN=\$(curl … | jq -r ".auth.client\_token")\`            | Session-scoped; not persisted to disk           |

> **triangle-alert** Storing tokens in plain text files can expose secrets if file permissions aren’t locked down. Always enforce least-privilege access.

### 2.1 Save to a File

```bash theme={null}
curl --request POST \
     --data @payload.json \
     http://127.0.0.1:8200/v1/auth/userpass/login/bryan \
  | jq -r ".auth.client_token" > token.txt
