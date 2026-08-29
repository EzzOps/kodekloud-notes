# Configuring Auth Methods using the API

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Configuring-Auth-Methods-using-the-API/page

Learn to configure AppRole authentication in HashiCorp Vault using API calls for enabling, creating roles, and authenticating with credentials.

## Introduction

Learn how to configure the [AppRole authentication method][vault-approle-docs] in HashiCorp Vault using direct API calls. This guide covers:

* Enabling the AppRole auth method
* Creating an AppRole with specific policies
* Retrieving the `Role ID` and `Secret ID`
* Authenticating with the generated credentials

## Prerequisites

* A running Vault server at `http://127.0.0.1:8200`
* A valid Vault token exported as an environment variable:

```bash theme={null}
export VAULT_TOKEN="s.TEKrNn3Cv53pZdbPh8xg4TPu"
```

<Callout icon="triangle-alert">
  Never commit your `VAULT_TOKEN` or any sensitive credentials to version control.
</Callout>

## 1. Enable the AppRole Auth Method

First, enable the AppRole authentication backend:

1. Create an `auth.json` file:

   ```json theme={null}
   {
     "type": "approle"
   }
   ```

2. Use `curl` to enable AppRole:

   ```bash theme={null}
   curl --header "X-Vault-Token: $VAULT_TOKEN" \
        --request POST \
        --data @auth.json \
        http://127.0.0.1:8200/v1/sys/auth/approle
   ```

3. Verify the mount:

   ```bash theme={null}
   vault auth list
   ```

You should see an entry for `approle/`.

## 2. Create an AppRole with Policies

Define which policies this AppRole will use:

1. Create `policies.json`:

   ```json theme={null}
   {
     "policies": ["bryan"]
   }
   ```

2. Create the AppRole named `vaultcourse`:

   ```bash theme={null}
   curl --header "X-Vault-Token: $VAULT_TOKEN" \
        --request POST \
        --data @policies.json \
        http://127.0.0.1:8200/v1/auth/approle/role/vaultcourse
   ```

A successful response confirms the role is created.

## 3. Fetch the Role ID

Each AppRole has a unique `Role ID`. Retrieve it:

```bash theme={null}
curl --header "X-Vault-Token: $VAULT_TOKEN" \
     http://127.0.0.1:8200/v1/auth/approle/role/vaultcourse/role-id | jq
```

Inspect `data.role_id` in the JSON response.

## 4. Generate a Secret ID

Generate the `Secret ID` needed alongside the `Role ID`:

```bash theme={null}
curl --header "X-Vault-Token: $VAULT_TOKEN" \
     --request POST \
     http://127.0.0.1:8200/v1/auth/approle/role/vaultcourse/secret-id | jq
```

The response returns:

* `data.secret_id`
* `data.secret_id_accessor`

With these credentials, you can log in:

```bash theme={null}
curl --request POST \
     --data '{"role_id":"<ROLE_ID>","secret_id":"<SECRET_ID>"}' \
     http://127.0.0.1:8200/v1/auth/approle/login
```

## Quick Reference Table

| Step | Endpoint                                      | Method | Description                                  |
| ---- | --------------------------------------------- | ------ | -------------------------------------------- |
| 1    | `/v1/sys/auth/approle`                        | POST   | Enable AppRole auth method                   |
| 2    | `/v1/auth/approle/role/vaultcourse`           | POST   | Create an AppRole with specified policies    |
| 3    | `/v1/auth/approle/role/vaultcourse/role-id`   | GET    | Retrieve the AppRole `Role ID`               |
| 4    | `/v1/auth/approle/role/vaultcourse/secret-id` | POST   | Generate the `Secret ID`                     |
| 5    | `/v1/auth/approle/login`                      | POST   | Authenticate using `Role ID` and `Secret ID` |

## Links and References

* [Vault AppRole Auth Method Documentation][vault-approle-docs]
* [Vault API Reference][vault-api-docs]
* [HashiCorp Vault GitHub](https://github.com/hashicorp/vault)

[vault-approle-docs]: https://www.vaultproject.io/docs/auth/approle

[vault-api-docs]: https://www.vaultproject.io/api-docs

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/e0610499-3eec-4296-9fcf-876e7cc458d5" />
</CardGroup>
