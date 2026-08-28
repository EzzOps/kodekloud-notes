# Root Tokens

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Root-Tokens/page

This guide covers root tokens in Vault, their secure usage, and methods for generation or recovery.

In Vault, a **root token** is the ultimate superuser credential. It carries the `root` policy, granting unrestricted access to every Vault operation. This guide covers what root tokens are, how to use them securely, and the various ways to generate or recover them.

<Frame>
  ![The image is a slide about root tokens, explaining their unlimited access, lack of expiration, and best practices for usage and revocation. It includes colorful text highlights and a cartoon character in the corner.](https://kodekloud.com/kk-media/image/upload/v1752878001/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Root-Tokens/root-tokens-access-best-practices-slide.jpg)
</Frame>

## What Is a Root Token?

A root token:

* Carries the `root` policy, allowing any Vault operation
* Is non-renewable by default (`token_renewable=false`)
* Has no expiration (TTL is ∞)

Running a lookup against a root token shows:

```bash theme={null}
$ vault token lookup s.<root-token>
Key                Value
---                -----
token              s.<root-token>
token_duration     ∞
token_renewable    false
policies           ["root"]
```

<Callout icon="lightbulb">
  You can use an existing root token to create a new token with a finite TTL if desired.
</Callout>

## Best Practices for Root Tokens

Root tokens should be handled with extreme caution:

| Scenario             | Usage                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| Initial Setup        | Perform your Vault initialization tasks.                                                         |
| Testing Integrations | Validate new auth methods (e.g., [LDAP](https://ldap.com), [OIDC](https://openid.net/connect/)). |
| Emergency Recovery   | Regenerate in a crisis when standard auth is unavailable.                                        |

<Callout icon="triangle-alert">
  Root tokens grant unlimited access. Always revoke them immediately after use to avoid security risks:

  ```bash theme={null}
  $ vault token revoke s.<root-token>
  Success! Revoked token (if it existed)
  ```
</Callout>

## Generating Root Tokens

You can obtain a root token through three primary methods:

| Method                     | When to Use                             | Command                        |
| -------------------------- | --------------------------------------- | ------------------------------ |
| Initialization             | First-time Vault setup                  | `vault operator init`          |
| Using an Existing Token    | Create additional root-level tokens     | `vault token create`           |
| Using Unseal/Recovery Keys | Emergency recovery when Vault is sealed | `vault operator generate-root` |

### 1. Initialization

During Vault initialization, the CLI outputs your initial root token:

```bash theme={null}
$ vault operator init
