# Replication

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Replication/page

Explains database replication, read scaling, replication lag and consistency trade offs, read routing and failover, and why backups remain essential.

A cache placed in front of a database keeps only the "hot" or frequently accessed data. Most data remains uncached, so many queries still reach the database. PhotoSharingApp is a read-heavy application—users view hundreds of photos—so the database continues to handle a large portion of traffic.

<Frame>
  <img alt="The image illustrates a read-heavy app architecture where the app fetches data from a database via a cache. If data is not in the cache, it's retrieved from the database; cache stores trending photos and hot profiles." />
</Frame>

Right now we have a single database instance. That single instance is a single point of failure: if it fails, the application becomes unavailable and data may be at risk. To improve resilience, we add replicas of the primary database. A common deployment pattern is a primary plus two replicas, giving three copies of the data. This increases costs because you’re running multiple database instances instead of one.

<Frame>
  <img alt="The image illustrates a system architecture involving a mobile app connected to three databases (one primary and two replicas), highlighting increased costs." />
</Frame>

If we keep three identical copies of the data, it makes sense to distribute read traffic across them instead of forcing all reads to the primary. We place a load balancer in front of the replicas so read queries can be spread across the instances, reducing load on the primary while writes continue to go to the primary.

<Frame>
  <img alt="The image is a schematic representation of a network setup, showing an app interface connected through a load balancer to a primary database and replica databases." />
</Frame>

Writes must go to the primary. Allowing writes on multiple replicas independently creates conflicting histories and ambiguity. For example, if a record x is 7 on both primary and replica, and one write changes x to 9 on the primary while another (erroneous) write changes x to 13 on a replica, you end up with inconsistent values and no clear way to choose the correct one. To avoid these conflicts, the system accepts writes only on the primary and streams changes to replicas.

<Frame>
  <img alt="The image illustrates a database load balancing system, depicting data flow from an app through a load balancer to a primary database and its replicas, showcasing different values of &#x22;x&#x22;." />
</Frame>

Replicas typically keep an open connection to the primary and stream changes from it. Because replicas copy changes over the network, they are normally slightly behind the primary—this delay is called replication lag. Lag is often measured in milliseconds but can vary based on workload, network, and system load.

<Frame>
  <img alt="The image illustrates a synchronization process between replicas and a primary database using an app and a load balancer. It shows a mobile app interface on the left, leading to an app server, load balancer, and then to a primary database with replicas on the right." />
</Frame>

Because of replication lag, replicas are not immediately consistent with the primary. Over time they converge; this property is called eventual consistency—replicas may not have the newest writes yet, but they will eventually receive and apply them.

<Frame>
  <img alt="The image illustrates a system architecture showing an app interacting with a load balancer that distributes requests to a primary database and its replicas, highlighting a replication lag of a few milliseconds." />
</Frame>

Replication lag can create observable anomalies. For example, Alan uploads a photo (a write to the primary). Half a second later Alan refreshes his profile (a read). If his read is routed to a replica that hasn’t yet applied the new write, he will not see the photo even though it is safely stored on the primary.

<Frame>
  <img alt="The image is a diagram illustrating a data flow from a mobile app through a load balancer to a series of databases, including a primary and two replicas, one of which is marked as &#x22;still behind.&#x22;" />
</Frame>

The correct fix for read-after-write anomalies is to ensure reads for a client’s recent writes come from a source that already has those writes—typically the primary. Practically, this can be implemented by:

* Routing a client’s read-after-write requests to the primary for a short time window (read-your-writes).
* Using write-through cache invalidation so the cache immediately reflects recent writes.
* Using sticky routing or session affinity for a brief period after a write.

<Callout icon="lightbulb">
  For user-visible operations (like uploading photos), implement read-after-write routing: direct the user’s subsequent reads to the primary briefly or invalidate the cache entry to ensure they immediately see their changes.
</Callout>

When every read must reflect the absolute latest data, the system requires strong consistency. The simplest way to achieve strong consistency is to read from the primary, since it contains the most recent writes. However, directing many reads to the primary increases its load—the very problem replication is meant to reduce. Most social or media applications accept eventual consistency for many use cases; deciding which parts of the application need strong consistency versus eventual consistency is a key system-design decision.

<Frame>
  <img alt="The image illustrates a system architecture diagram highlighting &#x22;Strong Consistency&#x22; with components including a mobile app, server, load balancer, and primary and replica databases. It suggests deciding which part of an app needs specific consistency levels." />
</Frame>

Replication also improves availability. If the primary fails, you can promote one of the replicas to become the new primary; this promotion is called failover. Automated failover requires robust monitoring, leader-election logic, and careful handling of in-flight transactions to be safe.

To summarize, replication provides two primary benefits:

* Replicas absorb read traffic and reduce the burden on the primary.
* Replicas provide redundancy so the app can recover when the primary fails.

Below is a quick comparison of trade-offs to consider when using replication.

| Aspect           | Benefit                                           | Considerations                                        |
| ---------------- | ------------------------------------------------- | ----------------------------------------------------- |
| Read scalability | Replicas handle read load, improving throughput   | Reads may be slightly stale (replication lag)         |
| Availability     | Failover to a replica reduces downtime            | Requires careful automation and monitoring            |
| Consistency      | Reading from the primary gives strong consistency | Routing more reads to the primary increases load      |
| Data safety      | Replication keeps multiple copies online          | Replicas mirror human mistakes and logical corruption |

One critical misunderstanding is to assume replicas protect against all data loss. Replicas faithfully copy everything from the primary—including accidental or malicious destructive operations. For example:

```sql theme={null}
DROP TABLE photos;
```

Within milliseconds, that destructive change will reach all replicas and all copies will be gone. Replication amplifies mistakes; it is not a substitute for backups. Always maintain versioned, off-cluster backups and regularly test restore procedures.

<Frame>
  <img alt="The image is a diagram showing an app's architecture, featuring a user interface, app server, load balancer, primary database, replica databases, and a backup system." />
</Frame>

<Callout icon="warning">
  Replication improves availability and read scalability, but it does not replace backups. Always maintain versioned, off-cluster backups and regularly test restores.
</Callout>

Further reading and references:

* [Database Replication Patterns and Trade-offs](https://en.wikipedia.org/wiki/Replication_\(computing\))
* [Designing for Consistency and Availability](https://martinfowler.com/articles/patterns-of-distributed-systems.html)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/8d7c5dae-aa01-4b58-9808-a742a13393a1" />
</CardGroup>
