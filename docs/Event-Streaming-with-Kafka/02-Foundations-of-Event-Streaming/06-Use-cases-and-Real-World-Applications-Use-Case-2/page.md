# Use cases and Real World Applications Use Case 2

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Foundations-of-Event-Streaming/Use-cases-and-Real-World-Applications-Use-Case-2/page

Explains using Apache Kafka to stream EV charging station status and session events for real time availability, billing, monitoring, and scalable stream processing

Hello and welcome back. In this lesson we examine how Apache Kafka can enable real-time updates, billing, and monitoring for an electric vehicle (EV) charging station network. This example demonstrates common event-driven design patterns for IoT, stream processing, and payment/billing workflows.

## Real-time requirements for EV charging stations

An EV charging station must address several simultaneous, real-time concerns:

* Notify drivers which chargers are free so they can find or reserve a charger.
* Track how long a vehicle was charged (and energy delivered) so users can be billed correctly.
* Provide administrators with remote monitoring of station health, faults, and utilization.

To support these needs reliably and at scale, the architecture typically models two distinct event types and routes them to separate Kafka topics.

## Event types and topic strategy

1. Station status events — indicate availability and operational state (e.g., `free`, `occupied`, `fault`, `reserved`).
2. Charging session events — capture session lifecycle data (start time, stop time, energy delivered, user id).

Keeping these event types in separate Kafka topics simplifies downstream processing and enables independent retention, schema evolution, and consumer behavior.

<Callout icon="lightbulb">
  Separate topics allow independent scaling, retention policies, and schema evolution. Use message keys (for example `station_id`) to ensure all messages for the same station route to the same partition (Kafka guarantees ordering within a partition) and to enable partitioned processing.
</Callout>

## Topic configuration patterns (recommended)

| Topic            | Typical retention & semantics                        | Keying / partitioning                                       | Primary use                                          |
| ---------------- | ---------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| Station status   | Compacted topic (keep latest state per `station_id`) | Key by `station_id` to preserve ordering                    | Reconstruct current state and feed availability APIs |
| Charging session | Append-only with longer retention (audit/billing)    | Key by `session_id` or `station_id` depending on processing | Billing, audit trail, analytics                      |

## Sample message formats

Use a clear schema (Avro/Protobuf/JSON Schema) and register schemas in a schema registry so producers and consumers evolve safely.

Example station status event (JSON):

```json theme={null}
{
  "station_id": "station-1234",
  "timestamp": "2026-07-15T12:34:56Z",
  "status": "occupied",
  "connector_id": "c1",
  "error_code": null
}
```

Example charging session event (JSON):

```json theme={null}
{
  "session_id": "sess-9876",
  "station_id": "station-1234",
  "user_id": "user-42",
  "start_time": "2026-07-15T12:35:00Z",
  "stop_time": "2026-07-15T13:10:00Z",
  "energy_kwh": 12.5,
  "price_cents": 1875
}
```

## End-to-end data flow (high level)

* IoT devices and charger controllers (producers) publish events into Kafka topics when plug-in/out, faults, reservations, or payments occur.
* Messages should be keyed by `station_id` (or `session_id` for session-scoped ordering) so updates for a given charger are routed to the same partition and ordering is preserved.
* A stream processing layer (Kafka Streams, ksqlDB, or another consumer) aggregates status events to compute real-time metrics such as "available chargers at station X" and publishes aggregates or exposes them via APIs.
* Downstream consumers:
  * Mobile/web apps subscribe to status aggregates or the `station-status` topic to show availability and enable reservations.
  * The billing/payment system consumes `charging-session` events to calculate duration/energy and perform invoicing or payment processing.
  * Admin dashboards and alerting systems consume both topics for monitoring, fault detection, and capacity planning.

## Consumers and processing patterns

* Real-time aggregates: use Kafka Streams or ksqlDB to compute running counts (e.g., available connectors), time-windowed metrics, or alerts.
* Billing pipelines: process append-only session events for accurate invoicing and audit. Use transactional producers/consumers or idempotent design when possible to ensure accuracy.
* Monitoring and alerting: feed metrics into Prometheus/Grafana or an observability platform; use compacted status topics to quickly reconstruct current station states.

<Callout icon="warning">
  For billing and financial workflows, ensure exactly-once semantics or strong deduplication. Use Kafka transactions, idempotent producers, or a robust reconciliation process to avoid duplicate charges or missing sessions.
</Callout>

## Benefits of this architecture

* Real-time user experience: drivers receive immediate availability updates and can reserve chargers.
* Accurate billing: session events provide an audit trail with start/stop times and energy consumption.
* Operational observability: administrators can monitor utilization, detect faults, and respond remotely.
* Scalability and decoupling: Kafka separates producers (IoT devices) from many independent consumers so each downstream service can scale and evolve separately.

Below is a diagram that illustrates these interactions and shows how event streams move from chargers through Kafka to the various consumers and systems.

<Frame>
  <img alt="The image is a flowchart illustrating the use of Kafka for real-time updates on electric vehicle charging, showing components like charging stations, session topics, and monitoring metrics. It details interactions between EV charging, payment systems, and station status consumers." />
</Frame>

## Further reading and references

* Apache Kafka: [https://kafka.apache.org/](https://kafka.apache.org/)
* Kafka Streams documentation: [https://kafka.apache.org/documentation/streams](https://kafka.apache.org/documentation/streams)
* ksqlDB: [https://ksqldb.io/](https://ksqldb.io/)
* Schema design and registry concepts (Confluent Schema Registry)

That is it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/2359e80d-66f6-4080-8e9c-d81a6a1600fe/lesson/ca84ed71-bfa4-48cf-8728-2f0cd993d689" />
</CardGroup>
