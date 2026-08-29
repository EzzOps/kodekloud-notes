# Producer: sending order event to Kafka
order_event = {
    'customer_name': name,
    'delivery_address': address,
    'products': cart,
    'total_amount': sum(item['price'] for item in cart)
}

event_string = json.dumps(order_event)
logger.info(f"Sending order event to Kafka: {event_string}")

producer.produce(
    topic='cartevnt',
    value=event_string
)
```

> **lightbulb** Producer delivery is asynchronous by default. To ensure delivery before shutdown, either call `producer.flush()` on shutdown or supply a delivery callback to confirm the message reached the broker.

Example terminal output from the front-end when placing an order:

```text theme={null}
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /add_to_cart/1 HTTP/1.1" 302 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /static/styles/toy1.jpg HTTP/1.1" 304 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /static/images/toy3.jpg HTTP/1.1" 304 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /static/images/toy2.jpg HTTP/1.1" 304 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /static/images/toy6.jpg HTTP/1.1" 304 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /static/images/toy1.jpg HTTP/1.1" 304 -
127.0.0.1 - - [20/Apr/2025 10:30:31] "GET /cart HTTP/1.1" 304 -
127.0.0.1 - - [20/Apr/2025 10:30:34] "POST /place_order HTTP/1.1" 200 -
```

## Configure the backend consumer to connect to your Kafka broker

Open the warehouse UI app (folder: `final-projects/warehouse`, file: `app.py`) and locate the Consumer import from `confluent_kafka`. The consumer configuration needs the broker address in `bootstrap.servers`. Replace the placeholder with the public IP (and port) of the EC2 instance running Kafka.

<Frame>
  <img alt="The image shows the AWS EC2 dashboard with a running instance named &#x22;kafka-server.&#x22; Details such as the instance ID, state, type, and public IPV4 address are displayed." />
</Frame>

> **lightbulb** Replace `bootstrap.servers` with the EC2 instance’s public IP and Kafka port (for example `54.234.163.236:9092`). This allows the consumer running locally (or from another host) to connect to the Kafka broker.

### Consumer configuration notes

Below are the important consumer settings used by the warehouse dashboard and why they matter:

| Config key           | Purpose                                                                                                                               | Example / Advice          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `bootstrap.servers`  | Broker address to connect to (host:port).                                                                                             | `54.234.163.236:9092`     |
| `group.id`           | Consumer group name. Use a stable ID in production; a unique one (e.g., appending a UUID) can be used for independent read-only runs. | `warehouse_reader_<uuid>` |
| `auto.offset.reset`  | Where to start when no committed offset exists.                                                                                       | `earliest`                |
| `enable.auto.commit` | Whether offsets are auto-committed. We disable this to control processing.                                                            | `False`                   |

> **warning** If you generate a new unique `group.id` on every run and do not commit offsets, the consumer will re-read messages from the earliest offset each time. For normal operation, use a stable `group.id` and commit offsets to avoid duplicate processing.

## Consumer implementation used by the warehouse UI

This implementation polls Kafka for available messages, decodes JSON payloads, skips tombstone messages (value is `None`), and returns a list of parsed order dictionaries for rendering in the UI.

```python theme={null}
import json
import uuid
import logging
from confluent_kafka import Consumer

logger = logging.getLogger(__name__)
KAFKA_TOPIC = 'cartevnt'

def get_kafka_messages():
    """Get all available messages from Kafka and return as a list of dicts."""
    messages = []

    # Consumer configuration - replace bootstrap.servers with your broker IP:port
    consumer_config = {
        'bootstrap.servers': '54.234.163.236:9092',
        'group.id': 'warehouse_reader_' + str(uuid.uuid4()),
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    }

    consumer = Consumer(consumer_config)
    logger.info("Created new Kafka consumer")

    try:
        consumer.subscribe([KAFKA_TOPIC])
        logger.info(f"Subscribed to topic: {KAFKA_TOPIC}")

        # Poll for messages with a timeout; adjust tries/timeouts as required
        for _ in range(10):  # try a few times to collect available messages
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                logger.error(f'Error consuming message: {msg.error()}')
                continue

            # Skip tombstone messages where value is None
            raw_val = msg.value()
            if raw_val is None:
                logger.info("Skipped tombstone or message with no value")
                continue

            try:
                # Ensure we have a string before loading JSON
                if isinstance(raw_val, (bytes, bytearray)):
                    raw_val = raw_val.decode('utf-8')
                value = json.loads(raw_val)
                logger.info(f'Reading message for customer: {value.get("customer_name")}')
                messages.append(value)
            except json.JSONDecodeError as e:
                logger.error(f'Failed to parse message: {e}')
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")

    return messages
```

How the UI uses this function:

* The dashboard calls `get_kafka_messages()` when the packer clicks "Refresh Dashboard".
* Each returned dict should contain `customer_name`, `delivery_address`, `products`, and `total_amount`.
* The frontend renders those fields in an actionable format for packers (items, prices, totals, address).

## Running the warehouse UI locally

1. Open a terminal in the `final-projects/warehouse` folder.
2. Start the app:
   * `python3 app.py`
3. Open the dashboard in your browser (or use the editor’s "Open in Browser").

## Test the end-to-end flow

1. Place an order in the shop front-end (e.g., add toy 6, view cart, enter customer name "Rose" and address "Delhi", then click Place Order). This produces an event to the `cartevnt` topic.
2. In the warehouse dashboard, click **Refresh Dashboard**. The backend consumer will poll Kafka, parse the event, and render it.

The dashboard displays orders in a packer-friendly way (product list, prices, totals, customer, address). You can extend the dashboard to:

* Auto-refresh on a timer or via WebSocket updates.
* Group orders into batches for efficient picking.
* Highlight priority shipments or fragile items.
* Enrich events with inventory metadata (e.g., rack locations).

<Frame>
  <img alt="The image shows a &#x22;Warehouse Packer Dashboard&#x22; displaying orders for packing, including products, prices, and total amounts for two customers." />
</Frame>

Example extension idea: For each product in the Kafka event, query an inventory service or database to join a `rack` or `location` field (e.g., "rack 15"), then include that in the rendered order to speed up picking.

## Key takeaway

Kafka serves as the central event bus connecting front-end producers and backend consumers like the warehouse UI. This decouples systems and enables a flexible, event-driven architecture where each service can independently produce or consume events.

This completes the end-to-end demo for the warehouse backend UI. See you in the next lesson!

## Links and references

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* [confluent-kafka-python (Confluent)](https://github.com/confluentinc/confluent-kafka-python)

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/95f49caf-8e0b-4ed9-b7dd-9f43ff31ed9a/lesson/52d6f4ac-f228-47d9-b3fd-f46e6605c637)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/95f49caf-8e0b-4ed9-b7dd-9f43ff31ed9a/lesson/b8ac19cd-cf27-4e2b-9b13-059c78ae7c23)


# Section Recap

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Project-Building-an-Event-Driven-System/Section-Recap/page

Recap of building an event driven order processing system using Apache Kafka where front end producers send events to topics and consumers update a warehouse dashboard

Welcome back. This recap walks through the full event-driven flow we implemented, highlighting each component and the sequence of actions from order creation to dashboard update.

What we built

* A shopping front-end that emits an "Order Placed" event. Each event carries the order payload (order ID, items and quantities, totals, customer info, timestamps).
* A producer that serializes and publishes those events to an Apache Kafka topic.
* A Kafka deployment (provisioned on an EC2 instance in this project) that hosts the topic(s) and persists the event stream.
* A warehouse dashboard that acts as a Kafka consumer: it subscribes to the topic, deserializes messages, manages offsets and consumer groups, and updates the UI based on consumed events.

How the data flows

1. User places an order in the front-end UI.
2. The front-end producer packages and serializes the order payload and publishes it to a Kafka topic.
3. Kafka stores the event in the topic partitions (running on an EC2-hosted broker for this project).
4. The warehouse dashboard consumer (or multiple consumers in a consumer group) reads, deserializes, and processes events, then updates the UI and any downstream systems.

<Frame>
  <img alt="The image illustrates an event-driven system flow involving a shopping application, where an &#x22;Order Placed&#x22; event is sent to a Kafka topic and then directed to a warehouse dashboard." />
</Frame>

Key phases at a glance

| Phase                   | Purpose                             | Example / Key settings                                                              |
| ----------------------- | ----------------------------------- | ----------------------------------------------------------------------------------- |
| Kafka provisioning      | Host brokers and topics             | Provision Kafka on an EC2 instance and create topic(s)                              |
| Producer (front-end)    | Emit and serialize events           | Ensure correct serializer (e.g., JSON/Avro), include metadata (timestamps, orderId) |
| Topic configuration     | Partitioning & retention            | Choose partitions for parallelism and retention for replayability                   |
| Consumer (dashboard)    | Consume, deserialize, and update UI | Configure consumer group, offset strategy (earliest/latest), and deserializer       |
| Validation & monitoring | Confirm end-to-end delivery         | Use producer/consumer CLI tools or integration tests; monitor lag and broker health |

> **lightbulb** Testing tip: Validate each stage independently. Produce test events directly to the Kafka topic, consume them with a simple CLI consumer, then verify the dashboard logic. This helps isolate producer, broker, and consumer issues.

Links and references

* [Apache Kafka — official docs](https://kafka.apache.org/documentation/)
* [Event Streaming with Kafka course (project)](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka)
* [Amazon EC2 documentation](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

Putting it together, the main steps were:

* Set up Kafka (cluster/topic provisioning)
* Build the front-end UI and producers to emit events
* Build the back-end/API and consumers to process those events and update the dashboard

I hope this recap gives you a clear, end-to-end view of building an event-driven system using Apache Kafka. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/95f49caf-8e0b-4ed9-b7dd-9f43ff31ed9a/lesson/e90a6252-9730-42b9-b4ed-f63e2220d9b9)
