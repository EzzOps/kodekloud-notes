# Create and activate the virtual environment
python3 -m venv kafka-demo-env
source kafka-demo-env/bin/activate

# Install kafka-python
pip install kafka-python
```

Expected installation output (truncated):

```bash theme={null}
Collecting kafka-python
Downloading kafka_python-2.2.4-py2.py3-none-any.whl (308 kB)
Installing collected packages: kafka-python
Successfully installed kafka-python-2.2.4
```

> **lightbulb** A Python virtual environment keeps demo packages isolated from system Python packages. Activate the virtual environment (`source kafka-demo-env/bin/activate`) in every terminal you use for this demo.

***

## 3) Create the producer: producer.py

Create `producer.py` and paste the following code. This producer sends 1000 messages and cycles keys through four values so they map across the 4 partitions. Serializers handle `None` safely.

```python theme={null}
# producer.py
from kafka import KafkaProducer
import time
import random

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    key_serializer=lambda k: k.encode('utf-8') if k is not None else None,
    value_serializer=lambda v: v.encode('utf-8')
)

topic = 'consumer-rebalancing-demo'

# Send 1000 messages to the topic
for i in range(1000):
    # Use a key that maps across 4 partitions (key distribution)
    key = f"key-{i % 4}"   # keys: key-0, key-1, key-2, key-3
    value = f"Message-{i}"
    producer.send(topic, key=key, value=value)
    print(f"Produced: {value} with key: {key}")
    time.sleep(0.5)  # Slow down message production for demo purposes

producer.close()
```

Run the producer:

```bash theme={null}
python3 producer.py
```

You should see output like:

```plaintext theme={null}
Produced: Message-0 with key: key-0
Produced: Message-1 with key: key-1
Produced: Message-2 with key: key-2
Produced: Message-3 with key: key-3
Produced: Message-4 with key: key-0
...
```

Because Kafka partitions messages deterministically based on the key (via the default partitioner), messages with the same key always go to the same partition. With keys cycling `key-0`..`key-3` and 4 partitions, the messages will spread across partitions 0–3.

***

## 4) Create the consumer: consumer.py

Create `consumer.py` and paste the following script. It accepts an optional command-line argument for the consumer group id; if none is provided it uses `default-group`.

```python theme={null}
# consumer.py
from kafka import KafkaConsumer
import sys

def consume_messages(group_id):
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        'consumer-rebalancing-demo',
        bootstrap_servers=['localhost:9092'],
        group_id=group_id,
        auto_offset_reset='earliest',
        key_deserializer=lambda k: k.decode('utf-8') if k is not None else None,
        value_deserializer=lambda v: v.decode('utf-8') if v is not None else None
    )

    print(f"Consumer {group_id} is starting...")
    try:
        for message in consumer:
            print(
                f"Consumer {group_id} received: {message.value} "
                f"from partition {message.partition}, key: {message.key}"
            )
    except KeyboardInterrupt:
        print(f"Consumer {group_id} is stopping...")
    finally:
        consumer.close()

if __name__ == "__main__":
    group_id = sys.argv[1] if len(sys.argv) > 1 else "default-group"
    consume_messages(group_id)
```

Notes:

* `auto_offset_reset='earliest'` ensures consumers without committed offsets will read from the beginning of the topic.
* Kafka automatically creates consumer groups when a consumer first joins using the provided `group_id`. You do not need to pre-create the group.

***

## 5) Run consumers and observe rebalancing

Start one consumer in group `consumer-group-1`:

Terminal 1

```bash theme={null}
source kafka-demo-env/bin/activate
python3 consumer.py consumer-group-1
```

Example output (single consumer consuming from all partitions over time):

```plaintext theme={null}
Consumer consumer-group-1 is starting...
Consumer consumer-group-1 received: Message-0 from partition 0, key: key-0
Consumer consumer-group-1 received: Message-1 from partition 1, key: key-1
Consumer consumer-group-1 received: Message-2 from partition 2, key: key-2
Consumer consumer-group-1 received: Message-3 from partition 3, key: key-3
...
```

With one consumer in the group, that consumer will be assigned all partitions (0, 1, 2, 3).

Now open a second terminal and start another consumer joining the same group:

Terminal 2

```bash theme={null}
source kafka-demo-env/bin/activate
python3 consumer.py consumer-group-1
```

When the second consumer joins, Kafka triggers a group rebalance and redistributes partitions across group members. With 4 partitions and 2 consumers, a typical assignment is that each consumer receives two partitions (e.g., consumer A → partitions 0 & 1; consumer B → partitions 2 & 3). You will start seeing partition-specific messages in each terminal.

Example after rebalance:

Terminal A:

```plaintext theme={null}
Consumer consumer-group-1 received: Message-100 from partition 0, key: key-0
Consumer consumer-group-1 received: Message-101 from partition 1, key: key-1
...
```

Terminal B:

```plaintext theme={null}
Consumer consumer-group-1 received: Message-102 from partition 2, key: key-2
Consumer consumer-group-1 received: Message-103 from partition 3, key: key-3
...
```

If you start two more consumers (total 4 consumers in the same group), Kafka will rebalance again so each consumer receives one partition (1-to-1), enabling maximum parallelism:

* Consumer 1 → partition 0
* Consumer 2 → partition 1
* Consumer 3 → partition 2
* Consumer 4 → partition 3

Stopping a consumer — rebalance on leave

* If you stop one consumer (Ctrl+C), Kafka removes it from the group and immediately triggers another rebalance.
* The partitions previously owned by the stopped consumer will be reassigned to the remaining group members, who will begin receiving messages for those partitions.

This dynamic reassignment ensures each partition is consumed by exactly one consumer within a group at any time and is the core behavior behind Kafka consumer group rebalancing.

> **lightbulb** Consumer groups enable horizontal scaling of message consumption. The maximum number of active consumers that can consume in parallel in a group is bounded by the number of partitions. With N partitions, up to N consumers in the same group can be actively assigned partitions; additional consumers will remain idle until partitions are freed.

***

## Summary

* Created a topic with 4 partitions.
* Produced keyed messages so they map deterministically to partitions.
* Launched multiple consumers in the same group and observed Kafka rebalancing partition assignments as consumers joined or left.
* With K partitions, up to K consumers can be actively assigned partitions; Kafka automatically rebalances when group membership changes.

That concludes this practical demo of Kafka consumer rebalancing.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/0d89579f-2c52-479e-996a-a7f4bc04f18f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/25a81d98-c284-444b-b64d-6141e562d17d/lesson/b31671b6-8301-4bd1-917f-a70a393b937f)


# Demo Kafka Consumers

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Demo-Kafka-Consumers/page

Guide to creating Kafka topics and writing Python producers and consumers with kafka-python, covering setup, message production, consumption, partitions, offsets, and production considerations

Welcome back. In this lesson you'll learn how to write a Kafka consumer in Python. We'll cover:

* Creating a topic with multiple partitions
* Producing messages with a Python producer (`kafka-python`)
* Implementing a simple Python consumer that reads and prints messages
* Real-world considerations for running consumers in production

Prerequisites

* A running Kafka broker reachable at `localhost:9092`
* Kafka command-line tools available (usually in `~/kafka/bin` or `/opt/kafka/bin`)
* Python 3 installed
* Basic familiarity with Kafka topics, partitions, and consumer groups

## 1) Create the topic

To consume messages you first need a topic and some messages in it. If you run the topic creation command from the wrong working directory, you may see an error like:

```bash theme={null}
root@kafka_host ~  ./kafka-topics.sh --create --topic multi-partition-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
-bash: ./kafka-topics.sh: No such file or directory
```

This indicates the `kafka-topics.sh` script is not found in the current folder. Kafka CLI tools live in the Kafka installation `bin` directory (for example `~/kafka/bin` or `/opt/kafka/bin`). Change to that directory and run the command again:

```bash theme={null}
cd ~/kafka/bin
./kafka-topics.sh --create --topic multi-partition-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

Expected successful output:

```bash theme={null}
Created topic multi-partition-topic.
```

> **lightbulb** If you are unsure where Kafka is installed, consult environment documentation or search for `kafka-topics.sh` with `find / -name kafka-topics.sh 2>/dev/null`.

## 2) Produce messages to the topic (Python producer)

Install a Python virtual environment and the Kafka client library `kafka-python`:

```bash theme={null}
sudo apt update
sudo apt install -y python3-venv        # if not already installed
python3 -m venv kafka-env
source kafka-env/bin/activate
pip install kafka-python
```

Create a producer script (e.g., `kafka_producer_example.py`) with the following content:

```python theme={null}
