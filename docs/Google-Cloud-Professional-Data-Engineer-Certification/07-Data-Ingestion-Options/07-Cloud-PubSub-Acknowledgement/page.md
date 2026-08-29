# Cloud PubSub Acknowledgement

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Cloud-PubSub-Acknowledgement/page

Explains Google Cloud Pub/Sub acknowledgement mechanisms, deadlines, ack/nack behaviors, and Python examples for reliable at least once message processing

Welcome back. This lesson explains how acknowledgements (acks) work in Google Cloud Pub/Sub, where they fit in the message lifecycle, the different acknowledgement behaviors, and practical code examples using the Python client library. Proper acknowledgement handling is essential for reliability, avoiding duplicate processing, and designing robust subscriber systems.

> **lightbulb** Acknowledgements let Pub/Sub know whether a delivered message was processed successfully. If Pub/Sub doesn't receive an ack, it will assume the message failed and will re-deliver it. Design your subscribers to handle at-least-once delivery semantics.

## Message lifecycle and where acknowledgements fit

1. A topic is created and publishers send messages to it.
2. A subscription is created for the topic; subscribers either pull messages or receive pushed messages from the subscription.
3. Pub/Sub delivers a message to the subscriber (push or pull).
4. The subscriber must acknowledge the message to signal successful processing.
5. If Pub/Sub does not receive an ack before the ack deadline expires, or if the subscriber explicitly nacks the message, the message becomes eligible for redelivery.

## Key implementation details

| Concept            | Description                                           | Notes / Example                                                |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------------------- |
| Ack ID             | Unique identifier for a delivered message (pull-mode) | Required when calling `acknowledge()` or `modifyAckDeadline()` |
| Ack deadline       | Time window for ack (default 10s)                     | Per-subscription default; adjustable up to 600s                |
| ModifyAckDeadline  | Extend/shorten per-message lease                      | Use to prevent premature redelivery while processing           |
| Delivery guarantee | Default is at-least-once                              | Implement idempotency or dedupe logic to handle duplicates     |

## Acknowledgement types and behaviors

| Type                            | Behavior                                                                                                                                                                                                                         | When to use                                                                          |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Negative acknowledgement (nack) | Subscriber explicitly indicates failure; in pull-mode you can call `modifyAckDeadline(..., ack_deadline_seconds=0)` or use `message.nack()` where supported. Pub/Sub will immediately make the message available for redelivery. | Use when processing definitively failed and you want immediate retry.                |
| Explicit acknowledgement (ack)  | Subscriber signals successful processing by calling `acknowledge()` or `message.ack()`. Pub/Sub will not redeliver the message.                                                                                                  | Use after processing succeeds.                                                       |
| Modify acknowledgement deadline | Extend or shorten the lease on the message using `modifyAckDeadline()` to avoid premature redelivery while processing continues.                                                                                                 | Use for long-running work or when processing time is variable.                       |
| Auto-acknowledgement            | In push subscriptions, any HTTP 2xx response is treated as an ack. Some client libraries provide options to auto-ack when the message callback returns.                                                                          | Use with caution—auto-ack can cause lost retries if processing fails after ack.      |
| Ack deadline expiry             | If no ack or `modifyAckDeadline()` arrives before expiry, the message becomes eligible for redelivery (common source of duplicates).                                                                                             | Avoid by extending the deadline when necessary and by designing idempotent handlers. |

<Frame>
  <img alt="A presentation slide titled &#x22;Acknowledgment&#x22; showing five colored boxes that summarize different message-acknowledgment types: Negative Acknowledgment (Nack), Explicit Acknowledgment, Modify Acknowledgment Deadline, Auto Acknowledgment, and Ack Deadline Expiry. Each box includes short bullet points explaining the behavior (nack/ack calls, modifyAckDeadline usage, auto-ack risks, and redelivery on deadline expiry)." />
</Frame>

## Practical examples (Python client library)

Synchronous pull: explicitly acknowledge messages

```python theme={null}
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-subscription")
