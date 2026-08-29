# app.py
import time
from flask import Flask, request
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource

def configure_meter():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())
    set_meter_provider(provider)
    return get_meter_provider().get_meter(name="shopping-app", version="0.1.2")

meter = configure_meter()

# Cumulative counter: total requests processed (completed)
requests_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of requests processed by the application",
    unit="1"
)

# Up-down counter: concurrent requests in progress
concurrent_requests = meter.create_up_down_counter(
    "concurrent_requests",
    description="Total number of requests in progress",
    unit="1"
)

app = Flask(__name__)

@app.before_request
def before_request():
    # Increment concurrent requests when a request starts.
    # Add attributes so we can break down by route/method if desired.
    concurrent_requests.add(1, {"route": request.path, "method": request.method})

@app.after_request
def after_request(response):
    # Decrement concurrent requests when the response is about to be sent.
    concurrent_requests.add(-1, {"route": request.path, "method": request.method})

    # Increment total requests processed (completed) here so we count only finished requests.
    requests_counter.add(1, {"route": request.path, "method": request.method})

    return response

@app.get("/products")
def get_products():
    return "Get All Products"

@app.get("/products/<int:id>")
def get_product(id):
    return f"Getting product detail for {id}"

@app.post("/products")
def create_product():
    # Simulate a slow route to observe concurrent requests.
    time.sleep(10)
    return "Creating Product", 201

if __name__ == "__main__":
    app.run(debug=True)
```

How it works

* `before_request` runs before Flask dispatches to the route handler. We increment `concurrent_requests` there (with `route` and `method` attributes) to indicate a request has started.
* `after_request` runs after the route handler returns but before the response is sent. We decrement `concurrent_requests` and increment `http_requests_total` here, so the total only counts completed responses.
* The slow `POST /products` route uses `time.sleep(10)` so you can make multiple concurrent requests and observe `concurrent_requests` rising while requests are still in-flight.

Testing with curl

* Fast route:

```bash theme={null}
curl -X GET http://127.0.0.1:5000/products
```

* Slow route (takes \~10 seconds to return):

```bash theme={null}
curl -X POST http://127.0.0.1:5000/products
```

Example console metric exports (sample)

```json theme={null}
{
  "attributes": {
    "route": "/products",
    "method": "POST"
  },
  "start_time_unix_nano": 1757999681879945400,
  "time_unix_nano": 1757997074651432000,
  "value": 1,
  "exemplars": []
}
```

```json theme={null}
{
  "attributes": {
    "route": "/products",
    "method": "GET"
  },
  "start_time_unix_nano": 1757996981879945000,
  "time_unix_nano": 1757996981948106000,
  "value": 2,
  "exemplars": []
}
```

Notes and practical tips

* Place the total requests increment in `after_request` so you count only completed responses.
* Attach attributes like `route` and `method` with each metric call to enable dimensional filtering and per-endpoint breakdowns. For example: `{"route": request.path, "method": request.method}`.
* Export interval controls how often metrics are pushed to the exporter. In this example the reader is configured with `export_interval_millis=5000` to export every 5 seconds.
* If your application can raise exceptions during request handling, consider ensuring the decrement always runs (see warning below).

<Callout icon="warning">
  If a request handler raises an exception, `after_request` may not always run. To guarantee the concurrent counter is decremented in all cases, consider using Flask's `teardown_request` (which runs for both successful and failed requests) or ensure exception paths also decrement the up-down counter.
</Callout>

Configuration summary

| Setting                    | Purpose                                    | Example                                                                |
| -------------------------- | ------------------------------------------ | ---------------------------------------------------------------------- |
| Exporter                   | Sends metric data to a destination         | `ConsoleMetricExporter()`                                              |
| Reader                     | Controls export frequency                  | `PeriodicExportingMetricReader(exporter, export_interval_millis=5000)` |
| Meter name/version         | Identify the instrumenting library/service | `get_meter(name="shopping-app", version="0.1.2")`                      |
| Attributes on metric calls | For dimensional metrics and filtering      | `{"route": request.path, "method": request.method}`                    |

Links and references

* Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* OpenTelemetry Python metrics: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* OpenTelemetry metrics SDK: [https://github.com/open-telemetry/opentelemetry-python](https://github.com/open-telemetry/opentelemetry-python)

This pattern gives you both a cumulative throughput signal (total requests processed) and a live concurrency signal (current in-progress requests), enabling better observability and capacity planning for your web service.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/5fbd3985-9c0d-489f-86a8-88c10f4724ff" />
</CardGroup>


# Exemplars

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Exemplars/page

Explains exemplars in observability, how metric samples capture trace and span context to link metrics to traces for faster root cause analysis and improved monitoring.

Exemplars are contextual breadcrumbs that metrics can leave behind to connect numeric measurements with trace data. Rather than being random samples, exemplars are representative specimens captured at the exact moment a measurement occurs. They let you attach additional context—most commonly trace IDs and span IDs—to a specific metric observation, making it possible to jump directly from a metric anomaly to the distributed trace that produced it.

<Frame>
  <img alt="The image explains exemplars as sample data points associated with specific time series in metrics, highlighting their role in capturing the context of measurements for enabling correlation of metric data with trace data." />
</Frame>

Why exemplars matter

* They enrich metrics with non-metric context (trace IDs, span IDs, and filtered attributes), turning raw numbers into actionable signals.
* The primary use case is linking a metric data point directly to the trace that was active when the measurement occurred, enabling rapid investigation.
* Exemplars speed up root-cause analysis by letting you navigate from an outlier metric point straight to the trace details.
* They improve observability by providing the “why” behind metric changes, not just the “what.”

What an exemplar contains

* Value: the measurement itself (e.g., the value passed to `counter.Add()` or `histogram.Record()`).
* Timestamp: the exact time the measurement was recorded.
* Filtered attributes: labels that remain after any views/filters are applied to reduce noise while preserving useful context.
* Trace context: the trace ID and span ID linking the measurement to a distributed trace.

<Frame>
  <img alt="The image illustrates four types of information an exemplar carries: Value, Timestamp, Filtered Attributes, and Trace Context, each with a brief description." />
</Frame>

Quick reference: exemplar components

| Element             | Description                               | Example                                     |
| ------------------- | ----------------------------------------- | ------------------------------------------- |
| Value               | The numeric measurement recorded          | `histogram.Record(245)`                     |
| Timestamp           | When the measurement occurred             | `2026-07-15T12:34:56Z`                      |
| Filtered attributes | Labels retained after views/filters       | `service="checkout", region="us-east-1"`    |
| Trace context       | Trace ID and span ID linking to the trace | `trace_id=4bf92f3577b34da6a3ce929d0e0e4736` |

Enabling exemplars (C# / .NET)
Below is a typical .NET MeterProvider configuration that enables trace-based exemplars and exports metrics to both the console and an OTLP collector endpoint:

```csharp theme={null}
using var meterProvider = Sdk.CreateMeterProviderBuilder()
    .SetResourceBuilder(resource)
    .AddMeter("MyCompany.MyProduct.MyLibrary")
    .SetExemplarFilter(ExemplarFilterType.TraceBased) // Enable trace-based exemplars
    .AddConsoleExporter() // Export metrics to console for debugging
    .AddOtlpExporter(options => options.Endpoint = new Uri("http://localhost:4317"))
    .Build();
```

<Callout icon="lightbulb">
  Setting `SetExemplarFilter(ExemplarFilterType.TraceBased)` tells the OpenTelemetry SDK to attach trace and span IDs to metric measurements when a trace is active, creating exemplars automatically.
</Callout>

How exemplars are captured and surfaced

* Capture: When a metric is recorded and there is an active trace, the metrics SDK captures the trace ID and span ID and attaches them to that measurement as an exemplar.
* Export: Exemplars are exported along with metric data to your observability backend (for example, an OTLP collector).
* Visualization: The observability backend (the visualization layer) links and stitches metrics, traces, and logs so that exemplars can be displayed as clickable markers on charts. Clicking an exemplar usually reveals the trace ID and a link to the full trace.

Using exemplars with Prometheus and UI integrations
In dashboards that plot histograms or other metrics (e.g., HTTP latency), exemplars appear as individual clickable markers. With exemplars enabled, clicking a plotted data point may provide the trace link for the exact request that produced it.

Example PromQL query to compute a percentile from an HTTP server histogram:

```promql theme={null}
histogram_quantile(
  0.75,
  sum by (le)(
    rate(http_server_duration_milliseconds_bucket{job="exemplar"}[5m])
  )
)
```

When exemplars are present, many UIs will show exemplar markers on the plotted series. Clicking one of those markers lets you follow the exemplar link to the trace that generated that measurement.

Practical benefits

* Correlation: Associate trace and attribute context with metric samples to get immediate context for metric anomalies.
* Faster troubleshooting: Jump from an anomalous metric point to the exact trace that produced it.
* Contextual observability: Move beyond isolated metrics to an integrated view of metrics, traces, and logs.
* Efficiency: Reduce time-to-resolution and improve resource utilization through clearer root-cause insights.

<Frame>
  <img alt="The image explains the importance of exemplars, highlighting their use in associating non-metric data with metric data, linking metrics to active traces, efficient troubleshooting, and improving contextual observability." />
</Frame>

How exemplars are created (step-by-step)

1. Configure the SDK to enable exemplar filtering (e.g., trace-based exemplars).
2. Record metrics in your instrumentation while traces are active.
3. The SDK captures trace context for those measurements and emits exemplars with the metric data.
4. The observability backend receives metrics and traces, stitches them together, and renders exemplar markers in the UI.

Summary

* Exemplars augment numeric metrics with trace and attribute context, providing a direct link between metrics and traces.
* They accelerate root-cause analysis by allowing you to jump from a metric anomaly to the exact trace that produced it.
* Exemplars enhance observability and reduce time-to-resolution by revealing why a metric value occurred, not just that it occurred.

<Frame>
  <img alt="The image lists three key benefits of exemplars: augmenting metrics with traces and logs, accelerating root cause analysis, and optimizing resource utilization." />
</Frame>

Further reading and references

* OpenTelemetry Metrics documentation: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* .NET instrumentation guide: [https://learn.microsoft.com/dotnet/](https://learn.microsoft.com/dotnet/)
* Prometheus querying basics: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)

That concludes this section about exemplars.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/e220557a-1a16-4b3e-9116-5b1d72122635" />
</CardGroup>
