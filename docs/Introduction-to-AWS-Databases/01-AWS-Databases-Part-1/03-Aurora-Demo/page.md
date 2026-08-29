# Aurora Demo

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/Aurora-Demo/page

Step-by-step Amazon Aurora demo showing how to create and configure an RDS Aurora cluster, review endpoints and settings, follow best practices, and clean up resources

This guide walks through a concise Amazon Aurora demo: create an Aurora cluster in the RDS console, review its configuration and endpoints, and clean up the resources when finished. It assumes you have an AWS account and the necessary IAM permissions to create RDS resources.

1. Open the Amazon RDS console. In the left navigation, choose Databases, then Create database to start the wizard.

<Frame>
  <img alt="A screenshot of the AWS Amazon RDS console showing the RDS dashboard with a left navigation menu, a central &#x22;Resources&#x22; panel listing DB instances, clusters, snapshots and limits, and a right column with recommended services. The page also includes a &#x22;Create database&#x22; section near the bottom." />
</Frame>

## 1 — Engine selection

* Select the Aurora engine that fits your application: Aurora MySQL-compatible or Aurora PostgreSQL-compatible.
* Choose the engine version required by your application (for example, Aurora PostgreSQL 15.4). You can use the default version shown or choose a specific minor/major release if you depend on particular features or bug fixes.

<Frame>
  <img alt="A screenshot of the AWS RDS console showing a dropdown list of Aurora PostgreSQL engine versions (various 13–15 releases) with a template selection area below. The selected option is &#x22;Aurora PostgreSQL (Compatible with PostgreSQL 15.4)&#x22;." />
</Frame>

## 2 — Templates and credentials

* Pick a creation template: Production, Dev/Test, or Free tier (if visible). For this demo we select the Production template to show typical production options.
* Provide a DB cluster identifier (for example, `aurora-example`) and set the master username. For the password, either let AWS Secrets Manager generate one or enter a secure password manually.

## 3 — Storage configuration

* Aurora storage is managed, but you can choose storage performance options such as Standard (cost-effective) or I/O-Optimized (for high I/O workloads). For a basic demo, select Standard.

## 4 — Instance configuration

* Decide between Serverless v2 (if supported by the chosen engine/version) and provisioned instances. For Serverless v2, specify min/max Aurora Capacity Units (ACUs).
* For provisioned instances, pick an instance class (for example, a burstable class like `db.t3.medium`, memory-optimized, or compute-optimized). Choose a class that matches your performance and cost goals.

<Frame>
  <img alt="A screenshot of the AWS RDS console showing Aurora engine options and the &#x22;Instance configuration&#x22; section with a DB instance class dropdown listing sizes like db.t3.medium and db.t3.large. The Availability & durability settings panel is partially visible below." />
</Frame>

## Quick reference: common configuration choices

| Area           | Typical options                         | Notes / Example                                       |
| -------------- | --------------------------------------- | ----------------------------------------------------- |
| Engine         | Aurora MySQL, Aurora PostgreSQL         | Choose based on application compatibility             |
| Template       | Production, Dev/Test, Free tier         | Production enables more resiliency defaults           |
| Storage        | Standard, I/O-Optimized                 | Standard for demos; I/O-Optimized for heavy workloads |
| Instance class | `db.t3.medium`, memory-optimized        | Match CPU/RAM to workload                             |
| Port           | `5432` for PostgreSQL, `3306` for MySQL | Can be customized under Additional configuration      |
| Public access  | Yes / No                                | Avoid public access in production                     |

## 5 — Availability, networking, and access

* Choose Availability & durability options: deploy a single writer only, or add Aurora Replicas (readers) across AZs for Multi-AZ/high availability. For production, enable Multi-AZ.
* Select the VPC and DB subnet group. Using the default VPC/subnet group will place instances across available AZs.
* Configure Public access: typically set to No for production. For short demos you may enable public access, but restrict access via security groups.
* If you need connectivity from EC2, configure it here (you can skip attaching an EC2 instance for a basic demo).

<Frame>
  <img alt="A screenshot of the AWS RDS configuration page showing Virtual Private Cloud (VPC) and DB subnet group selection, public access options, and VPC security group choices. The console is in the N. Virginia region with the default VPC/subnet group selected." />
</Frame>

<Callout icon="warning">
  Do not enable public access for production databases. If you temporarily enable public access for testing, restrict inbound traffic with security groups and remove public access when finished.
</Callout>

## 6 — Security and additional networking

* Attach or create VPC security groups to control inbound access. Limit source IPs and ports to reduce attack surface.
* Optionally enable an RDS Proxy to improve connection pooling and scalability.
* In Additional configuration you can set the database port (PostgreSQL default is `5432`), authentication options (IAM DB authentication), parameter groups, and initial database name.

<Frame>
  <img alt="A screenshot of the AWS RDS console showing the &#x22;Additional configuration&#x22; and &#x22;Database options&#x22; panel with the initial database name set to &#x22;postgres&#x22; and DB cluster/parameter groups set to default. The Backup retention period is set to 7 days and &#x22;Copy tags to snapshots&#x22; is checked." />
</Frame>

## 7 — Monitoring, logs, and maintenance

* Enable Performance Insights when you need advanced monitoring and query performance tuning (note: extra cost may apply).
* Configure database logging and retention only for the logs you need; longer retention increases storage costs.
* Set backup retention (commonly 7 days by default), enable encryption if required, pick parameter and option groups, and set a maintenance window.
* If deletion protection is enabled, you must disable it before deleting the cluster.

## 8 — Cost estimate

* Review the console’s estimated monthly cost for the chosen configuration (instances, storage, backups, and optional features). Adjust choices to balance cost and performance.

<Frame>
  <img alt="A screenshot of the AWS RDS console showing configuration options (auto minor version upgrades enabled, maintenance window set to &#x22;No preference&#x22;, and deletion protection enabled). Below that is an &#x22;Estimated Monthly costs&#x22; box listing DB instance 59.86 + storage 0.10 for a total of $59.96 USD." />
</Frame>

## 9 — Create the database

* When ready, click Create database. Provisioning can take several minutes depending on the configuration and region.

## 10 — Viewing cluster and instance endpoints

* After provisioning, the cluster (for example, `aurora-example`) appears in the Databases list and includes at least a writer instance and any reader instances you added.
* Important endpoints:
  * Cluster writer endpoint — routes writes to the primary/writer instance.
  * Cluster reader endpoint — load-balances reads across readers (if no readers exist, it resolves to the writer).
* Each instance exposes its own instance-level endpoint and networking metadata under the Connectivity & security tab (endpoint, port, VPC, subnets, AZ, and security groups).

<Frame>
  <img alt="A screenshot of the Amazon RDS web console showing the Connectivity & security tab for an Aurora PostgreSQL instance. It displays the instance endpoint and port, networking details (VPC, subnets, availability zone) and VPC security group information." />
</Frame>

## 11 — Cluster actions and management

From the cluster actions menu you can:

* Add reader instances to scale reads.
* Create blue/green deployments for safer upgrades.
* Take snapshots and restore from them.
* Export data to S3.
* Configure autoscaling for replicas and manage backups.

Use these features to scale, protect, and operate Aurora clusters in production.

## 12 — Deleting the cluster

To delete a cluster:

1. Ensure there are no blocking features (disable deletion protection if enabled).
2. Remove reader instances if necessary.
3. From the cluster actions menu, choose Delete. The console will prompt whether to create a final snapshot or retain automated backups—select according to your recovery needs.
4. Confirm by following the prompt (you may need to type the cluster name for confirmation).

<Frame>
  <img alt="A screenshot of the Amazon RDS console showing a confirmation dialog to delete the &#x22;database-aurora-example&#x22; Aurora DB cluster, with warnings and options to create a final snapshot, retain automated backups, and require typed confirmation. The modal overlays the RDS Databases page." />
</Frame>

<Callout icon="lightbulb">
  Before deleting a cluster: disable deletion protection and decide whether a final snapshot is required for recovery.
</Callout>

## Best practices checklist

* Use Multi-AZ and read replicas for high availability and read scaling.
* Do not expose production databases publicly; rely on secure VPC and security groups.
* Enable encryption at rest for sensitive data.
* Regularly review backup retention and snapshot strategies.
* Use monitoring (CloudWatch, Performance Insights) to detect performance issues early.

## Links and references

* Amazon Aurora overview: [https://docs.aws.amazon.com/aurora/latest/userguide/aurora-introduction.html](https://docs.aws.amazon.com/aurora/latest/userguide/aurora-introduction.html)
* Amazon RDS documentation: [https://docs.aws.amazon.com/rds/index.html](https://docs.aws.amazon.com/rds/index.html)
* Configure Amazon RDS security groups: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.SecurityGroups.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.SecurityGroups.html)

That covers the core Aurora demo: creating a cluster in the RDS console, understanding endpoints and configuration options, and safely tearing down the resources afterward.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/851f8f01-0dc4-4d68-894b-b7a9719a9b93" />
</CardGroup>
