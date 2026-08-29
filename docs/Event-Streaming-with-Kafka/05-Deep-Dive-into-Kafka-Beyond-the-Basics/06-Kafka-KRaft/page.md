# Kafka KRaft

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/Kafka-KRaft/page

Explains Kafka's KRaft architecture replacing ZooKeeper with embedded Raft consensus to simplify operations, improve scalability, and streamline migrations.

Welcome — in this article we’ll explain Kafka’s KRaft architecture, why it was introduced, and how it simplifies Kafka operations by removing the ZooKeeper dependency.

ZooKeeper historically acted as the external coordination service for Kafka, managing cluster metadata, broker state, and leader elections. While functional, this separation introduced operational and development complexity that grew with cluster size.

<Frame>
  <img alt="The image highlights the issue of complexity with Zookeeper in managing a Kafka cluster, depicting it with gears and a warning sign on a computer screen." />
</Frame>

Operational teams had to provision, monitor, and maintain a distinct ZooKeeper ensemble alongside Kafka brokers. That extra service increases cost, lengthens incident response, and creates more surface for configuration errors and outages.

<Frame>
  <img alt="The image discusses the operational overhead associated with Zookeeper, emphasizing the additional effort required for deployment, monitoring, and scaling. There is an illustration of a person holding a document with a smartphone displaying gears." />
</Frame>

As deployments scale—more brokers, more topics, and many partitions—ZooKeeper’s role in coordinating metadata can become a throughput and latency bottleneck. That limits Kafka’s ability to scale smoothly without additional operational tuning.

<Frame>
  <img alt="The image discusses the issue of Zookeeper's scaling limitations, showing a performance chart and mentioning its impact on large Kafka clusters." />
</Frame>

Another practical drawback: ZooKeeper is a separate open-source project. When Kafka introduces metadata or controller changes, corresponding coordination logic or API changes sometimes require cross-project work, complicating releases and testing.

To solve these problems, Kafka introduced KRaft (Kafka Raft). KRaft embeds a Raft-based consensus layer directly into Kafka brokers so brokers themselves manage metadata and controller responsibilities—eliminating the need for an external ZooKeeper ensemble.

<Frame>
  <img alt="The image discusses the evolution of Kafka's architecture, highlighting an issue with Zookeeper and Kafka's move toward self-management with KRaft to eliminate Zookeeper's need." />
</Frame>

How KRaft works at a glance:

* A subset of brokers form the metadata quorum.
* The quorum elects a controller using Raft leader election.
* The elected controller handles metadata changes, leader elections, and other control-plane tasks.
* Metadata is persisted into an internal metadata topic managed by Kafka brokers themselves.

<Frame>
  <img alt="The image illustrates Kafka's Zookeeper role, showing five brokers and a leader in a cluster, with metadata topic partitions numbered from 0 to 10." />
</Frame>

Key benefits of migrating to or starting with KRaft:

| Area                     | ZooKeeper (traditional)                               | KRaft (integrated)                                       |
| ------------------------ | ----------------------------------------------------- | -------------------------------------------------------- |
| Operational surface      | Separate ZooKeeper cluster to deploy and manage       | Only Kafka brokers to run and monitor                    |
| Cost & resource usage    | Additional nodes and management overhead              | Right-sized clusters; lower total cost                   |
| Failure recovery         | Depends on external ensemble health and configuration | Faster Raft-based controller failover built into brokers |
| Development lifecycle    | Coordination changes may touch two projects           | Unified codebase reduces cross-project changes           |
| Security & configuration | Two systems to secure/configure                       | Single, standardized security model                      |

<Frame>
  <img alt="The image displays a list of Kafka KRraft features, highlighting right-sized clusters, enhanced stability, a unified security model, and standardized configuration." />
</Frame>

Because Raft is embedded, controller failover is faster and more predictable: if a controller broker fails, the metadata quorum elects a replacement rapidly without relying on an external service—improving availability and reducing downtime during control-plane failures.

<Frame>
  <img alt="The image outlines features of Kafka KRraft, highlighting simplified startup and deployment, instant controller failover, and elimination of Zookeeper dependency." />
</Frame>

> **lightbulb** For new open-source Kafka deployments, prefer KRaft unless you have specific constraints requiring ZooKeeper. KRaft reduces operational overhead and often improves scalability and reliability.

> **warning** Existing Kafka clusters that use ZooKeeper require a careful, planned migration to KRaft. Migration involves metadata export/import, rolling broker upgrades, and validation—plan tests and backups before migrating production workloads.

Summary

* KRaft replaces ZooKeeper by integrating Raft-based consensus into Kafka brokers.
* It reduces operational complexity, simplifies security and configuration, and improves controller availability.
* For greenfield deployments choose KRaft; for brownfield clusters plan and test the migration carefully.

Links and references

* [Apache Kafka KRaft (official)](https://kafka.apache.org/documentation/#kraft)
* [Raft consensus algorithm — Diego Ongaro & John Ousterhout](https://raft.github.io/)
* [Kafka documentation — migration to KRaft](https://kafka.apache.org/documentation/#migration)

That concludes this lesson/article.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/08fadb98-c4e6-46e0-9aff-40623fbda81d)
