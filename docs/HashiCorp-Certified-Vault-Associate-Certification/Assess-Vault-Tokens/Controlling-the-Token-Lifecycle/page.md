# Controlling the Token Lifecycle

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Controlling-the-Token-Lifecycle/page

This guide explains managing token lifecycles in HashiCorp Vault, covering periodic, usage-limited, and orphan tokens for secure access.

Managing tokens effectively is crucial for secure, reliable access to Vault. By choosing the right token type, you can tailor authentication lifecycles to your application’s needs. This guide covers three core scenarios and shows you how to create:

* Periodic service tokens for long-running applications
* Service tokens with usage limits for sensitive actions
* Orphan tokens with independent lifecycles

## Periodic Service Tokens

For legacy or long-running applications that cannot handle token rotation, a **periodic service token** is ideal. It has a finite Time-To-Live (TTL) but no maximum TTL, so you can renew it indefinitely without changing the token string.

<Callout icon="lightbulb">
  Periodic service tokens allow your application to continue using the same token for as long as needed, avoiding code changes for token refresh.
</Callout>

```bash theme={null}
vault token create \
  -policy="your-policy" \
  -period="24h"
```

<Frame>
  ![The image shows an app developer expressing a concern about a long-running app that cannot handle token regeneration, with a suggestion to use a periodic service token.](https://kodekloud.com/kk-media/image/upload/v1752877974/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Controlling-the-Token-Lifecycle/app-developer-token-regeneration-concern.jpg)
</Frame>

## Service Tokens with Usage Limits

When you need a token to expire automatically after a set number of uses—such as for one-time administrative tasks—use a **service token** with the `num_uses` parameter. Vault revokes the token once it hits the usage threshold.

```bash theme={null}
vault token create \
  -policy="sensitive-action" \
  -num_uses=3
```

<Frame>
  ![The image shows a cartoon of a principal engineer requesting a token that revokes automatically after one use, with a suggestion to use a service token with a use limit.](https://kodekloud.com/kk-media/image/upload/v1752877975/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Controlling-the-Token-Lifecycle/principal-engineer-token-request-cartoon.jpg)
</Frame>

## Orphan Tokens

To prevent your token’s lifecycle from being tied to a parent token—ensuring its expiration or revocation only follows its own rules—create an **orphan token**. This token has no parent relationship, giving you full control over its lifecycle.

<Callout icon="triangle-alert">
  Orphan tokens are not revoked automatically with their parent. Always plan for manual revocation to avoid orphaned credentials.
</Callout>

```bash theme={null}
vault token create \
  -policy="independent-policy" \
  -orphan
```

<Frame>
  ![The image shows a cartoon character labeled "DevOps Engineer" expressing a concern about token expiration being influenced by its parent, under the title "Controlling Token Lifecycle."](https://kodekloud.com/kk-media/image/upload/v1752877977/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Controlling-the-Token-Lifecycle/devops-engineer-token-lifecycle-concern.jpg)
</Frame>

## Summary Table

Below is a quick reference comparing each token type, its primary use case, and example CLI commands.

| Token Type                     | Use Case                                     | Example CLI                                                 |
| ------------------------------ | -------------------------------------------- | ----------------------------------------------------------- |
| Periodic Service Token         | Long-running apps needing indefinite renewal | `vault token create -policy="your-policy" -period="24h"`    |
| Service Token with Usage Limit | One-time or limited-use operations           | `vault token create -policy="sensitive-action" -num_uses=3` |
| Orphan Token                   | Independent lifecycle, unaffected by parents | `vault token create -policy="independent-policy" -orphan`   |

<Frame>
  ![The image is a slide titled "Controlling Token Lifecycle" with a table summarizing challenges and solutions related to token management. It includes solutions like "Periodic Service Token" and "Orphan Service Token" for specific challenges.](https://kodekloud.com/kk-media/image/upload/v1752877978/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Controlling-the-Token-Lifecycle/controlling-token-lifecycle-challenges-solutions.jpg)
</Frame>

## Links and References

* [HashiCorp Vault Token Documentation](https://www.vaultproject.io/docs/concepts/tokens)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/cfadffc4-211b-436d-97d9-066c6abff97f" />
</CardGroup>
