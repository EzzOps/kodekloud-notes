# Database size growth over 12 months (in GB)
Jan: 120
Feb: 127
Mar: 134
Apr: 141
May: 148
Jun: 156
Jul: 164
Aug: 173
Sep: 182
Oct: 191
Nov: 210 (Black Friday sale)
Dec: 230 (Holiday season)
```

## Proactive vs reactive

Both proactive and reactive controls are necessary:

* Proactive: forecast demand, load-test, schedule upgrades, and right-size infrastructure ahead of peaks.
* Reactive: auto-scale, throttle, queue, or gracefully degrade when unexpected spikes occur.

<Frame>
  <img alt="A presentation slide titled &#x22;Proactive vs Reactive Capacity Management&#x22; showing a two-column table comparing proactive practices (forecast demand, load testing, design for growth, scheduled upgrades) with reactive ones (respond to real-time changes, auto-scale, graceful degradation, throttle/queue). A footer notes you need both: proactive stays ahead, reactive keeps you running." />
</Frame>

<Callout icon="lightbulb">
  Proactive planning reduces the number of emergency scale-ups you must perform, while reactive mechanisms keep the service available during unpredicted spikes. Both are necessary.
</Callout>

## Reactive strategy example: Kubernetes HPA

Kubernetes Horizontal Pod Autoscaler (HPA) is a common reactive tool that scales pods based on CPU, memory, or custom metrics. HPA complements capacity planning by absorbing short-term bursts while longer-term capacity is provisioned.

<Frame>
  <img alt="A presentation slide about capacity planning that highlights a reactive auto-scaling strategy. It shows the Kubernetes Horizontal Pod Autoscaler (HPA) logo with the note that it automatically adds or removes pods based on CPU and memory usage." />
</Frame>

Example HPA configuration (scales between 3 and 10 replicas based on average CPU utilization):

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kodekloud-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kodekloud-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Thresholds and alerts

Translate metrics into actionable alerts with thresholds that give you time to act while minimizing false positives.

<Frame>
  <img alt="A presentation slide titled &#x22;Setting Thresholds and Alerts&#x22; with a colorful funnel graphic on the left and a list of threshold types on the right. The list shows Utilization Threshold, Growth Rate Threshold, Time-to-Exhaustion, Performance Degradation, and Error Rate, each with a short description and icon." />
</Frame>

Common alert types:

* Utilization thresholds (CPU %, memory %).
* Growth rate thresholds (rate of change).
* Time-to-exhaustion (predict when a resource will be depleted).
* Performance degradation (p95/p99 latency increases).
* Error-rate thresholds (5xx spike).

<Frame>
  <img alt="A slide titled &#x22;Setting Thresholds and Alerts&#x22; showing a resource-monitoring diagram for CPU, Memory, Disk Space, Database Connections, and Request Queue. Each resource lists warning and critical percentage thresholds and a recommended action (e.g., scale out, scale up, add storage, increase pool)." />
</Frame>

Example thresholds and recommended actions:

| Resource       | Warning | Critical | Typical Action                      |
| -------------- | ------- | -------- | ----------------------------------- |
| CPU            | 70%     | 85%      | Scale out pods or add CPU           |
| Memory         | 80%     | 90%      | Increase instance size or add nodes |
| DB connections | 70%     | 85%      | Increase pool size, add replicas    |
| Request queue  | 60%     | 80%      | Add workers or throttle producers   |
| Disk           | 70-80%  | 90%      | Add storage or offload data         |

## Summary

Effective capacity planning combines measurement, forecasting, sensible thresholds, and automation. Build visibility with observability tools, choose forecasting models that reflect your workload, and implement both proactive strategies (planning and testing) and reactive controls (autoscaling and graceful degradation). This approach reduces outages, controls cost, and supports growth while keeping users happy.

## Links and references

* [Kubernetes Autoscaling (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [Prometheus: Monitoring System](https://prometheus.io/)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [Loki (Grafana Loki) Logs](https://grafana.com/oss/loki/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/5863d35a-6f2f-4453-9961-85eeb243c287/lesson/92bf54eb-30d0-4a80-ad50-97f2a383b609" />
</CardGroup>


# Change Management for Reliability

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Managing-Complexity-Risk-and-Toil/Change-Management-for-Reliability/page

Guidance for SRE change management to reduce production incidents using safe deployment strategies, monitoring, automated rollbacks, testing, and policies to balance velocity and stability

Welcome — this lesson covers change management for reliability in Site Reliability Engineering (SRE).

Change is both essential and risky. This guide explains how to accept that change is inevitable, and how to reduce the chance that a change causes production outages. Follow these practices to move faster with lower risk.

Start with a common story: an engineer pushes a hotfix directly to production without review because “it was just a quick config tweak.” Small, unreviewed changes frequently cause large, preventable incidents. That’s why structured change management is essential.

Change is the primary source of production incidents. At Google, roughly 70% of incidents were traced to system modifications — deployments, configuration edits, dependency updates, or environment changes. In short: most production issues are caused, directly or indirectly, by change.

<Frame>
  <img alt="A slide titled &#x22;Changes and Service Reliability&#x22; stating that change is the primary source of production incidents, with a pie chart from Google's analysis showing 70% caused by system modifications." />
</Frame>

If you care about uptime, you must care about how changes are made. Most engineers will at some point be involved in a production outage. The difference between a career-limiting event and a learning experience is often how well your change management process limits and contains damage.

Common change failure modes (what often goes wrong):

| Change Type            | Typical Failure Modes                                            |
| ---------------------- | ---------------------------------------------------------------- |
| Deployments / Rollouts | Expose code bugs, configuration drift, or rollout tooling errors |
| Configuration edits    | Typos, wrong environment targets, or incorrect values            |
| Dependency upgrades    | API changes, behavioral regressions, or compatibility breaks     |
| Environment changes    | OS/runtime updates, container runtime differences, infra changes |
| Database migrations    | Long-running locks, schema incompatibilities, or data corruption |

<Frame>
  <img alt="A presentation slide titled &#x22;Changes and Service Reliability&#x22; showing a table of common change failure modes and their failure causes. It lists Deployment Failures, Config Changes, Dependency Updates, Env Changes, and DB Migrations with brief descriptions of what can go wrong." />
</Frame>

The core SRE challenge is balancing two competing goals: velocity (delivering business value quickly) and stability (keeping services reliable during change). Your processes should let teams move fast while keeping risk acceptable.

<Frame>
  <img alt="A slide titled &#x22;Changes and Service Reliability&#x22; showing a balance scale that contrasts Velocity (deploying changes quickly for business value) on the left with Stability (maintaining reliable service during changes) on the right." />
</Frame>

Think of change like training at the gym: someone who trains consistently builds resilience. Frequent, small, validated changes increase resilience, speed feedback loops, and make recovery easier. Infrequent, large, untested changes are high risk.

When testing and validation improve, teams can increase agility while preserving reliability. This produces a virtuous cycle:

Small, frequent changes → faster feedback → improved testing and validation → higher confidence → greater stability.

<Frame>
  <img alt="A slide titled &#x22;Change and Stability — Partners, Not Opposites&#x22; showing a colorful circular diagram called &#x22;The Change Confidence Loop.&#x22; The loop links small, frequent changes to better feedback, improved testing/validation, increased confidence, and greater stability." />
</Frame>

Deployment strategies that reduce blast radius and increase safety

| Strategy      | Description                                                                                                                                  | When to use                                                        |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Blue-green    | Deploy the new version alongside the current one, validate it, then switch traffic. Enables near-instant rollback and environment isolation. | Fast API updates, minimal downtime requirements                    |
| Canary        | Roll out to a small subset of servers or users (e.g., 5% of traffic) and observe behavior before increasing traffic.                         | Testing new logic against production traffic with limited exposure |
| Feature flags | Ship code behind toggles and control feature exposure independently of deploys; enables gradual rollouts and rapid rollbacks.                | Complex feature rollouts, gradual experimentation, A/B testing     |

<Frame>
  <img alt="A presentation slide titled &#x22;Safe Deployment Strategies&#x22; showing a table that compares three deployment approaches—Blue-Green, Canary, and Feature Flags—with short descriptions, KodeKloud use cases, and benefits. The table highlights examples like instant rollback for Blue-Green, limited blast radius for Canary, and separating deployment from feature release for Feature Flags." />
</Frame>

Monitoring and observability during change

Change without monitoring is flying blind. Track these key metrics during and after deployments to determine whether a change is safe or if it should be halted/rolled back:

| Metric                         | Why it matters                                                           |
| ------------------------------ | ------------------------------------------------------------------------ |
| Error rates                    | Detect spikes in failures immediately after a change                     |
| Latency                        | Identify degraded response times affecting UX                            |
| Traffic                        | Verify that users can access services and that routing behaves correctly |
| Saturation (CPU, memory, disk) | Catch resource pressure that can lead to cascading failures              |
| Deployment progress            | Detect stuck rollouts or nodes that fail to update                       |

Use dashboards and alerting based on these metrics to trigger automated or human responses.

<Frame>
  <img alt="A presentation slide titled &#x22;Monitoring Changes&#x22; with a target and several colorful arrows on the left and a checklist on the right listing monitoring metrics: Error Rates, Latency, Traffic, and Saturation with brief questions about each. The slide illustrates tracking system health and performance after changes." />
</Frame>

When in doubt — roll back

Prefer automatic rollbacks where possible. Modern deployment systems can detect problematic behavior and revert changes before human intervention is required. Common automatic rollback triggers:

* Error rate thresholds exceeded
* Latency thresholds exceeded
* Health checks failing for the new version
* Deployment timeouts or stalled rollouts

These triggers should align with your SLOs and error budgets so rollbacks happen before user experience degrades unacceptably.

<Frame>
  <img alt="A presentation slide titled &#x22;Automatic Rollback Mechanisms&#x22; showing four colored tiles for rollback triggers: Error Rate Thresholds, Latency Thresholds, Failed Health Checks, and Deployment Timeouts. Each tile includes a short description of when to roll back (excess errors, degraded response times, failed health checks, or deployments taking too long)." />
</Frame>

Practical example — Argo Rollouts + Prometheus automated canary analysis

Below is a practical Argo Rollouts example that references an AnalysisTemplate named "error-rate-check". The template uses a Prometheus query to compute an error rate and triggers a failure (and thus a rollback) if the measured error rate exceeds the provided threshold argument.

Rollout (references the analysis template and sets the errorRate arg):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: example-rollout
spec:
  replicas: 3
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: { duration: 30s }
        - analysis:
            templates:
              - templateName: error-rate-check
                args:
                  - name: errorRate
                    value: "5" # 5% error threshold
        - setWeight: 50
        - pause: { duration: 30s }
        - setWeight: 100
```

AnalysisTemplate (invoked by the Rollout; uses a Prometheus query and a failureCondition referencing the passed argument):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-check
spec:
  metrics:
    - name: http-error-rate
      provider:
        prometheus:
          # Prometheus query computing percentage of error requests over total requests in the last 1m
          query: |
            sum(rate(http_request_errors_total[1m]))
            /
            sum(rate(http_requests_total[1m])) * 100
      # Use the passed-in argument to decide when the metric indicates failure.
      # This template evaluates to a numeric "result" and the rollout will fail if the condition is true.
      failureCondition: result > {{args.errorRate}}
```

<Callout icon="lightbulb">
  Align thresholds (for example, 5%) with your SLOs and error budget. Use conservative values for early-stage rollouts and tighten them as you gain confidence.
</Callout>

Post-deployment verification

Continue validating after rollout with a layered approach:

* Smoke tests: basic functionality checks to confirm the service is up.
* Integration tests: validate interactions between services.
* Performance tests: simulate real-world load to check behavior under stress.
* Canary user testing: let a subset of real users try the change.
* Gradual traffic shifting: ramp traffic slowly while watching metrics.

<Frame>
  <img alt="A slide titled &#x22;Post-Deployment Verification&#x22; showing a funnel diagram of the deployment verification process with stages: Smoke Tests, Integration Tests, Performance Tests, Canary User Testing, and Gradual Traffic Shifting. Each stage includes a short note (e.g., basic functionality checks, validating component interactions, verifying performance, real users testing, and gradually shifting traffic)." />
</Frame>

Change management policy — what to define

A written policy should specify different procedures for different change types (regular deployments, DB changes, emergency changes). For example:

| Change Category             |                          Scheduling | Typical Window          | Approval                        |
| --------------------------- | ----------------------------------: | ----------------------- | ------------------------------- |
| Regular deployments         |               Planned and scheduled | Tue/Thu 10:00–14:00 UTC | Team or release manager         |
| Database changes/migrations |                  Low-traffic window | Sun 02:00–06:00 UTC     | DB lead + SRE                   |
| Emergency changes           | As needed, follow emergency process | N/A                     | Pre-defined approver (SRE Lead) |

<Frame>
  <img alt="A slide titled &#x22;Practical Change Management Rules&#x22; showing a three-column table comparing Regular Deployments, Database Changes, and Emergency Changes across rows for days, time, reason, approval required, and approver. It lists windows like Tuesday/Thursday 10:00–14:00 UTC for regular deployments and Sunday 02:00–06:00 UTC for database changes, while emergency changes are N/A and require SRE Lead approval." />
</Frame>

Your policy should also specify:

* When to require a postmortem (for example, after emergency changes or any incident causing customer impact).
* Freeze periods when changes are restricted (e.g., during product launches or high-traffic events).
* Risk categories (low/medium/high) with approval gates and explicit approvers.

Wrap-up

Effective change management helps teams innovate without compromising reliability. Every deployment, configuration tweak, or feature also impacts capacity — the next step in reliable operations is capacity planning.

Related resources and references:

* [Site Reliability Engineering (SRE) concepts](https://sre.google/sre-book/)
* [Service-level objectives (SLOs)](https://en.wikipedia.org/wiki/Service-level_objective)
* [Argo Rollouts documentation](https://argoproj.github.io/argo-rollouts/)
* [Prometheus monitoring](https://prometheus.io/)
* [Kubernetes basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/5863d35a-6f2f-4453-9961-85eeb243c287/lesson/837c92f8-cd10-4ed1-8797-1123a031419d" />
</CardGroup>
