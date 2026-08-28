# Logging for Platforms Patterns That Scale

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Logging-for-Platforms-Patterns-That-Scale/page

Explains scalable Kubernetes logging with structured JSON, centralized pipeline stages, DaemonSet versus sidecar collection, log level strategies, and trace ID correlation for rapid root cause analysis.

In this lesson we'll cover logging, the third pillar of observability.\
Metrics tell you what happened, traces tell you where it happened, and logs explain why.

By the end you'll understand:

* why `kubectl logs` fails at scale,
* what structured logging looks like,
* how a log pipeline is built and operated,
* and how trace IDs tie logs to traces for rapid root-cause analysis.

<Frame>
  <img alt="The image shows a slide titled &#x22;Learning Objectives,&#x22; highlighting objective number 5: &#x22;Implement log-level strategies that balance signal vs noise.&#x22;" />
</Frame>

Real-world example

A company runs 350 pods across two clusters. A customer reports an error from six hours earlier. The pods that handled the request have been restarted twice; local logs were lost. `kubectl logs --previous` can't help because the pod was rescheduled to another node. Ninety minutes later, the team still doesn't know the root cause.

After implementing centralized logging, the same investigation took eight seconds. What took 90 minutes of searching became an instant query.

<Frame>
  <img alt="The image compares Kubernetes logging before and after implementing centralized logging with Fluentd and Elasticsearch, highlighting improvements in search efficiency and error tracking." />
</Frame>

What breaks at scale

* Pods are ephemeral: restarts, evictions, and reschedules remove local log files.
* No global search across pods or clusters.
* Difficult or impossible to correlate events across services.
* No retention guarantees for the specific logs you need.

What you actually need:

* persistent storage,
* centralized search and indexing,
* structured log format,
* and correlation IDs to link logs to traces.

<Frame>
  <img alt="The image outlines three needs for scalable Kubernetes logging: persistent storage, centralized search, and structured format." />
</Frame>

Structured logging is the foundation

A logging pipeline depends on structured logging — not free-form plaintext. Humans can read plain text, but machines cannot reliably extract fields such as severity, user ID, or duration without brittle regexes.

Example unstructured plaintext log:

```plaintext theme={null}
2024-03-15 14:32:01 ERROR PaymentSvc Failed to process payment for user 4821 - timeout after 5000ms
```

Same event as structured JSON (recommended):

```json theme={null}
{
  "ts": "2024-03-15T14:32:01Z",
  "level": "error",
  "service": "PaymentSvc",
  "msg": "Failed to process payment",
  "user_id": 4821,
  "duration_ms": 5000,
  "trace_id": "abc-123-def-456"
}
```

The `trace_id` field is the bridge between logs and traces. Click a `trace_id` in a log entry and jump to your tracing UI (for example, Jaeger) to see the full distributed trace.

<Frame>
  <img alt="The image outlines the benefits of using JSON for structured logging, highlighting its machine-readable, filterable, aggregatable, and correlatable properties." />
</Frame>

Why structured logging matters

* Machine-parsable: avoids brittle regex extraction.
* Filterable: run precise queries such as `level="error" AND user_id=4821`.
* Aggregatable: count and group errors per service.
* Correlatable: link logs to traces using trace IDs.

<Callout icon="lightbulb">
  Application teams should emit structured JSON to stdout. Platform teams are responsible for collection, enrichment, shipping, storage, and the query UI.
</Callout>

The log pipeline — five stages

A robust centralized logging setup typically implements these stages:

1. Collect\
   Run a collector as a DaemonSet on each cluster node to tail container logs from directories such as `/var/log/containers`. Popular collectors:
   * Fluentd — feature-rich aggregator ([fluentd.org](https://www.fluentd.org/))
   * Fluent Bit — lightweight ([fluentbit.io](https://fluentbit.io/))
   * Promtail — for pushing to Loki ([Grafana Loki](https://grafana.com/oss/loki/promtail))

2. Enrich\
   The collector attaches Kubernetes metadata (namespace, pod name, container, labels). This metadata powers label-based queries and dashboards.

3. Ship\
   Forward enriched logs over HTTP/gRPC (or supported protocols) to a central ingestion endpoint or scaling message bus.

4. Store & Index\
   Choose the storage/indexing trade-off:
   * Elasticsearch: full-text indexing, powerful search, higher cost ([elastic.co](https://www.elastic.co/elasticsearch))
   * Loki: indexes labels only and stores log content efficiently, integrates with Prometheus/Grafana ([grafana.com/oss/loki](https://grafana.com/oss/loki))

5. Query\
   Provide a UI for searching, filtering, and visualizing logs:
   * Kibana for Elasticsearch
   * Grafana for Loki (and multi-source dashboards)

<Frame>
  <img alt="The image depicts &#x22;The Log Aggregation Pipeline&#x22; with five stages: Collect, Enrich, Ship, and two unspecified stages. A note mentions forwarding enriched logs to a central store over HTTP or gRPC." />
</Frame>

<Frame>
  <img alt="The image illustrates &#x22;The Log Aggregation Pipeline&#x22; with five stages: Collect, Enrich, Ship, Store & Index, and Query. The Query stage includes options for using Kibana or Grafana for log data visualization and alerts." />
</Frame>

Kubernetes collection patterns

Two common collection patterns exist in Kubernetes:

* DaemonSet pattern (default)\
  One collector per node that mounts the host log directory and tails all containers. Pros: low overhead, simple, works for roughly 90% of use cases. Start here.

* Sidecar pattern (per-pod)\
  A per-pod sidecar collects stdout or file logs from the application. Useful for apps with unusual formats, multi-line logs, or when you need per-app customization. Cons: higher resource usage and more maintenance. Use only for exceptions.

<Frame>
  <img alt="The image presents a comparison between &#x22;DaemonSet Pattern&#x22; and &#x22;Sidecar Pattern&#x22; for Kubernetes log collection, outlining their methods, pros, cons, and usage recommendations. It suggests starting with DaemonSet for most use cases and adding sidecars only for apps needing custom log handling." />
</Frame>

Log levels — balance signal vs noise

Choosing appropriate log levels prevents you from drowning in logs or missing critical signals.

| Level | Meaning                            | Example                           | Action                           |
| ----- | ---------------------------------- | --------------------------------- | -------------------------------- |
| ERROR | A failure requiring attention      | Service failed to process payment | Alert and investigate            |
| WARN  | Something unexpected but recovered | Retry occurred after timeout      | Track trends on dashboards       |
| INFO  | Normal operational events          | User login succeeded              | Default level in production      |
| DEBUG | Detailed diagnostic output         | SQL query timings, internal state | Enable selectively for debugging |

<Frame>
  <img alt="The image is a table outlining log levels, their meanings, examples, and actions, comparing signal and noise in logging contexts. It includes levels like ERROR, WARN, INFO, and DEBUG." />
</Frame>

<Callout icon="warning">
  Do not run DEBUG logging globally in production — it generates high volume and may expose sensitive diagnostic data. Enable DEBUG only for targeted troubleshooting.
</Callout>

Recommended production strategy

* Default to `INFO`.
* Alert on `ERROR`.
* Use dashboards to monitor `WARN` trends.
* Enable `DEBUG` only for specific pods or short-lived investigations.

Trace integration — connect the dots

When your tracing SDK (for example, OpenTelemetry) is active, it can inject the current trace ID into the logging context so every log line carries the trace identifier. This enables fast, end-to-end troubleshooting:

1. Observe an error spike in metrics (Grafana/Prometheus).
2. Filter logs for `level="error"` in the time window and find entries with a `trace_id`.
3. Click the `trace_id` to open your tracer (e.g., Jaeger).
4. The trace waterfall highlights the failing span — you now see where and why.

This single ID ties metrics, traces, and logs into a unified story.

Key takeaways

* `kubectl logs` is useful for quick debugging but does not scale for post-mortem analysis across many ephemeral pods — use a logging pipeline.
* Structured JSON logs are essential for reliable enrichment, indexing, and querying.
* Start with a DaemonSet collector; use sidecars only for apps that need special handling.
* Emit trace IDs with logs and link to tracing tools (Jaeger, Zipkin, or OpenTelemetry backends) for fast root-cause analysis.

<Frame>
  <img alt="The image presents four key takeaways about logging in Kubernetes, including using a pipeline for logs, structured JSON logging, DaemonSet-based collection, and using trace IDs to connect metrics and logs." />
</Frame>

Metrics, traces, and logs become a single, navigable observability story when you centralize logs, adopt structured output, and correlate with traces.

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* Fluentd: [https://www.fluentd.org/](https://www.fluentd.org/)
* Fluent Bit: [https://fluentbit.io/](https://fluentbit.io/)
* Grafana Loki: [https://grafana.com/oss/loki/](https://grafana.com/oss/loki/)
* Elasticsearch: [https://www.elastic.co/elasticsearch](https://www.elastic.co/elasticsearch)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/96beb568-bbf6-4b91-9be1-543fdff42992" />
</CardGroup>
