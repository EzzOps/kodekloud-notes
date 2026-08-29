# Course Introduction

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/Introduction/Course-Introduction/page

Overview of AWS managed database services, use cases, and hands-on lab training covering RDS, Aurora, DynamoDB, ElastiCache, Redshift, Neptune, Timestream, and OpenSearch

Hello, I'm Sanjeev — welcome to the AWS Database Fundamentals course.

In today's data-driven world, organizations need reliable, highly available, and scalable database solutions to manage growing volumes of data. AWS offers a broad portfolio of managed database services tailored for relational, NoSQL, in-memory caching, analytics/warehousing, graph, and time-series workloads. This course gives you practical, hands-on coverage of those services and when to choose each.

What you'll learn

* Core AWS managed database services and their use cases
* Amazon RDS fundamentals, Aurora internals, and RDS Proxy for connection management
* Amazon DynamoDB design patterns, capacity modes, and pricing considerations
* DynamoDB Accelerator (DAX) for ultra-low-latency reads
* Caching and in-memory databases: Amazon ElastiCache and Amazon MemoryDB for Redis
* Data warehousing and analytics with Amazon Redshift (including serverless)
* Graph databases with Amazon Neptune
* Time-series workloads with Amazon Timestream
* Search, analytics, and observability using OpenSearch
* Hands-on experience via browser-based AWS Cloud Labs

Course roadmap (high level)

* Amazon RDS: managed relational databases (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server)
* Amazon Aurora and RDS Proxy: high-performance, compatible relational engine with connection pooling
* Amazon DynamoDB: fully managed NoSQL key-value and document store
* DAX: in-memory cache for DynamoDB to reduce read latency
* Amazon ElastiCache (Redis/Memcached) and Amazon MemoryDB for Redis
* Amazon Redshift: analytics, data warehousing (including serverless)
* Amazon Neptune: graph database for connected datasets
* Amazon Timestream: purpose-built time-series database for IoT and monitoring
* OpenSearch: search, log analytics, and observability

Key AWS database services at a glance

| Service                    | Primary use case                                              | Quick reference                                                                            |
| -------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Amazon RDS                 | Managed relational databases, automated backups, multi-AZ     | [https://aws.amazon.com/rds/](https://aws.amazon.com/rds/)                                 |
| Amazon Aurora              | High-performance, MySQL/Postgres-compatible relational engine | [https://aws.amazon.com/rds/aurora/](https://aws.amazon.com/rds/aurora/)                   |
| RDS Proxy                  | Connection pooling and improved application scalability       | [https://docs.aws.amazon.com/rds/](https://docs.aws.amazon.com/rds/)                       |
| Amazon DynamoDB            | Serverless NoSQL key-value and document store                 | [https://aws.amazon.com/dynamodb/](https://aws.amazon.com/dynamodb/)                       |
| DynamoDB Accelerator (DAX) | In-memory caching for DynamoDB reads                          | [https://docs.aws.amazon.com/amazondynamodb/](https://docs.aws.amazon.com/amazondynamodb/) |
| Amazon ElastiCache         | In-memory caching (Redis or Memcached)                        | [https://aws.amazon.com/elasticache/](https://aws.amazon.com/elasticache/)                 |
| Amazon MemoryDB for Redis  | Durable, Redis-compatible in-memory database                  | [https://aws.amazon.com/memorydb/](https://aws.amazon.com/memorydb/)                       |
| Amazon Redshift            | Data warehousing and analytics (serverless option)            | [https://aws.amazon.com/redshift/](https://aws.amazon.com/redshift/)                       |
| Amazon Neptune             | Managed graph database for highly connected data              | [https://aws.amazon.com/neptune/](https://aws.amazon.com/neptune/)                         |
| Amazon Timestream          | Time-series data for IoT, metrics, and monitoring             | [https://aws.amazon.com/timestream/](https://aws.amazon.com/timestream/)                   |
| OpenSearch                 | Search, log analytics, and observability                      | [https://opensearch.org/](https://opensearch.org/)                                         |

Deep dives and hands-on focus

* Amazon RDS: We'll cover provisioning, high availability (Multi-AZ), read replicas, backup and restore strategies, and performance tuning basics.
* Amazon Aurora & RDS Proxy: Understand Aurora's storage architecture, cluster endpoints, reader/writer separation, and how RDS Proxy reduces connection storms and improves pooling for serverless or microservices architectures.
* Amazon DynamoDB: Learn data modeling for single-table design, partition keys, secondary indexes, capacity modes (on-demand vs. provisioned), and cost trade-offs.
* DAX: When and how to add DAX for sub-millisecond read performance; trade-offs around consistency and cache invalidation.
* Caching (ElastiCache & MemoryDB): Compare Redis vs. Memcached patterns, clustering, persistence options, and how MemoryDB adds durability to in-memory workloads.
* Redshift: Query performance, distribution styles, sort keys, concurrency scaling, and using Redshift Serverless for ad-hoc analytics.
* Neptune

<Frame>
  <img alt="A presentation slide showing AWS Neptune global database architecture with a world map marking a primary region and several secondary regions, and a diagram of primary/secondary DB clusters with storage, reader, and writer nodes. A small presenter video thumbnail is visible in the corner." />
</Frame>

— architecture and graph models (Property Graph with Gremlin and RDF/SPARQL) for use cases such as social graphs, recommendations, and fraud detection.

* Timestream and OpenSearch

<Frame>
  <img alt="A presentation slide titled &#x22;Why do we need Time-Series Database?&#x22; showing three colorful icons (a connected car, sensors/devices, and a camera) feeding into a central cylindrical database graphic. A small circular presenter video thumbnail appears in the bottom-right." />
</Frame>

— Timestream for time-series ingestion, storage tiers, and querying; OpenSearch for full-text search, log analytics, and observability pipelines.

Hands-on learning: AWS Cloud Labs

<Callout icon="lightbulb">
  This course emphasizes hands-on learning through AWS Cloud Labs. Cloud Labs provide short-lived, browser-based access to AWS infrastructure so you can complete exercises safely and without managing your own cloud account. They let you practice provisioning, configuring, and experimenting with services while following the lesson material step-by-step.
</Callout>

Community and support
At KodeKloud, community engagement is an important part of learning. Use the course forum to ask questions, share insights, and collaborate with peers and instructors.

<Callout icon="warning">
  Hands-on labs simulate real environments. If you run your own AWS account outside of the lab environment, monitor resource usage and cost—especially for long-running RDS instances, Redshift clusters, and large ElastiCache nodes.
</Callout>

Related KodeKloud courses and further learning

* [Linux Professional Institute LPIC-1 Exam 101](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101)
* [AZ-104: Microsoft Azure Administrator (Updated)](https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator)
* [Open Source for Beginners](https://learn.kodekloud.com/user/courses/open-source-for-beginners)

Join us on this journey through AWS databases. Enroll now to gain practical skills in managed database services, caching, analytics, graph and time-series databases, and search/observability.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/00cedd0b-10e0-4a33-8fb2-8a0f3bc51fb9/lesson/31a08734-9e2c-42e2-ba34-688582a41f16" />
</CardGroup>
