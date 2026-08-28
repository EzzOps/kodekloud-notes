# Creating Read Replicas

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/Creating-Read-Replicas/page

Guide to creating and managing Amazon RDS read replicas, provisioning options, operational best practices, promotion, replication behavior, and choosing Aurora versus standard RDS for read scaling

This guide shows how to create read replicas manually for an existing Amazon RDS instance and how to provision read-capable instances at database creation time. It focuses on RDS for PostgreSQL examples, but the operational concepts apply to other supported engines (MySQL, MariaDB, Aurora).

## Prerequisites

* An existing RDS instance (Primary) in the Available state.
* Appropriate IAM permissions to view and modify RDS instances.
* VPC/networking access for any replica instances (same or different region).

## 1 — Create a primary DB (example: PostgreSQL)

To create a simple primary instance for this demo:

* Go to RDS Console → Create database → Standard create.
* Choose Engine: PostgreSQL.
* Select a template (e.g., Dev/Test).
* Provide a DB identifier and click Auto generate password (or enter your own).
* Leave instance configuration and other options at defaults for the demo, then choose Create database.

Before creating the DB, review the connectivity and networking settings:

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the RDS &#x22;Connectivity&#x22; settings for a database—options for EC2 compute connection, VPC selection, DB subnet group, public access, and VPC security groups. The right panel displays PostgreSQL information/documentation." />
</Frame>

Once created, the primary accepts both reads and writes. If you need to scale read throughput or isolate read-heavy queries, add one or more read replicas.

## 2 — Create a read replica from the primary

Wait until the primary is in the Available state, then:

* In the RDS Console select the primary DB instance.
* From Actions choose Create read replica.
* Enter a DB instance identifier (for example, `read-replica-01`).
* Configure the replica: choose instance class, storage type, destination region (for cross-region replicas), and any other options. The read replica can use different compute and storage settings than the primary so you can optimize for read workloads.
* Click Create read replica.

Example selection showing the replica identifier and instance/storage choices:

<Frame>
  <img alt="A screenshot of the AWS RDS &#x22;create DB instance&#x22; configuration page showing the DB instance identifier &#x22;read-replica-01&#x22;, instance class set to db.m5d.large, destination region EU (Frankfurt), and storage type General Purpose SSD (gp3). The page displays other instance options like class categories and a selection box for previous generation classes." />
</Frame>

When provisioning begins, RDS sets up replication from the primary to the replica. The RDS console shows both instances and their statuses. While the replica is being provisioned you may see statuses such as Creating or Modifying:

<Frame>
  <img alt="A screenshot of the AWS RDS Databases console showing upgrade/deprecation warnings and a Blue/Green deployment suggestion. The database table lists two PostgreSQL instances: &#x22;database-1&#x22; (Available, Primary) and &#x22;read-replica-01&#x22; (Modifying, Replica)." />
</Frame>

## Operational details & best practices

* Credentials: A read replica inherits the master username and password from the primary instance. You do not create new credentials when adding a replica.

<Callout icon="lightbulb">
  Read replicas are typically read-only. If you need writes to a replica, you must promote it to a standalone primary; promotion breaks replication and makes the instance writable.
</Callout>

* Promotion: To convert a read replica into a writable primary (useful for DR or planned failover), select the replica and choose Actions → Promote. Promotion removes replication and makes the instance fully writable.
* Multiple replicas: You can create multiple read replicas for the same primary to scale read throughput. Replica chaining (creating a replica from an existing replica) support depends on engine/version—RDS PostgreSQL typically creates replicas from the primary.
* Replication type and lag: RDS PostgreSQL uses physical streaming replication and is asynchronous by default. Expect potential replication lag; cross-region replicas will generally experience higher replication latency.
* Instance sizing: Because replicas serve reads only, choose instance classes and storage tailored to read performance (I/O, network throughput), which may differ from the primary.
* Cost considerations: Each replica is a separate billed instance and associated storage. Factor these costs into capacity planning.

<Callout icon="warning">
  Adding read replicas improves read scalability and availability but increases costs and can introduce replication lag. Test your application’s tolerance for eventual consistency from replicas before relying on them for critical reads.
</Callout>

## 3 — Provisioning read-capable instances at DB creation time

There are two common approaches when you want read-capable instances provisioned as part of database creation:

* Standard RDS engines (PostgreSQL/MySQL): Multi-AZ deployments provide a synchronous standby for high availability, but the standby is not readable. For read replicas you create them after the primary becomes available.
* Amazon Aurora (Aurora MySQL / Aurora PostgreSQL): Aurora uses a DB cluster model with a single primary writer and multiple reader instances (read replicas) that you can create as part of the cluster. Readers are available immediately across AZs.

When creating an Aurora cluster you can choose a Multi-AZ DB cluster option to provision primary and reader instances together. Example selection in the console where a Multi-AZ DB cluster is chosen:

<Frame>
  <img alt="A screenshot of the AWS RDS console showing PostgreSQL instance creation with the &#x22;Dev/Test&#x22; template selected. The &#x22;Multi-AZ DB cluster - new&#x22; deployment option is chosen and a DB cluster identifier field (database-3) is visible." />
</Frame>

### Quick decision table: When to use RDS vs Aurora

| Use case                                                      | Engine / option               | Behavior                                                                     |
| ------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------------- |
| Need immediate readable replicas as part of creation          | Amazon Aurora (DB cluster)    | Reader instances can be created with the cluster and serve reads immediately |
| Need synchronous high availability (standby) but not readable | RDS Multi-AZ (Postgres/MySQL) | Synchronous standby for failover — standby is not readable                   |
| Add replicas after primary creation                           | Standard RDS (Postgres/MySQL) | Create asynchronous read replicas after primary is Available                 |

## Summary

* To add read capacity to an existing RDS database: select the primary DB and use Actions → Create read replica.
* Read replicas inherit master credentials, are read-only, and can be promoted to writable primaries when necessary.
* If you need read replicas provisioned up front, prefer Aurora DB clusters; for standard RDS engines use Multi-AZ for HA (standby not readable) and create read replicas afterward.
* Monitor replication lag and costs, and design your application to handle eventual consistency from replicas.

## Links and references

* [Amazon RDS - Read Replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
* [Amazon Aurora overview](https://docs.aws.amazon.[SECRET_REDACTED]-is-Amazon-Aurora.html)
* [AWS RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)

I hope this guide clarifies how to create and manage read replicas for Amazon RDS and how to choose the right deployment pattern for read scaling.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/875fa570-3063-43cd-a2db-905754937a16" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/9f9c1b46-a86e-4223-a814-523e1bcf077f" />
</CardGroup>
