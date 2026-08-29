# What is System Design Actually

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/What-is-System-Design-Actually/page

Explains system design principles for scaling web applications, identifying failure modes and pragmatic mitigations like load balancers, caching, replication, and operational trade-offs.

When you survey the technology landscape you’ll see many tools: databases, caches, CDNs, load balancers, servers, and more. Those tools are means to an end — the real goal is to solve a concrete problem. For example: build an application that lets users upload and share photos.

System design is the craft of selecting the right components and placing them so the whole system solves the problem reliably, with acceptable cost and complexity. It’s not about memorizing diagrams; it’s about reasoning through trade-offs and failure modes.

As you progress from junior to senior roles, your responsibilities in system design change:

* Junior engineers implement a specified feature: inputs and expected outputs are clear.
* Mid-to-senior engineers are given a problem and must design an approach and integrate it into an existing system.
* Senior engineers define the overall architecture, make systemic choices about reliability, scalability, and operational costs.

<Frame>
  <img alt="The image illustrates a progression from junior to mid-senior roles in a tech workflow, showing a system architecture with components like servers and databases. It highlights that a junior builds one feature, while a mid-senior finds the approach." />
</Frame>

This article is written to help you think like a mid-senior or senior engineer: spot trade-offs, anticipate failure modes, and choose appropriate mitigations.

<Frame>
  <img alt="The image illustrates the progression from a junior to a senior engineer, highlighting their roles: a junior builds one feature, a mid-senior finds the approach, and a senior designs the whole system. It also includes a diagram of a system architecture workflow and suggests a course to &#x22;Think Like Senior Engineers.&#x22;" />
</Frame>

The best way to learn is by watching a system get designed and by observing how components fail and are fixed. We’ll work through a simple example and progressively handle the problems that arise.

Start simple: write the app and rent one server for a low monthly price. If you’re unsure what a server is — it’s just a computer in a data center whose job is to answer your visitors’ requests. In the simplest deployment you put everything on that server: the web app, the database, and uploaded photos.

Here’s a minimal upload handler:

```javascript theme={null}
// people upload & share photos
app.post('/upload', (req, res) => {
    savePhoto(req.file)
    db.insert(req.file.meta)
    res.sendStatus(201)
})
```

This single-server setup is easy to build and operate. Debugging usually involves looking at one machine. For many applications, starting this way is the right choice: simple, low cost, and fast to iterate.

Now imagine your app is featured on a popular site and ten thousand people visit in one business day. One server may not cope — or the site becomes painfully slow. Let’s examine concrete failure modes and common mitigations. Each failure has a name and a standard fix; that collection of fixes forms the core of system design.

<Frame>
  <img alt="The image illustrates a scenario where an app gains 10,000 users at once, causing slow performance due to server load, as indicated by a line connecting users, a phone, a server, and a database. The diagram highlights that the experience is &#x22;painfully slow&#x22; with visual and textual indicators of high server load." />
</Frame>

Failure #1 — CPU and memory exhaustion:

* Symptom: pages that loaded in 200 ms now take 10 seconds. The single server is doing CPU-heavy work (image processing, rendering) and many concurrent DB queries.
* Direct fix: add more servers and distribute requests across them.
* New requirement: you now need a traffic director (a load balancer) to route incoming HTTP requests across multiple servers.

<Frame>
  <img alt="The image illustrates a scenario of server failure due to CPU and RAM overload, involving over 10,000 users accessing a server and database setup. It shows indicators for CPU and RAM usage and a flow of data between users, servers, and a database." />
</Frame>

Failure #2 — database overload:

* Symptom: many users request the same trending photos or popular profiles; repeated identical queries make the DB a bottleneck.
* Common fix: add a cache layer (for example, an in-memory cache like Redis or Memcached) so popular results are served from fast memory instead of hitting the DB on every request.
* Placement: caches sit between application servers and the database and reduce both latency and DB load.

<Frame>
  <img alt="The image illustrates a database overload scenario caused by 10,000+ users accessing a popular profile, leading to repeated queries on the database through load balancers and servers." />
</Frame>

Failure #3 — hardware or machine failure (single point of failure):

* Symptom: a disk fails, power supply dies, or an operator accidentally unplugs a cable. If everything lives on one machine, the app is down and data can be lost.
* Fixes:
  * Replicate the database: add read replicas and implement backups.
  * Move large binary files (photos) to durable object storage such as `Amazon S3`, which stores objects redundantly across Availability Zones and can optionally replicate across regions for geographic redundancy.

<Frame>
  <img alt="The image illustrates a system architecture for handling over 10,000 users, featuring a load balancer, multiple servers, a database with a replica, cache, and S3 storage." />
</Frame>

Notice something important: we didn’t need to rewrite the application logic. The upload handler code remains the same:

```javascript theme={null}
// people upload & share photos
app.post('/upload', (req, res) => {
    savePhoto(req.file)
    db.insert(req.file.meta)
    res.sendStatus(201)
})
```

What changed is where each responsibility runs and how we route work. That is the heart of system design: deciding where components live and understanding the trade-offs those decisions introduce.

Every fix introduces new problems. Examples:

* Load balancer availability: the load balancer itself can become a single point of failure — make it highly available.
* Cache correctness: caches can serve stale data — you must define cache invalidation strategies and TTLs.
* Replica lag: read-replicas can be behind the primary — plan for eventual consistency and stale reads.

Summary table — common failure modes and standard mitigations:

| Failure Mode             | Root Cause                                          | Typical Mitigation                                                              |
| ------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------- |
| Server CPU/RAM overload  | Too much compute or concurrency on a single machine | Add servers + load balancer; horizontally scale stateless services              |
| Database overload        | High read/write volume or expensive queries         | Introduce caching (`Redis`), add read replicas, optimize queries                |
| Single point of failure  | Everything on one machine                           | Replicate data, use durable object storage (e.g., `Amazon S3`), add redundancy  |
| Stale data / consistency | Caching or replication introduces outdated reads    | Use TTLs, eviction/invalidation strategies, and design for eventual consistency |
| Operational complexity   | More components to manage                           | Automate deployments, monitoring, and alerting; weigh cost vs. benefit          |

<Callout icon="lightbulb">
  System design is iterative: fix a bottleneck, observe new failure modes, and choose the next mitigation by balancing correctness, latency, cost, and operational complexity. Start simple, measure, and evolve the architecture as real load and failure patterns emerge.
</Callout>

You don’t learn system design by memorizing diagrams; you learn by observing components fail, reasoning about trade-offs, and making pragmatic choices. When someone asks how you’d scale an app, aim to describe a logical approach: identify bottlenecks, choose mitigations, and balance correctness, cost, and complexity rather than reciting a single static diagram.

Links and references:

* [Amazon S3](https://aws.amazon.com/s3/)
* [Load Balancing Concepts (AWS)](https://aws.amazon.com/elasticloadbalancing/)
* [Redis](https://redis.io/) — common in-memory cache for reducing DB load
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — for container orchestration and scaling guidance

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/545248b6-7716-4243-b96a-6ee23c1c4348" />
</CardGroup>
