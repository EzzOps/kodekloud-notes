# Cloud SQL

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Cloud-SQL/page

Overview of Google Cloud SQL, a fully managed relational database service that automates maintenance, backups, replication, and offers high availability, engine choices, monitoring, and secure connectivity.

Hello and welcome back.

In this lesson we'll explore Cloud SQL on Google Cloud: a fully managed relational database service that removes much of the operational burden of running databases. For data engineers, Cloud SQL simplifies provisioning, maintenance, backups, replication, and recovery so your team can focus on schema design, query tuning, and application integration.

Cloud SQL automates many operational tasks—engine patch management, automated backups, replication and failover across zones for high availability, and point-in-time recovery (PITR) where the engine supports it (for example, MySQL and PostgreSQL). It supports widely used database engines (MySQL, PostgreSQL, and SQL Server), making migrations or hybrid deployments straightforward when your organization already uses one of these engines.

<Frame>
  <img alt="A presentation slide titled &#x22;Cloud SQL – Overview&#x22; with a blue Cloud SQL logo on the left. Three text boxes on the right summarize that Google Cloud SQL is a fully managed relational database service that automates tasks like patching, backups and replication and supports popular database engines." />
</Frame>

If you’re evaluating Cloud SQL, consider these engine capabilities and compatibility factors. The most common choices are:

| Engine     | Typical use cases                                          | Notes                                                                     |
| ---------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| MySQL      | Web applications, LAMP stacks, open-source ecosystems      | Widely supported; good for many transactional workloads                   |
| PostgreSQL | Standards compliance, advanced SQL features, extensibility | Excellent for complex queries, GIS, and custom extensions                 |
| SQL Server | Windows-centric enterprise apps, .NET workloads            | Best integration with Microsoft tools and existing SQL Server deployments |

<Frame>
  <img alt="The image is a slide titled &#x22;Cloud SQL Database Engines – Overview&#x22; showing a hexagonal cloud SQL icon on the left. On the right it lists three database engines — MySQL, PostgreSQL, and SQL Server — with brief descriptions of each." />
</Frame>

Core concepts when creating a Cloud SQL instance

* Choose the database engine and exact engine version that matches your application dependencies.
* Select the region (and optionally a zone) to minimize latency by placing data near your application and users.
* Pick a machine type (shared-core or dedicated) to define vCPU and memory characteristics.
* Choose storage type: SSD for higher throughput and IOPS, HDD for lower-cost, less I/O-intensive workloads.
* Set initial storage capacity and enable auto storage increase so instances grow automatically instead of hitting full-disk outages.
* Configure high availability (regional primary/standby with automatic failover) for production-critical systems.
* Add read replicas where needed (available for MySQL and PostgreSQL) to scale read traffic.
* Configure backups, automated maintenance windows, and, where supported, point-in-time recovery (PITR).

> **lightbulb** Enable auto storage increase and consider high availability for production instances. These are common best practices for preventing outages and meeting availability and recovery requirements.

Cloud SQL also integrates with Google Cloud monitoring and logging, IAM-based access control, and network options:

* Monitoring & logging: Use Cloud Monitoring and Cloud Logging to track performance metrics, CPU/Memory utilization, connections, and slow queries.
* Security & access: Enforce IAM roles, use private IP or Cloud SQL Proxy for secure connectivity, and enable SSL/TLS for client connections.
* Backup & recovery: Configure automated daily backups and use PITR (when supported) to restore to a specific point in time.
* Maintenance: Define maintenance windows so optional patching and engine version upgrades occur at a predictable time.

<Frame>
  <img alt="A diagram titled &#x22;Cloud SQL — Instance Management&#x22; showing options for creating Cloud SQL instances. It lists configurable choices like database engine (MySQL, PostgreSQL, SQL Server), versions, region/zone, machine type, storage type (SSD/HDD) and capacity." />
</Frame>

Next steps and further reading

* If you need global scale and strong consistency across regions, the next lesson covers Cloud Spanner (a globally distributed relational database).
* For guided setup and migration patterns, review the Cloud SQL documentation and Cloud SQL migration guides.

Links and references

* [Cloud SQL documentation](https://cloud.google.com/sql)
* [Cloud SQL best practices and high availability](https://cloud.google.com/sql/docs/mysql/high-availability)
* [Cloud Monitoring](https://cloud.google.com/monitoring)
* [Cloud Logging](https://cloud.google.com/logging)

Speak with you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/62f80d2f-49f3-45dd-8486-09edece8de52)
