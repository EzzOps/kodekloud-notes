# Redshift Main

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-2/Redshift-Main/page

Overview of Amazon Redshift, its architecture, features, use cases, and operational best practices for building and running analytical data warehouses on AWS.

In this lesson we explore Amazon Redshift: what it is, why you would use it, and the core concepts to design and operate an analytical data warehouse on AWS.

To understand Redshift, first review what a data warehouse is and how it differs from a traditional transactional database.

What is a data warehouse?

* Purpose-built to consolidate data from many sources—databases, logs, streaming systems, and cloud storage—into a unified, queryable repository.
* Optimized for analytical workloads: complex queries, aggregations, reporting and historical analysis over large datasets.
* Often includes ETL (extract, transform, load) capabilities to clean and transform data on ingestion, ensuring consistent data for analytics.
* Designed to scale compute and storage independently and to retain historical data for trend analysis and BI.

Why a data warehouse vs. a transactional database

| Characteristic     |                Transactional (OLTP) | Data Warehouse (Analytical)                  |
| ------------------ | ----------------------------------: | -------------------------------------------- |
| Typical operations |     Many small INSERT/UPDATE/DELETE | Large reads, aggregations, complex joins     |
| Optimization       |   Low-latency single-row operations | Scan throughput, compression, parallelism    |
| Storage layout     |                        Row-oriented | Columnar                                     |
| Use cases          | Operational systems, real-time OLTP | Reporting, BI, forecasting, analytics        |
| Scaling            |              Often scale vertically | Designed for distributed/MPP and large scale |

<Frame>
  <img alt="A slide titled &#x22;Why do we need Data Warehouse?&#x22; with an illustration of people working on a hexagonal data grid and stacked servers. To the right are colored boxes listing benefits like Data Integration, Optimized for Analytics, Historical Analysis, Data Transformation, Structured Data, Scalability, and Cost Efficiency." />
</Frame>

What is Amazon Redshift?
Amazon Redshift is a fully managed, petabyte-scale data warehouse service on AWS. It provides an enterprise-class, columnar relational engine optimized for analytics and integrates with a broad ecosystem of BI, reporting, and data tools. Redshift focuses on efficient storage, compression, and query performance for large analytical workloads.

Core Redshift components

| Component     | Role and notes                                                                                                                                                                                              |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Clusters      | The basic compute infrastructure. A cluster contains a leader node and one or more compute nodes.                                                                                                           |
| Leader node   | Parses SQL, creates query plans, compiles code, distributes work to compute nodes, aggregates results, and returns results to the client.                                                                   |
| Compute nodes | Execute query fragments and store data. Each node has CPU, memory, and local storage defined by its node type.                                                                                              |
| Storage       | Redshift Managed Storage (e.g., RA3/serverless) uses Amazon S3 for durable, petabyte-scale storage while local SSDs provide a high-performance cache. Older provisioned nodes use locally-attached storage. |
| Databases     | A cluster can host one or more databases running the Redshift SQL engine.                                                                                                                                   |

<Frame>
  <img alt="A labeled diagram titled &#x22;AWS Redshift – Components&#x22; showing Amazon Redshift serverless or provisioned architecture with a cloud-based serverless data warehouse and a cluster containing a leader node and multiple compute nodes. It also shows storage integrations (Redshift managed storage and Amazon S3) and a data-sharing cluster." />
</Frame>

Compatibility and design considerations
Redshift is based on PostgreSQL and supports many PostgreSQL client tools and SQL constructs. However, Redshift includes implementation differences and SQL extensions tailored for analytical processing. When migrating or developing for Redshift, focus on Redshift-specific performance practices:

* Distribution keys and distribution styles to co-locate rows used together.
* Sort keys to optimize range-restricted and equality queries.
* COPY command optimizations for high-performance bulk loading from S3 or other sources.
* Compression encodings and vacuum/ANALYZE patterns to maintain performance.

> **lightbulb** Redshift is PostgreSQL-compatible for many client tools and SQL constructs, but it has its own performance and distribution characteristics. Test queries and indexing/distribution strategies in Redshift rather than assuming PostgreSQL defaults.

Key Redshift features and capabilities

* Columnar storage: Reads only needed columns to reduce I/O for analytics.
* Massively parallel processing (MPP): Distributes query execution across compute nodes for large-scale performance.
* Compression: Automatic sampling and recommended encodings minimize storage and I/O.
* Elastic scaling: Add or remove nodes, change node types, or use Redshift Managed Storage (RA3/serverless) to decouple compute and storage scaling.
* Integration and ingestion: Native COPY from Amazon S3, integrations with RDS, EMR, data pipelines, and compatibility with common BI tools.
* SQL support: Standard SQL and Redshift-specific enhancements for analytics.
* Security: AES-256 encryption at rest, SSL/TLS in transit, IAM integration, and fine-grained access controls, including column-level permissions.
* High availability and backups: Automated/manual snapshots, replication options, and features to minimize downtime.
* Workload management: Query queues, resource allocation, concurrency scaling, and tools to monitor and tune performance.

Common Redshift use cases

* Forecasting and analytics: Financial, demand, and trend forecasting often tied into ML workflows.
* Secure data sharing: Share curated datasets across accounts, organizations, and partners.
* Business intelligence: Power dashboards and reports with QuickSight, Tableau, Looker, Power BI.
* Centralized analytics: Consolidate logs and operational data to simplify analytics and multi-language access.

<Frame>
  <img alt="A presentation slide titled &#x22;Redshift – Use Cases&#x22; with four colorful panels. Each panel lists a use case: improve financial and demand forecasts; collaborate and share data; optimize business intelligence; and increase developer productivity." />
</Frame>

Summary — what to remember about provisioned Redshift

* Node types and roles: Leader node (query coordination and planning) and compute nodes (data storage and query execution).
* Storage and performance: Columnar storage, MPP architecture, compression encodings, and local caches enable fast analytics at scale.
* Security and availability: Encryption (AES-256), secure transport (SSL/TLS), fine-grained IAM/column access, and automated snapshots/backups.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary Redshift Provisioned&#x22; with a brief overview of Amazon Redshift. It states Redshift is a fully managed, petabyte-scale cloud data warehouse and outlines node types (leader and compute nodes) and their roles." />
</Frame>

Additional highlights and operational tips

* Automatic sampling and compression help reduce storage costs and improve query performance without manual tuning.
* Fine-grained access controls and IAM integration protect sensitive columns and datasets.
* Automatic cluster scaling features (concurrency scaling, elastic resize, managed-storage autoscaling) provide headroom for query peaks and unpredictable workloads.
* Use automated and manual snapshots for point-in-time recovery and compliance-driven retention.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary Redshift Provisioned&#x22; with a turquoise left panel and three numbered highlights on the right. The points note AES-256/SSL encryption, fine-grain column-level access controls, and automatic cluster capacity scaling." />
</Frame>

References and further reading

* AWS Redshift documentation: [https://docs.aws.amazon.com/redshift/](https://docs.aws.amazon.com/redshift/)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Redshift best practices and performance tuning guides: [https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/6b775562-0b27-41e9-93fc-bb16dab05d87/lesson/40c10aa9-8805-4ec8-a7e2-ba1e195d0176)
