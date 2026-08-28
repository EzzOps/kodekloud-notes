# Back of Envelope Estimation

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Put-It-All-Together/Back-of-Envelope-Estimation/page

Guide to performing back-of-envelope capacity estimations for scalable web systems, converting user activity into RPS, storage, and component sizing with assumptions and trade-offs

Interviewers often ask a simple but revealing question: How big does this system actually need to be?

* How many servers?
* How much storage?
* What bottlenecks should you plan for?

This is a back-of-envelope estimation — a quick, reasoned approximation that demonstrates your assumptions and how you think about scale. Don’t give a single number without showing the factors that led you to it. Break large numbers into smaller pieces and explain each assumption.

Start from users and activity patterns.

Example assumptions

* Registered users: 100 million
* Daily active users (DAU): 20% → 20 million DAU
* App type: photo-sharing (reads dominate)
* Opens per active user per day: 20
* Posts per active user per day: 0.1 (one post every 10 days)

From those assumptions we compute daily totals:

* Feed reads per day = 20,000,000 × 20 = 400,000,000 reads/day
* Uploads per day = 20,000,000 × 0.1 = 2,000,000 uploads/day

Reads therefore vastly outnumber writes (\~200:1), which immediately suggests using caches, read replicas, CDNs, and object storage.

<Frame>
  <img alt="The image illustrates a server architecture diagram showing a flow from users through a load balancer to app servers, cache, database, object storage, and CDN, alongside traffic calculations involving reads and writes per day." />
</Frame>

Convert daily numbers into per-second rates — server sizing is usually driven by requests-per-second (RPS).

A day has:

```text theme={null}
24 h × 60 m × 60 s = 86,400 s (≈ 100,000 s for easier rounding)
```

Per-second estimates (exact and rounded):

| Metric            |               Exact (per second) |       Rounded (quick mental math) |
| ----------------- | -------------------------------: | --------------------------------: |
| Reads/day → r/s   | 400,000,000 / 86,400 ≈ 4,630 r/s | 400,000,000 / 100,000 = 4,000 r/s |
| Uploads/day → u/s |      2,000,000 / 86,400 ≈ 23 u/s |      2,000,000 / 100,000 = 20 u/s |

Traffic is not uniform. Peak traffic (time-of-day effects, promotions, viral events) is typically 3–5× the daily average. Always design for peak, not average.

Using the rounded average of \~4,000 r/s:

* Peak (3–5×) ≈ 12,000–20,000 r/s
* For conservatism, use peak ≈ 15,000 r/s

Uploads:

* Average uploads/sec ≈ 23 u/s
* Peak uploads/sec (3–5×) ≈ 60–120 u/s

Uploads consume more resources per request: network bandwidth, storage writes, and CPU for image processing (resizing, thumbnails, transcoding).

<Frame>
  <img alt="The image illustrates a network architecture diagram showing user interactions with a system involving a load balancer, app servers, cache, database, object storage, and CDN, alongside a traffic chart displaying 400 million reads and 2 million writes per day." />
</Frame>

Estimate storage needs.

Assume each uploaded photo averages 5 MB when you count original + compressed + resized versions. Then:

* Daily object data ingested = 2,000,000 × 5 MB = 10,000,000 MB = 10,000 GB = 10 TB/day
* Annual growth ≈ 10 TB/day × 365 ≈ 3,650 TB ≈ 3.65 PB/year

This confirms two important design decisions:

* Store image binaries in a cheap, scalable object store (S3, GCS, Azure Blob), not in the primary relational database.
* Keep only metadata (caption, owner, timestamps, storage location, indexes) in the DB — a few KB per photo.

<Frame>
  <img alt="The image shows a diagram of a system architecture involving users, a load balancer, app servers, a cache, a database, object storage, and a CDN. It also includes a calculation of storage requirements, indicating that 2 million photos each of 5 MB size taken daily would result in 10 TB of data per day over a year." />
</Frame>

Separate storage of binaries and metadata

<Frame>
  <img alt="The image depicts a system architecture diagram for a photo storage application, showing users, a load balancer, app servers, a cache, a database, object storage, and a CDN. The database only keeps metadata such as caption, timestamp, owner, and file location." />
</Frame>

Component sizing — simple assumptions and results

Assume:

* One app server can handle \~500 feed reads/sec (when reads hit cache or are efficiently served).
* Peak reads to serve = 15,000 r/s

Compute servers required:

* App servers = 15,000 / 500 = 30
* Add headroom and redundancy → plan for ≈ 40 app servers

Other sizing and considerations:

| Component               | Sizing/Need                        | Notes                                                         |
| ----------------------- | ---------------------------------- | ------------------------------------------------------------- |
| App servers             | \~30–40 (based on 500 r/s each)    | Add autoscaling, redundancy across AZs/regions                |
| Object storage          | \~10 TB/day → \~3.65 PB/year       | Use lifecycle policies (e.g., archive older images)           |
| CDN                     | Essential                          | Offload repeated downloads; reduces origin egress and latency |
| Cache (Redis/Memcached) | Required                           | Reduce hits to DB and object store for feeds                  |
| Read replicas           | Required                           | Scale reads on relational DB for metadata                     |
| Image processing        | Worker pool scaled to peak uploads | Consider asynchronous processing and queues                   |

<Frame>
  <img alt="The image shows a system architecture diagram on the left, illustrating the flow from users to various components like load balancer, app servers, database, cache, object storage, and CDN. On the right, there are notes outlining performance considerations, such as starting from users and focusing on peak rather than average metrics." />
</Frame>

Checklist: How to approach any back-of-envelope sizing question

1. Start from user counts and activity assumptions (DAU, opens/day, posts/day).
2. Separate reads from writes and compute daily totals.
3. Convert daily totals to per-second averages and then estimate peak (typically 3–5×).
4. Size compute by dividing peak RPS by throughput per server and add redundancy.
5. Size storage by item size × items/day × retention window.
6. Use caches, CDNs, read replicas, and object storage where appropriate — these are often required to meet performance and cost goals.
7. State assumptions and round aggressively in interview settings. Discuss trade-offs and system bottlenecks.

Useful references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Amazon S3 (object storage)](https://aws.amazon.com/s3/)
* [Content Delivery Networks (CDN) overview](https://en.wikipedia.org/wiki/Content_delivery_network)

<Callout icon="lightbulb">
  Round numbers and state your assumptions clearly. Interviewers are evaluating your approach and trade-offs more than any single exact number.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/7d9bce38-0967-4516-9f37-86b633ac4e22/lesson/3201dfe4-e1c7-4b53-80df-c8e08e2620aa" />
</CardGroup>
