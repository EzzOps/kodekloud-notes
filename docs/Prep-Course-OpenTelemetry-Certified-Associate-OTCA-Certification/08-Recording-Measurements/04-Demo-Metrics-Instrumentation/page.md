# metrics_setup.py
import time
import os
import random
import psutil

from flask import Flask, request
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics import MeterProvider, Observation
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import View, ExplicitBucketHistogramAggregation
from opentelemetry.sdk.resources import Resource

def configure_meter():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

    # Example: create provider without custom views for now
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create({}))
    set_meter_provider(provider)

    return get_meter_provider().get_meter(name="shopping-app", version="0.1.2")

meter = configure_meter()

# Instruments
requests_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of requests processed by the application",
    unit="1"
)
concurrent_requests = meter.create_up_down_counter(
    "concurrent_requests",
    description="Total number of requests in progress",
    unit="1"
)
total_request_duration = meter.create_histogram(
    "total_request_duration",
    description="Request Duration",
    unit="ms"
)
```

Table: Instruments and use cases

| Instrument    |                                     Use case | Example (attributes or recorded value)                                      |
| ------------- | -------------------------------------------: | --------------------------------------------------------------------------- |
| Counter       |               Track total number of requests | `requests_counter.add(1, {"route": "/products", "method": request.method})` |
| UpDownCounter | Track number of requests currently in-flight | `concurrent_requests.add(1)` and `concurrent_requests.add(-1)`              |
| Histogram     |      Record request duration in milliseconds | `total_request_duration.record(latency_ms, {"route": request.path})`        |

You can activate your virtual environment and exercise the API with curl:

```bash theme={null}
source /Users/sanjeev/Documents/courses/metrics-instrumentation/.venv/bin/activate
curl 127.0.0.1:5000/products
```

## Calculating per-request latency in Flask

Use Flask's `before_request` to capture the request start time and increment the concurrent counter. Use `after_request` to compute the latency, record it to the histogram, and decrement the concurrent counter.

Note: store the start time with `time.time()` (seconds) and convert to milliseconds when recording to the histogram (since the histogram's unit is `"ms"`).

```python theme={null}
# app.py
from flask import Flask, request
import time
import random

from metrics_setup import requests_counter, concurrent_requests, total_request_duration

app = Flask(__name__)

@app.before_request
def before_request():
    # store start timestamp in seconds
    request.start_time = time.time()
    concurrent_requests.add(1)

@app.after_request
def after_request(response):
    # compute latency in milliseconds
    request_latency_ms = (time.time() - request.start_time) * 1000
    concurrent_requests.add(-1)
    # record the latency with useful attributes
    total_request_duration.record(request_latency_ms, {"route": request.path, "method": request.method})
    return response

@app.get("/products")
def get_products():
    requests_counter.add(1, {"route": "/products", "method": request.method})
    # simulate variable processing time between 50ms and 1500ms
    time.sleep(random.uniform(0.05, 1.5))
    return "Get All Products"

@app.get("/products/<int:id>")
def get_product(id):
    requests_counter.add(1, {"route": "/products/<id>", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Getting product detail"

@app.post("/products")
def create_product():
    requests_counter.add(1, {"route": "/products", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Creating Product"

@app.patch("/products/<int:id>")
def patch_product(id):
    requests_counter.add(1, {"route": "/products/<id>", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Patching Product"

@app.delete("/products/<int:id>")
def delete_product(id):
    requests_counter.add(1, {"route": "/products/<id>", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Deleting Product"

@app.get("/cart")
def get_cart():
    requests_counter.add(1, {"route": "/cart", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Get Cart"

@app.patch("/cart/<int:id>")
def update_cart(id):
    requests_counter.add(1, {"route": "/cart/<id>", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Update Cart"

if __name__ == "__main__":
    app.run()
```

A few practical notes:

* Restart the application and send multiple requests so the histogram sees a variety of latencies:
  ```bash theme={null}
  curl 127.0.0.1:5000/products
  curl 127.0.0.1:5000/products
  curl 127.0.0.1:5000/products
  ```
* The `ConsoleMetricExporter` will periodically print the aggregated metrics (here every 5 seconds). The histogram export contains `count`, `sum`, `bucket_counts`, and `explicit_bounds`.

Example console histogram output (trimmed):

```json theme={null}
{
  "name": "total_request_duration",
  "description": "Request Duration",
  "unit": "ms",
  "data": {
    "data_points": [
      {
        "attributes": {},
        "start_time_unix_nano": 1762221197726008000,
        "time_unix_nano": 1762221323582426000,
        "count": 14,
        "sum": 1228.0471912733765,
        "bucket_counts": [0, 0, 0, 0, 2, 3, 4, 5, 0],
        "min": 35.089421272727783,
        "max": 141.25659465789795
      }
    ],
    "explicit_bounds": [
      0.0, 5.0, 10.0, 25.0, 50.0, 75.0, 100.0, 250.0
    ]
  }
}
```

Interpretation:

* `count` is the total number of recorded observations.
* `sum` is the sum of all latencies in milliseconds.
* `bucket_counts` is cumulative: each element is the count of observations \<= corresponding bound in `explicit_bounds`.
  * For example, the count for a 75ms bucket includes observations from the 0, 5, 10, 25, 50, and 75ms buckets.
* Use min/max to quickly spot extreme values.

<Callout icon="warning">
  Make sure `request.start_time` is set before `after_request` tries to compute latency. If your app raises an exception and `after_request` doesn't run, consider registering `teardown_request` or an exception handler to ensure counters are adjusted and latencies are recorded or cleaned up appropriately.
</Callout>

## Customizing histogram buckets

Default SDK histogram buckets may not match your application's latency profile. You can provide explicit bucket boundaries using a View and `ExplicitBucketHistogramAggregation`. This example shows how to configure a MeterProvider with custom buckets (in milliseconds). Save as `metrics_setup_with_buckets.py`.

```python theme={null}
# metrics_setup_with_buckets.py
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import View, ExplicitBucketHistogramAggregation
from opentelemetry.sdk.resources import Resource

def configure_meter_with_buckets():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

    # Custom bucket boundaries (in milliseconds)
    buckets = [0.0, 20.0, 30.0, 60.0, 100.0, 250.0, 2000.0]

    # Create a View for our histogram instrument name
    view = View(
        instrument_name="total_request_duration",
        [SECRET_REDACTED](boundaries=buckets),
    )

    # Pass the view(s) to the MeterProvider
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create({}), views=[view])
    set_meter_provider(provider)

    return get_meter_provider().get_meter(name="shopping-app", version="0.1.2")

# Use configure_meter_with_buckets() instead of configure_meter() when starting the app
```

Restart the app with the custom view, generate requests, and the console will show `explicit_bounds` equal to the `buckets` you provided:

```json theme={null}
{
  "name": "total_request_duration",
  "description": "Request Duration",
  "unit": "ms",
  "data": {
    "data_points": [
      {
        "attributes": {},
        "start_time_unix_nano": 1762221636170274000,
        "time_unix_nano": 1762222165960946000,
        "count": 7,
        "sum": 752.070283897705,
        "bucket_counts": [0, 0, 0, 1, 0, 5, 0, 0],
        "min": 50.12562274932861,
        "max": 150.26040077209473
      }
    ],
    "explicit_bounds": [0.0, 20.0, 30.0, 60.0, 100.0, 250.0, 2000.0]
  }
}
```

Table: Example bucket sets and when to use them

| Bucket set (ms)                    | Typical use case                                                        |
| ---------------------------------- | ----------------------------------------------------------------------- |
| `[0, 5, 10, 25, 50, 75, 100, 250]` | Low-latency services where most requests are under 250ms                |
| `[0, 20, 30, 60, 100, 250, 2000]`  | Services with mixed latencies (quick endpoints and occasional long ops) |
| `[0, 100, 300, 1000, 3000, 10000]` | Latency-sensitive background jobs or APIs with long tails               |

Choose bucket boundaries that give you actionable visibility into the distribution of latency for your traffic patterns.

<Callout icon="lightbulb">
  When recording histogram values, ensure the recorded unit matches the histogram unit. This example records latencies in milliseconds because the histogram's `unit` is set to `"ms"`.
</Callout>

## Quick troubleshooting & tips

* If you see all observations falling into a single bucket, your boundaries likely don't match your observed latencies — widen or shift the buckets.
* Use attributes (e.g., `route`, `method`) to filter or split the histogram for more granular insights. For example:
  * `total_request_duration.record(latency_ms, {"route": request.path, "method": request.method})`
* For production, replace `ConsoleMetricExporter` with a metrics backend exporter (Prometheus, OTLP, etc.) appropriate to your observability stack.

## Links and references

* Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* OpenTelemetry Python Metrics: [https://opentelemetry.io/docs/instrumentation/python/metrics/](https://opentelemetry.io/docs/instrumentation/python/metrics/)
* OpenTelemetry SDK: [https://github.com/open-telemetry/opentelemetry-python](https://github.com/open-telemetry/opentelemetry-python)
* ConsoleMetricExporter (example used for local testing): [https://opentelemetry-python.readthedocs.io/](https://opentelemetry-python.readthedocs.io/)

This guide gives you a straightforward way to add histograms to your Flask app, select bucket boundaries that align with your service's performance, and surface useful latency distributions for troubleshooting and alerting.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/eab44858-b688-4e74-b600-1cfd59195020" />
</CardGroup>


# Demo Metrics Instrumentation

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Demo-Metrics-Instrumentation/page

Instrumenting a minimal Flask application with OpenTelemetry metrics, configuring a MeterProvider and exporters, creating instruments, recording requests, and validating local exports before production backends

In this lesson we'll instrument a minimal Flask application with OpenTelemetry metrics. The goal is to introduce metrics support incrementally:

* add and configure an OpenTelemetry MeterProvider,
* register a metrics reader and exporter,
* create metric instruments (counters, histograms, etc.),
* record metrics from request handlers,
* and validate exports locally (Console exporter) before moving to a production backend such as Prometheus.

Minimal Flask app
This is the starting point — a minimal Flask API that exposes a single GET endpoint at `/products`:

```python theme={null}
from flask import Flask

app = Flask(__name__)

@app.get("/products")
def get_products():
    return "Get All Products"

if __name__ == "__main__":
    app.run()
```

We will extend this application to collect and export metrics using OpenTelemetry.

Installation
Install the OpenTelemetry API and SDK for Python:

```bash theme={null}
pip install opentelemetry-api opentelemetry-sdk
```

You can verify the installed packages with:

```bash theme={null}
pip freeze
```

(Exact versions will vary by environment.)

Configure metrics
Encapsulate the OpenTelemetry setup in a `configure_meter()` helper. The function:

* creates a metric exporter (ConsoleMetricExporter for local testing),
* creates a metrics reader (PeriodicExportingMetricReader) that periodically exports metrics,
* builds a `MeterProvider` with the reader and a `Resource`,
* sets it as the global meter provider,
* and returns a `Meter` instance for creating instruments.

Example implementation (place this in `main.py` or in a separate module that you import):

```python theme={null}
