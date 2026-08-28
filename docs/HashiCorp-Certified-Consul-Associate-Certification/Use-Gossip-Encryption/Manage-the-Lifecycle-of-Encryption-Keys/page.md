# Manage the Lifecycle of Encryption Keys

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Use-Gossip-Encryption/Manage-the-Lifecycle-of-Encryption-Keys/page

This article demonstrates managing encryption keys using Consuls keyring for listing, distributing, activating, and retiring keys while ensuring compliance and minimizing risk.

In this lesson we’ll demonstrate how to use Consul’s gossip encryption keyring to list, distribute, activate, and retire encryption keys—enabling you to enforce regular rotations (e.g., every six months or annually) without downtime. Many security policies mandate periodic key rotations to maintain compliance and minimize risk. Consul’s built-in `consul keyring` and `consul keygen` commands provide a straightforward day-two workflow for these tasks.

<Frame>
  ![The image provides instructions on managing encryption keys using "consul keyring" and "consul keygen," highlighting key management tasks and recommendations.](https://kodekloud.com/kk-media/image/upload/v1752877966/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Manage-the-Lifecycle-of-Encryption-Keys/consul-keyring-keygen-management-instructions.jpg)
</Frame>

## Why Rotate Gossip Encryption Keys?

* Ensures forward secrecy and mitigates the impact of key compromise
* Aligns with security best practices and compliance requirements (e.g., PCI-DSS, HIPAA)
* Operates transparently, maintaining cluster availability during rotation

<Callout icon="lightbulb">
  Consul’s gossip encryption uses a 32-byte Base64 key. You can generate this key with any tool, but `consul keygen` guarantees compatibility.
</Callout>

## 1. Generate a New Key

Leverage the built-in key generator to produce a 32-byte Base64 string:

```bash theme={null}
consul keygen
```

Example output:

```bash theme={null}
VCjCNv+521LNTBcQcdu8rl9pjTHEuw+dhzf2bvici3w=
```

## 2. Consul Keyring Commands

Use `consul keyring` to manage keys across your Consul agents. The four primary subcommands are:

| Command                        | Description                                      |
| ------------------------------ | ------------------------------------------------ |
| `consul keyring list`          | List all installed gossip encryption keys        |
| `consul keyring install <key>` | Distribute a new key to every Consul agent       |
| `consul keyring use <key>`     | Set a specific key as the primary encryption key |
| `consul keyring remove <key>`  | Retire a no-longer-used key from the cluster     |

<Callout icon="triangle-alert">
  Avoid running with multiple active keys longer than necessary. Each Consul agent will attempt decryption with every key on inbound messages, increasing CPU overhead.
</Callout>

## 3. Example Rotation Workflow

Follow these steps to rotate keys seamlessly:

```bash theme={null}
