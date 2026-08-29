# Interview Byte The First Five Minutes

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Interview-Byte-The-First-Five-Minutes/page

How to use the first five minutes of a system design interview to clarify requirements and justify architectural decisions

Always remember: the first five minutes of a design interview are not about drawing. Interviewers want to hear how you think, scope problems, and make trade-offs — not just see a diagram.

When asked to design something like a photo-sharing app, resist the impulse to start sketching immediately. Instead, spend the first few minutes clarifying scope and constraints. Those answers become the pillars that justify every component you add later.

Key clarifying questions to ask up front:

* How many users are we designing for? (expected scale)
* Is the workload read-heavy or write-heavy?
* What data can we never lose? (durability constraints)
* How fast must the system feel? (latency, perceived performance)
* What consistency guarantees do we need?
* What are the storage and retention requirements for photos?
* Are there special features (sharing, comments, stories, editing)?
* Are third-party integrations required (CDNs, authentication providers)?
* What are the failure and recovery expectations (RTO/RPO)?
* Any compliance, privacy, or moderation requirements?

<Frame>
  <img alt="The image shows a simple stick figure diagram with an &#x22;interviewer&#x22; and &#x22;you,&#x22; with options to &#x22;start drawing&#x22; or &#x22;ask questions first.&#x22; The figures are seated, facing each other, with corresponding labels above them." />
</Frame>

Why these questions matter — quick mapping

| Question                     |                                  Why it matters | Architectural impact                                                                   |
| ---------------------------- | ----------------------------------------------: | -------------------------------------------------------------------------------------- |
| Expected scale               |           Determines capacity planning and cost | Sharding, partitioning, autoscaling                                                    |
| Read vs write ratio          |        Affects caching and replication strategy | Add caches, read replicas, or write-optimized stores                                   |
| Durability requirements      | Drives backup, replication, and storage choices | Replication factor, cold/hot backups                                                   |
| Latency / perceived speed    |       Informs caching, CDNs, and edge placement | Use CDNs, caching, and async processing                                                |
| Consistency guarantees       |                  Determines sync vs async flows | Strong consistency → synchronous writes; eventual consistency → background propagation |
| Storage/retention for photos |           Impacts cost and lifecycle management | Object storage with lifecycle policies                                                 |
| Special features             |                    Changes data models and APIs | Additional services (search, feed, media processing)                                   |
| Third-party integrations     |      Influences operational and security design | CDN, OAuth, SSO, external storage                                                      |
| RTO/RPO                      |        Defines recovery SLAs & backup frequency | Cross-region replication, disaster recovery plans                                      |
| Compliance/moderation        |            Introduces audit and data governance | Logging, encryption, content moderation pipelines                                      |

How to convert answers into architecture decisions

* Define the scope and prioritize the system’s non-functional requirements (scale, latency, durability).
* Map each requirement to a concrete component or pattern:
  * Read-heavy: introduce caches (in-memory, CDN) and read replicas.
  * Strong delete consistency: ensure synchronous operations or employ distributed transactions for deletes.
  * Large media storage and retention: use object storage (S3-style) with lifecycle rules.
  * Low latency perceived by users: place static media behind a CDN and use edge caching.
* For each component you propose, explicitly state which interview requirement it satisfies and what trade-offs it introduces.

Example decision patterns

* Reads dominate → Cache layer (reduce DB load, faster responses). Use TTLs and invalidation strategies tailored to freshness requirements.
* Strong consistency for deletes → enforce synchronous writes to the canonical datastore or implement a delete-confirmation workflow.
* Large photo storage with infrequent access → object storage + lifecycle tiering (hot to cold), and serve through CDN for global performance.
* High availability and low RTO → multi-region replication, automated failover, and frequent backups.

<Frame>
  <img alt="The image depicts a simplified diagram of a caching system, emphasizing that &#x22;a cache—because reads dominate,&#x22; with icons representing users, read/write operations, data loss prevention, and speed. Two stick figures are labeled as &#x22;interviewer&#x22; and &#x22;you.&#x22;" />
</Frame>

Practical interview tips

* Verbalize assumptions and ask for confirmation. Example: “I’ll assume 10M monthly active users unless you say otherwise.”
* Tie every architecture decision back to a requirement. This shows intentional design rather than guesswork.
* Sketch a high-level diagram only after you’ve solidified the main constraints.
* Discuss trade-offs and alternative approaches briefly (cost, complexity, latency).
* If time permits, call out edge cases (data retention, abuse detection, rate limiting).

References and further reading

* [Designing Data-Intensive Applications](https://dataintensive.net/) — Concepts on consistency and durability
* [What is a CDN? (Cloudflare)](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) — CDN basics and benefits
* [Object storage overview (AWS S3)](https://aws.amazon.com/s3/) — Photo storage patterns

> **lightbulb** Begin every design discussion by eliciting requirements. Use those answers as justification for each major architectural choice you make during the rest of the design.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/98ad620b-c085-4a5b-968e-879136a8f41a)
