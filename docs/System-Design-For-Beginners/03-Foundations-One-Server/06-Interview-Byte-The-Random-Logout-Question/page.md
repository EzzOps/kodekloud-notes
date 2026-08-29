# Interview Byte The Random Logout Question

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Interview-Byte-The-Random-Logout-Question/page

Explains random user logouts after horizontal scaling caused by in-memory sessions and recommends using shared session stores or stateless tokens with trade-offs and operational guidance

This classic interview scenario tests your understanding of horizontal scaling and session management.

You scale a service from two servers to five, and users start getting randomly logged out. What happened, and how do you fix it?

## Root cause (state the cause clearly)

The most likely cause: sessions are stored in each server's local memory. When a user's subsequent request is routed to a different server that doesn't have that session in memory, the request appears unauthenticated and the user is effectively logged out.

<Frame>
  <img alt="The image is a diagram showing a flowchart related to a session management system, illustrating how a user's session data is distributed across multiple servers. It features stick figures labeled &#x22;interviewer&#x22; and &#x22;you,&#x22; along with icons representing a mobile device and servers." />
</Frame>

## Robust fix

Make session state accessible to all application servers by moving session storage out of local process memory and into a shared, centralized store. Examples:

* Redis: low-latency, supports persistence, replication, and clustering — good for session caches.
* Memcached: simple in-memory cache for ephemeral session storage.
* Relational or NoSQL DB: durable, but may need tuning for low latency.

This design keeps web/application servers stateless: any server can validate a user’s session, so routing a user to any backend instance will not cause a logout.

## Quick alternatives and trade-offs

Sticky sessions (session affinity)

* Explanation: configure the load balancer to pin a client to the same backend instance so their in-memory session is always available.
* When it's useful: simple, fast stopgap for small clusters or legacy apps.
* Drawbacks: reduces load-balancer flexibility, causes uneven utilization, complicates rolling deployments, and doesn't survive instance failures.

<Callout icon="lightbulb">
  Tip: In interviews answer in this order—(1) state the cause (local in-memory sessions), (2) propose the robust fix (shared session store and stateless servers), and (3) mention sticky sessions as an alternative and explain its trade-offs.
</Callout>

## Comparison: session strategies

| Strategy                 |                                          Description | Pros                                          | Cons                                                          |
| ------------------------ | ---------------------------------------------------: | --------------------------------------------- | ------------------------------------------------------------- |
| In-memory on each server |             Sessions stored in server process memory | Very fast, simple                             | Loses sessions when requests hit other servers; not scalable  |
| Sticky sessions          |        Load balancer affinitizes clients to a server | Quick to implement                            | Uneven load, poorer fault tolerance                           |
| Shared session store     | Central Redis/Memcached/DB accessible to all servers | Scalable, servers remain stateless            | Requires availability, replication, low latency               |
| Stateless tokens         |             Client holds signed tokens (e.g., `JWT`) | No server-side session storage; easy to scale | Revocation/rotation complexity; token security considerations |

## Operational considerations

* Choose a low-latency, highly available store for sessions (Redis or Memcached are common). Plan replication, persistence, and failover.
* Secure sessions:
  * Use cookie flags: `HttpOnly`, `Secure`, `SameSite`.
  * Encrypt sensitive session data at rest and in transit.
* Handle session expiration and revocation: design for logout flows and compromised tokens.
* Monitor performance and latency of the shared store; it becomes a critical dependency.
* Consider caching session lookups locally with short TTLs to reduce load, while handling invalidation carefully.

## Modern alternatives

* Stateless tokens (signed `JWT`s): avoid server-side storage, but implement revocation lists or short token lifetimes with refresh tokens to handle logout and compromise scenarios.
* Hybrid approaches: keep minimal session metadata in a shared store and use signed tokens for authentication claims.

<Callout icon="warning">
  Warning: Do not store sensitive session data in plaintext on the client or in an unprotected shared store. Secure your session store (authentication, TLS, ACLs), plan for replication and failover, and monitor performance to avoid introducing a single point of failure.
</Callout>

## Interview guidance

If you suggest a suboptimal approach during the interview, quickly explain why it’s incorrect and contrast it with your preferred solution. Demonstrating clear trade-off analysis and operational awareness is often more valuable than a single “perfect” answer.

## Links and references

* [Redis](https://redis.io/)
* [Memcached](https://memcached.org/)
* [JWT (JSON Web Tokens)](https://jwt.io/)
* [Session affinity (sticky sessions)](https://en.wikipedia.org/wiki/Session_affinity)
* MDN: `HttpOnly`, `Secure`, `SameSite` cookie flags — see the Set-Cookie documentation on MDN

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/2416183c-7c90-4fd4-853a-704a9839ffa9" />
</CardGroup>
