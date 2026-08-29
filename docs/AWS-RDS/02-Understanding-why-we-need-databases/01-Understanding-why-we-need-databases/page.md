# Understanding why we need databases

Source: https://notes.kodekloud.com/docs/AWS-RDS/Understanding-why-we-need-databases/Understanding-why-we-need-databases/page

Explains why applications need centralized databases, contrasts local storage limits, outlines database types and benefits of cloud managed services like Amazon RDS

Hello and welcome to this lesson. Before we dive into what AWS RDS is and how it works, let’s first understand why applications need a database.

Consider a web application that collects user information. Many users (for example, user01, user02, and so on) submit their data to this application. Where should that data be stored?

* One option is local storage on the application server (for example, the instance's local disk).
* Another option is using a centralized database that multiple application instances can read from and write to.

Local instance storage is simple but has important limitations as applications scale and evolve. When your app runs across multiple servers (Kubernetes pods, EC2 instances, or an Auto Scaling group), instance-local disks are not shared across nodes and are often ephemeral: data can be lost when an instance is terminated or replaced. Cloud block storage (for example, Amazon EBS) or networked file systems can provide persistence, but they add management complexity and availability considerations when many instances must access the same data concurrently. This is why centralized databases are the standard approach for scalable, durable, and consistent data storage.

<Frame>
  <img alt="A slide titled &#x22;Understanding the need for databases&#x22; showing a diagram where two users (User 01 and User 02) send data to a &#x22;User information collection application,&#x22; which then writes to storage options including local storage and databases." />
</Frame>

> **lightbulb** Local (instance) storage is tied to a single server and is not shared. For scalable, durable, and consistent storage across multiple application instances, use a centralized database or a managed storage service.

What makes databases different and necessary?

* Purpose-built for storing and retrieving structured (e.g., tables, rows) and unstructured (e.g., JSON documents) data.
* Provide durability, consistency, backups, and mechanisms for concurrent access.
* Support indexing, querying, transactions, and access controls that simple file storage does not.

Traditionally, organizations hosted databases in on-premises data centers. Running databases on-premises requires dedicated personnel (DBAs, networking engineers) and continuous maintenance (patching, backups, high availability). Because of the operational overhead and capital expenses, many organizations—especially startups—migrate databases to the cloud as part of digital transformation.

Data volume and application requirements change over time. Different workloads need different database characteristics, so projects often adopt multiple database technologies ("polyglot persistence") to optimize for specific use cases.

<Frame>
  <img alt="A slide titled &#x22;On Premises Data Centre&#x22; showing a row of server racks/network inside a dashed on-premises boundary. Surrounding boxes display database logos: MySQL, PostgreSQL, MariaDB, Oracle and Microsoft SQL Server." />
</Frame>

## Common database types and when to use them

| Database Type     | Use Case                                                        | Example                          |
| ----------------- | --------------------------------------------------------------- | -------------------------------- |
| Relational (SQL)  | Transactional systems requiring ACID, joins, structured schemas | MySQL, PostgreSQL, Aurora        |
| Key-value         | Fast lookups, caching, session storage                          | Redis, DynamoDB (key-value mode) |
| Document (NoSQL)  | Flexible schemas, hierarchical data, rapid iteration            | MongoDB, Couchbase               |
| Analytical / OLAP | Large-scale reporting, data warehousing                         | Amazon Redshift, Snowflake       |

> **warning** Selecting the wrong database for a workload can cause performance, cost, and maintenance issues. Evaluate data access patterns, consistency requirements, and operational overhead before choosing a solution.

Given these challenges and the desire to reduce on-premises operational overhead, cloud-managed database services provide compelling advantages:

* Managed backups, automated patching, and built-in monitoring.
* Simplified scaling (vertical and horizontal) with less operational effort.
* High availability and automated failover options.
* Integration with other cloud services and security controls.

AWS offers a managed relational database service—Amazon RDS (Relational Database Service)—that helps organizations run databases in the cloud without most of the operational burden of managing underlying infrastructure. In the next lesson, we’ll explore the key benefits of Amazon RDS, supported engines, and when to choose it versus other database options.

## Links and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Amazon EC2 documentation](https://docs.aws.amazon.com/ec2/index.html)
* [Amazon EBS](https://aws.amazon.com/ebs/)
* [Amazon RDS product page](https://aws.amazon.com/rds/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/bfb32eae-f423-4a2e-9ca1-60adc0ac3ff0/lesson/328ac9f3-aaa9-46ad-ad45-6d1b0e3a25a4)
