# Demo Managing the Lifecycle of Encryption Keys

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Use-Gossip-Encryption/Demo-Managing-the-Lifecycle-of-Encryption-Keys/page

This tutorial covers the process of rotating gossip encryption keys in a Consul cluster to enhance security.

Rotating gossip encryption keys in your Consul cluster helps maintain strong security posture. In this tutorial, we’ll walk through:

1. Reviewing the current configuration
2. Generating a new encryption key
3. Distributing the key across the cluster
4. Promoting the new key to primary
5. Removing the old key

## 1. Review Current Configuration

Inspect your existing gossip encryption key in `consul.d/config.hcl`:

```hcl theme={null}
{
  "log_level": "INFO",
  "node_name": "consul-node-b",
  "server": true,
  "ui": true,
  "leave_on_terminate": true,
  "data_dir": "/etc/consul.d/data",
  "datacenter": "us-east-1",
  "client_addr": "0.0.0.0",
  "bind_addr": "10.0.101.248",
  "advertise_addr": "10.0.101.248",
  "retry_join": ["10.0.101.110"],
  "bootstrap_expect": 2,
  "enable_syslog": true,
  "encrypt": "62qD/DH15Ax0lMRUpMKvttP53p4FAvu+FgARDU4MzA=",
  "encrypt_verify_incoming": true,
  "encrypt_verify_outgoing": true,
  "connect": {
    "enabled": true
  },
  "acl": {
    "enabled": true,
    "default_policy": "allow",
    "down_policy": "extend-cache"
  },
  "performance": {}
}
```

<Callout icon="lightbulb">
  Before you begin, back up your Consul configuration and data directory. This ensures you can recover quickly if something goes wrong.
</Callout>

## 2. Generate a New Gossip Encryption Key

Run the following command on any Consul server or client to create a fresh base64-encoded key:

```bash theme={null}
consul keygen
