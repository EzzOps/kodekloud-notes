# Cloud PubSub Intro Topics Subscriptions

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Cloud-PubSub-Intro-Topics-Subscriptions/page

Overview of Google Cloud Pub/Sub focusing on topics, subscriptions, delivery modes, architecture patterns and exam-relevant concepts for building scalable reliable event-driven ingestion systems

Hello and welcome back.

This lesson explains Google Cloud Pub/Sub — a fully managed, real-time messaging service on GCP — focusing on topics and subscriptions. You’ll learn what Pub/Sub is, why it’s useful for data engineers, common architecture patterns (one-to-one, one-to-many, many-to-many, many-to-one), and the exam-relevant points about topics, subscriptions, and delivery modes. Let’s get started.

## What is Google Cloud Pub/Sub?

Google Cloud Pub/Sub implements a publish–subscribe messaging model that decouples producers and consumers to enable scalable, reliable event-driven systems:

* Publishers produce messages and send them to a named resource called a topic.
* Topics durably store and route messages.
* Subscribers consume messages from a subscription attached to the topic and process them (for example, by writing to BigQuery or triggering Cloud Functions).

In short: publishers send messages to topics; subscribers receive messages from subscriptions. This separation lets you scale producers and consumers independently and build resilient ingestion pipelines.

## Common architecture patterns

Below are the canonical Pub/Sub patterns you’ll encounter when designing ingestion or streaming systems. Each pattern has different implications for scaling, ordering, and routing.

### One-to-one setup

A single publisher sends messages to a topic and a single subscriber consumes them. This is the simplest pattern: one producer → one topic → one consumer. Useful for straightforward point-to-point messaging.

<Frame>
  <img alt="A diagram titled &#x22;Cloud Pub/Sub – One-to-One Setup&#x22; showing a publisher on the left sending messages to &#x22;Topic A&#x22; inside Cloud Pub/Sub, with a consumer on the right receiving those messages." />
</Frame>

### One-to-many (fan-out)

Fan-out lets a single publisher send messages to one topic while multiple independent subscribers consume identical copies of each message. This pattern supports parallel downstream use cases (analytics, notifications, inventory updates) without coupling them together.

<Frame>
  <img alt="A diagram titled &#x22;Cloud Pub/Sub — One-to-Many Setup (Fan Out)&#x22; showing a publisher sending messages to Topic A inside Google Cloud Pub/Sub, which then fans out to three consumer/subscriber endpoints. The graphic uses a green publisher icon on the left, a blue topic in the center, and three orange subscriber icons on the right." />
</Frame>

### Many-to-many

Multiple publishers publish into a shared topic and multiple subscribers independently process those messages for different purposes. This is common in high-scale systems like gaming platforms where many producers generate events consumed by analytics, monitoring, and security pipelines.

<Frame>
  <img alt="A diagram titled &#x22;Cloud Pub/Sub – Many-to-Many Setup&#x22; showing multiple publishers on the left sending messages into a central Topic A in Cloud Pub/Sub, which then fan-outs to multiple consumers/subscribers on the right." />
</Frame>

### Many-to-one

Many producers send events into a topic but a single subscriber consumes them (for example, one real-time analytics engine). This centralizes processing while preserving distributed production.

All of these patterns affect how you design for throughput, message ordering, retries, and error handling (e.g., dead-letter topics).

## Pattern comparison

| Pattern               | Description                                               | Typical use case                                    |
| --------------------- | --------------------------------------------------------- | --------------------------------------------------- |
| One-to-one            | Single publisher → single topic → single subscriber       | Simple point-to-point messaging, low complexity     |
| One-to-many (fan-out) | Single publisher → single topic → multiple subscribers    | Broadcast events to analytics, alerts, and services |
| Many-to-many          | Multiple publishers → single topic → multiple subscribers | High-scale event systems with diverse consumers     |
| Many-to-one           | Multiple publishers → single topic → single subscriber    | Centralized processing (e.g., real-time analytics)  |

## Exam-focused summary

Remember these core exam concepts:

* Topic — a named Pub/Sub resource to which publishers send messages. Topics are used for real-time analytics, data-pipeline integration, and decoupling services across your architecture.

<Frame>
  <img alt="A presentation slide titled &#x22;Professional Data Engineer Exam – Key Points to Remember&#x22; with a highlighted &#x22;Topics&#x22; box. The slide defines a topic in Cloud Pub/Sub and notes it is globally distributed and used for real-time analytics, data pipeline integration, and service decoupling." />
</Frame>

> **lightbulb** Key subscription points for the exam: subscriptions define how messages are delivered. Pub/Sub supports pull subscriptions (the subscriber polls for messages) and push subscriptions (Pub/Sub delivers messages to an HTTPS endpoint). Messages must be acknowledged; Pub/Sub guarantees at-least-once delivery (duplicates can occur), and the default ack deadline is 10 seconds (which can be extended).

## Subscriptions and delivery modes

* Pull subscriptions: Subscribers explicitly poll Pub/Sub for messages when they are ready to process them. This model is common for managed processing frameworks (for example, Dataflow) or custom worker fleets that control their own concurrency and backpressure.
* Push subscriptions: Pub/Sub sends messages to a subscriber endpoint (HTTP/HTTPS). Use this when your consumer is a stateless web service that can accept inbound requests.

Other important features to be familiar with:

* Acknowledgement (ack) deadlines — default is 10 seconds; you can extend the deadline while processing.
* At-least-once delivery — consumers must be idempotent or deduplicate messages to handle duplicates.
* Ordering keys — preserve ordering for messages with the same key.
* Dead-letter topics — route undeliverable or repeatedly failing messages for inspection and recovery.

## Next steps

Now that you understand the Pub/Sub model, common patterns, and exam-relevant details, practice creating topics and subscriptions, experiment with pull vs. push delivery, and implement idempotent consumers. Hands-on experience (for example, sending messages with the gcloud CLI or a client library and observing ack behavior) will reinforce these concepts.

## Links and references

* [Google Cloud Pub/Sub documentation](https://cloud.google.com/pubsub)
* [BigQuery documentation](https://cloud.google.com/bigquery)
* [Cloud Functions documentation](https://cloud.google.com/functions)
* [Dataflow documentation](https://cloud.google.com/dataflow)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/6c75003a-7c42-43f2-a312-b014aceecfd6)
