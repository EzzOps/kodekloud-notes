# Good: All infrastructure code in Git
git add main.tf variables.tf
git commit -m "Add production database with backup retention"

# Bad: Making manual changes through the AWS console
# (Those are not captured in version control)
```

Use variables instead of hard-coded values:

```terraform theme={null}
# Good: Flexible and reusable
variable "environment" {
  description = "Environment name"
  type        = string
}

resource "aws_instance" "web" {
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  tags = {
    Environment = var.environment
  }
}
```

Avoid copy-pasting resource definitions — prefer modules:

```terraform theme={null}
# Good: Reusable web server module
module "web_server" {
  source         = "./modules/web-server"
  environment    = "production"
  instance_count = 3
  instance_type  = "t3.large"
}
```

Automated validation and previewing changes

* Preview changes before applying them. For Terraform, run `terraform plan`.
* Add linting and static checks (tflint, tfsec) and run those in CI.

```bash theme={null}
# Preview changes
terraform plan
# Validate syntax
terraform validate
# Lint for best practices
tflint
# Security scanning
tfsec .
```

Example CI snippet (GitHub Actions) — show plan, run a security scan, and require manual approval for production-affecting changes:

```yaml theme={null}
# .github/workflows/terraform-plan-and-scan.yml
name: Terraform Plan and Scan

on:
  pull_request:

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Security Scan
        run: tfsec .

      - name: Require Approval for Prod
        if: contains(github.event.pull_request.title, 'prod')
        uses: trstringer/manual-approval@v1
```

Policy as code
Policy-as-code tools such as Open Policy Agent (OPA) and HashiCorp Sentinel let you encode guardrails (for example: “no public S3 buckets,” “EC2 instances must have a backup tag,” or “production changes require explicit approval”) and evaluate them automatically as part of CI.

<Frame>
  <img alt="A presentation slide titled &#x22;Testing Infrastructure Changes&#x22; showing &#x22;Policy as Code&#x22; with Open Policy Agent and HashiCorp Sentinel logos. It lists three policies: no publicly readable S3 buckets, all EC2 instances must have backup tags, and production resources require approval." />
</Frame>

Real-world example: automating AWS IAM user creation
Manually creating many IAM users is slow and error-prone — people forget MFA, skip tags, and introduce inconsistencies. Instead, define users in code and let Terraform create them consistently.

<Frame>
  <img alt="A slide titled &#x22;Real-World Example: Automating AWS IAM User Creation&#x22; showing a seven-step circular flowchart of the repetitive manual process for creating IAM users (log in, click Add User, forget to enable MFA, realize mistake, navigate to IAM, set permissions manually, repeat 50 times). A callout notes the manual way is slow and error-prone for a growing company." />
</Frame>

Define a simple list of usernames in terraform.tfvars:

```hcl theme={null}
# terraform.tfvars
aws_region = "eu-north-1"

iam_usernames = [
  "iamuser-pablo",
  "iamuser-julia",
  "iamuser-diego",
]
```

Top-level module usage — pass managed policies and an optional inline policy document:

```terraform theme={null}
module "iam_users" {
  source = "./modules/iam-user"

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/IAMUserChangePassword"
  ]

  inline_policy_document = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:ListAllMyBuckets",
          "s3:GetBucketLocation",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "s3:List*",
          "s3:Get*",
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::dev-bucket",
          "arn:aws:s3:::dev-bucket/*",
        ]
      },
      {
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Effect = "Allow"
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.terraform_state.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.terraform_state.bucket}/*"
        ]
      },
    ]
  })
}
```

Note: the managed policy `IAMUserChangePassword` permits users to change their own passwords. Enforcing MFA is a separate concern — you can require MFA via IAM conditions (aws:MultiFactorAuthPresent), AWS Organizations SCPs, or other account-level controls. Choose an MFA strategy that matches your organization’s security posture.

Module internals — example implementation
This module loops over usernames, creates users and access keys, attaches managed policies, and creates an inline policy if provided:

```terraform theme={null}
# modules/iam-user/main.tf
resource "aws_iam_user" "new_users" {
  for_each = toset(var.iam_usernames)
  name     = each.value
  path     = "/"

  # If these users might be pre-existing and you don't want Terraform to modify them,
  # ignore lifecycle changes that would attempt updates.
  lifecycle {
    ignore_changes = all
  }
}

resource "aws_iam_access_key" "user_keys" {
  for_each = aws_iam_user.new_users
  user     = each.value.name
}

resource "aws_iam_user_policy_attachment" "user_policy_attachments" {
  for_each = {
    for pair in setproduct(keys(aws_iam_user.new_users), var.managed_policy_arns) : "${pair[0]}-${pair[1]}" => {
      user       = pair[0]
      policy_arn = pair[1]
    }
  }

  user       = aws_iam_user.new_users[each.value.user].name
  policy_arn = each.value.policy_arn
}

resource "aws_iam_user_policy" "inline_policy" {
  for_each = var.inline_policy_document != null ? aws_iam_user.new_users : {}
  name     = "${each.value.name}-inline-policy"
  user     = each.value.name
  policy   = var.inline_policy_document
}
```

Working with a real repo and CI/CD
Typical workflow with a sample repo (kodekloud-records-terraform-infrastructure):

* Fork and clone the repo.
* Create a feature branch (for example: dev-test).
* Edit variables (like `terraform.tfvars`) to add the IAM users you want.
* Run `terraform plan` locally or rely on CI to preview changes.
* Commit and push to trigger GitHub Actions which run Terraform.

<Frame>
  <img alt="A presentation slide titled &#x22;Let's Get Our Hands Dirty!&#x22; showing a colorful chevron timeline of steps for a Terraform workflow — fork and clone a repo, run terraform plan, edit variables to create IAM users, apply changes to build infrastructure, modify IAM policies for S3, and use Git version control." />
</Frame>

Project layout example — you’ll typically see directories for environments, modules, and workflows.

<Frame>
  <img alt="A dark-theme screenshot of a GitHub repository page for &#x22;kodekloud-records-terraform-infrastructure,&#x22; showing the main branch, a list of files and folders (e.g., .github/workflows, environments/dev, modules/iam-user) and recent commit messages. The right sidebar displays repository metadata (no description, stars/watchers/forks) and action buttons like Code, Issues, and Pull requests." />
</Frame>

Create and switch to a branch locally:

```bash theme={null}
# From repository root
git checkout -b dev-test
```

Backend and state handling
Remote state storage (for example, S3) is common for Terraform. If you create the backend bucket after your first apply, reconfigure with:

```bash theme={null}
terraform init -reconfigure
```

Example S3 backend and state bucket (abbreviated):

```terraform theme={null}
terraform {
  required_version = ">= 1.3.0"

  backend "s3" {
    key     = "global/terraform.tfstate"
    region  = "eu-north-1"
    encrypt = true
    # bucket will be set during terraform init with -backend-config
    # bucket = "terraform-state-kodekloud-jake-page"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-${random_id.bucket_suffix.hex}"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

If you pre-create the S3 bucket in the console for demos, the repo backend can point to that bucket. For production deployments, prefer creating and configuring state storage via IaC when possible.

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing the &#x22;General purpose buckets&#x22; view with a list of two buckets. The page shows columns for bucket name, AWS Region (Europe/Stockholm), and creation dates, plus the left navigation and a &#x22;Create bucket&#x22; button." />
</Frame>

CI/CD and secrets
When running Terraform from GitHub Actions, supply AWS credentials via repository secrets or use OIDC-based workflows. Example apply workflow that runs on pushes to selected branches:

```yaml theme={null}
# .github/workflows/terraform-apply.yml
name: Terraform Apply

on:
  push:
    branches:
      - main
      - dev-test

jobs:
  terraform:
    name: Terraform Apply
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: terraform init
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          TF_VAR_aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          TF_VAR_aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Terraform Apply
        run: terraform apply --auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          TF_VAR_aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          TF_VAR_aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

Set repository secrets in GitHub: Settings → Secrets and variables → Actions.

<Callout icon="warning">
  Never store secrets in plaintext within the repository. Prefer repository secrets, environment-level secrets, or OIDC for short-lived credentials.
</Callout>

<Frame>
  <img alt="A screenshot of a GitHub repository Settings page (Secrets and variables → Actions) showing no environment secrets and two repository secrets listed: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY. A &#x22;New repository secret&#x22; button is visible on the right." />
</Frame>

Triggering workflows
Push your branch to trigger apply workflows. Monitor runs in the Actions tab and inspect logs if anything fails.

<Frame>
  <img alt="A screenshot of a GitHub repository's Actions page showing Terraform workflow runs. The list shows recent workflow jobs with names, branches, statuses and timestamps, and a left sidebar with workflow and management options." />
</Frame>

Successful apply example

<Frame>
  <img alt="A screenshot of a GitHub Actions run showing a successful &#x22;trigger a run to create users with terraform&#x22; workflow (Terraform Apply) for the repo &#x22;kodekloud-records-terraform-infrastructure,&#x22; with status &#x22;Success&#x22; and total duration 34s. The left sidebar displays the Summary and job details." />
</Frame>

Cleanup workflows
Provide a safe destroy workflow that requires explicit confirmation (for example, typing the word "destroy") to avoid accidental destruction of resources.

<Frame>
  <img alt="A GitHub Actions page for a repository showing the &#x22;Terraform Destroy&#x22; workflow and a list of workflow runs. A run dialog is open asking the user to type &#x22;destroy&#x22; to confirm before running the workflow." />
</Frame>

Infrastructure drift
Drift happens when live resources diverge from IaC configurations (for example, someone makes a one-off console change). Detect drift by running:

```bash theme={null}
# Preview changes
terraform plan

# Detect configuration drift (exit codes indicate differences)
terraform plan -detailed-exitcode
echo "Exit code: $?"

# Exit codes:
# 0 → No changes
# 1 → Error
# 2 → Changes present (e.g., drift or a planned change)
```

When you detect drift, you can:

* Accept and codify the manual change into IaC (update the code and commit).
* Revert the manual change by applying the IaC.
* Import the manual resource into Terraform state so it becomes managed:

```bash theme={null}
terraform import aws_iam_user_policy.manual_policy pablo:manual-cloudwatch-access
```

Monitoring, alerts, and policy-as-code can help reduce manual modifications to live resources.

Example IAM policy JSON snippet used for monitoring permissions:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics"
      ],
      "Resource": "*"
    }
  ]
}
```

Wrap-up
Infrastructure as Code is a fundamental SRE practice. It reduces manual toil, enforces consistency, and brings infrastructure under the same engineering controls as application code. Keep your Git repository as the source of truth, add automated validation and policy checks, and monitor for drift so code and live infrastructure stay aligned.

Configuration management — managing software and system settings on provisioned infrastructure — is closely related and often complements IaC.

Links and references

* [Terraform Documentation](https://www.terraform.io/docs)
* [Open Policy Agent (OPA)](https://www.openpolicyagent.org/)
* [HashiCorp Sentinel](https://www.hashicorp.com/sentinel)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/e98006b4-4a70-4ad0-afdd-367519355d7b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/65ea5014-9c99-43e8-a293-943796760c74" />
</CardGroup>


# Production Readiness

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Release-Engineering/Production-Readiness/page

Guidelines for production readiness and release engineering ensuring safe, tested, observable, and reversible deployments through checklists, load testing, risk assessment, canaries, and SRE sign‑off

Hey there — welcome back. In this lesson we dive into the Release Engineering module.

In the previous module we covered incident management: preparing for outages, responding under pressure, and learning from failures. Release Engineering aims to prevent those incidents by making change safe. Most outages aren’t random hardware failures; they stem from change — an unsafe deployment, an untested configuration, or a vulnerable dependency. SREs focused on release engineering enable fast shipping while enforcing guardrails that protect users and the business.

This module covers production readiness, Infrastructure as Code, configuration management, securing releases, and safe deployment practices at scale. Think of it as building the foundation for “boring” releases: reliable, repeatable, and drama-free. Observability and monitoring then explain what happens once releases are live.

But first: production readiness. Before code reaches real users, we must ask: is it truly ready for production? This lesson is about building confidence that a system can handle real load, recover from problems, and avoid costly failures. Readiness goes beyond unit tests — it means the system is safe under realistic, production-like conditions.

<Frame>
  <img alt="A slide titled &#x22;Production Readiness — Introduction&#x22; showing three people discussing at a table and whiteboard. To the right is a four-point list: 01 Ready for real users, 02 Withstands real load, 03 Handles real problems, 04 Avoids costly failures." />
</Frame>

History shows the cost of ignoring production readiness. Large retailers have lost tens of millions in sales during peak outages. Trading firms have lost hundreds of millions from botched deployments. In 2017, GitLab suffered a six‑hour data-loss incident when backups failed. These examples emphasize that shipping code means protecting the business, not just launching features.

Production readiness requires a mindset shift: developers may say “it works on my machine,” while SREs ask, “will it work for millions of users?” SREs bridge the gap between code that builds locally and systems that survive real-world traffic and failure modes.

<Frame>
  <img alt="A slide titled &#x22;SRE in the Release Lifecycle&#x22; showing a flow from &#x22;It compiles on my machine&#x22; at the top to &#x22;It works for millions of users&#x22; at the bottom, with an SRE Team icon in the middle labeled &#x22;Bridging the gap&#x22; and a speech bubble saying &#x22;It's not easy, but someone has got to do it!&#x22;" />
</Frame>

SREs participate across the release lifecycle: before launch they verify and test, on launch day they monitor and respond, and after launch they analyze outcomes and iterate. Requiring SRE sign-off before a production launch is not red tape — it’s a safeguard learned from costly lessons. The best SREs say “no” to launches that aren’t ready; the worst say “yes” and end up firefighting at 3 a.m.

<Callout icon="lightbulb">
  Require cross-functional sign-off (engineering, product, SRE) before production launches. Make sign-off traceable in the release ticket and tied to the readiness checklist.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;SRE in the Release Lifecycle&#x22; showing the Google logo and the text &#x22;No service launches without SRE sign-off.&#x22; A callout at the bottom reads &#x22;Best SREs: Say 'No' to launches that aren't ready,&#x22; with a KodeKloud copyright." />
</Frame>

How do we know a system is ready? With checklists. Think of a readiness checklist like a pilot’s pre-flight inspection: routine but lifesaving. The four non-negotiable items are:

| Readiness Item     |                                                           Why it matters | Practical example                                                                                   |
| ------------------ | -----------------------------------------------------------------------: | --------------------------------------------------------------------------------------------------- |
| Environment parity |    Prevents misleading test results when staging differs from production | Match OS, runtime, config, feature flags, and external endpoints between staging and prod (use IaC) |
| Load testing       | Ensures the system sustains realistic sustained traffic, not just spikes | Run tests at ≥3× expected peak with realistic data and session patterns (Gatling, k6, JMeter)       |
| Monitoring hooks   |                              Enables detection and diagnosis of failures | Emit metrics, structured logs, and traces for critical workflows; test alerting pathways            |
| Rollback plan      |                              Reduces MTTR when a change causes an outage | Document and rehearse rollback or fail‑open strategies; ensure runbooks and automation exist        |

Pre-launch verification focuses on three critical questions: does the service start and operate end-to-end, can it handle real load, and does it integrate with external dependencies?

* Start (smoke test): Beyond an HTTP 200, verify core user workflows end-to-end: sign-in, purchases, uploads, and error paths. Smoke tests should exercise the user experience, not just health endpoints.
* Load (capacity test): Test at least 3× expected peak using realistic traffic patterns and representative data. Validate sustained throughput and resource usage (CPU, memory, I/O) over meaningful durations.
* Dependencies (integration validation): Confirm external APIs, databases, caches, third-party services, DNS, and network settings behave under production constraints (authentication, rate limits, timeouts).

Answering these three areas with confidence separates a safe launch from a risky one.

<Frame>
  <img alt="A presentation slide titled &#x22;Pre-Launch Verification — Did We Actually Test This?&#x22; showing three checklist boxes: Smoke Test, Load Testing Reality, and Dependency Validation Checklist. Each box lists brief test items like user login/core workflows/error pages, testing at 3× peak traffic with sustained realistic load, and validating APIs, databases, third‑party services and DNS." />
</Frame>

Risk assessment determines the level of caution required for each change. Use a risk matrix (likelihood vs. impact) to guide rollout strategy and safety mechanisms. For example, a new recommendation algorithm (complex ML model) might have medium likelihood of issues and high impact because it touches every product page. The prudent approach: a canary rollout starting at 1% of users combined with a feature flag as an immediate kill switch.

<Frame>
  <img alt="A presentation slide titled &#x22;Risk Assessment Techniques — The 'How Bad Could This Go?' Matrix&#x22; showing an SRE risk matrix with colored indicators (green/yellow/orange/red) for different likelihood and impact levels. On the right is a use case for a new recommendation algorithm launch noting Likelihood: Medium, Impact: High, Action: Canary rollout (start at 1% of users), and Safety Net: feature flag to instantly disable." />
</Frame>

When assessing risk, ask practical, operational questions that map directly to mitigations:

| Question                                           |              Operational intent | Typical action                                                                       |
| -------------------------------------------------- | ------------------------------: | ------------------------------------------------------------------------------------ |
| Blast radius: If it fails, what breaks?            |           Limit scope of impact | Use canaries, sharding, circuit breakers, and feature flags                          |
| Recovery time: How long to fix or rollback?        |                     Reduce MTTR | Keep automated rollbacks and well-practiced runbooks                                 |
| User impact: How many users are affected?          |                Control exposure | Start with small percentages (1–5%) then ramp based on metrics                       |
| Revenue impact: Dollar cost per minute of downtime | Decide tolerance and guardrails | Apply stricter controls (manual approvals, extended canaries) for high‑cost services |

<Frame>
  <img alt="A presentation slide titled &#x22;Risk Assessment Techniques — The 'How Bad Could This Go?' Matrix&#x22; with a central &#x22;Questions That Matter&#x22; box. It lists four assessment questions: &#x22;If this fails, what breaks?&#x22;, &#x22;How long to fix/rollback?&#x22;, &#x22;How many users are affected?&#x22;, and &#x22;Dollar cost per minute of downtime.&#x22;" />
</Frame>

Observability is the final arbiter of readiness: metrics that show when you’re slow, logs that explain why, and traces that pinpoint where latency or errors originate. Good observability lets you answer readiness SLAs:

* Can you determine service health within 30 seconds?
* Can you identify the root cause within 5 minutes?
* Will the right person be paged automatically, and are alerts actionable?

If the answers are “yes,” your system is close to true production readiness.

<Callout icon="warning">
  Avoid alert fatigue: alerts must be actionable and route to the correct on‑call. Test the full alerting pipeline during pre‑launch (alert → paging → runbook execution).
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Observability — Your Early Warning System&#x22; showing a &#x22;Readiness Questions&#x22; panel with three checklist items: telling if the service is healthy in 30 seconds, identifying the problem in 5 minutes, and automatically waking the right person." />
</Frame>

This concludes our introduction to release engineering and production readiness. Next we'll introduce Infrastructure as Code (IaC) — a crucial practice to make system changes declarative, reviewable, and testable so changes become repeatable and less error‑prone.

Further reading and references:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — Useful for environment parity and deployment models.
* [GitLab Incident Postmortem (2017)](https://about.gitlab.com/blog/2017/01/31/gitlab-com-database-incident/) — Example of a production incident caused by backup/configuration failures.
* [Google SRE Practices](https://sre.google/) — Operational guidance and sign‑off discipline.
* Load testing tools: k6 ([https://k6.io/](https://k6.io/)), Gatling ([https://gatling.io/](https://gatling.io/)), JMeter ([https://jmeter.apache.org/](https://jmeter.apache.org/)).

If you want, I can convert the readiness checklist into a reusable release template (Markdown or checklist JSON) you can drop into your CI/CD pipeline.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/db8e4424-ea5b-4676-84f7-b08c6231d8e4" />
</CardGroup>
