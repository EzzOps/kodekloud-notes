# Avoid direct exec into Vault pods:
# Use remote Vault CLI instead:
vault status
```

### 1.3 Limit Services on Vault Nodes

Run only Vault (plus telemetry or log agents such as Splunk, Sumo Logic, or Datadog). Fewer services mean fewer firewall rules and less risk of binary tampering or memory exposure.

### 1.4 Permit Only Required Firewall Ports

Restrict ingress to only Vault’s and Consul’s necessary ports. By default:

| Service               | Port | Protocol | Purpose              |
| --------------------- | ---- | -------- | -------------------- |
| Vault API             | 8200 | TCP      | Client communication |
| Vault cluster (Raft)  | 8201 | TCP      | Node replication     |
| Consul HTTP (if used) | 8500 | TCP      | Consul UI/API        |
| Consul RPC            | 8300 | TCP      | Raft & internal RPC  |
| Consul Serf           | 8301 | TCP/UDP  | Gossip               |

![The image is a slide discussing firewall port requirements for Vault and Consul, emphasizing the use of dedicated ports to reduce attack surfaces, with specific default ports listed for each.](https://kodekloud.com/kk-media/image/upload/v1752878519/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/firewall-port-requirements-vault-consul.jpg)

### 1.5 Allow Outbound Connections to Backends

Vault requires outbound connectivity to its secret backends (e.g., cloud APIs, databases, LDAP, object storage).

| Backend            | Ports    | Protocol |
| ------------------ | -------- | -------- |
| Cloud Platform API | 443      | TCP      |
| MySQL              | 3306     | TCP      |
| LDAP               | 389, 636 | TCP      |
| S3 / Azure Blob    | 443      | TCP      |

![The image is a diagram showing a Vault Cluster with connections to various services like Cloud Platform API, Database Servers, Active Directory, and Cloud-Based File Storage, each using specific TCP ports. It also includes a certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878520/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/vault-cluster-diagram-services-connections.jpg)

### 1.6 Simplify with Integrated Storage

Using Vault’s Raft-based Integrated Storage reduces the number of open ports—only 8200 (client) and 8201 (Raft). No Consul ports are needed.

![The image is a network diagram illustrating the required ports on a firewall for a Consul and Vault cluster setup, showing connections between Vault nodes and Consul nodes.](https://kodekloud.com/kk-media/image/upload/v1752878521/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/consul-vault-cluster-firewall-ports-diagram.jpg)

Or view the Raft replication topology:

![The image is a diagram illustrating a network setup for a Vault system with nodes A, B, and C, showing data replication and required ports on a firewall. It includes a Vault client connecting to Node B and indicates roles like Raft Leader and Follower.](https://kodekloud.com/kk-media/image/upload/v1752878522/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/vault-network-setup-diagram-nodes.jpg)

### 1.7 Immutable Upgrades

Adopt immutable infrastructure: destroy unhealthy nodes and spin up new ones via automation. Leverage Consul Autopilot or Raft Autopilot to maintain quorum. Always add and replicate to new nodes before decommissioning old ones to avoid data loss.

![The image is a slide discussing immutable upgrades, highlighting the benefits of known states, ease of node replacement, and the use of AutoPilot with Consul and Raft. It also emphasizes the importance of ensuring replication when using Raft.](https://kodekloud.com/kk-media/image/upload/v1752878524/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/immutable-upgrades-autopilot-consul-raft.jpg)

***

## 2. Operating System Recommendations

### 2.1 Run Vault as a Non-Root User

Create a dedicated `vault` user and restrict directory ownership:

```bash theme={null}
useradd --system --home /opt/vault vault
chown -R vault:vault /opt/vault/data
```

### 2.2 Secure Critical Directories and Files

Audit and enforce strict permissions on binaries, configs (`/etc/vault.d`), plugins, service definitions, logs, and snapshots:

```bash theme={null}
chmod -R 740 /etc/vault.d
```

### 2.3 Protect the Storage Backend

When using Consul storage, enable ACLs, enforce TLS, limit node access, and verify hostnames in `consul.hcl`.

![The image is a slide about protecting the storage backend in Vault, emphasizing the importance of using a storage backend and providing tips for using Consul as a storage backend. It includes a certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878525/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/vault-storage-backend-consul-tips-slide.jpg)

### 2.4 Disable Shell History

Prevent sensitive data from ending up in shell history:

```bash theme={null}
echo 'set +o history' >> /etc/profile
```

![The image is a slide about turning off core dumps, highlighting that they could reveal encryption keys and should be disabled in production environments, though not required for an exam.](https://kodekloud.com/kk-media/image/upload/v1752878526/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/turning-off-core-dumps-encryption-keys.jpg)

### 2.5 Configure SELinux or AppArmor

Enable SELinux/AppArmor to align with CIS/DISA benchmarks and enhance OS-level protection.

![The image is a slide about configuring SELinux/AppArmor, emphasizing not disabling them for easier management, providing additional OS protection, and adhering to CIS or DISA standards. It also references a blog about hardening HashiCorp Vault with SELinux.](https://kodekloud.com/kk-media/image/upload/v1752878527/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/selinux-apparmor-configuration-slide.jpg)

### 2.6 Turn Off Core Dumps

Disabling core dumps prevents leakage of memory contents and encryption keys in the event of a crash.

### 2.7 Protect and Audit the Vault Service File

Monitor the systemd or service definition file for unauthorized changes, which could indicate binary tampering.

### 2.8 Frequent OS Patching

Regularly update Vault hosts. With immutable architectures, rebuild nodes using tools like [Packer](https://www.packer.io), Satellite, or Spacewalk.

![The image is a slide about frequently patching the operating system, suggesting options like Satellite and SpaceWalk, and using Packer for immutable architecture. It includes a Vault certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878528/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/frequent-os-patching-satellite-packer.jpg)

### 2.9 Disable Swap

Prevent sensitive data from being written to disk by disabling swap or using `mlock` on Linux.

![The image is a slide about disabling swap to protect sensitive data stored in-memory by Vault, suggesting that data should not be written to disk and mentioning the use of mlock to prevent memory swap.](https://kodekloud.com/kk-media/image/upload/v1752878529/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/disable-swap-protect-sensitive-data.jpg)

***

## 3. Vault-Specific Recommendations

### 3.1 Enforce TLS Everywhere

Configure trusted TLS certificates in `vault.hcl` (except for local development).

![The image provides guidelines for securing a Vault with TLS, emphasizing the importance of TLS for communication and configuration settings. It includes a certification badge in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752878530/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/vault-tls-security-guidelines-badge.jpg)

### 3.2 Secure Consul Backend

For Consul storage, enforce TLS, trusted certs, ACLs, and gossip encryption (generate with `consul keygen`).

![The image provides guidelines for securing Consul, emphasizing the use of TLS, trusted certificates, ACLs, and gossip encryption. It also features a Vault certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878531/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/consul-security-guidelines-tls-acls.jpg)

### 3.3 Enable Auditing

Activate one or more audit devices, send logs to a centralized server, archive them, and configure alerts for critical events.

![The image is a slide about enabling auditing, listing steps such as using multiple audit devices, sending data to a server, archiving logs, and creating alerts. It also features a certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878532/notes-assetshttps://kodekloud.com/kk-media/image/upload/v1752878532/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/enabling-auditing-steps-certification-badge.jpg)

### 3.4 Avoid Clear-Text Credentials

Never embed access keys or HSM credentials in `vault.hcl`. Use environment variables or cloud IAM roles/MSIs instead.

```hcl theme={null}
# ❌ Do not store clear-text AWS credentials
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "1234abcd-..."
  access_key = "AKIAIOSFODNNEXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRficEXAMPLEKEY"
}
```

> **triangle-alert** Avoid clear-text secrets in configuration files. Leverage IAM roles or environment variables for dynamic credentials.

![The image is a slide about enabling auditing, listing steps such as using multiple audit devices, sending data to a server, archiving logs, and creating alerts. It also features a certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878532/notes-assetshttps://kodekloud.com/kk-media/image/upload/v1752878532/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/enabling-auditing-steps-certification-badge.jpg)

### 3.5 Upgrade Vault Frequently

Track new releases at [releases.hashicorp.com/vault](https://releases.hashicorp.com/vault). Regular updates deliver security fixes and new cipher suites.

![The image is a slide about upgrading Vault frequently, highlighting benefits like security fixes, new cipher suites, and new functionality. It includes a screenshot of a webpage listing Vault versions and a certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878534/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/vault-upgrading-benefits-screenshot-badge.jpg)

### 3.6 Discontinue Root Tokens

Root tokens bypass ACLs and never expire. Revoke the root token after setup:

```bash theme={null}
vault token revoke <root-token>
```

Generate a new one later via unseal/recovery keys if necessary.

### 3.7 Verify Binary Integrity

Download Vault binaries from HashiCorp and validate checksums before use.

> **lightbulb** Always verify the SHA256 checksum against the value provided on the official HashiCorp site to prevent tampering.

![The image is a slide about verifying the integrity of the Vault binary, advising to get binaries directly from HashiCorp, use the HashiCorp checksum for validation, and warning that modified binaries could leak data. It includes a certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878535/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/vault-binary-integrity-verification-slide.jpg)

### 3.8 Disable Unused UI

If you don’t need the Vault web UI, disable it in `vault.hcl`:

```hcl theme={null}
ui = false
```

### 3.9 Encrypt Gossip Protocol

Consul gossip traffic isn’t protected by TLS—use a 32-byte key generated with `consul keygen` and rotate with `consul keyring`.

```hcl theme={null}
encrypt = "generated-32-byte-key"
```

![The image is a slide about encrypting the Gossip Protocol in Consul, highlighting that TLS secures interfaces but not gossip traffic, and suggesting the use of a 32-byte key generated with consul keygen.](https://kodekloud.com/kk-media/image/upload/v1752878536/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/encrypting-gossip-protocol-consul-tls.jpg)

### 3.10 Secure Unseal/Recovery Keys

During initialization, use PGP keys (e.g., via [Keybase](https://keybase.io)) so each operator receives an encrypted unseal key. Store keys offline and distribute among team members—losing them results in irreversible data loss.

![The image provides guidelines for securing unseal/recovery keys, including using PGP keys, distributing them among team members, and not storing them in the Vault. It features a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878538/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/securing-unseal-recovery-keys-guidelines.jpg)

### 3.11 Minimize Token and Lease TTLs

Define the smallest TTLs needed and set maximum TTLs to prevent runaway renewals. This also reduces load on the storage backend via garbage collection.

![The image is a slide discussing minimizing TTLs (Time To Live) for leases and tokens, suggesting using the smallest possible TTL, defining max TTLs, and noting that minimizing TTL reduces the burden on the storage backend. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878539/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/minimizing-ttls-leases-tokens-slide.jpg)

### 3.12 Follow the Principle of Least Privilege

Grant tokens only the permissions required. Separate policies for applications and users, limit wildcards (`*`, `+`), and consider templated policies for consistency.

![The image provides guidelines on following the Principle of Least Privilege, including giving tokens limited access, separating policies, limiting certain symbols in policies, and using templated policies. It features a small illustration of a person and a certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878540/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/least-privilege-guidelines-illustration.jpg)

### 3.13 Perform Regular Backups

Automate and schedule snapshots, then test restores:

```bash theme={null}
# Open Source Raft snapshot
vault operator raft snapshot save daily.snap

# Enterprise auto-snapshot
vault write sys/storage/raft/snapshot-auto/config/daily
```

### 3.14 Integrate with Identity Providers

Leverage your existing IdP (AD, Okta, etc.) to manage user authentication. When a user is disabled upstream, Vault access is revoked automatically.

![The image is a slide discussing the integration with existing identity providers, highlighting benefits such as immediate access revocation and reduced administrative burden. It includes a Vault certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878541/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Security-Hardening/identity-provider-integration-benefits-slide.jpg)

***

## 4. Monitoring and Alerting

Centralize your Vault audit logs in a SIEM or log collector (Splunk, Sumo Logic, Datadog) and set up alerts for critical events:

* Root token usage or creation
* Policy modifications
* Auth method creations
* Transit configuration changes or key deletions
* Audit log failures

<Frame>
  <img alt="The image lists various aspects of Vault Security Monitoring, such as root token usage, policy modifications, and audit log failures, with a note about using an audit log and log collection tool." />
</Frame>

***

## References

* [Vault Security Best Practices](https://www.vaultproject.io/docs/security)
* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
* [Kubernetes Security](https://kubernetes.io/docs/concepts/security/overview/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/1435ac1b-fcd3-4bfb-b3e1-ee5274ddd6af)


# Vault Tokens Auth Method

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Vault-Tokens-Auth-Method/page

Vaults token authentication is essential for accessing Vault, requiring valid tokens for most operations and supporting various token types for different use cases.

Vault’s token authentication is the default and core method for accessing Vault. Almost every Vault operation (aside from health checks and auth endpoints) requires a valid token. Since all auth methods eventually issue tokens, mastering tokens is essential for secure and efficient Vault usage.

> **lightbulb** Tokens are written to Vault’s storage backend and cannot be disabled. Each token carries one or more policies, determining its permissions. By default, every token inherits the `default` policy.

## Token Types Comparison

Vault supports multiple token types. Below is a comparison of the two primary types:

| Token Type    | Prefix | Persistence    | Renewable | Typical Use Case                             |
| ------------- | ------ | -------------- | --------- | -------------------------------------------- |
| Service Token | hvs    | Stored on disk | Yes       | Long-lived sessions, child token creation    |
| Batch Token   | hvb    | Ephemeral      | No        | High-volume operations, DR replication sales |

![The image is a slide titled "Introduction to Tokens," explaining the differences between service tokens and batch tokens in Vault, highlighting their features and use cases.](https://kodekloud.com/kk-media/image/upload/v1752878542/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Tokens-Auth-Method/introduction-to-tokens-vault-differences.jpg)

For more details, see the [Vault Token Auth Method](https://www.vaultproject.io/docs/auth/token) documentation.

***

## Creating Tokens

Vault lets you tailor tokens for different scenarios: periodic, use-limited, or orphan. Below are examples for each.

### Periodic Tokens

Periodic tokens have no maximum TTL and can be renewed indefinitely at a fixed interval.

```bash theme={null}
vault token create \
  -policy="hcvop" \
  -period="24h"
```

Example output:

```text theme={null}
Key                Value
---                -----
token              hvs.CAESINq3yTGLYZofP7iZBStz3zAktvOHfWBigN
token_accessor     fy9Jjse9SRTLIYLufysE6qP0
token_duration     24h
token_renewable    true
token_policies     ["default" "hcvop"]
policies           ["default" "hcvop"]
```

> **lightbulb** Ideal for long-running applications that can renew instead of rotating tokens frequently.

### Use-Limited Tokens

Use-limited tokens expire after a specified number of uses or when the TTL is reached.

```bash theme={null}
vault token create \
  -policy="hcvop" \
  -use-limit=2
```

### Orphan Tokens

Orphan tokens have no parent relationship. They remain valid even if the creator token is revoked.

```bash theme={null}
vault token create \
  -policy="hcvop" \
  -orphan
```

***

## Configuring Auth Methods for Token Types

You can configure other auth backends (e.g., AppRole) to issue specific token types:

```bash theme={null}
