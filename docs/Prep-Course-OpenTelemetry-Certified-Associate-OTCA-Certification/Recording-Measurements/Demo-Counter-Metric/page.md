# main.py
import os
import time

import psutil
from flask import Flask, request

from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

# --- Metric provider / exporter setup ---
exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
resource = Resource.create({
    "telemetry.sdk.language": "python",
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.version": "1.37.0",
    "service.name": "shopping-app"
})
provider = MeterProvider(metric_readers=[reader], resource=resource)
set_meter_provider(provider)
meter = get_meter_provider().get_meter(name="shopping-app", version="0.1.2")

# --- Synchronous metrics (example) ---
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

# --- Observable gauge (polled) for memory usage ---
process = psutil.Process(os.getpid())

def memory_usage_callback(options):
    """
    This callback will be called periodically by the metric reader.
    It must return an iterable of Observation objects or (value, attributes) tuples.
    Each observation holds a numeric value and optional attributes.
    """
    mem_info = process.memory_info()  # returns an object with rss and vms (and more)
    observations = [
        (mem_info.rss, {"type": "rss"}),  # resident set size (bytes)
        (mem_info.vms, {"type": "vms"}),  # virtual memory size (bytes)
    ]
    return observations

meter.create_observable_gauge(
    "application_memory_usage",
    description="Memory usage of application",
    unit="By",
    callbacks=[memory_usage_callback]
)

# --- Flask app (example endpoints) ---
app = Flask(__name__)

@app.before_request
def before_request():
    concurrent_requests.add(1)

@app.after_request
def after_request(response):
    concurrent_requests.add(-1)
    return response

@app.get("/products")
def get_products():
    requests_counter.add(1, {"route": "/products", "method": request.method})
    # Simulate some work
    time.sleep(1)
    return "Get All Products"

@app.get("/products/<int:id>")
def get_product(id):
    requests_counter.add(1, {"route": "/products/<id>", "method": request.method})
    return f"Get product {id}"

if __name__ == "__main__":
    app.run()
```

Install psutil (used to read the process memory):

```bash theme={null}
pip install psutil
```

### Example console-exported metric snapshot

The ConsoleMetricExporter prints resource and scope metrics as JSON-like structures. With the periodic reader configured to 5000 ms, the observable gauge will be polled every 5 seconds and you will see observations for `rss` and `vms` within the exported metrics.

```json theme={null}
{
  "resource_metrics": [
    {
      "resource": {
        "attributes": {
          "telemetry.sdk.language": "python",
          "telemetry.sdk.name": "opentelemetry",
          "telemetry.sdk.version": "1.37.0",
          "service.name": "shopping-app"
        }
      },
      "schema_url": "",
      "scope_metrics": [
        {
          "scope": {
            "name": "shopping-app",
            "version": "0.1.2"
          },
          "metrics": [
            {
              "name": "application_memory_usage",
              "description": "Memory usage of application",
              "unit": "By",
              "data_points": [
                { "value": 34526720, "attributes": { "type": "rss" } },
                { "value": 12163456, "attributes": { "type": "vms" } }
              ]
            },
            {
              "name": "http_requests_total",
              "data_points": [ /* ... */ ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Quick reference: metric types and when to use them

| Metric Type      | Use Case                                               | When to use                                           |
| ---------------- | ------------------------------------------------------ | ----------------------------------------------------- |
| Counter          | Monotonic counts of events                             | `http_requests_total` (increment on each request)     |
| Up-down counter  | Values you explicitly increase/decrease in code        | `concurrent_requests` (add 1 / add -1)                |
| Observable gauge | Polled values that can increase/decrease independently | `application_memory_usage` (RSS/VMS polled by psutil) |

## Notes and best practices

* Use `rss` (resident set size) to monitor actual memory resident in RAM. Use `vms` to inspect the total virtual address space requested by the process.
* The callback receives an `options` parameter (not used in this example). Always return an iterable (e.g., a list) of Observation objects or `(value, attributes)` tuples.
* The periodic exporter polls your observable callbacks at the configured interval (5 seconds in this example).
* For production, run behind a proper WSGI server (e.g., Gunicorn, uWSGI) and replace the ConsoleMetricExporter with a production-ready exporter such as OTLP.

<Callout icon="warning">
  Do not use Flask's development server in production. Configure a production WSGI server and a proper exporter (e.g., OTLP) for reliable metric delivery and performance.
</Callout>

## Links and references

* OpenTelemetry Python metrics: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* OpenTelemetry metrics SDK: [https://opentelemetry.io/docs/reference/specification/metrics/](https://opentelemetry.io/docs/reference/specification/metrics/)
* psutil (process utilities for Python): [https://pypi.org/project/psutil/](https://pypi.org/project/psutil/)
* Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* OTLP exporter information: [https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/protocol/otlp](https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/protocol/otlp)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/e7a4e55e-dafc-4c51-b19f-f20e08b0eaee" />
</CardGroup>


# Demo Counter Metric

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Demo-Counter-Metric/page

Demonstrates instrumenting a Flask app with an OpenTelemetry Counter to count HTTP requests, add route and method attributes, and centralize counting via a before_request hook.

In this lesson you'll instrument a simple Flask app with an OpenTelemetry Counter metric to track how many HTTP requests your application processes. The guide covers:

* configuring an OpenTelemetry MeterProvider with a console exporter and periodic reader,
* creating a Counter metric,
* incrementing the counter on incoming requests,
* adding attributes to break metrics down by route and method,
* centralizing instrumentation using a `before_request` hook.

This is intended for development and testing. For production, use a production-ready WSGI server (examples in References).

<Callout icon="lightbulb">
  This example uses the `ConsoleMetricExporter` with a `PeriodicExportingMetricReader` configured for a 5s export interval so you can see metrics printed to the console while testing.
</Callout>

<Callout icon="warning">
  The Flask development server is not suitable for production. Use a production WSGI server such as `gunicorn` or `uwsgi` for deployments.
</Callout>

## 1. Configure the meter and console exporter

Create a function to configure the MeterProvider and attach a periodic exporting reader that prints metrics every 5 seconds. Then get a named meter for your application:

```python theme={null}
