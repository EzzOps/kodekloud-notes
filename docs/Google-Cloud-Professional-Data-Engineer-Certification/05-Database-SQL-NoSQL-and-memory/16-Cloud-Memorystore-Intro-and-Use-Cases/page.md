# Hashed prefix (3 shards)
shard-02#sensor123#2023-05-01T12:00:00Z

# Reversed timestamp (MAX_TS - timestamp)
sensor123#(9999999999 - 1682942400)
```

<Callout icon="lightbulb">
  Exam tip: Questions about avoiding hotspotting usually expect answers mentioning hashing, bucketing, or adding randomness to the row key to distribute writes.
</Callout>

<Callout icon="warning">
  Avoid using strictly increasing values (like leading timestamps) as the first part of the row key for high-write workloads—this is a common cause of hot tablets.
</Callout>

5. Denormalization for performance

* Bigtable is optimized for wide rows and single-table access. Duplicate frequently used fields (for example, sensor location or type) inside each row to avoid additional lookups or joins.
* Trade-off: higher storage costs for much faster read latency.

6. Storage efficiency and sparse columns

* Bigtable stores only columns with values; sparse columns do not consume storage for rows that lack them.
* Put optional or infrequent attributes in separate columns or families to avoid extra IO for common queries.

Principles summary table

| Principle                     | Problem solved                           | Example                                         |
| ----------------------------- | ---------------------------------------- | ----------------------------------------------- |
| Row key ordering & clustering | Efficient range scans and locality       | `sensor123#2023-05-01T12:00:00Z`                |
| Column families               | Reduce IO by grouping commonly-read data | `measurements:temperature`, `logs:system`       |
| Timestamps & versions         | Short-term history without extra rows    | Keep last 5 versions (`gc: max_versions=5`)     |
| Hotspot avoidance             | Prevent single-tablet write overload     | `shard-02#sensor123#...` or reversed timestamps |
| Denormalization               | Faster reads, fewer lookups              | Duplicate `sensor_location` in each row         |
| Sparse columns                | Save storage and IO for optional fields  | Use separate optional columns per attribute     |

Monitoring and testing

* Test with a realistic workload and monitor tablet splits, CPU, and IO in Cloud Monitoring (Stackdriver). Watch for skew in tablet sizes and request rates.
* If you see hotspots, try introducing hashing or additional shards and re-evaluate read patterns.

Links and references

* [Bigtable Overview](https://cloud.google.com/bigtable/docs)
* [Designing schemas in Cloud Bigtable](https://cloud.google.com/bigtable/docs/schema-design)
* [Cloud Monitoring for Bigtable](https://cloud.google.com/bigtable/docs/monitoring)

Summary
Row key design is the single most important Bigtable schema decision. The right pattern depends on access patterns (point lookups vs. range scans), write volume, retention requirements, and whether you need to prioritize read locality or write distribution. Use these six principles as a checklist: order keys for locality, group columns sensibly, use timestamps and GC settings, avoid hotspotting with bucketing or hashing, denormalize for performance, and exploit sparse columns to save space.

<Frame>
  <img alt="An infographic titled &#x22;6 Core Principles&#x22; for BigTable schema design with a large blue &#x22;6&#x22; and brief introductory text on the left. Six numbered panels on the right list principles like row key design, column families, timestamp usage, avoiding hotspots, denormalization, and sparse columns with short explanations." />
</Frame>

That concludes this lesson. A concise Bigtable summary that ties these concepts together will follow.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/d6495f69-f5ae-451e-a9b3-f57c31ce1fa4" />
</CardGroup>


# Cloud Memorystore Intro and Use Cases

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Cloud-Memorystore-Intro-and-Use-Cases/page

Overview of Google Cloud Memorystore, caching benefits, Redis versus Memcached tradeoffs, cache-aside patterns, TTL and invalidation guidance to improve read latency and reduce database load.

Welcome back. In this lesson we’ll explore Google Cloud Memorystore — a managed, in-memory caching service designed to accelerate read-heavy workloads and reduce load on durable databases. Memorystore is ideal when you need extremely low-latency access to frequently read data that doesn’t need to go to long-term, persistent storage every time.

Why caching? Firestore and Cloud SQL provide durable, long-term storage and strong persistence guarantees. However, many applications repeatedly read the same data (e.g., session data, product metadata, leaderboards). Hitting the durable database on every request increases latency and load. Introducing an in-memory cache like Cloud Memorystore lets you keep “hot” data in RAM for microsecond-to-millisecond access.

Example scenario:

* A service queries Cloud SQL on each user request for product info.
* Repeated requests for the same product create unnecessary database load and higher latency.
* Add Cloud Memorystore as a cache layer: the service checks the cache first, falling back to Cloud SQL only on cache misses.

A typical cache-aside flow:

* The service asks the cache (Cloud Memorystore) for a value.
* If the value exists (cache hit), return it immediately.
* On a cache miss, load from Cloud SQL, return to the client, and write the value into the cache for future requests.

<Frame>
  <img alt="An infographic titled &#x22;Memorystore – Introduction&#x22; showing a comparison between direct client-to-Cloud SQL calls and an architecture that inserts Cloud Memorystore as a caching layer between the client and Cloud SQL. It notes that caching can reduce database calls and speed up data access." />
</Frame>

This cache layer typically stores a subset of your data — the hot keys — and drastically improves read latency while reducing I/O and CPU load on your primary DB.

<Callout icon="lightbulb">
  A common and safe pattern is cache-aside (lazy loading): check the cache first; on a miss, load from the database and populate the cache. Alternative patterns include write-through, write-behind, and read-through — choose based on your consistency and performance requirements.
</Callout>

Memorystore supports two managed engines:

* Memorystore for Redis
* Memorystore for Memcached

Key differences and when to choose each:

| Feature                   | Memorystore for Redis                                                                                                        | Memorystore for Memcached                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Persistence & replication | Supports replication, replicas, and optional persistence depending on configuration; managed HA with failover                | Pure in-memory; no built-in persistence or automatic replication                                  |
| Use-case fit              | Real-time applications requiring richer data structures or stronger availability (sessions, leaderboards, counters, streams) | Simple, transient caching (page fragments, CDN-like object caches) where cache loss is acceptable |
| Features                  | Rich data types (lists, sets, sorted sets), pub/sub, Lua scripts, transactions, clustering                                   | Lightweight key-value store; simple operations and horizontal scaling by adding nodes             |
| Complexity & cost         | More features, typically higher cost for HA setups                                                                           | Simpler and usually cheaper                                                                       |

In practice, teams often pick Redis for production workloads that need durability, advanced data structures, and HA. Memcached works well when your primary goal is a low-cost, simple cache.

<Frame>
  <img alt="A presentation slide titled &#x22;Memorystore – Introduction&#x22; showing a comparison table between Memorystore for Redis and Memorystore for Memcached. The table contrasts data persistence/replication, use-case fit (durable real-time apps vs simple caching), and complexity/scalability with price notes." />
</Frame>

Practical caching considerations

* Eviction policy & TTL: Choose eviction policies (LRU, TTL) and time-to-live values that reflect how stale data can be.
* Cache invalidation: On writes, invalidate or update related cache keys to avoid serving stale data.
* Warm-up strategies: Preload caches or use gradual ramp-up to avoid a cold-cache spike.
* Monitoring: Track hit rate, miss rate, latency, and eviction events to tune sizing and autoscaling.
* Security & networking: Use VPCs, authorized networks, and IAM to restrict access to Memorystore instances.

Recommended cache-aside patterns (examples)

Python (cache-aside using redis-py):

```python theme={null}
import redis
import psycopg2
import json

r = redis.Redis(host="10.0.0.5", port=6379, db=0)
conn = psycopg2.connect(...)

def get_product(product_id):
    key = f"product:{product_id}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)        # cache hit

    # cache miss: load from DB
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, price FROM products WHERE id = %s", (product_id,))
        row = cur.fetchone()
    if row:
        product = {"id": row[0], "name": row[1], "price": row[2]}
        r.set(key, json.dumps(product), ex=3600)  # populate cache with TTL
        return product
    return None
```

Node.js (cache-aside using ioredis):

```javascript theme={null}
const Redis = require("ioredis");
const { Pool } = require("pg");
const redis = new Redis({ host: "10.0.0.5", port: 6379 });
const pool = new Pool(/* db config */);

async function getProduct(productId) {
  const key = `product:${productId}`;
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached); // cache hit

  const res = await pool.query("SELECT id, name, price FROM products WHERE id = $1", [productId]);
  if (res.rowCount) {
    const product = res.rows[0];
    await redis.set(key, JSON.stringify(product), "EX", 3600); // set TTL
    return product;
  }
  return null;
}
```

<Callout icon="warning">
  Be careful with cache invalidation. Incorrect invalidation can lead to stale reads. Decide whether your application tolerates eventual consistency or requires strict consistency, then design cache write/update flows accordingly.
</Callout>

Summary

* Use Cloud Memorystore to dramatically reduce latency for repeated reads and to offload traffic from Cloud SQL or Firestore.
* Choose Memorystore for Redis when you need durability, HA, and advanced data structures.
* Choose Memorystore for Memcached for simple, cost-effective, transient caches.
* Implement a cache strategy (cache-aside, write-through, etc.), set TTLs/eviction policies, and monitor hit rates to tune performance.

Links and references

* [Cloud Memorystore documentation](https://cloud.google.com/memorystore)
* [Redis documentation](https://redis.io/documentation)
* [Memcached documentation](https://memcached.org)
* [Cloud SQL documentation](https://cloud.google.com/sql)
* [Google Cloud best practices for caching](https://cloud.google.com/architecture/best-practices-for-caching)

Thanks for reading — that concludes this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/0caf213e-64c8-4836-b5e7-05cdd2e7247c" />
</CardGroup>
