# Rate Limiting and Security Basics

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Failure-Protection-and-Operations/Rate-Limiting-and-Security-Basics/page

Practical security and rate limiting guidance for public APIs, covering rate limits, TLS, authentication and authorization, signed URLs, input validation, and secrets management.

Now that your photo app's API is reachable from the public internet, users and attackers alike can contact your servers directly. Most traffic is legitimate, but you must plan for both malicious actors and accidental misuse.

Common ways an exposed API can be abused:

* Scrapers downloading every photo.
* Bots attempting to brute-force or guess passwords.
* Buggy clients repeatedly hammering your servers and consuming capacity.

When you expose an API, add defenses and follow basic security best practices in design and implementation. The following covers the most important, practical controls to reduce risk.

## 1) Rate limiting

You already encounter rate limiting in everyday apps: type a password wrong too many times and the app demands you wait before trying again. That behavior protects login endpoints from repeated attempts.

<Frame>
  <img alt="The image depicts a login interface labeled &#x22;Sign In&#x22; on the left, connected to a flowchart illustrating network elements like a load balancer and app servers, under the title &#x22;Defense 1: Rate Limiting.&#x22;" />
</Frame>

Apply the same principle to your API: cap how many requests a single identity (user, API key, or IP) can make in a given interval. Example policy: `100 requests per minute` per API key. When a client exceeds the limit, respond with HTTP 429 (Too Many Requests) and include a `Retry-After` header indicating when requests can resume.

Example HTTP response for a throttled request:

```http theme={null}
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 60

{
  "error": "rate_limit_exceeded",
  "message": "You have exceeded the request quota. Try again in 60 seconds."
}
```

When a client is blocked for exceeding a configured threshold, we say the client is throttled. Rate limiting helps in two important ways:

1. Stops abuse — scrapers and other malicious clients are slowed or blocked.
2. Protects resiliency — buggy clients can't take down entire services because the rate limiter caps their impact.

Useful rate-limiting strategies:

* Token bucket or leaky bucket algorithms for smooth enforcement.
* Per-user, per-API-key, per-IP, and per-endpoint limits (different endpoints may need different limits).
* Burst allowance for short spikes, but enforce sustained limits.
* Expose limits and remaining quota in response headers (e.g., `X-RateLimit-Limit`, `X-RateLimit-Remaining`).

<Frame>
  <img alt="The image illustrates a rate-limiting concept with a mobile app interface, showing a &#x22;429 Too Many Requests&#x22; response and a load balancer handling requests at a rate of 100 requests per minute." />
</Frame>

## 2) Encrypt all connections (HTTPS / TLS)

Every client-server connection must be encrypted: use HTTPS (TLS). Plain HTTP transmits credentials, tokens, and data in plaintext that can be observed or modified in transit. In production, TLS termination commonly happens at the edge (e.g., load balancer, CDN, or edge proxy).

Best practices for TLS:

* Require TLS 1.2+ and prefer TLS 1.3.
* Use strong cipher suites and disable legacy, insecure protocols.
* Renew and rotate certificates before expiry; automate certificate management where possible.
* Terminate TLS at trusted edge components and protect internal traffic appropriately.

<Frame>
  <img alt="The image illustrates a flowchart emphasizing encrypting connections with HTTPS, showing a mobile application interface, password entry, and a load balancer directing traffic to app servers." />
</Frame>

## 3) Authentication vs Authorization

Understanding and separating authentication and authorization is critical.

* Authentication: "Who are you?" — the process of verifying a user or client (login flows, API keys, OAuth tokens).
* Authorization: "What are you allowed to do?" — once identity is established, check permissions for specific actions or resources.

For example, authentication confirms the caller is user John. Authorization enforces whether John may delete a photo. Getting authorization wrong is a common source of data leaks; implement fine-grained checks to ensure users cannot access or modify others' private data.

<Frame>
  <img alt="The image is a diagram illustrating the concepts of authentication and authorization within a network setup. It shows user interaction with a mobile interface, a load balancer, app servers, and connections to databases and object storage." />
</Frame>

Design tips:

* Centralize authorization checks or use well-tested libraries/policies (e.g., attribute-based access control, RBAC).
* Validate both resource ownership and action-level permissions before performing sensitive operations.
* Log authorization failures for visibility and incident investigation.

## 4) Signed URLs for private content

In a photo app, public assets are accessible broadly, while private photos must remain restricted even if hosted in the same object storage and served through a CDN. If a direct object URL leaks, how can you limit access?

Use signed (time-limited) URLs. A signed URL is analogous to a ticket that grants access to a single resource for a short period. The server generates a URL that includes an expiration and cryptographic signature. After the expiry time, the URL becomes invalid, limiting the damage if links leak.

Use cases:

* Short-lived access for private files delivered via CDN.
* Pre-signed PUT/POST URLs for direct uploads to object storage.

## 5) Never trust incoming data — validate and sanitize

Treat all client input as untrusted. Validate every field, header, and query parameter before using it in business logic or database statements.

A classic risk is SQL injection. If you concatenate raw input into SQL, an attacker can escape the query context and run arbitrary commands. For example, a malicious payload might look like:

```sql theme={null}
'); DROP TABLE photos;
```

Protect your database by:

* Using parameterized queries / prepared statements.
* Enforcing strong input validation (types, sizes, allowed characters).
* Using ORM abstractions that automatically parameterize queries where appropriate.

Example (pseudo-code) safe query pattern:

```JavaScript theme={null}
db.query("SELECT * FROM photos WHERE owner_id = $1 AND id = $2", [ownerId, photoId])
```

## 6) Secrets management

Your system relies on secrets: database passwords, API keys, signing keys, and more. Protect secrets by following these principles:

* Never hard-code secrets in source code or bake them into container images.
* Store secrets in a dedicated secrets manager and inject them at runtime.
* Limit secret scope and grant least privilege.
* Rotate secrets regularly and log access to the secrets store.

Avoid accidental exposure by auditing repositories, build artifacts, and container images.

<Callout icon="lightbulb">
  Security checklist for a public API: rate limit clients, encrypt all connections, enforce authentication and authorization, use signed URLs for private content, validate all incoming data, and keep secrets out of source code.
</Callout>

## Quick reference table: core controls

| Control            | Purpose                             | Example / Recommended Practice                                  |
| ------------------ | ----------------------------------- | --------------------------------------------------------------- |
| Rate limiting      | Prevent abuse and protect capacity  | `100 requests/minute` per API key; return `429` + `Retry-After` |
| TLS / HTTPS        | Encrypt data in transit             | TLS 1.3 preferred; automate cert renewals                       |
| Authentication     | Prove identity                      | OAuth2, JWTs, API keys                                          |
| Authorization      | Enforce permissions                 | RBAC or ABAC checks per operation                               |
| Signed URLs        | Protect private object access       | Time-limited, signed pre-signed URLs for object storage         |
| Input validation   | Prevent injection & malformed input | Parameterized queries, type checks, length limits               |
| Secrets management | Protect credentials                 | Use a secrets manager and rotate regularly                      |

None of the above dives into advanced offensive-security techniques, but these basics are where most real incidents start. Implementing and consistently enforcing these measures will mitigate a large fraction of common attacks and accidental outages.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/c7a8e3b7-9370-4462-a298-4a441dd68f8a/lesson/37c07301-5490-4432-a5a7-666370219ea8" />
</CardGroup>
