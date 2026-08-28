# Repeat the same request; this may be served from cache
controlplane ~ on ☁️ (us-east-1) ➔ curl localhost:8000/profile/7
{"id": 7, "bio": "Original bio for user 7."}

# Inspect recent application logs
controlplane ~ on ☁️ (us-east-1) ➔ docker compose logs app | tail -2
# (example log lines)
app_1  | INFO  cache: hit for profile 7
app_1  | INFO  response served from cache
```

<Callout icon="lightbulb">
  This lesson demonstrates the cache-aside pattern: on a cache miss the application reads from the database and populates Redis; on a cache hit it serves data directly from Redis. If the database is updated without invalidating or updating the cache, the application may continue to serve stale data until the cache entry expires or is refreshed.
</Callout>

## What you'll observe

* Baseline: requests read directly from the database (no Redis), with typical latency.
* After adding Redis: first request for an item populates the cache (cache miss → DB read); subsequent requests for the same item are served from Redis (cache hit), reducing latency.
* Stale data scenario: if you update the database directly without invalidating the Redis entry, the application may return the old value until the cached key expires or is explicitly refreshed/invalidated.

## Quick commands and examples

| Action                | Command / Example                              | Notes                                            |
| --------------------- | ---------------------------------------------- | ------------------------------------------------ |
| Request profile       | `curl localhost:8000/profile/7`                | Hits app endpoint that uses cache-aside logic    |
| Repeat request        | `curl localhost:8000/profile/7`                | Likely a cache hit on subsequent call            |
| View app logs         | `docker compose logs app \| tail -2`           | Look for `cache: hit` or `cache: miss` lines     |
| Example JSON response | `{"id": 7, "bio": "Original bio for user 7."}` | Response format returned by the profile endpoint |

## How the cache-aside pattern works (summary)

1. Application receives a request for resource X.
2. Check Redis for key X:
   * If present (cache hit): deserialize and return to client.
   * If absent (cache miss): read X from the database, return to client, and write X into Redis (optionally with a TTL).
3. If the database is modified by another process, the cache must be invalidated or updated to avoid serving stale data. Common strategies are: write-through, write-behind, explicit invalidation, or short TTLs.

## Debugging tips

* Look for log lines indicating cache behavior, e.g. `cache: hit for profile 7` or `cache: miss for profile 7`.
* When debugging stale reads:
  * Verify if the database row actually changed.
  * Check whether the Redis key still exists and contains the old value.
  * Confirm whether your application invalidates cache keys on updates.
* Use Redis CLI to inspect keys: `redis-cli GET profile:7` (or the key format your app uses).

## Common invalidation strategies

| Strategy                  | Description                                                     | When to use                                              |
| ------------------------- | --------------------------------------------------------------- | -------------------------------------------------------- |
| Explicit invalidation     | On DB update, delete or update the corresponding cache key      | Works when all writes go through the application         |
| Short TTL                 | Set a short expiration on cache entries                         | Useful if occasional staleness is acceptable             |
| Write-through             | Write to cache and DB synchronously on updates                  | Ensures cache is up-to-date but adds write latency       |
| Event-driven invalidation | Use messaging or change data capture to invalidate/update cache | Scales when multiple services or processes modify the DB |

## References and further reading

* [Redis documentation](https://redis.io/documentation)
* [Cache-aside pattern overview (Martin Fowler)](https://martinfowler.com/bliki/CacheAside.html)
* \[Designing Data-Intensive Applications (Book) — caching patterns]

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/1282acaf-ea40-49df-a44a-df97a78d22ac" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/f85b3eb5-e4cc-4bf6-83a6-e89fae919f4f" />
</CardGroup>


# Cache Invalidation TTLs

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Cache-Invalidation-TTLs/page

Strategies for keeping caches consistent with databases, comparing TTL expiration and active invalidation plus mitigations for stampedes and race conditions

When you add a cache in front of your database, you get faster reads and reduced DB load — but you also introduce a consistency problem. The database is the canonical source of truth; the cache holds a copy. If those copies diverge, users can see stale data. For example, if Lionel Messi updates his bio in the database but the cache still serves the old bio, the system is correct at the DB level but wrong at the user-visible layer.

<Callout icon="lightbulb">
  Define how much staleness your application can tolerate before choosing an invalidation strategy. Measure the acceptable staleness window and use it to guide whether you need TTLs, active invalidation, or a hybrid approach.
</Callout>

There are two common strategies to keep cache and database consistent:

* TTL (time to live): let cached items expire automatically.
* Active invalidation: explicitly remove or update cache entries on database writes.

Below we explain both, when to use them, and common mitigations for their pitfalls.

## TTL (time to live)

TTL means writing items into the cache with an expiry time. Example: set a user bio in Redis with a 60-second TTL. When the TTL expires, Redis evicts the entry; the next request misses the cache, fetches the latest data from the database, and repopulates the cache.

TTL is a lazy approach: it trades eventual consistency for simplicity and scalability. It’s a good fit when short periods of staleness are acceptable (e.g., follower counts, trending metrics). But if your application cannot tolerate even a second of stale data (e.g., privacy settings), TTL alone is insufficient.

<Frame>
  <img alt="The image illustrates a system design using a Time to Live (TTL) cache mechanism, showing data flow between an app, Redis cache, and a database, with old and new bio information." />
</Frame>

### Cache stampede (thundering herd)

A common TTL-related failure mode is the cache stampede: when a very popular cache key expires, many clients request it simultaneously, causing a surge of identical DB queries. This can overload your database.

<Frame>
  <img alt="The image is a diagram illustrating a cache stampede scenario in a system involving an app, Redis cache, and a database, depicting the flow of photo requests from a user." />
</Frame>

Mitigations for stampedes and TTL issues:

* Add jitter to TTLs so hot keys don’t all expire at the same instant.
* Request coalescing / single-flight: ensure only one in-flight DB fetch repopulates the cache for a given key.
* Per-key mutexes or locks to serialize refreshes.
* Background refresh (prefetching) for known hot keys.
* Serve a slightly stale value while refreshing asynchronously (stale-while-revalidate).

<Frame>
  <img alt="The image illustrates a data flow process using &#x22;TTL, Time to Live&#x22; with an app accessing data through Redis cache and a database, showing elements like follower count and bio update times." />
</Frame>

## Active invalidation

Active invalidation means the application updates or deletes the cached copy as part of the write flow. Typical pattern: write the new value to the DB, then delete or update the corresponding cache entry so future reads fetch fresh data. This approach minimizes the staleness window and is required when correctness is critical.

However, active invalidation can be tricky because of races. For example, a read may occur between the DB write and the cache delete, potentially repopulating the cache with the old value.

Common strategies to make active invalidation safer:

* Double-delete: delete the cache before and after writing to the DB (or delete after DB write and repeat shortly after).
* Write-through / write-behind: write the value to the cache as part of the DB update so the cache holds the new value immediately.
* Versioned keys or optimistic concurrency: include a version or timestamp in cache keys/values so readers can detect stale entries.
* Distributed locks or single-flight: serialize cache refreshes to avoid races.

<Callout icon="warning">
  If you invalidate the cache in the wrong order relative to the DB write, you risk serving stale entries. Design your write+invalidate ordering carefully and consider extra safeguards (double-delete, versioning, or locking) to guarantee correctness.
</Callout>

<Frame>
  <img alt="The image illustrates a process of active invalidation involving an app, Redis cache, and a database, where a bio update is propagated through the system." />
</Frame>

Active invalidation increases implementation complexity because every write path must include cache maintenance. It’s the right choice when staleness is unacceptable (security/permissions/privacy).

## Choosing the right approach

There’s no single answer — choose based on your correctness requirements, traffic patterns, and operational complexity:

* Use short TTLs (with jitter) for high-throughput, eventually-consistent data (home feed, counts).
* Use active invalidation for security- or privacy-sensitive fields (permissions, feature flags).
* Use longer TTLs for rarely-changing data (user profile information) to reduce read latency and DB load.
* Combine strategies: TTLs + jitter for general load reduction, request coalescing to avoid stampedes, and active invalidation for critical fields.

<Frame>
  <img alt="The image illustrates a choice between using a short TTL (Time to Live) for a trending feed, where a few seconds of staleness is acceptable, and ensuring privacy settings that can't be stale even for a second." />
</Frame>

## Industry defaults (good starting points)

| Resource / Feature                            | Typical default                  | Rationale                                                                  |
| --------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------- |
| Home feed                                     | \~30-second TTL                  | Balances freshness with load reduction; short staleness acceptable         |
| Profile card                                  | Few minutes TTL                  | Profiles change infrequently; longer TTL reduces DB load                   |
| Trending list                                 | \~60-second TTL                  | Trends tolerate short delays; helps smooth traffic                         |
| Security-sensitive data (permissions/privacy) | No TTL — use active invalidation | Even momentary staleness can cause breaches; require immediate consistency |

These are tunable defaults — measure your latency, cache hit rate, and correctness requirements and iterate.

<Frame>
  <img alt="The image illustrates industry benchmarks for various app features like &#x22;Home Feed&#x22; and &#x22;Trending List&#x22; with their respective time-to-live (TTL) durations, alongside a phone interface showing privacy settings." />
</Frame>

One final point: the worst bugs are not when the cache is empty. The worst bugs are when the cache confidently serves wrong data.

There’s an old joke that there are only two hard things in computer science: cache invalidation, naming things, and off-by-one errors.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/61093e0d-f42a-4ec2-833c-356964524728" />
</CardGroup>
