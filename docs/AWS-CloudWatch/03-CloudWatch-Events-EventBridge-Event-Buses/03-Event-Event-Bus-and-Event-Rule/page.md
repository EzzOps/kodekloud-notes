# Event Event Bus and Event Rule

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/CloudWatch-Events-EventBridge-Event-Buses/Event-Event-Bus-and-Event-Rule/page

This lesson explains AWS Events, Event Buses, and Event Rules for building decoupled, scalable architectures.

Welcome to this lesson on AWS Events, Event Buses, and Event Rules. By the end of this guide, you’ll understand how these components interact to build decoupled, scalable architectures.

## What Is an Event?

An **event** is a JSON document that captures a state change or activity in your environment. Think of it as a structured message with metadata and payload—whenever something happens (for example, a new order is placed), an event is emitted.

Example event payload:

```json theme={null}
{
  "version": "0",
  "id": "abcd-1234-efgh-5678",
  "detail-type": "OrderPlaced",
  "source": "ecommerce.app",
  "time": "2024-06-01T12:34:56Z",
  "detail": {
    "orderId": "12345",
    "paymentStatus": "SUCCESS",
    "amount": 99.99
  }
}
```

<Callout icon="lightbulb">
  Events are immutable and timestamped. Use descriptive `detail-type` and `source` fields to simplify filtering.
</Callout>

## What Is an Event Bus?

An **event bus** acts as a central router for all your events. AWS EventBridge provides three types of buses:

| Bus Type | Description                                                 |
| -------- | ----------------------------------------------------------- |
| Default  | Automatically available; receives events from AWS services. |
| Custom   | Created by you; receives events from your applications.     |
| Partner  | Ingests events from SaaS partners and third-party services. |

The event bus handles ingestion, filtering, and routing—abstracting away the need to maintain custom message brokers.

## What Is an Event Rule?

An **event rule** inspects incoming events on a bus against a pattern or schedule. When an event matches, the rule routes it to one or more targets (Lambda functions, SNS topics, SQS queues, Step Functions, etc.).

Key features:

* **Pattern matching**: Filter by JSON fields, prefixes, or numeric ranges.
* **Scheduled events**: Trigger actions on cron or rate-based schedules.
* **Multiple targets**: Fan out a single event to various downstream services.

Example rule pattern:

```json theme={null}
{
  "source": ["ecommerce.app"],
  "detail-type": ["OrderPlaced"],
  "detail": {
    "paymentStatus": ["SUCCESS"]
  }
}
```

## How They Work Together

The following table summarizes the roles of each component:

| Component  | Role                                 | Example Target                  |
| ---------- | ------------------------------------ | ------------------------------- |
| Event      | Payload describing a change          | `{ "paymentStatus":"SUCCESS" }` |
| Event Bus  | Central router for events            | Default or custom bus           |
| Event Rule | Filters and forwards matching events | Lambda, SNS, SQS, etc.          |

### E-Commerce Order Processing Workflow

1. **OrderPlaced** event is emitted when a customer completes checkout.
2. EventBridge sends the event to the **default event bus**.
3. An **event rule** filters for `paymentStatus: ["SUCCESS"]`.
4. Matched events trigger a **Lambda function** that fulfills the order and sends a confirmation email.

```bash theme={null}
