# Poison Pill in Kafka

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/Poison-Pill-in-Kafka/page

Explains Kafka poison pill problem where a malformed message stalls partition processing and outlines causes, real world impact, and mitigation patterns like DLQs and safe consumer handling.

Welcome — this lesson explains the poison pill problem in Apache Kafka: how a single bad message can stop partition processing, why it happens, and what you can do about it.

## Analogy: production line blockage

Imagine a conveyor belt where packages are scanned one-by-one. A crane places a package under a QR scanner, the scanner reads the code, and the package continues down the line. If one package has a damaged QR code, the scanner cannot read it and the conveyor stops: everything behind the unreadable package waits.

Kafka partitions behave the same way. Within a partition, messages are read and processed in strict order. A single malformed or unexpected record at a given offset can prevent the consumer from advancing, causing the partition’s processing to stall.

Concretely: within a consumer group each partition is assigned to a single consumer which reads offsets sequentially. If that consumer encounters a problematic offset (for example offset 2) and throws an unhandled exception or never advances/commits the offset, it will try to re-process the same offset repeatedly (on restart or re-poll) and keep failing. Because offsets must be processed in order, the partition cannot make forward progress. The result is processing lag, potential event loss if not addressed, and wasted resources as the consumer repeatedly retries or crashes.

<Frame>
  <img alt="The image illustrates a Kafka architecture with a broker labeled &#x22;Topic A / Partition 1&#x22; and a Consumer Group A consisting of three consumers. It depicts a sequence of messages, highlighting the message numbered '2'." />
</Frame>

## What is a poison pill message?

A poison pill is any record that causes a consumer to repeatedly fail or get stuck at a particular offset. Typical causes include:

* Malformed data (e.g., broken or truncated JSON).
* Unexpected content that violates the schema or business invariants.
* Resource-exhausting payloads that make processing impossible within limits.
* Any content that causes continuous consumer crashes or unbounded retries, creating backlog growth.

<Frame>
  <img alt="The image outlines four types of Kafka &#x22;Poison Pills&#x22;: Malformed Data, Unexpected Content, Resource Exhaustion, and System Instability, with brief descriptions of each." />
</Frame>

## Quick reference: poison pill types

| Type                | Symptoms                                      | Typical sources                             |
| ------------------- | --------------------------------------------- | ------------------------------------------- |
| Malformed data      | Deserialization exceptions, parse errors      | Program bugs, producer corruption           |
| Schema violations   | Validation failures, nulls where not expected | Outdated producers or schema drift          |
| Resource exhaustion | OOM, timeouts, long GC pauses                 | Very large payloads or expensive processing |
| System instability  | Consumer crashes, repeated retries            | Dependency failures, transient exceptions   |

## Real-world impact

Left unchecked, poison pills cause:

* Stalled partitions and increased consumer lag.
* Backlog growth across the topic.
* Potential data loss if operators delete or skip data without proper handling.
* Operational overhead: restarts, alerts, and manual intervention.

## Mitigation patterns

Below are standard approaches to avoid or reduce poison-pill impact. Use them in combination depending on your system’s reliability requirements.

| Pattern                                       | Description                                                                                      | When to use                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| Producer-side validation & schema enforcement | Validate and reject bad messages before they reach Kafka (e.g., Schema Registry + Avro/Protobuf) | Prevents most malformed data                                |
| Consumer-side validation & error handling     | Catch exceptions, validate payloads, and isolate problematic records                             | Always use as a defensive measure                           |
| Dead-letter queue (DLQ)                       | Route unprocessable records to a separate topic for later inspection                             | For irrecoverable messages that should not block processing |
| Selective offset commits                      | Commit past irrecoverable messages after recording them                                          | When business logic allows skipping bad records             |
| Exponential backoff & circuit breakers        | Retry transient failures with backoff; open circuit on persistent faults                         | For transient dependencies like downstream services         |
| Monitoring & alerts                           | Detect stuck partitions, high consumer lag, and repeated errors                                  | Enables fast operational response                           |

<Callout icon="lightbulb">
  Common mitigations include producer-side schema validation, consumer-side safe exception handling, routing problematic messages to a dead-letter queue (DLQ), committing offsets selectively to skip irrecoverable messages, exponential backoff and circuit breakers for transient failures, and monitoring/alerts to surface stuck partitions quickly.
</Callout>

## Example: safe consumer error handling

A consumer should validate inbound records and handle failures without letting the partition stall. The following pseudocode demonstrates a pattern to detect a bad message, route it to a DLQ, commit the offset, and continue processing:

```pseudo theme={null}
while (poll()) {
  record = poll.next()
  try {
    validate(record)
    process(record)
    commit(record.offset)
  } catch (ValidationError e) {
    // send to DLQ for later inspection
    produce(dlqTopic, record)
    // commit the offset to skip this bad record
    commit(record.offset)
    log.warn("Record moved to DLQ and offset committed", record.offset, e)
  } catch (TransientError e) {
    // retry with backoff or rethrow to let consumer retry later
    retryWithBackoff(record)
  } catch (Throwable t) {
    // fail-fast for unknown critical errors, allow restart and alert
    alertOps(t)
    throw t
  }
}
```

Notes:

* Committing the offset after sending to a DLQ ensures progress while preserving the problematic payload for inspection.
* Use idempotent or transactional producers where applicable when writing to DLQs to avoid duplicates.
* For some systems, selective skip/commit strategies must align with business requirements (e.g., auditability, exactly-once semantics).

## References and further reading

* Apache Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Confluent blog: Dead-letter queue patterns and best practices

In the next lesson we’ll dive into concrete code examples and operational practices for implementing DLQs, selective commits, and robust consumer designs to avoid production outages.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/8be9df9e-fb9d-47b7-ba44-8954150e2161" />
</CardGroup>
