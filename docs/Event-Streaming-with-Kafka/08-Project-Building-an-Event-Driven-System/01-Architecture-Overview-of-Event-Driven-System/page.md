# Architecture Overview of Event Driven System

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Project-Building-an-Event-Driven-System/Architecture-Overview-of-Event-Driven-System/page

Overview of building an end-to-end event-driven e-commerce architecture using Apache Kafka, mapping UI events to producers, brokers, and independent consumers with a near-real-time dashboard

Welcome to this lesson. We will design and implement an end-to-end event-driven architecture for an e-commerce scenario using Apache Kafka. The goal is to convert a user-centric UI flow into a working producer/consumer system and then implement a near-real-time dashboard that reacts to events.

This article explains the user flow, maps it to Kafka components, and outlines an implementation plan you can follow in code and on an EC2 demo host.

User flow (high-level)

* A user opens the web UI and starts a session.
* The user adds items to a cart and eventually places an order.
* When the user places an order, the front-end triggers an "order placed" event that is produced to Kafka.
* Multiple independent consumers read the same event; for example:
  * A warehouse dashboard updates so staff can begin packing.
  * Fraud detection, analytics, and notification services independently consume the event.
* Each consumer processes events independently without interfering with one another.

This pattern demonstrates a core benefit of event-driven architectures: a single immutable event in Kafka can be consumed by multiple downstream systems, enabling loose coupling and parallel processing.

<Frame>
  <img alt="The image is a flowchart illustrating an event-driven system using Kafka, where user interactions like starting a session, adding items to a cart, and placing orders trigger events that update a dashboard and warehouse system." />
</Frame>

How the components map to responsibilities

* Producer (front-end / backend): Sends an `orders.placed` event to a Kafka topic. The producer can be invoked via a simple HTTP POST from the UI to a small backend service that writes to Kafka.
* Kafka cluster (broker): Persists events in topics. Topics are append-only logs and can be partitioned for throughput and ordering guarantees.
* Consumers: Independent services that subscribe to the topic and process events. Examples include the warehouse dashboard, fraud detection, analytics, and notification services.
* Dashboard / UI: Subscribes to Kafka (directly or via a lightweight backend/websocket layer) and displays near-real-time order state.

Component responsibilities and examples

| Component    | Responsibility                                             | Example / Notes                                        |
| ------------ | ---------------------------------------------------------- | ------------------------------------------------------ |
| Producer     | Create and publish `orders.placed` events                  | Front-end → HTTP POST → Flask backend → Kafka producer |
| Kafka broker | Persist events to topics, provide partitions and retention | Use topic name `orders.placed` or `orders.events`      |
| Consumer     | Subscribe and process events independently                 | Warehouse dashboard consumer, fraud detection consumer |
| Dashboard    | Real-time UI that reflects incoming events                 | Use websockets or SSE for live updates to the browser  |

Key technical concepts (practical tips)

* Topic naming: Use clear, intent-driven names like `orders.placed` or `orders.events`.
* Ordering: If strict ordering is required per user, ensure events for that user use the same partition key (e.g., user ID) so they land in the same partition.
* Idempotency and deduplication: Consumers must handle retries and potential duplicate deliveries; design processors to be idempotent or to detect and discard duplicates.
* Consumer groups: Multiple instances of the same logical consumer can form a consumer group to share partitions (scale-out). Different logical consumers (warehouse vs fraud) should use different consumer group IDs so each receives all events.

> **lightbulb** This is a simplified end-to-end architecture. In production you will also consider schema management (e.g., Avro/Schema Registry), monitoring, security (TLS/auth), retention policies, and error-handling strategies (dead-letter queues, retries).

> **warning** Ordering and idempotency are common pain points: if you need per-user ordering, consistently key events by user. For at-least-once delivery (Kafka default), make consumer processing idempotent or add deduplication logic to avoid processing the same event multiple times.

Implementation plan — step by step

1. Build a simple static website (HTML/CSS) with an "Place Order" action that triggers an HTTP request to the backend.
2. Implement a lightweight backend (Python + Flask) that receives the UI request and produces an `orders.placed` event to Kafka.
   * Example flow: browser → `POST /orders` → Flask handler → Kafka producer → return success.
3. Deploy Kafka and the services to an EC2 instance for a self-contained demo environment.
4. Implement one or more consumers (Python) that read the `orders.placed` topic and:
   * Update a warehouse dashboard (via a backend + websockets or SSE).
   * Optionally write to analytics stores or trigger notification services.
5. Wire the dashboard to refresh in near real time as new events arrive.

Technology choices (for this lesson)

* Python: producer and consumer logic (kafka-python or confluent-kafka)
* Flask: simple HTTP endpoint for receiving UI requests and producing events
* HTML/CSS: minimal front-end to trigger order events
* EC2: host Kafka cluster and demo services
* VS Code: development environment

Practical examples and naming conventions

* Topic: `orders.placed`
* Event payload (JSON): include `order_id`, `user_id`, `items`, `total`, `timestamp`
* Partition key: use `user_id` if you require per-user ordering

Next steps

* In the next article we will set up Kafka on an EC2 instance, create the `orders.placed` topic, and implement the Flask producer and Python consumer code to wire the end-to-end flow.
* After that, we'll add schema validation (Schema Registry + Avro), monitoring, and a production-ready deployment plan.

Links and references

* Apache Kafka: [https://kafka.apache.org/](https://kafka.apache.org/)
* Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Confluent Schema Registry: [https://docs.confluent.io/platform/current/schema-registry/index.html](https://docs.confluent.io/platform/current/schema-registry/index.html)
* Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* AWS EC2: [https://aws.amazon.com/ec2/](https://aws.amazon.com/ec2/)

That’s it for this lesson. In the next article we’ll start provisioning the demo environment and implementing the producer and consumer code. See you there.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/95f49caf-8e0b-4ed9-b7dd-9f43ff31ed9a/lesson/f6633582-0c5d-4e44-8daa-059e0d9b364c)
