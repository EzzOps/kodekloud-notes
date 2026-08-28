# Stop and remove containers (if running)
docker rm -f kafka-cluster kafka-ui

# Remove the network if you want to clean up
docker network rm kafka-net
```

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/2359e80d-66f6-4080-8e9c-d81a6a1600fe/lesson/745d2f7b-c59f-441c-9203-554e09cb90b4" />
</CardGroup>


# Event Driven Architecture Basics

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Foundations-of-Event-Streaming/Event-Driven-Architecture-Basics/page

Introduction to event-driven architecture and how Apache Kafka provides durable, scalable, decoupled event streams enabling persistence, replay, fault tolerance, and independent consumer scaling.

Welcome back.

This lesson builds on the fundamentals of Apache Kafka and clarifies the event-driven architecture (EDA) problem we aim to solve. We'll revisit the basic event flow, examine common failure modes at scale, and explain how Kafka changes the architecture to provide durability, scalability, and decoupling.

Overview of a simple event flow

* System A emits an event. A producer can be a microservice, an IoT device, a mobile app, or any application component.
* System B consumes and processes that event, potentially producing output that System X will later consume.
* After processing, System B may acknowledge the event, notify System A, or persist the result.

This cycle—produce, consume, process, acknowledge—is straightforward at small scale. When System A emits n events concurrently, System B must process all n events without losing any and often must reply or persist the results. At scale, throughput, persistence, failure handling, and response coordination become challenging.

<Frame>
  <img alt="The image illustrates the basics of event-driven architecture, showing a flow of events and responses between System A, System B, and System X. Events are issued by System A and processed by System B, which interacts with System X, returning responses back to System A." />
</Frame>

Why this becomes hard at scale

* High concurrency increases load and exposes transient failures.
* Synchronous point-to-point integrations create tight coupling and deployment friction.
* Lack of durable storage for events can lead to data loss and inconsistent state.

Apache Kafka provides a durable, distributed event log that decouples producers and consumers, allowing each to scale and evolve independently. It changes the contract: once an event is durably written to Kafka, the producer's responsibility ends and consumers can process at their own pace.

<Frame>
  <img alt="The image illustrates the basics of event-driven architecture, showing how events from &#x22;System A&#x22; are sent to &#x22;System B&#x22; and how responses are managed, with connections to &#x22;System X&#x22; and a processed event indicator." />
</Frame>

Common pitfalls in event-driven architectures

| Pitfall                 | Impact                                                         | Example                                                                                                                   |
| ----------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Tight coupling          | Breaks independent deploys and increases blast radius          | An order service directly depends on a payment service API; a deployment in payment can break orders.                     |
| Reduced scalability     | Prevents effective horizontal scaling                          | Synchronous coordination limits the ability to scale consumers under spikes (e.g., social platforms during viral events). |
| Single point of failure | Causes cascading outages when a critical component fails       | A central dispatcher without redundancy brings down downstream pipelines.                                                 |
| No message persistence  | Lost messages lead to data inconsistency and lost transactions | Financial or logistics events lost without durable storage cause incorrect records.                                       |
| Limited feature set     | Missed opportunities for resilience and analytics              | Systems without replay, retention, or offset management cannot recover or run real-time analytics.                        |

<Frame>
  <img alt="The image outlines pitfalls of event-driven architecture, including tight coupling, reduced scalability, single points of failure, and no message persistence." />
</Frame>

The practical consequence: without durable persistence and replay, a logistics tracking system can lose status updates; a recommendation engine may stop serving users when its pipeline fails.

<Callout icon="lightbulb">
  Kafka addresses many of these pitfalls by providing a durable event log that decouples producers and consumers, supports high throughput, enables replay, and offers built-in fault tolerance and scalability.
</Callout>

How Kafka transforms the architecture

* Producers (System A) write events to Kafka topics and return immediately after the event is durably stored; producers do not need to manage downstream state.
* Multiple independent consumers (System B, System X, etc.) can read the same events at their own pace, maintain offsets, and reprocess when needed.
* Consumers scale independently; Kafka partitions and consumer groups enable parallel consumption without changing producers.
* Persistence, replication, and retention policies allow replay, auditing, and backfills for analytics and error recovery.

This decoupling simplifies deployments, reduces coordination overhead, and adds operational resilience.

<Frame>
  <img alt="The image depicts a diagram illustrating the role of Kafka as a message broker, connecting systems A, X, and B, resulting in a processed event." />
</Frame>

Kafka’s core strengths

| Strength                     | What it provides                                   | Why it matters                                                         |
| ---------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| High throughput              | Efficient write/read paths and sequential disk I/O | Handles large event volumes with low latency                           |
| Durability & fault tolerance | Replicated partitions across brokers               | Survives machine failures without data loss                            |
| Scalability                  | Partitioned topics and consumer groups             | Enables horizontal scaling of producers, brokers, and consumers        |
| Real-time processing         | Low-latency streaming with stream processors       | Supports real-time analytics, transformations, and stateful processing |

<Frame>
  <img alt="The image describes Kafka as the backbone of event-driven architectures, highlighting its features like high throughput, fault tolerance, scalability, and real-time processing capabilities." />
</Frame>

Design considerations and practical tips

* Model events as facts: use immutable, append-only events for reliable replay and auditability.
* Choose partition keys that balance throughput and ordering requirements.
* Tune retention and compaction policies based on recovery and storage needs.
* Use consumer groups to scale processing while preserving partition-level ordering when required.

<Callout icon="warning">
  Design choices (partitioning, retention, ordering guarantees) directly affect scalability and correctness. Test failure scenarios and recovery flows to ensure your pipeline meets SLAs.
</Callout>

Conclusion
With a durable event log like Kafka, systems can react to events as they occur, replay historical events when needed, and evolve independently without tight coupling. In the next lesson we'll dive into Kafka's core primitives—topics, partitions, producers, consumers, and consumer groups—and walk through concrete patterns for building resilient, scalable event-driven systems.

Links and references

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* [Event-Driven Architecture Overview (Martin Fowler)](https://martinfowler.[SECRET_REDACTED].html)
* [Kafka: The Definitive Guide (Confluent)](https://www.confluent.io/resources/kafka-the-definitive-guide/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/2359e80d-66f6-4080-8e9c-d81a6a1600fe/lesson/a869b71d-86de-4c60-be03-c1b48200e87c" />
</CardGroup>
