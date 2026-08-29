# Interview Byte Answer at the Right Altitude

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Interview-Byte-Answer-at-the-Right-Altitude/page

Advice for system design interviews recommending stating the desired level of detail up front and outlining high level architecture, trade offs, and when to drill into low level design

When an interviewer asks you to "design Instagram", start by stating the altitude at which you'll answer. Setting the expected scope up front prevents wasted effort and shows you understand the difference between high-level architecture and low-level design.

A concise one-line opener you can use:

"I'll stay at a high level — I'll describe components, data flow, and trade-offs; we can zoom into any single component later if you'd like."

Saying this sentence up front demonstrates clarity about scope. Many candidates lose momentum because they immediately dive into implementation details without confirming the interviewer’s expectations.

<Callout icon="lightbulb">
  Always confirm the expected level of detail. Ask a clarifying question such as: "Do you want a high-level system architecture or a low-level class/data-structure design?"
</Callout>

Why set the altitude?

* Avoids answering the wrong question. Interviewers rarely interrupt early — it’s your responsibility to set the altitude.
* Keeps your design organized: high-level first (components, data flow, QoS and failure domains), low-level only when asked (data structures, algorithms, class signatures).
* Helps you prioritize trade-offs relevant to the requested scope (scalability, availability, cost).

High-level vs low-level — examples and when to use each

* High-level system design (e.g., "Design Instagram"): cover major components such as API gateway, web/mobile clients, media storage, feed generation, notification service; explain data flow between components; discuss capacity planning and scaling strategies (sharding, caching, CDN) and failure-recovery approaches.
* Low-level system design (e.g., "Design an in-memory cache"): focus on classes, data structures, and algorithms (for example, implementing an LRU cache); do not discuss servers, load balancers, or CDNs unless the interviewer asks you to expand the scope.

Practical one-line guardrail you can say before diving in:

* "I'll assume a high-level architecture first (components + data flow + scaling), and then we can pick one component to design in-depth."

Common interview example: If the interviewer wanted a class/algorithm, they expect something like:

```typescript theme={null}
class LRUCache {
  get(key: string): any
  put(key: string, val: any): void
}
```

Comparison table: high-level vs low-level focus

| Focus level | Typical scope                              | Example topics                                                               | When to use                                                    |
| ----------- | ------------------------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------- |
| High-level  | System components and interactions         | API gateway, clients, CDN, media storage, feed generation, caching, sharding | When asked to "design Instagram" or "design a social network"  |
| Low-level   | Code, classes, algorithms, data structures | LRU cache, hash maps, threading, concurrency primitives, API signatures      | When asked to "design an LRU cache" or "implement X algorithm" |

Interview tips and phrasing

* Start with your altitude declaration: sets expectations and invites clarification.
* Ask one clarifying question if the prompt is ambiguous (e.g., scale targets, consistency vs availability trade-offs, read/write ratio).
* Outline end-to-end data flow at a glance (clients → API layer → service components → storage → CDN/caches).
* Present one or two scaling strategies and trade-offs instead of listing every possible pattern.
* If asked to drill down, say which component you'll zoom into and why (e.g., "I'll drill into feed generation because it's the core scalability challenge here").

Common mistakes to avoid

* Diving into low-level details (data structures, code) when the interviewer expects a high-level architecture.
* Describing components without explaining data flow or the motivations for choices.
* Not discussing failure modes and recovery (e.g., backups, replication, eventual consistency).
* Listing buzzwords without tying them to concrete trade-offs (e.g., "use sharding" — explain shard key and how it affects rebalancing).

Quick checklist to follow in a design interview

1. Clarify scope: altitude, constraints (scale, latency, budgets), and success metrics.
2. High-level diagram: components and data flow.
3. Capacity/scale planning: rough numbers and strategies (caching, sharding, CDNs).
4. Resilience: fault domains, replication, failover.
5. Drill-down on a single component when asked (include APIs, data models, algorithms).
6. Summarize trade-offs and next steps.

Resources and further reading

* [System Design Primer](https://github.com/donnemartin/system-design-primer)
* [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
* [High Scalability](http://highscalability.com/)

<Callout icon="warning">
  Avoid starting with implementation details (classes, code) when the interviewer asked for a high-level system design. Confirm the expected altitude upfront.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/6c85b350-ee21-4923-a539-742c78880e71" />
</CardGroup>
