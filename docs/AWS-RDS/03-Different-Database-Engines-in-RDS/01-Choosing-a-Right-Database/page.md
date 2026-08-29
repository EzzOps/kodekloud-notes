# Choosing a Right Database

Source: https://notes.kodekloud.com/docs/AWS-RDS/Different-Database-Engines-in-RDS/Choosing-a-Right-Database/page

Guidance on selecting databases based on workload, compatibility, scaling, operational and ML needs, recommending MySQL/MariaDB, Oracle/SQL Server, or PostgreSQL for common scenarios

Choosing the right database requires balancing application requirements, traffic patterns, operational constraints, and any analytics or machine learning (ML) needs. Key decision drivers include expected concurrency and throughput, transactional guarantees (ACID vs eventual consistency), existing vendor dependencies, and your scaling strategy (vertical vs horizontal).

<Callout icon="lightbulb">
  When selecting a database, evaluate these key factors first: expected traffic and concurrency, transactional guarantees (ACID vs eventual consistency), existing application dependencies (Oracle/MSSQL), scaling strategy (vertical vs horizontal), and any ML or analytical requirements.
</Callout>

Guidelines for common scenarios

* Small or low-activity back-end services / microservices\
  For services with modest traffic and primarily OLTP (online transaction processing) needs, MySQL or MariaDB are reliable, easy-to-operate choices. They have broad ecosystem support and are well-suited to small-to-medium microservices where predictable transactional performance is required. If reducing operational overhead is a priority, consider managed offerings such as [AWS RDS](https://learn.kodekloud.com/user/courses/aws-rds) or Amazon Aurora.

* Applications that must integrate with Oracle or Microsoft SQL Server\
  If you have legacy applications or third-party software that depend on Oracle or MS SQL Server features, using the same engine (on a managed platform like [AWS RDS](https://learn.kodekloud.com/user/courses/aws-rds)) preserves compatibility and minimizes migration risk. This avoids costly rewrites and preserves application behavior when moving to the cloud.

* High-traffic, user-facing systems or ML-enabled workloads\
  PostgreSQL is a strong candidate for high-throughput, user-facing systems and workloads that benefit from advanced data types or ML-friendly extensions. PostgreSQL scales for many workloads and has a rich extension ecosystem—examples include [PostGIS](https://postgis.net/) for geospatial data and [pgvector](https://pgvector.org/) for vector embeddings—making it a common choice for feature stores and ML pipelines. Managed PostgreSQL (and Aurora PostgreSQL) can simplify high-availability and scaling.

Operational and licensing considerations

* Managed database services (RDS, Aurora) reduce operational effort for backups, failover, patching, and point-in-time recovery.
* Licensing and total cost: Oracle and SQL Server typically have licensing costs—factor these into migration and TCO analyses.
* For extreme horizontal scaling, very large analytical workloads, or highly specialized access patterns, consider purpose-built NoSQL or analytic databases. For most structured OLTP use cases, MySQL/MariaDB, Oracle/SQL Server (for compatibility), and PostgreSQL cover the common needs.

Quick comparison table

| Use Case                          | Recommended Engines                  | Why / Notes                                                                          |
| --------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------ |
| Small/low-activity microservices  | MySQL, MariaDB                       | Simple OLTP, wide ecosystem, low operational complexity; consider managed RDS/Aurora |
| Legacy/enterprise compatibility   | Oracle, Microsoft SQL Server         | Preserves behavior for existing apps; managed offerings reduce migration effort      |
| High-traffic / ML-capable systems | PostgreSQL (incl. Aurora PostgreSQL) | Rich extensions (PostGIS, pgvector), good for feature stores, analytics-friendly     |

Summary

* Small/medium transactional services: MySQL or MariaDB (consider managed offerings).
* Legacy/compatibility-driven migrations: Oracle or SQL Server on managed platforms to minimize risk.
* High-traffic, ML-capable systems: PostgreSQL for extensibility and ML integration.

Further reading and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [PostGIS](https://postgis.net/) — geospatial extension for PostgreSQL
* [pgvector](https://pgvector.org/) — vector similarity for PostgreSQL
* [AWS RDS](https://learn.kodekloud.com/user/courses/aws-rds) — managed relational database service

<Frame>
  <img alt="A diagram showing a &#x22;Structured Database&#x22; on the left branching to three use-case boxes on the right. The boxes label recommended databases: small microservices (MySQL, MariaDB), Microsoft/Oracle-compatible apps (Oracle, Microsoft SQL Server), and high-availability/ML use (PostgreSQL)." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/0525aa45-ab52-4496-8a27-0ab6ec827d6f/lesson/d25cf5e2-57d4-4db1-ac10-b8891d689d3c" />
</CardGroup>
