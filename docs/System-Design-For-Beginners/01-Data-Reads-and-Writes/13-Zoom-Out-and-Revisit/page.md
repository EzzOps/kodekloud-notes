# Zoom Out and Revisit

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Zoom-Out-and-Revisit/page

Overview of a photo app system architecture detailing stateless servers, load balancing, Redis sessions and cache, Postgres primary with read replicas, MongoDB, and scaling and operational strategies

Let's zoom out and revisit the photo-app architecture we've built so far. This overview shows how incoming requests flow, where state is stored, and how we scale reads and writes to meet production traffic.

When a user opens the photo app, the request first hits the load balancer. The load balancer forwards the request to one of our stateless application servers (we currently run 10). Because the application servers are stateless, any server can handle any user request, which simplifies scaling and failover.

Request flow (high level):

* Client → Load Balancer → Stateless App Server → Cache → Database(s)

Session management

* All user login sessions are stored centrally in Redis. Centralized sessions let any app server authenticate a user without sticky sessions, enabling seamless scaling and server replacement.

<Callout icon="lightbulb">
  Store sessions in a dedicated Redis cluster configured with persistence (RDB/AOF), eviction policies, and clustering to avoid session loss and bottlenecks. For very high security requirements, couple Redis session data with short TTLs and server-side session validation.
</Callout>

Caching strategies

* For frequently accessed (“hot”) data—trending photos, popular profiles, or feed fragments—the application checks the cache (Redis or a dedicated cache layer) before querying the primary database.
* Cache synchronization with Postgres uses TTLs and explicit invalidation when data changes. Common patterns:
  * Write-through: write to cache and DB synchronously for strong consistency.
  * Write-back: write to cache first and flush to DB later for high write throughput.
  * Explicit invalidation: update DB then delete/refresh cache on change.

Note: Cache invalidation is one of the hardest problems in distributed systems—choose a pattern based on consistency vs. latency trade-offs.

Primary and read-scale database (Postgres)

* Structured entities—users, photos, likes, comments, follows—are stored in Postgres with indexed columns for common queries.
* To scale read throughput, we run one primary that accepts all writes and two read replicas for read traffic. A read load balancer distributes queries to replicas (and optionally the primary).

<Callout icon="warning">
  Read replicas often replicate asynchronously. Expect replication lag: reads served from replicas may be eventually consistent. Design UX and critical reads to tolerate or avoid stale data (e.g., read-your-writes scenarios).
</Callout>

Additional data stores

* MongoDB (NoSQL) holds unstructured or semi-structured data such as user preferences, activity streams, and behavioral events where flexible schemas are helpful.
* If dataset size grows beyond a single instance’s capacity, use sharding/partitioning to split data across machines and scale horizontally.

Operational considerations

* Configure Redis for persistence and clustering; tune eviction policies for session vs. cache data.
* Monitor replica lag, index usage, and cache hit rates.
* Automate backups and test failover procedures regularly.

Component responsibilities (quick reference)

| Component               | Role                                | Examples / Notes                                 |
| ----------------------- | ----------------------------------- | ------------------------------------------------ |
| Load balancer           | Distributes incoming traffic        | Layer 4/7 LB, health checks, connection draining |
| App servers (stateless) | Handle requests, business logic     | Auto-scale, no local session state               |
| Session store           | Centralized session management      | `Redis` (clustered, persistent, TTLs)            |
| Cache                   | Fast reads for hot data             | `Redis`, TTLs, invalidation strategies           |
| Primary DB              | Canonical structured data           | `Postgres` (writes go here, indexed)             |
| Read replicas           | Read scaling                        | `Postgres` replicas, monitor replication lag     |
| NoSQL store             | Unstructured/semi-structured data   | `MongoDB` for events, preferences                |
| Sharding/partitioning   | Horizontal scale for large datasets | Apply to Postgres or NoSQL as needed             |

References and links

* Redis: [https://redis.io/](https://redis.io/)
* Postgres: [https://www.postgresql.org/](https://www.postgresql.org/)
* MongoDB: [https://www.mongodb.com/](https://www.mongodb.com/)

If the dataset grows beyond what a single database instance can hold, we can partition the data using sharding to split it across multiple database machines.

<Frame>
  <img alt="The image is a diagram of a server architecture featuring a user interacting with a stateless server setup through a load balancer, with caching, session management, and data storage systems using Postgres and MongoDB." />
</Frame>

This diagram summarizes the complete design so far. As requirements evolve—higher throughput, lower latency, stronger consistency guarantees—we will add components and apply optimizations such as CDN edge caching, async job queues, rate limiting, and more advanced database partitioning.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/7bb42e92-567c-4e82-ba3a-1b74d9d70ea7" />
</CardGroup>
