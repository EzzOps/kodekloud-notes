# Interview Byte Which DB and Why

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Interview-Byte-Which-DB-and-Why/page

Guidelines and a checklist for choosing SQL or NoSQL based on data model, access patterns, consistency needs, transactions, scaling and operational tradeoffs, with interview examples.

One question that appears in almost every system-design interview is: choose SQL or NoSQL for your design and explain why.

The key to a strong answer is not just naming a database family — it’s justifying that choice from your access patterns and the guarantees your application needs.

## Answer framework

A concise, persuasive justification typically covers:

* The structure of your data (entities and relationships).
* The queries and access patterns you must support (especially joins and complex reads).
* Consistency and transactional guarantees required by the application.
* How you would handle other workload types (real systems often combine SQL and NoSQL stores).

## What to explain (quick checklist)

* Data model: Is it relational (`users`, `photos`, `follows`) or schemaless/document-oriented?
* Query shape: Do you need multi-table joins, aggregations, or secondary indexes?
* Transactions: Are atomic, multi-row updates necessary for correctness?
* Scale and latency: Do you need multi-region reads/writes or extreme write throughput that requires sharding?
* Operational tradeoffs: How will you do backups, replication, and failover?

## Example concise justification

"My data is relational — `users`, `photos`, and `follows` are connected. To build a home feed I must combine these entities, which implies joins and transactional consistency. Therefore a relational SQL database makes sense for the core social graph. If I later add a high‑volume, schemaless stream such as analytics events, I would store that separately in a NoSQL store optimized for ingestion and OLAP."

## What earns points in an interview

* Start from access patterns (reads, writes, queries, joins), not buzzwords like “it scales.”
* Explain *why* joins, transactions, or schema enforcement are necessary for correctness.
* If you propose NoSQL, be specific: what about SQL fails for this workload? (e.g., multi-region latency, write hotspot that requires consistent hashing/sharding, or highly variable record schemas).
* Describe how you will handle consistency and transactions under a NoSQL choice (e.g., single-shard transactions, application-level compensation, or CRDTs).
* Acknowledge hybrid approaches: identify which parts map to SQL vs NoSQL and why.

## Avoid weak answers

Do not answer “NoSQL because it scales” without follow-up. Interviewers will ask: what prevents SQL from meeting the requirements? How would you partition, replicate, or increase capacity? What consistency tradeoffs will you accept?

## Remember ACID

Before an interview, be ready to state which of the ACID properties your system requires and why:

| Property    |                                                                           What it means | When you need it                                                               |
| ----------- | --------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------ |
| Atomicity   |                                          All parts of a transaction succeed or none do. | Payments, transfers, or any multi-row mutation that must not partially apply.  |
| Consistency | Transactions move the DB from one valid state to another (schema/constraints enforced). | Referential integrity among related entities (e.g., users and their profiles). |
| Isolation   |                          Concurrent transactions don't produce incorrect interleavings. | When concurrent updates could violate invariants without isolation.            |
| Durability  |                                          Once committed, data persists despite crashes. | Any data that must survive failures (e.g., user content, financial records).   |

## Quick workload → store mapping

| Workload                                         |                         Recommended store type | Why                                             |
| ------------------------------------------------ | ---------------------------------------------: | ----------------------------------------------- |
| Core relational data with joins and transactions |                    SQL (Postgres, MySQL, etc.) | Strong ACID, expressive joins, mature tooling   |
| High-ingest event streams / time-series          | NoSQL / TSDB (Cassandra, ClickHouse, InfluxDB) | Optimized for write throughput and OLAP queries |
| Flexible schema or nested documents              |               Document DB (MongoDB, Couchbase) | Schema flexibility and document-centric queries |
| Caching / low-latency reads                      |             In-memory store (Redis, Memcached) | Sub-ms reads and TTL-based eviction             |

## Suggested short answer template you can adapt in an interview

1. Describe the data model and primary access patterns (reads, writes, query shapes).
2. Explain whether joins and multi-row transactions are required; if yes, favor SQL.
3. If choosing NoSQL, state the scalability or schema reasons and how you'll handle consistency/transactions.
4. Mention other components and where they would live (e.g., SQL for core relational data, NoSQL for logs/analytics).
5. Conclude with operational considerations: sharding, replication, backups, expected latencies, and monitoring.

Keeping the answer focused on access patterns and guarantees demonstrates both technical understanding and practical design sense.

> **lightbulb** When you justify a database choice, explicitly tie ACID (or relaxed consistency models like eventual consistency / BASE) to your application needs — for example, whether user-facing actions require strict transactions or whether background analytics can tolerate eventual consistency.

## Links and references

* [ACID (Wikipedia)](https://en.wikipedia.org/wiki/ACID)
* [NoSQL (Wikipedia)](https://en.wikipedia.org/wiki/NoSQL)
* [CAP Theorem (Wikipedia)](https://en.wikipedia.org/wiki/CAP_theorem)
* [Designing Data-Intensive Applications — Book](https://dataintensive.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/b101cd8e-87f9-406d-8616-354d50412109)
