# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Define some sample coffee shop data
coffee_shops = [
    {"name": "Espresso Bliss", "location": "Downtown", "rating": 4.5},
    {"name": "Cappuccino Corner", "location": "Uptown", "rating": 4.2},
    {"name": "Latte Lounge", "location": "Suburbs", "rating": 4.8},
    {"name": "Mocha Magic", "location": "City Center", "rating": 4.6},
    {"name": "Coffee Haven", "location": "East Side", "rating": 4.3},
]

# Generate and send 10 messages
for i in range(10):
    coffee_shop = random.choice(coffee_shops)
    message = f"Coffee Shop: {coffee_shop['name']}, Location: {coffee_shop['location']}, Rating: {coffee_shop['rating']}"

    try:
        future = producer.send(
            'multi-partition-topic',
            key=str(i).encode('utf-8'),
            value=message.encode('utf-8')
        )
        record_metadata = future.get(timeout=10)
        logging.info("Message delivered to %s [%d]", record_metadata.topic, record_metadata.partition)
    except Exception as e:
        logging.error("Message delivery failed: %s", e)

producer.flush()
logging.info("Finished sending messages")
```

> **lightbulb** Note: When you provide a message `key`, Kafka's partitioner uses it to determine the target partition. Messages with the same key are guaranteed to go to the same partition. Without a key, the producer distributes messages across partitions (modern producers may use sticky batching for throughput).

## 5) Run the producer and observe delivery

Run the script from the activated virtual environment:

```bash theme={null}
(kafka-env) root@kafka-host ~/kafka/bin ➜ python3 kafka-producer-example.py
```

Example logs:

```text theme={null}
2025-04-13 02:44:46,443 - INFO - <BrokerConnection client_id=bootstrap-0 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>
2025-04-13 02:44:46,451 - INFO - <BrokerConnection client_id=1 host=kafka-node:9092 <connected> [IPv4 ('192.2.52.10', 9092)]>
2025-04-13 02:44:46,606 - INFO - Message delivered to multi-partition-topic [2]
2025-04-13 02:44:46,610 - INFO - Message delivered to multi-partition-topic [0]
...
```

The logs indicate successful deliveries and the partition targets for each message.

<Frame>
  <img alt="The image shows a Kafdrop dashboard displaying details of a Kafka topic named &#x22;multi-partition-topic,&#x22; including an overview of partitions, replicas, and consumers." />
</Frame>

## 6) Verify messages in Kafdrop

Refresh the Kafdrop UI and inspect `multi-partition-topic`. The message count should reflect the number of messages you sent (10 in this demo). Click "View Messages" to inspect message contents.

<Frame>
  <img alt="The image shows a Kafdrop interface displaying topic messages from a Kafka topic named &#x22;multi-partition-topic,&#x22; detailing coffee shop information such as name, location, and rating." />
</Frame>

If you initially see messages for only one partition, use the partition selector in Kafdrop to view partitions 0, 1, and 2 individually. The messages will be distributed across partitions (e.g., 4/2/4 or another distribution depending on the keys and partitioner).

## Why partitions matter

* Partitions enable parallelism: multiple consumers in a consumer group can process partitions in parallel.
* Keys ensure ordering per key: records with the same key are written to the same partition and consumed in order.

## Quick reference — Common commands

| Task              | Command / Notes                                                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Create topic      | `./kafka-topics.sh --create --topic multi-partition-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1` |
| Describe topic    | `./kafka-topics.sh --describe --topic multi-partition-topic --bootstrap-server localhost:9092`                                     |
| Produce (console) | `./kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092`                                                   |
| Consume (console) | `./kafka-console-consumer.sh --topic my-topic --bootstrap-server localhost:9092 --from-beginning`                                  |
| Python client     | `pip install kafka-python` and use `KafkaProducer` / `KafkaConsumer`                                                               |

## References

* Kafdrop (UI): [https://github.com/obsidiandynamics/kafdrop](https://github.com/obsidiandynamics/kafdrop)
* kafka-python client: [https://pypi.org/project/kafka-python/](https://pypi.org/project/kafka-python/)
* Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)

That concludes this demo on producing messages to Kafka using a Python producer. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/f9b083a9-4e84-4b91-a66d-a039ca140cef)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/d0d556b9-bf7b-4e9c-8d60-c6327e1f5c2d)


# Producer Acknowledgments Acks and Reliability Guarantees

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Producer-Acknowledgments-Acks-and-Reliability-Guarantees/page

Explains Kafka producer acknowledgment settings and their impact on durability, latency, throughput, and configuration best practices for preventing data loss.

Hello and welcome back.

In this lesson we cover Kafka producer acknowledgments (acks) and how they relate to reliability guarantees. These producer settings determine when a producer considers a send successful — and therefore the trade-off between throughput/latency and data durability.

To make this concrete, imagine a producer sending messages to a topic with multiple partitions (for example, partition 0 and partition 1). The key question: when the producer sends a message, does it receive confirmation that Kafka has durably stored that message?

<Frame>
  <img alt="The image illustrates a Kafka message flow, showing how producers send messages to a broker and questioning the acknowledgment process back." />
</Frame>

Overview: Kafka producers can request acknowledgments at different levels using the `acks` setting. The chosen level affects latency, throughput, and the risk of data loss.

* acks=0\
  The producer does not wait for any acknowledgment from the broker. The send is fire-and-forget. This yields the highest throughput and lowest latency, but messages can be lost if the broker fails before persisting them.

* acks=1\
  The producer waits for an acknowledgment from the partition leader only. This guarantees the leader has accepted and appended the record to its local log, but it does not guarantee replication to followers. If the leader fails before followers replicate the message, data loss is possible.

* acks=all (equivalently `acks=-1`)\
  The producer waits until all in-sync replicas (ISRs) have acknowledged the write. This provides the strongest durability guarantee (assuming the ISR is correctly configured) but increases latency.

<Frame>
  <img alt="The image explains Kafka Producer acknowledgment settings for data writes, detailing the potential for data loss with different acknowledgment levels: &#x22;acks=0&#x22; (possible data loss), &#x22;acks=1&#x22; (limited data loss), and &#x22;acks=all&#x22; (no data loss)." />
</Frame>

Practical details

1. acks=1 (leader acknowledgment)

* Flow: producer sends the record to the partition leader → leader appends to its local log → leader returns acknowledgment to the producer.
* Implication: producer does not wait for followers to replicate; replication success is unknown to the producer.
* Risk: if the leader fails after acknowledging the write and before followers have replicated it, the record can be lost.

<Frame>
  <img alt="The image is a diagram illustrating producer acknowledgments and reliability guarantees in Kafka. It shows a producer sending a message to &#x22;Broker 1, Partition 01,&#x22; and receiving an acknowledgment after the data is stored." />
</Frame>

2. acks=all / `acks=-1` (all in-sync replicas)

* Flow: producer sends to leader → leader writes locally and waits until all in-sync replicas have persisted the record → producer receives acknowledgment only then.
* Implication: strong durability guarantee so long as your replication and ISR configuration are correct.
* Important knobs: replica count and `min.insync.replicas` — together they define how many brokers must have a copy before a write is considered successful.

<Frame>
  <img alt="The image illustrates a data flow diagram showing producer acknowledgments and reliability guarantees in a broker-based system with one main partition and multiple replicas, emphasizing limited data loss when &#x22;acks=all&#x22; is used." />
</Frame>

Configuration examples

* Java (Producer properties)

```properties theme={null}
bootstrap.servers=broker1:9092,broker2:9092
key.serializer=org.apache.kafka.common.serialization.StringSerializer
value.serializer=org.apache.kafka.common.serialization.StringSerializer
acks=all
```

* Console producer (shell)

```bash theme={null}
kafka-console-producer.sh --broker-list broker1:9092 --topic my-topic \
  --producer-property acks=all
```

* Confluent Python (confluent\_kafka)

```python theme={null}
from confluent_kafka import Producer
conf = {'bootstrap.servers': 'broker1:9092',
        'acks': 'all'}
p = Producer(conf)
```

Quick comparison table

| `acks` value | Latency | Throughput | Durability risk                                             | When to use                                                                                    |
| ------------ | ------- | ---------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `0`          | Lowest  | Highest    | High (message loss likely on broker failure)                | Best-effort high-throughput use cases where some loss is acceptable                            |
| `1`          | Low     | High       | Moderate (depends on leader stability)                      | Balanced cases where latency matters and some risk is acceptable                               |
| `all` / `-1` | Highest | Lower      | Lowest (strongest durability when ISR configured correctly) | Critical data where durability is required; combine with replication and `min.insync.replicas` |

Guidance and best practices

* Use `acks=0` when minimal latency and maximum throughput are primary, and occasional loss is acceptable (e.g., non-critical telemetry).
* Use `acks=1` for a compromise: good latency with reasonable durability, but accept the risk of leader-only writes.
* Use `acks=all` for the strongest durability. Also ensure:
  * You have an appropriate replication factor (≥ 3 is common for production).
  * `min.insync.replicas` is configured to prevent writes when too few replicas are available.

> **lightbulb** Choosing the right `acks` value is a trade-off: higher durability (e.g., `acks=all`) increases latency, while lower acknowledgment levels improve throughput but increase the risk of data loss. Tune `acks` together with replication settings and `min.insync.replicas` to meet your availability and durability requirements.

Summary

Kafka producer `acks` controls when the producer considers a send successful. Pick the value that aligns with your application's tolerance for latency and data loss, and always consider replication and broker-level settings to enforce the durability you need.

That covers producer acknowledgments and reliability guarantees in Kafka. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/6f9ace38-d976-4881-b1d6-edfd2290adc6)
