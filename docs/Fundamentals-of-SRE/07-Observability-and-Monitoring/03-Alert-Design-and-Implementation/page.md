# Generate synthetic traffic and logs
./scripts/generate_logs.sh

# Dashboards to inspect locally
# Engineer: operational details and drill-downs
# Executive: business impact and trends
echo "Engineer: http://localhost:3000/d/engineer-dashboard"
echo "Executive: http://localhost:3000/d/executive-dashboard"
```

Example of how the same incident might be summarized differently in each dashboard:

```text theme={null}
Engineer
Error Rate: 0.05 (5%)
- Top affected endpoints: /checkout (60%), /orders (30%), /cart (10%)
- Recent deployment: build-2026.02.15@14:32

Executive
Customer Impact: 45 errors this hour
Estimated Revenue Impact: $1,350/hour
Mitigation: Rollback payment service (in progress). ETR ~ 20 minutes.
```

That concludes this lesson's coverage of observability, dashboards, and reporting. The next material in the course covers advanced SRE practices and techniques for improving system reliability and incident response.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Grafana](https://grafana.com) — dashboard and visualization platform
* [Prometheus](https://prometheus.io/) — metrics and alerting
* [OpenTelemetry](https://opentelemetry.io/) — traces, metrics, and logs standards
* [Designing Data-Intensive Applications (book)](https://dataintensive.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/92f39ae4-b287-4850-93aa-3f0119393754/lesson/8c2096e5-2b4e-4de4-a8d2-2a71ca2a2da4)


# Alert Design and Implementation

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Observability-and-Monitoring/Alert-Design-and-Implementation/page

Guide to designing actionable alerts that reduce noise, align with SLOs and error budgets, provide context and runbooks, and route notifications to the right teams to improve reliability.

Welcome back. In this lesson we cover practical alert design and implementation: how to design alerts that reduce noise, focus responders on user-facing failures, and integrate with SLOs and error-budget-driven workflows. Good alerts improve reliability and reduce on-call fatigue; bad alerts do the opposite.

## Why alerts matter (and how they fail)

Alerts are the front line of reliability: they wake you up at 3 AM and guide day-to-day operations. Poorly designed alerts create noise, cause alert fatigue, and bury real incidents under false alarms. On-call engineers frequently receive many alerts—many of which do not require immediate action—leading to ignored or dismissed notifications and missed critical incidents.

<Frame>
  <img alt="A presentation slide titled &#x22;The Dangers of Alert Fatigue&#x22; with four colored panels numbered 01–04 listing: High Alert Volume, Unnecessary Alerts, Alert Fatigue, and Critical Incidents. The slide has a clean white background and a small &#x22;© Copyright KodeKloud&#x22; notice at the bottom." />
</Frame>

> **warning** Alert fatigue is real: prioritize signals that require immediate human action and reduce noisy, low-value alerts. Otherwise, responders may miss critical incidents.

## Design principles for effective alerting

Not every metric or event should generate an alert. Before converting a signal into an alert, ensure it answers these four questions:

* Is it actionable now? If not, keep it as a metric or dashboard.
* Does it require human intervention? If not, automate remediation.
* Does it affect users or revenue? If not, avoid waking someone.
* Can the on-call person fix it? If not, route it to the appropriate team.

<Frame>
  <img alt="A slide titled &#x22;Effective Alerting – Principles&#x22; listing the four questions every alert must answer: 01 Actionable now? 02 Requires human intervention? 03 Affects users/revenue? 04 Can on-call fix it? Each question is paired with guidance if the answer is no (e.g., it's a metric not an alert; automate; don't wake anyone; route properly)." />
</Frame>

> **lightbulb** Only alert on signals that require immediate human attention and which the recipient can reasonably act on. Use metrics, automation, or routing for everything else.

## Make alerts actionable: scope, context, and runbooks

Low-value alerts often trigger during normal operation and lack context. Provide:

* A clear service scope (which service or component)
* A user-facing signal (errors, latency, availability)
* Severity and owning team labels
* Links to runbooks and dashboards

Compare a low-context alert with a richer, actionable alert:

Low-context alert:

```yaml theme={null}
alert: HighCPU
expr: cpu_usage > 70
for: 1m
labels:
  severity: critical
annotations:
  summary: "High CPU detected"
```

Actionable alert (Prometheus):

```yaml theme={null}
alert: CheckoutServiceDegraded
expr: rate(http_requests_total{service="checkout",status=~"5.."}[5m]) / rate(http_requests_total{service="checkout"}[5m]) > 0.05
for: 3m
labels:
  severity: critical
  team: platform
annotations:
  summary: "Checkout error rate above 5%"
  description: "Checkout error rate over the last 5 minutes exceeds 5%. Revenue impact likely."
  runbook_url: "https://wiki.example.com/checkout-debugging"
  dashboard_url: "https://grafana.example.com/d/checkout-dashboard"
```

Why the second is better:

* Scopes to a specific service.
* Uses a user-facing metric (error rate).
* Provides severity, team ownership, and remediation resources so responders can act quickly.

## SLO-based alerting: focus on user experience

SLO-based alerting shifts focus from infrastructure thresholds (CPU, disk) to user experience and business impact. Alerts driven by SLOs and error budgets better reflect when users are affected and when engineering must intervene.

<Frame>
  <img alt="A presentation slide titled &#x22;SLO‑Based Alerting&#x22; that visually compares Traditional Alerting (focusing on technical thresholds) with a user‑focused SLO approach, using icons and a &#x22;VS&#x22; between them." />
</Frame>

Example SLO alert (checks P95 latency for search service, fires if > 200ms):

```yaml theme={null}
- alert: SearchLatencySLOViolation
  expr: |
    histogram_quantile(0.95,
      rate(http_request_duration_seconds_bucket{service="search"}[10m])
    ) > 0.2
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Search latency SLO violation"
    description: "P95 latency {{ $value }}s exceeds 0.2s SLO"
```

## Error-budget and burn-rate alerting

Error-budget alerting uses a burn rate: how quickly you are consuming your allowable errors versus the expected pace. Burn-rate alerts provide urgency levels tied to SLOs.

<Frame>
  <img alt="A presentation slide titled &#x22;Error Budget Alerting&#x22; with a centered panel labeled &#x22;Burn Rate.&#x22; It explains burn rate as how fast you're consuming your error budget compared to the &#x22;normal&#x22; rate." />
</Frame>

Burn-rate tiers and recommended responses:

| Burn-rate tier | Example multiplier | What it means                          | Recommended action                                        |
| -------------- | ------------------ | -------------------------------------- | --------------------------------------------------------- |
| High           | 10x+               | You'll exhaust monthly budget in hours | Immediate attention — page on-call and mitigate now       |
| Medium         | 2–5x               | Rapid consumption, but not instant     | Investigate and plan fixes; consider temporary mitigation |
| Low            | 1–2x               | Early warning                          | Monitor trends and schedule improvements                  |

<Frame>
  <img alt="A presentation slide titled &#x22;Error Budget Alerting&#x22; showing three tiers—High burn rate (10x+) needing immediate attention, Medium burn rate (2–5x) to plan a fix soon, and Low burn rate (1–2x) for early trend detection and monitoring. The slide includes brief descriptions of the problem speed and recommended actions for each tier." />
</Frame>

Concrete burn-rate calculation example (Python-style pseudocode):

```python theme={null}
