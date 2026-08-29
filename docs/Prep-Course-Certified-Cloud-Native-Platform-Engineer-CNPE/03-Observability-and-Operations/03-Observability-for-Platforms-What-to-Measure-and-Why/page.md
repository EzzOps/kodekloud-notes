# Instant vector: current memory per pod (instant query)
container_memory_usage_bytes{namespace="production"}
```

```promql theme={null}
# Range vector + rate: requests per second over a 5m window
rate(http_requests_total[5m])
```

```promql theme={null}
# Aggregation: total error rate (5xx) by service over 5m
sum by (service) (
  rate(http_requests_total{code=~"5.."}[5m])
)
```

<Callout icon="lightbulb">
  Remember: counters may reset when a process restarts. Functions like `rate()` and `increase()` are resilient to resets. Use gauges for instantaneous values and avoid `rate()` on non-monotonic series.
</Callout>

## Prometheus in Kubernetes — discovery and common targets

Common discovery methods in Kubernetes:

* Pod annotations: quick for simple setups. Example:

```yaml theme={null}
# Pod annotation example
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
```

* ServiceMonitor: CRD from the Prometheus Operator (recommended for scale). ServiceMonitors let you declaratively manage scrape targets and relabeling.
* Static configuration: use for external systems or legacy services that are not discovered via Kubernetes.

Typical metric sources:

* kube-state-metrics: exposes desired/actual state of Kubernetes objects — deployments, replicasets, pods. ([https://github.com/kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics))
* node-exporter: node-level hardware metrics — CPU, memory, disk, network. ([https://github.com/prometheus/node\_exporter](https://github.com/prometheus/node_exporter))
* cAdvisor: container-level CPU and memory metrics. ([https://github.com/google/cadvisor](https://github.com/google/cadvisor))
* Your app’s `/metrics` endpoint: business and application-specific metrics.

<Frame>
  <img alt="The image provides an overview of integrating Prometheus in Kubernetes, outlining methods such as pod annotations, ServiceMonitor, and static configuration, along with resources like kube-state-metrics, node-exporter, and cAdvisor. It briefly describes each component’s role in monitoring metrics within Kubernetes clusters." />
</Frame>

## Quick reference — common PromQL snippets

* Current memory per pod:

```promql theme={null}
container_memory_usage_bytes{namespace="production"}
```

* Requests per second (5m):

```promql theme={null}
rate(http_requests_total[5m])
```

* Aggregate 5xx error rate by service:

```promql theme={null}
sum by (service) (
  rate(http_requests_total{code=~"5.."}[5m])
)
```

* 95th percentile latency from histograms:

```promql theme={null}
histogram_quantile(0.95, sum by (le) (rate(request_duration_seconds_bucket[5m])))
```

## Summary — core takeaways

* Prometheus is pull-based: this enables central control and automatic health detection.
* There are three primary metric types (counter, gauge, histogram). Use the proper query patterns:
  * Counters → `rate()` / `increase()`
  * Gauges → instant values or non-monotonic functions
  * Histograms → operate on bucket counters and use `histogram_quantile()`
* Labels make metrics dimensional and enable filtering, grouping, and correlation. Enforce consistent labeling conventions.
* PromQL supports instant, range, and aggregation queries — these cover most dashboarding and alerting needs.

<Frame>
  <img alt="The image outlines four key takeaways about Prometheus: its pull-based design, metric types and query patterns, the importance of labels for metrics, and the use of PromQL as a query language." />
</Frame>

## Links and further reading

* Prometheus docs: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* PromQL basics: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* Prometheus Operator and ServiceMonitor: [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* kube-state-metrics: [https://github.com/kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
* node-exporter: [https://github.com/prometheus/node\_exporter](https://github.com/prometheus/node_exporter)
* Pushgateway best practices: [https://prometheus.io/docs/practices/pushing/](https://prometheus.io/docs/practices/pushing/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/dafd2315-36be-4318-b3e4-cc408da620c5" />
</CardGroup>


# Observability for Platforms What to Measure and Why

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Observability-for-Platforms-What-to-Measure-and-Why/page

Guide to platform observability covering metrics, logs, traces, golden signals, tooling, deployment and cost metrics, and operational practices for building and running a self service observability stack.

Welcome to the Observability and Operations section.

This domain separates platform engineers who build systems from those who keep them running. The central operational question is simple but critical: when something goes wrong on the platform — and it will — how quickly can you answer what happened, why it happened, and where it happened?

In this lesson we build a mental model that underpins the rest of the course: metrics with Prometheus, dashboards with Grafana, traces with OpenTelemetry and Jaeger, and incident response practices.

<Frame>
  <img alt="The image outlines five learning objectives related to monitoring and observability in cloud-native platforms, including understanding the limitations of traditional monitoring, distinguishing between monitoring and observability, and identifying key metrics." />
</Frame>

Why observability matters

Think of running a large commercial building with offices, a restaurant, and a gym. If tenants complain, a purely monitoring mindset forces you to walk every floor and manually inspect every panel to find the problem. Observability gives you correlated, centralized signals so you can diagnose from the outside — without physically visiting each system.

In a cloud-native example, a SaaS company running 120 microservices might see checkout latency jump from 200 ms to 8 s during a peak event. Without correlated metrics, traces, and deployment metadata, an on-call engineer can spend 45+ minutes hunting across namespaces and Slack channels. With a well-instrumented platform — centralized metrics, distributed traces tied to deployment metadata, and searchable logs — the root cause can be found in minutes.

Monitoring vs observability

* Monitoring: predefined checks, known failure modes, and binary answers — “is something broken according to the checks we wrote?”
* Observability: exploratory, correlated signals enabling ad-hoc questions — “why is this happening, where is the hotspot, and what change triggered it?”

<Frame>
  <img alt="The image compares traditional monitoring with observability, highlighting aspects like predefined checks, binary answers, and reactive approaches for monitoring versus more dynamic, exploratory, and proactive characteristics in observability." />
</Frame>

In short: monitoring tells you something is wrong; observability helps you answer why and where.

The three pillars of observability

Observability is commonly described with three complementary pillars. Each pillar answers a different operational question:

* Metrics — “What is happening?” Numeric time series: counters, gauges, histograms. Compact, efficient, ideal for dashboards and alerts.
* Logs — “What was the context?” Time-stamped event records with high cardinality and rich context for debugging.
* Traces — “What was the path?” Distributed traces show the sequence of service hops and timings for a request.

Collectively they let you go from a metrics alert to the trace that identifies the slow service and then to the log line with the exception.

<Frame>
  <img alt="The image outlines &#x22;The Three Pillars of Observability&#x22;: Metrics, Logs, and Traces, describing their characteristics and providing examples of tools associated with each." />
</Frame>

Pillars mapped to common tools

| Pillar  |     Question answered | Typical tools / examples                                                   |
| ------- | --------------------: | -------------------------------------------------------------------------- |
| Metrics |    What is happening? | Prometheus (scraping), Grafana (visualization)                             |
| Logs    | What was the context? | Fluentd / Fluent Bit (collection), Elasticsearch / Loki (storage & search) |
| Traces  |    What was the path? | OpenTelemetry (instrumentation/export), Jaeger / Tempo (visualization)     |

How these pillars map to a practical stack

A platform observability stack usually separates responsibilities into layers:

* Signal sources: instrumented apps, node exporters, service mesh sidecars, kube-state metrics.
* Collection layer: Prometheus for metrics scraping, OpenTelemetry Collector for traces and metrics, and Fluentd/Fluent Bit for logs.
* Visualization & alerting: Grafana for dashboards, Jaeger/Tempo for traces, and Alertmanager (or other systems) for notifications and incident workflows.

This diagram is a mental map of signal flow from sources through collection into storage, visualization, and alerting.

<Frame>
  <img alt="The image illustrates &#x22;The Platform Observability Stack,&#x22; detailing components like Signal Sources, Collection Layer, and Viz and Alerting, along with tools such as Grafana, Prometheus, and OpenTelemetry." />
</Frame>

What to measure — four practical categories

When choosing signals, group them into logical categories that support both incident response and long-term reliability improvements.

1. Golden signals
   * Latency: request durations (p50, p90, p99) and distributions by endpoint.
   * Traffic: request rates (RPS), throughput, or transactions per second.
   * Errors: error count or error-rate percentage, per endpoint/service.
   * Saturation: resource usage that limits capacity (CPU, memory, disk, network).
     These are the highest-value signals — if you measure only a few things, start here.

<Callout icon="lightbulb">
  The golden signals give immediate insight into user experience and capacity. Instrument critical endpoints and paths to capture latency, traffic, errors, and saturation with labels for service, endpoint, and region to keep cardinality manageable.
</Callout>

2. Platform health
   * Node metrics: CPU, memory, disk I/O, network throughput, and filesystem metrics.
   * Pod health: restart counts, CrashLoopBackOff events, and OOM kills.
   * Control plane metrics: API server latencies, etcd performance, scheduler queues.

3. Deployment and delivery metrics (DORA metrics)
   * Deployment release frequency.
   * Lead time for changes (commit to production).
   * Change failure rate (deployments requiring remediation).
   * Mean time to recovery (MTTR).

4. Cost and efficiency
   * Requested vs actual resource usage by namespace or workload.
   * Cost per service / namespace, and utilization efficiency.
     Tools such as OpenCost help map cloud spend to workloads and teams.

Key metrics and examples

| Category        | Example metrics                                                                                        | Why they matter                                           |
| --------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| Golden signals  | `http_request_duration_seconds` (histogram), `http_requests_total` (counter), `node_cpu_seconds_total` | Detect user-facing latency, load, and capacity limits     |
| Platform health | `kube_pod_container_status_restarts_total`, `node_filesystem_avail_bytes`                              | Early warning of infrastructure degradation               |
| DORA            | `deployments_total`, `lead_time_seconds`                                                               | Measure delivery performance and correlate with incidents |
| Cost            | `namespace_cpu_cost`, `pod_memory_actual_bytes`                                                        | Optimize spend and identify wasteful workloads            |

<Callout icon="warning">
  High-cardinality metrics and verbose log retention can dramatically increase storage and costs. Instrument thoughtfully (sample, aggregate, or use histograms), set sensible retention policies, and label with necessary dimensions only.
</Callout>

Operational responsibilities — who owns observability?

* Platform engineers should own the observability stack: provision it, operate it, and provide it as a self-service capability for application teams.
* Application teams should instrument their code with metrics, traces, and meaningful logs using OpenTelemetry and the platform’s recommended libraries and conventions.
* Define SLIs/SLOs and align alerting to actionable thresholds to reduce pager fatigue and false positives.

Quick checklist for a practical observability rollout

* Start with the golden signals for every user-facing service.
* Ensure traces are correlated with request IDs and deployment metadata.
* Centralize logs with searchable context linked from traces and metrics.
* Implement SLOs and configure alerts targeting the right on-call teams.
* Monitor cost and cardinality to keep the observability platform sustainable.

<Frame>
  <img alt="The image outlines key metrics to measure for system monitoring, including Golden Signals, Platform Health, Deployment Metrics, and Cost and Efficiency. Each section lists specific components such as latency, resource usage, and deployment frequency." />
</Frame>

Final thoughts

Observability is broader than monitoring: it empowers teams to investigate unforeseen problems by correlating metrics, logs, and traces. When the platform team owns a well-instrumented, self-service observability stack, development teams move faster and incidents are resolved more quickly and accurately.

Recommended references

* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* Fluentd: [https://www.fluentd.org/](https://www.fluentd.org/)
* Fluent Bit: [https://fluentbit.io/](https://fluentbit.io/)
* Loki: [https://grafana.com/oss/loki](https://grafana.com/oss/loki)
* SRE and Golden Signals: [https://sre.google/](https://sre.google/)
* DORA metrics: [https://devops-research.com/](https://devops-research.com/)
* OpenCost: [https://opencost.io/](https://opencost.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/cbe0340a-9f87-477d-8288-1353a3c3a688" />
</CardGroup>
