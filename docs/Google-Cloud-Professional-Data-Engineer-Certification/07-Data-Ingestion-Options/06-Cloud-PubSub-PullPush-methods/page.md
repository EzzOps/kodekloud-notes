# Cloud PubSub PullPush methods

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Cloud-PubSub-PullPush-methods/page

Compares Cloud Pub/Sub push and pull delivery methods, explaining mechanisms, acknowledgements, use cases, scaling, and guidance for choosing between low-latency push and batch-oriented pull

Hello and welcome back.

This lesson builds on connecting to Cloud Pub/Sub and how publishers and subscribers communicate using topics and subscriptions. Here we dive deeper into how that communication actually happens — specifically through push and pull delivery methods. Understanding push vs. pull is important when designing reliable, low-latency, or high-throughput data pipelines on Google Cloud.

We'll cover:

* How push subscriptions deliver messages to HTTPS endpoints
* How pull subscriptions let clients fetch messages (synchronously or via streaming)
* When to choose each approach, with practical examples and a decision guide

For official reference, see the Cloud Pub/Sub docs: [https://cloud.google.com/pubsub/docs](https://cloud.google.com/pubsub/docs)

## Push subscriptions

Push subscriptions are endpoint-driven: Cloud Pub/Sub delivers messages by making HTTPS POST requests to a pre-configured endpoint. Typical endpoints include App Engine apps, Cloud Run services, Compute Engine load balancers that terminate HTTPS, or any properly configured HTTPS server reachable by Pub/Sub.

Key behaviors and characteristics:

* Delivery: Pub/Sub sends each message to the subscriber endpoint as an HTTPS POST containing the message and attributes.
* Acknowledgement: The subscriber must return an HTTP 2xx response to acknowledge receipt. Non-2xx responses or network errors trigger retries with exponential backoff until the message is acknowledged or the message retention / dead-letter policy takes effect.
* Low latency: Because Pub/Sub actively pushes messages, push subscriptions are well suited for real-time use cases such as fraud detection, notifications, or IoT scenarios that need immediate reaction.
* Simplified client logic: The subscriber does not poll for messages; delivery, retry mechanics, and basic flow control are managed by Pub/Sub.

Example: a typical push POST payload looks like this:

```json theme={null}
{
  "message": {
    "data": "BASE64_ENCODED_PAYLOAD",
    "attributes": {
      "key": "value"
    },
    "messageId": "2070443601311540",
    "publishTime": "2020-04-22T23:11:55.123Z"
  },
  "subscription": "projects/myproject/subscriptions/mysub"
}
```

* The `data` field is base64 encoded; your subscriber must decode it.
* To acknowledge the message, return an HTTP `200 OK` (or any 2xx) response.

When to choose push:

* Your application requires near-instant processing of individual messages.
* You can host a reliable HTTPS endpoint (or use Cloud Run/App Engine) that can scale or handle retries.
* You prefer simplified subscriber logic and offloaded retry handling.

## Pull subscriptions

With pull subscriptions, the subscriber is responsible for actively requesting messages from Pub/Sub. Pull has two models:

* Synchronous Pull API: the client issues Pull requests to fetch messages.
* StreamingPull: a long-lived gRPC stream that delivers messages to the client, improving throughput and latency for high-volume consumers.

Key behaviors and characteristics:

* Client-driven: The subscriber controls when and how many messages to fetch, and must explicitly acknowledge messages using the Ack API.
* Ack deadline: Messages must be acknowledged within the ack deadline (default 10s); otherwise the message becomes available for redelivery. Subscribers can call ModifyAckDeadline to extend processing time.
* Batch- and throughput-friendly: Pull is ideal when you want to batch-process large volumes of messages at controlled rates — for example, periodic ingestion into BigQuery or feeding Dataflow pipelines.
* Flexible scaling: You can scale worker instances up or down to match processing capacity; pull gives you finer control over parallelism and batching behavior.

Example: a simple synchronous Pull request body:

```json theme={null}
{
  "maxMessages": 10
}
```

The server returns a list of messages and `ackIds`; to acknowledge:

```json theme={null}
{
  "ackIds": ["ACK_ID_1", "ACK_ID_2"]
}
```

StreamingPull is recommended for high-throughput consumers because it reduces per-request overhead and increases throughput and responsiveness.

When to choose pull:

* You process messages in batches or at scheduled intervals (e.g., 15-minute or hourly batches).
* You need explicit control over concurrency, rate limiting, or ack timing.
* You integrate with batch-oriented systems or worker pools that coordinate parallel processing.

<Frame>
  <img alt="A slide titled &#x22;Push and Pull Subscriptions&#x22; with a central consumer/subscriber icon. Two dashed panels compare Push Subscriptions (endpoint-driven, low-latency, simplified code) versus Pull Subscriptions (client-driven, batch-friendly)." />
</Frame>

You can safely scale the number of worker instances for pull subscriptions without worrying about message loss: Pub/Sub retains unacknowledged messages until they are acknowledged, expire, or are moved to a dead-letter topic, depending on your configuration.

## Feature comparison

| Feature           |                              Push subscriptions | Pull subscriptions                                          |
| ----------------- | ----------------------------------------------: | ----------------------------------------------------------- |
| Delivery model    |                     Server-initiated HTTPS POST | Client-initiated Pull/StreamingPull                         |
| Typical latency   |                            Low (near real-time) | Variable; low with StreamingPull, higher for batch pulls    |
| Client complexity |                      Lower (simple HTTP server) | Higher (explicit Pull, Ack, ModifyAckDeadline)              |
| Best for          |              Event-driven, real-time processing | Batch processing, bulk ingestion, high-throughput pipelines |
| Scaling model     | Endpoint must scale to handle concurrent pushes | Scale workers independently to control throughput           |
| Retry handling    |         Managed by Pub/Sub (retries on non-2xx) | Managed by client (retries, ack deadlines)                  |
| Examples          |                 Notifications, webhooks, alerts | Bulk ETL, periodic BigQuery loads, worker pools             |

## Quick decision guide

* Need instant, per-message processing? Choose push.
* Processing in near real-time batches or large-volume batch jobs? Choose pull (StreamingPull for high throughput).
* Want simplified subscriber code and managed retries? Push is simpler.
* Need fine-grained control over batching, concurrency, and ack deadlines? Use pull.

> **lightbulb** This lesson focused on how messages are delivered (pushed vs pulled). Related topics to review next: acknowledgement types, ack deadlines, retry strategies, dead-letter topics, and how to determine that a message was successfully processed (not just delivered).

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/a66b2e75-4011-4cd4-bfae-2a5ef2536aac)
