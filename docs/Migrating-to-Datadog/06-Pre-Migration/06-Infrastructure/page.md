# Infrastructure

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Infrastructure/page

Guidelines and checklist for planning, validating, and coordinating staged infrastructure migrations including inventory, testing, rollouts, rollback, and communication to minimize disruption.

In this lesson we cover best practices for migrating infrastructure. Infrastructure migrations are typically more complex than application migrations because the stack is broader and more distributed. Components can include Kubernetes clusters, virtual machines, databases, serverless functions, cloud services, messaging systems, and many observability integrations (agents, API keys, exporters, and monitoring pipelines). Each of these elements must be discovered, validated, and coordinated across teams.

<Frame>
  <img alt="The image outlines components and integrations involved in migrating infrastructure, highlighting that infrastructure is harder to migrate than applications. It lists infrastructure components like Kubernetes and virtual machines, and supporting integrations such as agents and API keys." />
</Frame>

Because infrastructure components are often shared across teams, a single misconfiguration can impact large parts of the environment. That’s why infrastructure changes should be conservative, validated by stakeholders, and rolled out in stages with clear rollback paths.

## Why infrastructure migrations are harder

* Broad component surface area: clusters, VMs, databases, queues, serverless, and cloud services.
* Cross-team dependencies: shared resources mean changes can have wide impact.
* Observability complexity: agents, exporters, and API keys must be migrated and validated.
* Version and configuration sensitivity: upgrading agents or exporters can change metric labels or behavior.

## Suggested checklist for infrastructure migration

| Item                           | Purpose                                    | Example / Notes                                                                      |
| ------------------------------ | ------------------------------------------ | ------------------------------------------------------------------------------------ |
| Inventory components           | Understand scope of migration              | Kubernetes clusters, VMs, databases, serverless, queues, agents, API keys, exporters |
| Identify owners & stakeholders | Ensure accountability and impact awareness | List owners per component and communication channels                                 |
| Record versions & configs      | Verify compatibility and reproduce state   | `kubectl get nodes -o wide`, `aws ec2 describe-instances`                            |
| Define validation tests        | Confirm functionality and telemetry        | Connectivity, metrics/logs ingestion, alerting, dashboards, performance baselines    |
| Plan staged rollout            | Minimize blast radius                      | Canary -> region -> account -> global                                                |
| Define rollback procedures     | Reduce downtime if issues occur            | Automated rollback thresholds and manual steps                                       |
| Communicate status             | Keep teams informed                        | Daily standups, status dashboard, incident channel                                   |

> **lightbulb** Start by creating a shared migration plan and a migration runbook per component that includes owners, a test checklist, and rollback steps.

## Migration steps (detailed)

1. Discovery & inventory
   * Compile a complete inventory of components and integrations.
   * Map owners and downstream consumers for each item.
   * Recommended commands and tools: `kubectl`, cloud provider CLIs, CMDB exports, and observability agent registries.
2. Compatibility review
   * Check agent/exporter versions and breaking changes in release notes.
   * Validate configuration formats and credential access patterns.
3. Validation test design
   * Define tests for telemetry ingestion, alert firing, dashboard rendering, and performance baselines.
   * Create automated smoke tests where possible (synthetic requests, metric presence checks).
4. Staged rollout
   * Start with non-critical environments or canary workloads.
   * Monitor key telemetry and alert thresholds before expanding the rollout.
5. Monitoring & verification
   * Continuously verify telemetry, dashboards, and alerts after each stage.
   * Maintain a short feedback loop with affected teams.
6. Rollback & remediation
   * Trigger rollback on predefined thresholds or manual approval.
   * Post-mortem and follow-up fixes before resuming the rollout.

## Validation checklist (example)

* Telemetry: Are expected metrics and logs present in the target system?
* Alerts: Do existing alerts trigger (or remain suppressed) correctly after migration?
* Dashboards: Do visualizations show expected data and time ranges?
* Connectivity: Are components reachable and performing within SLAs?
* Performance: No regressions in latency or throughput compared to baseline.

> **warning** Because infrastructure is shared, validate changes in a staging environment first and communicate rollbacks immediately. A single misconfiguration can affect many teams.

## Communication & coordination

* The platform or central observability team should coordinate schedules, validation results, and impact notifications.
* Provide regular status updates (e.g., daily migration digest, Slack channel, runbook updates).
* Document decisions, post-migration verification steps, and any follow-up actions.

## Practical tips and commands

* Inventory examples:
  * Kubernetes: `kubectl get pods --all-namespaces -o wide`
  * AWS EC2: `aws ec2 describe-instances --filters "Name=tag:Environment,Values=prod"`
* Use automated checks to validate telemetry arrival (API queries, metric existence checks).
* Keep a change log for every component migrated and who approved it.

Successful infrastructure migration depends less on one-off technical tricks and more on coordination, thorough validation, and a careful staged rollout. With a documented plan, clear ownership, and strong communication, you can minimize disruption and achieve a smooth transition.

References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [AWS Documentation](https://docs.aws.amazon.com/)
* [Terraform Documentation](https://www.terraform.io/docs)

That's it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/d7ad7244-375e-4070-be0d-b2b1c3f4d8de)
