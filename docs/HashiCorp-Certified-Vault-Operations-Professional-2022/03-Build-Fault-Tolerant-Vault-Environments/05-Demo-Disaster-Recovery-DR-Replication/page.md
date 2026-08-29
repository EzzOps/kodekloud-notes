# Expected output:
# Key              Value
# ---              -----
# Initialized      false
# Sealed           true
# Storage Type     raft
# HA Enabled       true
# Version          1.10.3+ent
# Recovery Seal Type awskms
```

***

## 2. Stop Vault on All Nodes

Before updating configuration, stop Vault on each server:

```bash theme={null}
sudo systemctl stop vault
# Repeat this command on vault-1, vault-2, vault-3
```

***

## 3. Configure retry\_join on vault-3 (10.1.101.25)

Edit `/etc/vault/vault.hcl` on **vault-3** and add both peer addresses under the Raft storage stanza:

```hcl theme={null}
storage "raft" {
  path    = "/opt/vault"
  node_id = "vault-3"

  retry_join {
    leader_api_addr = "http://10.1.101.108:8200"
  }
  retry_join {
    leader_api_addr = "http://10.1.101.199:8200"
  }
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = true
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "arn:aws:kms:us-east-1:003674902126:key/…"
}

api_addr     = "http://10.1.101.25:8200"
cluster_addr = "http://10.1.101.25:8201"
cluster_name = "vault"
ui           = true
log_level    = "INFO"
```

***

## 4. Configure retry\_join on vault-2 (10.1.101.108)

On **vault-2**, update `/etc/vault/vault.hcl`:

```hcl theme={null}
storage "raft" {
  path    = "/opt/vault"
  node_id = "vault-2"

  retry_join {
    leader_api_addr = "http://10.1.101.25:8200"
  }
  retry_join {
    leader_api_addr = "http://10.1.101.199:8200"
  }
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = true
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "arn:aws:kms:us-east-1:003674902126:key/…"
}

api_addr     = "http://10.1.101.108:8200"
cluster_addr = "http://10.1.101.108:8201"
cluster_name = "vault"
ui           = true
log_level    = "INFO"
```

***

## 5. Configure retry\_join on vault-1 (10.1.101.199)

Finally, modify `/etc/vault/vault.hcl` on **vault-1**:

```hcl theme={null}
storage "raft" {
  path    = "/opt/vault"
  node_id = "vault-1"

  retry_join {
    leader_api_addr = "http://10.1.101.108:8200"
  }
  retry_join {
    leader_api_addr = "http://10.1.101.25:8200"
  }
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = true
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "arn:aws:kms:us-east-1:003674902126:key/…"
}

api_addr     = "http://10.1.101.199:8200"
cluster_addr = "http://10.1.101.199:8201"
cluster_name = "vault"
ui           = true
log_level    = "INFO"
```

***

## 6. Start Vault on All Nodes

Bring Vault back online on each server:

```bash theme={null}
sudo systemctl start vault
# Do this on vault-1, vault-2, vault-3
```

Verify that the service is running without errors:

```bash theme={null}
sudo systemctl status vault
```

***

## 7. Initialize the Cluster

Pick one node (e.g., **vault-1**) to initialize Vault:

```bash theme={null}
vault operator init
# You will see Recovery Keys and an Initial Root Token
```

> **lightbulb** Since AWS KMS auto-unseal is enabled, Vault will automatically unseal itself—no manual unseal commands are needed.

***

## 8. Verify Cluster Peers

Authenticate using the root token you received:

```bash theme={null}
vault login <Initial Root Token>
```

Then list your Raft peers:

```bash theme={null}
vault operator raft list-peers
# Output should show all three nodes and their roles:
# Node      Address            State     Voter
# ----      -------            -----     -----
# vault-1   10.1.101.199:8201  leader    true
# vault-2   10.1.101.108:8201  follower  true
# vault-3   10.1.101.25:8201   follower  true
```

Congratulations—your Vault HA cluster is up and running, with each node automatically discovering its peers via the `retry_join` configuration.

***

## What’s Next?

* Explore [AWS Auto-Join via Tags](https://www.vaultproject.io/docs/configuration/storage/raft#retry_join-aws) to replace static IPs with dynamic discovery.
* Review the official [Vault HA documentation](https://www.vaultproject.io/docs/enterprise/ha).

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/c1dd23ce-c7fd-4564-84d8-4ff14b115bd7/lesson/8dd8efdb-098a-4bca-b2dd-1753b74c0590)


# Demo Disaster Recovery DR Replication

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Build-Fault-Tolerant-Vault-Environments/Demo-Disaster-Recovery-DR-Replication/page

This guide explains how to configure Disaster Recovery replication between two Vault Enterprise clusters.

In this guide, you’ll configure Disaster Recovery (DR) replication across two Vault Enterprise clusters. We assume both single-node clusters are already initialized, unsealed, and you’re logged in as root:

* **Primary** (10.1.101.199, tan background)
* **Secondary** (10.1.101.108, white background)

> DR replication requires Vault Enterprise; it is not supported in the open-source edition.

***

## 1. Check Current Replication Status

On the **primary** (10.1.101.199), confirm DR and performance replication are disabled:

```bash theme={null}
ec2-user@ip-10-1-101-199 vault]$ vault read sys/replication/status
Key         Value
---         -----
dr          map[mode:disabled]
performance map[mode:disabled]
```

***

## 2. Enable DR Replication on Primary

Enable DR replication in **primary** mode:

```bash theme={null}
ec2-user@ip-10-1-101-199 vault]$ vault write -force sys/replication/dr/primary/enable
WARNING! The following warnings were returned from Vault:
* This cluster is being enabled as a primary for replication. Vault will be unavailable for a brief period and will resume service shortly.
```

> **lightbulb** Enabling primary DR replication causes a short downtime. Plan accordingly for production environments.

Verify that DR is now **primary**:

```bash theme={null}
ec2-user@ip-10-1-101-199 vault]$ vault read sys/replication/status
Key         Value
---         -----
dr          map[cluster_id:65b5025a-b5ee-67de-6df6-6b2033dc75ed mode:primary state:running ...]
performance map[mode:disabled]
```

Or view as JSON:

```bash theme={null}
ec2-user@ip-10-1-101-199 vault]$ vault read -format=json sys/replication/status | jq
{
  "data": {
    "dr": {
      "cluster_id": "65b5025a-b5ee-67de-d6f6-6b2033dc75ed",
      "mode": "primary",
      "state": "running",
      "known_secondaries": [],
      ...
    },
    "performance": {"mode":"disabled"}
  }
}
```

***

## 3. Generate a Secondary Token

Still on the **primary**, create a one-time wrapping token for the secondary:

```bash theme={null}
ec2-user@ip-10-1-101-199 vault]$ vault write -f sys/replication/dr/primary/secondary-token id=secondary-dallas
Key                   Value
---                   -----
wrapping_token        [C|JeHAiOjE2NTM0MTIxOTIsImlhdC1hIGB...]
wrapping_token_ttl    30m
wrapping_creation_path sys/replication/dr/primary/secondary-token
```

Copy the `wrapping_token` value (valid for 30 minutes).

***

## 4. Enable DR Replication on Secondary

Switch to the **secondary** (10.1.101.108) and join it to the primary:

```bash theme={null}
[root@ip-10-1-101-108 vault]# vault write -f sys/replication/dr/secondary/enable token=<WRAPPING_TOKEN>
WARNING! The following warnings were returned from Vault:
* Vault has successfully found secondary information; it may take a while to perform setup tasks. Vault will be unavailable until these tasks and initial sync complete.
```

> **triangle-alert** Enabling DR on a secondary **will wipe any existing data**. Be sure this node is dedicated for DR replication.

***

## 5. Verify DR Status on Secondary

On the **secondary**, confirm replication is active:

```bash theme={null}
[root@ip-10-1-101-108 vault]# vault read -format=json sys/replication/status | jq
{
  "data": {
    "dr": {
      "cluster_id": "65b5025a-b5ee-67de-6b2033dc75ed",
      "mode": "secondary",
      "state": "stream-wals",
      "connection_state": "ready",
      "secondary_id": "secondary-dallas",
      "known_primary_cluster_addr": ["https://10.1.101.199:8201"],
      ...
    },
    "performance": {"mode":"disabled"}
  }
}
```

> A DR secondary does **not** serve client requests—most paths are disabled.

***

## 6. Verify DR Status on Primary

Back on the **primary**, list known secondaries:

```bash theme={null}
[root@ip-10-1-101-199 vault]# vault read -format=json sys/replication/status | jq
{
  "data": {
    "dr": {
      "mode": "primary",
      "state": "running",
      "known_secondaries": ["secondary-dallas"],
      "secondaries": [
        {
          "api_address": "http://10.1.101.108:8200",
          "cluster_address": "https://10.1.101.108:8201",
          "connection_status": "connected",
          "node_id": "secondary-dallas",
          ...
        }
      ]
    },
    "performance": {"mode":"disabled"}
  }
}
```

***

## 7. DR Replication in the UI

### Primary Cluster Dashboard

1. Log in to the primary UI and go to **Status → Disaster Recovery**.

![The image shows a web interface for HashiCorp Vault, displaying the "Secrets Engines" section with a "cubbyhole" engine listed. The status menu on the right indicates the server is unsealed and operational.](https://kodekloud.com/kk-media/image/upload/v1752878298/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Disaster-Recovery-DR-Replication/hashicorp-vault-secrets-engines-interface.jpg)

2. Click **Disaster Recovery** to view replication details:

![The image shows a web interface for disaster recovery management, indicating the cluster's state as "running" and listing one known secondary connection.](https://kodekloud.com/kk-media/image/upload/v1752878298/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Disaster-Recovery-DR-Replication/disaster-recovery-management-web-interface.jpg)

3. Under **Manage**, you can disable replication, force a re-index, or demote this primary:

![The image shows a web interface for managing disaster recovery settings, with options to disable replication, recover, reindex, and demote a cluster.](https://kodekloud.com/kk-media/image/upload/v1752878299/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Disaster-Recovery-DR-Replication/disaster-recovery-settings-web-interface.jpg)

### Secondary Cluster Dashboard

On the secondary UI, you’ll land directly in the DR dashboard (no login prompt). It shows the cluster in **stream-wals** state:

![The image shows a "Disaster Recovery" dashboard from a Vault application, displaying the status and details of a secondary cluster's connection and replication settings. It includes information about the primary cluster address, connection state, and replication set ID.](https://kodekloud.com/kk-media/image/upload/v1752878300/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Disaster-Recovery-DR-Replication/disaster-recovery-dashboard-vault-application.jpg)

Under **Manage**, you can promote this secondary or generate an operational token:

![The image shows a web interface for promoting a disaster recovery cluster in Vault, with fields for entering a DR operation token and an optional primary cluster address.](https://kodekloud.com/kk-media/image/upload/v1752878301/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Disaster-Recovery-DR-Replication/disaster-recovery-cluster-vault-interface.jpg)

***

## Command Summary

| Step                        | Command                                                     | Description                           |
| --------------------------- | ----------------------------------------------------------- | ------------------------------------- |
| 1. Check Status             | `vault read sys/replication/status`                         | View current DR & performance mode    |
| 2. Enable Primary DR        | `vault write -force sys/replication/dr/primary/enable`      | Activate DR on primary                |
| 3. Generate Secondary Token | `vault write -f sys/replication/dr/primary/secondary-token` | Create a one-time token for secondary |
| 4. Enable Secondary DR      | `vault write -f sys/replication/dr/secondary/enable`        | Connect secondary to primary          |
| 5. Verify Secondary         | `vault read -format=json sys/replication/status`            | Confirm secondary is streaming WALs   |
| 6. Verify Primary           | `vault read -format=json sys/replication/status`            | List connected secondaries            |

***

## Links and References

* [Vault Replication Overview](https://www.vaultproject.io/docs/enterprise/replication)
* [sys/replication/dr API](https://www.vaultproject.io/api-docs/replication/dr)
* [Vault Enterprise Licensing](https://www.vaultproject.io/docs/enterprise)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/c1dd23ce-c7fd-4564-84d8-4ff14b115bd7/lesson/b87b9aa9-5eb3-4277-972f-8cc96c4b4ab3)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/c1dd23ce-c7fd-4564-84d8-4ff14b115bd7/lesson/7a7b4f9a-81c9-4a18-b3d4-06af23c64438)
