# Setting up Managing Aurora

Source: https://notes.kodekloud.com/docs/AWS-RDS/AWS-Aurora/Setting-up-Managing-Aurora/page

Guide to creating and managing Aurora PostgreSQL clusters in the RDS console, covering cluster creation, endpoints, storage, replication, scaling, and monitoring tips

Welcome back. In this lesson we’ll walk through creating an Amazon Aurora cluster (PostgreSQL-compatible) from the RDS console and explain how Aurora handles storage, replication, and endpoints. This guide follows the RDS console flow and highlights practical tips for development and production usage.

## Create the cluster

Follow these steps in the RDS console to create an Aurora (PostgreSQL-compatible) cluster:

1. Open the RDS console and click **Create database**.
2. Choose **Standard Create** and select **Aurora (PostgreSQL-compatible)** as the engine.
3. For the use case, pick **Dev and Test** (or **Production** for production workloads).
4. Set the DB cluster identifier and master username (for example, `postgres`). You can select **Auto-generate password** if you want RDS to create a password for you—store the generated password securely because it’s shown only once during creation.
5. Under **Availability & durability**, add reader instances (Aurora Readers) and configure instance placement across Availability Zones if required.
6. Configure **Public access** to match your network and security requirements.
   <Callout icon="warning">
     Enabling Public access can simplify quick testing but increases exposure. For production workloads, restrict public access and use private networking (VPC, security groups, and proper IAM policies).
   </Callout>
7. Review all settings and click **Create database**.

<Frame>
  <img alt="Screenshot of the AWS RDS database creation page showing &#x22;Choose a database creation method&#x22; and various engine options. The &#x22;Aurora (PostgreSQL Compatible)&#x22; engine is selected among choices like MySQL, MariaDB, PostgreSQL, Oracle, and SQL Server." />
</Frame>

After you submit the creation form, the console shows the cluster configuration and highlights options such as the Aurora storage type. If you accepted auto-generated credentials, copy and securely save the password before leaving the creation workflow.

<Frame>
  <img alt="A screenshot of the AWS RDS console for creating an Aurora PostgreSQL DB cluster, showing the DB cluster identifier set to &#x22;database-1&#x22; and the master username &#x22;postgres&#x22; with auto-generate password checked. The lower section shows cluster storage configuration options with &#x22;Aurora Standard&#x22; highlighted." />
</Frame>

## What Aurora creates

When you create an Aurora cluster, RDS provisions:

* A primary (writer) instance that accepts read/write connections.
* Optionally, one or more reader instances for read scaling and high availability.
* A cluster-level endpoint for read/write traffic and reader endpoints for load-balanced read-only traffic.
* A distributed, fault-tolerant storage layer that is decoupled from compute.

The RDS event log and Databases list will show the cluster and instance creation lifecycle. During provisioning you may also see snapshot and lifecycle messages in the console.

<Frame>
  <img alt="A screenshot of the Amazon RDS console showing a Databases list for Aurora PostgreSQL. It shows a regional cluster &#x22;database-1&#x22; and reader instances in creating state, with a &#x22;database-1-snapshot&#x22; entry being deleted." />
</Frame>

## Connecting to the cluster

Once the cluster status is **Available**, open the cluster details to find endpoints and connection information. Use the cluster (writer) endpoint for read/write operations. For read scaling and load distribution, use the reader endpoint which load-balances across available read replicas. You can also connect directly to a specific instance using its instance endpoint when you need instance-level access (for diagnostics or targeted read traffic).

Endpoint types and common uses:

| Endpoint type             | Use case                                    | Typical connection                           |
| ------------------------- | ------------------------------------------- | -------------------------------------------- |
| Cluster (writer) endpoint | Read/write transactions, DDL                | Primary DB client connections                |
| Reader endpoint           | Load-balanced read-only queries             | Reporting, analytics, read scaling           |
| Instance endpoint         | Targeted connections to a specific instance | Diagnostics, session pinning, targeted reads |

<Frame>
  <img alt="Screenshot of the AWS RDS console showing an Aurora PostgreSQL cluster named &#x22;database-1&#x22; with two reader instances and endpoints listed. The instances and endpoints are shown as &#x22;Creating&#x22; in the eu-central-1 region." />
</Frame>

Quick tips:

* The master password cannot be retrieved after creation. If you lose it, reset the password from the RDS console.
* Prefer the cluster endpoint for application connections. Use reader endpoints for scaling read workloads.
* Monitor instance roles (writer vs. reader) and failover events in the RDS console and CloudWatch.

## Quick-create option

If you want a faster setup with sensible defaults, use **Easy create**:

* From **Create database** → **Easy create**, pick **Aurora (PostgreSQL)** and select your use case (Dev/Test or Production).
* Easy create automatically configures backups, performance insights, instance sizing recommendations, and other operational settings.

## Storage behavior and scaling

Aurora abstracts storage from the user—there’s no fixed disk size to choose at creation. The storage layer is a distributed, SSD-backed system that automatically grows as your database consumes more data (up to the service limit, e.g., 128 TB for Aurora PostgreSQL).

<Callout icon="lightbulb">
  Aurora manages storage automatically and charges for the storage you consume. This lets you focus on scaling compute and connections while Aurora transparently expands the storage volume as needed.
</Callout>

## Monitoring and next steps

* Return to the Databases list to check cluster status and instance roles.
* Use CloudWatch metrics and Performance Insights for query performance and resource utilization.
* Configure automated backups, snapshots, and maintenance windows for production systems.
* For more details, see the official AWS documentation: [Amazon RDS for Aurora](https://docs.aws.amazon.com/aurora/latest/userguide/).

That’s it — creating an Aurora cluster in the RDS console is a few clicks, and Aurora takes care of storage, replication, and many operational details for you.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/dbfb72c4-207e-424e-ac83-55f55758740a/lesson/e643cfa1-cd41-4246-8e43-9cfecd79d96e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-rds/module/dbfb72c4-207e-424e-ac83-55f55758740a/lesson/3d9b67a1-30e7-4101-8f93-12127bba593c" />
</CardGroup>
