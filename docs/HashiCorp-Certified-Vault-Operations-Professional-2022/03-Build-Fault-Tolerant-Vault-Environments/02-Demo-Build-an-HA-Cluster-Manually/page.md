# Peer removed successfully!
```

After removal, re-run `vault operator raft list-peers` to confirm.

A hands-on lab will walk you through both manual and automated cluster formation.

## Links and References

* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
* [Vault Integrated Storage (Raft)](https://www.vaultproject.io/docs/configuration/storage/raft)
* [Consul Storage Backend](https://www.consul.io/docs)
* [Vault Operations Professional Certification](https://www.hashicorp.com/certification/vault-operations-professional)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/c1dd23ce-c7fd-4564-84d8-4ff14b115bd7/lesson/8cfe546c-02ba-4273-a3e2-19f0d82fa146" />
</CardGroup>


# Demo Build an HA Cluster Manually

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Build-Fault-Tolerant-Vault-Environments/Demo-Build-an-HA-Cluster-Manually/page

This tutorial guides manual deployment of a high-availability Vault cluster on AWS EC2 using Raft and AWS KMS for auto-unseal.

In this tutorial, you’ll manually deploy a three-node Vault cluster on AWS EC2 using the Raft storage backend and AWS KMS auto-unseal. This configuration provides strong consistency, high-availability failover, and seamless unsealing.

## Cluster Topology

We have three EC2 instances running Vault v1.10.3+ent:

| Node    | IP Address   | Role               |
| ------- | ------------ | ------------------ |
| vault-3 | 10.1.101.25  | Initial leader     |
| vault-1 | 10.1.101.199 | Follower candidate |
| vault-2 | 10.1.101.108 | Follower candidate |

Each instance is configured with:

* `storage "raft"` (Vault Raft storage backend)
* `seal "awskms"` (AWS KMS auto-unseal)

## 1. Verify Vault Status on All Nodes

On each node, confirm Vault is running but neither initialized nor unsealed:

```bash theme={null}
vault status
```

Expected output:

Key                     Value

***

Recovery Seal Type      awskms\
Initialized             false\
Sealed                  true\
Version                 1.10.3+ent\
Storage Type            raft\
HA Enabled              true

## 2. Initialize the Leader (vault-3)

SSH into vault-3 and run:

```bash theme={null}
vault operator init
```

Save the recovery keys and the Initial Root Token securely.

```bash theme={null}
vault status
```

Now you should see `Initialized true` but `Sealed true`. AWS KMS will auto-unseal followers when they join.

<Callout icon="triangle-alert">
  Store your recovery keys and root token in a secure vault or vaultless backup. Losing them can lock you out of your cluster.
</Callout>

<Callout icon="lightbulb">
  Ensure the IAM role attached to each EC2 instance has permissions to decrypt with your AWS KMS key, or auto-unseal will fail.
</Callout>

## 3. List Raft Peers on vault-3

Authenticate with the root token and list peers:

```bash theme={null}
vault login <root-token>
vault operator raft list-peers
```

Initially, only vault-3 appears as the `leader`.

## 4. Join vault-1 to the Cluster

On vault-1:

```bash theme={null}
vault operator raft join http://10.1.101.25:8200
```

Back on vault-3, watch vault-1 join and become a voter:

```bash theme={null}
vault operator raft list-peers
```

Repeat until vault-1’s **Voter** column is `true`. Then on vault-1:

```bash theme={null}
vault status
```

You should see:

* `Initialized true`
* `Sealed false`
* `Performance Standby Node true`

## 5. Add vault-2 to the Raft Cluster

On vault-2:

```bash theme={null}
vault operator raft join http://10.1.101.25:8200
```

Confirm all three peers are present and voters on any node:

```bash theme={null}
vault operator raft list-peers
```

## 6. Test Leader Failover

1. **Stop** Vault on the current leader (vault-3):
   ```bash theme={null}
   sudo systemctl stop vault
   ```
2. On vault-1 or vault-2, confirm a new leader election:
   ```bash theme={null}
   vault operator raft list-peers
   ```
3. **Restart** vault-3:
   ```bash theme={null}
   sudo systemctl start vault
   ```

vault-3 rejoins as a follower and does not reclaim leadership automatically.

## 7. Manual Step-Down

Force the current leader to step down manually (on vault-1, for example):

```bash theme={null}
vault operator step-down
```

Confirm the new leader:

```bash theme={null}
vault operator raft list-peers
```

## Summary

* Initialized vault-3 and formed a single-node cluster.
* Joined vault-1 and vault-2 with `vault operator raft join`.
* Verified AWS KMS auto-unseal on followers.
* Simulated automatic leader election by stopping the leader.
* Demonstrated manual failover using `vault operator step-down`.

Next, we’ll automate cluster formation with the \[Raft retry-join configuration] and EC2 tags for dynamic membership.

## Links and References

* [Vault Raft Storage Backend](https://www.vaultproject.io/docs/concepts/raft-backend)
* [Vault AWS KMS Auto-Unseal](https://www.vaultproject.io/docs/seal/aws-kms)
* [Raft Retry-Join Configuration](https://www.vaultproject.io/docs/configuration/retry-join#raft)
* [Using EC2 Tags](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/c1dd23ce-c7fd-4564-84d8-4ff14b115bd7/lesson/81a2a13d-24d9-4754-89d7-13e97ce7e060" />
</CardGroup>
