# Database Migration Service

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/Migrations-Security/Database-Migration-Service/page

Overview of AWS Database Migration Service, its tools and components for migrating and continuously replicating databases to AWS with minimal downtime and schema conversion support

This article describes AWS Database Migration Service (DMS): a managed service for migrating and continuously replicating databases and analytics workloads to AWS. DMS minimizes downtime and reduces data loss during migrations. Conceptually, DMS is to databases what [AWS Application Migration Service](https://aws.amazon.com/application-migration-service/) is to servers — a purpose-built toolset optimized for moving data stores and their schemas.

DMS supports more than twenty database and analytics engines, including MySQL, PostgreSQL, Oracle, Microsoft SQL Server, MongoDB, Amazon Redshift, and Amazon DocumentDB.

## DMS architecture and components

DMS is built from several cooperating components that discover source systems, convert schemas when needed, and replicate data from source to target. The sections below walk through each major component and show where it fits in a typical migration workflow.

### DMS Fleet Advisor

DMS Fleet Advisor performs discovery and metadata collection across database environments to help plan migrations. You deploy a lightweight data collector on database hosts (for example, on-premises MySQL or SQL Server). The collector inventories schemas, objects, and configurations and sends metadata to DMS for analysis. You can export results (CSV) for offline planning and effort estimation.

<Frame>
  <img alt="A diagram titled &#x22;DMS Components – DMS Fleet Advisor&#x22; showing data flowing from a Data Center via a DMS Data Collector into S3, then to AWS DMS and out to an Export CSV. A dashed loop labeled &#x22;Continues Discovery&#x22; indicates ongoing discovery between the components." />
</Frame>

Think of Fleet Advisor as the discovery and inventory phase: it helps you understand what you have, estimate complexity, and prioritize conversion effort.

### Schema Conversion Tool (SCT)

The AWS Schema Conversion Tool (SCT) analyzes your source database and flags schema objects, stored procedures, and other constructs that require conversion for a heterogeneous migration. SCT can automate many conversions and generates a report of items needing manual intervention. It also supports data type mappings and can generate a migration plan for use with DMS.

SCT is especially useful for heterogeneous migrations (for example, Oracle → PostgreSQL or an enterprise data warehouse → Amazon Redshift), where database constructs and data types differ.

### Replication instance and endpoints

The replication instance is the managed compute resource that runs DMS replication tasks. It reads data from source endpoints, applies any configured transformations, and writes to target endpoints. Choose replication instance capacity based on expected throughput and latency requirements.

An endpoint is a configuration that describes a source or target data store. Endpoint settings include:

* Endpoint type: `source` or `target`
* Engine type: e.g., MySQL, PostgreSQL, Oracle
* Server host/IP and port
* Encryption configuration (TLS certificates, if required)
* Authentication credentials

Before you create tasks, ensure network connectivity (VPC/subnets, routing, security groups) and authentication details are in place so the replication instance can reach each endpoint.

<Frame>
  <img alt="An infographic titled &#x22;DMS Components – Replication Instance&#x22; showing a purple DMS endpoint icon and a gray panel of five circular icons labeled Source or Target, DB Type, Server Name and port, Encryption, and Credentials. The graphic summarizes endpoint info for a replication instance." />
</Frame>

<Callout icon="lightbulb">
  When configuring endpoints, verify network access (VPC, routing, security groups) and confirm credentials and any required certificates. Missing network routes or incorrect authentication are common causes of connection failures.
</Callout>

### Replication tasks and migration modes

A replication task is the job that moves and/or replicates data between a source endpoint and a target endpoint. When creating a task you select:

* The replication instance
* Source and target endpoints
* A migration type (mode)
* Table mappings and optional transformation rules

Tasks are start/stop/pause capable and expose progress metrics and logs for monitoring and troubleshooting.

|  Migration mode | Description                                                                                              | When to use                                                                                            |
| --------------: | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
|       Full load | Copies existing data from source to target as an initial bulk transfer                                   | For initial migrations where downtime for a bulk copy is acceptable                                    |
| Full load + CDC | Performs an initial full load and captures ongoing changes (Change Data Capture) to apply after the load | To minimize downtime: bulk load then keep source and target synchronized until cutover                 |
|        CDC only | Captures and applies only ongoing changes                                                                | When you handle the initial bulk copy with another tool and use DMS for continuous sync during cutover |

<Frame>
  <img alt="A slide titled &#x22;DMS Components – Replication Task&#x22; showing a source endpoint, DMS endpoint, and target endpoint connected by a Task arrow. On the right is a Replication Instance box listing three modes: Full Load, Full load + CDC, and CDC Only." />
</Frame>

Use the Full load + CDC pattern to reduce application downtime: perform the initial load while the source remains live, capture ongoing changes during the migration, and cut over once target lag is acceptable.

<Callout icon="warning">
  Always validate data consistency and plan for cutover testing. Network latency, LOBs/large objects, and unsupported data types can introduce replication delays or require manual reconciliation.
</Callout>

### Automatic schema conversion and mappings

For heterogeneous migrations, pair DMS with SCT. SCT converts schema objects and helps define mappings (for example, mapping Oracle `VARCHAR2` to PostgreSQL `VARCHAR`). SCT attempts automated conversions and flags objects that need manual work. DMS focuses on data movement and CDC — SCT handles the schema and code translation.

<Frame>
  <img alt="Diagram titled &#x22;Schema Conversion&#x22; showing an on-premises/corporate Oracle instance routed through a central Schema Conversion Tool (SCT) and converted to AWS Cloud targets, including an Oracle instance and Amazon Redshift." />
</Frame>

## Key terminology (recap)

* Endpoint: A source or destination database configuration used by DMS.
* Replication instance: The compute resource that runs replication tasks.
* Task: The migration job that moves data and/or applies ongoing changes between endpoints.
* CDC (Change Data Capture): The mechanism that captures and applies ongoing changes from the source to the target.

## Common use cases

DMS is used for a variety of migration and replication scenarios:

| Use case                            | Description                                                                               | Examples                                            |
| ----------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Migrate production databases to AWS | Move on-premises or cloud databases to managed AWS targets with minimal downtime          | RDS MySQL, Amazon Aurora, Amazon RDS for SQL Server |
| Continuous replication (CDC)        | Keep source and target synchronized during migration or for ongoing replication workflows | Active-active replication, read scaling             |
| Load data into analytics platforms  | Ingest data into data warehouses and data lakes for analytics                             | Amazon Redshift, S3-based lakehouses                |

<Frame>
  <img alt="A presentation slide titled &#x22;Use Cases&#x22; with three numbered cards labeled &#x22;Migrate Data&#x22;, &#x22;CDC&#x22;, and &#x22;Data Lake.&#x22; Each card features a purple circular icon representing the respective data-related use case." />
</Frame>

## Putting it all together

DMS, Fleet Advisor, and SCT form a complementary toolkit:

* Fleet Advisor discovers and inventories your database estate so you can estimate migration effort.
* SCT converts schemas and application code for heterogeneous targets.
* DMS performs data movement and CDC to keep source and target synchronized with minimal downtime.

Plan a migration by discovering with Fleet Advisor, convert schemas with SCT where needed, and execute replication tasks on appropriately sized replication instances. Monitor logs and metrics, validate data, and run cutover tests before switching production traffic to the target.

## Links and references

* [AWS Database Migration Service documentation](https://docs.aws.amazon.com/dms/)
* [AWS Schema Conversion Tool documentation](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/Welcome.html)
* [AWS DMS Fleet Advisor overview](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_FleetAdvisor.html)
* [Amazon Redshift](https://aws.amazon.com/redshift/)
* [Amazon S3](https://aws.amazon.com/s3/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/79ca746d-b567-4dae-92cd-e572992ff80e/lesson/d761aaa1-f331-4966-beae-4b97768ea898" />
</CardGroup>
