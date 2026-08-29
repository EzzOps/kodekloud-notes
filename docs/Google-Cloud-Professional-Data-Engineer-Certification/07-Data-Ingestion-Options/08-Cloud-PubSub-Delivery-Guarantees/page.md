# Create the dead-letter topic
gcloud pubsub topics create my-dead-letter-topic

# Create the main topic
gcloud pubsub topics create my-main-topic

# Create a subscription for the main topic that forwards messages to the DLQ
gcloud pubsub subscriptions create my-subscription \
  --topic=my-main-topic \
  --dead-letter-topic=my-dead-letter-topic \
  --max-delivery-attempts=5
```

## Reprocessing DLQ messages

Common approaches:

* Pull messages from the dead-letter topic and republish to the original topic after fixing payloads.
* Run a Dataflow job to transform and republish DLQ messages in bulk.
* Add a manual review step for sensitive records before reprocessing.

Always design reprocessing to be idempotent and ensure duplicate handling in downstream systems.

<Frame>
  <img alt="A &#x22;Best Practices&#x22; diagram for Cloud Pub/Sub showing a publisher sending messages to Topic A, a Dead Letter Queue holding failed messages, and a subscriber consuming messages, with brief recommendations about retry limits, DLQ monitoring, and reprocessing." />
</Frame>

This approach ensures data completeness so messages are not lost forever.

## Real-world example

Imagine an e-commerce system where payment events are published to Pub/Sub. If some events fail due to missing fields or malformed payloads, they land in the DLQ. After diagnosing and fixing the root cause (for example, updating the publisher schema or adding defensive parsing in the subscriber), engineers can reprocess DLQ messages to ensure no transactions are missed—preserving financial accuracy and customer trust.

## Summary

Dead letter queues in Pub/Sub:

* Prevent message blockage by isolating repeatedly failing messages.
* Allow focused analysis and remediation of problematic records.
* Improve system reliability, traceability, and data completeness.

For hands-on practice, create and configure Pub/Sub topics and subscriptions with DLQs in your GCP project and build a reprocessing flow using Dataflow or custom tooling.

## Links and references

* [Cloud Pub/Sub documentation](https://cloud.google.com/pubsub)
* [Cloud Monitoring](https://cloud.google.com/monitoring)
* [Dataflow (Apache Beam)](https://cloud.google.com/dataflow)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/fdec956d-7a93-4107-9f0e-0af807f5f53e)


# Cloud PubSub Delivery Guarantees

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Cloud-PubSub-Delivery-Guarantees/page

Explains Cloud Pub/Sub delivery guarantees, comparing at‑least‑once and exactly‑once semantics, how acknowledgements affect duplicates, and guidance on idempotency, deduplication, and use cases.

Welcome — in this lesson you'll learn how Cloud Pub/Sub delivery guarantees work and how subscriber acknowledgments affect message reliability. We cover the two delivery models Pub/Sub supports, explain their behavior, and show when to choose each approach for robust, production-ready messaging.

There are two primary delivery guarantees:

* `At‑least‑once` (the default)
* `Exactly‑once`

We’ll define each, show common causes of duplicates or message loss, and give practical guidance for designing subscribers and downstream systems.

## At‑least‑once delivery (default)

`At‑least‑once` is Pub/Sub’s default delivery guarantee: every published message will be delivered to subscribers at least once, so messages are never silently lost. However, individual messages can be delivered multiple times.

Duplicates most often arise when:

* A subscriber delays an acknowledgement
* The ack deadline expires before processing completes
* Network retries or transient errors cause redelivery

Because duplicates are possible, subscribers must be built to tolerate repeated deliveries by using stable IDs, idempotent operations, or explicit deduplication logic.

<Frame>
  <img alt="Slide titled &#x22;Cloud Pub/Sub Delivery Guarantees&#x22; showing that the default is &#x22;At‑Least‑Once Delivery.&#x22; It notes messages may be duplicated if acknowledgments are delayed or retried, ensuring no message loss but requiring subscribers to handle duplicates." />
</Frame>

Why this matters for engineers

* Use a stable, application-level message identifier so repeated IDs can be detected and ignored.
* Implement idempotent processing: handling the same message multiple times should result in the same state as handling it once.
* Add a deduplication layer (in memory, in a database, or in an external service) when absolute uniqueness is required.

<Frame>
  <img alt="A slide titled &#x22;Cloud Pub/Sub Delivery Guarantees&#x22; showing &#x22;At-Least-Once Delivery&#x22; (the default) with a truck icon. It notes the use case: best when reliability matters more than occasional duplication (e.g., logging, metrics ingestion)." />
</Frame>

Use cases

* Logging and metrics ingestion where occasional duplicates are acceptable.
* Telemetry and analytics event collection where completeness is more important than perfect uniqueness.
* Any pipeline where losing messages is unacceptable but downstream systems can handle or deduplicate repeats.

> **lightbulb** When asked about Cloud Pub/Sub's default delivery mode, the correct answer is at‑least‑once delivery.

## Exactly‑once delivery

`Exactly‑once` aims to ensure each published message is delivered and processed exactly one time. Implementing exactly‑once semantics usually combines:

* Precise acknowledgement and checkpointing,
* Idempotency or deduplication in the subscriber or downstream systems,
* Integrations with tools that support deduplication (for example, [Cloud Dataflow](https://cloud.google.com/dataflow)).

Exactly‑once eliminates duplicates but increases operational complexity and cost. If a message is acknowledged as processed under an exactly‑once setup, Pub/Sub will not re‑deliver it — so recovery and auditing strategies are essential to prevent data loss.

> **warning** Exactly‑once reduces duplicates but requires careful operational controls. If processing fails after acknowledging a message, recovery can be difficult—plan for auditing, retries, or replay mechanisms outside Pub/Sub.

<Frame>
  <img alt="A presentation slide titled &#x22;Cloud Pub/Sub Delivery Guarantees.&#x22; It highlights &#x22;Exactly-Once Delivery&#x22; and notes it uses acknowledgment tracking, idempotency checks, and integration with Cloud Dataflow or a deduplicating subscriber." />
</Frame>

When to use exactly‑once
Use exactly‑once delivery when duplicates would cause serious correctness or financial problems and you can accept the extra design and operational cost:

* Financial transactions and billing systems (to avoid double charges).
* Stateful workflows or counters where duplicate events would corrupt state.
* Mission-critical reconciliation processes requiring strict uniqueness guarantees.

<Frame>
  <img alt="A slide titled &#x22;Cloud Pub/Sub Delivery Guarantees&#x22; with an icon and label for &#x22;Exactly-Once Delivery&#x22; on the left. On the right is a &#x22;Use Case&#x22; note saying it's best for financial transactions, billing, or stateful workflows where duplicates cannot be tolerated." />
</Frame>

## Quick comparison

| Guarantee       | Delivery behavior                                                        | Duplicates                            | Typical use cases                                   | Complexity / Cost |
| --------------- | ------------------------------------------------------------------------ | ------------------------------------- | --------------------------------------------------- | ----------------- |
| `At‑least‑once` | Messages are delivered ≥1 times; Pub/Sub retries until acknowledged      | Possible                              | Logging, telemetry, analytics ingestion             | Low to medium     |
| `Exactly‑once`  | Guarantees single effective processing (with deduplication/ack tracking) | Eliminated (if implemented correctly) | Billing, financial transactions, stateful workflows | High              |

## Summary

* At‑least‑once is Pub/Sub’s default: it prevents message loss but permits duplicate deliveries. Build subscribers to tolerate or remove duplicates.
* Exactly‑once removes duplicates when you implement acknowledgement tracking and deduplication, but it raises complexity and operational cost. Use it only for workloads where duplicates are unacceptable.

We’ll also cover how Pub/Sub handles messages that repeatedly fail processing and introduce the dead letter queue (DLQ) concept next: see the [dead letter topics documentation](https://cloud.google.com/pubsub/docs/dead-letter-topics) for details and configuration guidance.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/51294116-c719-48d0-a5a0-fa9fdcdf9163)
