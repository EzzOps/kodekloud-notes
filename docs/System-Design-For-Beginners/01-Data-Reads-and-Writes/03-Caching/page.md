# Caching

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Caching/page

Explains caching concepts, patterns, trade-offs, and best practices for using Redis to speed reads, manage consistency, and handle invalidation in distributed systems.

When the same item is requested repeatedly, reading it from the database each time is wasteful. Consider a public figure on your app—like Lionel Messi or Cristiano Ronaldo—whose post is viewed millions of times. The database can be hammered with identical queries for the same photo. A cache placed in front of the database solves this by serving popular items from a small, extremely fast store.

<Frame>
  <img alt="The image illustrates a system architecture flow, depicting an app accessing data with an added cache layer between the app and the database to improve performance." />
</Frame>

Why use a cache?

* Reads from an in-memory cache often complete in under 1 ms; the same read from a typical database may take 20–30 ms or more.
* Under heavy load, those milliseconds multiply into significantly higher throughput and lower cost.

Typical request flow with a cache (using Redis as an example):

1. A request arrives for a trending photo.
2. The application checks Redis first:
   * If Redis contains the item → cache hit: return value from Redis; skip the database.
   * If Redis does not contain the item → cache miss: query the database, write the result back into Redis (often with a TTL), then return the response. Future requests will hit the cache.

<Frame>
  <img alt="The image illustrates how a cache system using Redis works between a mobile application and a database. It shows the process of requesting photos, with Redis checking if the data exists before querying the database." />
</Frame>

Example: cache-aside (lazy population) in Python

```python theme={null}
