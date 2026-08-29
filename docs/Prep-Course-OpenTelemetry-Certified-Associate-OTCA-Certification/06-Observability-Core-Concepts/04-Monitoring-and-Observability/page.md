# Monitoring and Observability

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Observability-Core-Concepts/Monitoring-and-Observability/page

Differences and complementary roles of monitoring and observability for detecting system symptoms and diagnosing root causes using metrics, logs, traces, and profiling in distributed systems

Now that we've covered what observability means, it's important to treat monitoring and observability as related but distinct capabilities. This article clarifies their differences, how they complement each other, and when to rely on one versus both for reliable systems.

Monitoring answers the "what" — it tells you what is happening right now (symptoms). Observability helps answer the "why" by combining multiple telemetry signals (metrics, logs, traces, profiles, and baggage) to expose root causes.

***

## Monitoring (the "what")

Monitoring begins with collecting and analyzing data to measure progress toward objectives and to support operational decisions.

* Focus: detect and alert on known symptoms using predefined metrics and thresholds.
* Common metrics: CPU usage, memory usage, disk latency, response times, error rates.
* Typical workflow: instrument, record metrics, set alerts, respond with runbooks.
* Best fit: predictable failure modes where symptoms and remediation steps are already known.
* Role of logs: logs complement metrics but in many monitoring setups they remain siloed and less flexible for ad-hoc investigation.

<Frame>
  <img alt="The image is a slide titled &#x22;When Is Monitoring Enough?&#x22; with a message suggesting monitoring is sufficient for predictable system failures. It includes a database performance dashboard showing graphs for CPU utilization, memory usage, and cache hit ratio." />
</Frame>

Skilled operators rely on thresholds and pattern recognition to spot issues early. For predictable incidents — for example, a spike in DB latency caused by a scheduled maintenance job — monitoring alone can be sufficient to detect and act.

***

## Observability (the "why")

Observability enables you to infer internal system state by correlating telemetry signals so teams can investigate and reason about unexpected behavior.

* Focus: provide context and flexible instrumentation to support ad-hoc queries and root-cause analysis.
* Telemetry signals: metrics, logs, distributed traces, profiling data, and contextual baggage.
* Enables asking new questions during incidents without predefining every possible failure mode.
* Best fit: complex, distributed systems where failures are often emergent and not predictable.
* Outcome: faster, more accurate diagnosis of unknown issues and improved system understanding.

<Frame>
  <img alt="The image illustrates the concept of observability in complex systems, highlighting three key steps: detect, investigate, and resolve." />
</Frame>

***

## Monitoring vs Observability — Side-by-side

* Monitoring: tracks what is happening (symptoms). Uses predefined metrics and alerts to notify you of known issues.
* Observability: explains why something is happening (root cause). Provides contextual telemetry required to investigate unknown issues and to form new hypotheses.

Example: if database latency spikes:

* Monitoring alerts you that latency is high (the symptom).
* Observability lets you drill into traces, logs, and profiles to find that a deployed schema change or an inefficient query introduced the slowdown (the cause).

| Aspect           | Monitoring                            | Observability                                         |
| ---------------- | ------------------------------------- | ----------------------------------------------------- |
| Primary question | What is happening?                    | Why is it happening?                                  |
| Typical signals  | Metrics, thresholds, alerts           | Metrics, logs, traces, profiles, baggage              |
| Best for         | Known failure modes, SLA/SLI tracking | Unknown/complex failures, root-cause analysis         |
| Workflow         | Alert → Runbook → Remediate           | Detect → Explore telemetry → Hypothesize → Fix        |
| Example          | Alert on high CPU                     | Trace the request path to find slow service/component |

<Frame>
  <img alt="The image compares monitoring and observability by highlighting differences in focus, examples, insight levels, and approaches. Monitoring tracks what is happening, while observability explains why it is happening." />
</Frame>

> **lightbulb** Monitoring and observability are complementary: monitoring gives rapid detection via metrics and alerts, while observability provides the richer telemetry and context needed to investigate and diagnose unknown or complex failures.

***

## Practical guidance

* Combine both: use monitoring for SLAs, SLOs, and alerting; use observability to reduce mean time to resolution (MTTR) when incidents are novel or complex.
* Instrument intentionally: capture high-cardinality context only where it aids debugging (e.g., request IDs, user IDs, endpoint names).
* Correlate signals: ensure traces, logs, and metrics share common identifiers to enable seamless investigation.
* Balance cost and retention: observability data can be voluminous — set retention and sampling policies that match your business needs.

***

## Conclusion

* Monitoring provides visibility into system health and known symptoms.
* Observability gives teams the flexible tooling and contextual telemetry to investigate and diagnose root causes.
* Together, monitoring and observability deliver the visibility and investigative power required for reliable, performant systems — especially in modern distributed architectures.

<Frame>
  <img alt="The image explains the differences and complementary roles of monitoring and observability, highlighting how monitoring shows what is happening and observability explains why it is happening. Together, they ensure system visibility and performance reliability." />
</Frame>

***

## Links and References

* [OpenTelemetry](https://opentelemetry.io/) — vendor-neutral collection of observability tools.
* [Prometheus — Monitoring system](https://prometheus.io/) — popular metrics-based monitoring.
* [Distributed Tracing — Concepts](https://opentracing.io/guides/what-is-tracing/) — overview of tracing for distributed systems.
* [Site Reliability Engineering (SRE) concepts](https://landing.google.com/sre/) — for SLAs, SLOs, and error budgets.

That's it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/79b34fea-6f94-4854-a31e-9ac0fbc10eca/lesson/bde139d7-bd99-4517-8e29-472c9495dca2)
