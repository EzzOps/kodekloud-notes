# Demo Promote a Secondary Cluster

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Build-Fault-Tolerant-Vault-Environments/Demo-Promote-a-Secondary-Cluster/page

Learn to safely demote a primary cluster and promote a DR secondary cluster in HashiCorp Vault with minimal downtime and data integrity.

In this guide, you’ll learn how to safely **demote** the existing primary cluster in a Vault Disaster Recovery (DR) replication setup and then **promote** the DR secondary cluster to become the new primary. This procedure ensures minimal downtime and maintains data integrity across clusters.

> **lightbulb** * Vault version **1.9+** installed on both clusters
  * Network connectivity between primary and secondary
  * Root or privileged token access on both clusters
  * `jq` installed for JSON formatting

## Quick Reference

| Step | Action                                   | Command                                            |
| ---- | ---------------------------------------- | -------------------------------------------------- |
| 1    | Verify DR replication status on primary  | `vault read sys/replication/dr/status`             |
| 2    | Demote primary to secondary              | `vault write -f sys/replication/dr/primary/demote` |
| 3    | Generate DR operation token on secondary | `vault operator generate-root -dr-token`           |
| 4    | Promote secondary to primary             | `vault write sys/replication/dr/secondary/promote` |
| 5    | Verify the new primary status and peers  | `vault operator raft list-peers`                   |

***

## 1. Verify Current DR Replication Status

On your **primary** cluster, confirm that the DR replication relationship is healthy:

```bash theme={null}
vault read -format=json sys/replication/dr/status | jq
```

Sample output:

```json theme={null}
{
  "mode": "primary",
  "state": "running",
  "known_secondaries": ["secondary-dallas"],
  "secondaries": [
    {
      "node_id": "secondary-dallas",
      "connection_status": "connected",
      "api_address": "http://10.1.101.108:8200",
      "cluster_address": "https://10.1.101.108:8201",
      "last_heartbeat": "2022-05-24T20:13:45Z"
    }
  ]
}
```

If the `connection_status` is not `connected`, troubleshoot network connectivity and TLS settings before proceeding.

***

## 2. Demote the Current Primary Cluster

Demoting the primary ensures there is no conflict when promoting the secondary.

```bash theme={null}
