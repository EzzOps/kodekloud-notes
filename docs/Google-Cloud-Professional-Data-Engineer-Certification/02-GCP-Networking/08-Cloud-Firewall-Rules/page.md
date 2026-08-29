# Authenticate and set defaults
gcloud auth login
gcloud config set project my-project-id
gcloud config set compute/region us-central1

# Create a VM (defaults used where applicable)
gcloud compute instances create vm-1

# Create a Cloud SQL instance (additional flags usually required in production)
gcloud sql instances create my-sql
```

Note: Some commands require explicit flags (e.g., `--zone`, `--machine-type`, `--tier`) if defaults are not set or if the action needs them.

Configuration management and multi-project workflows

* Keep environments organized to avoid accidental deployments to the wrong project (dev, staging, prod).
* gcloud supports multiple named configurations that make switching contexts simple.

Useful configuration commands

| Command                                           | Purpose                                                                    |
| ------------------------------------------------- | -------------------------------------------------------------------------- |
| `gcloud auth list`                                | List authenticated accounts and show the active account                    |
| `gcloud config list`                              | Show current configuration values (project, region, zone, etc.)            |
| `gcloud config configurations list`               | List named configurations                                                  |
| `gcloud config configurations activate my-config` | Activate a named configuration replacing `my-config` with your config name |
| `gcloud config set project <PROJECT_ID>`          | Set the active project for the current configuration                       |

Use these commands to script environment setup or to switch contexts in interactive sessions.

> **lightbulb** Use the CLI for quick tasks, automation scripts, and CI/CD pipelines. For long-lived, reproducible infrastructure, combine gcloud with infrastructure-as-code tools like Terraform.

When to use gcloud vs. other tools

* Use gcloud for quick administration, ad-hoc scripting, or when you need direct control for a single project or operation.
* For repeatable, versioned infrastructure deployments across environments, prefer IaC tools (Terraform, Deployment Manager) and integrate gcloud commands into CI jobs when needed.
* For storage operations, use gsutil for bulk object transfers; for data warehouse operations, use `bq` for BigQuery tasks; for Kubernetes workloads, use `kubectl` or integrate with `gcloud container` commands for GKE.

Further reading and references

* gcloud CLI overview: [https://cloud.google.com/sdk/gcloud](https://cloud.google.com/sdk/gcloud)
* Authentication for gcloud: [https://cloud.google.com/sdk/docs/authorizing](https://cloud.google.com/sdk/docs/authorizing)
* Configurations guide: [https://cloud.google.com/sdk/docs/configurations](https://cloud.google.com/sdk/docs/configurations)
* gsutil documentation: [https://cloud.google.com/storage/docs/gsutil](https://cloud.google.com/storage/docs/gsutil)
* BigQuery bq tool: [https://cloud.google.com/bigquery/docs/bq-command-line-tool](https://cloud.google.com/bigquery/docs/bq-command-line-tool)
* kubectl reference: [https://kubernetes.io/docs/reference/kubectl/](https://kubernetes.io/docs/reference/kubectl/)

<Frame>
  <img alt="A presentation slide titled &#x22;gcloud CLI Basics – Configuration Management in GCP&#x22; showing a colorful circular diagram. The diagram highlights Local System Configuration, Multiple Accounts, and Multiple Projects revolving around a central &#x22;Correct Project Connection.&#x22;" />
</Frame>

Try these commands in a hands-on session to reinforce learning. Thanks for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/02c15300-8e2a-455b-9032-0d4630391b66/lesson/d4a4226c-2844-4b0d-8374-287b74d2773a)


# Cloud Firewall Rules

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-Firewall-Rules/page

Overview of Google Cloud VPC firewall rules, their components, configuration examples, best practices and troubleshooting guidance for data engineers securing and managing network access to instances

In this lesson we cover Cloud firewall rules in Google Cloud Platform (GCP): what they are, how they’re defined, and why they matter for data engineers. Firewalls act like digital bouncers for your virtual machines—deciding who can connect, who is blocked, and under what conditions. In GCP, firewall rules live in a VPC network and control traffic to and from instances in that VPC.

<Frame>
  <img alt="An infographic slide titled &#x22;Cloud Firewall Rules&#x22; showing a dashed boundary around server/database icons protected by a shield checkmark. To the right are three colored icons with labels: &#x22;Who gets in,&#x22; &#x22;Who stays out,&#x22; and &#x22;Under what conditions.&#x22;" />
</Frame>

Why this matters for data engineers

* When connecting to a database, message broker, or other data service, network teams will ask which ports, source CIDR ranges, or service accounts require access.
* Knowing how VPC firewall rules work lets you provide precise requirements, speed up approvals, and troubleshoot connectivity issues faster.

<Frame>
  <img alt="An illustration titled &#x22;Why This Matters for Data Engineers&#x22; showing a person at a laptop with speech bubbles asking about ports and firewall rules, connected through a GCP cloud icon to a database icon." />
</Frame>

Core concepts — how a firewall rule is defined

When you create a firewall rule in a VPC you specify several properties. The table below summarizes each key field, what it controls, and an example.

| Component            | What it controls                                                                      | Example                                                               |
| -------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Direction            | Whether the rule inspects entering or leaving traffic                                 | `INGRESS` or `EGRESS`                                                 |
| Action               | Permit or block matching traffic                                                      | `allow` or `deny`                                                     |
| Targets              | Which instances the rule applies to                                                   | `target-tags: db-server` or instances with a specific service account |
| Source / Destination | Where traffic originates (ingress) or goes (egress) — CIDR, tags, or service accounts | `--source-ranges 10.1.0.0/16`                                         |
| Protocols & ports    | Protocols (TCP/UDP/ICMP) and port ranges allowed or denied                            | `--allow tcp:5432`                                                    |
| Priority             | Numeric order for rule evaluation — lower = higher priority                           | `--priority 1000`                                                     |

1. Direction

* Ingress: traffic entering instances in the VPC (incoming).
* Egress: traffic leaving instances in the VPC (outgoing).

2. Action

* Allow: permit the matching traffic.
* Deny: block the matching traffic.

<Frame>
  <img alt="A presentation slide titled &#x22;Configuring VPC Firewall Rules&#x22; with a teal VPC cloud icon on the left. The slide lists two steps: &#x22;Define Rule Direction&#x22; (ingress/egress) and &#x22;Set Rule Action&#x22; (allow or deny traffic)." />
</Frame>

3. Targets

* Apply rules to:
  * All instances in the network (no target specification).
  * Instances with specific network tags (e.g., `frontend`, `db-server`).
  * Instances running under specific service accounts.
* Use targets to scope rules only to the intended VMs and reduce blast radius.

4. Source and destination

* Specify where traffic comes from (for ingress) or goes to (for egress):
  * IP ranges using CIDR (e.g., `10.0.0.0/8`, `0.0.0.0/0`).
  * Source tags or service accounts (useful for internal VPC communications).
* This controls which systems are allowed to talk to each other.

5. Protocols and ports

* Specify allowed or denied protocols (TCP, UDP, ICMP) and port ranges.
* Common examples:
  * `tcp:5432` for PostgreSQL
  * `tcp:22` for SSH

6. Priority

* Numeric value where lower numbers have higher priority.
* GCP evaluates rules starting with the lowest numeric priority and stops when a matching rule explicitly allows or denies the traffic. If multiple matching rules share the same priority, DENY rules take precedence over ALLOW rules.

> **lightbulb** When creating or requesting firewall changes, be ready to provide: direction, action, targets (`tags` or service accounts), source/destination ranges, allowed/denied protocols and ports, and the desired priority.

Example: allow inbound PostgreSQL (TCP 5432) from a specific CIDR to VMs tagged `db-server`

```bash theme={null}
gcloud compute firewall-rules create allow-postgres-ingress \
  --network my-vpc \
  --direction INGRESS \
  --priority 1000 \
  --allow tcp:5432 \
  --source-ranges 10.1.0.0/16 \
  --target-tags db-server \
  --description "Allow Postgres from internal network to db servers"
```

Common best practices and tips

* Principle of least privilege: allow only the ports and source ranges that are required.
* Prefer network tags or service accounts for targets (instead of broad all-instances rules).
* Use specific CIDR ranges; avoid `0.0.0.0/0` unless absolutely necessary and documented.
* Use priorities to ensure more specific rules take effect before broad ones.
* Test changes in a staging VPC before applying to production.

> **warning** Be cautious when using `0.0.0.0/0` as a source or destination. Broad exposure increases security risk—document and justify any open ranges.

Notes on permissions and organizational roles

* Many organizations restrict who can create or modify firewall rules. Data engineers often need to request changes from network or cloud operations teams.
* Providing a clear, minimal set of requirements reduces back-and-forth and speeds approvals:
  * Which ports and protocols (e.g., `tcp:5432`)
  * Source CIDR(s) or source tags/service accounts
  * Target tags or service account for the VM(s)
  * Direction (`INGRESS`/`EGRESS`)
  * Desired `priority` and a short `description`

Troubleshooting checklist

* Confirm the VM has the expected network tag or service account.
* Verify the rule priority and whether another rule is blocking traffic.
* Check that the GCE instance-level firewall (iptables) or application firewall isn’t blocking traffic.
* Use `gcloud compute firewall-rules list` and `gcloud compute firewall-rules describe <NAME>` to inspect rules.
* Test connectivity with `telnet <host> <port>` or `nc -vz <host> <port>` from an allowed source.

References and further reading

* [VPC firewall rules — GCP Documentation](https://cloud.google.com/vpc/docs/firewalls)
* [gcloud compute firewall-rules](https://cloud.google.com/sdk/gcloud/reference/compute/firewall-rules)

That covers the essentials of VPC firewall rules and why they matter for data engineers. Understanding these elements will help you design secure connections between your data sources and sinks.

That concludes this article.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/b842c390-bcc5-4180-9899-18e491a2c523)
