# Check status, stage changes, commit and push
ec2-user@environment ~/aws-microservice-project (master) $ git status
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  modified: templates/product.html

ec2-user@environment ~/aws-microservice-project (master) $ git add .
ec2-user@environment ~/aws-microservice-project (master) $ git commit -m "Deploy product page v01"
[master abc1234] Deploy product page v01
 1 file changed, 60 insertions(+), 2 deletions(-)
ec2-user@environment ~/aws-microservice-project (master) $ git push origin master
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 2 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1.20 KiB | 1.20 MiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
To https://git-codecommit.us-east-1.amazonaws.com/v1/repos/aws-microservice-project
   def5678..abc1234  master -> master
```

Login microservice — example terminal steps:

```bash theme={null}
ec2-user@environment ~/login-page-microservice (master) $ git status
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  modified: templates/login.html

ec2-user@environment ~/login-page-microservice (master) $ git add .
ec2-user@environment ~/login-page-microservice (master) $ git commit -m "Update login button text"
[master def5678] Update login button text
 1 file changed, 22 insertions(+), 8 deletions(-)
ec2-user@environment ~/login-page-microservice (master) $ git push origin master
Counting objects: 6, done.
Delta compression using up to 2 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 1.05 KiB | 1.05 MiB/s, done.
Total 4 (delta 1), reused 0 (delta 0)
To https://git-codecommit.us-east-1.amazonaws.com/v1/repos/login-page-microservice
   123abcd..def5678  master -> master
```

Pushing these commits started the pipelines in CodePipeline automatically.

<Frame>
  <img alt="The image shows the AWS CodePipeline interface with two pipelines, &#x22;login-page-microservice&#x22; and &#x22;crypto-app,&#x22; both currently in progress. It includes details such as source information and execution status." />
</Frame>

## Monitor pipeline progress and verify deployment

I opened each pipeline in the AWS Console and watched them progress through the standard stages:

| Stage  | Typical Actions                                                   |
| ------ | ----------------------------------------------------------------- |
| Source | CodeCommit detects a push and supplies source artifacts           |
| Build  | CodeBuild builds Docker images and pushes to ECR                  |
| Deploy | CodePipeline updates ECS task definitions and deploys to services |

Both pipelines progressed through Source → Build → Deploy automatically. When the build completed, new ECS task definitions were registered and the ECS services were updated.

To verify the login UI change:

1. Open the ECS service for the login application.
2. Click "View Load Balancer" and copy the load balancer DNS name.
3. Open the DNS in your browser.

During a rolling deployment you may briefly see the old and new UI versions as the load balancer routes traffic between old and new containers. This is expected behavior until draining and health checks finish.

<Callout icon="lightbulb">
  During a rolling deployment, you may briefly see both old and new versions as the load balancer routes traffic between container instances. This is expected until old tasks are drained and the new tasks pass health checks.
</Callout>

After the deployment finished, the login button consistently showed "Application login." I logged in with valid credentials and was redirected to the updated product page — confirming both microservices were independently deployed and working together.

## Why this approach matters

| Benefit         | Description                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------- |
| Faster releases | Independent pipelines let teams ship changes without coordinating a monolithic release.       |
| Fault isolation | A problematic deployment in one service does not require rolling back the entire application. |
| Clear ownership | Teams own their code, pipeline, and deployment lifecycle.                                     |
| Scalable CI/CD  | Pipeline automation scales as you add services or teams.                                      |

## Key takeaways

* Continuous deployment was implemented for both microservices using CodeCommit → CodePipeline → CodeBuild → ECS.
* Each service has an independent pipeline; pushing to a repository triggers only that service’s pipeline.
* Rolling ECS deployments can show temporary mixed versions while tasks are being replaced — this is expected.
* Microservice architecture enables faster iteration and independent team velocity.

## Links and references

* [AWS CodePipeline documentation](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Amazon ECS documentation](https://docs.aws.amazon.com/ecs/latest/developerguide/what-is-ecs.html)
* [AWS CodeCommit documentation](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)

That concludes this lesson. See you in the next article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/fcec06b7-0521-4544-949d-07c4c6f84d16" />
</CardGroup>


# Create AWS RDS instance

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Create-AWS-RDS-instance/page

Guide to provisioning and configuring an AWS RDS PostgreSQL instance, initializing a users table, and securing credentials for a login application's database.

Hello — in this lesson we'll provision an AWS RDS (PostgreSQL) instance to store user credentials for the login application in our architecture.

Why an RDS instance?

* The login page authenticates users with username and password. These credentials must be persisted in a reliable, managed relational database.
* Amazon RDS provides a managed PostgreSQL service with backups, automated maintenance, and scaling options, making it suitable for production or development environments.

Relevant links and references

* [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* Password hashing: [bcrypt](https://en.wikipedia.org/wiki/Bcrypt), [Argon2](https://en.wikipedia.org/wiki/Argon2)
* Migration tools: [Flyway](https://flywaydb.org), [Liquibase](https://www.liquibase.com)

## Step-by-step (AWS Console)

1. Sign in to the AWS Console and open the RDS service.
2. Click **Create database**.
3. Choose **PostgreSQL** (selected by default).
4. Select the **Production** template (or another template appropriate for your workload).
5. Choose **Single DB instance**.
6. Set a DB instance identifier (example: `microservice`).
7. In **Credentials**, provide a master username and password or use the automatic password generator. In this lesson we use the auto-generated password.

<Callout icon="lightbulb">
  If you use the auto-generated password, save it securely (for example, in AWS Secrets Manager) so your application can retrieve it at runtime without exposing credentials in code or configuration files.
</Callout>

8. Leave most other settings at their defaults unless you need to customize them.
9. For **Public access** choose `Yes` if you need external connectivity for development or testing. For production, prefer private access (see the security callout below).

<Frame>
  <img alt="This image shows an AWS RDS configuration page where options for VPC, DB subnet group, public access, and VPC security groups are being set. It's part of the setup process for a database instance in AWS." />
</Frame>

Continue with additional options:

10. Scroll down to **Performance Insights** and disable it if you do not need it.
11. In **Additional configuration**, set the initial database name to `microservice`.
12. Review all settings and click **Create database**.

<Frame>
  <img alt="The image shows the AWS RDS (Amazon Relational Database Service) configuration page, where a user is setting up database options for a new database instance named &#x22;microservice.&#x22;" />
</Frame>

## After creation

Wait for the DB instance status to become `available` in the RDS console. Once the instance is available, note the instance endpoint and port (default PostgreSQL port is `5432`). You will use these values to connect and initialize the schema.

<Frame>
  <img alt="This image shows the Amazon RDS console with a list of databases. A PostgreSQL database named &#x22;microservice&#x22; is displayed with its status marked as &#x22;available.&#x22;" />
</Frame>

Quick reference — recommended settings

| Setting                | Recommended value (example) | Notes                                                     |
| ---------------------- | --------------------------- | --------------------------------------------------------- |
| Engine                 | PostgreSQL                  | Choose the major version appropriate for your app         |
| DB instance identifier | `microservice`              | Short, descriptive identifier                             |
| Initial DB name        | `microservice`              | Used by your application connection string                |
| Port                   | `5432`                      | Default PostgreSQL port                                   |
| Public access          | `Yes` (dev) / `No` (prod)   | For production use private subnets and bastion/VPN access |
| Performance Insights   | Off (optional)              | Enable for deep performance troubleshooting               |

## Initialize schema and seed users

Connect to the new database with `psql`, a GUI client, or any PostgreSQL client. Example `psql` command (replace the endpoint and username):

```bash theme={null}
psql -h your-instance-endpoint.rds.amazonaws.com -p 5432 -U postgres -d microservice
```

Once connected, create a simple `users` table and insert sample rows for testing:

```sql theme={null}
-- create a simple users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- insert dummy users (do NOT use plain-text passwords in production)
INSERT INTO users (username, password_hash) VALUES
  ('alice', 'pbkdf2_sha256$...'),
  ('bob', 'pbkdf2_sha256$...'),
  ('carol', 'pbkdf2_sha256$...');
```

Use secure password handling in production: always store salted and hashed passwords (for example, `bcrypt` or `Argon2`) and never store plain-text credentials.

## Security note

<Callout icon="warning">
  Setting Public access to `Yes` exposes the database to the Internet. For production systems, prefer placing the RDS instance in private subnets, use VPNs or bastion hosts to connect, and restrict inbound security group rules to only trusted IP addresses or VPCs. If public access is enabled for development, lock down inbound rules immediately and rotate credentials afterward.
</Callout>

## Next steps

* Use the seeded user accounts to test authentication flows in the login application.
* Configure your application to read DB credentials securely (for example, from AWS Secrets Manager or environment-specific secret stores).
* Automate schema creation and versioning with migration tools such as Flyway or Liquibase for repeatable deployments.
* Monitor and tune performance with RDS monitoring tools and enable automated backups as needed.

That is it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/71e633a9-7507-4a1b-8a17-c0b1f7a09a85" />
</CardGroup>
