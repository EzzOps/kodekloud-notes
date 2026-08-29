# Serialization in Kafka

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Serialization-in-Kafka/page

Explains Kafka message serialization, common formats like JSON Avro Protobuf, configuring serializers and Schema Registry integration, and best practices for security, performance, and compatibility.

Hello and welcome back.

In this lesson/article we explain serialization in Kafka: what it is, why it matters, common formats, and how to configure serializers on the producer so messages are written and read correctly.

Why do we need serialization in Kafka?

Kafka persists and transfers messages as raw bytes. Any data your producer emits—JSON, a language object, Avro, Protobuf, etc.—must be converted into a byte\[] before being written to Kafka. For example, a JSON event:

```json theme={null}
{
  "user_id": 123,
  "event": "page_view"
}
```

contains keys (`user_id`, `event`) and values (`123`, `"page_view"`). The producer must serialize this logical structure into bytes so Kafka can store and transmit it reliably.

Common serialization formats

Several serialization formats are commonly used with Kafka, each with trade-offs between human-readability, performance, and schema support:

* JSON — human readable, easy to debug, good for simple or ad-hoc data exchange.
* [Apache Avro](https://avro.apache.org/) — compact binary format with explicit schemas, great for large-scale data pipelines and schema evolution.
* [Protocol Buffers (Protobuf)](https://developers.google.com/protocol-buffers) — compact binary format from Google, efficient with strong schema support.

<Frame>
  <img alt="The image is a comparison of serialization formats in Kafka: JSON, Apache Avro, and Protocol Buffers (Protobuf), highlighting their attributes and efficiency." />
</Frame>

Avro and Protobuf are compact binary formats and are commonly used in production because they enable schema validation, compatibility checks, and more efficient storage compared to plain JSON.

How serialization works in practice

Kafka producers use separate serializers for message keys and values. A serializer's job is to convert an in-memory key or value into a `byte[]` that Kafka can store and transmit. Choose the serializer that matches the data type you are sending and ensure the consumer uses a matching deserializer.

Common mappings (Java):

| Data           | Typical serializer (Java)                                         | When to use                                |
| -------------- | ----------------------------------------------------------------- | ------------------------------------------ |
| Integer key    | `org.apache.kafka.common.serialization.IntegerSerializer`         | Numeric partitioning keys                  |
| Long key       | `org.apache.kafka.common.serialization.LongSerializer`            | Time-based or large numeric IDs            |
| String value   | `org.apache.kafka.common.serialization.StringSerializer`          | Simple textual payloads or JSON strings    |
| Avro value     | `io.confluent.kafka.serializers.KafkaAvroSerializer`              | When using Avro with a Schema Registry     |
| Protobuf value | `io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer` | When using Protobuf with a Schema Registry |

Basic Java producer properties configuring key and value serializers:

```java theme={null}
// Java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.IntegerSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

KafkaProducer<Integer, String> producer = new KafkaProducer<>(props);
ProducerRecord<Integer, String> record = new ProducerRecord<>("topic-name", 123, "{\"user_id\":123,\"event\":\"page_view\"}");
producer.send(record);
producer.close();
```

Using Avro or Protobuf typically requires integrating with a Schema Registry. That integration appends a small schema identifier to each message so consumers can retrieve the schema and deserialize correctly, enabling controlled schema evolution (backward, forward, or full compatibility).

Example additional properties when using Confluent serializers with a Schema Registry:

```properties theme={null}
value.serializer=io.confluent.kafka.serializers.KafkaAvroSerializer
key.serializer=org.apache.kafka.common.serialization.StringSerializer
schema.registry.url=http://localhost:8081
```

<Frame>
  <img alt="The image illustrates the process of serialization in Kafka, converting a JSON object containing a user ID and event into binary formats using key and value serializers before sending to Kafka." />
</Frame>

Security and operational considerations

* Serialization is not encryption. For confidentiality use TLS for transport and encryption at rest (disk-level encryption, cloud storage encryption) plus Kafka ACLs for access control.
* A Schema Registry combined with Avro/Protobuf serializers improves governance: schemas are centrally stored, validated, and versioned.
* Producer CPU and latency can be affected by heavy serialization workloads (large Avro/Protobuf messages, intensive schema processing). Use batching, async sends, and properly sized producer instances.
* Ensure producers and consumers agree on the wire format (which serializer/deserializer pair is used). Mismatches lead to deserialization failures and runtime errors.

Best practices

* Choose a format that matches your needs: JSON for simplicity and debugging, Avro/Protobuf for efficiency and schema-driven pipelines.
* Use a Schema Registry for Avro/Protobuf to enable compatibility checks and governance.
* Configure `key.serializer` and `value.serializer` correctly on the producer and the corresponding deserializers on the consumer.
* Use compact binary formats (Avro/Protobuf) when storage efficiency and network performance matter.
* Combine serialization with Kafka security features (TLS, ACLs) and storage-level encryption for sensitive data.
* Monitor producer CPU and latency, and use batching and asynchronous sends to mitigate serialization overhead.

Next

Now that you understand why and how data is serialized in Kafka, a useful follow-up is understanding the role of message keys in Kafka and how they affect partitioning and ordering.

> **lightbulb** Kafka stores messages as bytes. Always ensure your producer configures the correct key and value serializers so both producers and consumers agree on the wire format.

References

* [Apache Avro](https://avro.apache.org/)
* [Protocol Buffers (Protobuf)](https://developers.google.com/protocol-buffers)
* [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
* [Kafka Documentation — Serializers and Deserializers](https://kafka.apache.org/documentation/#serializers)

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/e88b16cf-c86a-4eb3-918e-1381b22e08cc)
