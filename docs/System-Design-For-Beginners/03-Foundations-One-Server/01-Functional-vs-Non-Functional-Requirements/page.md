# Pseudo-code
attempt = 0
max_attempts = 5
base_delay = 1.0  # seconds

while attempt < max_attempts:
    attempt += 1
    try:
        return call_remote_service()
    except TransientError:
        sleep_time = min(base_delay * (2 ** (attempt - 1)), 30)
        # Add small random jitter
        sleep_time *= (0.5 + random.random() * 0.5)
        sleep(sleep_time)
# if we get here, return error to caller
```

Note: Reads (GETs) are usually safe to retry because they do not change state. Writes (POST/PUT/PATCH) are potentially dangerous to retry unless you can guarantee the side effects happen at most once — which is where idempotency comes in.

<Frame>
  <img alt="The image is an illustration showing a flowchart of a payment failure and retry mechanism involving a load balancer, app server, and service, with a timeline indicating retry attempts." />
</Frame>

## Idempotency

Idempotency guarantees that performing the same operation multiple times has the same effect as performing it once. This property makes retries safe for state-changing operations.

The elevator-button metaphor is helpful: pressing a call button once or ten times only causes the elevator to come once.

A common approach is to attach an idempotency key to each client-initiated request. The service stores the state of processed keys and uses them to deduplicate work.

Example behavior with idempotency key:

* Client sends a write request with `Idempotency-Key: A7Q`.
* On first receipt of `A7Q`: the service performs the action, records that `A7Q` has been completed (and optionally stores the response), and returns success.
* On subsequent receipts of `A7Q`: the service detects `A7Q` is already processed and returns the stored success result without performing the action again.

<Frame>
  <img alt="The image illustrates a system architecture flowchart for idempotency in processing a &#x22;like&#x22; request in a social media app. It shows the interaction between a mobile interface, load balancer, app server, service, and database." />
</Frame>

Implementation considerations:

* Where to store idempotency records: use a durable store that supports fast lookups (a database table, a distributed cache with persistence, etc.).
* TTL for idempotency records: keep them long enough to cover retries (minutes to days depending on use-case) but not indefinitely.
* Store both the outcome and any meaningful response payload you want to replay to the client.
* Ensure the idempotency check and the action are atomic or use a transactional pattern so race conditions cannot lead to double processing.

Example idempotency record (JSON):

```json theme={null}
{
  "idempotency_key": "A7Q",
  "status": "completed",
  "response": { "payment_id": "pay_12345", "amount": 1000 },
  "created_at": "2025-01-01T12:00:00Z",
  "expires_at": "2025-01-08T12:00:00Z"
}
```

When to use idempotency keys:

* Payments and billing operations
* Order creation and inventory reservations
* Any state-changing operation where duplicates are harmful

When not to use them:

* Non-critical, cheap operations where duplicates are acceptable
* Operations where deduplication logic would be more complex or costly than the impact of duplicates

## Quick Reference

| Topic       | Recommendation                             | Example / Notes                                            |
| ----------- | ------------------------------------------ | ---------------------------------------------------------- |
| Timeout     | Set per-call timeout and fail fast         | `2s` for user-facing calls; propagate deadlines downstream |
| Retries     | Exponential backoff + jitter; cap attempts | Try immediately, then 1s, 2s, 4s, … up to 5 tries          |
| Idempotency | Use unique idempotency keys for writes     | Store `idempotency_key`, `status`, and `response` with TTL |

## Summary

Combine these three tools:

* Timeouts so slow calls fail fast and don’t exhaust resources.
* Retries with exponential backoff and jitter, and a capped attempt count so transient errors can recover without creating retry storms.
* Idempotency so retries of state-changing operations do not create duplicate side-effects.

> **lightbulb** Timeouts, retries (with backoff), and idempotency are complementary. Timeouts prevent resource exhaustion, backoff-controlled retries handle transient failures, and idempotency makes retries safe for writes.

## Links and References

* [Exponential backoff (Wikipedia)](https://en.wikipedia.org/wiki/Exponential_backoff)
* [Stripe: Idempotent requests](https://stripe.com/docs/api/idempotent_requests)
* [AWS Architecture: Exponential backoff and jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
* [Microsoft: Resiliency best practices](https://learn.microsoft.com/azure/architecture/best-practices/resiliency)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/c7a8e3b7-9370-4462-a298-4a441dd68f8a/lesson/54183933-9f00-46d7-bc16-11c45fde371b)


# Functional vs Non Functional Requirements

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Functional-vs-Non-Functional-Requirements/page

Explains functional versus nonfunctional requirements and how latency, scalability, availability, durability, and cost influence app design and architecture decisions

Before you design an app, answer two distinct but equally important questions:

* What should the app do?
* How well must the app do it?

The answer to the first question defines functional requirements. The answer to the second defines non-functional requirements. This distinction may sound academic until you see how it affects system design and architecture decisions.

## Functional requirements

Functional requirements describe the visible features and behaviors of the system — the actions your users can perform and the outcomes you can test. For a simple photo-sharing app, typical functional requirements include:

* A user can sign up.
* A user can upload a photo.
* A user can follow another user.
* A user can scroll their feed.
* A user can like and comment on posts.

Each item is a concrete feature you can validate: a photo upload either succeeds or fails. If a functional requirement is missing, the app is incomplete, and everyone notices immediately.

<Frame>
  <img alt="The image illustrates the functionality of a photo app, featuring a mockup of the app interface and a checklist of required features like signing up, uploading photos, and interacting with content." />
</Frame>

## Non-functional requirements

Non-functional requirements (NFRs) describe quality attributes and operational constraints rather than specific features. Common NFRs include latency, durability, scalability, availability, and cost. These requirements drive architectural choices even though users never ask for them explicitly.

Ask questions like:

* How fast should the feed load — 0.5 seconds or 8 seconds?
* Will uploaded photos survive a disk failure?
* Will the app support one million users during peak traffic or only a few hundred?

These are not single features you can point to in a UI demo, but they critically shape design decisions.

<Frame>
  <img alt="The image illustrates a conceptual diagram of a mobile app called &#x22;PhotoShare,&#x22; showing its interface alongside a technical overview of its app server, database, and cache, with a focus on non-functional aspects like scalability for one million users." />
</Frame>

Two apps with the same functional list can look and behave very differently once you add non-functional constraints. For example:

* A family photo app can tolerate occasional lag and lower availability.
* Instagram must serve millions (or billions) of users with low latency and high availability.

This distinction explains why additional components appear in real-world systems — load balancers, caches, replicas, message queues, CDNs, and so on. Users ask for a fast, reliable app; engineers choose caches and CDNs to meet the non-functional goals of speed and availability.

| Aspect         | Family Photo App               | Instagram-scale App                     |
| -------------- | ------------------------------ | --------------------------------------- |
| Typical users  | Small group / family           | Millions of global users                |
| Latency target | Relaxed (seconds)              | Strict (\<200ms for many requests)      |
| Availability   | Moderate                       | Very high (multi-regional)              |
| Durability     | Local backups often sufficient | Distributed replication, geo-redundancy |
| Typical cost   | Low                            | High operational cost for scale         |

> **warning** Non-functional requirements frequently conflict. Higher performance and higher availability usually increase cost and complexity. For example, maintaining hot standby machines to tolerate failures increases ongoing infrastructure expenses.

You cannot add every possible component by default. Prioritize components based on the NFRs that matter most for your product and constraints.

> **lightbulb** Ask targeted questions to decide what to build: Who are your users? What are expected peak loads? What latency, durability, and availability targets do you need? What is your budget for infrastructure and operational complexity?

Answering these questions clarifies which non-functional requirements are critical, and that clarity guides the architectural choices you make next.

Further reading and references:

* [System design basics and patterns](https://en.wikipedia.org/wiki/Software_architecture)
* [Designing Data-Intensive Applications](https://dataintensive.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/d9a2aa00-d3e4-44ee-8890-2fa7feca84e0)
