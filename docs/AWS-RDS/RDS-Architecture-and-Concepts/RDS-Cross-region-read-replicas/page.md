# RDS Cross region read replicas

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/RDS-Cross-region-read-replicas/page

Explains Amazon RDS cross region read replicas, their asynchronous read scaling, latency reduction for distant users, operational behaviors, costs, encryption and promotion considerations.

This page explains Amazon RDS cross‑region read replicas: what they are, when to use them, operational characteristics, and important cost and security considerations.

Problem statement

* You run your primary RDS instance in one AWS region (for example, US‑East) because most users are there.
* As your application grows globally, users from other regions (for example, Africa) access the same primary database, increasing latency and degrading read performance for those distant users.

Solution overview

* Create a cross‑region read replica in the target region closer to those users.
* A read replica serves read traffic locally, reducing latency and improving user experience.
* Read replicas are read‑only copies that receive updates from the primary database asynchronously; they are intended for read scaling and geographic locality—not synchronous, zero‑lag replication.

<Frame>
  <img alt="A slide titled &#x22;RDS Cross-Region Read Replicas&#x22; showing a stylized map with a database icon in North America connected by a dashed line labeled &#x22;AWS Secure communication channel&#x22; to a database icon in Africa labeled &#x22;Cross-region read replica.&#x22;" />
</Frame>

How cross‑region replication works

* Replication traffic is routed over AWS’s managed backbone. Data in transit is protected (for example, TLS/SSL where applicable).
* Replication between source and cross‑region replica is asynchronous — occasional replication lag is normal.
* If the source DB is encrypted at rest, any cross‑region snapshot or replica must also be encrypted. This requires KMS keys in the replica’s region; see AWS KMS documentation for cross‑region key management: [https://docs.aws.amazon.com/kms/latest/developerguide/](https://docs.aws.amazon.com/kms/latest/developerguide/).

Operational characteristics

* Asynchronous replication: expect eventual consistency for replica reads.
* Read‑only by default: replicas cannot process writes until promoted to a standalone primary.
* Promotion: you can promote a read replica to read/write, but promotion changes topology and can result in downtime during switchover.
* Engine differences: features and cross‑region behaviors vary by engine. For example, Amazon Aurora provides a dedicated Global Database feature optimized for low‑latency global reads: [https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html).

<Callout icon="lightbulb">
  Cross‑region read replicas are designed to improve read latency and scale reads for geographically distributed users. They are asynchronous and intended for read scaling and geographic locality — not for synchronous cross‑region writes or instant failover.
</Callout>

Cost, security, and operational considerations

| Consideration                | Impact                                                                           | Recommendation                                                                              |
| ---------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Inter‑region data transfer   | Replication traffic incurs AWS inter‑region transfer charges                     | Estimate ongoing transfer costs before provisioning replicas                                |
| Additional compute & storage | Each replica is a separate instance with its own hourly and storage costs        | Right‑size replica instance and storage; consider reserved instances or savings plans       |
| Replication lag              | Asynchronous replication can cause stale reads on the replica                    | Use for workloads that tolerate eventual consistency (analytics, reporting, regional reads) |
| Encryption & KMS             | Cross‑region replicas of encrypted sources require KMS keys in the target region | Plan KMS key replication or use separate KMS keys and adjust snapshot copy operations       |
| Failover behavior            | Failover is not automatic to a cross‑region replica                              | Implement application routing and runbooks for promotion and DNS updates                    |

When to use cross‑region read replicas

| Use case                                     | Why a cross‑region replica helps                                                |
| -------------------------------------------- | ------------------------------------------------------------------------------- |
| Large read‑heavy user base in another region | Reduces network latency and improves read performance                           |
| Regional analytics or reporting pipelines    | Offloads analytics reads from primary and keeps compute local                   |
| Geographic locality requirements for reads   | Provides local read endpoints without running active writes in multiple regions |

When not to use them

* Only a very small portion of traffic is from the remote region — added costs may not justify benefits.
* Your application requires synchronous, strongly consistent cross‑region writes — cross‑region read replicas cannot provide this.

Promotion and failover

* You can promote a cross‑region read replica to a standalone read/write instance when needed.
* Promotion typically requires application cutover (DNS changes, failover testing) and may create a second writable primary; plan for potential downtime and data reconciliation needs.

Alternatives and engine‑specific options

* Amazon Aurora Global Database is optimized for low‑latency global reads and can be preferable for Aurora workloads: [https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)
* For non‑Aurora engines, cross‑region read replicas are the common approach to provide regional read endpoints.

<Callout icon="warning">
  Before creating cross‑region read replicas, evaluate replication lag tolerance, ongoing inter‑region transfer and instance costs, and encryption key requirements in the target region (KMS). For Aurora workloads, consider Aurora Global Database as a lower‑latency alternative.
</Callout>

Links and references

* Amazon RDS Read Replicas documentation: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER\_ReadRepl.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
* AWS Key Management Service (KMS) guide: [https://docs.aws.amazon.com/kms/latest/developerguide/](https://docs.aws.amazon.com/kms/latest/developerguide/)
* Amazon Aurora Global Database: [https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)
* AWS Data Transfer Pricing (inter‑region): [https://aws.amazon.com/ec2/pricing/on-demand/#Data\_Transfer](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer)

Summary

* Cross‑region read replicas are a practical way to reduce read latency and scale read throughput for geographically distributed users.
* They are asynchronous and read‑only; plan for replication lag, cross‑region costs, and KMS key management.
* Choose cross‑region replicas when geographic read locality and read scalability outweigh added cost and operational complexity.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/b3c847e6-7c77-40bf-b3cf-badf08c9937d" />
</CardGroup>
