# Assess Vault Tokens Section Overview

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Assess-Vault-Tokens-Section-Overview/page

This article explains the token prefix changes in Vault 1.10 while maintaining existing token functionality and policy enforcement.

In this article, we explain the token prefix changes introduced in [Vault 1.10](https://github.com/hashicorp/vault/blob/v1.10.0/CHANGELOG.md) (released March 23, 2022). While the prefix format has been updated, token functionality and policy enforcement remain the same. Note that examples recorded before Vault 1.10 may still show the older single-letter prefixes.

<Frame>
  ![The image describes updates to tokens in Vault 1.10, highlighting major changes such as a new prefix for service tokens and an increase in token length.](https://kodekloud.com/kk-media/image/upload/v1752877972/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Assess-Vault-Tokens-Section-Overview/vault-1-10-token-updates-changes.jpg)
</Frame>

<Callout icon="lightbulb">
  Existing tokens created before the upgrade keep their original prefixes (`S.`, `B.`, `R.`). Only tokens generated **after** upgrading to Vault 1.10 receive the new three-letter prefixes.
</Callout>

## Token Prefix Changes in Vault 1.10

Vault 1.10 replaces the previous one-letter prefixes with more descriptive three-letter identifiers. The new mapping is:

| Token Type     | Old Prefix | New Prefix | Minimum Length |
| -------------- | ---------- | ---------- | -------------- |
| Service Token  | `S.`       | `hvs.`     | 95 bytes       |
| Batch Token    | `B.`       | `hvb.`     | unchanged      |
| Recovery Token | `R.`       | `hvr.`     | unchanged      |

### Service Tokens

Service tokens are the most common token type. In Vault 1.10, they now start with `hvs.` followed by at least 95 random bytes:

```text theme={null}
hvs.QRx4pz2RIka7RhhrjiVRBNjq...   # ≥95 bytes after “hvs.”
```

* `hvs.` indicates a **HashiCorp Vault Service** token.
* The random string that follows provides the required entropy.

<Callout icon="triangle-alert">
  Service tokens with insufficient length will be rejected. Always verify token length when automating creation.
</Callout>

### Batch and Recovery Tokens

<Frame>
  ![The image shows updates to token prefixes in Vault 1.10, with batch tokens now using the prefix "hvb.xxxxx" and recovery tokens using "hvr.xxxxx".](https://kodekloud.com/kk-media/image/upload/v1752877973/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Assess-Vault-Tokens-Section-Overview/vault-1-10-token-prefixes-update.jpg)
</Frame>

Batch and recovery tokens have also switched to three-letter prefixes:

```text theme={null}
hvb.AAAAQLQLP      # Batch token (was B.<string>)
hvr.ZZZZRTYUI      # Recovery token (was R.<string>)
```

* `hvb.` marks a **Batch** token used for one-time API operations.
* `hvr.` marks a **Recovery** token used for root recovery workflows.

## Summary

When working with Vault 1.10 or later, newly generated tokens will use:

* `hvs.` → Service token
* `hvb.` → Batch token
* `hvr.` → Recovery token

All token operations—`vault token create`, `vault token revoke`, or policy checks—remain unchanged under the new prefix scheme.

## Links and References

* [Vault 1.10 Changelog](https://github.com/hashicorp/vault/blob/v1.10.0/CHANGELOG.md)
* [Vault Token Authentication](https://www.vaultproject.io/docs/concepts/token)
* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/76dd19b1-ee88-4935-8b32-0b10052dfa45" />
</CardGroup>
