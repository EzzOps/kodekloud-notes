# Kafka Partitions Scaling and Parallelizing Your Data Processing

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Building-Blocks-of-Kafka/Kafka-Partitions-Scaling-and-Parallelizing-Your-Data-Processing/page

Describes Kafka partitioning for distributing topic data across brokers to achieve parallelism, scalability, per key ordering, consumer group sizing, and trade offs when choosing partition counts

Welcome back. This lesson explains how Kafka achieves high availability and throughput through partitioning (with replication discussed in the next lesson). We'll use the charging-station example from the architecture to ground the concepts.

We have multiple charging stations that publish status messages to a topic named `charging_station_status`. Some of that topic's data may live on broker 1, which leads to key operational questions:

* What happens if that broker goes down?
* How do we scale consumption of this data?
* Can a single broker handle many concurrent consumers or large throughput?

A single broker handling all traffic becomes a bottleneck (CPU, memory, or disk I/O). Kafka solves this by partitioning topic data across brokers and replicating partitions for fault tolerance. First, let’s focus on partitioning.

Why partitioning matters

* Distribution: Partitions spread a topic’s data across brokers, preventing any single broker from becoming a throughput or availability bottleneck.
* Parallelism: Each partition can be read independently; multiple consumers can process different partitions concurrently.
* Scalability: Partitions allow load to be distributed as data and consumer demand grow.
* Fault tolerance: When combined with replication, partitions ensure data remains available if a broker fails.
* Ordering: Kafka guarantees ordering only within a partition; messages with the same key remain ordered.

Below is an updated architecture showing a Kafka cluster (3 brokers) and a `charging_station_status` topic split into three partitions. Messages include keys (e.g., `stationA`, `stationB`) which influence partition assignment.

<Frame>
  <img alt="The image explains the high availability of Kafka using replication and partitions, highlighting distribution, parallelism, scalability, and fault tolerance. Each concept describes how partitioning enhances Kafka's performance and reliability." />
</Frame>

Partitioning details

Partition key

* You can provide a partition key when producing messages to control distribution. Using a `user_id` or `station_id` ensures all events for that entity land in the same partition, preserving order for that entity.
* Keys keep related data together (data locality), simplifying stateful processing and reducing cross-partition coordination.

Example producer snippet (shows how a key is provided):

```js theme={null}
producer.send({
  topic: 'charging_station_status',
  messages: [
    { key: 'stationA', value: '{"status":"charging","level":80}' },
    { key: 'stationB', value: '{"status":"idle","level":100}' }
  ]
});
```

Partitioning trade-offs

|                    Concern | Benefit / Risk                                          | Guidance                                                             |
| -------------------------: | :------------------------------------------------------ | :------------------------------------------------------------------- |
| Distribution & parallelism | Spreads load, enables concurrent consumers              | Use multiple partitions to match throughput and consumer concurrency |
|          Over-partitioning | Increased metadata, coordination cost, and memory usage | Avoid extremely high partition counts without need                   |
|         Under-partitioning | Limited parallelism, potential bottlenecks              | Increase partitions to match throughput needs and consumer capacity  |
|                   Ordering | Ordering is guaranteed per partition only               | Use consistent keys for entities that need strict ordering           |

Over-partitioning vs under-partitioning

* Over-partitioning: Too many partitions lead to higher coordinator overhead, larger replication metadata, and more memory required on brokers and clients.
* Under-partitioning: Too few partitions limit concurrency; consumers can’t parallelize work effectively, creating throughput bottlenecks.
* Choose a partition count based on expected throughput, number of consumers, and operational limits. Start with a reasonable number and monitor metrics (throughput, latency, consumer lag) to adjust.

Data locality

* Select partition keys so related records remain in one partition (e.g., all events for a station or user).
* Proper keys reduce cross-partition joins and simplify stateful stream processing.

Consumer group sizing

* Each partition is consumed by at most one consumer instance in a consumer group.
* If there are more partitions than consumers, some consumers will handle multiple partitions.
* If there are more consumers than partitions, some consumers will be idle.

Example mapping:

| Partitions | Consumers | Result                                                                     |
| ---------: | :-------: | :------------------------------------------------------------------------- |
|          3 |     1     | Single consumer handles all 3 partitions (no parallelism across consumers) |
|          3 |     2     | Two consumers share the 3 partitions (one consumer gets 2 partitions)      |
|          3 |     3     | Optimal utilization: 1 consumer per partition                              |
|          3 |     4     | One consumer will be idle (more consumers than partitions)                 |

Match consumer group size to the partition count to maximize utilization and throughput.

<Frame>
  <img alt="The image illustrates the high availability of Kafka using replication and partitions, showing multiple stations feeding data into partitions across different brokers." />
</Frame>

Best practices summary

* Choose keys that keep related events together to preserve ordering and simplify processing.
* Start with a conservative number of partitions based on expected throughput, then scale partitions as needed (note: increasing partitions later can affect ordering semantics).
* Align consumer group size with partition count to avoid idle consumers or underutilized partitions.
* Monitor broker and client metrics (CPU, memory, disk I/O, consumer lag) and tune partition counts accordingly.

> **lightbulb** Match the number of partitions to your expected concurrency and throughput. Too many partitions increase operational overhead; too few limit parallelism.

Fault tolerance recap

* Partitioning spreads data across brokers. With replication (covered in the next lesson), Kafka ensures partitions are duplicated on multiple brokers so the topic remains available if a broker fails.

<Frame>
  <img alt="The image illustrates key considerations for achieving high availability in Kafka using replication and partitions, including partition key selection, over-partitioning, under-partitioning, data locality, and consumer group size." />
</Frame>

Further reading and references

* Apache Kafka documentation — Partitioning: [https://kafka.apache.org/intro](https://kafka.apache.org/intro)
* Kafka consumer groups and partition assignment: [https://kafka.apache.org/documentation](https://kafka.apache.org/documentation)
* Designing partition keys and capacity planning (blogs & best practices): refer to your platform’s Kafka guides and operational runbooks

That’s it for this lesson. Next, we’ll cover replication and how Kafka ensures high availability when brokers fail. See you next time.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/ee6ed9ab-202a-4dfc-bcd5-8a6941e1440b/lesson/cbbcc696-8cb7-4711-a7d2-87d744a0867b)
