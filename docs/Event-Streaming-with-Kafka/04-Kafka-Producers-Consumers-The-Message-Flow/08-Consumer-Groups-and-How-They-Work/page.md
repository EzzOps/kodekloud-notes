# Consumer Groups and How They Work

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Consumer-Groups-and-How-They-Work/page

Explains Kafka consumer groups, partition assignment, scaling, fault tolerance, rebalancing, ordering guarantees, delivery semantics, and best practices for scalable, coordinated consumption of topic data.

Welcome back.

In the previous lesson we covered what a consumer is and how to configure a consumer to read messages from a Kafka topic. In this lesson we’ll explain consumer groups: what they are, why they matter, and how they enable scalable, fault-tolerant consumption of topic data.

## Recap: producers and consumers

* Producers publish events to Kafka topics.
* Consumers read and process those events.

Consider this scenario:

* A topic named "topic A" has four partitions: partition 1–4.
* One consumer is responsible for reading and processing all messages from those four partitions.

If event traffic is low, a single consumer may keep up. In high-throughput environments (for example, telemetry from many IoT devices), a single consumer will likely fall behind: while it processes messages from partition 1, new messages on other partitions queue up, limiting throughput.

## Introducing consumer groups

A consumer group is a set of consumers that coordinate to consume data from the same topic. Group members can perform identical processing (to scale throughput) or different processing tasks while consuming the same topic.

Kafka divides partition ownership among the members of a consumer group so each partition is read by at most one consumer in the group. That enables parallel processing of partitions and scales consumption horizontally.

Example: two consumers

* Consumer 1 → partitions 1 and 2
* Consumer 2 → partitions 3 and 4

This distributes workload and increases throughput. If you add more consumers (for example, consumers 3 and 4), Kafka will assign partitions so that each active consumer handles one or more partitions.

<Frame>
  <img alt="The image illustrates how Kafka consumer groups work, showing the distribution of partitions across multiple consumers within a consumer group labeled as &#x22;Consumer Group A.&#x22;" />
</Frame>

Small assignment example (conceptual)

```text theme={null}
Topic "topic-A" partitions: P0, P1, P2, P3

Consumer group "group-A" with two consumers:
  consumer-A -> P0, P1
  consumer-B -> P2, P3
```

## Key behaviors and guarantees

| Behavior                           | Description                                                                                                                                                                                                                             |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Partition assignment               | Each partition within a consumer group is assigned to exactly one consumer at a time.                                                                                                                                                   |
| Ordering                           | Kafka guarantees ordering within a partition. Because a single consumer reads a partition at any time, per-partition ordering is preserved.                                                                                             |
| Parallelism limit                  | The maximum number of concurrently active consumers for a topic equals the number of partitions. Extra consumers remain idle until partitions become available.                                                                         |
| Duplication and delivery semantics | A partition is not processed in parallel by two consumers in the same group, but Kafka’s default semantics are typically at-least-once. Exactly-once end-to-end requires idempotent producers, transactions, or external deduplication. |

> **lightbulb** A partition is consumed by exactly one consumer in a consumer group at any time, which prevents parallel duplicate processing across consumers. That said, Kafka’s default delivery semantics are typically at-least-once; achieving true exactly-once processing end-to-end requires extra safeguards.

<Frame>
  <img alt="The image explains how consumer groups function, highlighting parallel processing and message guarantees. It describes how consumers in a group process partitions and ensure ordered message processing." />
</Frame>

## Recommended practice

* To maximize parallel processing while preserving per-partition ordering, create up to N active consumers for a topic with N partitions (one consumer per partition).
* Tune consumer session and heartbeat settings so that occasional transient network hiccups do not trigger unnecessary rebalances.
* Use idempotent producers, transactions, or an external deduplication layer if you require exactly-once semantics.

## Fault tolerance, rebalancing, and coordination

When a consumer leaves the group (crash, network partition, or graceful shutdown), the group coordinator triggers a rebalance to reassign the affected partitions to remaining consumers. Rebalancing restores availability but introduces transient overhead and short pauses while assignments are recomputed and consumers resume fetches.

Consumer group coordination is handled by the Kafka broker (the group coordinator), which manages group membership, heartbeats, partition assignments, and rebalances. Historically, Kafka used ZooKeeper for metadata and coordination; modern Kafka can run in KRaft mode (Kafka Raft metadata mode) to manage controller responsibilities without ZooKeeper. Both are cluster-level concerns important for administrators.

<Frame>
  <img alt="The image illustrates how consumer groups work, focusing on aspects like group coordination, group scaling, and rebalancing overhead. Each aspect is described with an icon and brief explanation." />
</Frame>

> **warning** Frequent or large rebalances can cause noticeable processing pauses. Design your consumer scaling strategy and tune session/heartbeat settings to minimize unnecessary rebalances.

## Scaling consumer groups

* Add consumers to a group to increase throughput when load grows; remove them when load drops.
* Each membership change causes a rebalance; plan scaling (and sticky assignment strategies) to reduce churn.
* Use monitoring (consumer lag, partition distribution) to decide when to scale horizontally.

This concludes the lesson. Next, we will dive deeper into how rebalancing works and what happens under the hood when group membership changes.

## Links and references

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* [Kafka Consumer API — Group management](https://kafka.apache.org/uses)
* [KRaft mode overview](https://kafka.apache.org/documentation/#kraft)

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/54e3f4cb-93be-42c7-aa5e-3003bff81f54)
