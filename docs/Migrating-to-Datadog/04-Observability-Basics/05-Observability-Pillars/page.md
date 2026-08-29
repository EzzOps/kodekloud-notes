# Observability Pillars

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Observability-Basics/Observability-Pillars/page

Explains metrics, logs, traces, and profiles and how correlating them helps diagnose incidents and optimize system performance.

We're returning to fundamentals to cover the four pillars of observability: metrics, logs, traces, and profiles. An observability stack exposes different kinds of telemetry so engineers can reason about system behavior. Knowing what each telemetry type represents, how it's used, and how to correlate them helps you diagnose incidents faster and optimize systems more effectively.

<Callout icon="lightbulb">
  Observability is most powerful when you combine telemetry types: metrics for trends and alerts, logs for detailed events, traces for request flow, and profiles for resource-level hotspots.
</Callout>

An observability stack commonly provides the following telemetry:

| Pillar   | What it captures                                       | Typical use / visualization                           | Example                                                                            |
| -------- | ------------------------------------------------------ | ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Metrics  | Numeric measurements at a timestamp                    | Dashboards, alerting, trend analysis                  | `cpu.utilization`, `requests.count`                                                |
| Logs     | Time-stamped, structured or unstructured event records | Searchable event history, forensic analysis           | `{"timestamp":"2023-07-01T10:31:54Z","source":"MediaSystem","action":"NextMusic"}` |
| Traces   | Distributed request flows composed of spans            | Latency breakdowns, service dependency maps           | Trace with spans showing RPC times                                                 |
| Profiles | Runtime samples of CPU, memory, I/O, locks             | Flame graphs, allocation hotspots, performance tuning | CPU flame graph from a sampled profiler                                            |

<Frame>
  <img alt="The image describes the &#x22;Four Pillars of Observability&#x22;: Metrics, Logs, Traces, and Profiles, explaining each briefly." />
</Frame>

## Metrics

Metrics are numeric observations of system state recorded at specific timestamps. Think of a car speedometer: it tells you how fast you're going at a moment in time. When you accelerate, the metric increases; when you brake, it decreases.

Common metric types:

* Gauges — instantaneous values (e.g., temperature, current heap size).
* Counters — monotonic counts that are typically converted to rates (e.g., requests served).
* Histograms / Summaries — distributions used for latency percentiles and value aggregation.

Metrics are ideal for dashboards and alerting because they are lightweight, easy to aggregate, and efficient to retain over long periods.

<Frame>
  <img alt="The image contains three metrics for a car, a ball, and an API, displaying speed and gas for the car, weight and kick speed for the ball, and requests and average response time for the API." />
</Frame>

## Logs

Logs are chronological records that describe discrete events with contextual fields. They are invaluable for reconstructing what happened during an incident and for storing rich diagnostic information.

* Structured logs (JSON, key-value) are preferred because they make querying and correlation straightforward.
* Include context fields (request ID, user ID, component name) to link logs to traces and metrics.

Examples:

```json theme={null}
{ "timestamp": "2023-07-01T10:31:54Z", "source": "MediaSystem", "action": "NextMusic" }
```

```csv theme={null}
2023-07-01T10:31:54Z,MediaSystem,NextMusic
```

<Frame>
  <img alt="The image shows a log entry system illustrating how log data is formatted in both JSON and CSV formats, with timestamps and actions performed by a media system." />
</Frame>

## Traces

Traces record the end-to-end flow of a request through a distributed system. A trace is composed of spans; each span represents an operation, its start and end time, status, and metadata. Tracing helps you see ordering, cross-service latency, and where time is spent.

Use cases:

* Pinpoint slow services or downstream dependencies.
* Understand causality and the sequence of operations.
* Correlate traces with logs via trace IDs and with metrics for aggregate latency.

Example scenario: if a car won’t start, metrics and logs might only show symptoms. A trace could reveal a failing fuel-injector span that blocks fuel delivery and causes the failure.

<Frame>
  <img alt="The image shows a car on a road with a highlighted engine part and a warning that the injector is malfunctioning, blocking gas from entering the engine." />
</Frame>

## Profiles

Profiling captures continuous, low-overhead runtime information about resource usage (CPU sampling, memory allocations, blocking operations, I/O) so you can identify hotspots and inefficient code paths. Flame graphs are the common visualization for profiling data and make hot call stacks easy to spot.

* Sampling profilers periodically capture stack traces with minimal runtime overhead.
* Instrumentation profilers record detailed allocation or lock events when deeper insight is required.
* Profiles complement traces: use traces to find which requests are slow and profiles to see which functions consume the most CPU or memory during those requests.

<Frame>
  <img alt="The image is an infographic titled &#x22;Profiles&#x22; with icons and text explaining features like understanding application processes, identifying performance problems, using flame graphs, and enhancing system optimization." />
</Frame>

Key benefits of profiling:

* Understand internal behavior of applications at the function-call level.
* Identify and prioritize performance improvements.
* Use flame graphs to quickly locate long-running or resource-heavy call stacks.
* Combine profiles with traces to connect slow requests to hot code paths.

<Callout icon="warning">
  Be mindful of data volume and sampling: high-cardinality metrics and verbose logs can increase costs, while overly aggressive profiling or tracing can add overhead. Use sampling, aggregation, and structured logging to balance observability depth with performance and cost.
</Callout>

Links and References

* [OpenTelemetry](https://opentelemetry.io/) — vendor-neutral observability instrumentation.
* [Prometheus](https://prometheus.io/) — metrics collection and alerting.
* [Jaeger](https://www.jaegertracing.io/) — distributed tracing.
* [Flame Graphs (Brendan Gregg)](http://www.brendangregg.com/flamegraphs.html) — profiling visualization techniques.

And that's it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/9d4795bc-91eb-4262-ae9c-f7153c17438e/lesson/662a3003-2c3e-4afc-b8da-f53c2d8c6ebe" />
</CardGroup>
