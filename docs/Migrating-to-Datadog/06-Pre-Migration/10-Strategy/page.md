# Inspect rollout history for a deployment
kubectl rollout history deployment/my-app

# Roll back to the previous revision
kubectl rollout undo deployment/my-app

# Roll back to a specific revision (if available)
kubectl rollout undo deployment/my-app --to-revision=2
```

For Helm-managed releases:

```bash theme={null}
helm history my-release
helm rollback my-release 1
```

Quick reference table

| Tool       | Action                          | Command example                                          |
| ---------- | ------------------------------- | -------------------------------------------------------- |
| Kubernetes | Show rollout history            | `kubectl rollout history deployment/my-app`              |
| Kubernetes | Roll back to previous revision  | `kubectl rollout undo deployment/my-app`                 |
| Kubernetes | Roll back to specific revision  | `kubectl rollout undo deployment/my-app --to-revision=2` |
| Helm       | Show release history            | `helm history my-release`                                |
| Helm       | Roll back to a specific release | `helm rollback my-release 1`                             |

<Frame>
  <img alt="The image illustrates a software rollback process, showing the transition from a new component (v2.1) back to an old stable component (v1.9) within a CI/CD pipeline. It emphasizes retaining version 1.9 until all integrations are validated." />
</Frame>

Thinking about the environment's sustainability, it's important to keep older versions around while not all components are migrated. Erasing older artifacts or images should only be done once all integrations have been validated and the migration solution has earned your trust.

> **lightbulb** Keep build artifacts, deployment manifests, and image tags for a reasonable retention period. This ensures you can quickly redeploy a known-good version without relying on rebuilds that may produce different artifacts.

> **warning** Be cautious with stateful or schema-changing migrations. Rolling back code without rolling back incompatible database schema changes can leave the system in an unusable state. Coordinate application, schema, and data migrations with clear forward/backward compatibility strategies.

<Frame>
  <img alt="The image is an infographic titled &#x22;Rollback,&#x22; outlining four steps: protecting the environment during bad deployments, reverting to stable versions using CI/CD and IaC, maintaining observability during issues, and removing old versions after validation." />
</Frame>

Best practices

* Automate rollback paths where possible and test them regularly as part of your deployment pipeline.
* Retain artifacts (images, manifests, Helm charts) for a defined retention window to guarantee reproducibility.
* Maintain full observability (logs, metrics, traces) before and after rollbacks to speed root-cause analysis.
* Use feature flags and progressive rollouts (canary, blue/green) to reduce blast radius and make rollback safer.
* Document rollback runbooks and make them easily accessible to on-call teams.

Summary

* Rollbacks are an intentional, tested part of release and migration strategies.
* Automate rollback paths and preserve artifacts and observability so you can recover fast and investigate with full context.
* Treat data migrations and schema changes with extra caution—ensure forward/backward compatibility or add explicit migration rollback steps.

Links and references

* [Kubernetes Rollouts](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)
* [Helm Rollbacks](https://helm.sh/docs/helm/helm_rollback/)
* [CI/CD best practices for safe deployments](https://www.redhat.com/en/topics/devops/what-is-ci-cd)

That’s it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/ce3fc0dc-fca5-4eb2-b433-b850e85b7582)


# Strategy

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Strategy/page

Guidance for planning and executing a risk‑controlled migration from legacy observability to a new platform, covering strategies, success criteria, approaches, validation gates, and scheduling buffers.

This lesson explains how to plan, execute, and validate a migration from a legacy observability stack to a new platform. After you map your legacy environment and pick a target observability solution, establish a migration strategy that defines the steps, timelines, verification gates, and how teams will be coached through the change.

## Key success criteria

Any migration plan should target these three outcomes:

* Impactless: End users and production behavior must not be negatively affected. Platform teams should coordinate feature migrations, communicate deadlines and changes clearly, and expect a feedback loop where product teams request help or provide implementation feedback.
* Legacy deactivation: Decommission legacy tools as equivalent capabilities are validated on the new platform to avoid duplication and configuration drift. Ownership for deactivation is determined by where the feature runs — either the platform team or the owning product team.
* Full coverage: Confirm that every monitoring capability—metrics, logs, traces, and alerting—works on the new platform before switching off legacy tooling. Missing observability data during an incident severely impedes debugging and recovery.

> **warning** Do not deactivate legacy systems until you have validated coverage and run-throughs for critical incidents. Accidental gaps in observability are a major operational risk.

<Frame>
  <img alt="The image presents a strategy diagram with three stages: &#x22;Impactless,&#x22; &#x22;Legacy Deactivation,&#x22; and &#x22;Full Coverage,&#x22; each in different colors with icons above them." />
</Frame>

## Types of migration approaches

Two common migration approaches are used depending on risk tolerance, timelines, and organizational capacity.

| Approach             | When to use it                                                | Pros                                                                            | Cons                                                                             |
| -------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Phased (recommended) | When you want to mitigate risk and learn incrementally        | Lower risk; easier troubleshooting; teams adapt dashboards and alerts gradually | Longer overall duration because legacy remains active until coverage is verified |
| Big-bang             | When timelines are tight and business requires a fast cutover | Fast completion; avoids long-running parallel systems                           | High risk of missing pieces, poor adoption, and operational mistakes             |

Phased approach (recommended when risk mitigation and learning are priorities)

* Migrate features incrementally. Map features (dashboards, alerts, traces, log parsers) and move them one at a time.
* Easier isolation of issues, better troubleshooting, and continuous improvement.
* Allows product teams to adopt and tune dashboards/alerts progressively.
* Expect a longer timeline because the legacy platform stays active until verification is complete.

Big-bang approach (used when timelines are strict)

* Migrate everything in a short window and switch over at once.
* Faster overall completion but much higher risk: missing capabilities, insufficient testing, or poor adoption are common.
* Teams have less time to learn the new platform, increasing operational pressure and likelihood of mistakes.
* Only recommend this when the business accepts the higher risk for a rapid cutover.

<Frame>
  <img alt="The image compares two strategies: the Phased Approach and the Big-Bang Approach, highlighting their key characteristics such as safety, risk, planning, and learning." />
</Frame>

## Three variables that shape your migration plan

When choosing an approach and building a schedule, explicitly consider these variables:

1. Environment topology
   * Most organizations run multiple environments (development, QA/staging, production). Use lower environments to validate instrumentation, dashboards, and alerts prior to production rollout.
   * Create promotion gates (e.g., dev → staging → production) with validation checklists for each stage.

2. Team capacity
   * Estimate engineering bandwidth and coordinate with project managers and product owners. Migration work competes with feature work and requires realistic capacity planning.
   * Identify owners for observability artifacts (dashboards, monitors, runbooks) to avoid single-person bottlenecks.

3. Business backlog and priorities
   * Align migration timelines with business milestones. Migration typically competes with product backlog items; coordinate with stakeholders so critical features aren’t blocked.
   * Accept that business work rarely pauses for infrastructure projects—prioritize migration tasks that reduce risk or unblock high-impact features.

<Frame>
  <img alt="The image is a strategy diagram outlining three areas to consider: Environment (size and complexity), Team (capacity), and Business (deadlines and priorities)." />
</Frame>

## Schedule and buffers

Build a timeline that includes explicit verification gates and contingency buffers. Even well-planned migrations surface edge cases: add slack time for validating coverage, fixing instrumentation, and iterating on alerts and dashboards.

Recommended practices:

* Add a contingency buffer of 10–25% of the planned duration to absorb unforeseen issues.
* Include verification gates after each environment promotion (e.g., smoke tests, alert validation, incident runbooks).
* Run full-playbook incident simulations in a staging environment to confirm observability coverage and resolution steps.

<Frame>
  <img alt="The image outlines a strategy with a timeline showing a migration phase lasting 8 weeks and a 1-2 week buffer. It emphasizes avoiding management pressure and ensuring engineer confidence." />
</Frame>

> **lightbulb** Add a contingency buffer to your timeline (for example, 10–25% of the planned duration). This protects the team from last-minute pressure and gives time to verify that coverage, alerts, and dashboards are functioning before decommissioning the legacy system.

## Summary

* Define clear success criteria: impactless migration, controlled legacy deactivation, and full coverage on the new platform.
* Choose the migration approach that matches your risk tolerance and timelines: phased for lower risk and learning; big-bang only when a fast cutover is required and the business accepts higher risk.
* Account for environment topology, team capacity, and business priorities when scheduling work and assigning owners.
* Add verification gates and schedule buffers to reduce risk, build confidence, and ensure reliable decommissioning of legacy tools.

That's it for this lesson. I hope you found it helpful.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/68d2c963-cc16-48bd-a963-cfa31c021a60)
