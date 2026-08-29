# Design a Home Feed For Instagram

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/System-Design/Design-a-Home-Feed-For-Instagram/page

Progressive designs for scalable Instagram-style home feeds explaining fan-out, hybrid push-pull strategies and Redis caching to handle celebrity write storms

This guide walks through progressively better designs for building a home feed like Instagram’s: users post photos and their followers see those photos in a personal feed. We present four versions — why each works, where it fails at scale, and how to combine techniques for a production-ready architecture.

## Version 1 — Naive: compute feed at read time

When a user opens the app, the server runs a single SQL query to fetch recent posts from everyone the user follows, ordered by time and limited to N results:

```sql theme={null}
SELECT *
FROM posts
WHERE author_id IN (`followed_user_ids`)
ORDER BY created_at DESC
LIMIT 50;
```

This is simple and correct, and it works well for small deployments.

Why it breaks at scale

* Typical users follow \~200 people; power users may follow thousands. Even with indexes, the query must fetch, merge, and sort across many author timelines on every read.
* Users open the app many times per day, creating repeated heavy read queries that quickly overwhelm the database.

## Version 2 — Fan-out on write (precompute feeds)

Flip the model: compute each follower’s feed when a user posts. On write, push the new post ID into every follower’s inbox (a precomputed per-user feed). On read, you simply fetch a precomputed list of post IDs and then fetch post details.

<Frame>
  <img alt="The image shows a technical explanation of database stress with many users and a proposed solution using &#x22;fan-out on write&#x22; to manage feed updates, illustrated with stick figures and text annotations." />
</Frame>

Benefits

* Reads are cheap and fast: a single lookup of a per-user inbox.
* Eliminates runtime fan-in (merging many author timelines) on reads.

New problem: high-fanout writers (celebrities)

* Some accounts have tens or hundreds of millions of followers. A single celebrity post causes tens or hundreds of millions of inbox writes.
* The write pipeline and queueing system can be flooded, stalling the entire feed update process.

<Frame>
  <img alt="The image illustrates a scenario where a celebrity with 80 million followers makes a single post, leading to 80 million writes to a server. There's also a reference to &#x22;700 million&#x22; and an included photo of a person." />
</Frame>

## Version 3 — Hybrid push + pull

Use a hybrid approach that combines push (fan-out-on-write) and pull (fetch at read time):

* Push (fan-out) for normal users (small–medium follower counts): when they post, push the post ID into followers' inboxes.
* Pull for high-fanout authors (e.g., >100k followers — tuneable): store an author-centric feed for them (a small, recent list), and do not fan out their posts at write time.
* On feed load, merge:
  * The precomputed inbox (push results)
  * Recent posts fetched from author feeds for any large accounts the user follows
  * Re-rank and trim to the requested size

<Frame>
  <img alt="The image is a diagram explaining a hybrid model for content distribution. It shows how normal users use a push model (fan-out on write), and celebrities with over 100K followers use a pull model at feed time, incorporating servers, follower inboxes, and parallel writes to a PostgreSQL database." />
</Frame>

Why this helps

* Large fan-out storms are avoided because celebrity posts are pulled at read time.
* Most users still get the low-latency benefit of precomputed inboxes.

Remaining question: where to store per-user inboxes?

## Version 4 — Move precomputed feeds out of the primary database into a cache

Don’t store hot, frequently-updated inboxes in the primary relational database. Instead:

* Use the relational DB (Postgres, MySQL) as the canonical source of truth for posts and metadata.
* Store per-user inboxes in a fast in-memory store such as Redis. Typical data model:
  * Redis sorted set per user (score = timestamp) or a capped list
  * Trim inboxes to a reasonable cap (e.g., 800 entries)
* For celebrity/author feeds use a small author-centric cache (recent N posts) in Redis or a similar cache.

Benefits

* Feed loads become single-digit milliseconds.
* Primary DB is protected from feed write/read churn.
* Celebrity posts are pulled from author caches, not the primary DB.

<Frame>
  <img alt="The image illustrates a system architecture with an inbox stored in the main database (Postgres) handling millions of feed writes per second, and a Redis caching system enabling fast read times for users." />
</Frame>

## Final data-flow summary (recommended production architecture)

1. User uploads a photo
   * Write the post to the primary DB (Postgres) as the canonical record.
2. Fan-out service receives the write and decides:
   * If author is a “normal” user: push the post ID into each follower’s Redis inbox (sorted set), trimming to the inbox cap.
   * If author is a celebrity (above threshold): append the post to the author-feed cache and skip pushing to followers.
3. On feed load:
   * Read the user’s Redis inbox (fast).
   * For each followed celebrity above the threshold, fetch recent posts from the author-feed caches.
   * Merge inbox items and pulled author posts; re-rank by timestamp and/or relevance.
   * Fetch full post content from a post cache or from Postgres if needed, and perform privacy checks before rendering.

### Tradeoffs at a glance

| Version | Approach                       |            Read Cost |              Write Cost | When to use                                    |
| ------: | ------------------------------ | -------------------: | ----------------------: | ---------------------------------------------- |
|      V1 | Read-time compute              | High (heavy queries) |                     Low | Small user bases or prototypes                 |
|      V2 | Fan-out on write               |                  Low |        High (can burst) | Most cases if no huge celebrities              |
|      V3 | Hybrid push + pull             |                  Low |                Moderate | When some authors have massive follower counts |
|      V4 | Hybrid + cache (Redis inboxes) |             Very low | Moderate (cache writes) | Production at scale (recommended)              |

## Implementation tips and operational knobs

* Celebrity threshold: e.g., `100_000` followers. Tune based on your traffic and write pipeline capacity.
* Redis inbox cap: e.g., `800` entries per user — most users do not scroll beyond a few hundred items.
* Fan-out batching and parallelism: batch writes to Redis and use parallel workers for pushes; use rate-limits for very large events.
* Cache TTLs and eviction: set sensible TTLs for author caches and post caches to balance freshness and cost.
* Observability: monitor tail latencies, queue backlogs, and Redis CPU/IO to detect fan-out storms.

<Callout icon="lightbulb">
  Tuneable knobs: the celebrity threshold (e.g., 100k followers), Redis inbox cap (e.g., 800), cache TTLs, and batching/parallelism of fan-out writes are key levers for performance and cost. Monitor tail latencies and queue backlog to adjust these values.
</Callout>

## Conclusion

The hybrid + cache pattern (fan-out for most users, pull for extremely high-fanout authors, and Redis for hot inbox storage) is a proven, scalable architecture for social feeds. It minimizes read latency for the majority of users while containing the cost and operational risk of celebrity write storms, and keeps the primary database as the durable source of truth.

## Links and References

* [Redis](https://redis.io/)
* [PostgreSQL](https://www.postgresql.org/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for deployment/scale patterns)
* Articles on feed architectures and fan-out strategies for social applications

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/ef53ec43-96e9-4d1b-8a6e-e6eb97b0d0dc/lesson/52c78fe5-5c2c-4c07-882e-2707c503d886" />
</CardGroup>
