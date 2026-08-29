# Argo Events Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Argo-Events-Architecture/page

Overview of Argo Events architecture, describing EventSources, EventBus, and Sensors for building CloudEvents-based event-driven workflows and triggers on Kubernetes

Let's explore Argo Events, an event-driven workflow automation framework for Kubernetes. Argo Events enables you to trigger actions — for example, Kubernetes Jobs, Argo Workflows, AWS Lambda, notifications, or custom HTTP requests — in response to events from many external systems. This guide explains the core components, responsibilities, and the end-to-end flow for building reliable event-driven workflows on Kubernetes.

## High-level components

Argo Events centers on three primary components that separate concerns for event capture, transport, and reaction:

| Component   | Role                                                    | Example responsibilities                                                   |
| ----------- | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| EventSource | Capture & normalize incoming events                     | Listen to webhooks, S3, Kafka; emit CloudEvents                            |
| EventBus    | Transport events between producers and consumers        | Durable pub/sub (NATS/JetStream, Kafka)                                    |
| Sensor      | Consume events, evaluate dependencies, execute triggers | Evaluate event conditions, run triggers (K8s objects, Workflows, webhooks) |

Each component has a clear responsibility: EventSources handle ingestion and normalization, the EventBus provides decoupled transport, and Sensors orchestrate triggers once dependencies are satisfied.

## Event sources

EventSources are the system's ingress points — they connect to external producers and convert their native payloads into a consistent internal format.

Common EventSource types:

* Webhooks (GitHub, GitLab, generic HTTP)
* Cloud object storage notifications (e.g., [AWS S3](https://aws.amazon.com/s3/))
* Messaging systems ([AWS SQS](https://aws.amazon.com/sqs/), [SNS](https://aws.amazon.com/sns/), [Kafka](https://kafka.apache.org/), [GCP Pub/Sub](https://cloud.google.com/pubsub))
* Schedulers (time-based cron events)
* Custom providers or third-party services

EventSource responsibilities:

* Listening/consuming events from external systems
* Normalizing events into the CloudEvents format (id, source, type, time, data, etc.)

<Callout icon="lightbulb">
  Standardizing events to the CloudEvents spec simplifies downstream processing. CloudEvents provides a predictable envelope so Sensors and other consumers can reason about events without per-source parsing logic.
</Callout>

Example minimal EventSource (webhook) YAML:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: webhook-source
spec:
  webhook:
    example:
      endpoint: /payload
      port: "12000"
      method: POST
      url: /payload
```

## EventBus — the transport layer

After an EventSource converts an incoming event to CloudEvents, it publishes the event to the EventBus. The EventBus decouples producers and consumers using a publish/subscribe model and provides durability and scalability for event delivery.

Popular EventBus implementations:

| Implementation | Use case / benefits                                                        |
| -------------- | -------------------------------------------------------------------------- |
| NATS           | Lightweight, low-latency pub/sub                                           |
| JetStream      | NATS persistence, message retention, at-least-once delivery                |
| Kafka          | High-throughput, partitioning, long-term retention and ordering guarantees |

Argo Events uses these underlying messaging systems to route CloudEvents from EventSources to Sensors, allowing EventSources to simply publish without knowing which Sensors will consume the events.

<Callout icon="warning">
  NATS Streaming (STAN) is deprecated. For new deployments prefer NATS JetStream or Kafka, which provide better persistence and streaming semantics.
</Callout>

## Sensor — the event consumer and orchestrator

Sensors subscribe to the EventBus to receive CloudEvents. A Sensor defines:

* Event dependencies: which events (and conditions) must arrive
* Dependency evaluation: logic for combining or matching events (single, multiple, or grouped)
* Triggers: what actions to run when dependencies are satisfied

Sensor responsibilities:

* Continuously monitor the EventBus for matching CloudEvents
* Evaluate dependency expressions and conditions
* Execute one or more triggers with optional payload transformation, retries, and backoff

Common trigger types:

| Trigger type      | Example actions                                     |
| ----------------- | --------------------------------------------------- |
| Kubernetes object | Create/update Deployments, Jobs, CRDs               |
| Argo Workflows    | Start a workflow DAG                                |
| Serverless        | Invoke [AWS Lambda](https://aws.amazon.com/lambda/) |
| Notifications     | Send Slack messages, email alerts                   |
| HTTP/webhook      | POST data to an endpoint                            |

Example Sensor YAML that waits for an event and triggers a Kubernetes Job:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: simple-sensor
spec:
  dependencies:
    - name: example-dep
      eventSourceName: webhook-source
      eventName: example
  triggers:
    - template:
        name: k8s-job-trigger
        k8s:
          group: batch
          version: v1
          resource: jobs
          operation: create
          source:
            resource:
              apiVersion: batch/v1
              kind: Job
              metadata:
                generateName: triggered-job-
              spec:
                template:
                  spec:
                    containers:
                      - name: hello
                        image: busybox
                        command: ["echo", "event triggered"]
                    restartPolicy: Never
```

Sensors support payload transformations (patching trigger payloads with event data), retry/backoff policies, and conditional triggers so you can model complex event-driven workflows.

## End-to-end flow (summary)

1. An external system or service generates an event.
2. The EventSource captures the event and converts it into the CloudEvents format.
3. The EventSource publishes the CloudEvent to the EventBus.
4. The Sensor, subscribed to the EventBus, receives the CloudEvent and evaluates its dependencies.
5. Once the Sensor’s dependencies are satisfied, it executes the configured trigger(s).

This separation (capture → normalize → transport → evaluate → trigger) forms a reliable, decoupled architecture for building event-driven automation in Kubernetes.

## Best practices and recommendations

* Use CloudEvents everywhere to keep payloads consistent.
* Choose an EventBus with the durability and throughput you need (JetStream or Kafka for persistence).
* Configure Sensor retry and backoff policies for transient failures.
* Keep EventSources lightweight; push heavy processing into downstream consumers or workflows.
* Monitor EventBus health and retention to avoid data loss or backpressure.

## Links and references

* [Argo Events on GitHub](https://github.com/argoproj/argo-events)
* [CloudEvents specification](https://cloudevents.io/)
* [NATS Project](https://nats.io/)
* [Apache Kafka](https://kafka.apache.org/)
* [Kubernetes documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/c18b034d-c1e0-4c2d-84cc-0cb94cfef165" />
</CardGroup>
