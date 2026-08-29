# main.py
import time
import random
from flask import Flask, request

from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

app = Flask(__name__)

def configure_meter():
    # Start an HTTP server to expose Prometheus metrics (port 8000 on localhost).
    # Prometheus will scrape this endpoint (e.g., http://localhost:8000/metrics).
    start_http_server(port=8000, addr="localhost")

    # Use the PrometheusMetricReader so metrics are available to Prometheus.
    reader = PrometheusMetricReader()

    # Histogram bucket boundaries are in milliseconds in this example.
    buckets = [0.0, 20, 30, 60, 100, 250, 2000]
    view = View(
        instrument_name="total_request_duration",
        aggregation=ExplicitBucketHistogramAggregation(boundaries=buckets),
    )

    provider = MeterProvider(metric_readers=[reader], resource=Resource.create(), views=[view])
    set_meter_provider(provider)

    # Return a meter for use by the application
    return get_meter_provider().get_meter(name="shopping-app", version="0.1.2")

meter = configure_meter()

# Create instruments
requests_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of requests processed by the application",
)
concurrent_requests = meter.create_up_down_counter(
    name="concurrent_requests",
    description="Total number of requests in progress",
)
total_request_duration = meter.create_histogram(
    name="total_request_duration",
    description="Request Duration",
    unit="ms",
)

# Flask request hooks to record metrics
@app.before_request
def before_request():
    request.start_time = time.time()
    concurrent_requests.add(1)

@app.after_request
def after_request(response):
    # Convert latency to milliseconds
    request_latency_ms = (time.time() - request.start_time) * 1000
    concurrent_requests.add(-1)
    total_request_duration.record(request_latency_ms)
    return response

@app.get("/products")
def get_products():
    requests_counter.add(1, {"route": "/products", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return "Get All Products"

@app.get("/products/<int:id>")
def get_product(id):
    requests_counter.add(1, {"route": "/products/<id>", "method": request.method})
    time.sleep(random.uniform(0.05, 1.5))
    return f"Getting product detail {id}"

if __name__ == "__main__":
    # Start the Flask app on port 5000
    app.run(host="0.0.0.0", port=5000)
```

<Callout icon="warning">
  If you want Prometheus (running on another host or in a container) to scrape your app, bind the metrics server to an address accessible to Prometheus. In the example above `start_http_server(port=8000, addr="localhost")` binds to `localhost`—change to `0.0.0.0` or the appropriate host if external scraping is required.
</Callout>

## Key parts explained

| Component                 |                                             Purpose | Example / Notes                                                                 |
| ------------------------- | --------------------------------------------------: | ------------------------------------------------------------------------------- |
| Prometheus metrics server |         Exposes `/metrics` for Prometheus to scrape | `start_http_server(port=8000, addr="localhost")`                                |
| Metric Reader             | Makes OpenTelemetry metrics available to Prometheus | `PrometheusMetricReader()`                                                      |
| Views & Aggregation       |               Apply bucket boundaries to histograms | `View(..., aggregation=ExplicitBucketHistogramAggregation(boundaries=buckets))` |
| Instruments               |     Counters, gauges and histograms used by the app | `http_requests_total`, `concurrent_requests`, `total_request_duration`          |

Notes on the example:

* `start_http_server(port=8000, addr="localhost")` (from the Prometheus client library) serves metrics at `http://localhost:8000/metrics`.
* `PrometheusMetricReader()` bridges OpenTelemetry metrics to the Prometheus client server.
* The `View` with `ExplicitBucketHistogramAggregation` configures histogram bucket boundaries for `total_request_duration` (milliseconds).

## Exercise the application and inspect metrics

1. Start the Flask app:
   ```bash theme={null}
   python main.py
   ```

2. Send a few requests to the Flask app (port 5000):
   ```bash theme={null}
   curl 127.0.0.1:5000/products
   curl 127.0.0.1:5000/products
   curl 127.0.0.1:5000/products
   ```

3. Request the metrics endpoint exposed for Prometheus (port 8000):
   ```bash theme={null}
   curl localhost:8000/metrics
   ```

You should see Prometheus-formatted metrics similar to the excerpt below:

```text theme={null}
# HELP concurrent_requests Total number of requests in progress
# TYPE concurrent_requests gauge
concurrent_requests 0.0

# HELP http_requests_total Total number of requests processed by the application
# TYPE http_requests_total counter
http_requests_total{method="GET",route="/products"} 3.0

# HELP total_request_duration_milliseconds Request Duration
# TYPE total_request_duration_milliseconds histogram
total_request_duration_milliseconds_bucket{le="0.0"} 0.0
total_request_duration_milliseconds_bucket{le="20.0"} 1.0
total_request_duration_milliseconds_bucket{le="30.0"} 2.0
total_request_duration_milliseconds_bucket{le="60.0"} 3.0
total_request_duration_milliseconds_bucket{le="100.0"} 3.0
total_request_duration_milliseconds_bucket{le="250.0"} 3.0
total_request_duration_milliseconds_bucket{le="2000.0"} 3.0
total_request_duration_milliseconds_count 3.0
total_request_duration_milliseconds_sum 214.5
```

This output shows:

* Runtime and Python default metrics (if enabled),
* Your application counters and gauge (`http_requests_total`, `concurrent_requests`),
* Histogram buckets, count, and sum for `total_request_duration` (milliseconds).

## Summary

To expose OpenTelemetry metrics to Prometheus:

1. Start a Prometheus-compatible metrics server in your app (`prometheus_client.start_http_server`).
2. Configure `PrometheusMetricReader` with your MeterProvider (and views for histograms).
3. Register counters / gauges / histograms and record metrics via request hooks or application code.
4. Point Prometheus to the app's `/metrics` endpoint (or use a scraping sidecar / collector).

## Links and References

* [Prometheus](https://prometheus.io/)
* [OpenTelemetry](https://opentelemetry.io/)
* [opentelemetry-exporter-prometheus (PyPI)](https://pypi.org/project/opentelemetry-exporter-prometheus)
* [Prometheus Python client library](https://github.com/prometheus/client_python)
* [Flask Documentation](https://flask.palletsprojects.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/6c005157-aba9-4784-ac50-c6334944bf94" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/5289ccef-8df6-436a-912b-bdd4e993b218" />
</CardGroup>


# Demo Updown Counter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Demo-Updown-Counter/page

Explains adding an up down counter to Flask using OpenTelemetry to track concurrent in-progress requests alongside a cumulative requests counter

Previously we added a cumulative request counter to measure the total number of requests handled by an application and broke it down by attributes such as route and method. In this article we'll add a second metric to track how many requests are actively being processed at any given moment — i.e., concurrent in-progress requests.

Goals

* Keep the cumulative total requests metric (`http_requests_total`).
* Add a metric that represents the number of concurrent requests currently being processed (a value that can increase and decrease).

Why a different metric type is needed
A traditional counter only increases, which is ideal for cumulative totals. To represent in-progress concurrency — a value that should increment when a request starts and decrement when it finishes — we need a metric type that can go up and down.

Compare the options:

| Metric type     | Behavior                                           | When to use                                                                              |
| --------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Counter         | Monotonic (only increases)                         | Total number of events processed (e.g., requests completed).                             |
| Gauge           | Arbitrary instantaneous value                      | Point-in-time measurements that aren't relative to previous values (e.g., memory usage). |
| Up-down counter | Increment and decrement relative to previous value | Active/in-progress counts that should rise and fall (e.g., concurrent requests).         |

<Callout icon="lightbulb">
  For tracking concurrent requests, an up-down counter is the preferred choice because its value moves up and down relative to the previous state.
</Callout>

Complete Flask example

* Configures a MeterProvider with a console exporter.
* Creates a cumulative `http_requests_total` counter (incremented when responses are sent).
* Creates a `concurrent_requests` up-down counter (incremented at request start, decremented after response).
* Uses Flask `before_request` and `after_request` hooks to manage the concurrent counter.
* Adds a slow route to let you observe concurrent requests.

```python theme={null}
