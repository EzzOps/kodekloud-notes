# Designing a Caching System

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/System-Design/Designing-a-Caching-System/page

Guide to designing a robust caching layer for user profile services, covering cache-aside, staleness mitigation, TTL and invalidation, single-flight, jitter, replication, and operational best practices.

This guide walks through designing a robust caching layer for a backend that serves user profiles. The user journey is straightforward: a client requests a profile (for example, `Alan1`). The backend first consults the cache; on a hit it returns cached data, on a miss it reads the database, populates the cache, and returns the result. We’ll build that flow step-by-step and show where it breaks and how to harden it.

Version one — naive approach

When a request asks for a user profile (e.g., `Alan1`), the application follows the cache-aside pattern:

* Check cache.
* If present (cache hit) → return cached value.
* If absent (cache miss) → read from DB, write result to cache, and return to client.

This is simple and fast for read-heavy workloads but has correctness and operational pitfalls.

<Frame>
  <img alt="The image depicts a flow diagram showing a &#x22;naive&#x22; caching strategy with Redis, where data is served from the cache to users, bypassing the database." />
</Frame>

Cache staleness: a correctness problem

A major correctness issue with the naive approach is staleness. If `Alan1` updates their username to `Alan4` in the database, the DB contains the fresh value but the cache still holds the old `Alan1`. Unless the application explicitly updates or evicts the cache entry during the write, clients will continue to see stale data.

<Frame>
  <img alt="The image illustrates a data flow issue where a backend app retrieves incorrect data from Redis while the correct data exists in the database, leading to a stale state." />
</Frame>

Version two — TTL and invalidation

Common mitigations:

* TTL (time-to-live): add expiration to cache entries so stale values are eventually evicted. For example, set a 5-minute TTL per profile key.
* Active invalidation: when the database is updated, explicitly evict (or update) the corresponding cache entry.
* Ordering: for the cache-aside pattern, a safe approach is to commit the DB write and then invalidate the cache (or populate the cache after the DB transaction commits). Other variants include write-through and write-back caches, each with different trade-offs.

Example cache-aside pseudocode:

```pseudo theme={null}
// Read path
value = cache.get(key)
if value == nil:
    value = db.read(key)
    cache.set(key, value, ttl)
return value

// Write path (safe ordering)
db.write(key, newValue)
cache.del(key)  // or cache.set(key, newValue)
```

Notes on alternative strategies:

* Write-through: writes go to cache first and synchronously to DB; simplifies reads but increases write latency.
* Write-back: writes are buffered in cache and flushed to DB later; can improve write throughput but risks data loss on failures.

Version two helps, but fixed TTLs alone (e.g., exactly five minutes) can still expose users to stale data and can create synchronized expiration spikes. Combine TTL + invalidation for better freshness.

Version three — cache miss storm (cache stampede)

When a very hot key receives heavy traffic, a single expiration or eviction can cause a large number of clients to miss the cache simultaneously. This “stampede” floods the database with read requests and can overwhelm it.

Mitigations to prevent cache stampedes:

1. Single-flight / Request coalescing

* Ensure that when multiple concurrent requests miss the same key, only one request queries the database and populates the cache; other requests wait and then read the cached value.
* In single-process systems, in-memory synchronization (e.g., mutexes) is sufficient. In distributed systems, use short-lived per-key locks in Redis, a coordination service, or a distributed single-flight implementation.

<Callout icon="lightbulb">
  Use single-flight/coalescing so concurrent cache misses for the same key result in a single database load.
</Callout>

<Frame>
  <img alt="The image is a diagram illustrating a system architecture using Redis as a cache between a backend application and a database, showing how requests are managed to prevent cache misses." />
</Frame>

Simple single-flight pseudocode (conceptual):

```pseudo theme={null}
if cache.get(key) == nil:
    lock = acquire_distributed_lock(key)
    if lock.acquired:
        value = db.read(key)
        cache.set(key, value, ttl)
        release(lock)
    else:
        wait_for_cache_fill_or_lock_release()
return cache.get(key)
```

2. TTL jitter

* Add a small random offset to TTLs so keys do not all expire at the exact same time. This smooths expiration and reduces synchronized load spikes.

<Frame>
  <img alt="The image is a diagram showing a Redis implementation with various keys and their time-to-live (TTL) values set to 5:00. It illustrates the concept of adding random seconds to each TTL value." />
</Frame>

3. Replication for extremely hot keys

* When a single key’s read volume exceeds what one cache node can serve, replicate that object across multiple cache nodes (read replicas) so multiple nodes can serve reads for the same key.
* Sharding distributes keys across nodes but does not split one key; replication or read-multiplexing increases aggregate read capacity for extremely popular objects.

Summary of techniques

| Technique           |                      What it does | Pros                               | Cons                                                       | When to use                               |
| ------------------- | --------------------------------: | ---------------------------------- | ---------------------------------------------------------- | ----------------------------------------- |
| TTL                 |         Evicts entries after time | Simple, reduces stale window       | Fixed TTLs can be too long or synchronized                 | Use when eventual freshness is acceptable |
| Active invalidation |   Evict/update cache on DB writes | Keeps cache fresh immediately      | Requires correct ordering and extra complexity             | Use for high-freshness data               |
| Single-flight       |  Coalesce concurrent cache misses | Prevents DB overload during misses | Requires cross-process coordination in distributed systems | Use for hot keys with bursty traffic      |
| TTL jitter          |             Randomize expirations | Smooths load spikes                | Adds complexity to TTL management                          | Use for many keys with similar TTLs       |
| Replication         | Copy hot keys to many cache nodes | Increases read throughput          | More memory and replication overhead                       | Use for extremely popular objects         |

Final guidance and warnings

* Combine techniques: TTL + invalidation + single-flight + jitter + replication as appropriate for your workload.
* Measure and tune TTLs, lock durations, and replication strategies based on traffic patterns, read/write ratios, and acceptable staleness.
* Test failure scenarios (network partitions, cache evictions, DB latency spikes) to validate that cascading failure is contained.

<Callout icon="warning">
  Be careful: caching introduces complexity — staleness, invalidation, race conditions, and potential for cache stampedes. Combine TTL, invalidation, single-flight, TTL jitter, and replication as appropriate to balance freshness, latency, and system resilience.
</Callout>

Links and references

* Cache-aside pattern: [https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
* Singleflight (Go): [https://pkg.go.dev/golang.org/x/sync/singleflight](https://pkg.go.dev/golang.org/x/sync/singleflight)
* Redis docs: [https://redis.io/](https://redis.io/)
* Write-through vs write-back: [https://en.wikipedia.org/wiki/Write-through\_cache](https://en.wikipedia.org/wiki/Write-through_cache) and [https://en.wikipedia.org/wiki/Write-back\_cache](https://en.wikipedia.org/wiki/Write-back_cache)
* TTL / Time to live: [https://en.wikipedia.org/wiki/Time\_to\_live\_(networking)](https://en.wikipedia.org/wiki/Time_to_live_\(networking\))
* Jitter and backoff guidance: [https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/ef53ec43-96e9-4d1b-8a6e-e6eb97b0d0dc/lesson/bcc983fc-45fb-41f5-8a9f-4a73893294f0" />
</CardGroup>
