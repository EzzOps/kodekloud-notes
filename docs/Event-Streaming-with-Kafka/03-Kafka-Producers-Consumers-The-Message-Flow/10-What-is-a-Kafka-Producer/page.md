# What is a Kafka Producer

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/What-is-a-Kafka-Producer/page

Describes Kafka producers, message publishing and partitioning, essential configurations, tuning for reliability and throughput, plus a Java example and troubleshooting tips.

Hello and welcome back.

This lesson focuses on Kafka producers — the components that publish messages into Kafka topics. We’ll cover what producers do, how they distribute messages across partitions, the essential configuration needed to publish reliably, and a practical producer example you can adapt.

Overview

* Producers are applications that write data to Kafka topics.
* Consumers read data from Kafka topics.
* Producers are often the entry point for message flows: microservices, IoT devices, log emitters, streaming jobs, and batch processes.

Producer responsibilities and behavior

* A producer establishes a connection to one or more Kafka brokers and publishes records to a topic.
* Topics are partitioned. The producer determines which partition a record goes to using:
  * a provided record key (ensures ordering for that key), or
  * the producer’s partitioning strategy (e.g., round-robin, sticky partitioner, or a custom partitioner).
* Producers optimize for throughput and latency using buffering, batching, and compression. These behaviors are controlled by configuration parameters to balance durability and performance.

What a producer needs to publish messages
A producer needs the following minimum elements to produce messages to Kafka:

* `bootstrap.servers` — Broker addresses used to discover the Kafka cluster.
* Topic name — The target topic for messages.
* Serializers — Key and value serializers (e.g., `StringSerializer`, `ByteArraySerializer`, Avro/JSON serializers, or custom implementations).
* Additional producer configurations that affect reliability and performance.

Common producer configuration options

| Configuration key                     | Purpose                                                    | Typical values / notes                                   |
| ------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------- |
| `bootstrap.servers`                   | Addresses for initial broker discovery                     | `broker1:9092,broker2:9092`                              |
| `acks`                                | Durability/acknowledgement level                           | `0`, `1`, `all` (`-1` synonym)                           |
| `retries`                             | Number of retry attempts on transient failures             | `0` or positive integers                                 |
| `linger.ms`                           | Time to wait for additional records before sending a batch | milliseconds (e.g., `5`, `50`)                           |
| `batch.size`                          | Maximum batch size in bytes                                | e.g., `16384`                                            |
| `buffer.memory`                       | Total memory for buffering records                         | bytes (e.g., `33554432`)                                 |
| `compression.type`                    | Compression algorithm for payloads                         | `none`, `gzip`, `snappy`, `lz4`, `zstd`                  |
| `key.serializer` / `value.serializer` | Serializers for record key and value                       | `org.apache.kafka.common.serialization.StringSerializer` |
| `partitioner.class`                   | Custom partitioning implementation (optional)              | Fully-qualified class name                               |

The diagram below illustrates a producer sending messages to multiple brokers; each broker hosts partitions for one or more topics.

<Frame>
  <img alt="The image is a diagram illustrating how a Kafka producer sends messages to multiple brokers, each with specific topics and partitions." />
</Frame>

Practical example
Below is a minimal Java producer example showing essential properties and a basic send. Adapt serializers, error handling, and batching parameters to match your throughput and durability requirements.

```java theme={null}
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Properties;
import java.util.concurrent.Future;

Properties props = new Properties();
props.put("bootstrap.servers", "broker1:9092,broker2:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");           // durability
props.put("retries", 3);            // transient errors
props.put("linger.ms", 5);          // batch delay
props.put("batch.size", 16384);     // bytes

try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
    ProducerRecord<String, String> record =
        new ProducerRecord<>("my-topic", "key1", "Hello Kafka");
    Future<RecordMetadata> future = producer.send(record);
    RecordMetadata meta = future.get(); // synchronous wait (optional)
    System.out.println("Sent to partition " + meta.partition() + " with offset " + meta.offset());
}
```

Callouts and practical tips

<Callout icon="lightbulb">
  A complete producer example includes bootstrap configuration, serializers, and common tuning parameters such as `acks`, `retries`, `linger.ms`, and `batch.size`. For high throughput, prefer larger `batch.size`, `linger.ms`, and compression (e.g., `lz4` or `zstd`). For stronger durability, use `acks=all` and tune `retries` and `max.in.flight.requests.per.connection`.
</Callout>

Quick troubleshooting checklist

* Can the producer resolve and reach `bootstrap.servers`? Check DNS/firewall.
* Are serializers compatible with the consumer/registry (for Avro/Schema Registry setups)?
* Are the broker logs showing leader/ISR issues or partition unavailability?
* Are producer exceptions being logged (e.g., `TimeoutException`, `SerializationException`)?

Further reading and links

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* Producer configuration reference: [https://kafka.apache.org/documentation/#producerconfigs](https://kafka.apache.org/documentation/#producerconfigs)

That is it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/d556c0ab-fb04-44b1-8367-0d6103e48cf1" />
</CardGroup>
