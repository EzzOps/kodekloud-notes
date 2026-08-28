# What is a Coupled System

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/What-is-a-Coupled-System/page

Explains differences between tightly coupled and loosely coupled microservice designs using login and fraud services, comparing trade offs, use cases, and message bus options.

Hello and welcome back.

This lesson explains the difference between tightly coupled and loosely coupled systems in the context of microservices. We'll use a simple example — an authentication (login) service and a downstream fraud detection service — to illustrate the trade-offs and when each approach is appropriate.

Scenario: a login microservice must validate credentials and then notify downstream systems (for example, a fraud detection service) about the login event.

## Tightly coupled system

In a tightly coupled design the login service calls the fraud service directly and waits for it to process the event before continuing. Because the login service depends on the fraud service being available and responsive, the two services become tightly coupled.

Key consequences of tight coupling:

* Direct dependency: producer (login service) calls the consumer (fraud service) directly, creating a single point of failure.
* Synchronous communication: the producer blocks until the consumer responds, increasing latency and reducing throughput.
* Reduced flexibility: changing, adding, or scaling downstream checks may require changes and redeployment of the login service.
* Poor fault tolerance: if the fraud service is down, login processing can be blocked or fail, which may cause cascading failures.

This design can be appropriate for flows that require an immediate, synchronous decision (for example, blocking a login based on an instantaneous fraud check). However, for many scalable production systems, tight coupling is a liability.

<Frame>
  <img alt="A presentation slide titled &#x22;Tightly Coupled System&#x22; listing four issues: Direct Dependency, Synchronous Communication, Limited Flexibility, and Poor Fault Tolerance. Each point has a short description explaining linked producers/consumers, blocking waits, difficulty adding consumers, and risk of cascading failures." />
</Frame>

<Callout icon="lightbulb">
  Tightly coupled systems are simpler to implement for small or latency-sensitive flows, but they reduce resilience and make independent evolution of services harder.
</Callout>

## Loosely coupled system (event-driven)

A loosely coupled design uses a central messaging layer (message bus / event broker). Instead of calling the fraud service directly, the login service publishes a login event to the message bus and continues immediately without waiting for downstream processing.

The message bus persists events until consumers (fraud service, auditing, analytics) fetch and process them. Consumers can process events asynchronously, recover after downtime, and replay events when needed. New consumers can subscribe to the same events without changing the producer.

Key characteristics of loosely coupled systems:

* Independence: services can be developed, deployed, and scaled independently. Producers do not need to know the identity of consumers.
* Reusability: one published event can be consumed by multiple systems (fraud detection, auditing, metrics) without modifying the producer.
* Fault isolation: consumer failures do not block producers; messages remain durable until processed.
* Flexibility and scalability: consumers can be scaled or replaced independently; new consumers are easy to add.

<Frame>
  <img alt="A presentation slide titled &#x22;Loosely Coupled System&#x22; showing four labeled benefits—Independence, Reusability, Fault Isolation, and Flexibility & Scalability—each with a short explanatory note below." />
</Frame>

## Quick comparison

| Aspect         | Tightly coupled                    | Loosely coupled (event-driven)                  |
| -------------- | ---------------------------------- | ----------------------------------------------- |
| Communication  | Synchronous, direct                | Asynchronous, via message bus                   |
| Failure impact | High — failures cascade            | Lower — messages persisted, consumers can retry |
| Flexibility    | Low — producer must know consumers | High — producers publish events only            |
| Scaling        | Harder — coordinated               | Easier — scale consumers independently          |
| Use case       | Immediate decision required        | Auditing, analytics, decoupled workflows        |

## When to choose which

* Choose tight coupling when:
  * You require immediate results and cannot proceed without the downstream response.
  * Latency constraints force a synchronous flow and the downstream service is highly available.
* Choose loose coupling when:
  * You need scalability, resilience, and independent evolution of services.
  * You want multiple consumers for the same event (analytics, audit logs, monitoring).
  * You need durable, replayable events and fault isolation.

## What is the central message bus?

Common implementations of the central messaging layer include:

* Cloud Pub/Sub — fully managed, scalable message bus on Google Cloud: [https://cloud.google.com/pubsub](https://cloud.google.com/pubsub)
* Apache Kafka — high-throughput distributed event streaming platform: [https://kafka.apache.org/](https://kafka.apache.org/)
* Confluent Platform — enterprise Kafka distribution and tooling: [https://www.confluent.io/](https://www.confluent.io/)

These systems provide durable event storage, configurable delivery semantics (for example, at-least-once delivery), consumer groups, and replay capabilities — all essential building blocks for loosely coupled microservice architectures.

## Links and references

* [Cloud Pub/Sub](https://cloud.google.com/pubsub)
* [Apache Kafka](https://kafka.apache.org/)
* [Confluent](https://www.confluent.io/)

Use these resources to learn how message brokers implement durability, delivery guarantees, and scaling patterns that enable loosely coupled microservices.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/994928ec-3115-48ca-9e59-23851dcd512c" />
</CardGroup>
