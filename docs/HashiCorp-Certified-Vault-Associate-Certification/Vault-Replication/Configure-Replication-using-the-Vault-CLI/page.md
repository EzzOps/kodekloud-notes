# Configure Replication using the Vault CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Vault-Replication/Configure-Replication-using-the-Vault-CLI/page

This guide shows how to configure Vault DR replication using the Vault CLI in Vault Enterprise.

HashiCorp Vault’s Disaster Recovery (DR) replication ensures high availability by maintaining a standby cluster that can take over in case of a primary failure. This guide shows you how to configure DR replication using the Vault CLI in Vault Enterprise.

## Prerequisites

* Vault Enterprise license
* Two Vault clusters (Primary and Secondary)
* Network connectivity on port `8200` between clusters
* Vault CLI configured (`VAULT_ADDR` and token)

> \[!note]
> DR replication is an enterprise-only feature. Verify your Vault version supports DR replication before proceeding.

## Step 1: Enable DR on the Primary Cluster

On the **primary** Vault server, run:

```shell theme={null}
vault write -f sys/replication/dr/primary/enable
```

| Endpoint                          | Action                           |
| --------------------------------- | -------------------------------- |
| sys/replication/dr/primary/enable | Enable DR replication on primary |

## Step 2: Generate the Secondary Token

Still on the primary cluster, generate a token for the secondary:

```shell theme={null}
vault write sys/replication/dr/primary/secondary-token id="us-east2-dr"
```

* `id`: A meaningful identifier (e.g., region or datacenter).
* The command returns a `token` to use in Step 3.

> \[!warning]
> Keep the secondary token secret—avoid committing it to code repositories or logs.

## Step 3: Enable DR on the Secondary Cluster

On the **secondary** Vault server, use the token from Step 2:

```shell theme={null}
vault write sys/replication/dr/secondary/enable token="s.XXXXXXXXXXXXXX"
```

| Endpoint                            | Action                             |
| ----------------------------------- | ---------------------------------- |
| sys/replication/dr/secondary/enable | Enable DR replication on secondary |

## Example Workflow

```shell theme={null}
