# BigQuery Anatomy of BigQuery

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Anatomy-of-BigQuery/page

Explains BigQuery architecture and core systems showing how Colossus, Capacitor, Dremel, Borg, Jupiter enable scalable, fast, reliable serverless analytics

Welcome back. This guide walks through how BigQuery works under the hood so you can understand why it’s fast, highly available, and scalable. Instead of treating BigQuery as a black box that returns query results instantly, we’ll explore the core systems Google uses — their roles, how they interact, and what that means for performance, cost, and reliability.

BigQuery is more than a database: it’s a managed service built on top of Google’s global infrastructure and decades of distributed-systems engineering. The same technologies that power Google Search, YouTube, and Gmail help BigQuery deliver low-latency, petabyte-scale analytics.

<Frame>
  <img alt="A presentation slide showing the Google logo and BigQuery icon with the title &#x22;Google Infrastructure Powering BigQuery.&#x22; The caption explains BigQuery is built on Google's massive infrastructure and expertise in distributed systems, storage, and data processing." />
</Frame>

## Query lifecycle — what happens when you run SQL

A high-level query lifecycle in BigQuery looks like this:

1. Client submits a SQL query via the Console, client SDK, or REST API. Front-end handles authentication and syntactic validation.
2. Query planner and optimizer produce a distributed execution plan.
3. Borg schedules and assigns compute resources (slots) to run the plan.
4. Dremel executes the query in parallel across many workers (tree-based aggregation).
5. Workers read data from Colossus using the Capacitor columnar format and return partial results.
6. Results are aggregated and merged, then returned to the client.

Example query (simple filter scan):

```sql theme={null}
SELECT *
FROM sales
WHERE date > '2024-01-01';
```

Below we examine each component in more detail.

## Colossus — distributed storage layer

Colossus is Google’s next-generation distributed file system and is the foundation of BigQuery’s durable, scalable storage. BigQuery stores data in columnar files inside Colossus; this layout reduces unnecessary I/O because queries only read the columns they need.

Columnar storage also enables stronger compression and encoding techniques, which reduces storage cost and speeds up scans.

<Frame>
  <img alt="A presentation slide titled &#x22;Colossus – Google's Distributed File System&#x22; with a small document icon bearing the Google logo. The slide states Colossus is Google's next‑generation distributed file system that powers BigQuery's storage layer, providing massive scalability and reliability." />
</Frame>

## Capacitor — BigQuery’s columnar format

Capacitor is BigQuery’s optimized columnar format for analytics. It stores each column contiguously and applies column-level compression/encoding (dictionary encoding, run-length encoding, delta encoding, etc.). These features often yield very large space savings (Google reports up to \~90% in some cases), which directly lowers I/O and cost while improving query performance.

<Frame>
  <img alt="A presentation slide titled &#x22;Columnar Storage Format&#x22; with four labeled boxes: Capacitor, Compression, Encoding, and Benefits. Each box includes brief notes about Google's columnar format, up to 90% size reduction, dictionary/RLE/delta encoding, and faster queries with less I/O." />
</Frame>

## Replication, erasure coding, and fault tolerance

BigQuery ensures durability and availability via multi-layer redundancy:

* Data is distributed across machines, racks, and geographic locations.
* Erasure coding (parity-based protection) reduces overhead compared to full replication while preserving fault tolerance.
* Automatic rebuild and recovery processes restore lost data when hardware fails.

These mechanisms let BigQuery tolerate the loss of individual machines, racks, or even complete data centers without user-visible data loss.

<Frame>
  <img alt="A presentation slide titled &#x22;Replication and Fault Tolerance&#x22; showing four feature tiles: 3-Way Replication, Erasure Coding, Geographic Distribution, and Automatic Recovery, each with a short descriptor beneath." />
</Frame>

## Dremel — distributed query execution engine

Dremel is the tree-based, massively parallel query engine that runs SQL queries in BigQuery. Its architecture is optimized for aggregating results from thousands of parallel workers with minimal network overhead:

* Leaf servers scan columnar data from Colossus and compute partial results.
* Intermediate servers aggregate and combine child results.
* A root server merges final results and returns them to the client.

This hierarchical aggregation reduces cross-network data movement and enables low-latency execution even at petabyte scale.

<Frame>
  <img alt="A diagram titled &#x22;Dremel Query Execution Engine&#x22; showing a tree-based execution model with a Root Server at the top, Intermediate Servers for aggregation and routing, and Leaf Servers for data scanning." />
</Frame>

## Borg — cluster management and scheduling

Borg is Google’s cluster manager that schedules and isolates compute tasks across the fleet. For BigQuery:

* Borg assigns workers to run Dremel tasks.
* It enforces resource constraints and isolation.
* It maximizes overall utilization across many tenants and workloads.

Borg enables BigQuery to elastically scale compute across Google’s infrastructure while maintaining reliability and security.

<Frame>
  <img alt="A presentation slide titled &#x22;Borg – Google's Cluster Management&#x22; featuring the Google BigQuery logo and text explaining that Borg manages BigQuery's compute resources to ensure optimal performance and resource utilization across Google's global infrastructure." />
</Frame>

## Slots and resource management

BigQuery runs query work using logical units called slots. A slot is a slice of CPU and memory used by Dremel execution workers. Key behaviors:

* Slots are allocated dynamically per query; BigQuery can scale allocation up or down based on workload.
* Customers can purchase reserved slots for predictable, guaranteed capacity.
* BigQuery uses fair scheduling to balance throughput and fairness for concurrent jobs.

Understanding slots helps you plan for performance and cost trade-offs.

<Frame>
  <img alt="A presentation slide titled &#x22;Slot Management&#x22; showing four items: Compute Slots, Dynamic Allocation, Reservation System, and Fair Scheduling. Each item has a short description (virtual CPU/memory units; auto-scaling; guaranteed capacity; equitable resource distribution)." />
</Frame>

## Global network fabric — Jupiter

BigQuery depends on Google’s global network fabric (often referenced as Jupiter) to move data rapidly between storage and compute. Features include:

* Multiple regions and availability zones for geographic diversity.
* Low-latency, high-bandwidth links within and across data centers.
* Petabit-scale backbone to support large-scale analytics.

This networking ensures that distributed query execution is not bottlenecked by slow data transfer.

<Frame>
  <img alt="A presentation slide titled &#x22;Global Infrastructure&#x22; with four highlighted features: Data Centers, Availability Zones, Network Latency, and Bandwidth. Each feature has a short note: &#x22;20+ regions worldwide&#x22;, &#x22;Multiple zones per region&#x22;, &#x22;<1 ms within region&#x22;, and &#x22;Petabit-scale networking.&#x22;" />
</Frame>

## Component summary

| Component                   | Role                                           | Why it matters                                                  |
| --------------------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| Colossus                    | Distributed file system                        | Durable, scalable object storage for BigQuery data              |
| Capacitor (columnar format) | Columnar file format with compression/encoding | Reduces I/O and cost; speeds up queries                         |
| Dremel                      | Distributed, tree-based query engine           | Enables low-latency, massively parallel query execution         |
| Borg                        | Cluster manager and scheduler                  | Allocates compute, enforces isolation, maximizes utilization    |
| Slots                       | Logical CPU/memory units                       | Controls query parallelism and performance; reservable for SLAs |
| Jupiter (network)           | High-performance datacenter network            | Fast data movement across compute and storage                   |

## Putting it all together

When you submit a query, BigQuery converts SQL into a distributed plan that Dremel executes using slots scheduled by Borg. Dremel workers scan columnar Capacitor files stored in Colossus; aggregated partial results flow up the Dremel tree and are merged at the root. Jupiter’s high-bandwidth network keeps data movement fast, and Colossus’ replication/erasure coding ensures durability and availability.

BigQuery is serverless from the user’s perspective: Google manages the underlying compute, storage, and network so you can focus on analytics rather than cluster operations.

<Callout icon="lightbulb">
  "Serverless" in BigQuery means Google manages the servers, capacity, and operations for you — but the underlying compute, storage, and network infrastructure (Borg, Dremel, Colossus, Jupiter, etc.) still exists and is optimized for performance, scalability, and reliability.
</Callout>

## Next topics to explore

* BigQuery logical model: datasets, tables, views
* Table design: schema best practices, partitioning, and clustering
* Performance tuning: slot reservations, flat-rate vs on-demand pricing
* Storage management and compression strategies

## Links and references

* BigQuery documentation: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)
* Dremel paper (Google): [https://research.google/pubs/pub36632/](https://research.google/pubs/pub36632/)
* Colossus and GoogleFS: [https://research.google/pubs/](https://research.google/pubs/)

These references provide additional depth on the systems summarized here.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/ddb507de-5463-4585-a4c7-7dfb62cd2f5b" />
</CardGroup>
