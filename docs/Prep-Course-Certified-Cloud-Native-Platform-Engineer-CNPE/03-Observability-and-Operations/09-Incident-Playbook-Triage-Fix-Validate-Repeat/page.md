# Service identification
OTEL_SERVICE_NAME=order-service

# Exporter endpoint (Jaeger collector or OTLP receiver)
OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger-collector:4317

# Protocol for OTLP (grpc or http/protobuf)
OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# Traces exporter (common values: otlp, jaeger, none)
OTEL_TRACES_EXPORTER=otlp
```

Note: gRPC OTLP often uses port `4317`; HTTP/protobuf OTLP often uses port `4318`. Ensure the protocol and endpoint match your collector.

<Callout icon="lightbulb">
  OpenTelemetry SDKs and auto-instrumentation inject and extract trace context automatically. In most cases you only need to set environment variables and enable auto-instrumentation or initialize the SDK in your app.
</Callout>

Jaeger — collect and visualize traces

Jaeger collects, stores, and visualizes traces. Typical architecture:

* OTEL SDK in your application exports traces to the Jaeger collector (often via OTLP).
* The collector writes traces to a storage backend (Elasticsearch, Cassandra, etc.).
* The query service reads the stored traces and powers the Jaeger UI.

<Frame>
  <img alt="The image is a diagram of Jaeger's trace collection and visualization architecture, detailing components like OTEL SDK, Jaeger Collector, Storage Backend, and Jaeger Query/UI. There's also a cartoon character in a traditional hat at the bottom left." />
</Frame>

Using the Jaeger UI

* Search traces by service name, operation, minimum duration, or tags.
* The waterfall/timeline view shows spans as horizontal bars whose widths represent duration. The widest bar is often the bottleneck.
* Click a span to view tags, logs/events, and process information.
* The service dependency graph is built from real trace data and shows call relationships between services.

<Frame>
  <img alt="The image is an infographic about Jaeger, explaining trace collection and visualization with five key features: search traces, trace timeline, span details, service dependency, and compare traces. Each feature is briefly described with visual icons." />
</Frame>

Context propagation: an example flow

1. Service A receives an incoming request and creates the root span (and a trace ID).
2. When Service A calls Service B, it injects a trace context header into the outgoing HTTP request.
3. Service B extracts the header, creates a child span (same trace ID, new span ID), and continues the chain when calling Service C.
4. All services share the single trace ID, allowing Jaeger to reconstruct the complete end-to-end journey.

<Frame>
  <img alt="The image illustrates &#x22;Context Propagation: How Traces Flow,&#x22; showing a call chain from Service A to Service B and then to Service C, with mention of trace context and operations like extracting traceparent and creating child spans." />
</Frame>

W3C trace context: the `traceparent` header

The W3C `traceparent` header is a standard way to carry trace context across process boundaries. It has four hyphen-separated fields:

* Version (currently `00`)
* Trace ID (32 hex characters) — identifies the entire trace
* Span ID (16 hex characters) — identifies the specific span
* Trace flags (e.g., `01` indicates the trace is sampled)

Example header:

```http theme={null}
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

In practice you rarely need to parse or create this header manually — OpenTelemetry injects and extracts it automatically.

Reference: W3C Trace Context — [https://www.w3.org/TR/trace-context/](https://www.w3.org/TR/trace-context/)

<Frame>
  <img alt="The image outlines key takeaways about tracing and OpenTelemetry, including the end-to-end path visibility of requests, the connection of spans through trace IDs, and standardizing instrumentation with configurations like OTEL_SERVICE_NAME." />
</Frame>

Quick checklist to get tracing working

| Step            | Action                                                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Instrumentation | Enable OpenTelemetry SDK or auto-instrumentation for your runtime (Java, Node, Python, Go, etc.). See [https://opentelemetry.io/](https://opentelemetry.io/) |
| Configure       | Set `OTEL_SERVICE_NAME` and OTLP exporter variables (example above).                                                                                         |
| Collector       | Deploy or point to a collector (Jaeger collector or OTLP receiver).                                                                                          |
| Storage & UI    | Configure Jaeger (or another backend) for storage and enable the UI for trace analysis.                                                                      |
| Verify          | Generate traffic and search traces in Jaeger; inspect the waterfall view to find slow spans.                                                                 |

Final summary

Tracing gives you end-to-end visibility that metrics and logs cannot provide alone. Traces are built from spans linked by a shared trace ID and joined together via context propagation (for example, the W3C `traceparent` header). Use OpenTelemetry for standardized instrumentation and OTLP export, and use Jaeger (or another backend) to collect, store, and analyze traces.

Useful references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* W3C Trace Context: [https://www.w3.org/TR/trace-context/](https://www.w3.org/TR/trace-context/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/b2773c70-7a8a-419b-9174-eb64ea3190c9" />
</CardGroup>


# Incident Playbook Triage Fix Validate Repeat

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Incident-Playbook-Triage-Fix-Validate-Repeat/page

A five-phase incident response playbook guiding teams from alert to validation using observability tools and safe reversible fixes to reduce mean time to recovery

This capstone ties together the observability and incident-response concepts covered earlier into a single, repeatable flow. Use this five-phase playbook to go from “something’s broken” to “it's fixed and confirmed” and to map each phase to the right tools and actions.

A logistics company had all the right tools — Prometheus, Grafana, Jaeger, Loki, and Alertmanager — but no playbook. At 2:00 a.m. their shipping API went down. The on-call engineer opened Grafana, saw red everywhere, panicked, and started restarting pods at random. Forty-five minutes later they discovered the root cause: an HPA had scaled the API to zero because a custom metric was broken.

After implementing a simple playbook, the next similar incident took four minutes instead of forty-five. The tools were the same; the outcome changed because they had a process.

Use this playbook for every incident, every time.

* Alert: Something triggered (Alertmanager, PagerDuty, Slack, or a custom report). It tells you which metric crossed a threshold and when.

<Frame>
  <img alt="The image outlines a &#x22;Five-Phase Incident Playbook&#x22; consisting of steps: Alert, Assess, Investigate, Fix, and Validate. A description under &#x22;Alert&#x22; mentions triggers like PagerDuty and Slack, detailing what and when a metric threshold was crossed." />
</Frame>

* Assess: Before you touch anything, spend a short, focused time (aim \~60 seconds) to understand the scope: how bad it is, who is affected, and whether it's partial or total.

<Frame>
  <img alt="The image depicts a five-phase incident playbook with steps: Alert, Assess, Investigate, Fix, and Validate, highlighting &#x22;Assess&#x22; with a note on evaluating scope, impact, and urgency." />
</Frame>

<Callout icon="lightbulb">
  Spend a minute to assess before you act. Skipping assess is the most common cause of wasted time and harmful changes.
</Callout>

* Investigate: Dig into the root cause in a focused, methodical order: metrics first, then traces, then logs. Follow a triage workflow to narrow scope gradually.

<Frame>
  <img alt="The image illustrates &#x22;The Five-Phase Incident Playbook,&#x22; detailing phases: Alert, Assess, Investigate, Fix, and Validate. There is additional text guiding the investigation process with steps like searching and correlating." />
</Frame>

* Fix: Apply the minimum-change necessary to restore service: rollback, scale up, adjust configuration, or restart. Prefer a reversible, conservative change that buys time to investigate further.

<Frame>
  <img alt="The image presents a &#x22;Five-Phase Incident Playbook&#x22; consisting of five steps: Alert, Assess, Investigate, Fix, and Validate, with detailed instructions under the &#x22;Fix&#x22; phase." />
</Frame>

* Validate: Don't close the incident until you confirm the fix worked. Watch dashboards and verify stability for a few minutes.

Tools map naturally to the phases:

* Alertmanager, PagerDuty, Slack — alerts and notification (Alert, Validate)
* Grafana — dashboards and runbooks (Assess, Validate)
* Prometheus — metrics and PromQL (Investigate)
* Jaeger — distributed traces (Investigate)
* Loki / kubectl logs — logs and pod-level details (Investigate)
* kubectl, GitOps, Helm — apply safe, reversible fixes (Fix)

Now let’s dig into each phase, starting with Assess — the step most engineers skip or rush.

Assess: four quick questions

* What’s broken? Read the alert and identify the affected service, endpoint, or pod.
* How bad is it? Is the outage partial (a single endpoint or region) or total?
* Who’s affected? One customer, a region, or everyone?
* What changed recently? A deployment or config change within the alert window is a prime suspect.

Investigation: use the observability funnel (metrics → traces → logs)

* Metrics first: Inspect the alert’s PromQL expression and open Grafana. Confirm the alert timestamps, pattern (sudden vs gradual), and compare to baseline (same time yesterday, same weekday).
* Traces next: Search Jaeger for slow or error traces. Use minimal-duration filters, inspect the waterfall, and find the longest-duration span or failing service.
* Logs last: Query logs by service and timestamp, or by trace ID to pinpoint the exact error message.

Each pillar narrows the search: metrics detect and scope, traces locate the problematic service or interaction, and logs explain the root cause.

<Frame>
  <img alt="The image outlines &#x22;Phase 3: Investigate With ALL Three Pillars&#x22; in observability, featuring metrics, traces, and logs using tools like Prometheus, Grafana, Jaeger, Loki, and Kubectl logs." />
</Frame>

Measure platform performance over time with DORA metrics. These give you objective targets to reduce MTTR and improve reliability.

| DORA Metric                  | What it measures                          | Example target |
| ---------------------------- | ----------------------------------------- | -------------- |
| Deployment Frequency         | How often you ship to production          | Daily or more  |
| Lead Time for Changes        | Time from commit to production            | Under 1 hour   |
| Change Failure Rate          | % of deployments causing failures         | Under 5%       |
| Mean Time to Recovery (MTTR) | Time to restore service after an incident | Under 1 hour   |

<Frame>
  <img alt="The image lists key platform efficiency metrics for measuring platform health, featuring four DORA metrics: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and MTTR. Each metric includes a brief explanation and a target goal." />
</Frame>

Phase 4 — Fix: four safe strategies

* Rollback
  * When to use: a recent deployment caused the incident and assessment/investigation confirm it.
  * Why: fastest, lowest-risk path to restore service.
  * Example:

```bash theme={null}
kubectl rollout undo deployment app
```

* Scale up
  * When to use: load exceeds capacity (CPU/memory/requests throttled) and you need breathing room.
  * Why: buys time to investigate whether load is legitimate or anomalous.
  * Example:

```bash theme={null}
kubectl scale deployment app --replicas=5
```

* Config fixes
  * When to use: misconfigured DB URL, expired secret, or bad environment variable.
  * How: update ConfigMap/Secret and trigger a restart or rolling update.
  * Example:

```bash theme={null}
kubectl rollout restart deployment app
```

* Resource adjustments (scheduling failures)
  * When to use: pods Pending because nodes lack allocatable resources.
  * How: free resources, tune requests/limits, or adjust quotas for targeted workloads.
  * Note: avoid broad, cluster-wide changes during an active incident; prefer targeted, minimal changes.

<Callout icon="warning">
  During an incident prefer reversible, minimal changes. Large, unreviewed edits or cluster-wide operations increase risk and can create cascading failures.
</Callout>

Quick phase-to-tool reference

| Phase       | Common tools / actions                                             |
| ----------- | ------------------------------------------------------------------ |
| Alert       | Alertmanager, PagerDuty, Slack; check alert details and timestamps |
| Assess      | Grafana dashboards, runbooks, deployment history                   |
| Investigate | Prometheus (PromQL), Jaeger traces, Loki/kubectl logs              |
| Fix         | kubectl, Helm, GitOps rollbacks, targeted scaling or config edits  |
| Validate    | Grafana dashboards, synthetic tests, user-facing checks            |

Key takeaways

* Follow the playbook every time: Alert → Assess → Investigate → Fix → Validate.
* Never skip the Assess phase; the 60-second check prevents wasted effort.
* Use the three observability pillars as a funnel: metrics detect, traces locate, logs explain.
* Prefer minimal, reversible fixes that restore service quickly and enable deeper post-incident investigation.
* Track DORA metrics to measure platform health and quantify improvements to MTTR.

Links and references

* [Prometheus Documentation](https://prometheus.io/docs/)
* [Grafana Docs](https://grafana.com/docs/)
* [Jaeger Tracing](https://www.jaegertracing.io/docs/)
* [Loki Logging](https://grafana.com/oss/loki/)
* [Kubernetes kubectl reference](https://kubernetes.io/docs/reference/kubectl/)

Use this playbook as your default incident response flow. With consistent practice and post-incident learning, the same tools will yield much faster, safer outcomes.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/a32b40e5-e639-40ca-bd3a-00bb8cf752cf" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/e88d8670-511b-4f7a-b1ba-5fa0421e2bbe" />
</CardGroup>
