# Introduction

Source: https://notes.kodekloud.com/docs/AWS-RDS/Introduction/Introduction/page

Course on AWS RDS covering concepts, engines, scaling, backups, security, performance and hands-on labs for deploying and managing relational databases on AWS

Hello and welcome to this course on AWS RDS. I'm Raghunandana Sanur, and I'll be your instructor for this series.

AWS RDS (Relational Database Service) is AWS's managed relational database offering that simplifies the heavy lifting of running production databases. RDS automates routine database tasks such as provisioning, patching, backups, recovery, and scaling so you can focus on designing and building applications. RDS supports multiple database engines including Amazon Aurora, MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server.

<Frame>
  <img alt="A screenshot of the AWS RDS &#x22;Create database&#x22; console showing database creation methods and engine options, with Aurora (PostgreSQL) selected. On the right is a video/photo frame of a person wearing a &#x22;KodeKloud&#x22; t‑shirt." />
</Frame>

This course combines concise theory with hands-on demos in every module so you can immediately apply what you learn. Each module includes practical lab exercises designed to reinforce the concepts and give you real-world experience with RDS.

What you'll learn in this course:

* AWS RDS overview and core concepts (instances, parameter groups, security groups, subnet groups)
* How to scale RDS: Multi-AZ deployments, read replicas, and storage scaling
* Backup and recovery strategies: automated backups, snapshots, point-in-time recovery
* Security best practices for RDS: IAM integration, encryption at rest and in transit, network isolation
* Performance basics and tuning: monitoring, instance sizing, and basic indexing strategies
* Hands-on labs: creating instances, configuring Multi‑AZ and read replicas, and managing backups and snapshots

Key features and benefits:

* Managed operations: automated backups, patching, and maintenance windows
* High availability: easy Multi‑AZ deployments for failover
* Scalability: read replicas and storage/compute scaling options
* Engine flexibility: choose the engine that fits your application needs
* Monitoring and metrics: integration with Amazon CloudWatch

RDS Engines at a glance:

| Engine        | Best for                                                   | Notes                                               |
| ------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| Amazon Aurora | High performance, MySQL/PostgreSQL-compatible applications | Managed, cloud-native, and optimized for AWS        |
| MySQL         | Web applications with broad ecosystem support              | Widely used open-source option                      |
| PostgreSQL    | Complex queries, GIS, and advanced features                | Strong SQL feature set and extensibility            |
| MariaDB       | Drop-in replacement for MySQL                              | Community-driven fork with performance improvements |
| Oracle        | Enterprise commercial workloads                            | License-included or BYOL options                    |
| SQL Server    | .NET and Windows-centric applications                      | Multiple editions supported                         |

Labs included in the course (hands-on topics):

* Creating RDS instances and selecting the right engine and instance class
* Configuring Multi‑AZ for high availability and testing failover
* Creating and promoting read replicas for read scaling
* Setting up automated backups and manual snapshots for point‑in‑time recovery
* Basic performance checks and tuning (monitoring, instance resizing, and indexing)

<Callout icon="lightbulb">
  To follow the labs you will need an [AWS account](https://aws.amazon.com/) with sufficient permissions to create and manage RDS instances (or use a provided sandbox). Basic familiarity with AWS Console navigation and core database concepts will help you move faster.
</Callout>

Join our community while you progress through the course to ask questions, share lab results, and collaborate with other learners. Ready to get started? Let’s dive into AWS RDS and learn how to design, deploy, and maintain relational databases on AWS.

Links and references:

* [AWS RDS product page](https://aws.amazon.com/rds/)
* [Amazon Aurora](https://aws.amazon.com/rds/aurora/)
* [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for related orchestration concepts)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/87f5dd22-d5af-450f-ad8d-f41d9c5f205e/lesson/fefba510-b3b1-4606-b7d9-f53d31d67a3f" />
</CardGroup>
