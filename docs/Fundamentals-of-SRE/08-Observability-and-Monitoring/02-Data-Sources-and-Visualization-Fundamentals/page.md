# SLO: 99.9% availability → 0.1% error budget per month
monthly_error_budget = 0.001     # 0.1% expressed as decimal
daily_error_budget = monthly_error_budget / 30    # ~0.00003333 per day

# Example: Current error rate = 0.02 (2% failure rate)
current_daily_error_rate = 0.02

# Burn rate multiplier = actual error rate / daily error budget
burn_rate_multiplier = current_daily_error_rate / daily_error_budget

# At this rate, monthly error budget exhausted in:
days_to_exhaust = 30 / burn_rate_multiplier  # ≈ 0.05 days ≈ 1.2 hours
```

Prometheus example for a payments SLO (critical alert if burn is > 14.4x monthly-normal fraction):

```yaml theme={null}
alert: PaymentSLOBurnRateFast
expr: |
  (
    rate(http_requests_total{service="payment",status=~"5.."}[1h]) /
    rate(http_requests_total{service="payment"}[1h])
  ) > (14.4 * 0.001)  # threshold = 14.4x * monthly_error_budget (0.001)
for: 2m
labels:
  severity: critical
annotations:
  summary: "Payment SLO burning too fast"
  description: "Current error rate is {{ $value }} (fraction); threshold corresponds to 14.4x the monthly error budget (0.001)."
```

Burn-rate alerts are effective because they quantify urgency and map technical metrics to reliability goals.

## Alert routing: get alerts to the right people

Good alerting includes routing so the correct team receives the right severity at the right time. Use routing tools such as Alertmanager or PagerDuty to:

* Group similar alerts to reduce notification volume
* Route by service, severity, and time of day
* Send low-severity signals to chat channels for visibility (no paging)

Basic Alertmanager routing example (grouping, receivers, and matches):

```yaml theme={null}
route:
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: default

routes:
  - match:
      service: payment
      severity: critical
    receiver: payment-team-urgent

  - match:
      service: catalog
      severity: warning
    receiver: platform-team-business-hours

  - match:
      severity: info
    receiver: slack-only
```

Time-based routing example: business-hours vs after-hours:

```yaml theme={null}
routes:
  - match:
      service: user-service
    active_time_intervals: [business_hours]
    receiver: user-team-business-hours

  - match:
      service: user-service
    active_time_intervals: [after_hours]
    receiver: user-team-on-call

time_intervals:
  - name: business_hours
    time_intervals:
      - times:
          - start_time: '09:00'
            end_time: '17:00'
        weekdays: ['monday:friday']

  - name: after_hours
    time_intervals:
      - times:
          - start_time: '17:00'
            end_time: '09:00'
        weekdays: ['monday:friday']
      - weekdays: ['saturday', 'sunday']
```

During business hours, alerts route to a triage channel; after hours they go to the on-call rotation.

## Where alerts live in the KodeKloud RecordStore repo

In the KodeKloud RecordStore example, Alertmanager configuration controls routing/receivers and AlertRules.yaml defines the alerts. Here’s a compact Alertmanager snippet you might find in the repository:

```yaml theme={null}
route:
  receiver: default
  routes:
    - match:
        severity: 'critical'
      receiver: 'critical-alerts'
      group_wait: 10s
      repeat_interval: 30m
    - match:
        severity: 'warning'
      receiver: 'default'

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://host.docker.internal:5001/webhook'
        send_resolved: true

  - name: 'critical-alerts'
    webhook_configs:
      - url: 'http://host.docker.internal:5001/webhook/critical'
        send_resolved: true

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

Example groups and rules from AlertRules.yaml (cause-based alerts and SLO-based alerts):

Cause-based alerts:

```yaml theme={null}
groups:
- name: Cause Alerts
  rules:
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{status=~"[45].*"}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      description: "Error rate exceeds 5% for the last 5 minutes."

  - alert: LongRequestDuration
    expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Long request duration detected"
      description: "95th percentile request duration is above 1 second for the last 5 minutes."

  - alert: HighUserLatency
    expr: probe_duration_seconds{job="blackbox"} > 2
    for: 5m
    labels:
      severity: warning
      monitoring_type: black-box
    annotations:
      summary: "High user-observed latency"
      description: "User probe latency has exceeded 2 seconds."
```

SLO-based alerts for Checkout service:

```yaml theme={null}
groups:
  - name: KodeKloud_Records_Checkout_SLOs
    rules:
      - alert: CheckoutErrorBudgetBurnFast
        expr: checkout:request_failures:ratio_5m > 0.1
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Checkout API error budget burning too fast"
          description: "Checkout is failing at {{ $value }} (ratio over 10%)."
          dashboard: "https://grafana.kodekloud-records.com/d/checkout"
          playbook: "https://wiki.kodekloud-records.com/playbooks/checkout"
          impact: "Customers are unable to complete purchases"

      - alert: CheckoutErrorBudgetBurnMedium
        expr: checkout:request_failures:ratio_5m > 0.02
        for: 30m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "Checkout API error budget burning at medium rate"
          description: "Checkout is failing at {{ $value }} (ratio over 2%)."
          dashboard: "https://grafana.kodekloud-records.com/d/checkout"
          playbook: "https://wiki.kodekloud-records.com/playbooks/checkout"

      - alert: CheckoutLatencyTooHigh
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service='checkout'}[10m])) > 0.5
        for: 5m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "Checkout API p95 latency exceeding SLO"
          description: "95th percentile checkout latency is {{ $value }}s, above target."
          dashboard: "https://grafana.kodekloud-records.com/d/checkout-performance"
          playbook: "https://wiki.kodekloud-records.com/playbooks/checkout-latency"

      - alert: CheckoutErrorBudgetBurnSlow
        expr: checkout:request_failures:ratio_5m > 0.005
        for: 3h
        labels:
          severity: info
          team: platform
        annotations:
          summary: "Checkout API error budget burning slowly"
          description: "Checkout has a {{ $value }} error ratio; monitor and plan fixes."
          dashboard: "https://grafana.kodekloud-records.com/d/checkout"
```

Review these rules and mappings to understand how alerts map to runbooks, dashboards, and routing.

## Best practices checklist

* Alert on user-facing signals (errors, latency, availability), not raw capacity metrics, unless they directly affect users.
* Use SLOs and error budgets to prioritize and quantify urgency.
* Provide context: service, severity, team, runbook, and dashboard URLs.
* Group and route alerts to the correct receiver; use time-based routing to avoid waking unnecessary people.
* Automate remediation for common, low-risk failures.
* Measure alert volume and triage time; iterate to reduce noise.

## Links and references

* [Prometheus Alerting](https://prometheus.io/docs/alerting/latest/)
* [Alertmanager documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [PagerDuty](https://www.pagerduty.com/)
* [Kubernetes Monitoring and SRE resources](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)

We’ve reached the end of the alert design and implementation lesson. Next, we’ll move into performance monitoring to explore how system performance ties to user experience and SLOs.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/92f39ae4-b287-4850-93aa-3f0119393754/lesson/0aa144f9-018b-4017-8dae-c7ad9cf3aa98)


# Data Sources and Visualization Fundamentals

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Observability-and-Monitoring/Data-Sources-and-Visualization-Fundamentals/page

A guide to observability pipelines and Grafana dashboards covering Prometheus Loki Jaeger data sources PromQL provisioning dashboard design and SLO driven visualizations for troubleshooting

Welcome back. This lesson connects the telemetry you collect to the dashboards you use to make decisions. Observability isn't just about collecting metrics, logs, and traces — it's about turning that raw telemetry into actionable insights. We'll cover the common data sources (how Prometheus, Loki, and Jaeger feed your stack) and the visualization fundamentals for building effective Grafana dashboards.

Think of observability as a pipeline:
application code → metrics collection → time-series storage → Grafana dashboards.

<Frame>
  <img alt="A slide titled &#x22;The Observability Data Flow&#x22; showing a left-to-right pipeline of boxes: Application Code → Metrics Collection (Prometheus) → Data Source (TSDB) → Dashboard (Grafana). It visually depicts how application metrics move from code through Prometheus into a time-series database and then into a Grafana dashboard." />
</Frame>

Each stage in this pipeline has a specific role:

* Application code: export metrics and add trace/log context.
* Prometheus: scrapes metrics and stores samples in its TSDB.
* Grafana: queries Prometheus, Loki, and Jaeger to render dashboards and correlate data.

Example metric instrumentation in a Python app (metrics.py):

```python theme={null}
