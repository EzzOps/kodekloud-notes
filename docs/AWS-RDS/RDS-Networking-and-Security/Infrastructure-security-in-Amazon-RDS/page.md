# Infrastructure security in Amazon RDS

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Networking-and-Security/Infrastructure-security-in-Amazon-RDS/page

Guidance on securing Amazon RDS infrastructure, covering shared responsibility, network isolation, encryption, authentication, backups, monitoring, and operational best practices.

Welcome back. In this lesson we cover infrastructure security for Amazon RDS and the security responsibilities you retain when using a managed database service.

Using a managed service like Amazon RDS gives you a major advantage: AWS operates and secures the underlying global infrastructure (physical datacenters, hardware, hypervisor, and core network). That removes much of the operational burden compared to an on‑premises deployment. However, you still retain important responsibilities for configuration, access, and data protection inside your AWS account.

<Callout icon="lightbulb">
  AWS secures the cloud infrastructure; you secure the resources and configuration inside your account. Knowing which controls AWS manages and which are your responsibility is essential for a secure RDS deployment.
</Callout>

## Shared responsibility model

At a high level:

* AWS is responsible for the security "of" the cloud: physical facilities, host infrastructure, virtualization, and managed service runtimes.
* You are responsible for security "in" the cloud: network configuration, access control, encryption keys (when customer‑managed), database users and credentials, and the data stored in RDS.

| Responsibility                       |                                    AWS (Security of the cloud) | You (Security in the cloud)                                      |
| ------------------------------------ | -------------------------------------------------------------: | ---------------------------------------------------------------- |
| Physical security & datacenters      |                                                             ✔️ |                                                                  |
| Hypervisor & managed runtime         |                                                             ✔️ |                                                                  |
| OS patching for managed engines      |                                      ✔️ (major responsibility) | Keep parameter groups/engine versions current                    |
| Network configuration (VPC, subnets) |                                                                | ✔️                                                               |
| Security groups & NACLs              |                                                                | ✔️                                                               |
| IAM, roles, and user policies        |                                                                | ✔️                                                               |
| Data encryption keys                 | Shared: AWS-managed CMKs by default; customer-managed possible | Choose CMK type and manage policies/rotation if customer-managed |
| Database credentials & schema        |                                                                | ✔️                                                               |

References:

* [AWS Organizations overview](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
* [Amazon RDS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)

## Network isolation and access control

Best practices:

* Launch RDS instances inside a VPC and place them in DB subnet groups. Use private subnets unless public access is required.
* Use security groups (stateful) to permit only the application servers and management IPs that need access to the DB port.
* Use network ACLs (stateless) for additional subnet-level boundaries.
* Avoid setting RDS to "publicly accessible" in production; prefer private subnets and tightly scoped security groups.

Table — network controls and typical uses:

| Control                       | Purpose                       | Example                                                              |
| ----------------------------- | ----------------------------- | -------------------------------------------------------------------- |
| VPC & private subnets         | Isolate DB from internet      | Place DB instances in private subnets with no internet gateway route |
| Security groups               | Host-level access control     | Allow MyApp EC2 IPs or ALB security group to access port 5432        |
| Network ACLs                  | Subnet-level stateless filter | Deny a suspicious CIDR range on the subnet                           |
| VPC Peering / Transit Gateway | Inter-VPC connectivity        | Connect application VPCs to DB VPC with minimal exposure             |
| PrivateLink                   | Private service endpoints     | Expose management services without public IPs                        |

## Isolation and tenancy

For stronger isolation:

* Use separate AWS accounts and VPCs for dev/test/prod, managed via [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html).
* Use strict IAM boundaries and role-based access.
* If you require physical single-tenant isolation, consult AWS and RDS documentation for options (dedicated hosts or self-managed DBs on EC2).

## Encryption and key management

Protect data at rest and in transit:

* Enable encryption at rest using AWS KMS. Decide between AWS-managed CMKs or customer-managed CMKs. Customer CMKs provide more control (key policies, rotation, access restrictions).
* Enforce TLS for in-transit encryption. Configure your database clients to validate certificates and require TLS.
* When using customer-managed CMKs, create strict IAM policies and key policies to limit who can use or manage the keys.

Helpful links:

* [Amazon RDS encryption overview](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
* [AWS KMS developer guide](https://docs.aws.amazon.com/kms/latest/developerguide/)

## Authentication, secrets, and least privilege

* Store DB credentials in [AWS Secrets Manager](https://docs.aws.amazon.[SECRET_REDACTED].html) or [Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) rather than hard‑coding secrets.
* Use IAM for management‑plane operations and enable [IAM DB authentication](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].IAMDBAuth.html) for supported engines (e.g., MySQL, PostgreSQL).
* Implement least privilege for both AWS IAM roles and database accounts; avoid using a single, high‑privilege account for all operations.
* Enforce Multi‑Factor Authentication (MFA) for privileged IAM users and require strong password policies.

## High availability, backups, and monitoring

* Use [Multi‑AZ deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html) for automatic failover and improved availability.
* Configure automated backups, snapshots, and point‑in‑time recovery to meet your RPO/RTO.
* Enable enhanced monitoring, database audit logs, and CloudWatch alarms to detect performance issues and suspicious activity.
* Use [AWS Config rules](https://docs.aws.amazon.com/config/latest/developerguide/what-is-aws-config.html) to detect misconfigurations and enforce policy compliance.

Relevant documentation:

* [Automated Backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
* [Monitoring overview for RDS](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Database engine logs and audit](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.html)
* [CloudWatch](https://docs.aws.amazon.[SECRET_REDACTED].html)

## Cross‑region networking and global deployments

When spanning regions:

* Understand replication options: cross‑region read replicas ([RDS Read Replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)) or [Aurora Global Database](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-global-database.html).
* Choose networking strategies: inter‑region VPC peering, [AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html), PrivateLink, or VPN/Direct Connect depending on latency and security needs.
* Account for cross‑region data transfer and snapshot copy costs when designing global deployments.

Network/repl links:

* [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)
* [AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)
* [AWS PrivateLink](https://docs.aws.amazon.com/privatelink/latest/userguide/what-is-aws-privatelink.html)
* [AWS Direct Connect](https://docs.aws.amazon.[SECRET_REDACTED].html)

## Operational security hygiene

* Keep database engine versions and parameter groups current. RDS manages much of the patching, but you must schedule upgrades and review parameters.
* Regularly rotate credentials and keys, audit account activity using CloudTrail, and remove unused IAM permissions.
* Periodically review security group rules and NACLs to remove overly permissive entries and close unnecessary openings.
* Implement logging and centralize logs for analysis, retention, and compliance.

## Putting it together — practical checklist

* Use separate VPCs and accounts to isolate environments (dev/test/prod).
* Keep databases in private subnets with tightly scoped security groups.
* Centralize secrets and encryption key management (Secrets Manager + KMS).
* Enforce TLS for client connections and use customer-managed CMKs when regulatory control is required.
* Enable Multi‑AZ and automated backups aligned with business RPO/RTO.
* Monitor engine and infrastructure metrics; create alarms and ingest logs into a central SIEM.
* Design cross‑region deployments deliberately, balancing security, latency, and cost.

<Frame>
  <img alt="A presentation slide titled &#x22;Infrastructure Security in Amazon RDS&#x22; that lists three points about RDS being protected by AWS global network security, the AWS shared responsibility model, and configuring RDS based on application usage. Each point is paired with a colorful circular icon, and a © KodeKloud credit appears at the bottom." />
</Frame>

## Links and references

* [Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* [Amazon RDS encryption overview](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
* [RDS SSL/TLS guide](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].SSL.html)
* [AWS KMS developer guide](https://docs.aws.amazon.com/kms/latest/developerguide/)
* [Secrets Manager overview](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
* [IAM DB authentication for RDS](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].IAMDBAuth.html)
* [RDS Multi‑AZ concept](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
* [RDS Read Replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
* [Aurora Global Database](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-global-database.html)
* [AWS Organizations introduction](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
* [AWS Config overview](https://docs.aws.amazon.com/config/latest/developerguide/what-is-aws-config.html)

Use this guidance to design a secure, resilient Amazon RDS deployment that aligns with your compliance and operational requirements.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/12fd8771-ab60-4e87-8f8b-67fe9507bb76/lesson/3f3f90d3-194b-4a61-8994-e6dd2f577163" />
</CardGroup>
