# SLOSLASLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Observability-Fundamentals/SLOSLASLI/page

Explains SLIs, SLOs, and SLAs, how to measure and set targets, and use error budgets to balance feature work with service reliability and contracts

When designing reliable systems, teams must set clear, measurable targets to balance feature development with operational work. These targets let organizations and customers understand what level of reliability to expect—for example, “97% uptime over a rolling 30-day window.” This article explains the three core concepts used to measure and guarantee reliability: SLIs, SLOs, and SLAs.

<Callout icon="lightbulb">
  Use these primitives to align engineering priorities with customer expectations. Clear SLIs make monitoring meaningful, SLOs define acceptable behavior, and SLAs document contractual obligations.
</Callout>

## Key concepts at a glance

* Service Level Indicator (SLI): a measurable metric that reflects an aspect of user experience.
* Service Level Objective (SLO): an explicit target (value or range) for an SLI over a time window.
* Service Level Agreement (SLA): a formal contract that often guarantees an SLO and specifies remedies for violations.

## Service Level Indicator (SLI)

An SLI is a quantitative metric that measures a specific characteristic of service behavior from the user’s perspective. Good SLIs are user-centric and directly correlate with user experience—what users actually see and feel.

Common SLIs:

* Request latency (response time)
* Error rate (failed requests)
* Throughput or request rate
* Saturation (resource utilization impacting request handling)
* Availability (uptime)

Best practices:

* Prefer SLIs tied to customer experience (latency, errors, availability).
* Avoid infrastructure-only metrics (e.g., CPU, memory) as SLIs unless they directly map to user impact.
* Define measurement windows and aggregation methods (percentiles, rolling windows).

<Frame>
  <img alt="The image explains Service Level Indicator (SLI) as a quantitative measure of service level and lists common SLIs such as request latency, error rate, saturation, throughput, and availability." />
</Frame>

## Service Level Objective (SLO)

An SLO is the target for one or more SLIs. It states what level of service is acceptable over a defined time window (commonly a rolling window, though calendar windows are also used).

Examples:

* Latency SLO: 99% of requests must have latency \< 100 ms over a 30-day rolling window.
* Availability SLO: the service should be available 99.9% of the time over a 30-day rolling window.

SLO design guidance:

* Make SLOs customer-centric and realistic—aim to balance reliability with business cost.
* Avoid aspirational 100% SLOs; they are expensive and fragile.
* Define alerting thresholds using the SLO (e.g., burn rate alerts when error budget is being consumed too quickly).
* Track SLOs continuously and use them to guide prioritization (investigate reliability issues when the error budget is depleted).

<Callout icon="warning">
  Setting an SLO to 100% availability is usually impractical. Instead, use an achievable target and an error budget to balance feature work and reliability investments.
</Callout>

<Frame>
  <img alt="The image explains Service Level Objectives (SLOs) with examples of latency and availability metrics, emphasizing their link to customer experience." />
</Frame>

## Service Level Agreement (SLA)

An SLA is a formal (often legal) contract between a provider and a customer that guarantees a specific SLO. SLAs define remedies that apply when the guaranteed SLO is not met—commonly service credits, termination rights, or other corrective actions.

SLA best practices:

* Be explicit about measurement methodology, time windows, and sampling.
* Define clear remedies and how customers claim them.
* Monitor SLA-related SLOs independently to produce audit-ready reports.
* Use SLAs sparingly for critical services where contractual guarantees are necessary.

<Frame>
  <img alt="The image describes a Service Level Agreement (SLA) as a contract between a vendor and a user guaranteeing a certain Service Level Objective (SLO). It mentions that not meeting an SLO can have financial and other consequences." />
</Frame>

## Comparison: SLI vs SLO vs SLA

| Concept | Purpose                                       | Example                                                   |
| ------- | --------------------------------------------- | --------------------------------------------------------- |
| SLI     | Measurable metric indicating service behavior | `request latency (p99) = 120ms`                           |
| SLO     | Target for an SLI over a time window          | `99% of requests < 100ms over 30 days`                    |
| SLA     | Contractual guarantee of an SLO with remedies | `99.9% uptime over 30 days → service credits if violated` |

## Practical tips for implementation

* Instrument user-facing metrics early: latency, error counts, and availability.
* Define aggregation rules (percentiles, sliding windows) and storage retention.
* Create alerts around SLO burn rate, not just instantaneous metric thresholds.
* Use error budgets to drive release cadence and reliability engineering work.
* Include measurement methodology in runbooks to ensure reproducible reports for customers and auditors.

## Summary

* Choose SLIs that reflect user experience (latency, errors, availability).
* Define SLOs that balance customer satisfaction with operational cost.
* Use SLAs to document legally binding guarantees and remedies when required.
* Monitor continuously and use error budgets to prioritize reliability work.

## Links and references

* [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/)
* [Prometheus: Monitoring system and time series database](https://prometheus.io/)
* [SRE and SLIs/SLOs best practices](https://landing.google.com/sre/book.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e2f3102c-1761-4800-9e21-1f2f4b36f050/lesson/20583163-f65a-4d19-bebb-cd01280711f1" />
</CardGroup>
