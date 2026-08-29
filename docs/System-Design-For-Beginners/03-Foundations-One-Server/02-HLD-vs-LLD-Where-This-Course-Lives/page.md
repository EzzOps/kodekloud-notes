# HLD vs LLD Where This Course Lives

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/HLD-vs-LLD-Where-This-Course-Lives/page

Explains differences between high-level and low-level system design, focusing on HLD concepts, components, data flow, scaling, and contrasting with LLD implementation details.

In system design discussions you'll repeatedly encounter two complementary perspectives: High-Level Design (HLD) and Low-Level Design (LLD). Both matter, but they answer different questions and are used in different contexts.

<Frame>
  <img alt="The image shows a diagram with two boxes labeled &#x22;L-L-D&#x22; (Low-Level Design) and &#x22;H-L-D&#x22; (High-Level Design) under the title &#x22;System Design.&#x22;" />
</Frame>

High-level design is the zoomed-out blueprint. It identifies major components—application servers, databases, caches, queues, CDNs—and maps how requests flow between them. When interviewers ask you to "design Instagram," they usually expect an HLD: how requests travel, where data lives, how the system scales under load, where single points of failure exist, and how to recover.

Low-level design zooms into a single component or feature. It describes implementation details: function responsibilities, data structures, APIs, and edge-case handling. Examples of LLD interview prompts include "Design the Like feature" or "Implement an in-memory cache." These questions probe the detailed code structure, algorithms, and performance trade-offs.

> **lightbulb** This lesson focuses on High-Level Design—component interaction, system behavior under load, and scaling strategies. We deliberately avoid internal implementation details for each component in this course.

To make the difference concrete, consider a photo-sharing app:

* HLD: Show where the web/mobile clients connect, which frontends and backend services handle requests, where the image store and metadata DB live, any caches or message queues, and how to scale or replicate components.
* LLD: Cover the exact steps when a user taps "like": which API is called, how to enforce idempotency, how to update counters atomically, and how to design cache keys and TTLs.

Comparison at a glance:

| Aspect             | High-Level Design (HLD)                                        | Low-Level Design (LLD)                                                  |
| ------------------ | -------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Scope              | System architecture, major components, data flow               | Component internals, functions, classes, data structures                |
| Questions answered | "Where do requests go?" "How does the system scale?"           | "What happens when this API is called?" "How to avoid double-counting?" |
| Artifacts          | Architecture diagrams, component diagrams, deployment topology | Sequence diagrams, interface definitions, code snippets, pseudocode     |
| Interview examples | "Design Instagram", "Design a scalable messaging system"       | "Design the Like feature", "Implement an LRU cache"                     |
| Deliverables       | Service boundary definitions, scaling and redundancy plan      | API design, algorithms, concurrency control, optimizations              |

<Frame>
  <img alt="The image depicts an interview scenario where the interviewer asks candidates to design different features: &#x22;Design Instagram&#x22; (HLD), &#x22;Design the Like feature&#x22; (LLD), and &#x22;Design an in-memory cache&#x22; (LLD)." />
</Frame>

Below is a short LLD-style example showing the kind of code-level detail we intentionally do not cover in this HLD-focused course. It illustrates cache lookups, database checks, and count updates for a "like" action. Note: this is illustrative only.

```javascript theme={null}
import { db, cache } from "./store";

async function handleLike(userId, photoId) {
  if (await hasLiked(userId, photoId)) return;
  await saveLike(userId, photoId);
  await bumpCount(photoId);
}

async function hasLiked(userId, photoId) {
  // Check cache first for speed
  const key = `likes:${userId}:${photoId}`;
  const cached = await cache.get(key);
  if (cached !== null) return Boolean(cached);

  // Fallback to the database
  const exists = await db.likes.exists({ userId, photoId });
  // Cache the result for a short time
  await cache.set(key, exists ? 1 : 0, { ttl: 300 });
  return exists;
}
```

Further reading and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Designing Data-Intensive Applications (book)](https://dataintensive.net/)
* [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/a74821f4-078b-4dfa-b6ef-00f0df665e29)
