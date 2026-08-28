# Token Hierarchy

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Token-Hierarchy/page

This article explains how HashiCorp Vault manages token TTL, renewal, revocation, and the relationships in a token hierarchy for secure deployments.

In this lesson, we’ll dive into how HashiCorp Vault manages token time-to-live (TTL), renewal, revocation, and the parent-child relationships that form a token hierarchy. Understanding these concepts is essential for secure, scalable Vault deployments.

<Frame>
  ![The image is a slide titled "Token Hierarchy," explaining the concept of token time-to-live (TTL) and revocation, with a note that root tokens have no TTL and a sad face emoji.](https://kodekloud.com/kk-media/image/upload/v1752878005/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Token-Hierarchy/token-hierarchy-ttl-revocation-slide.jpg)
</Frame>

## Token TTL and Renewal

Every Vault token is issued with a TTL—the duration after which Vault automatically revokes the token. The initial root token is the exception, as it has no TTL by default (though you can configure a TTL for additional root tokens).

| Scenario                                 | Description                                                                              |
| ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| Token TTL = 1 hour; Max Renewable = 24 h | Must renew within 1 hour. Each renewal resets the TTL until 24 hours total have elapsed. |
| Renewal before TTL expiry                | Resets the TTL back to its original value, up to the maximum renewable period.           |
| Exceeding Max Renewable Period           | Vault permanently revokes the token, regardless of further renewal attempts.             |

<Callout icon="lightbulb">
  Root tokens have no TTL by default. Use `vault token create -policy="root" -ttl="48h"` to issue a root token with a custom TTL.
</Callout>

## Manual Revocation

You can revoke tokens on demand using either the Vault CLI or the HTTP API. Immediate revocation invalidates the token and its descendants.

| Method   | Command / Endpoint                                         |
| -------- | ---------------------------------------------------------- |
| CLI      | `vault token revoke <token>`                               |
| HTTP API | `POST /v1/sys/revoke` with JSON payload `{ "token": ... }` |

```bash theme={null}
