# Vault server configuration
disable_performance_standby = true
```

After restarting, the node will no longer advertise performance standby status.

***

## References

* [Vault HA Concepts](https://www.vaultproject.io/docs/concepts/ha)
* [Performance Standby in Enterprise](https://www.vaultproject.io/docs/enterprise/ha/performance-standby)
* [Integrated Storage Overview](https://www.vaultproject.io/docs/operations/storage/integrated)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b6a41fdb-447c-43b2-9489-6c8459821fab/lesson/b4aeb833-e804-4138-913b-280fc9b0e988" />
</CardGroup>


# Section Overview Scale Vault for Performance

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Scale-Vault-for-Performance/Section-Overview-Scale-Vault-for-Performance/page

Learn to optimize HashiCorp Vault for high throughput and low latency through key performance features and techniques.

In this lesson, you’ll learn how to optimize HashiCorp Vault for high throughput and low latency. We’ll cover four key areas:

* Batch Tokens
* Performance Standby Nodes (Vault Enterprise)
* Performance Replication (Vault Enterprise)
* Path Filters

<Callout icon="lightbulb">
  Performance Standby Nodes and Performance Replication features require Vault Enterprise.
</Callout>

| Feature                   | Vault Version    | Purpose                                      |
| ------------------------- | ---------------- | -------------------------------------------- |
| Batch Tokens              | OSS & Enterprise | Reduce client API calls and boost throughput |
| Performance Standby Nodes | Enterprise       | Offload read-only traffic                    |
| Performance Replication   | Enterprise       | Asynchronous data synchronization            |
| Path Filters              | OSS & Enterprise | Limit which secrets paths are replicated     |

<Frame>
  ![The image is an "Objective Overview" slide for scaling Vault for performance, listing tasks such as using batch tokens and configuring performance replication. It includes a certification badge and a cartoon character at the bottom right.](https://kodekloud.com/kk-media/image/upload/v1752878618/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Section-Overview-Scale-Vault-for-Performance/scaling-vault-performance-overview-slide.jpg)
</Frame>

## Batch Tokens

Let’s dive into the first topic: batch tokens.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b6a41fdb-447c-43b2-9489-6c8459821fab/lesson/12509202-2566-4999-a5b7-94f54cbca281" />
</CardGroup>
