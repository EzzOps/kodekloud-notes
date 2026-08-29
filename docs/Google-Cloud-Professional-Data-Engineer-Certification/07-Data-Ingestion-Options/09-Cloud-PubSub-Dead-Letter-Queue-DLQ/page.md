# Pull messages
response = subscriber.pull(subscription=subscription_path, max_messages=1)

for received in response.received_messages:
    data = received.message.data
    print("Received:", data)
    ack_id = received.ack_id

    # Acknowledge the message so it won't be redelivered
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[ack_id])
```

Modify ack deadline (extend lease) for a pulled message

```python theme={null}
# Extend the ack deadline for this ack_id to 60 seconds
subscriber.modify_ack_deadline(
    subscription=subscription_path,
    ack_ids=[ack_id],
    ack_deadline_seconds=60,
)
```

Streaming pull with callback: automatic lease management with explicit ack/nack

```python theme={null}
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-subscription")

def callback(message):
    print("Received:", message.data)
    try:
        # Process the message...
        message.ack()  # Explicit acknowledgement
    except Exception:
        # Signal failure; many client libraries support message.nack()
        message.nack()

subscriber.subscribe(subscription_path, callback=callback)

# Keep the main thread alive to allow background threads to process messages
import time
while True:
    time.sleep(60)
```

## Notes on system design and subscriber behavior

* Subscriber processing times vary. For short, predictable tasks, short ack deadlines may suffice. For long-running tasks, extend the ack deadline per message or increase the subscription default.
* At-least-once delivery requires idempotency or deduplication. If your processing can't be made idempotent, use dedupe strategies (unique message IDs, external dedupe stores, etc.).
* For push endpoints, only return HTTP 2xx when processing actually succeeded. Returning 2xx will stop retries and is treated as an acknowledgement by Pub/Sub.
* Use `modifyAckDeadline()` responsibly to avoid holding messages indefinitely and to ensure fair redelivery behavior.

> **warning** Be careful with auto-ack behavior. If messages are auto-acknowledged before processing completes (or if a push endpoint returns 2xx while processing actually failed), you may lose the ability to retry and risk data loss or missed processing.

## Quick exam pointers

* Pub/Sub uses ack IDs and ack deadlines to manage delivery and retries.
* The typical exam concept is "at-least-once delivery": messages may be delivered more than once unless you implement deduplication or enable exactly-once features where supported.

## Links and references

* [Pub/Sub documentation - Subscriber best practices](https://cloud.google.com/pubsub/docs/subscriber)
* [Pub/Sub Python client library](https://googleapis.dev/python/pubsub/latest/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/fa7afdf0-da07-4adf-87a3-2ba02ce25ce3)


# Cloud PubSub Dead Letter Queue DLQ

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Cloud-PubSub-Dead-Letter-Queue-DLQ/page

Overview of Google Cloud Pub/Sub dead letter queues, configuration, causes, monitoring, and reprocessing strategies for handling messages that repeatedly fail processing

Welcome back.

Acknowledgements in Google Cloud Pub/Sub let subscribers confirm successful message processing so Pub/Sub can remove those messages or re-deliver them when needed. This lesson extends that concept to handle messages that continually fail: dead letter queues (DLQs).

## What is a Dead Letter Queue (DLQ)?

A dead letter queue is a secondary Pub/Sub topic that safely stores messages that repeatedly fail processing. Instead of allowing a single problematic message to block the subscription and slow your pipeline, Pub/Sub forwards those messages to the DLQ for later inspection, repair, or reprocessing.

## Typical DLQ flow

1. A publisher sends messages to a topic.
2. Subscribers consume messages and attempt processing.
3. If a message exceeds the configured maximum delivery attempts, Pub/Sub forwards it to the subscription's dead letter topic.
4. Engineers inspect and fix DLQ messages, then either reprocess them or update subscriber logic to handle the payloads.

> **lightbulb** Exam tip: DLQs are configured on subscriptions, not topics. This is a common multiple-choice trap.

## Why messages end up in a DLQ

Messages commonly land in a DLQ for these reasons:

| Category            | Examples                                                         |
| ------------------- | ---------------------------------------------------------------- |
| Schema & format     | Unexpected additional fields, schema mismatches, wrong types     |
| Payload corruption  | Malformed JSON or binary data                                    |
| Downstream failures | External service outages that cause repeated processing failures |
| Application bugs    | Subscriber code that doesn't handle certain inputs               |

## Example scenario

* A publisher sends JSON messages that must include exactly four keys.
* Some messages contain extra keys or malformed fields.
* The subscriber logic throws errors for those payloads and never acknowledges them.
* After the configured number of delivery attempts, Pub/Sub moves the problematic messages to the DLQ for manual review.

## Why use a DLQ?

* Prevent blocked subscriptions: without a DLQ, Pub/Sub keeps retrying failed messages and may slow the entire subscription.
* Isolate problematic messages: engineers can review individual failed records and choose to reprocess or discard.
* Improve reliability and traceability: individual bad messages won't derail the whole pipeline.

## Best practices for DLQs in Pub/Sub

* Configure a sensible `maxDeliveryAttempts` (often 5–10).
  * Too low: transient errors may cause premature DLQing.
  * Too high: excessive retries increase latency and waste resources.
    Tune based on failure patterns and message criticality.

* Monitor DLQ growth and set alerts. Use [Cloud Monitoring](https://cloud.google.com/monitoring) to detect sudden increases in DLQ messages, which can indicate schema changes or downstream outages.

* Build a robust reprocessing workflow. After fixing root causes, re-ingest DLQ messages back into the pipeline or transform them with [Dataflow](https://cloud.google.com/dataflow) / [Apache Beam](https://beam.apache.org) before republishing.

* Ensure idempotency when reprocessing to avoid duplicate side effects.

## Configuration example

Note: the dead-letter topic must already exist as a Pub/Sub topic and should typically be in the same project as the subscription. When using `gcloud` in the same project you can refer to topics by their short names; otherwise supply the full resource name: `projects/PROJECT_ID/topics/TOPIC`.

Create a dead-letter topic and a subscription with a dead letter policy using `gcloud`:

```bash theme={null}
