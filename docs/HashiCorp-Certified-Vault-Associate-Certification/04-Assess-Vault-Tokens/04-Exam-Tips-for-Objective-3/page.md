# Exam Tips for Objective 3

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Exam-Tips-for-Objective-3/page

Exam tips for understanding Vaults token system, including types, differences, commands, and best practices for effective preparation.

Before you dive into exam questions, ensure you have a solid grasp of Vault’s token system. In this lesson, we’ll cover:

* An overview of all token types
* Key differences between Service and Batch tokens
* How to use the `vault token` command
* Root Token best practices

## Token Types Overview

![The image provides exam tips about different types of tokens, including Service, Batch, Root, Periodic, Orphan, and CIDR-Bound Tokens, and emphasizes understanding their unique characteristics and use cases.](https://kodekloud.com/kk-media/image/upload/v1752877985/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Exam-Tips-for-Objective-3/exam-tips-token-types-characteristics.jpg)

| Token Type | TTL Renewal       | Revocation | Storage Behavior                     |
| ---------- | ----------------- | ---------- | ------------------------------------ |
| Service    | Configurable ✓    | ✓          | Persisted in Vault’s storage backend |
| Batch      | ✗                 | ✗          | Encrypted blob, not persisted        |
| Root       | — (never expires) | ✓          | Persisted                            |
| Periodic   | ✓                 | ✓          | Persisted                            |
| Orphan     | ✓                 | ✓          | Persisted (no parent)                |
| CIDR-Bound | ✓                 | ✓          | Persisted (IP-restricted)            |

Key actions you should be able to perform:

* **List** all token types
* **Describe** TTL, renewal, revocation, and storage details for each
* **Match** real-world use cases to the appropriate token

## Service vs. Batch Tokens

![The image provides exam tips related to service and batch tokens, emphasizing the differences, storage practices, and the use of the "vault token" command. It features a stylized character in the bottom right corner.](https://kodekloud.com/kk-media/image/upload/v1752877986/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Exam-Tips-for-Objective-3/exam-tips-service-batch-tokens.jpg)

| Feature                | Service Tokens                 | Batch Tokens                        |
| ---------------------- | ------------------------------ | ----------------------------------- |
| Renewability           | Fully renewable                | Not renewable                       |
| Revocability           | Fully revocable                | Not revocable                       |
| Storage Backend Impact | Persisted to backend           | No backend storage                  |
| Use Case               | Long-lived clients, automation | One-time operations, scale concerns |

> **lightbulb** Use batch tokens when you need to minimize storage-backend impact.

### Practice with `vault token`

Launch a local Dev Server and run:

```bash theme={null}
