# Interview Byte How Does the Feed Get Built

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Media-APIs-and-Async-Work/Interview-Byte-How-Does-the-Feed-Get-Built/page

Explains push, pull, and hybrid feed strategies for social apps, comparing tradeoffs and operational mitigations like batching, queues, caching, and celebrity thresholding

When designing a photo‑sharing app, a common interview prompt is: when someone famous posts a photo, how do eighty million followers’ feeds get updated? Interviewers expect you to name the main approaches, explain trade‑offs, and recommend a practical solution with operational details.

High‑level options:

* Fan‑out on write (push): update followers’ timelines at post time.
* Fan‑out on read (pull): build the timeline when a user opens the app.
* Hybrid: combine push for normal users and pull for celebrities.

## Fan‑out on write (push at post time)

At post time, the system pushes a reference (or a copy) of the new photo into each follower’s prebuilt feed/timeline.

Benefits

* Extremely fast reads — timelines are precomputed and ready to serve.
* Simplified read path: minimal merging and ranking on fetch.

Costs and operational challenges

* Write amplification: a celebrity post can produce millions of writes.
* Storage duplication: storing references or cached copies across many timelines.
* Backpressure on write pipelines, requiring robust queuing, batching, retries, and idempotency.
* Need for storage strategies that tolerate high write fan‑out (sharding, compaction, TTL).

<Frame>
  <img alt="The image illustrates two approaches to data distribution: &#x22;Fan-out on Write&#x22; and &#x22;Fan-out on Read,&#x22; with diagrams showing their processes and impacts on a feed system." />
</Frame>

Mitigations commonly discussed in interviews

* Batch writes and aggregate fan‑outs into worker jobs.
* Use message queues (Kafka, Pub/Sub) and backpressure controls.
* Write only references (IDs) instead of full payloads to reduce storage.
* Incremental rebuilds and background reconciliation for consistency.
* Rate limiting or throttling for extreme fan‑outs (celebrity posts).

## Fan‑out on read (pull at fetch time)

When a user opens the app, the system fetches recent posts from followed accounts, merges and ranks them, and returns a timeline.

Benefits

* Writes are localized to the author’s activity store; posting does not trigger massive downstream writes.
* Freshness: reads can reflect the latest state without replaying many writes.

Costs and operational challenges

* Reads are heavier: each request triggers many fetches, merges, and ranking operations.
* Higher latency and CPU/I/O per read, which can hurt user experience without caching or aggressive optimization.
* Increased complexity in optimizing and parallelizing reads across services and caches.

Common optimizations

* Caching hot accounts’ recent posts.
* Parallel fetching and efficient merging/ranking pipelines.
* Read replicas and CDN caches for media content.
* Partial precomputation (e.g., cache top results for frequent followers).

## Hybrid approach (practical at scale)

Most large systems use a hybrid:

* Push to followers for typical (low‑fanout) users so reads are fast for the common case.
* Pull for a small set of high‑fanout accounts (celebrities) to avoid massive write storms and storage duplication.

Why hybrid works

* Balances read latency and write throughput.
* Controls storage costs by avoiding full duplication for extreme fan‑outs.
* Lets you tune thresholds (e.g., account follower count) to decide push vs pull.

<Frame>
  <img alt="The image illustrates two data distribution methods: &#x22;Fan-out on Write,&#x22; which pre-builds feeds for instant reads but involves many writes, and &#x22;Fan-out on Read,&#x22; which performs fewer writes but may result in users waiting longer. It also mentions a hybrid approach with both push and pull methods." />
</Frame>

## Quick comparison

| Approach         |                                       Read latency | Write amplification |      Storage cost | Operational complexity                            |
| ---------------- | -------------------------------------------------: | ------------------: | ----------------: | ------------------------------------------------- |
| Fan‑out on write |                                  Low (precomputed) |  High (many writes) | High (duplicates) | High (queues, batching, idempotency)              |
| Fan‑out on read  |                                Higher (on‑the‑fly) |  Low (local writes) |               Low | Medium (parallel fetch, ranking)                  |
| Hybrid           | Low for common users; higher for celebrity content |              Medium |            Medium | Medium–High (thresholding logic + both pipelines) |

## Key considerations to discuss in an interview

* Latency: precomputed timelines minimize read latency; on‑read increases user‑perceived wait.
* Throughput & durability: large fan‑outs demand scalable, idempotent write pipelines and durable queues.
* Storage vs compute: push duplicates data (more storage); pull increases per‑read compute.
* Operational complexity: batching, queue management, backpressure controls, and incremental rebuilds help but add system complexity.
* Consistency & freshness: push gives faster visibility to followers; pull can show the absolute latest state without heavy replay.

<Callout icon="lightbulb">
  Interview tip: Describe both strategies and their trade‑offs (latency, cost, complexity). Recommend a hybrid solution and mention implementation details such as batching, message queues, rate limiting, and thresholds for offloading celebrity accounts to a pull model.
</Callout>

References and further reading

* \[System Design: Fan‑out patterns and tradeoffs] — discuss push vs pull strategies and mitigation options.
* \[Designing data pipelines at scale] — guides on queues, batching, and idempotency for high‑fanout systems.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/02240fc4-695f-4112-9594-bb05cfc5ca73/lesson/fbca447b-063f-4920-af96-99ee020edc8d" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/02240fc4-695f-4112-9594-bb05cfc5ca73/lesson/250f24b6-8363-4e27-8b26-33e6736e9a5e" />
</CardGroup>
