# Starting Your Migration

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-What-should-you-look-into/Starting-Your-Migration/page

Guidance for executing iterative small-batch platform migrations with observability, validation, risk-reducing rollouts, decommissioning legacy components, and managing technical debt.

Now it’s time to move from planning into execution. After weeks of mapping components and designing the target architecture, this lesson shows how to begin shifting workloads from the legacy platform to the new one. The execution phase is iterative and hands-on: install core platform components, migrate services incrementally, verify observability and integrations, publish the new implementations, then decommission legacy counterparts.

The migration approach below emphasizes a repeatable, low-risk cycle and strong observability coverage so you can detect regressions and operational issues early.

## Migration cycle (repeatable)

Follow a small-batch, repeatable loop. Each iteration should be scoped to a single component, service, or small group of related components.

| Step                               | Purpose                           | Key actions                                                                     |
| ---------------------------------- | --------------------------------- | ------------------------------------------------------------------------------- |
| Install core platform components   | Prepare the target environment    | Deploy observability agents, collectors, authentication, and central dashboards |
| Select a component to migrate      | Limit blast radius                | Choose one service or small subsystem with clear dependencies                   |
| Migrate and validate observability | Ensure telemetry continuity       | Verify metrics, logs, traces, dashboards, and alerts for the migrated component |
| Publish migrated component         | Promote to production             | Flip routing/feature flags or update deployment targets                         |
| Deactivate legacy implementation   | Remove duplicated work            | Decommission or disable old service once validated                              |
| Repeat                             | Continue until migration complete | Continue iterating until all components are migrated                            |

Use feature flags, canary releases, and small-batch rollouts to reduce risk. After each iteration, update runbooks, documentation, and on-call alerts so the operations team has accurate information during incidents.

## Validation and observability

During every migration iteration verify both functional correctness and observability:

* Validate end-to-end functionality: API responses, background jobs, scheduled tasks.
* Confirm telemetry integrity: metrics, logs, traces, and distributed tracing links.
* Validate dashboards and alerts: ensure existing alerts fire appropriately and dashboards reflect the new implementation.
* Add tests and synthetic checks to prevent regressions.

Include observability checks as part of your CI/CD pipeline and post-deployment validation tasks so telemetry gaps are detected early.

## Managing technical debt during migration

Technical debt often accumulates when teams take shortcuts to meet deadlines or unblock work. If left untracked, debt slows future development and increases operational risk. Treat debt as first-class work and incorporate remediation into migration sprints.

| Action                                   | Why it matters                           | Example                                                    |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------------------------- |
| Identify and document deviations         | Ensures visibility and prioritization    | Create backlog items for every intentional workaround      |
| Prioritize by risk and impact            | Focus limited effort on high-value fixes | Prioritize items that affect availability or observability |
| Include remediation in migration sprints | Avoid indefinite deferral                | Schedule fixes alongside migration tasks                   |
| Use small-batch rollouts                 | Minimize blast radius of risky changes   | Canary or phased deployment strategies                     |
| Validate observability coverage          | Prevent blind spots                      | Add dashboards, alerts, and tests for migrated components  |
| Communicate deprecations                 | Reduce surprise to consumers             | Update API docs and notify stakeholders of timeline        |

<Callout icon="lightbulb">
  Track technical debt items as first-class work items in your backlog. Address high-risk debt early and schedule lower-risk items into regular maintenance windows.
</Callout>

<Frame>
  <img alt="The image is a flowchart outlining steps for starting a migration process, including installing core components, migrating, verifying, publishing, and deactivating, with a loop for repeating the process. It also mentions controlling technical debt, dashboards, and alerts." />
</Frame>

## Practical checklist (quick reference)

* Install and verify observability agents, collectors, and central dashboards.
* Pick one small component for the next migration iteration.
* Validate metrics, logs, and traces before and after migration.
* Update dashboards and alerts to reference the new implementation.
* Run canaries or smoke tests in production-like traffic.
* Flip traffic or promote the new service once validated.
* Decommission the legacy component and update runbooks.
* Close or reschedule tracked technical debt items.

## Links and references

* [Datadog - Migration guidance and observability best practices](https://www.datadoghq.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — general reference for deployments and rollouts

That's it for this lesson — apply the cycle repeatedly, keep observability tight, and treat technical debt as work to be planned and tracked.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/d7aaa833-22da-4f94-af5c-5d196f04ab31/lesson/f2c13f1e-18b1-478f-ad35-aa9f65813a00" />
</CardGroup>
