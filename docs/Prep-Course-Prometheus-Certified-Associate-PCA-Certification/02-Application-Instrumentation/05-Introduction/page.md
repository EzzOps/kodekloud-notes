# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 77.0
python_gc_collections_total{generation="1"} 7.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="5",version="3.9.5"} 1.0
# HELP http_requests_total Total number of requests
# TYPE http_requests_total counter
http_requests_total 5.0
# HELP http_requests_created Total number of requests
# TYPE http_requests_created gauge
http_requests_created 1.6654499091926205e+09
```

## Expose metrics via Flask (same port)

If you prefer to expose metrics on the same port as your Flask app (e.g., at `http://localhost:5001/metrics`), use the WSGI helper `make_wsgi_app` and `DispatcherMiddleware` from `werkzeug`:

```python theme={null}
from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Add Prometheus middleware to export metrics at /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

if __name__ == "__main__":
    app.run(port=5001)
```

This makes the Prometheus metrics available at `http://localhost:5001/metrics`. Use whichever approach fits your deployment model: a separate metrics server (good for simple setups) or WSGI middleware (keeps everything on one port).

## Multi-route application and counting across all endpoints

Let's expand the app with additional endpoints and show two ways to ensure `http_requests_total` counts requests across your entire application.

1. Manual increments in each handler:

```python theme={null}
from flask import Flask
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

REQUESTS = Counter("http_requests_total", "Total number of requests")

app = Flask(__name__)

# Expose metrics at /metrics on the same Flask port
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

@app.get("/cars")
def get_cars():
    REQUESTS.inc()
    return ["toyota", "honda", "mazda", "lexus"]

@app.get("/cars/<int:id>")
def get_car(id):
    REQUESTS.inc()
    return f"Single car {id}"

@app.post("/cars")
def create_car():
    REQUESTS.inc()
    return "Create Car"

@app.patch("/cars/<int:id>")
def update_car(id):
    REQUESTS.inc()
    return f"Updating Car {id}"

@app.delete("/cars/<int:id>")
def delete_car(id):
    REQUESTS.inc()
    return f"Deleting Car {id}"

if __name__ == "__main__":
    app.run(port=5001)
```

2. Increment once for every incoming request using a global hook (recommended to avoid repeating increments). If you expose metrics at `"/metrics"` via the same Flask app (for example, if `/metrics` is handled by Flask), make sure you do not count requests to `/metrics` itself. If you mount the Prometheus WSGI app via `DispatcherMiddleware`, requests to `/metrics` are handled by the metrics WSGI app and won't trigger Flask `before_request` hooks:

```python theme={null}
from flask import Flask, request
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

REQUESTS = Counter("http_requests_total", "Total number of requests")

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

@app.before_request
def increment_request_counter():
    # Avoid counting the /metrics endpoint itself
    if request.path != "/metrics":
        REQUESTS.inc()

@app.get("/cars")
def get_cars():
    return ["toyota", "honda", "mazda", "lexus"]

@app.get("/cars/<int:id>")
def get_car(id):
    return f"Single car {id}"

@app.post("/cars")
def create_car():
    return "Create Car"

@app.patch("/cars/<int:id>")
def update_car(id):
    return f"Updating Car {id}"

@app.delete("/cars/<int:id>")
def delete_car(id):
    return f"Deleting Car {id}"

if __name__ == "__main__":
    app.run(port=5001)
```

## Callouts

<Callout icon="lightbulb">
  If you use `start_http_server`, the metrics endpoint is a separate HTTP server (different port) and will not be handled by Flask middleware or Flask hooks like `before_request`. If you want metrics to be part of the same Flask process and port, use `make_wsgi_app` with `DispatcherMiddleware`.
</Callout>

<Callout icon="warning">
  If you expose metrics at `"/metrics"` on the same Flask app, ensure you do not inadvertently count `/metrics` requests in your application metrics unless that is intentional.
</Callout>

## Summary

* Create and register Prometheus metrics (e.g., `Counter`, `Gauge`, `Histogram`) using `prometheus_client`.
* Increment metrics where appropriate (inside handlers, or globally via `before_request`).
* Expose metrics either with `start_http_server` (separate port) or with `make_wsgi_app` + `DispatcherMiddleware` (same port at `"/metrics"`).
* Avoid double-counting metrics (for example, counting scrapes of the `/metrics` endpoint itself).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/0c0155c7-00c8-4ca2-a061-e66baa1a3216/lesson/f79526d0-2745-40a9-ab84-5b8a9acaab25" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Application-Instrumentation/Introduction/page

Explains how to instrument applications with Prometheus client libraries, metric types, Python examples, exposing metrics endpoint and best practices for naming, labels, and latency measurement

We've already set up Prometheus to collect metrics from our infrastructure — from servers (Linux or Windows) to Docker containers and the Docker Engine. But to understand how your application behaves in production, you should instrument the application code itself so it can expose internal metrics (requests, latencies, errors, resource usage, etc.) in a format Prometheus can scrape.

This is the role of Prometheus client libraries.

<Frame>
  <img alt="The image illustrates a network diagram showing instrumentation with Prometheus collecting data from multiple servers, each associated with Python scripts." />
</Frame>

A Prometheus client library makes it straightforward to instrument application code so it produces metrics Prometheus understands. In practice, a client library performs two core functions:

* It provides metric types (counters, gauges, histograms, summaries) and APIs to record values from your code.
* It exposes those metrics in the Prometheus exposition format via an HTTP endpoint (commonly `GET /metrics`) so Prometheus can scrape them.

Prometheus maintains official client libraries for several widely used languages and many community libraries for other environments. If your language isn't supported or you want a lightweight integration, you can implement the exposition format yourself.

<Frame>
  <img alt="The image lists official and unofficial client libraries for Prometheus. Official libraries are for Go, Java/Scala, Python, Ruby, and unofficial ones include languages like Bash, C++, Dart, and more." />
</Frame>

<Callout icon="lightbulb">
  Focus on what metrics you capture and how you expose them, not the specifics of the language. The concepts (counters, gauges, histograms/summaries, and the `/metrics` endpoint) apply across languages and frameworks.
</Callout>

In the sections below, we demonstrate how to instrument a Python-based API so you can track and expose essential application metrics. The concepts translate directly to other languages supported by Prometheus client libraries.

## Key Prometheus metric types

| Metric type | Purpose                                                                                  | Typical name example                    |
| ----------- | ---------------------------------------------------------------------------------------- | --------------------------------------- |
| Counter     | Monotonically increasing value for counting events (e.g., requests served)               | `myapp_requests_total`                  |
| Gauge       | Value that can go up and down (e.g., concurrent sessions, memory usage)                  | `myapp_active_sessions`                 |
| Histogram   | Buckets request/latency distributions for quantiles/percentiles and sum/count            | `myapp_request_duration_seconds_bucket` |
| Summary     | Directly observes quantiles for latency (client libraries may differ in recommended use) | `myapp_request_duration_seconds`        |

## Quick Python instrumentation example

Below is a compact example showing common patterns when instrumenting a Python web API with the `prometheus_client` library:

* Define metrics (counter, gauge, histogram)
* Increment/observe metrics in your request handlers
* Expose metrics via an HTTP endpoint (e.g., `GET /metrics`) so Prometheus can scrape them

```python theme={null}
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from time import sleep
from random import random
