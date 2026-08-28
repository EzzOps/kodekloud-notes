# config.py
# (accidentally public!)
DATABASE_PASSWORD = "super_secret_123"
AWS_ACCESS_KEY = "[AWS_ACCESS_KEY_ID]"
```

Environment inconsistency example (three environment documents):

```yaml theme={null}
# Dev
connections: 5
cache_gb: 1
debug: true
---
# Staging
connections: 10
cache_gb: 2
debug: false
---
# Production (incorrectly left with debug=true)
connections: 10
cache_gb: 2
debug: true
```

These pitfalls make systems fragile and often surface during incidents.

<Frame>
  <img alt="A slide titled &#x22;Common Pitfalls&#x22; that lists four warnings: Manual Config Drift, Sensitive Data Exposure, Environment Inconsistency, and Uncontrolled Changes. Below is a table showing daily config changes (Alice, Bob, Charlie) that overwrite timeouts and lead to a production incident." />
</Frame>

Treat configuration as code: store configuration files, dashboards, and environment-specific variables in version control so every change is reviewed, tested, and auditable.

Example repository layout (KodeKloud example):

```text theme={null}
kodekloud-records-store-web-app
  config/monitoring
    grafana-provisioning
      dashboards
        dashboard.yaml
        end-to-end-purchase-journey.json
        engineer-dashboard.json
        executive-dashboard.json
        kodekloud-records-store-slis.json
        kodekloud-records-store-slos.json
        observability-dashboard.json
        performance-metrics-dashboard.json
      datasources
    logging
    alert_rules.yml
    alertmanager.yml
    blackbox.yml
    prometheus.yml
    README.md
    sli_rules.yml

.github
config
deploy
  environments
  templates
    env.dev.template
    env.prod.template
    env.staging.template
```

With this layout, configuration changes travel through the same review and CI pipeline as code changes.

Safe change management techniques

* Infrastructure as Code (IaC): keep environment and infrastructure definitions in Git to enforce review and reproducibility.
* Feature flags: ship code disabled, then toggle behavior at runtime for quick rollback and safe experimentation.
* Gradual rollouts: expose new configuration to a small subset of users, monitor metrics, and expand progressively.
* Version control for every config change: maintain provenance (who changed what and when) to enable rapid rollback.

```python theme={null}
# Example feature flag usage
if feature_flag("new_payment_processor"):
    return new_payment_flow()
else:
    return old_payment_flow()
```

<Frame>
  <img alt="A presentation slide titled &#x22;Safe Change Techniques&#x22; listing four practices: Infrastructure as Code, Feature Flags, Gradual Rollouts, and Configuration Version Control, with checkmarks beside the first two. A callout shows a rollout strategy (10% → Monitor → 50% → Monitor → 100%) and a note to rollback if metrics degrade." />
</Frame>

Use staged environment promotion. Changes should flow from development to staging and then to production with guardrails at each stage: config validation, build and test in dev, container/image scanning, integration tests, and manual approvals when warranted.

<Callout icon="lightbulb">
  Staged promotions ensure that by the time changes hit production, they have been validated in realistic environments and checked at multiple gates.
</Callout>

A simple CI pipeline that enforces environment promotion (GitHub Actions-style example):

```yaml theme={null}
jobs:
  validate-configuration:
    runs-on: ubuntu-latest

  build-and-test:
    runs-on: ubuntu-latest
    needs: validate-configuration

  build-container:
    runs-on: ubuntu-latest
    needs: [validate-configuration, build-and-test]

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build-container]
    environment: staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    environment: production
```

Each job depends on earlier gates. Start with configuration validation, then build and test in dev. After successful builds and scans, deploy to staging; only after staging gates pass should the pipeline promote to production.

Environment-specific configuration keeps deployments flexible and safe. For example, Docker Compose can load environment variables from files per environment so you can test in realistic conditions without mixing values across environments.

docker-compose service example:

```yaml theme={null}
version: "3.9"
services:
  db:
    image: postgres:15
    container_name: kodekloud-record-store-db
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

Store your .env templates under deploy/templates (as shown earlier) and select the appropriate environment file when launching Compose:

```bash theme={null}
# Run with development variables
docker-compose --env-file .env.dev up

# Run with staging variables
docker-compose --env-file .env.staging up

# Run with production variables
docker-compose --env-file .env.prod up
```

Summary

* Treat configuration as code: version, review, test, and audit.
* Use feature flags and gradual rollouts to reduce blast radius.
* Enforce staged promotions and pipeline gates for any change that affects production.
* Keep environment-specific values isolated and never check secrets into source control.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Documentation](https://docs.docker.com/)
* [GitHub Actions](https://docs.github.com/en/actions)
* [KodeKloud Learn - GitHub Actions Course](https://learn.kodekloud.com/user/courses/github-actions)

That wraps up this lesson on configuration management: why it matters, where it tends to go wrong, and practical patterns to manage configuration safely. A subsequent lesson will cover secure software releases.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/0b6a5943-1428-45e2-9fca-a1acec0c1004" />
</CardGroup>


# Infrastructure as Code for SRE

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Release-Engineering/Infrastructure-as-Code-for-SRE/page

Explains Infrastructure as Code for SREs, covering tools, best practices, CI/CD, policy as code, state management, drift detection, and automating AWS IAM using Terraform.

Welcome back. This lesson covers Infrastructure as Code (IaC): the practice of defining and managing infrastructure using the same engineering workflows as application code — version control, code review, automated testing, and repeatable deployments. IaC transforms provisioning from a manual, error-prone activity into a reliable, auditable, and testable process.

In the past, provisioning meant SSHing into machines, editing configs by hand, restarting services, and hoping nothing broke. That produced infrastructure drift, inconsistent environments, and no reliable history of changes. IaC flips that model: you declare the desired state in files, keep them in Git, review changes via pull requests, preview their effects, and apply them automatically. The result: consistent environments, auditable change history, and the ability to test updates before they reach production.

<Frame>
  <img alt="A slide titled &#x22;Infrastructure as Code – The 'Stop clicking buttons' Revolution&#x22; comparing the old manual server workflow (SSH, edit configs, restart services, hope nothing breaks, forget what changed) with the IaC approach (write changes as code, review, apply automatically, track in version control). The left side lists the old five-step manual process and the right side shows the four-step automated IaC process." />
</Frame>

Why SRE teams adopt IaC

* No more snowflake servers — the same code builds identical systems.
* Predictable disaster recovery: rebuild full environments from code.
* Full, auditable change tracking — know who changed what and when.
* Test infrastructure updates before they reach production to avoid surprises and late-night incidents.

<Frame>
  <img alt="A presentation slide titled &#x22;Infrastructure as Code – The 'Stop clicking buttons' Revolution&#x22; showing four colorful cards explaining why SREs love IaC. The cards list: &#x22;No snowflake servers,&#x22; &#x22;Disaster recovery,&#x22; &#x22;Change tracking,&#x22; and &#x22;Test before deploy,&#x22; with a small &#x22;© KodeKloud&#x22; footer." />
</Frame>

Core IaC tools

| Tool               | Purpose                                      | Notes                                      |
| ------------------ | -------------------------------------------- | ------------------------------------------ |
| Terraform          | Multi-cloud provisioning via declarative HCL | Widely used, supports modules and backends |
| AWS CloudFormation | AWS-native infrastructure as code            | Deep AWS integration; YAML/JSON templates  |
| Pulumi             | Code-first IaC using familiar languages      | Use TypeScript, Python, Go, etc.           |

IaC best practices

* Version control everything — if it’s not in Git, it’s not managed.
* Use variables; avoid hard-coded values to make configs reusable.
* Embrace modules and DRY principles to prevent copy-paste errors.
* Treat infrastructure changes like app changes: require pull requests, preview plans, and run automated checks.

<Frame>
  <img alt="A presentation slide titled &#x22;IaC Best Practices&#x22; showing a vertical checklist with green checkmarks for &#x22;Version Control Everything&#x22;, &#x22;Use Variables, Not Hardcoded Values&#x22;, and &#x22;Modules: Don't Repeat Yourself&#x22;, plus an unchecked &#x22;Review Everything&#x22;. A faded sidebar lists related tips like &#x22;Pull requests for all changes&#x22;, &#x22;Preview with terraform plan&#x22;, &#x22;Require peer approval&#x22;, and &#x22;Automated tests for IaC&#x22;." />
</Frame>

<Callout icon="lightbulb">
  Always keep your infrastructure code as the single source of truth. Use pull requests and plan previews so reviewers can see intended changes before apply.
</Callout>

Example: keep all infrastructure files in Git (good) and avoid making manual changes directly in the cloud console (bad).

```bash theme={null}
