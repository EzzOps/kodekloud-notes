# Example output:
wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4=
```

## 3. Distribute the New Key Across the Cluster

Install the newly generated key into the cluster keyring:

```bash theme={null}
consul keyring -install wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4=
```

You should see:

```text theme={null}
Installing new key "wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4="
```

### 3.1. Verify Key Distribution

On another node, list installed keys:

```bash theme={null}
consul keyring -list
```

Expected output:

```text theme={null}
==> Gathering installed encryption keys...
us-east-1 (LAN):
  62qD/DH15Ax0lMRUpMKvttP53p4FAvu+FgARDU4MzA=  [2/2]
  wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4=  [2/2]
```

## 4. Promote the New Key to Primary

Switch the cluster’s primary gossip encryption key:

```bash theme={null}
consul keyring -use wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4=
```

You’ll see:

```text theme={null}
Changing primary gossip encryption key to "wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4="
```

Confirm the change:

```bash theme={null}
consul keyring -list
```

Should display the new key first under both WAN and LAN segments.

## 5. Remove the Old Encryption Key

Once every node is using the new key, remove the old one:

```bash theme={null}
consul keyring -remove 62qD/DH15Ax0lMRUpMKvttP53p4FAvu+FgARDU4MzA=
```

Output:

```text theme={null}
Removing encryption key "62qD/DH15Ax0lMRUpMKvttP53p4FAvu+FgARDU4MzA="
```

Verify only the new key remains:

```bash theme={null}
consul keyring -list
```

```text theme={null}
==> Gathering installed encryption keys...
WAN:
  wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4=  [2/2]
us-east-1 (LAN):
  wlVkhlSnyl7SEy63/XsXMJ/48gIQSghShhUqn/05C4=  [2/2]
```

<Callout icon="triangle-alert">
  Do **not** remove the old key until all nodes report the new key as primary. Premature removal can lead to cluster partitions and service disruptions.
</Callout>

## Command Reference

| Command                         | Description                                     |
| ------------------------------- | ----------------------------------------------- |
| `consul keygen`                 | Generates a new base64-encoded key              |
| `consul keyring -install <key>` | Installs a key into the cluster keyring         |
| `consul keyring -list`          | Lists installed keys and their usage counts     |
| `consul keyring -use <key>`     | Promotes a key to be the primary encryption key |
| `consul keyring -remove <key>`  | Deletes an old key from the keyring             |

## Links and References

* [Consul Encryption Keys Documentation](https://www.consul.io/docs/enterprise/encryption)
* [HashiCorp Consul Official Site](https://www.consul.io/)
* [HashiCorp Tutorials](https://learn.hashicorp.com/consul)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/d256f82f-c1cb-4bad-80c0-790ffa3cb05d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/e1e232fc-c8a0-43fc-a8a6-42107bbb69b0" />
</CardGroup>


# Intro to Gossip Encryption

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Use-Gossip-Encryption/Intro-to-Gossip-Encryption/page

This article explores securing Consuls gossip protocol with symmetric encryption, including key generation, configuration, and rotation for a secure cluster.

In this lesson, we’ll explore how Consul secures its Serf-based gossip protocol with symmetric encryption. You’ll learn how to generate, configure, and rotate gossip keys to maintain a highly secure Consul cluster across LANs and federated data centers.

<Frame>
  ![The image outlines a security model review with five components: Gossip Protocol Encryption, Built-In ACL System, Consul Agent Communication, mTLS for Authenticity and Encryption, and Certificate Authority. It features a colorful, numbered list with icons representing each component.](https://kodekloud.com/kk-media/image/upload/v1752877965/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Intro-to-Gossip-Encryption/security-model-review-components-list.jpg)
</Frame>

Consul’s security model consists of five key layers:

1. **Gossip Protocol Encryption**
2. **Built-In ACL System**
3. **Consul Agent Communication** (RPC and HTTP API secured with TLS)
4. **mTLS for Service Mesh** (ensures authenticity and encryption)
5. **Certificate Authority** (built-in or external, e.g., [Vault](https://www.vaultproject.io/))

***

## Gossip Protocol Encryption

Consul uses a single 32-byte symmetric key to encrypt all gossip messages exchanged between agents (servers and clients). Every agent’s configuration must include this key in Base64 form so it can join the gossip pool and communicate securely.

### Key Properties

* **Length**: 32 bytes
* **Encoding**: Base64
* **Purpose**: Encrypts and decrypts all Serf gossip traffic

<Callout icon="lightbulb">
  When federating multiple datacenters (WAN gossip), use the same encryption key in each datacenter. This ensures messages can be decrypted and forwarded properly across the WAN pool.
</Callout>

### Generating a Gossip Encryption Key

Consul provides a simple key generator—no agent required. Run:

```bash theme={null}
consul keygen
```

Example output:

```bash theme={null}
hDqYxqqepKyRADn4Zn+u+D9vLge8Wm+LpFAPLGhtco=
```

Then add the Base64 string to every agent’s configuration file:

```json theme={null}
{
  "encrypt": "hDqYxqqepKyRADn4Zn+u+D9vLge8Wm+LpFAPLGhtco="
}
```

<Callout icon="lightbulb">
  Treat your gossip key like a password. Store it in a secure vault or environment variable—never commit it to version control.
</Callout>

### Day-Two Operations: Key Rotation

Regularly rotating your gossip key helps maintain cluster security. Consul’s `keyring` subcommands let you add, promote, and retire keys without downtime:

| Command                           | Description                                  |
| --------------------------------- | -------------------------------------------- |
| `consul keyring list`             | List all known gossip encryption keys        |
| `consul keyring add`              | Generate and add a new key to the ring       |
| `consul keyring promote <key-id>` | Promote a specific key to be the primary one |
| `consul keyring remove <key-id>`  | Remove an old or compromised key             |

<Callout icon="triangle-alert">
  Ensure all agents have pulled the new key before removing the old one. Nodes missing the primary key will be unable to decrypt gossip traffic and may leave the cluster.
</Callout>

***

## References

* [Consul Security Documentation](https://www.consul.io/docs/security)
* [Vault PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki)
* [Serf: A Service for Cluster Membership and Failure Detection](https://www.serf.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/6243f581-af52-4a39-ab1e-ab15d5eeea9b" />
</CardGroup>
