# Cache Aside with Redis

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Cache-Aside-with-Redis/page

Demonstrates Redis cache-aside pattern to accelerate reads, show cache hits and misses, and illustrate stale data when the database is updated without cache invalidation.

In this lesson you'll place a Redis cache in front of your database to accelerate read requests. You'll measure response behavior before and after adding the cache, then modify the underlying database and observe the application returning stale data because it was served from Redis.

This demonstrates the cache-aside (lazy-loading) pattern: on a cache miss the application reads from the database and populates Redis; on a cache hit it serves data directly from Redis. If the database changes and the cache is not invalidated or updated, the application may continue returning stale data until the cache entry expires or is refreshed.

Here is an example interaction showing a request for a user profile, a repeated request (served from cache), and a short look at the application logs:

```bash theme={null}
controlplane ~ on ☁️ (us-east-1) ➔ curl localhost:8000/profile/7
{"id": 7, "bio": "Original bio for user 7."}
