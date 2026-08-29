# optional: write logs to a file instead of STDOUT
export TF_LOG_PATH=./terraform.log
```

* On Windows PowerShell:

```powershell theme={null}
$env:TF_LOG = "TRACE"
# optional: write logs to a file
$env:TF_LOG_PATH = "C:\temp\terraform.log"
```

After enabling `TRACE` and running `terraform plan`, you will observe many more internal messages. The excerpts below are representative: they show Terraform's graph transforms, provider matching, HCL source ranges, and diff decisions.

```bash theme={null}
2026-02-14T20:43:00.330-0500 [TRACE] Completed graph transform *terraform.TargetsTransformer
2026-02-14T20:43:00.330-0500 [TRACE] Executing graph transform *terraform.ephemeralResourceTransformer
2026-02-14T20:43:00.330-0500 [TRACE] Completed graph transform *terraform.ephemeralResourceTransformer
2026-02-14T20:43:00.330-0500 [TRACE] Executing graph transform *terraform.CloseProviderTransformer
2026-02-14T20:43:00.330-0500 [TRACE] Completed graph transform *terraform.CloseProviderTransformer

2026-02-14T20:43:00.329-0500 [TRACE] (graphTransformerMulti) Executing graph transform *terraform.transformer
2026-02-14T20:43:00.329-0500 [TRACE] ProviderTransformer: exact match for provider["registry.terraform.io/hashicorp/aws"] serving aws_subnet.private (expand)
2026-02-14T20:43:00.329-0500 [DEBUG] ProviderTransformer: "aws_subnet.private (expand)" (*terraform.nodeExpandApplicableResource) needs provider["registry.terraform.io/hashicorp/aws"]
2026-02-14T20:43:00.329-0500 [TRACE] ProviderTransformer: exact match for provider["registry.terraform.io/hashicorp/aws"] serving aws_subnet.public
2026-02-14T20:43:00.329-0500 [DEBUG] ProviderTransformer: "aws_subnet.public" (*terraform.nodeApplyableResourceInstance) needs provider["registry.terraform.io/hashicorp/aws"]
```

You will also see resource attachment and HCL source references, which are useful for pinpointing the source file and location for a resource:

```bash theme={null}
2026-02-14T20:43:00.329-0500 [TRACE] AttachResourceConfigTransformer: attaching provider to aws_subnet.public
2026-02-14T20:43:00.329-0500 [TRACE] AttachResourceConfigTransformer: attaching to "aws_subnet.private" (*terraform.NodeApplicableResourceInstance) config from hcl.Range{Filename: "main.tf", Start:hcl.Pos{Line:11, Column:1, Byte:202}, End:hcl.Pos{Line:11, Column:32, Byte:233}}
2026-02-14T20:43:00.329-0500 [TRACE] AttachResourceConfigTransformer: attaching provider to aws_subnet.private
2026-02-14T20:43:00.329-0500 [TRACE] AttachResourceConfigTransformer: attaching to "aws_vpc.main" (*terraform.NodeApplicableResourceInstance) config from hcl.Range{Filename: "main.tf", Start:hcl.Pos{Line:1, Column:1, Byte:0}, End:hcl.Pos{Line:1, Column:26, Byte:25}}
2026-02-14T20:43:00.329-0500 [TRACE] Completed graph transform *terraform.AttachResourceConfigTransformer (no changes)
```

Diff determination and change representation are also logged:

```bash theme={null}
2026-02-14T20:43:00.329-0500 [TRACE] DiffTransformer: found Create change for aws_subnet.private
2026-02-14T20:43:00.329-0500 [TRACE] DiffTransformer: aws_subnet.private will be represented as create
2026-02-14T20:43:00.329-0500 [TRACE] DiffTransformer complete
2026-02-14T20:43:00.329-0500 [TRACE] Completed graph transform *terraform.DiffTransformer
```

These traces make it easier to locate where Terraform is assigning providers, how it builds the resource graph, and why particular resources are created, changed, or left unchanged.

<Callout icon="lightbulb">
  TRACE logs can include sensitive data (like provider tokens, API keys, or resource attributes). Avoid sending raw trace logs to third parties without sanitizing them first.
</Callout>

<Callout icon="warning">
  If you must share logs with HashiCorp or a provider, redact secrets (API keys, tokens, passwords, and any sensitive attributes) before uploading. Consider limiting logs to a file and opening it in a secure editor to mask secrets.
</Callout>

## Disable logging when finished

When you've captured the necessary information, turn logging off to restore concise output.

* On macOS / Linux:

```bash theme={null}
unset TF_LOG
# optionally unset TF_LOG_PATH
unset TF_LOG_PATH
```

* On Windows PowerShell:

```powershell theme={null}
Remove-Item Env:\TF_LOG
# optionally:
Remove-Item Env:\TF_LOG_PATH
```

After unsetting, `terraform plan` returns to the normal concise output:

```bash theme={null}
$ terraform plan
Plan: 3 to add, 0 to change, 0 to destroy.

Note: You didn't use the --out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

## References

* [Terraform CLI — Environment variables (TF\_LOG)](https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_log)
* [Terraform CLI — plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)

Thanks for following this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5a3363d1-83cc-4a39-997d-82fa687251ac/lesson/745b1ae5-da9e-4c2f-8c70-9b21c811d6f4" />
</CardGroup>


# AWS RDS Demo

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/AWS-RDS-Demo/page

Step-by-step guide to deploying, configuring, and connecting to a managed PostgreSQL instance on Amazon RDS, covering instance creation, storage, networking, security, backups, and client connections.

In this lesson you'll learn how to deploy a managed PostgreSQL instance using Amazon RDS. RDS removes the need to provision and operate the underlying database server by handling instance provisioning, storage management, automated backups, and other operational tasks.

## 1. Create Database (Standard vs Easy)

Open the AWS Management Console, search for **RDS**, and choose **Create database**. You can pick:

* **Easy (Simple) create** — applies opinionated defaults and speeds up creation.
* **Standard create** — exposes all configuration options for full control.

For this walkthrough we use **Standard create** so you can see the available configuration settings.

<Frame>
  <img alt="A screenshot of the AWS RDS &#x22;Create database&#x22; console showing the database creation method (Standard vs Easy) and engine options. The engine tiles visible include Aurora (MySQL/PostgreSQL compatible), MySQL, MariaDB, PostgreSQL and Oracle." />
</Frame>

## 2. Engine selection and version

Select the database engine you want — choose **PostgreSQL** for a Postgres instance. Then select the engine version; the default is suitable in most cases unless you need a specific release for compatibility or features.

## 3. Templates and intended use

RDS offers templates that preconfigure many settings:

| Template   | Use case                                | Key differences                                                     |
| ---------- | --------------------------------------- | ------------------------------------------------------------------- |
| Production | Critical workloads                      | Enables Multi-AZ, higher availability and resilience                |
| Dev/Test   | Development and experimentation         | Balanced defaults for cost and function                             |
| Free tier  | New accounts / cost-constrained testing | Uses settings that may qualify for the AWS Free Tier (if available) |

Select the template that matches your workload — we used **Dev/Test** for this lesson.

## 4. Instance configuration (compute)

RDS instances run on instance classes that resemble EC2 types. Pick an instance class that matches your CPU, memory, and network requirements — the console shows vCPU, RAM, and network throughput for each option.

<Frame>
  <img alt="A screenshot of a cloud console dropdown showing database instance classes (e.g., db.m6i.large, db.m6i.xlarge) with their vCPU counts, RAM sizes and network Mbps values. It appears to be an AWS RDS instance type selection panel." />
</Frame>

## 5. Storage

Choose a storage type and the initial size. You can enable storage autoscaling so RDS grows storage as required up to a maximum you define. Storage options (General Purpose SSD, Provisioned IOPS, etc.) vary by cost and performance.

| Storage type               | Best for                           |
| -------------------------- | ---------------------------------- |
| General Purpose (gp2/gp3)  | General workloads, cost-effective  |
| Provisioned IOPS (io1/io2) | I/O-intensive production databases |

<Frame>
  <img alt="A cloud database storage settings panel (likely AWS RDS) showing &#x22;Provisioned IOPS SSD (io1)&#x22; with 100 GiB allocated storage, 3000 provisioned IOPS, and storage autoscaling enabled with a 1000 GiB max threshold." />
</Frame>

Tip: For workloads with unpredictable growth, enable storage autoscaling and set a sensible maximum to avoid unexpected costs.

## 6. Connectivity, networking, and optional compute helper

Decide whether to provision an associated compute resource for quick connectivity tests (optional). Choose the VPC and subnets where the DB instance should run — you can use the default VPC or supply a custom network.

<Frame>
  <img alt="A screenshot of an AWS RDS setup page showing compute and network settings with &#x22;Don't connect to an EC2 compute resource&#x22; and &#x22;IPv4&#x22; selected. It also displays the Virtual Private Cloud (Default VPC), DB subnet group, and Public access options." />
</Frame>

* Set **Public access** to `No` for production (keeps the instance in private subnets). Set to `Yes` only for temporary testing and ensure strong security rules.
* Choose a DB subnet group and optionally specify an Availability Zone or leave it as **No preference** for AWS to pick.

## 7. Security groups and public access

Create or reuse a security group to control inbound traffic. For local testing, add a rule to allow your client IP on the PostgreSQL port (`5432` by default). For production, restrict access to known application subnets or a bastion host.

## 8. Additional configuration

Under Additional configuration you can:

* Change the default port (`5432`).
* Select authentication methods (password, `IAM` authentication).
* Enable enhanced monitoring, performance insights, backups, encryption, and set backup retention windows.

RDS automated backups and point-in-time recovery simplify restores.

When ready, click **Create database**. Provisioning typically takes several minutes while AWS provisions compute, storage, and networking.

## 9. Instance available — find connectivity details

After the instance status changes to **Available**, open the DB instance details. Note the `Endpoint` (host) and `Port` — you'll use these, together with the master username and password, to connect from a client.

<Frame>
  <img alt="A screenshot of the Amazon RDS console showing a PostgreSQL DB instance summary (my-first-db) with CPU/status info. The page displays connectivity and security details including endpoint, port, VPC/subnets, and security group." />
</Frame>

Example connection using psql:

* `psql -h <your-rds-endpoint> -U postgres -p 5432 -d postgres`

Replace `<your-rds-endpoint>` with the value shown in the console.

## 10. Connect using pgAdmin

You can connect with GUI tools such as pgAdmin. Create a new server entry and supply:

* Host: the RDS endpoint (paste from the console)
* Port: `5432` (or your custom port)
* Maintenance DB: typically `postgres`
* Username: the master username (e.g., `postgres`)
* Password: the password you set

<Frame>
  <img alt="A screenshot of the pgAdmin &#x22;Create - Server&#x22; dialog on the Connection tab, showing an Amazon RDS host endpoint, port 5432, maintenance database and username set to &#x22;postgres,&#x22; and an empty password field. The pgAdmin dashboard with welcome/configure tiles is visible in the background and Cancel/Reset/Save buttons appear at the bottom." />
</Frame>

After you save, pgAdmin will show the server and default database. You can create new databases, schemas, tables, and run queries as usual.

<Frame>
  <img alt="A screenshot of the pgAdmin database dashboard with the server/database tree on the left and the &#x22;my_app&#x22; database selected. The right side shows metrics panels (sessions, transactions/sec, tuples in/out, block I/O) and a server activity table at the bottom." />
</Frame>

<Callout icon="lightbulb">
  Do not use the master account credentials for application connections. Create an application-specific database user with the minimum required privileges. For production, use `IAM` authentication or a secrets manager such as [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) to store and rotate credentials securely.
</Callout>

## 11. Modify or delete the instance

* To change instance settings later, choose **Modify** in the RDS console to update instance class, storage, backup windows, maintenance windows, and more.
* To remove the instance, choose **Delete**. The console will prompt whether to create a final snapshot and whether to retain automated backups — for production systems, create and retain snapshots or export data before deletion.

<Frame>
  <img alt="Screenshot of the Amazon RDS console for a database named &#x22;my-first-db.&#x22; It shows the instance summary (CPU, status &#x22;Available&#x22;, PostgreSQL engine) and the Connectivity & security section with endpoint, port and VPC/subnet details." />
</Frame>

<Callout icon="warning">
  If you enable public access, ensure your security group only allows trusted IP addresses on the database port. Exposing a database to the public internet without strict controls increases the risk of unauthorized access.
</Callout>

If you choose **Delete**, confirm the deletion checkbox(s) and acknowledge the prompt to remove the instance and any retained snapshots (depending on your choices).

<Frame>
  <img alt="A confirmation dialog for deleting the &#x22;my-first-db&#x22; database instance with checkboxes to create a final snapshot, retain automated backups, and an acknowledgment. There’s an input field partially filled to confirm deletion and Cancel/Delete buttons at the bottom." />
</Frame>

That concludes this lesson on deploying and connecting to a PostgreSQL instance on Amazon RDS.

## References

* [Amazon RDS Documentation](https://docs.aws.amazon.com/rds/)
* [PostgreSQL Official Site](https://www.postgresql.org/)
* [pgAdmin](https://www.pgadmin.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/dbb798b2-1272-4fd7-9384-41e371499a97" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/c10c0f10-c2d5-4117-aa57-6f70ff667ea7" />
</CardGroup>
