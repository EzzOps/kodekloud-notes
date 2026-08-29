# Elasticache Overview

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/Elasticache-Overview/page

Overview of Amazon ElastiCache, in-memory caching benefits, use cases, and guidance on choosing Redis or Memcached for performance, durability, and scalability.

This lesson explains Amazon ElastiCache and how in-memory caching improves application performance and scalability. You’ll learn common caching patterns, typical use cases (like database caching and session stores), and how to choose between Redis and Memcached for your workloads.

First, consider an application that relies only on a disk-backed database with no caching. Every user request produces a database query, increasing disk I/O and latency as traffic grows. As read volume rises, the database becomes a bottleneck and overall response times suffer.

<Frame>
  <img alt="A slide titled &#x22;ElastiCache&#x22; showing four colored tiles with icons labeled: High Load, Disk-Based Storage, Performance Impact, and Scalability Issues." />
</Frame>

Caching solves these problems by storing frequently accessed or transient data in fast, in-memory stores. When you offload read-heavy traffic to a cache you:

* Reduce the number of database reads
* Decrease latency for end users
* Improve application responsiveness and scalability

Cache lookup follows a simple pattern: check the cache first, then fall back to the database on misses.

<Frame>
  <img alt="A simple ElastiCache architecture diagram showing a client using an e-commerce website that queries a cache (with &#x22;Cache Hit&#x22; and &#x22;Cache Miss&#x22; paths) and falls back to a database. The flow arrows illustrate requests between client, website, cache, and database." />
</Frame>

Cache lookup pattern (high level):

1. Application queries the cache.
2. If the data exists (cache hit) — return it immediately.
3. If the data does not exist (cache miss) — query the database, return the result, and optionally store it back in the cache.

Example: simple cache-get pseudo-code (Node.js style)

```js theme={null}
// Pseudocode: cache-first lookup
async function getUserProfile(userId) {
  const cached = await cache.get(`user:${userId}`);
  if (cached) {
    return JSON.parse(cached); // cache hit
  }
  const profile = await db.queryUser(userId); // cache miss -> DB
  if (profile) {
    await cache.set(`user:${userId}`, JSON.stringify(profile), { ttl: 3600 });
  }
  return profile;
}
```

Caching is also ideal for session stores: storing short-lived session state (login tokens, shopping cart) in-memory is faster and simpler than persisting that data to disk.

<Frame>
  <img alt="An ElastiCache infographic showing two use cases: &#x22;Database Caching&#x22; on the left (to decrease read-heavy database loads) and &#x22;Session Store&#x22; on the right (to manage session information for web applications)." />
</Frame>

Amazon ElastiCache is AWS’s managed in-memory caching service. Key benefits include:

* Managed provisioning, engine and OS patching, and monitoring
* Built-in failure recovery and automated maintenance operations
* Support for Redis and Memcached as drop-in engines
* Backup/restore for Redis (Memcached is ephemeral)
* Scaling options (scale out/in via clusters or scale up/down instance types)
* High availability features (Multi-AZ replication and automatic failover for Redis depending on configuration)

When choosing between Redis and Memcached, consider the following differences. Use this to map engine capabilities to your application requirements (durability, data structures, replication, etc.).

<Frame>
  <img alt="A slide titled &#x22;ElastiCache&#x22; showing a two-column comparison of Redis (left) and Memcached (right) with rows listing differences such as data structures, persistence, replication/failover, Multi-AZ support, backups, partitioning, and threading." />
</Frame>

Feature comparison (high-level)

| Feature                  | Redis                                                                          | Memcached                                                    |
| ------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| Data model               | Rich data types (strings, hashes, lists, sets, sorted sets)                    | Simple key-value                                             |
| Persistence              | Optional persistence; ElastiCache supports snapshots/backups                   | No persistence; data is ephemeral                            |
| Replication and failover | Built-in replication, Multi-AZ, and automatic failover for replication groups  | No built-in replication or automatic failover                |
| Backups                  | Snapshot and restore supported                                                 | No backups                                                   |
| Partitioning / sharding  | Cluster mode provides sharding                                                 | Client-side partitioning; lacks centralized cluster sharding |
| Concurrency              | Single-threaded per shard/process (good for atomic ops and complex data types) | Multi-threaded (can use multiple CPU cores)                  |

When to choose Redis vs. Memcached

* Choose Redis if you need:
  * Advanced data structures (lists, sets, sorted sets, hashes)
  * Persistence or backup/restore capabilities
  * Built-in replication, automatic failover, and Multi-AZ high availability
  * Atomic operations and server-side scripting (Lua)

* Choose Memcached if you need:
  * A simple high-throughput, ephemeral cache
  * Multi-threaded performance to utilize multiple CPU cores
  * Lightweight key-value caching without persistence or replication concerns

> **lightbulb** Redis is a better fit when you need advanced data structures, durability, replication, or backups. Memcached can be preferable for simple, high-performance ephemeral caching where multi-threaded CPU utilization matters.

Summary

* Amazon ElastiCache is a fully managed, in-memory caching service that supports Redis and Memcached.
* Use caching to reduce database load, lower latency, and improve application scalability.
* Select Redis for durability and complex data structures; select Memcached for simple, high-throughput ephemeral caches.

Links and references

* [Amazon ElastiCache documentation](https://docs.aws.amazon.com/elasticache/)
* [Redis](https://redis.io/)
* [Memcached](https://memcached.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/e70d44d3-2460-4344-8cc8-6b82e9be84e4)
