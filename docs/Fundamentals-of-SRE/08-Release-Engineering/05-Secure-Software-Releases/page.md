# Create the repository
aws ecr create-repository --repository-name kodekloud/records-api
```

Save the lifecycle policy as policy.json:

```json theme={null}
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 10 production images",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["prod-"],
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
```

Apply the policy:

```bash theme={null}
aws ecr put-lifecycle-policy --repository-name kodekloud/records-api --lifecycle-policy-text file://policy.json
```

Example repository access model:

```yaml theme={null}
repositories:
  production:
    read: [sre-team, deploy-service]
    write: [release-automation]
    admin: [platform-team]

  staging:
    read: [developers, qa-team]
    write: [ci-system, developers]
    admin: [team-leads]
```

Environment-specific registry settings:

```yaml theme={null}
environments:
  development:
    docker_registry: "dev-registry.kodekloud.internal"
    package_repo: "https://packages-dev.kodekloud.internal"
    retention: "7 days"
    vulnerability_scan: "advisory"

  staging:
    docker_registry: "staging-registry.kodekloud.internal"
    package_repo: "https://packages-staging.kodekloud.internal"
    retention: "30 days"
    vulnerability_scan: "blocking"

  production:
    docker_registry: "prod-registry.kodekloud.internal"
    package_repo: "https://packages-prod.kodekloud.internal"
    retention: "1 year"
    vulnerability_scan: "blocking + attestation"
    immutable: true  # Prevent overwriting tags
```

## CI/CD pipeline best practices

A robust pipeline automates build, test, security, deployment, verification, and monitoring. Key elements:

* Build artifacts in a reproducible, hermetic environment.
* Run unit, integration, and end-to-end tests before artifacts are promoted.
* Run security and vulnerability scans early (shift-left).
* Deploy to staging with automated integration tests and performance checks.
* Require explicit approvals for risky production changes (policy as code).
* Perform health checks and automated rollbacks on failure.

A healthy pipeline sequence:
Build → Test → Security scan → Deploy to staging → Integration tests → Deploy to production → Health check → Monitor

<Frame>
  <img alt="The image is a slide titled &#x22;CI/CD Pipeline Best Practices&#x22; showing a circular workflow. It diagrams stages: Build → Test → Security scan → Deploy to staging → Integration tests → Deploy to production → Health check → Monitor." />
</Frame>

## Secrets management

Secrets and credential leaks are a common source of incidents. Follow these rules:

* Never hard-code secrets in source code or config files.
* Centralize secrets in a dedicated secrets manager (HashiCorp Vault, AWS Secrets Manager, etc.).
* Use short-lived, revocable credentials and automate secret rotation.
* Monitor for leaked secrets and automate incident response.

<Callout icon="warning">
  Never commit credentials or long-lived keys to source control. Assume secrets will leak and design for short-lived, revocable credentials plus automated rotation and monitoring.
</Callout>

<Frame>
  <img alt="A slide titled &#x22;CI/CD Pipeline Best Practices&#x22; listing four tips: 01 Never hardcode secrets, 02 Use secret management tools, 03 Rotate secrets regularly, and 04 Monitor for secret leaks." />
</Frame>

## Communication and continuous learning

Release engineering is as much about people and process as it is about tools.

* Before release: Notify stakeholders, prepare the support rota, and document rollback and mitigation plans.
* During release: Publish real-time updates and decide Go/No-Go using metrics (error rate, latency, saturation) rather than intuition.
* After release: Compare outcomes to success criteria, run blameless postmortems on failures, and update runbooks and automation.

<Frame>
  <img alt="A slide titled &#x22;Communication and Learning&#x22; showing three connected stages—Before Release, During Release, and After Release. Each stage has checklist bullets (e.g., stakeholders notified, rollback plan and support ready; real-time updates and metric-based Go/No-Go; success metrics, blameless post-mortem, and docs/process updates)." />
</Frame>

## Wrap-up

This lesson covered the operational patterns, technical controls, and organizational practices that make change safe and predictable:

* Automation and policy-as-code
* Progressive delivery (canaries, feature flags)
* Fast, tested rollback processes
* Artifact repository management with lifecycle and access controls
* Secure CI/CD pipelines with shift-left security
* Secrets management with rotation and monitoring
* Continuous communication and blameless learning

The next hands-on topic dives into observability—logs, metrics, traces, dashboards, and alerting—where release engineering and SRE work together to ensure releases behave as expected in production.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [AWS Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)
* [Google Artifact Registry](https://cloud.google.com/artifact-registry)
* [HashiCorp Vault](https://www.vaultproject.io/)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/5c7b8c62-d391-4230-b4ac-9417a91e5760" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/d6970a1f-f93f-4d6c-9ff3-8738274e912e" />
</CardGroup>


# Secure Software Releases

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Release-Engineering/Secure-Software-Releases/page

Guide to securing software releases by integrating CI/CD security checks, SBOMs, dependency and container scanning, least privilege, artifact signing, and safe authentication in deployment pipelines.

In this lesson we focus on making software releases secure and resilient. Security is not only about what features you ship — it’s about ensuring the release process itself does not introduce risk. Developers write code, security teams define controls, and SREs operationalize and enforce those controls. When ownership gets assumed by others, SREs often become the last line of defense; many postmortems note “this should have been caught at deployment.”

<Frame>
  <img alt="A presentation slide titled &#x22;Security in Software Releases Is Essential&#x22; showing an &#x22;Expensive Hall of Fame&#x22; of three major incidents. It lists SolarWinds hack (2020), Log4Shell/Log4j (2021), and the Target breach (2013) with short notes on their impacts." />
</Frame>

Real incidents demonstrate how the release path can amplify risk: the SolarWinds supply-chain compromise (2020) propagated a poisoned build broadly; Log4Shell (2021) showed how a single vulnerable library can cascade across ecosystems; and the Target breach (2013) involved stolen deployment credentials with costly business impact.

SREs validate deployments, enforce security policies, and stop misconfigurations before they become incidents.

<Frame>
  <img alt="A presentation slide titled &#x22;Security in Software Releases Is Essential&#x22; stating &#x22;SREs are the last line of defense.&#x22; It lists three points showing developers write code (SREs ensure secure deployment), security teams set policies (SREs enforce them), and everyone assumes someone else checks (SREs actually check)." />
</Frame>

Common release-path risks and mitigations

| Risk                                                | Why it matters                                                                                        | Typical mitigation                                                         |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Vulnerable third-party dependencies                 | Large dependency trees mean most code is third-party; one vulnerable package can affect many services | Automated dependency scanning (pip-audit, npm audit), SBOM generation      |
| Misconfigured permissions (e.g., public S3 buckets) | Overly-broad permissions expose data and infrastructure                                               | Principle of least privilege, scoped IAM policies, automated policy checks |
| Lack of automation or visibility                    | Manual audits don’t scale; blind spots allow vulnerabilities to slip to production                    | CI-driven scanning, artifact signing, centralized logs/alerts              |
| Weak authentication for registries/pipelines        | Hardcoded credentials or weak tokens lead to credential theft                                         | Token-based auth, short-lived credentials, secrets management              |

A small misstep can expose everything. For example:

```bash theme={null}
