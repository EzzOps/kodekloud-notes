# Monotonicity

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Monotonicity/page

Describes metric monotonicity, choosing Counters versus Gauges and proper aggregation for accurate rates and current state measurements

Monotonicity describes whether a metric's value moves in a single direction over time (only increases) or can both increase and decrease. Understanding monotonicity is essential for choosing the right instrument, aggregation, and downstream calculations (for example, computing rates or deltas).

<Frame>
  <img alt="The image explains the concept of monotonicity, describing it as a property where a metric's value either only increases (monotonic) or can both increase and decrease (non-monotonic)." />
</Frame>

Key distinctions:

* Monotonic metric: Value only increases (e.g., cumulative counters).
* Non-monotonic metric: Value can increase and decrease (e.g., gauges).

Common analogies:

* Monotonic: an electricity meter or an HTTP request counter — readings only go up.
* Non-monotonic: a speedometer or thermometer — readings go up and down.

A typical monotonic example is a counter that tracks the total number of HTTP requests handled by a service. Gauges are used for values that fluctuate, such as current CPU or memory usage.

<Frame>
  <img alt="The image compares monotonic and non-monotonic values, using a clicker counter to represent monotonic values that only increase, and a speedometer and thermometer to illustrate non-monotonic values that can both increase and decrease." />
</Frame>

Operational metrics such as CPU usage, memory usage, and queue length are normally non-monotonic: they rise and fall as load changes. Monotonicity directly influences the choice of instrument type and aggregation method:

* Use a `Counter` for monotonically increasing measurements and aggregate as `Sum` (often used to compute deltas or rates).
* Use a `Gauge` or `ObservableGauge` for measurements that can go up and down and aggregate as `LastValue` (to represent the current state).

Summary table: instrument, aggregation, and example use cases.

|                  Instrument |        Typical aggregation | Typical use case                              |
| --------------------------: | -------------------------: | --------------------------------------------- |
|                   `Counter` |                      `Sum` | Total number of requests, retries, bytes sent |
| `Gauge` / `ObservableGauge` |                `LastValue` | Current CPU usage, memory usage, queue length |
|                 `Histogram` | `Distribution` / `Buckets` | Latency distributions, payload sizes          |

<Frame>
  <img alt="The image is an educational slide explaining why monotonicity matters, highlighting the importance of choosing the right instrument (Counter/Gauge) and ensuring correct metric aggregation, accompanied by a graphic of a laptop loading." />
</Frame>

Illustration: a monotonic HTTP request counter never decreases. The slope varies (fast during traffic spikes, flat when idle), but the value always moves forward. This property makes Counters ideal for computing rates (requests per second) by taking deltas over time.

<Frame>
  <img alt="The image is a graph showing the monotonic increase in HTTP request counts over time for an Apollo Gateway, with specific points marked at times T1, T2, and T3. The axis represents the number of requests, displaying a step-like pattern as it increases." />
</Frame>

Contrast with non-monotonic metrics: queue size, CPU, and memory usage can increase and decrease. These fluctuations require different handling and aggregations because deltas or rate computations on these values do not make sense.

<Frame>
  <img alt="The image displays a non-monotonic example with a graph showing queue size changes over time and gauges for CPU and memory usage, indicating 16.775% CPU usage and 48.2% memory usage." />
</Frame>

Practical examples (pseudocode):

* Monotonic Counter (OpenTelemetry-like pseudocode)

```javascript theme={null}
const requests = meter.createCounter("http.server.requests", {
  description: "Total number of HTTP requests"
});

// Increment on each request
requests.add(1, { route: "/api" });
```

* Non-monotonic Gauge (OpenTelemetry-like pseudocode)

```python theme={null}
cpu_gauge = meter.create_observable_gauge(
    "system.cpu.usage",
    callback=observe_cpu_usage,
    description="Current CPU usage percentage"
)
```

In short:

* If the measurement only ever increases, treat it as monotonic: use `Counter` and aggregate as `Sum`.
* If it can go up and down, treat it as non-monotonic: use `Gauge`/`ObservableGauge` and aggregate as `LastValue`.

> **lightbulb** Choosing the correct instrument and aggregation for monotonic vs. non-monotonic metrics ensures accurate downstream calculations (for example, computing rates, deltas, or current-state snapshots). This improves alerting, dashboards, and capacity planning.

> **warning** Do not model decreasing values with a `Counter`. Treating non-monotonic data as monotonic leads to incorrect sums, rates, and alerts. If you need to represent decreases, use a `Gauge` or an appropriate observable instrument.

Links and references:

* [OpenTelemetry Metrics Specification](https://opentelemetry.io/docs/specs/otel/metrics/)
* [OpenTelemetry Instrumentation Concepts](https://opentelemetry.io/docs/concepts/)
* [Monitoring Best Practices: Counters vs Gauges](https://prometheus.io/docs/practices/naming/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/6251147c-cf4c-4afa-b83d-558a4da5350e)
