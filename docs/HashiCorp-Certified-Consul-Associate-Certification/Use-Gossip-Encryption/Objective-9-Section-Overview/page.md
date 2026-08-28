# 1. List existing keys
consul keyring list
# ==> Gathering installed encryption keys...
# dc1 (LAN):
# 2. Install the newly generated key
consul keyring install [SECRET_REDACTED]=
# 3. Activate the new key
consul keyring use [SECRET_REDACTED]=
# 4. Remove the old key (optional once no longer used)
consul keyring remove [SECRET_REDACTED]=
# ==> Removing gossip encryption key...
```

If you attempt to remove a key that’s still active, Consul will refuse and require you to switch primary keys first.

## 4. Rotation Workflow Cheat Sheet

| Step           | Command                            |
| -------------- | ---------------------------------- |
| Generate key   | `consul keygen`                    |
| Distribute key | `consul keyring install <new_key>` |
| Activate key   | `consul keyring use <new_key>`     |
| Retire key     | `consul keyring remove <old_key>`  |

This process incurs zero downtime for Consul servers and clients. Automate these commands via scripts or integrate into your CI/CD pipeline to enforce more frequent rotations (daily, weekly, or monthly).

***

## Links and References

* [Consul Encryption Overview](https://www.consul.io/docs/security/encryption)
* [Consul Key Management](https://www.consul.io/docs/commands/keyring)
* [HashiCorp Best Practices](https://www.hashicorp.com/resources)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/bb937eb8-5bb0-4a2d-9684-d119ddb68855" />
</CardGroup>


# Objective 9 Section Overview

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Use-Gossip-Encryption/Objective-9-Section-Overview/page

Gossip Encryption secures Consuls internal communications through threat model review, configuration, and key management for ongoing operations.

Gossip Encryption is the final objective in the Consul Certified Associate curriculum. In this section, we’ll dive into how to secure Consul’s internal communications by:

1. Reviewing the Consul Security Threat Model
2. Configuring Gossip Encryption on an existing data center
3. Managing the lifecycle of Gossip Encryption keys for day-two operations

<Frame>
  ![The image outlines objectives for using gossip encryption, including understanding the Consul security model, configuring encryption for a data center, and managing encryption keys. It also indicates a difficulty level of 2 out of 5.](https://kodekloud.com/kk-media/image/upload/v1752877968/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Objective-9-Section-Overview/gossip-encryption-objectives-consul-security.jpg)
</Frame>

<Callout icon="lightbulb">
  If you need a deeper dive into the Consul Security Threat Model, review the [Consul Security Threat Model guide](/docs/security/threat-model) before proceeding.
</Callout>

We’ll begin with a concise recap of the Threat Model, then move on to:

* **Enabling Gossip Encryption** on a running Consul cluster
* **Rotating and retiring** encryption keys over time

Let’s get started!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/c9b7cce3-7268-4bac-b450-7b8b03dc0b7c" />
</CardGroup>
