# Defining Your Architecture

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Defining-Your-Architecture/page

Guidelines for designing scalable, secure enterprise observability architecture covering access controls, data security, backups, compliance, CI/CD artifact security, and operational support models

In this lesson we cover how to design an enterprise-grade observability architecture that is scalable, resilient, and aligned with Datadog best practices. Design holistically—your observability platform should serve the entire organization (multiple teams, environments, and regulatory needs), not just a single project or environment.

Observability platforms have different priorities and trade-offs compared to other platform types (e.g., data processing or CI/CD). Keep those differences in mind when defining controls, ownership, and operational processes.

> **lightbulb** This article focuses on architecture for observability solutions. If you are designing a different type of platform (e.g., pure data processing or CI/CD), some priorities and controls may differ.

Core areas to prioritize for enterprise observability

| Area               | Why it matters                                        | Key controls & examples                                                      |
| ------------------ | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| Access             | Limits blast radius, enforces separation of duties    | RBAC, least-privilege roles, centralized identity (SSO, SCIM), audit logging |
| Data security      | Protects sensitive telemetry and credentials          | TLS, encryption at rest, certificate management, VPN/private links           |
| Backup & retention | Satisfies operational, auditing, and regulatory needs | Retention policies, archival for logs/traces, backup schedules               |
| Compliance         | Demonstrates controls and supports audits             | Policy evidence, access logs, retention proof, automated reporting           |

<Frame>
  <img alt="The image describes four key components of creating an enterprise-grade architecture: Access, Data Security, Backup/Retention, and Compliance, each with brief explanations." />
</Frame>

Artifact management and automated security controls

Collect build artifacts—container images, application libraries, packages—into a managed artifact repository. All artifacts intended for production use should be gated by automated security checks during CI/CD so only vetted components move downstream.

Essential automated security controls to integrate into build and release pipelines:

* Image scanning (container vulnerability scanning)
* SAST (Static Application Security Testing)
* SCA (Software Composition Analysis)
* Runtime vulnerability assessment and policy enforcement

Integrate these checks as pipeline gates so artifacts are promoted or quarantined based on policy. This approach preserves security posture while minimizing friction for development teams.

Table: Example artifact flow and controls

| Stage         | Typical controls                   | Outcome                            |
| ------------- | ---------------------------------- | ---------------------------------- |
| Build         | SAST, unit tests                   | Fails fast for code-level issues   |
| Package       | SCA, SBOM generation               | Identifies vulnerable dependencies |
| Image publish | Container image scanning, signing  | Quarantine or sign for promotion   |
| Release       | Policy enforcement, canary rollout | Controlled production rollout      |

<Frame>
  <img alt="The image depicts a flowchart showing security controls including image scanning, SAST, SCA, and vulnerability assessment applied to Docker, Helm, and other components, leading to an organization." />
</Frame>

Operational readiness: support model and escalation

A clear support model reduces mean time to resolution (MTTR) and ensures observability issues are routed efficiently. Document roles, escalation paths, SLAs, and runbooks so on-call engineers and platform teams can act confidently.

A typical three-step support flow:

1. Open a ticket in the service platform (examples: [ServiceNow](https://www.servicenow.com/), [Zendesk](https://www.zendesk.com/)).
2. Internal platform or SRE team performs initial triage, mitigation, and root-cause analysis.
3. If required, escalate to enterprise/vendor support for deeper investigation or product-level issues.

Include these operational artifacts in your documentation:

* Runbooks for common alerts and outages
* Contact and escalation matrix with SLAs
* Playbooks for incident postmortems and remediation
* Access and authorization procedures for vendor support engagement

<Frame>
  <img alt="The image shows a three-step contact process: Initial Contact via ticket, Second Contact with an internal platform team, and Third Contact through enterprise support." />
</Frame>

Summary and next steps

* Build an observability architecture that scales across teams and environments by prioritizing access control, data security, retention, and compliance.
* Gate artifacts with automated security controls in CI/CD to maintain velocity and safety.
* Define support models, SLAs, and runbooks so teams can operate reliably and escalate when necessary.

References and further reading

* [Datadog Best Practices](https://www.datadoghq.com/)
* [Kubernetes Documentation](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [ServiceNow](https://www.servicenow.com/)
* [Zendesk](https://www.zendesk.com/)

That's it for this lesson. I hope you found it useful and that it helps you plan a secure, compliant, and supportable observability architecture for your organization.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/1999fbe6-9b79-4b34-98f0-0d0961cc4a0d)
