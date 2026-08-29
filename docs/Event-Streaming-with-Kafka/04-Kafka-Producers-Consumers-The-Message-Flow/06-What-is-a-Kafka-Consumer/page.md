# What is a Kafka Consumer

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/What-is-a-Kafka-Consumer/page

Explains Kafka consumers how they read and process topic partitions, ordering guarantees, partition independence, replay and offset management, and the pull-based consumption model.

Hello, and welcome back.

In this lesson we'll explain what consumers are in Apache Kafka, how they interact with topics and partitions, and the guarantees Kafka provides for reading and processing events.

Producers send events into Kafka. Once events are in Kafka, consumers are the applications that read (consume) and process those events. A consumer typically:

* Reads events from one or more topic partitions.
* Processes each event (for example, updating a UI, writing results to a database, invoking downstream services, or making a decision).
* Optionally commits its progress (offsets) so it can resume processing later.

Example: An EV charging station sends an "arrival" event to Kafka when a vehicle plugs in. A consumer subscribed to that topic receives the event and updates a mobile app to mark the station as occupied, reducing the available-station count.

Producers can write events to Kafka even when no consumers are currently subscribed; Kafka will retain those events according to broker-side retention policies. Kafka is not intended as a primary long-term database—event value often decays with time (e.g., a stock quote from an hour ago is less useful for real-time trading but may still be valuable for historical analysis).

A consumer connects to Kafka using broker connection information and topic details, then reads from the topic’s partitions.

<Frame>
  <img alt="The image shows a Kafka consumer architecture with brokers handling different partitions of Topic A, each connecting to separate consumers." />
</Frame>

> **lightbulb** Consumers read and process messages but do not remove them from Kafka. Message retention and deletion are controlled by broker-side settings such as retention time, size-based retention, and compaction.

Key characteristics of Kafka consumers

1. Sequential access

* Each partition is an ordered, immutable sequence of records identified by offsets.
* A consumer reads records in increasing offset order from a configured or committed position, guaranteeing per-partition ordering (equivalent to reading a log from start to end).

2. Partition independence

* Ordering is only guaranteed inside a single partition; Kafka does not provide global ordering across partitions of the same topic.
* Each partition acts as an independent ordered log. Consumers can read multiple partitions concurrently, but cross-partition message order is not guaranteed.

3. Historical control

* Consumers commonly read new messages as they arrive. For consumer groups without a prior committed offset, `auto.offset.reset` controls whether they start at the `earliest` or `latest` offset.
* Consumers can intentionally read older offsets (replay) as long as the data is still retained by brokers.
* Consumers manage and commit offsets to checkpoint processing progress and support reprocessing when needed.

Summary table

| Characteristic         |                                 What it means | Why it matters                                                                             |
| ---------------------- | --------------------------------------------: | ------------------------------------------------------------------------------------------ |
| Sequential access      | Messages in a partition are ordered by offset | Guarantees per-partition ordering for deterministic processing                             |
| Partition independence |      Ordering is not global across partitions | Enables parallelism and scaling but requires design for cross-partition ordering if needed |
| Historical control     |     Consumers can read older offsets (replay) | Supports reprocessing, debugging, and backfills when data retention allows                 |

<Frame>
  <img alt="The image describes three features of a Kafka Consumer: Sequential Access, Partition Independence, and Historical Control, with brief explanations for each." />
</Frame>

Kafka uses a pull-based consumption model

* Consumers request records from brokers (Kafka does not push records to consumers).
* Because consumers initiate reads, they control consumption rate and can apply backpressure by adjusting poll frequency or processing concurrency.
* Consumers manage offsets (their current read position) and typically commit offsets to Kafka or an external store to checkpoint progress and enable fault recovery.

These properties—ordered reads per partition, partition independence, historical access, and a pull-based model—define how applications reliably and scalably consume streaming data from Kafka.

Next steps

* In the next lesson we'll set up a Kafka consumer and demonstrate consuming messages from a topic.
* For implementation details and client libraries, consult the official documentation and client-specific guides linked below.

Links and References

* [Kafka: Consumers — Apache Kafka Documentation](https://kafka.apache.org/documentation/#consumer)
* [Kafka Retention Policies and Log Compaction](https://kafka.apache.org/documentation/#design_logretention)
* [Kafka Consumer Groups and Offsets](https://kafka.apache.org/documentation/#consumerconfigs)

That is it for this lesson. Speak with you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/6a37c911-e3fd-48eb-a45a-4f2cb15556c1)
