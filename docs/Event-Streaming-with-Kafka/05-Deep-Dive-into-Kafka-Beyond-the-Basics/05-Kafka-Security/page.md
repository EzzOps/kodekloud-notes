# Kafka Security

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/Kafka-Security/page

Overview of Kafka security best practices using a banking example, covering encryption in transit and at rest, authentication and authorization, schema use, and access controls for sensitive event data.

Hello and welcome back.

In this lesson we’ll explain core Kafka security concerns using a concise banking example and show practical controls you can apply. This article covers the common threats and recommended defenses so teams can make informed choices about confidentiality, integrity, and access control for event data.

## Example scenario

Imagine a banking application that produces events to a Kafka cluster:

* When a customer logs in, the app produces an event to the topic `login-events`.
* When a payment occurs, the app produces an event to the topic `card-payment-event`.

Various internal consumers (microservices, analytics pipelines, or partner systems) read these topics. Because these topics may contain sensitive customer information, we must answer several security questions:

* Are events protected while in transit from producers/consumers to brokers?
* Who is consuming these events and are they authorized to read them?
* How is the data stored on broker disks protected?

## Producers and consumers

* Producers: banking app writing to `login-events` and `card-payment-event`.
* Consumers: internal data consumers that read one or both topics.

From a security perspective you should ensure:

* Encryption for data in transit (TLS).
* Strong client authentication and authorization (SASL / OAuth + ACLs or RBAC).
* Protection of data at rest (disk-level encryption or application-level encryption).

## Data in transit: TLS (encryption and client auth)

Encrypt connections between clients and brokers using TLS. For mutual TLS, enable client certificate authentication so brokers verify producer/consumer identities.

Example server-side configuration snippets (server.properties):

```properties theme={null}
