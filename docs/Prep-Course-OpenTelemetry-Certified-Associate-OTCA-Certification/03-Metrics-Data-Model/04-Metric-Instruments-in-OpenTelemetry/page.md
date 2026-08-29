# Metric Instruments in OpenTelemetry

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Metric-Instruments-in-OpenTelemetry/page

Overview of OpenTelemetry metric instruments, their synchronous versus asynchronous types, instrument behaviors (counter, histogram, gauge, updowncounter), and guidance for selecting and using them

In this lesson we examine metric instruments in OpenTelemetry: the primitives that produce metric data points. Every instrument you define begins with a few core parameters: a name and a kind (type). Optionally, you can supply a unit, description, and advisory hints (for example, explicit histogram bucket boundaries).

Here’s a typical example that creates a synchronous counter in Python:

```python theme={null}
request_counter = meter.create_counter(
    name="http.requests_total",
    unit="1",
    description="Total number of HTTP requests",
)
```

* name: the instrument identifier, e.g. `http.requests_total`.
* unit: the measurement unit, e.g. `"1"` for a simple count.
* description: a human-readable explanation of what the instrument measures.

<Frame>
  <img alt="The image outlines the components of &#x22;Instrument Parameters,&#x22; including Instrument Name, Kind, Units, Descriptions, and Advisory Parameters, with descriptions of their purposes. It also includes an example of a &#x22;Counter&#x22; named &#x22;request_count&#x22; that tallies incoming requests." />
</Frame>

Instrument parameters (quick reference)

* Instrument name: identifies what is being measured (for example, `request_count` or `http.requests_total`).
* Kind: determines the instrument behavior (Counter, Gauge/ObservableGauge, Histogram, UpDownCounter, and their async counterparts).
* Unit and description: give context so humans and backends can interpret values correctly.
* Advisory hints: optional guidance such as explicit histogram bucket boundaries.

OpenTelemetry instruments are grouped into synchronous and asynchronous types.

Synchronous instruments record measurements inline within application logic. They run on the same thread and carry the active execution context, so recorded values can be associated with the current trace/span and other contextual attributes.

<Frame>
  <img alt="The image compares synchronous and asynchronous instruments, highlighting that synchronous measurements are recorded &#x22;inline&#x22; with application logic and are context-aware." />
</Frame>

<Callout icon="warning">
  Asynchronous callbacks typically run without an active trace/span context. Do not rely on trace context inside asynchronous callbacks—design async metrics to be context-independent.
</Callout>

Asynchronous instruments are callback-driven and report values at collection time. They are ideal when periodic or on-request snapshots are sufficient and when frequent synchronous updates are unnecessary.

Instrument types and when to use them

* Counter (synchronous)
  * Records increases only (monotonic).
  * Synchronous: can be associated with the current trace/span and context.
  * Use for counting events such as completed orders, processed requests, or errors in real time.
  * Aggregation: sum.

<Frame>
  <img alt="The image describes a &#x22;Counter Instrument,&#x22; which is a synchronous monotonic tool that tracks ever-increasing totals like requests or bytes processed. It highlights features such as synchrony, monotonic behavior, count recording, and context association." />
</Frame>

* Asynchronous Counter
  * Callback-based: the SDK invokes a function at collection time to obtain a reported value.
  * Monotonic: typically used to represent cumulative totals (depending on how the callback reports the metric).
  * No guaranteed context association during callback execution.
  * Use for metrics like total bytes transmitted since process start, where continuous synchronous updates are unnecessary.

Example asynchronous counter callback (Python pseudocode):

```python theme={null}
def collect_total_bytes(observer):
    # Compute the cumulative total when the collector runs
    observer.observe(total_bytes_sent, attributes={"unit": "bytes"})

meter.create_observable_counter(
    name="process.network.bytes_total",
    callback=collect_total_bytes,
    description="Total network bytes sent by process"
)
```

<Frame>
  <img alt="The image describes an &#x22;Asynchronous Counter Instrument,&#x22; highlighting its use for reporting cumulative, monotonic values via callbacks, and its characteristics like being ideal for metrics such as CPU time, callback-based, and having no context association." />
</Frame>

* Histogram (synchronous)
  * Records arbitrary values (not restricted to monotonic increases).
  * Produces statistical summaries such as percentiles and distributions (backends compute percentiles from histogram aggregates).
  * Useful for response times, payload sizes, or any measurement where distribution matters.
  * Aggregation: histogram (bucketed distribution).

<Frame>
  <img alt="The image describes a histogram instrument as a tool for capturing arbitrary measurements to produce statistical summaries like percentiles. It lists features such as recording arbitrary values, generating summaries and percentiles, understanding distributions, and not requiring monotonicity." />
</Frame>

* Gauge (last-value snapshot)
  * Represents a current state or snapshot (values can go up or down).
  * Non-additive and typically uses last-value aggregation.
  * In OpenTelemetry, gauges are commonly implemented as observable (asynchronous) instruments reported via callbacks (ObservableGauge). Some SDKs may also offer last-value synchronous instruments—behavior and context association depend on the SDK.
  * Ideal for CPU usage, memory usage, queue length, active user counts, or any value representing current state.

<Frame>
  <img alt="The image is an infographic about a gauge instrument, describing it as recording non-additive measurements that update with changes in values, such as background noise levels, and highlighting features like non-additive values, constant changes, current value, and context association." />
</Frame>

* Asynchronous Gauge
  * Callback-based snapshot collected on demand (ObservableGauge).
  * No guaranteed context association during callback execution.
  * Use for periodically sampled readings such as disk space remaining, battery level, thread count, temperature, or humidity.

* UpDownCounter (synchronous)
  * Supports both increments and decrements (non-monotonic).
  * Additive aggregation (sum), but values can go up or down.
  * Synchronous version supports context association.
  * Use for dynamic counts like queue sizes, active connections, or concurrent requests.

<Frame>
  <img alt="The image is a presentation slide about the UpDownCounter Instrument, highlighting its features such as tracking increments and decrements, non-monotonic behavior, queue size, and context association. It is useful for tracking dynamic counts like active requests or queue length." />
</Frame>

* Asynchronous UpDownCounter
  * Callback-based, reports additive snapshots but values can increase or decrease (ObservableUpDownCounter).
  * No guaranteed context association during callback execution.
  * Use cases: number of running processes, open file descriptors, connected clients—metrics collected periodically via a callback.

<Frame>
  <img alt="The image describes the &#x22;Asynchronous UpDownCounter Instrument,&#x22; highlighting that it is callback-based, reports additive values such as process snapshots, and operates on observation without context association. Examples include running processes and open file descriptors reported by a callback." />
</Frame>

Comparison summary (behavior and aggregation)

| Instrument                                 | Behavior                                                             | Aggregation          | Typical use cases                                     |
| ------------------------------------------ | -------------------------------------------------------------------- | -------------------- | ----------------------------------------------------- |
| Counter (sync) / Async Counter             | Additive, monotonic. Sync is context-aware; async is callback-based. | Sum                  | Event counts, total requests, bytes transmitted       |
| Histogram (sync)                           | Non-additive, non-monotonic; records distributions                   | Histogram (bucketed) | Latencies, payload sizes, response time distributions |
| Gauge (ObservableGauge)                    | Non-additive, non-monotonic; last-value snapshot                     | Last-value           | CPU, memory, queue length, live counts                |
| UpDownCounter (sync) / Async UpDownCounter | Additive but non-monotonic; sync supports context                    | Sum                  | Queue size, active connections, running processes     |

<Callout icon="lightbulb">
  Choose the instrument that matches how you want the metric to behave and how your backend will aggregate it:

  * Counter: count occurrences over time (monotonic sum).
  * UpDownCounter: counts that can increase or decrease (e.g., active sessions).
  * Gauge / ObservableGauge: current-state snapshots (last-value).
  * Histogram: distributions and percentiles (latencies, sizes).
</Callout>

That covers the key metric instruments in OpenTelemetry: counters, up-down counters, gauges (last-value/observable), histograms, and their asynchronous counterparts. Select instruments based on metric semantics, collection cadence, and whether you need trace/context association.

Links and references

* OpenTelemetry Metrics specification: [https://opentelemetry.io/docs/reference/specification/metrics/](https://opentelemetry.io/docs/reference/specification/metrics/)
* OpenTelemetry Python metrics API: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* For aggregation and backend behavior, consult your metrics backend documentation (e.g., Prometheus, OTLP-compatible backends).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/396517cd-fd19-4a34-9dfa-033278b18024" />
</CardGroup>
