# When using IAM auth, paste the generated token at the password prompt and ensure TLS is enabled.
```

Best practices

* Use RDS Proxy for serverless or high-concurrency services to avoid connection storms.
* Keep client-side retries and exponential backoff; some in-flight requests may still fail during backend failover.
* Integrate RDS Proxy with Secrets Manager for automatic credential rotation and with IAM DB auth for short-lived credentials.
* Monitor proxy metrics (ConnectionsBorrowed, NewConnections, ConnectionPoolFullCount, etc.) using CloudWatch to tune pool size and behavior.

<Callout icon="lightbulb">
  Use RDS Proxy for high-concurrency applications (including serverless workloads), to centralize secrets and IAM authentication, and to reduce the connection-management burden on your database. RDS Proxy supports Amazon RDS and Aurora engines for MySQL and PostgreSQL.
</Callout>

Further reading and references

* [Amazon RDS Proxy documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
* [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
* [IAM database authentication for MySQL and PostgreSQL on Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)

Next, lab exercises covering AWS proxies are provided.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/12fd8771-ab60-4e87-8f8b-67fe9507bb76/lesson/0280e09e-d8b7-4ed4-b91b-107779e080ff" />
</CardGroup>


# Security Best Practices for Amazon RDS

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Networking-and-Security/Security-Best-Practices-for-Amazon-RDS/page

Security best practices for Amazon RDS focusing on IAM identities, least privilege, IAM roles, credential rotation, Secrets Manager usage, logging, and auditability

Welcome back. This lesson summarizes recommended AWS guidelines for securing Amazon RDS. These recommendations reduce risk, simplify administration, and help meet compliance requirements when multiple people or services access your databases.

Why this matters

* Databases hold sensitive data and credentials; misconfiguration or shared credentials increases attack surface.
* Applying least privilege, enforcing strong identity controls, and automating secret rotation minimize the window of exposure and simplify audits.

Key recommendations

* Create individual identities: Give each team member their own IAM user or role. Never share credentials. Individual identities provide an audit trail and enable per-user access control.
* Avoid using the root account: Reserve the AWS account root user for account-level tasks (billing, account settings). Protect it with a strong password and MFA.
* Apply least privilege: Grant only the permissions required — e.g., read-only SELECT rather than CREATE/ALTER where appropriate. Use tightly scoped IAM policies for actions and resources.
* Use IAM groups and roles: Manage permissions by grouping users and attaching policies to those groups. For services, prefer IAM roles (EC2 instance roles, ECS task roles, Lambda execution roles) that issue temporary credentials via STS.
* Rotate credentials regularly: Rotate IAM keys and database passwords on a schedule. Automated rotation reduces exposure from leaked credentials.
* Use AWS Secrets Manager or Systems Manager Parameter Store: Store database credentials and secrets centrally and securely. Configure automatic rotation where supported so applications retrieve updated credentials without downtime.

Quick summary table

|         Recommendation | Purpose                                      | Example / Where to start                        |
| ---------------------: | -------------------------------------------- | ----------------------------------------------- |
|  Individual identities | Auditability & per-user controls             | Create IAM users and roles; enable CloudTrail   |
|   Root user protection | Minimize high-privilege exposure             | Enable MFA on root; avoid routine use           |
|        Least privilege | Limit blast radius                           | Use resource-scoped IAM policies (`rds:db:arn`) |
| IAM roles for services | Temporary credentials, no long-lived secrets | Use EC2/ECS/Lambda execution roles              |
|     Automated rotation | Reduce credential exposure                   | Use Secrets Manager rotation for RDS            |
|   Central secret store | Secure, auditable secret access              | AWS Secrets Manager / Parameter Store           |

Managing service credentials and rotation

* Prefer IAM roles and instance/task roles for services that access RDS. Roles produce temporary credentials rotated by AWS and eliminate long-lived IAM user keys.
* If your app requires database usernames/passwords, use AWS Secrets Manager to manage and auto-rotate those credentials. Applications can retrieve secrets via the Secrets Manager SDK or the AWS SDK integration.
* Ensure all rotation policies are consistently applied across environments (dev, staging, prod) and include monitoring for rotation failures.

Operational practices

* Enforce strong password policies and require MFA for interactive access where possible.
* Regularly review IAM policies, group memberships, and role assumptions to remove unnecessary privileges.
* Enable and review CloudTrail for control-plane events, and enable RDS logging (e.g., general logs, audit logs, enhanced monitoring) for data-plane activity.
* Integrate logging and alerts into your SIEM or monitoring stack to respond to suspicious activity quickly.

Practical checklist

* [ ] Create per-user IAM identities and enable CloudTrail
* [ ] Enable MFA for root and privileged users
* [ ] Replace long-lived credentials with IAM roles for services
* [ ] Move DB credentials to Secrets Manager with auto-rotation
* [ ] Audit IAM policies quarterly and remove unused roles
* [ ] Enable RDS and OS-level logging and forward logs to your monitoring system

References and further reading

* [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
* [Amazon RDS Security Overview](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Security.html)
* [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
* [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)

<Frame>
  <img alt="A presentation slide titled &#x22;Security Best Practices for Amazon RDS – Summary&#x22; listing recommendations like creating individual users, granting minimum permissions, using IAM groups, rotating IAM credentials, and configuring AWS Secrets Manager to auto-rotate RDS secrets. The slide shows five gray boxes with those concise best-practice points." />
</Frame>

<Callout icon="lightbulb">
  Follow the principle of least privilege and automate secret rotation wherever possible. Prefer IAM roles and temporary credentials for services, and use Secrets Manager for application-facing secrets to minimize operational risk.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/12fd8771-ab60-4e87-8f8b-67fe9507bb76/lesson/78e4ae72-c6aa-4636-89fa-0ccb0d2cb84f" />
</CardGroup>
