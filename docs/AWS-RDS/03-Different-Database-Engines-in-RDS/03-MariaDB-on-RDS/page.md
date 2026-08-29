# MariaDB on RDS

Source: https://notes.kodekloud.com/docs/AWS-RDS/Different-Database-Engines-in-RDS/MariaDB-on-RDS/page

Overview of running MariaDB on Amazon RDS highlighting MySQL compatibility, managed high availability, scaling options, simpler operations, and suitability for development, staging, and production workloads

MariaDB is an open-source fork of MySQL that offers a familiar, easy-to-use relational database engine. It is a solid choice for development, proof-of-concept (POC), QA, and staging environments, and it is also production-capable. MariaDB strikes a balance between functionality and simplicity: it supports a broad set of data types, indexing options, and storage engines while typically presenting lower operational complexity and a gentler learning curve than some more feature-rich databases.

Why choose MariaDB on RDS?

* Drop-in MySQL compatibility: migration from MySQL is usually straightforward, minimizing application changes and developer retraining.
* Simpler operations: compared with PostgreSQL, MariaDB can be easier to administer for teams that do not need PostgreSQL’s advanced features.
* Production readiness: supports replication, clustering, and read-scaling strategies suitable for many production workloads.
* Managed benefits on RDS: automated backups, Multi-AZ failover, read replicas, and managed patching reduce operational overhead.

Compatibility and migration
MariaDB is often selected as a drop-in replacement for MySQL. That compatibility simplifies migrations and preserves existing tooling and developer workflows. If your team already has MySQL expertise but wants additional features, performance improvements, or specific storage engines, MariaDB is a practical alternative.

Feature comparison (at-a-glance)

| Database   | Typical Use Case                                             | Strengths                                                   |
| ---------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| MariaDB    | Development, staging, production (lighter operational model) | MySQL compatibility, multiple storage engines, simpler ops  |
| MySQL      | Web apps, general-purpose OLTP                               | Broad ecosystem, strong vendor support                      |
| PostgreSQL | Advanced analytics, complex queries, extensibility           | Advanced SQL features, extensibility, strong data integrity |

High availability, scaling, and clustering
MariaDB supports a variety of HA and scaling approaches:

* Built-in replication for primary-replica topologies.
* Clustering options such as Galera Cluster for synchronous multi-master setups (deployment-specific).
* Read replicas for scaling read-heavy workloads.

When you run MariaDB on a managed service such as Amazon RDS, you gain additional operational features like automated backups, Multi-AZ failover for high availability, automated minor version upgrades, and managed patching.

> **lightbulb** On [Amazon RDS](https://aws.amazon.com/rds/) specifically, MariaDB is supported with managed Multi-AZ deployments for high availability and automated backups. RDS also allows read replicas for scaling read workloads and handles routine maintenance tasks such as OS and database patching. Check the [RDS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MariaDB.html) for supported MariaDB versions and regional availability.

In conclusion, MariaDB presents itself as an optimal

<Frame>
  <img alt="A presentation slide showing four use-cases for a MySQL-compatible open-source database: feature-rich relational DB, drop-in MySQL replacement, open-source/MySQL ecosystem compatibility, and high availability/scalability—each paired with a colorful circular icon." />
</Frame>

choice when you need a feature-rich, MySQL-compatible open source database but prefer a simpler operational model than PostgreSQL. It fits across a spectrum of projects—from small-scale apps and developer environments to production deployments that require managed high availability and horizontal scaling.

Quick example: creating a MariaDB instance on RDS using the AWS CLI

```Expected Output: theme={null}
bash
aws rds create-db-instance \
  --db-instance-identifier my-mariadb \
  --engine mariadb \
  --allocated-storage 20 \
  --db-instance-class db.t3.medium \
  --master-username admin \
  --master-user-password <password> \
  --multi-az \
  --backup-retention-period 7
```

Links and references

* Amazon RDS: [https://aws.amazon.com/rds/](https://aws.amazon.com/rds/)
* RDS MariaDB documentation: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP\_MariaDB.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MariaDB.html)
* Galera Cluster: [https://galeracluster.com/](https://galeracluster.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/0525aa45-ab52-4496-8a27-0ab6ec827d6f/lesson/4201ec45-5ec3-44e1-9505-e5bd40377eb5)
