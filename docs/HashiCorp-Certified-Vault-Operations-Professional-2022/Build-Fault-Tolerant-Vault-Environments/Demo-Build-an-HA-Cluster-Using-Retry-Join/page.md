# Demo Build an HA Cluster Using Retry Join

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Build-Fault-Tolerant-Vault-Environments/Demo-Build-an-HA-Cluster-Using-Retry-Join/page

This guide explains how to deploy a three-node Vault High Availability cluster on EC2 using the retry_join configuration for automatic node discovery.

In this guide, you’ll learn how to deploy a three-node Vault High Availability (HA) cluster on EC2. By configuring the `retry_join` stanza in each Vault server’s configuration file, nodes will automatically discover and join the Raft-based cluster—eliminating any manual join steps after initialization.

## Prerequisites

* Three EC2 instances named **vault-1**, **vault-2**, **vault-3**, each running Vault 1.10.3+ent
* Raft storage backend
* AWS KMS auto-unseal configured
* Vault binary installed and a systemd unit in place

| Instance | Private IP   |
| -------- | ------------ |
| vault-1  | 10.1.101.199 |
| vault-2  | 10.1.101.108 |
| vault-3  | 10.1.101.25  |

<Callout icon="lightbulb">
  Ensure all nodes can communicate over ports **8200** (API) and **8201** (Raft). Configure your security groups accordingly.
</Callout>

***

## 1. Verify a Clean State

On any node (for example, **vault-3**), stop Vault and clear existing data. Then confirm that Vault is uninitialized:

```bash theme={null}
sudo systemctl stop vault
sudo rm -rf /opt/vault/*

vault status
