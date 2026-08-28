# 1. Enable performance replication on the primary
vault write -f [SECRET_REDACTED]

# 2. Generate a secondary token
vault write [SECRET_REDACTED]-token id="region-west"

# 3. Enable performance replication on the secondary
vault write sys/[AWS_SECRET_ACCESS_KEY] token="s.XYZ1234"
```

<Callout icon="lightbulb">
  Enabling replication on a secondary wipes its existing data and replaces it with the primary’s data, including unseal and recovery keys.
</Callout>

## Monitoring Replication

Check status using:

```bash theme={null}
# Overall replication status
vault read -format=json sys/replication/status

# Performance replication
vault read -format=json sys/replication/performance/status

# DR replication (if configured)
vault read -format=json sys/replication/dr/status
```

***

## References

* [Vault Replication Concepts](https://www.vaultproject.io/docs/enterprise/replication)
* [High Availability with Vault Performance Replication](https://www.hashicorp.com/blog/vault-performance-replication)
* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b6a41fdb-447c-43b2-9489-6c8459821fab/lesson/2efdccb7-4865-412b-8473-d628f3a139b4" />
</CardGroup>


# Performance Standby Nodes

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Scale-Vault-for-Performance/Performance-Standby-Nodes/page

This article explains Performance Standby Nodes in HashiCorp Vault for scaling read throughput in Vault Enterprise.

Understanding Performance Standby Nodes is critical for scaling read throughput in Vault Enterprise. This guide covers:

* Vault Open Source HA behavior
* Vault Enterprise Performance Standby features
* Scaling out read performance
* Consistency and replication
* Health checks and routing
* Enabling/disabling performance standby

<Callout icon="lightbulb">
  You need to *describe* what performance standby nodes are and why they’re used. Configuration commands aren’t required for the HashiCorp exam.
</Callout>

***

## Vault Open Source HA Cluster

In **Vault Open Source**, an HA cluster contains:

* 1 active node (handles all reads and writes)
* Multiple standby nodes (forward requests to active, monitor health)

A load balancer must direct client traffic to the active node. If a client request lands on a standby, Vault uses RPC forwarding (or returns a redirect) so that only the active processes reads and writes.

<Frame>
  ![The image illustrates a Vault clustering setup with five nodes, where Node C is active, and the others are on standby. It also shows a developer making credential requests with read and write permissions.](https://kodekloud.com/kk-media/image/upload/v1752878610/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/vault-clustering-setup-five-nodes.jpg)
</Frame>

Because standby nodes don’t respond to reads or writes locally, scaling in Vault OSS means scaling **up**—increasing CPU, memory, or disk size rather than adding more nodes.

<Frame>
  ![The image illustrates a Vault Clustering setup with five nodes, where Node C is active, and the others are on standby. It shows a developer making a credential request, with a note that Vault OSS is a scale-up application.](https://kodekloud.com/kk-media/image/upload/v1752878611/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/vault-clustering-setup-five-nodes-2.jpg)
</Frame>

| Feature               | Vault Open Source | Vault Enterprise          |
| --------------------- | ----------------- | ------------------------- |
| Active writes         | Yes               | Yes                       |
| Standby reads         | No                | Yes (performance standby) |
| Scaling method        | Scale-up          | Scale-out                 |
| Licensing requirement | None              | Enterprise license        |

***

## Vault Enterprise with Performance Standby Nodes

Vault Enterprise introduces **Performance Standby** nodes that:

* Serve **read** requests locally
* Forward **write** requests to the active node
* Scale out read capacity by adding more performance standby nodes

<Frame>
  ![The image illustrates a Vault Clustering setup for enterprise, showing multiple Vault nodes (A to E) with their read and write capabilities, and a developer making credential requests. Node C is active, while others are in performance standby.](https://kodekloud.com/kk-media/image/upload/v1752878613/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/vault-clustering-setup-nodes-diagram.jpg)
</Frame>

<Frame>
  ![The image is a slide about "Vault Enterprise with Performance Standby," explaining how performance standby nodes can handle read requests to scale a cluster and maintain high availability. It includes a reminder that this functionality is specific to Vault Enterprise.](https://kodekloud.com/kk-media/image/upload/v1752878614/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/vault-enterprise-performance-standby-slide.jpg)
</Frame>

***

## Scaling Out Read Performance

To scale read performance in Vault Enterprise:

1. **Add performance standby nodes** to your cluster.
2. **Configure your load balancer** or DNS to route read-only traffic to performance standby nodes.
3. **Use health checks** to differentiate between active (writes+reads) and performance standby (reads only).

<Frame>
  ![The image illustrates a system architecture for "Scaling Out with Performance Secondaries," showing an active node and multiple performance standby nodes connected in a sequence. It includes a label indicating scaling out for read performance.](https://kodekloud.com/kk-media/image/upload/v1752878615/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/scaling-out-performance-secondaries-architecture.jpg)
</Frame>

### Defining a Read

A **read** is any Vault operation that does *not* result in a storage write. Examples include:

```bash theme={null}
vault read secret/data/my-app/config
```

Common read-only engines:

* **Key/Value Secrets Engine**: fetching secrets
* **Transit Secrets Engine**: encrypt/decrypt without persisting data
* **SSH Signing**: signing client keys without storage

Performance standby nodes can service these requests locally, reducing load on the active node.

***

## Consistency and Eventual Replication

When using [Integrated Storage](https://www.vaultproject.io/docs/operations/storage/integrated), replication to performance standbys is **eventual**. After a write:

1. Active node commits locally.
2. Changes replicate asynchronously to standby nodes.
3. Standbys serve fresh data only after replication completes.

<Callout icon="triangle-alert">
  A client reading immediately from a performance standby might see stale data or receive an error until replication finishes.
</Callout>

<Frame>
  ![The image illustrates a diagram of a system with five Vault Nodes labeled A to E, showing their roles in eventual consistency. Node C is marked as "Active" and "Write," while the others are in "Performance Standby."](https://kodekloud.com/kk-media/image/upload/v1752878615/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/vault-nodes-consistency-diagram.jpg)
</Frame>

***

## Health Checks and Targeting Standbys

Use Vault’s health endpoint and a load balancer to route traffic:

Endpoint:

```text theme={null}
GET /v1/sys/health
```

HTTP status codes:

| Status Code | Meaning                          |
| ----------- | -------------------------------- |
| 200         | Active (initialized & unsealed)  |
| 473         | Performance standby (reads only) |
| 501/503     | Uninitialized or sealed          |

Configure your load balancer to send read-only clients to nodes returning **473** and all other traffic to **200**.

<Frame>
  ![The image is a slide explaining how to target a performance standby in Vault, detailing health information endpoints and default status codes. It includes a note that these details are not needed for an exam.](https://kodekloud.com/kk-media/image/upload/v1752878617/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Performance-Standby-Nodes/vault-performance-standby-health-info.jpg)
</Frame>

***

## Enabling and Disabling Performance Standby

Performance standby is **enabled by default** for Vault Enterprise with a valid license. To disable:

```hcl theme={null}
