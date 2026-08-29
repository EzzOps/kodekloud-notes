# Creating a single MariaDB RDS instance

Source: https://notes.kodekloud.com/docs/AWS-RDS/Understanding-why-we-need-databases/Creating-a-single-MariaDB-RDS-instance/page

Guide to creating a single free tier MariaDB instance on Amazon RDS via the AWS console, covering setup, credentials, monitoring, backups, maintenance, and deletion

This guide walks through provisioning a single MariaDB instance on Amazon RDS using the AWS Management Console. It assumes you understand the benefits of using Amazon RDS (managed backups, automated maintenance, scaling, and monitoring). Follow the steps below to create a free-tier, single-instance MariaDB database quickly.

## Prerequisites

* An AWS account with permissions to create RDS instances.
* Familiarity with the AWS Management Console.
* Decide the AWS Region to use (billing and latency depend on region).

## Quick overview

1. Choose the AWS Region.
2. Open the RDS console and start Create database.
3. Select MariaDB and Free tier options.
4. Configure DB instance identifier and master credentials.
5. Create the database and retrieve credentials.
6. Review instance details, monitoring, backups, and tags.

## Step-by-step: Create the MariaDB instance

1. Sign in to the AWS Management Console and confirm the Region (for this example: Europe (Frankfurt)).
2. Open Amazon RDS from the Services menu or Recently visited apps.
3. On the RDS landing page click Create database.
4. Choose Easy create and select MariaDB. If you’re eligible for the Free Tier, choose the Free tier configuration.
5. Set a DB instance identifier (name). Use a descriptive name to identify project or environment — for example, `my-first-db`.
6. For the master username, use a meaningful admin name (the console defaults to `admin`). For the password, click Auto-generate password so RDS creates a strong password and displays it immediately.

<Frame>
  <img alt="A screenshot of the AWS RDS &#x22;Create database&#x22; setup page for MariaDB. It shows the Free tier instance selected (db.t3.micro), DB instance identifier set to &#x22;my-first-db&#x22;, master username &#x22;admin&#x22;, and the &#x22;Create database&#x22; button." />
</Frame>

7. Confirm the settings and click Create database.

## What happens after you click Create

* RDS begins automated provisioning. Typical availability time is around 5 minutes, but provisioning can take up to 20 minutes depending on region and configuration.
* While provisioning, the DB instance status will read Creating. Use the Refresh button to update the console view.

When you selected Auto-generate password, RDS shows the generated credentials immediately. Click View credential details to reveal the master username and master password. Copy and store these in a secure place such as a password manager.

> **lightbulb** Important: The master password is shown only once during creation. After the DB is created successfully, the master password will not be visible in the RDS console. If you lose it, you'll need to reset the password or create a new user.

## After creation: Instance Available

When provisioning completes the instance status becomes Available. At that point you can view CPU utilization and other performance metrics in the console.

Click the DB instance name to open the details page. The console groups instance information into these sections:

* Connectivity & security
* Monitoring (metrics)
* Logs & events
* Configuration
* Maintenance & backups
* Tags

<Frame>
  <img alt="A screenshot of the AWS RDS console showing a database instance called &#x22;my-first-db&#x22; with status &#x22;Available&#x22; (Engine: MariaDB) and CPU activity displayed. The Configuration tab lists instance class db.t3.micro, 2 vCPU/1 GB RAM, and 20 GiB General Purpose SSD storage with Performance Insights turned off." />
</Frame>

* Configuration displays instance class (for example `db.t3.micro`), CPU, memory, storage type and size.
* Monitoring shows metrics (CPU, memory, disk I/O) useful for understanding resource consumption and guiding right-sizing decisions.

## Maintenance, backups, and tags

Maintenance and backups are managed separately:

* Enable automatic minor version upgrades if you want RDS to apply non-disruptive patches automatically.
* View or modify the maintenance window and see any pending maintenance operations.

<Frame>
  <img alt="A screenshot of the Amazon RDS console showing a database instance named &#x22;my-first-db&#x22; (Engine: MariaDB, Status: Available, Class: db.t3.micro). The Maintenance & backups tab shows auto minor version upgrades enabled, a maintenance window on August 18, 2023, and no pending maintenance." />
</Frame>

Tags let you categorize resources by project, environment, owner, or cost center so you can track billing and manage resources effectively.

## Deleting the DB instance

To delete the DB instance:

1. Select the DB instance.
2. Choose Actions → Delete.
3. The console prompts you to create a final snapshot. If you do not need a final backup, uncheck Create final snapshot (skip final snapshot), type the confirmation text (often the DB instance identifier), and click Delete.

## Choosing an RDS engine

MariaDB is one of several managed database engines available on Amazon RDS. Choose an engine based on application compatibility, required features, performance needs, licensing, and operational preferences.

| Engine               | Use case                                                     | Reference                                                                                |
| -------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| MariaDB              | MySQL-compatible workloads that want MariaDB features        | [https://mariadb.org/](https://mariadb.org/)                                             |
| MySQL                | Widely-used open-source relational database                  | [https://www.mysql.com/](https://www.mysql.com/)                                         |
| PostgreSQL           | Advanced SQL features, extensions, analytics workloads       | [https://www.postgresql.org/](https://www.postgresql.org/)                               |
| Oracle Database      | Enterprise features and Oracle-specific workloads (licensed) | [https://www.oracle.com/database/](https://www.oracle.com/database/)                     |
| Microsoft SQL Server | Windows/.NET heavy workloads and enterprise features         | [https://www.microsoft.com/en-us/sql-server](https://www.microsoft.com/en-us/sql-server) |
| Amazon Aurora        | High-performance, MySQL- or PostgreSQL-compatible managed DB | [https://aws.amazon.com/rds/aurora/](https://aws.amazon.com/rds/aurora/)                 |

For detailed RDS capabilities and limits, see the official Amazon RDS documentation.

## Links and references

* Amazon RDS documentation: [https://docs.aws.amazon.com/rds/](https://docs.aws.amazon.com/rds/)
* MariaDB: [https://mariadb.org/](https://mariadb.org/)
* MySQL: [https://www.mysql.com/](https://www.mysql.com/)
* PostgreSQL: [https://www.postgresql.org/](https://www.postgresql.org/)
* Amazon Aurora: [https://aws.amazon.com/rds/aurora/](https://aws.amazon.com/rds/aurora/)

That’s it — you’ve provisioned a MariaDB instance on Amazon RDS using the console. Thanks for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/bfb32eae-f423-4a2e-9ca1-60adc0ac3ff0/lesson/820f4937-c206-4385-a83f-b171f545f41a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-rds/module/bfb32eae-f423-4a2e-9ca1-60adc0ac3ff0/lesson/022cb4ef-942e-4fa9-9647-bba6f25a2cbe)
