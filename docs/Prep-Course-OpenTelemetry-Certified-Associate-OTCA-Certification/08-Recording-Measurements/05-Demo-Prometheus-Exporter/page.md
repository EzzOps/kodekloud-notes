# main.py
from flask import Flask
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.metrics import set_meter_provider, get_meter_provider

def configure_meter(export_interval_millis: int = 5000):
    """
    Configure and install a MeterProvider that periodically exports metrics.

    Args:
        export_interval_millis: Export interval in milliseconds (default: 5000).

    Returns:
        opentelemetry.metrics.Meter: A Meter instance to create instruments.
    """
    # Export metrics to the console (useful for development/testing)
    exporter = ConsoleMetricExporter()

    # Periodically export metrics every `export_interval_millis` milliseconds
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=export_interval_millis)

    # Create a MeterProvider with the reader. You can add service attributes to the Resource.
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create({}))

    # Set this provider as the global provider so the rest of the app can access it
    set_meter_provider(provider)

    # Return a Meter instance to create instruments from.
    return get_meter_provider().get_meter(name="shopping-app", version="0.1.2")
```

Key components

| Component                     |                                                          Purpose | Example / Notes                                                        |
| ----------------------------- | ---------------------------------------------------------------: | ---------------------------------------------------------------------- |
| ConsoleMetricExporter         |           Sends metric data to stdout for quick local validation | Useful in development; not for production                              |
| PeriodicExportingMetricReader |        Periodically collects and forwards metrics to an exporter | `PeriodicExportingMetricReader(exporter, export_interval_millis=5000)` |
| MeterProvider                 |                 Central provider that manages meters and readers | `MeterProvider(metric_readers=[reader], resource=Resource.create({}))` |
| Resource                      | Describes the application/service (attributes like service.name) | `Resource.create({})` — replace with attributes as needed              |

Integrate with the Flask app
Call `configure_meter()` at application startup, then create instruments from the returned `meter`. Record metrics inside request handlers.

A compact `main.py` that includes the configuration and a counter instrument:

```python theme={null}
# main.py
from flask import Flask
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.metrics import set_meter_provider, get_meter_provider

def configure_meter(export_interval_millis: int = 5000):
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=export_interval_millis)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create({}))
    set_meter_provider(provider)
    return get_meter_provider().get_meter(name="shopping-app", version="0.1.2")

app = Flask(__name__)

# Configure metrics and obtain a Meter
meter = configure_meter()

# Create instruments from the meter
request_counter = meter.create_counter(
    "shopping_requests",
    description="Number of requests received by the shopping API"
)

@app.get("/products")
def get_products():
    # Increment request counter by 1 for each GET /products call
    request_counter.add(1, {"endpoint": "/products", "method": "GET"})
    return "Get All Products"

if __name__ == "__main__":
    app.run()
```

Tips and best practices

> **lightbulb** Use attributes (labels) on metric recordings to slice metrics by endpoint, HTTP method, status code, or other dimensions. For production, add meaningful `Resource` attributes such as `service.name`, `service.version`, and environment tags.

Running the app
Start the application:

```bash theme={null}
python main.py
```

Typical Flask output:

```plaintext theme={null}
 * Serving Flask app 'main'
 * Debug mode off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000/
Press CTRL+C to quit
```

While the app runs, the `PeriodicExportingMetricReader` will invoke the `ConsoleMetricExporter` at the configured interval (default 5 seconds). You should see exported metric lines printed to stdout when metrics have been recorded.

Warnings

> **warning** ConsoleMetricExporter and Flask's built-in development server are intended for local development and testing only. For production, use a proper exporter (e.g., OTLP or Prometheus exporter) and a production WSGI server such as Gunicorn or uWSGI.

Next steps

* Add more instruments: histograms for request latency, up-down counters for in-flight requests, or observable instruments.
* Export to production backends:
  * Prometheus: use the Prometheus exporter/agent to scrape metrics.
  * OTLP: send metrics to an OpenTelemetry Collector and then route to your backend.
* Enrich `Resource.create({})` with metadata such as:
  * `service.name`, `service.instance.id`, `service.version`.

Links and references

* OpenTelemetry Python Metrics: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* Prometheus: [https://prometheus.io](https://prometheus.io)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

This guide gives you a minimal, reproducible path from a simple Flask app to basic OpenTelemetry metrics collection and local export. From here you can extend the instrumentation and switch exporters to match your observability stack.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/97b726bd-9938-4032-b79d-d3e25123d237)


# Demo Prometheus Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Demo-Prometheus-Exporter/page

Guide demonstrating how to expose OpenTelemetry metrics to Prometheus from a Flask app by running a metrics server, configuring PrometheusMetricReader, and registering counters gauges and histograms.

So far in this lesson we've used the console metric exporter for quick debugging and learning. In production, you’ll usually expose metrics to a backend such as Prometheus so you can centralize scraping, alerting, and long-term storage.

Prometheus uses a pull model: your application runs a small HTTP endpoint (commonly `/metrics`) and Prometheus (or a collector) scrapes that endpoint via HTTP GET on a schedule.

> **lightbulb** [Prometheus](https://prometheus.io/) scrapes metrics by pulling them from your application. To integrate with Prometheus you run a small HTTP server in your app that serves the `/metrics` endpoint (the [Prometheus client library](https://github.com/prometheus/client_python) provides this for you).

This guide shows how to configure OpenTelemetry to expose metrics via the Prometheus exporter, create a few instruments, and hook everything into a Flask app.

## What you’ll set up

* Start a Prometheus-compatible metrics server inside your app (so Prometheus can scrape `/metrics`).
* Configure the OpenTelemetry `PrometheusMetricReader`.
* Register counters, gauges, and a histogram (with explicit buckets).
* Expose application endpoints (Flask) and record metrics on request lifecycle hooks.

## Prerequisites

Install the Prometheus exporter and the Prometheus client:

```bash theme={null}
pip install opentelemetry-exporter-prometheus prometheus-client
```

## Full example: Flask + OpenTelemetry + Prometheus

Save the following as `main.py`. It contains imports, configuration, a small Flask app, and the instruments used by the application:

```python theme={null}
