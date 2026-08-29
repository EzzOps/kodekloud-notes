# Consumer Rebalancing

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Consumer-Rebalancing/page

Explains Kafka consumer rebalancing, triggers, eager vs cooperative protocols, pauses during reassignment, and operational best practices

Welcome back.

In this lesson we'll cover consumer rebalancing in Kafka — what it is, why it happens, and how it impacts your consumer applications.

Overview of the architecture

Imagine a Kafka cluster with brokers 1, 2, 3, and 4. Topic A has four partitions. A consumer group contains four consumers, each assigned to one partition so messages are processed in parallel.

If consumer 4 fails, partition 4 stops being processed. In a real-world stream (for example, a payment stream) this could block critical messages until the system recovers. Kafka prevents prolonged stalls by reassigning partitions via consumer rebalancing.

What triggers a rebalance

* A consumer leaves the group (crash or graceful shutdown).
* A new consumer joins the group.
* Topic partition count changes, or subscription changes.
* Administrative changes that affect group membership or partition assignments.

What happens during a rebalance

* The group coordinator detects the membership change and pauses assignment while it computes a new mapping of partitions to consumers.
* Consumers may revoke their current partitions, then receive new partition assignments.
* After assignments are delivered, consumers resume processing the newly assigned partitions.

Following our example: when consumer 4 fails, the coordinator will reassign partition 4 to another active consumer (e.g., consumer 3). That consumer begins processing partition 4’s messages after the assignment is applied.

Rebalancing protocols

Kafka supports two main rebalancing protocols: eager (stop-the-world) and cooperative (incremental). Each has trade-offs in complexity and disruption.

| Protocol                  | Behavior                                                                                                   | Impact                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Eager (stop-the-world)    | Consumers revoke all partitions, coordinator computes a full reassignment, consumers re-acquire partitions | Simpler to implement but causes a short pause where no consumer in the group processes messages                        |
| Cooperative (incremental) | Only the minimal set of partitions required for a safe transition are revoked and reassigned               | Less disruptive — most partitions continue to be processed during reassignment; implemented via KIPs such as `KIP-429` |

<Callout icon="lightbulb">
  Cooperative rebalancing (introduced via KIPs such as [KIP-429](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%[SECRET_REDACTED])) reduces the scope of the pause by moving partitions incrementally. Eager rebalancing is simpler but causes a short “stop-the-world” pause for all consumers in the group.
</Callout>

Why the brief pause exists

The brief pause during rebalancing is intentional: it maintains data consistency and prevents duplicated or missed messages while ownership of partitions moves between consumers. Kafka’s coordinator and consumer protocols are optimized to minimize the duration of these pauses so consumer lag remains low.

Key points to remember

1. Partition reassignment\
   Whenever consumers join or leave a consumer group, Kafka redistributes topic partitions among active consumers to maintain balanced processing and avoid idle or overloaded consumers.

<Frame>
  <img alt="The image describes the process of Kafka consumer rebalancing, highlighting partition reassignment, group membership changes, and consumption pauses to ensure data consistency." />
</Frame>

2. Consumer group membership change\
   Any change in membership—crash, shutdown, or a new consumer joining—triggers the group coordinator to re-evaluate and reassign partitions to keep the consumer group healthy.

3. Consumption pause\
   During the rebalance, Kafka temporarily pauses consumption for the affected consumers to ensure messages are not missed or duplicated. Cooperative rebalancing reduces the scope and duration of these pauses compared with eager rebalancing.

<Frame>
  <img alt="The image outlines the concept of consumer rebalancing in Kafka, including partition reassignment, group membership change, and consumption pause, to ensure data consistency." />
</Frame>

Best practices and operational tips

* Prefer cooperative rebalancing where supported by your client library to reduce disruption for high-availability consumers.
* Monitor consumer lag and group rebalances via metrics (consumer\_lag, rebalance\_count) to detect frequent churn.
* Ensure consumers commit offsets appropriately (either automatically or explicitly) before and after rebalances to avoid reprocessing or data loss.
* Test consumer behavior under node failures and scaling events to understand rebalance impact on your workload.

Links and references

* [Kafka documentation](https://kafka.apache.org/)
* [KIP-429: Cooperative Rebalancing for Kafka Consumers](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%[SECRET_REDACTED])

Understanding consumer rebalancing — how partitions are reassigned, what triggers membership changes, and why consumption is paused — is essential for building resilient, scalable Kafka consumer applications and for efficient debugging at scale.

Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/0c31d3f3-91dd-4aed-93e8-328dc02f2226" />
</CardGroup>
