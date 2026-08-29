# Interview ByteTwo Caching Questions

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Interview-ByteTwo-Caching-Questions/page

Concise interview guide covering cache eviction policies, stampede defenses, and consistency strategies with tradeoffs and short examples.

Caching questions in interviews often go beyond “what is caching?” — interviewers frequently ask two follow-ups: (1) when the cache is full, what do you evict? and (2) what happens when a hot entry expires and many requests miss the cache at once? This article gives focused, interview-ready answers, practical trade-offs, and short examples you can mention.

## 1) Eviction: what do you remove when the cache is full?

A practical, widely accepted answer: LRU (Least Recently Used). LRU evicts the items that haven’t been accessed for the longest time, and it works well when recent access correlates with future access.

Other policies are valid depending on access patterns and constraints. The table below summarizes common eviction strategies and when to use them.

| Policy                      |                                                        When to use | Notes                                                                                 |
| --------------------------- | -----------------------------------------------------------------: | ------------------------------------------------------------------------------------- |
| LRU (Least Recently Used)   |  Recent access predicts future access (web caches, session caches) | Good general-purpose choice; O(1) implementations exist with linked lists + hash maps |
| LFU (Least Frequently Used) | Stable, long-term popularity matters (popular items rarely change) | Tracks frequency; needs aging to avoid staleness bias                                 |
| FIFO (First In, First Out)  |          Simple implementations or strict insertion-order eviction | Easy but ignores recency/frequency                                                    |
| Size-aware / Cost-aware     |                    Items differ greatly in size or generation cost | Evict items by cost-to-store or cost-to-recompute rather than count                   |
| TTL-based eviction          |              Data tolerates staleness and freshness is time-driven | Simple and scalable; combine with jitter to avoid synchronized expirations            |

If you’re asked to pick one policy in an interview, explain why it fits the workload (access skew, item size, and cost-to-recompute are common factors).

## 2) Cache stampede (thundering herd): what happens and how to defend?

When a hot entry expires, many concurrent requests may all try to rebuild it at once. Without mitigation, this “stampede” can overwhelm the backend and cause latency spikes or errors.

Common defenses (pick one or more depending on system constraints):

* Request coalescing / single-flight\
  Let one request rebuild the entry while others wait for the result. This reduces duplicate work and backend load.
* Serve stale values while refreshing (stale-while-revalidate)\
  Return the old cached value immediately while a background refresh is performed.
* Refresh-ahead (proactive refresh)\
  Refresh hot entries before they expire to avoid synchronous regeneration.
* Randomized TTLs (jitter)\
  Add randomness to expiration times so many entries don’t expire simultaneously.
* Distributed locks or coordination\
  Use a lock to ensure only one process rebuilds an entry; be careful: locks can introduce contention or single points of failure.
* Rate-limit or backoff rebuilds\
  Apply exponential backoff to retries that fail when rebuilding to avoid amplifying load.

Short pseudocode examples:

Request coalescing / single-flight (conceptual)

```text theme={null}
if cache.miss(key):
    if singleflight.begin(key):         # only one goroutine/process wins
        value = regenerate(key)
        cache.set(key, value)
        singleflight.done(key, value)
    else:
        value = singleflight.wait(key)  # other requests wait for the winner
return value
```

Stale-while-revalidate pattern

```text theme={null}
value, meta = cache.get(key)
if meta.expired:
    spawn_background_refresh(key)
    return value   # serve stale immediately
else:
    return value
```

Jittered TTL example (set TTL with ±jitter)

```text theme={null}
base_ttl = 600  # seconds
jitter = rand(-60, +60)
ttl = base_ttl + jitter
cache.set(key, value, ttl)
```

<Callout icon="warning">
  Using distributed locks for rebuilds is effective but introduces operational risk: poorly implemented locks can become bottlenecks or single points of failure. Mention alternatives like single-flight or stale-while-revalidate if you want to avoid lock complexity.
</Callout>

<Callout icon="lightbulb">
  If you mention cache stampede and at least one mitigation (e.g., single-flight or stale-while-revalidate) proactively in an interview, it signals you’ve considered operational failure modes beyond basic eviction strategies.
</Callout>

## 3) Keeping cache and database consistent

Pick a consistency strategy based on how much staleness your application can tolerate, throughput requirements, and operational complexity.

Common approaches:

* TTLs (leasable staleness)\
  Let entries expire naturally. Good for low-consistency requirements and high read throughput.
* Cache-aside (explicit invalidation)\
  Update or delete cache entries after a DB write. Typical sequence for a write:
  1. Write to the database
  2. Delete or update cache entry
     This avoids serving stale results after the write. Example:
  ```text theme={null}
  db.update(item)
  cache.delete(key)  # invalidate so next read repopulates from DB
  ```
* Write-through / write-behind\
  Write-through: writes go through the cache and synchronously to the DB (stronger consistency, more latency).\
  Write-behind: cache acknowledges write and asynchronously persists to DB (better write performance but risk of data loss).
* Pub/Sub or CDC-based invalidation\
  Use a message bus or change-data-capture system to broadcast changes and invalidate caches across distributed services quickly.

Table: cache-consistency strategies at a glance

| Strategy                             |                                         Pros | Cons                                               |
| ------------------------------------ | -------------------------------------------: | -------------------------------------------------- |
| TTL                                  |                             Simple, scalable | Stale reads until expiry                           |
| Cache-aside (invalidate after write) |             Simple, common, explicit control | Requires correct application logic on every writer |
| Write-through                        |                    Stronger read consistency | Higher write latency                               |
| Write-behind                         |                      Better write throughput | Risk of data loss or complexity in retries         |
| Pub/Sub / CDC                        | Near real-time invalidation across processes | Infrastructure complexity                          |

<Callout icon="lightbulb">
  When discussing cache consistency in interviews, explain the trade-offs (staleness vs. complexity vs. throughput) and justify your choice against a hypothetical workload (e.g., “session data vs. inventory counts”).
</Callout>

## Quick interview-ready checklist

* Eviction: name a policy (LRU), and justify it for the workload (or mention alternatives: LFU, FIFO, size-aware).
* Stampede: define the problem and name at least one mitigation (single-flight, stale-while-revalidate, refresh-ahead, TTL jitter).
* Consistency: choose between TTL, cache-aside, write-through/behind, or CDC and explain trade-offs.

## Links and references

* [Redis eviction policies (LRU/LFU)](https://redis.io/docs/manual/eviction/)
* [Go singleflight package concept (golang.org/x/sync/singleflight)](https://pkg.go.dev/golang.org/x/sync/singleflight)
* [stale-while-revalidate pattern (RFC & CDN docs)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#stale-while-revalidate)
* [Change Data Capture (CDC) overview](https://debezium.io/documentation/)

Answer succinctly in interviews, back choices with workload reasoning, and mention at least one operational failure mode (like cache stampede) to stand out.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/456810d7-90d7-4778-abed-8b79da1a23ac" />
</CardGroup>
