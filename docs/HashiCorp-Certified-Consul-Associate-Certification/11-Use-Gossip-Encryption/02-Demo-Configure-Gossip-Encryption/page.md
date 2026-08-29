# Demo Configure Gossip Encryption

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Use-Gossip-Encryption/Demo-Configure-Gossip-Encryption/page

This guide explains how to secure gossip traffic in a HashiCorp Consul cluster by enabling gossip encryption and message verification.

In this guide, you'll secure all gossip traffic within an existing HashiCorp Consul cluster by enabling gossip encryption and message verification. By default, gossip communications are unencrypted. We’ll update each server’s agent configuration to use a shared encryption key and enable both incoming and outgoing verification.

***

## Table of Contents

1. [Check Current Configuration](#1-check-current-configuration)
2. [Enable Gossip Encryption](#2-enable-gossip-encryption)
3. [Validate Encryption](#3-validate-encryption)
4. [Links and References](#links-and-references)

***

## 1. Check Current Configuration

First, verify that your cluster is using a shared encryption key but has message verification disabled.

| Consul Node | Configuration Path         | Action                             |
| ----------- | -------------------------- | ---------------------------------- |
| Node A      | `/etc/consul.d/config.hcl` | Open and inspect existing settings |
| Node B      | `/etc/consul.d/config.hcl` | Verify identical `encrypt` value   |

### On Consul Node A

```bash theme={null}
sudo vi /etc/consul.d/config.hcl
```

You should see an HCL block similar to:

```hcl theme={null}
{
  "log_level": "INFO",
  "node_name": "consul-node-a",
  "server": true,
  "ui": true,
  "leave_on_terminate": true,
  "data_dir": "/etc/consul.d/data/",
  "datacenter": "us-east-1",
  "client_addr": "0.0.0.0",
  "bind_addr": "10.0.101.110",
  "advertise_addr": "10.0.101.110",
  "retry_join": ["10.0.101.248"],
  "bootstrap_expect": 2,
  "enable_syslog": true,
  "encrypt": "[SECRET_REDACTED]=",
  "encrypt_verify_incoming": false,
  "encrypt_verify_outgoing": false,
  "connect": { "enabled": true },
  "acl": {
    "enabled": true,
    "default_policy": "allow",
    "down_policy": "extend-cache"
  },
  "performance": { "raft_multiplier": 1 }
}
```

<Callout icon="lightbulb">
  To generate or rotate a gossip encryption key, run:

  ```bash theme={null}
  consul keygen
  ```

  Ensure the same key appears in every server’s `encrypt` field.
</Callout>

### On Consul Node B

```bash theme={null}
sudo vi /etc/consul.d/config.hcl
```

Confirm the `encrypt` value matches Node A and that both verification flags are set to `false`.

```hcl theme={null}
{
  "node_name": "consul-node-b",
  // ...
  "encrypt": "[SECRET_REDACTED]=",
  "encrypt_verify_incoming": false,
  "encrypt_verify_outgoing": false,
  // ...
}
```

### Restart Agents to View Current State

```bash theme={null}
sudo systemctl restart consul
journalctl -u consul --no-pager | grep "Encrypt:"
```

Expected log output:

```text theme={null}
Encrypt: Gossip: true, TLS-Incoming: false, TLS-Outgoing: false
```

***

## 2. Enable Gossip Encryption

Follow two steps to fully secure gossip traffic:

| Step | Flag to Enable                   |
| ---- | -------------------------------- |
| 1    | `encrypt_verify_outgoing = true` |
| 2    | `encrypt_verify_incoming = true` |

### Step 1: Enable Outgoing Verification

Edit each node’s `config.hcl`:

```hcl theme={null}
{
  // ... existing settings ...
  "encrypt_verify_incoming": false,
  "encrypt_verify_outgoing": true,
  // ...
}
```

Restart the agent:

```bash theme={null}
sudo systemctl restart consul
```

### Step 2: Enable Incoming Verification

Update both nodes again:

```hcl theme={null}
{
  // ... existing settings ...
  "encrypt_verify_incoming": true,
  "encrypt_verify_outgoing": true,
  // ...
}
```

Restart to apply changes:

```bash theme={null}
sudo systemctl restart consul
```

<Callout icon="triangle-alert">
  Restarting the Consul agent will momentarily interrupt cluster membership. Perform these steps during a maintenance window.
</Callout>

***

## 3. Validate Encryption

After enabling both flags, verify the cluster membership and confirm the encryption status in logs.

### 3.1 Check Cluster Membership

```bash theme={null}
consul members
```

Expected output:

| Node          | Address           | Status | Type   | Protocol | DC        |
| ------------- | ----------------- | ------ | ------ | -------- | --------- |
| consul-node-a | 10.0.101.110:8301 | alive  | server | 2        | us-east-1 |
| consul-node-b | 10.0.101.248:8301 | alive  | server | 2        | us-east-1 |

### 3.2 Confirm Gossip Encryption in Logs

```bash theme={null}
journalctl -u consul --no-pager | grep "Encrypt:"
```

Look for:

```text theme={null}
Encrypt: Gossip: true, TLS-Incoming: false, TLS-Outgoing: false
```

Once verified, all gossip communication is encrypted and integrity-checked. Any new agent joining the cluster must include the same `encrypt` key in its configuration.

***

## Links and References

* [Consul Gossip Encryption](https://www.consul.io/docs/agent/encryption)
* [Consul Key Management](https://www.consul.io/docs/enterprise/key-management)
* [HashiCorp Consul Documentation](https://www.consul.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/77dd90fc-e13b-4f9d-b69d-c64c8d8d3238" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/9a4e194f-ec51-43be-a364-9db2ec36087c/lesson/ba1d7fec-a86a-487f-816c-4b4d5dd398c7" />
</CardGroup>
