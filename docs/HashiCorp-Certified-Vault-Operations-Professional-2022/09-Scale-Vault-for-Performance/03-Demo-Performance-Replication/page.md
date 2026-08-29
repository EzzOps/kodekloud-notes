# [...]
```

## Batch Token Characteristics

| Feature       | Description                            |
| ------------- | -------------------------------------- |
| No Accessor   | Won’t appear in `auth/token/accessors` |
| Non-Renewable | `renewable: false`                     |
| Non-Revocable | Attempts to revoke result in an error  |

```bash theme={null}
vault token revoke hvb.AAAAQL7ypVnQ...
vault token renew hvb.AAAAQL7ypVnQ...
# Error renewing token: batch tokens cannot be renewed
```

> **triangle-alert** Batch tokens cannot be renewed or revoked. Plan token lifecycles accordingly.

## Using a Batch Token

Authenticate and export the token:

```bash theme={null}
vault login hvb.AAAAQL7ypVnQ...
```

```text theme={null}
Success! You are now authenticated.
```

```bash theme={null}
export VAULT_TOKEN=hvb.AAAAQL7ypVnQ...
```

If you lack permissions, listing secrets fails:

```bash theme={null}
vault secrets list
# Error listing secrets engines: permission denied
```

Clean up by unsetting the token:

```bash theme={null}
unset VAULT_TOKEN
vault secrets list
# Error listing secrets engines: permission denied
```

***

You’ve now learned how to create, inspect, and securely use Vault Batch Tokens. For more details, see the [Vault Tokens documentation](https://www.vaultproject.io/docs/concepts/token/).

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b6a41fdb-447c-43b2-9489-6c8459821fab/lesson/38df6481-bcbd-4c5c-b7ea-061362970f7f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b6a41fdb-447c-43b2-9489-6c8459821fab/lesson/b6d94cbf-1da0-4a4b-a8e0-b898706cc2b3)


# Demo Performance Replication

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Scale-Vault-for-Performance/Demo-Performance-Replication/page

This tutorial covers configuring Vault Enterprise performance replication between primary and secondary clusters for high-throughput, low-latency synchronization.

In this tutorial, you’ll configure Vault Enterprise performance replication between two clusters—a primary and a secondary. Performance replication streams all changes on the primary (auth methods, secrets engines, data, audit logs, etc.) to the secondary, ensuring high-throughput, low-latency synchronization.

## Cluster Details

| Role      | IP Address   |
| --------- | ------------ |
| Primary   | 10.1.102.170 |
| Secondary | 10.1.102.156 |

***

## 1. Enable Performance Replication on the Primary

1. Authenticate to the primary cluster:

   ```bash theme={null}
   ec2-user@ip-10-1-102-170:~$ vault login hvs.KYjTNrIdZaOPkriOuD5tfClA
   Success! You are now authenticated. Future Vault clients will automatically use this token.
   ```

2. Enable the primary replication role:

> **triangle-alert** Enabling the primary replication role will briefly make Vault unavailable. Expect a short service interruption.

```bash theme={null}
ec2-user@ip-10-1-102-170:~$ vault write -f sys/replication/performance/primary/enable
WARNING! The following warnings were returned from Vault:
* This cluster is being enabled as a primary for replication. Vault will be unavailable for a brief period and will resume service shortly.
```

3. Generate a wrapped token for the secondary:

   ```bash theme={null}
   ec2-user@ip-10-1-102-170:~$ vault write sys/replication/performance/primary/secondary-token id=hcvop-performance
   Key                           Value
   ---                           -----
   wrapping_token                eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   wrapping_token_ttl            30m
   wrapping_token_creation_time  2022-06-02T01:19:11.387715359Z +0000 UTC
   wrapping_token_creation_path  sys/replication/performance/primary/secondary-token
   ```

> **lightbulb** Copy the `wrapping_token` value; you’ll need it to enable replication on the secondary node.

***

## 2. Enable Performance Replication on the Secondary

1. Authenticate to the secondary cluster:

   ```bash theme={null}
   ec2-user@ip-10-1-102-156:~$ vault login hvs.AVecCoMzQSmLYTQ9ufdpRAZ
   Success! You are now authenticated.
   ```

2. Initialize the secondary with the wrapped token:

   ```bash theme={null}
   ec2-user@ip-10-1-102-156:~$ vault write sys/replication/performance/secondary/enable \
       token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   WARNING! The following warnings were returned from Vault:
   * Vault has successfully found secondary information; it may take a while to perform setup tasks. Vault will be unavailable until these tasks and the initial sync complete.
   ```

***

## 3. Verify Replication Status

Run this command on **either** node to check the performance replication status:

```bash theme={null}
ec2-user@ip-10-1-102-156:~$ vault read sys/replication/performance/status
Key                           Value
---                           -----
cluster_id                    d7c75ca6-1cc4-bc99-faa1-db2401ec56bf
connection_state              ready
known_primary_cluster_addrs   [https://10.1.102.170:8201]
mode                          secondary
state                         stream-wals
```

| Field                          | Description                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| connection\_state              | `ready` indicates the link is active and healthy.             |
| mode                           | `primary` or `secondary` role of this node.                   |
| state                          | Replication phase; `stream-wals` is continuous log streaming. |
| known\_primary\_cluster\_addrs | List of primary endpoint URLs.                                |

***

## 4. Token & Unseal Key Behavior

Once performance replication is active, the secondary cluster adopts the primary’s unseal keys and root tokens.

* Attempting to log in with the old secondary root token fails:

  ```bash theme={null}
  ec2-user@ip-10-1-102-156:~$ vault login hvs.AVecCoMzQSmYLytQ9ufdpRA2
  Error making API request.
  Code: 403. Errors:
  * permission denied
  ```

* Use the primary’s root token to authenticate on the secondary:

  ```bash theme={null}
  ec2-user@ip-10-1-102-156:~$ vault login hvs.KYjTNrIdZaOPkriOuD5tfClA
  Success! You are now authenticated.
  ```

***

## 5. Replicating Auth Methods, Secrets Engines & Data

All Vault configuration changes—enabled auth methods, secrets engines, user accounts, and KV data—on the primary automatically replicate to the secondary.

**Example: Enable `userpass` auth and create a user on the primary:**

```bash theme={null}
