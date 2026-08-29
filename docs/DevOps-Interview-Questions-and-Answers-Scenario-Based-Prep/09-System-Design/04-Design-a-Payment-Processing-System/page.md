# Design a Payment Processing System

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/System-Design/Design-a-Payment-Processing-System/page

Designing a resilient payment processing system using idempotency keys, an append only payment event ledger, and webhook based eventual consistency with operational best practices

This guide walks through building a robust payment system for a website. The user journey is straightforward: a customer enters card details, you charge them, and they receive a receipt. We’ll implement that flow and highlight where failures can occur and how to design around them.

Key topics covered:

* Common pitfalls of a naive design
* Preventing duplicate charges with idempotency keys
* Modeling payments as an append-only ledger for auditability
* Handling asynchronous updates with webhooks and eventual consistency
* Operational best practices for production systems

Version one — the naive approach

1. The user enters card details in the browser.
2. Stripe’s JavaScript collects those details securely and sends them directly to Stripe, so your server never sees the raw card number. See [https://stripe.com/docs/js](https://stripe.com/docs/js).
3. Stripe processes the payment and returns a response to your server.
4. Your server marks the order as paid in the database and sends a receipt.

This works for a prototype or hackathon, but it breaks in several important ways.

<Frame>
  <img alt="The image illustrates a simple payment system user journey involving a user entering card details through a browser, using Stripe for payment processing, and receiving a response on their server to confirm payment." />
</Frame>

Where this breaks

Network failures, client retries, or slow servers can cause the request to time out. A user retrying the request can cause duplicate charges if you blindly re-call the payment processor. This leads to customer frustration and operational headaches.

Version two — idempotency keys

To prevent duplicate charges, generate a unique idempotency key (usually a UUID) for each payment attempt. Include that key with the payment request. Write the key to your database before initiating the charge. If the same key is submitted again, return the recorded result instead of issuing a new charge.

Benefits:

* Protects against retries and browser resubmits
* Ensures a single logical payment attempt maps to a single provider charge

Implementation sketch:

* Client generates `idempotency_key` (or the server generates and returns it to the client).
* Server stores (`order_id`, `idempotency_key`, `created_at`) before calling the payment API.
* When receiving the same `idempotency_key` again, look up and return the stored outcome.

<Frame>
  <img alt="The image illustrates a scenario where a duplicate transaction occurs due to a timeout, with a suggestion to use idempotency keys as a solution." />
</Frame>

This eliminates many duplicate-charge scenarios, but payments have richer lifecycles than a single `status` field can represent.

The need for a payment ledger

Payments progress through multiple states: initiated, authorized, captured, refunded, disputed, etc. Modeling a payment as a single mutable database row and overwriting a `status` loses history. When finance, customer support, or regulators ask what happened to a transaction, you must be able to reconstruct the full timeline.

Version three — an immutable ledger

Use an append-only event ledger for each payment. Instead of updating a single `status` repeatedly, append an event for every state change:

* `payment_initiated` — user started the flow
* `payment_authorized` — card issuer authorized the amount
* `payment_captured` — funds captured
* `payment_refunded` — refund issued
* `dispute_opened` — a chargeback or dispute received

Compute the current state by replaying or querying the payment’s ordered event list. This approach preserves an auditable trail and helps when external events (like provider webhooks) arrive out of order.

<Frame>
  <img alt="The image compares a single row payment status system with an immutable ledger, highlighting that an immutable ledger maintains a detailed audit trail through append-only payment events." />
</Frame>

> **lightbulb** Design your payment table as an append-only event ledger. Store each event with its timestamp, source (e.g., client, Stripe webhook), event ID, and raw payload. Compute the current state from that ordered list of events rather than trusting a single mutable `status`.

We still have another major issue: payments are asynchronous.

Version four — webhooks and eventual consistency

When you submit a payment to Stripe (or another processor), you may receive an immediate partial response. Final authorization, capture, or settlement can occur later—seconds, minutes, or even days after the initial request. Your server should not block waiting for finality. Instead, rely on asynchronous notifications (webhooks).

When processing provider webhooks:

* Verify the webhook signature to confirm the payload is from the provider. See [https://stripe.com/docs/webhooks/signatures](https://stripe.com/docs/webhooks/signatures).
* Deduplicate events using the provider’s event ID to avoid double-processing.
* Append each verified webhook as an event in your immutable ledger.
* Make webhook processing idempotent and safe to re-run.

Final architecture (summary)

* Client sends an `idempotency_key` with each payment attempt.
* Server writes a `payment_initiated` intent into the ledger before calling the payment processor.
* The processor may return immediate responses and later send webhook events which your server verifies and appends as new events to the same ledger.
* The payment’s current status is derived from the full event history (replayed or queried).

Example ledger (append-only payment events)

```text theme={null}
payment_events (immutable ledger)
1. payment_initiated      t+0s
2. payment_authorized     t+10s
3. payment_captured       t+1d
```

Operational checklist

| Concern                 | Recommendation                                                                                     |
| ----------------------- | -------------------------------------------------------------------------------------------------- |
| Raw event replayability | Store the raw webhook payload alongside parsed fields for reparsing and reprocessing.              |
| Deduplication           | Index idempotency keys and provider event IDs for efficient lookup.                                |
| Latency & retries       | Implement retries with exponential backoff for outgoing calls; make webhook handlers idempotent.   |
| Audit & compliance      | Retain append-only events for audit; define retention and archival policies for long-term storage. |
| Troubleshooting         | Log correlation IDs, and keep timestamps and event sources (client vs provider) indexed.           |

> **warning** Remember PCI and regulatory requirements: do not log raw card numbers, encrypt sensitive data at rest, and follow your payment provider’s guidance for compliance. Use provider-hosted fields (e.g., Stripe Elements) so your server never handles raw PANs.

Additional recommendations and links

* Keep a single canonical ledger per logical payment to make queries, reporting, and reconciliations straightforward.
* Use provider-side idempotency features in addition to your own keys when available.
* Monitor webhook delivery metrics and implement alerting for failed deliveries or processing errors.

Relevant resources

* Stripe Payments overview: [https://stripe.com/docs/payments](https://stripe.com/docs/payments)
* Stripe webhooks: [https://stripe.com/docs/webhooks](https://stripe.com/docs/webhooks)
* Stripe JS integration: [https://stripe.com/docs/js](https://stripe.com/docs/js)
* Webhook signature verification: [https://stripe.com/docs/webhooks/signatures](https://stripe.com/docs/webhooks/signatures)

This pattern—client-generated idempotency keys, an immutable append-only payment event ledger, and verified webhook handling—yields a resilient, auditable, and production-ready payment processing architecture that handles retries, out-of-order events, and lifecycle events such as refunds and disputes.

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/ef53ec43-96e9-4d1b-8a6e-e6eb97b0d0dc/lesson/8deae359-0cb6-4c99-b9a1-92ee1706239d)
