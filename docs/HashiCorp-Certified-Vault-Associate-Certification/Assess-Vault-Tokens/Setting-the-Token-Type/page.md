# Perform a Vault operation with the token...
vault kv get secret/my-app

# Then re-check the token
vault token lookup s.abc123xyz
```

```bash theme={null}
Key           Value
---           -----
id            s.abc123xyz
ttl           23h00m
num_uses      2
```

Repeat until `num_uses` reaches `0`.

## Summary

By defining both a TTL and a `-use-limit`, Vault tokens can expire on whichever limit is reached first—time or uses. This adds a robust safeguard against token misuse, replay attacks, and unintended long-lived credentials.

## Links and References

* [Vault Token Tuning](https://www.vaultproject.io/docs/concepts/tokens#token-tuning)
* [Vault Token CLI Commands](https://www.vaultproject.io/docs/commands/token)
* [Vault Best Practices](https://www.vaultproject.io/docs/best-practices)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/966e8b59-f69f-4d8f-8bed-95aedc4091be" />
</CardGroup>


# Setting the Token Type

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Setting-the-Token-Type/page

This article explains how to create and configure token types in Vault using CLI and authentication methods.

When you create a Vault token, you control its lifecycle and capabilities by specifying its type and duration. You can do this either directly via the CLI/API or by configuring an authentication method such as AppRole.

## 1. Creating Tokens via CLI

Use `vault token create` flags to define token type, TTL, and renewal behavior.

### Common Flags

| Flag      | Purpose                                         | Example         |
| --------- | ----------------------------------------------- | --------------- |
| `-type`   | Specifies the token type (`service` or `batch`) | `-type="batch"` |
| `-ttl`    | Sets a time-to-live (non-renewable)             | `-ttl="60s"`    |
| `-period` | Creates a renewable (periodic) token            | `-period="24h"` |

<Callout icon="lightbulb">
  By default, Vault issues a non-renewable **service** token when no `-type` or `-period` is provided.
</Callout>

### Example: Periodic Token (24h)

```bash theme={null}
vault token create \
  -policy="training" \
  -period="24h"
```

Output:

```text theme={null}
Key                 Value
---                 -----
token               s.2kjqZl2ofDr3efPdtMJ1z5dZ
token_accessor      73rjN1kmnzW7lpMw9H7p6P9
token_duration      24h
token_renewable     true
token_policies      ["default" "training"]
identity_policies   []
policies            ["default" "training"]
```

* The `-period="24h"` flag makes the token **periodic** and renewable.
* Omit `-period` to create a one-time service token.
* Use `-type="batch"` with `-ttl` to generate a batch token.

## 2. Configuring Token Types in an Auth Method

You can predefine token types for roles within an auth method. This example uses [AppRole Auth Method](https://www.vaultproject.io/docs/auth/approle):

1. **Enable AppRole**
   ```bash theme={null}
   vault auth enable approle
   ```

2. **Create Roles with Specific Token Settings**

   * **Batch Token Role (TTL = 60s)**
     ```bash theme={null}
     vault write auth/approle/role/training \
       policies="training" \
       token_type="batch" \
       token_ttl="60s"
     ```

   * **Periodic Token Role (Period = 72h)**
     ```bash theme={null}
     vault write auth/approle/role/jenkins \
       policies="jenkins" \
       period="72h"
     ```

| Role     | Token Type         | Duration        | Description                            |
| -------- | ------------------ | --------------- | -------------------------------------- |
| training | batch              | 60s (TTL)       | Short-lived, non-renewable batch token |
| jenkins  | service → periodic | 72h (renewable) | Renewable periodic service token       |

<Callout icon="triangle-alert">
  Roles without an explicit `token_type` default to **service** tokens. Ensure you set `token_type` or `period` for the desired behavior.
</Callout>

## Summary

You have two methods to control Vault token types and lifecycles:

* **CLI/API Flags**:
  * `-type` for service or batch
  * `-ttl` for non-renewable duration
  * `-period` for renewable tokens

* **Auth Method Configuration**:
  * Set `token_type`, `token_ttl`, and `period` in role definitions

By using these techniques, you can ensure Vault issues tokens that match your security and operational requirements.

***

## Links and References

* [Vault Tokens](https://www.vaultproject.io/docs/concepts/tokens)
* [AppRole Auth Method](https://www.vaultproject.io/docs/auth/approle)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/f03aba50-5092-49f2-9afa-d27fac80c53a" />
</CardGroup>
