# kafka_producer_example.py
import random
import logging
from kafka import KafkaProducer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Example coffee shop data
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
        # Send message (key and value must be bytes)
        future = producer.send('multi-partition-topic', key=str(i).encode('utf-8'), value=message.encode('utf-8'))
        # Block until the message is sent (or an exception)
        record_metadata = future.get(timeout=10)
        logging.info(f"Message delivered to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}")
    except Exception as e:
        logging.error(f"Message delivery failed: {e}")

producer.flush()
producer.close()
logging.info("Finished sending messages")
```

Run the producer:

```bash theme={null}
python3 kafka_producer_example.py
```

You should see logs showing connections and message delivery, for example:

```text theme={null}
2025-04-13 02:58:42,749 - INFO - Message delivered to multi-partition-topic [0] at offset 0
2025-04-13 02:58:42,749 - INFO - Message delivered to multi-partition-topic [1] at offset 0
2025-04-13 02:58:42,750 - INFO - Message delivered to multi-partition-topic [2] at offset 0
2025-04-13 02:58:42,750 - INFO - Finished sending messages
```

You can also verify messages with a Kafka UI (if available) by opening the topic and inspecting messages per partition.

## 3) Write the Python consumer

Create `kafka_consumer.py` and add the following consumer code. This consumer subscribes to `multi-partition-topic`, reads from the earliest offset when there is no committed offset, and prints message contents with partition and offset metadata:

```python theme={null}
# kafka_consumer.py
from kafka import KafkaConsumer

# Kafka Consumer configuration
consumer = KafkaConsumer(
    'multi-partition-topic',
    bootstrap_servers='localhost:9092',
    group_id='partition-checker-group',  # consumer group id
    auto_offset_reset='earliest'         # start reading from the earliest available message
)

try:
    print("Listening for messages...")
    for message in consumer:
        # message.value is bytes, decode to string
        print(f"Message received: {message.value.decode('utf-8')}")
        print(f"Partition: {message.partition}, Offset: {message.offset}")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    consumer.close()
```

Key consumer settings explained:

| Setting             | Purpose                                                                 | Example                     |
| ------------------- | ----------------------------------------------------------------------- | --------------------------- |
| `topic`             | Topic(s) to subscribe to                                                | `'multi-partition-topic'`   |
| `bootstrap_servers` | Kafka broker addresses to connect to                                    | `'localhost:9092'`          |
| `group_id`          | Consumer group identifier; consumers in the same group share partitions | `'partition-checker-group'` |
| `auto_offset_reset` | Where to start when no committed offset exists                          | `'earliest'` or `'latest'`  |

Run the consumer:

```bash theme={null}
python3 kafka_consumer.py
```

Expected output (example):

```text theme={null}
Listening for messages...
Message received: Coffee Shop: Cappuccino Corner, Location: Uptown, Rating: 4.2
Partition: 2, Offset: 0
Message received: Coffee Shop: Latte Lounge, Location: Suburbs, Rating: 4.8
Partition: 0, Offset: 1
...
```

When you stop the consumer with Ctrl+C it exits cleanly and closes the connection.

<Callout icon="lightbulb">
  If you omit `group_id`, Kafka treats the consumer as a new, distinct consumer; it may receive duplicates or begin from offsets determined by `auto_offset_reset`. Both `bootstrap_servers` and `topic` are required.
</Callout>

## 4) Real-world considerations

The example prints messages to stdout for demonstration. In production you would typically:

* Parse the message payload (JSON, Avro, Protobuf, etc.)
* Apply business logic and transformations
* Persist results to a database or forward processed events to another topic
* Add robust error handling, retries, backoff, and dead-letter queues
* Instrument metrics and tracing for monitoring and debugging
* Gracefully handle shutdown signals and rebalances to avoid duplicate processing

Useful patterns and topics to research:

* Exactly-once vs at-least-once processing
* Partitioning and keys (how message keys affect partition assignment)
* Consumer rebalances and `max.poll.interval.ms`
* Offset committing strategies (automatic vs manual commits)

Links and References

* Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* kafka-python (PyPI): [https://pypi.org/project/kafka-python/](https://pypi.org/project/kafka-python/)
* Kafka consumer groups and partitioning: [https://kafka.apache.org/documentation/#consumerapi](https://kafka.apache.org/documentation/#consumerapi)
* Kubernetes for running consumers in production: [https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial)

Thanks for reading — that’s it for this lesson on building a Python Kafka consumer.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/cae2efcd-1cef-4c16-bb16-83d58c5e7f65" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/342607e9-5455-4822-b5c8-356aa25613a9" />
</CardGroup>


# Demo Kafka Producers

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Demo-Kafka-Producers/page

Demonstrates creating a multi-partition Kafka topic and producing messages with a Python kafka-python producer, showing partitioning, message delivery, and Kafdrop inspection.

Hello, and welcome back.

In this lesson we'll set up a Kafka producer and produce messages to a topic. The walkthrough uses a local Kafka broker, the `kafka-python` client, and the Kafdrop UI to inspect messages and partitions. Follow the steps in order to reproduce the demo in your lab environment.

We are in our lab environment, where Apache Kafka is already up and running.

<Frame>
  <img alt="The image shows a KodeKloud Kafka playground with a task description on the left and a terminal interface on the right displaying a KodeKloud ASCII logo." />
</Frame>

## Prerequisites

* Kafka broker running on `localhost:9092`
* Access to the Kafka installation directory (scripts live under `bin/`)
* Python 3 with `venv` support (we'll create an isolated virtual environment)
* `kafka-python` client library (installed into the venv)
* Optional: Kafdrop or another Kafka UI to inspect topics and messages

## 1) Inspect the Kafka CLI utilities

From the Kafka installation `bin` directory you can list the available CLI scripts. Example truncated output:

```bash theme={null}
root@kafka-host ~  ➜  cd /root/

total 160
-rwxr-xr-x 1 root root  1019 Sep 13  2022 zookeeper-shell.sh
-rwxr-xr-x 1 root root  1366 Sep 13  2022 zookeeper-server-stop.sh
-rwxr-xr-x 1 root root  1393 Sep 13  2022 zookeeper-server-start.sh
...
-rwxr-xr-x 1 root root  1068 Sep 13  2022 kafka-console-producer.sh
-rwxr-xr-x 1 root root   870 Sep 13  2022 kafka-configs.sh
-rwxr-xr-x 1 root root   893 Sep 13  2022 kafka-cluster.sh
...
```

You will use `kafka-topics.sh` to create and manage topics in the next step.

## 2) Create a topic with multiple partitions

Create a topic named `multi-partition-topic` with 3 partitions and a replication factor of 1:

```bash theme={null}
./kafka-topics.sh --create \
  --topic multi-partition-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

Tip: Once the topic is created, you can verify its configuration using `kafka-topics.sh --describe --topic multi-partition-topic --bootstrap-server localhost:9092` or inspect it visually with Kafdrop.

<Frame>
  <img alt="The image shows a Kafdrop web interface displaying a Kafka Cluster Overview, including details about bootstrap servers, topics, partitions, and brokers." />
</Frame>

## 3) Prepare a Python virtual environment and install the client

To avoid modifying the system Python, create and activate a virtual environment and install `kafka-python`:

Update package lists (example):

```bash theme={null}
sudo apt update
```

Create and activate the venv, then install the client:

```bash theme={null}
python3 -m venv kafka-env
source kafka-env/bin/activate
pip install kafka-python
```

Example pip output:

```text theme={null}
Collecting kafka-python
Downloading kafka_python-2.1.5-py2.py3-none-any.whl (285 kB)
Installing collected packages: kafka-python
Successfully installed kafka-python-2.1.5
```

## 4) Example Python producer script

Create `kafka-producer-example.py`. The script below:

* configures logging,
* creates a `KafkaProducer` connected to `localhost:9092`,
* composes sample "coffee shop" messages,
* sends 10 messages to `multi-partition-topic` with an explicit key (so partitioning is deterministic for identical keys),
* waits for each send to complete and flushes before exit.

```python theme={null}
import random
import logging
from kafka import KafkaProducer
