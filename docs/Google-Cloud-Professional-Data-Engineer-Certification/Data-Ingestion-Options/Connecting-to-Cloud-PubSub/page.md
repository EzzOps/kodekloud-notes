# Connecting to Cloud PubSub

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Connecting-to-Cloud-PubSub/page

Overview of connecting applications to Google Cloud Pub/Sub, covering client libraries, authentication with Application Default Credentials, publish and subscribe patterns, code examples, and operational best practices

Welcome back. In this lesson we’ll examine how applications and services connect to Google Cloud Pub/Sub, the managed messaging service for asynchronous communication. You’ll learn where connections occur, how client libraries communicate with the service, recommended authentication patterns, commonly used publish/subscribe designs, code examples in popular languages, and operational best practices.

## Architecture overview

Connections to Cloud Pub/Sub happen in two primary places:

* Publisher side — applications that send messages (for example, microservices, data collection APIs, or logging agents like Fluent Bit).
* Subscriber side — applications that receive messages from a subscription (for example, other microservices, data pipeline workers, or serverless functions).

Both publishers and subscribers use Google Cloud client libraries. Think of the client library as a language-specific connector that handles authentication, retries, batching, flow control, and network details so your application can focus on message semantics.

## How client libraries communicate

* Protocols: gRPC is used by default for performance and low latency. REST/JSON endpoints are also available for certain use cases and tooling.
* Endpoint: Client libraries communicate with the Pub/Sub endpoint at `pubsub.googleapis.com` unless you explicitly configure a different endpoint.
* Responsibilities handled by libraries: authentication (Application Default Credentials or explicit service account keys), automatic retries, publish batching, and subscription flow control/backpressure.

## Authentication and IAM

Application Default Credentials (ADC) are the recommended authentication method:

* In Google Cloud runtimes (Compute Engine, GKE, Cloud Run, Cloud Functions), ADC is usually available automatically.
* When running outside Google Cloud (for example, local development), set `GOOGLE_APPLICATION_CREDENTIALS` to a service-account key file:

```bash theme={null}
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

<Callout icon="lightbulb">
  Use least-privilege IAM roles. For publishing and subscribing, grant the `roles/pubsub.publisher` or `roles/pubsub.subscriber` role respectively to the service account.
</Callout>

## Publish vs. subscribe patterns

* Publishing: Clients publish messages to a topic. Libraries support synchronous and asynchronous (future/promise-based) publish APIs and provide batching options for higher throughput.
* Pull subscribers: Clients pull messages from a subscription. Modern libraries support streaming pull with callback handlers and automatic lease (ack deadline) management.
* Push subscribers: Pub/Sub sends HTTP POST requests to a configured HTTPS endpoint when new messages arrive. Push endpoints must acknowledge the request (e.g., return HTTP 200) to avoid redelivery.

## Client library packages (common languages)

| Language | Official package                       |
| -------- | -------------------------------------- |
| Python   | `google-cloud-pubsub`                  |
| Java     | `com.google.cloud:google-cloud-pubsub` |
| Node.js  | `@google-cloud/pubsub`                 |
| Go       | `cloud.google.com/go/pubsub`           |
| C#       | `Google.Cloud.PubSub.V1`               |

Installation examples:

```bash theme={null}
