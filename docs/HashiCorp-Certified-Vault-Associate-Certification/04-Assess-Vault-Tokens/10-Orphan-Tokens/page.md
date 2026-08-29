# Check Vault status via CLI
export VAULT_TOKEN=<your-copied-token>
vault status
```

```shell theme={null}
# Query Vault health endpoint via API
curl \
  --header "X-Vault-Token: $VAULT_TOKEN" \
  http://127.0.0.1:8200/v1/sys/health
```

These examples demonstrate how easy it is to switch from the UI to scripted workflows.

## References

* [Vault UI Overview](https://www.vaultproject.io/docs/getting-started/ui)
* [Vault Authentication Methods](https://www.vaultproject.io/docs/auth)
* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/a5ce78d5-1851-4f25-a69b-2fe15446ae3c)


# Orphan Tokens

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Orphan-Tokens/page

Orphan tokens in HashiCorp Vault are independent credentials not tied to parent tokens, with configurable TTL and renewal options.

Orphan tokens in HashiCorp Vault provide an independent authentication credential outside the standard parent–child token hierarchy. Unlike regular child tokens, an orphan token’s lifecycle isn’t tied to a parent token’s expiration. However, it still adheres to its own configurable TTL and can be renewed just like any other token.

## Why Use Orphan Tokens?

| Token Type   | Parent Relationship | Expiry Behavior                                         |
| ------------ | ------------------- | ------------------------------------------------------- |
| Child Token  | Linked              | Expires automatically when its parent token expires.    |
| Orphan Token | Unlinked            | Expires only when its own TTL elapses or isn’t renewed. |

> **lightbulb** Orphan tokens can still be revoked manually or automatically when their own `max_ttl` is reached. Make sure to configure TTL settings according to your security requirements.

## Required Privileges

To create an orphan token, your Vault policy must grant access to the `auth/token/create-orphan` endpoint with `sudo` capabilities, along with general token creation rights:

```hcl theme={null}
path "auth/token/create-orphan" {
  capabilities = [ "create", "read", "update", "delete", "sudo" ]
}
```

> **triangle-alert** Creating orphan tokens typically requires a root token or a token with elevated `sudo` privileges. Use with caution to avoid unintended privilege escalation.

## Creating an Orphan Token

Run the `vault token create` command with the `-orphan` flag to generate an orphan token. You can also attach policies at creation:

```bash theme={null}
vault token create -policy="training" -orphan
```

Example output:

```text theme={null}
Key         Value
---         -----
token       s.3rPJCQbGWD906uybtTuojjFs
```

## Inspecting an Orphan Token

Verify that your token is indeed an orphan by using `vault token lookup`:

```bash theme={null}
vault token lookup s.3rPJCQbGWD906uybtTuojjFs
```

Example response:

```text theme={null}
Key         Value
---         -----
id          s.3rPJCQbGWD906uybtTuojjFs
issue_time  2018-12-13T18:35:41.02532-08:00
meta        <nil>
num_uses    0
orphan      true
```

The `orphan = true` field confirms the token is not part of the parent–child hierarchy.

## Links and References

* [Vault Tokens Overview](https://www.vaultproject.io/docs/concepts/token)
* [Token Authentication](https://www.vaultproject.io/docs/concepts/auth)
* [HCL Syntax Guide](https://github.com/hashicorp/hcl)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/e1272f3e-9fd3-4465-ab72-f9c0709339e8)
