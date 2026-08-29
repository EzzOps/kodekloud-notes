# collector-config.yaml (high-level example)
processors:
  tail_sampling:
    policies:
      - name: errors-policy
        type: status_code
      - name: latency-policy
        type: latency
      - name: probabilistic
        type: probabilistic
        sampling_percentage: 10
```

How tail sampling works (internal flow):

* Spans arrive at the OpenTelemetry Collector and are buffered until the trace completes or `decision_wait` expires.
* The tail sampler evaluates configured policies in order.
* The first matching policy determines whether the trace is kept; otherwise fallback rules (rate allocation, probabilistic rules) apply.
* Kept traces are exported; others are dropped.

<Frame>
  <img alt="The image is a flowchart showing how tail sampling works internally, with stages labeled as &#x22;Spans in,&#x22; &#x22;Buffer,&#x22; &#x22;Tail Sampler Policies,&#x22; and &#x22;Export.&#x22;" />
</Frame>

Policy examples, `decision_wait`, and behavior

The `decision_wait` parameter controls how long the collector waits for late-arriving spans before making a sampling decision. Typical values are a few seconds (for example, `5s`). Policies are evaluated in the configured order — the first matching policy decides to keep a trace.

Detailed example showing multiple policy types, a decision wait, and rate allocation:

```yaml theme={null}
# collector-config.yaml (detailed tail-sampling example)
processors:
  tail_sampling:
    decision_wait: 5s
    policies:
      - status_code:
          status_codes: ["ERROR"]
      - latency:
          threshold_ms: 1200
      - spans_count:
          min_spans: 50
      - string_attribute:
          key: tenant
          values: ["vip"]
      - rate_limiting:
          spans_per_second: 2000
    rate_allocation:
      policies:
        - name: remaining
          percentage: 5
```

Common policy types and when to use them:

| Policy Type     | Purpose                                       | Example snippet                   |
| --------------- | --------------------------------------------- | --------------------------------- |
| Status code     | Retain traces with error/failed status        | `status_codes: ["ERROR"]`         |
| Latency         | Capture slow requests exceeding a threshold   | `threshold_ms: 1200`              |
| Spans count     | Keep high-complexity traces with many spans   | `min_spans: 50`                   |
| Attribute match | Retain traces from important tenants/services | `key: tenant` / `values: ["vip"]` |
| Rate limiting   | Cap throughput to limit resource usage        | `spans_per_second: 2000`          |
| Rate allocation | Sample a percentage of remaining traces       | `percentage: 5`                   |

* The status code policy retains traces containing errors.
* The latency policy retains traces slower than 1200 ms.
* The spans count policy retains traces with many spans (e.g., >= 50).
* The attribute policy retains traces containing `tenant: "vip"`.
* The rate-limiting policy caps throughput (e.g., 2000 spans/sec).
* The rate allocation policy samples a percentage of traces that didn't match earlier rules (e.g., 5%).

<Callout icon="lightbulb">
  Set an appropriate `decision_wait` (for example, `decision_wait: 5s`) to balance waiting for late spans against export latency. Monitor late-span patterns and tune this value to match your environment.
</Callout>

Trade-offs of tail sampling

Tail sampling is powerful for retaining outcome-relevant traces, but it introduces trade-offs you must manage:

|             Trade-off | Impact                                                                                        |
| --------------------: | --------------------------------------------------------------------------------------------- |
|       Memory pressure | Traces are buffered until completion; memory usage increases with traffic and trace duration. |
|         Added latency | Export decisions are delayed until the trace completes (plus `decision_wait`).                |
|           Correctness | All spans for a trace must reach the same collector for accurate decisions.                   |
| Late spans / timeouts | Spans arriving after buffer expiry are dropped, potentially causing incomplete traces.        |

Monitor collector metrics (buffer sizes, dropped spans, memory usage, sampling decisions) to detect and address these impacts.

<Frame>
  <img alt="The image outlines trade-offs to watch in tail sampling, including memory pressure, latency, correctness, and timeout. Each trade-off has an associated consequence, such as increasing memory pressure or dropped late traces." />
</Frame>

Scaling: combine head and tail sampling

For high-volume environments, combine head (early) and tail (late) sampling:

* Head sampler (application or edge collector): perform early probabilistic sampling to reduce telemetry volume and cost.
* Tail sampler (downstream collector): retain outcome-relevant traces such as errors, slow traces, or traces from important tenants or services.

This hybrid approach balances cost control with the ability to preserve high-value traces for debugging and analysis.

<Frame>
  <img alt="The image illustrates a flowchart showing a &#x22;Head Sampler&#x22; leading to a &#x22;Tail Sampler,&#x22; emphasizing cost control and outcome relevance in optimizing pipeline efficiency." />
</Frame>

Distributed collectors and consistent hashing

When collectors are horizontally scaled, spans for the same trace can be routed to different collector instances. For correct tail sampling, ensure all spans for a given trace are routed to the same downstream collector. A common pattern:

* Deploy a first layer of stateless collectors (or edge collectors).
* Use a load-balancing exporter with consistent hashing (trace ID as the routing key) to route spans for the same trace to the same downstream stateful collector instance (e.g., a StatefulSet).
* The downstream collectors perform tail sampling on complete traces.

If a single collector handles all traffic, extra routing is not required. At scale, also add memory limiting and batching processors to stabilize resource usage:

```yaml theme={null}
# processors for resource control and batching
processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 3500
    spike_limit_mib: 500
  batch:
    send_batch_size: 2000
    timeout: 2s
```

Monitor collector metrics (dropped spans, memory usage, sampling decisions, buffer sizes) and tune `memory_limiter`, `batch`, and `decision_wait` accordingly.

<Callout icon="warning">
  If spans for a trace are routed to different collectors, tail sampling decisions will be inaccurate. Use consistent hashing (trace ID) in the load-balancing exporter to maintain trace integrity.
</Callout>

Summary and best practices

* Use head sampling to control telemetry volume early and reduce costs; use tail sampling to retain traces that matter based on full trace outcomes.
* Tail sampling is especially valuable where retaining all traces is infeasible but outcome-relevant traces must be preserved.
* For correct tail sampling at scale, route all spans of a trace to the same collector using consistent hashing on the trace ID.
* Monitor and tune: `decision_wait`, `memory_limiter`, and batching parameters to balance memory usage, latency, and sampling accuracy.
* Consider hybrid architectures (head + tail) to achieve both cost efficiency and diagnostic fidelity.

<Frame>
  <img alt="The image outlines various use cases for sampling, emphasizing head sampling for controlling telemetry volume, tail sampling for retaining high-value traces, and combining both for optimal results. It also suggests using tail sampling with load-balanced collectors to maintain accuracy." />
</Frame>

This means every trace must be routed (via consistent hashing on trace ID) to the same downstream collector so tail-based sampling decisions are accurate and trace integrity is preserved.

Links and references

* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Consistent hashing overview: [https://en.wikipedia.org/wiki/Consistent\_hashing](https://en.wikipedia.org/wiki/Consistent_hashing)
* OpenTelemetry sampling concepts: [https://opentelemetry.io/docs/concepts/sampling/](https://opentelemetry.io/docs/concepts/sampling/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/a6cac766-f402-4dc0-bc99-21b176f07b1f" />
</CardGroup>


# Alertmanager Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Alerting/Alertmanager-Architecture/page

Overview of Alertmanager architecture and alert processing flow from Prometheus including grouping, silences, inhibition, routing, and notification delivery to integrations

In this lesson we will learn about the architecture of Alertmanager and how it processes alerts from Prometheus.

What is Alertmanager?
Alertmanager receives alerts generated by one or more Prometheus servers and turns them into notifications. These notifications can be sent via integrations such as PagerDuty, webhooks, email, SMS, and chat. Multiple Prometheus servers can be configured to forward alerts to a single Alertmanager instance (or a highly available cluster of Alertmanagers) using the Alertmanager API.

High-level processing flow
When alerts arrive at Alertmanager they are processed through several stages in sequence. The core stages are: dispatching/grouping, silences, inhibition, routing, and finally notification delivery. The following diagram shows this flow and the typical receivers:

<Frame>
  <img alt="The image is a diagram illustrating the architecture of Alertmanager, showing the flow from alert sources through dispatching groups, inhibition, silencing, routing, notifications, and receivers like chat, pager, and email." />
</Frame>

Dispatcher / grouping
The first component that handles incoming alerts is the dispatcher (also called the grouping engine). It receives alerts and groups them according to your grouping configuration (for example by alertname and instance). Grouping controls how alerts are batched into notification messages and also helps with deduplication so that related alerts are sent together rather than as many individual notifications.

Silences
After grouping, alerts are evaluated against configured silences. Silences are temporary muting rules you create (often via the Alertmanager UI or API) to suppress notifications for known maintenance windows or expected disruptions. When a silence matches an alert, that alert’s notifications will be suppressed for the duration of the silence.

Inhibition
Following grouping and silences, alerts pass through the inhibition logic. Inhibition allows you to suppress one alert when a related alert is firing (and not silenced). For example, you can configure a rule that says: if alert X exists and is active, suppress alert Y. This is useful to avoid noisy or redundant notifications when a single root cause generates multiple dependent alerts.

Silences vs. Inhibition note:
Silences explicitly mute alerts for a configured time window. Inhibition conditionally suppresses notifications for target alerts when one or more source alerts are active; typically a source alert must be firing (and not silenced) for inhibition to take effect.

Routing
The routing tree determines which alerts are sent to which receivers and via which integration. Routes are matched based on alert labels and can inherit settings from parent routes. Routing controls:

* which receiver (or receivers) should get a particular alert,
* the grouping behavior and timing (how long to wait before sending grouped alerts),
* and any route-specific notification settings.

Notification engine
Once the routing logic has determined the receiver(s), the notification engine is responsible for actually delivering the notifications to the configured integrations (email, PagerDuty, webhooks, chat platforms, etc.). It handles formatting the messages, retrying failed deliveries, and tracking notification statuses.

Putting it together

* Prometheus sends alerts to Alertmanager via its API.
* The dispatcher groups alerts.
* Silences temporarily mute alerts for planned events or maintenance.
* Inhibition suppresses dependent or redundant alerts when configured source alerts are active.
* Routing decides which receiver(s) should be notified.
* The notification engine delivers the alerts to external systems.

<Callout icon="lightbulb">
  Configure grouping, inhibition, silences, and routing thoughtfully to minimize noisy alerts and ensure the right teams receive meaningful notifications.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/ab0e2c24-453b-49ce-be91-5344c9b697c8" />
</CardGroup>
