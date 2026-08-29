# Introduction to Apache Kafka

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Foundations-of-Event-Streaming/Introduction-to-Apache-Kafka/page

Introduction to Apache Kafka describing its role as a distributed event streaming platform, core concepts, architecture integration, and common use cases like stream processing and real-time analytics

Hello and welcome back.

In this lesson we take a high-level look at Apache Kafka and where it fits in a modern data architecture. This guide covers what Kafka is, why teams use it, and the core concepts you’ll encounter when designing event-driven systems.

What you’ll learn

* A concise definition of Apache Kafka and its primary use cases
* How Kafka integrates producers and consumers in a data architecture
* Key Kafka concepts: topics, partitions, brokers, producers, consumers, and retention
* Where to find further reading and official documentation

## What is Apache Kafka?

Apache Kafka is a distributed event streaming platform built for large-scale, high-throughput, low-latency data streams. Kafka excels at:

* Durable, fault-tolerant storage of event streams
* A publish/subscribe model that decouples producers (writers) from consumers (readers)
* Enabling real-time stream processing, event sourcing, and analytics

> **lightbulb** Kafka is commonly used for event sourcing, stream processing, log aggregation, and real-time analytics. It acts as a durable, scalable backbone for transporting events between systems.

## How Kafka fits into a data architecture

Many systems generate events (web apps, mobile apps, IoT devices, microservices). Kafka sits in the middle as a central, durable event bus: producers publish events to Kafka topics, and one or more consumers subscribe to those topics to process, analyze, or store the data. This decoupling allows independent scaling and resilience across services.

<Frame>
  <img alt="The image illustrates an introduction to Apache Kafka, showing how various data sources like webpages and IoT devices feed into Kafka, which then connects to different systems like microservices and databases." />
</Frame>

In the diagram above:

* Left: producers (web pages, microservices, IoT devices, mobile apps) generate events.
* Center: Kafka topics receive and durably store those events.
* Right: consumers (microservices, analytics platforms, databases) subscribe to topics and process or persist the events.

Kafka enables multiple independent consumers to read the same stream of events at their own pace. This durable, decoupled architecture simplifies integration patterns compared to brittle point-to-point connections.

<Frame>
  <img alt="The image is an introduction to Apache Kafka, illustrating its role as a data processing platform that connects various sources like webpages, microservices, IoT devices, and Android mobiles to destinations such as microservices, analytical platforms, and databases." />
</Frame>

Think of Kafka as a superhighway for data: producers put events on the highway, Kafka stores and transports them reliably, and consumers pick them up as needed.

## Core Kafka concepts

Below are the fundamental building blocks you will encounter when working with Kafka.

|   Concept | What it is                                                                | Why it matters                                                         |
| --------: | ------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
|     Topic | A named feed to which records are published and from which consumers read | Logical channel for organizing event streams                           |
| Partition | An ordered, immutable sequence of records within a topic                  | Enables parallelism and ordering guarantees per partition              |
|    Broker | A Kafka server that stores partitions and serves clients                  | Provides durability and fault tolerance; clusters are multiple brokers |
|  Producer | A client that writes records to topics                                    | Decouples event creation from downstream processing                    |
|  Consumer | A client that reads records from topics                                   | Can process or persist events independently and at its own pace        |
| Retention | The configured time or size a topic retains records                       | Allows replay and time-travel across event streams                     |

## Why use Kafka instead of point-to-point integrations?

* Decoupling: Producers and consumers evolve independently without direct dependencies.
* Scalability: Partitions allow distributed processing across consumers.
* Durability: Events are stored reliably for replay or auditability.
* Multiple consumers: Different teams or systems can independently consume the same events.
* Real-time processing: Enables streaming analytics and near-real-time reactions.

This article introduces the motivations, delivery guarantees, and core Kafka concepts — topics, partitions, brokers, producers, consumers, and retention — which you’ll explore in greater depth in subsequent lessons.

## Links and references

* Apache Kafka official documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Confluent Kafka resources: [https://www.confluent.io/resources/](https://www.confluent.io/resources/)
* Event streaming overview: [https://www.confluent.io/what-is-event-streaming/](https://www.confluent.io/what-is-event-streaming/)

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/2359e80d-66f6-4080-8e9c-d81a6a1600fe/lesson/43a2ea6f-42d6-427a-895c-4826b8d557c2)
