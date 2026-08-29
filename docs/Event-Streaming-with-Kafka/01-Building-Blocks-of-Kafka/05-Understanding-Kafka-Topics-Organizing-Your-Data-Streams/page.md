# Strong durability: write acknowledged when all in-sync replicas have the record
acks=all
# Optional: wait for leader to fully commit to disk
# linger.ms and batch.size tune throughput/latency tradeoffs
```

Failure scenarios:

* If broker 3 (a follower) goes down, the cluster loses one replica but still has leader + another follower. Producers and consumers continue normally; the controller can later replicate data to restore the desired replica count.
* If broker 1 (the leader for partition 1) fails, Kafka elects a new leader from the in-sync replicas (for example, broker 2) so producers and consumers resume interaction with the new leader. Leader election is automatic (subject to cluster configuration), minimizing downtime.

<Callout icon="lightbulb">
  In Kafka, each partition has one leader and one or more follower replicas. Producers and consumers interact with the leader. Followers replicate the leader’s log and can be promoted to leader if the current leader fails. The replication factor controls how many copies of each partition exist.
</Callout>

Operational notes and tuning tips:

* Replication factor: Set to at least 2; 3 is typical to withstand one broker plus maintenance operations. Higher values increase durability but use more storage.
* ISR (in-sync replica) management: Only replicas sufficiently up-to-date are eligible for leader election. Monitor ISR sizes and set appropriate `min.insync.replicas` if you need stronger durability guarantees.
* Producer acknowledgements:
  * `acks=0`: Very low latency, no durability guarantee.
  * `acks=1`: Leader acknowledged; risk if leader fails before replication.
  * `acks=all`: Waits for all in-sync replicas — strongest durability, higher latency.
* Monitoring: Track replica lag, ISR changes, and controller health to detect and mitigate replication issues early.
* Rebalancing & reassignment: Use automated tools or `kafka-reassign-partitions.sh` to restore replication factor after failures or to rebalance replicas across brokers.

Replication summary

* Partitioning provides parallelism and distributes data across brokers.
* Replication keeps copies of partitions across brokers for durability, fault tolerance, and high availability.
* Together, partitioning and replication make Kafka resilient and suitable for production-grade event streaming.

Further reading and references:

* Apache Kafka Documentation — Replication: [https://kafka.apache.org/documentation/#replication](https://kafka.apache.org/documentation/#replication)
* Kafka Producer Configuration — acks: [https://kafka.apache.org/documentation/#producerconfigs\_acks](https://kafka.apache.org/documentation/#producerconfigs_acks)
* Kafka Topic Management — kafka-topics CLI: [https://kafka.apache.org/documentation/#basic\_ops](https://kafka.apache.org/documentation/#basic_ops)

That’s it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/ee6ed9ab-202a-4dfc-bcd5-8a6941e1440b/lesson/5047c311-c819-4910-9c6d-a6e404b0795a" />
</CardGroup>


# Understanding Kafka Topics Organizing Your Data Streams

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Building-Blocks-of-Kafka/Understanding-Kafka-Topics-Organizing-Your-Data-Streams/page

Explains Kafka topics and features for organizing event streams, covering categorization, append only logs, retention, multi consumer access, decoupling, partitioning, and replication.

Hello and welcome back.

In the previous lesson we learned about Kafka brokers and how they store incoming events inside a Kafka cluster. In this lesson we'll focus on organizing the data that producers send into Kafka so consumers can discover and process the streams they need.

Revisiting the previous example: brokers hold all events produced by our producers, but we still need a way to categorize those events so consumers can find the exact data they want. The logical container producers publish into is called a topic.

Examples:

* The EV charging station sends its events to a topic named `EV_charging_topic`.
* Charging station metrics are published to a topic named `station_metrics_topic`.

A topic is a named stream that groups related messages. Unlike brokers — which are physical servers — topics are logical constructs built on top of brokers. When you create a Kafka cluster you provision brokers first, then create topics. Together, brokers and topics are the fundamental building blocks for producing and consuming events in Kafka.

What is a topic?

* A topic groups related messages logically. Think of each topic as a named stream for a particular type of data (device events, logs, user actions, metrics).
* You can create many topics to organize data streams; Kafka itself doesn't impose a strict upper limit, but practical constraints arise from cluster resources and metadata overhead. Tens of thousands of topics may require broker tuning.

Key features of Kafka topics

1. Message categorization

* Topics let you group similar messages so consumers subscribe only to needed data streams.
* Proper topic design improves discoverability and simplifies downstream processing, analytics, and monitoring.

2. Immutable, append-only logs

* Messages in a topic are written to an append-only log. Once a record is written it cannot be modified.
* This sequential, append-only storage preserves order within a partition (partitions are covered in the next lesson) and is important for use cases such as event sourcing and financial transactions.
* Retention controls how long records are kept (for example, `7d` or up to a certain size like `1GB`). When retention thresholds are reached, older data is removed according to your configured policy.

<Callout icon="lightbulb">
  Align retention settings with your application’s processing guarantees. If retention is too short, consumers might miss messages before they process them. If too long, you may incur unnecessary storage costs.
</Callout>

3. Multi-consumer access

* Multiple consumers (organized as consumer groups) can read from the same topic independently. Each consumer group maintains its own offsets (read positions), so different applications can consume the same data without interfering with one another.
* This enables parallel analytics, monitoring, and real-time processing from a single event stream.

4. Decoupled communication

* Producers write to topics and consumers read from topics. Producers and consumers are decoupled and do not need to be aware of each other or be online simultaneously.
* This decoupling supports scalable, asynchronous architectures where producers and consumers evolve independently.

5. Replication (high availability)

* Topics (more precisely, topic partitions) are replicated across multiple brokers to provide fault tolerance and data availability.
* Replication ensures that if one broker fails, another broker holding a replica can continue to serve the data.
* We will cover replication details and leader/follower behavior in a later lesson.

Comparison at a glance

|       Resource | Purpose                                                            | Example                                                  |
| -------------: | ------------------------------------------------------------------ | -------------------------------------------------------- |
|         Broker | Physical server that stores partitions and coordinates replication | Broker nodes in your Kafka cluster                       |
|          Topic | Logical stream grouping related messages                           | `EV_charging_topic`, `station_metrics_topic`             |
|      Partition | Unit of parallelism within a topic — preserves order per partition | Topic partitioning for throughput and parallel consumers |
| Consumer Group | Set of consumers that coordinate to consume a topic                | Analytics service group, monitoring service group        |

Why topic design matters (short checklist)

* Keep related data together so consumers can subscribe to meaningful streams.
* Consider retention: balance consumer needs vs storage costs.
* Plan partitioning (next lesson) for throughput and ordering guarantees.
* Use replication to protect against broker failures.

<Frame>
  <img alt="The image is an infographic about Kafka topics and their role in organizing data streams. It highlights five features: message categorization, immutable log, multi-consumer access, decoupled communication, and replication." />
</Frame>

Those five aspects—categorization, immutability, multi-consumer access, decoupling, and replication—make Kafka topics the backbone of reliable real-time data streams. Topics provide structure and reliability for building event-driven architectures.

Next lesson
To understand how Kafka distributes and scales your data, we'll dive into partitions and how they enable parallelism, ordering guarantees, and higher throughput. See you in the next lesson.

Links and references

* Apache Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Kafka Concepts — Topics and Partitions: [https://kafka.apache.org/documentation/#basic\_concepts](https://kafka.apache.org/documentation/#basic_concepts)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/ee6ed9ab-202a-4dfc-bcd5-8a6941e1440b/lesson/4e203abd-9e43-4c10-b39e-51d66af8a1cf" />
</CardGroup>
