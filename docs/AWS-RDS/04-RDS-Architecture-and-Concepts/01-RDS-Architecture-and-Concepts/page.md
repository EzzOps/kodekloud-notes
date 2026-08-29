# RDS Architecture and Concepts

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/RDS-Architecture-and-Concepts/page

Overview of deploying a three-layer web app on AWS using EC2 and Amazon RDS PostgreSQL, covering architecture, connectivity, security, secrets, backups, monitoring, and best practices.

Welcome back.

In this lesson we’ll explore the core Amazon RDS architecture and related concepts by deploying a simple three-layer application to AWS and observing how the app interacts with a managed PostgreSQL database.

This article covers:

* A concise use-case overview and conceptual architecture.
* What we’ll deploy (EC2 + RDS PostgreSQL + static web layer).
* A high-level sequence of interactions between components.
* Key operational considerations, best practices, and references for further reading.

Use case overview

* A user interacts with a static web front-end (Web layer).
* The application logic runs in Python on an EC2 instance (App layer).
* User information is persisted in PostgreSQL managed by Amazon RDS (DB layer).

Below is a conceptual diagram showing these three layers inside the application stack that we’ll deploy to AWS. The diagram is titled "RDS Architecture and Concepts" and illustrates a user connecting to the web layer, which then interacts with the application and database layers in the cloud.

<Frame>
  <img alt="A slide titled &#x22;RDS Architecture and Concepts&#x22; showing a user icon connecting to an application that links into an AWS-hosted stack of Web, App, and DB layers. The right-hand box is labeled &#x22;User information collection application&#x22; and contains three colored blocks for Web, App, and DB." />
</Frame>

What we’ll deploy

* Python application (app layer) running on an EC2 instance.
* Managed PostgreSQL database provided by Amazon RDS (DB layer).
* Static HTML web layer that serves pages and forwards requests to the Python app.
* The Python app connects to the RDS PostgreSQL endpoint to read and write user information.

How the components interact (high level)

1. The user’s browser requests an HTML page from the web layer (HTTP/HTTPS).
2. The web layer forwards application requests to the Python app on EC2.
3. The Python app uses a PostgreSQL client/driver to open a TCP connection to the Amazon RDS PostgreSQL endpoint.
4. Amazon RDS accepts the connection according to VPC, subnet, and security-group rules, executes SQL queries, and returns results.
5. The application processes the results and renders HTML responses back to the user.

Key operational considerations

| Area                        | Concern                                    | Recommended action                                                                                                                  |
| --------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Connectivity                | EC2 must reach the RDS endpoint            | Place EC2 and RDS in the same VPC and appropriate subnets, or configure VPC peering / routing                                       |
| Network security            | Limit access to the DB port (default 5432) | Configure security groups to allow only the EC2 instance (or an application security group) to connect; never open RDS to 0.0.0.0/0 |
| Credentials & secrets       | Avoid hard-coding DB credentials           | Use AWS Secrets Manager or AWS Systems Manager Parameter Store to rotate and inject credentials securely                            |
| High availability & backups | Meet recovery and uptime objectives        | Use Multi-AZ RDS deployments, enable automated backups and snapshots, plan restore tests                                            |
| Monitoring & scaling        | Track resource usage and connections       | Monitor CPU, memory, disk, and connection count; use read replicas or instance resizing for scaling reads/writes                    |

Best practices and operational tips

* Use VPC security groups and subnet isolation to limit lateral movement and reduce blast radius.
* Enable RDS Enhanced Monitoring and CloudWatch alarms for CPU, memory, disk I/O, and connections.
* Use Secrets Manager with IAM roles for EC2 (or an instance profile) to grant least-privilege access to database credentials.
* Test backups and failover procedures regularly to validate recovery time and point objectives (RTO/RPO).
* Consider RDS Performance Insights for query-level diagnostics when troubleshooting slow queries.

AWS services referenced

| Service                     | Purpose                                                   |
| --------------------------- | --------------------------------------------------------- |
| EC2                         | Host the Python application and runtime                   |
| Amazon RDS (PostgreSQL)     | Managed relational database service for storing user data |
| VPC                         | Network isolation and routing for EC2 and RDS             |
| AWS Secrets Manager         | Secure storage and rotation of database credentials       |
| CloudWatch / RDS Monitoring | Metrics, logs, and alarms for operational visibility      |

Next steps in this lesson/article

* Provision the EC2 instance and Amazon RDS PostgreSQL instance in the same VPC.
* Configure security groups, subnets, and routing so the EC2 instance can securely reach RDS.
* Store DB credentials in AWS Secrets Manager and retrieve them from the application using an IAM role.
* Deploy the Python application to EC2 and demonstrate read/write operations against RDS PostgreSQL.

> **lightbulb** Before deploying, ensure you have an [AWS account](https://aws.amazon.com/) with permissions to create EC2, Amazon RDS, VPC, and AWS Secrets Manager resources. Test in a separate, cost-monitored environment or use the [AWS Free Tier](https://aws.amazon.com/free/) where available.

Links and references

* [Amazon RDS product page](https://aws.amazon.com/rds/)
* [Amazon EC2 product page](https://aws.amazon.com/ec2/)
* [Amazon VPC documentation](https://docs.aws.amazon.com/vpc/)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
* [PostgreSQL official site](https://www.postgresql.org/)
* [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

By following this architectural pattern—separating Web, App, and DB layers and using Amazon RDS for managed PostgreSQL—you get the benefits of a managed database (automated backups, patching, and high availability options) while retaining control over application deployment, scaling, and security.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/89a2181a-a115-40b2-b6b2-aca71e351913)
