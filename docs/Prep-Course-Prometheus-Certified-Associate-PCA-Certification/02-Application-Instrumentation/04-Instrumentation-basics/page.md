# HELP request_latency_seconds Request Latency
# TYPE request_latency_seconds histogram
request_latency_seconds_bucket{le="0.005",method="GET",path="/cars"} 0.0
request_latency_seconds_bucket{le="0.01",method="GET",path="/cars"} 0.0
request_latency_seconds_bucket{le="0.025",method="GET",path="/cars"} 0.0
request_latency_seconds_bucket{le="0.05",method="GET",path="/cars"} 1.0
request_latency_seconds_bucket{le="0.075",method="GET",path="/cars"} 3.0
request_latency_seconds_bucket{le="0.1",method="GET",path="/cars"} 3.0
request_latency_seconds_bucket{le="0.25",method="GET",path="/cars"} 4.0
request_latency_seconds_bucket{le="0.5",method="GET",path="/cars"} 6.0
request_latency_seconds_bucket{le="0.75",method="GET",path="/cars"} 6.0
request_latency_seconds_bucket{le="1.0",method="GET",path="/cars"} 8.0
request_latency_seconds_bucket{le="2.5",method="GET",path="/cars"} 8.0
request_latency_seconds_bucket{le="5.0",method="GET",path="/cars"} 8.0
request_latency_seconds_bucket{le="7.5",method="GET",path="/cars"} 8.0
request_latency_seconds_bucket{le="10.0",method="GET",path="/cars"} 8.0
request_latency_seconds_bucket{le="+Inf",method="GET",path="/cars"} 8.0
request_latency_seconds_count{method="GET",path="/cars"} 8.0
request_latency_seconds_sum{method="GET",path="/cars"} 1.234
```

The client provides helpful default buckets suitable for many web applications, but you will often want to customize them.

## Customizing histogram buckets

To change bucket boundaries, pass the `buckets` parameter when you instantiate the `Histogram`. For low-latency, high-resolution needs, provide a list of bucket upper bounds:

```python theme={null}
LATENCY = Histogram(
    'request_latency_seconds',
    'Flask Request Latency',
    labelnames=['path', 'method'],
    buckets=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
)
```

Adjust buckets to match the latency distribution of your application. Use finer buckets for low latency applications and wider buckets for higher-latency systems.

## Using a Summary metric

A `Summary` records observed values and can calculate configurable quantiles (in some client libraries). The usage pattern is almost identical to a `Histogram`: create the metric and call `.observe()` with the measured latency.

```python theme={null}
from prometheus_client import Summary

LATENCY_SUMMARY = Summary(
    'request_latency_seconds',
    'Flask Request Latency',
    labelnames=['path', 'method']
)

# Later, in your after_request:
LATENCY_SUMMARY.labels(request.path, request.method).observe(request_latency)
```

<Callout icon="warning">
  Warning: The Python Prometheus client does not implement configurable quantiles for Summary metrics the same way some other language clients do. If you need server-side quantiles, prefer Histograms and compute quantiles in Prometheus (e.g., `histogram_quantile()`), or check the client library updates for support in your language.
</Callout>

## Histogram vs Summary — quick comparison

| Metric Type | Use Case                                                                                              | Notes                                                                                                               |
| ----------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Histogram   | Ideal for calculating quantiles in Prometheus (via `histogram_quantile`) and exposing bucketed counts | You must choose buckets; Prometheus can compute quantiles from buckets                                              |
| Summary     | Records quantiles and sum/count on the client side                                                    | Some client libraries (like Python) lack configurable quantiles; server-side quantile calculation may be preferable |

## Links and references

* [Prometheus Python client](https://github.com/prometheus/client_python)
* [PromQL histogram\_quantile()](https://prometheus.[SECRET_REDACTED]/#histogram_quantile)
* [Flask request lifecycle (before\_request/after\_request)](https://flask.palletsprojects.com/en/latest/api/#flask.Flask.before_request)

Use the examples above to add latency instrumentation to your Flask app, tune bucket boundaries to your observed latency distribution, and choose between Histogram and Summary depending on your quantile needs and client library support.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/0c0155c7-00c8-4ca2-a061-e66baa1a3216/lesson/3b52f98d-3825-4cfd-8293-5902005dd533" />
</CardGroup>


# Instrumentation basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Application-Instrumentation/Instrumentation-basics/page

Guide to adding Prometheus metrics to a Flask application, creating counters, exposing metrics via separate server or WSGI middleware, and counting requests safely.

In this lesson/article we'll build a small dummy application and walk through how to add Prometheus instrumentation. We'll use Flask (a lightweight Python web framework) to create a few endpoints and then add metrics using the `prometheus_client` library.

## Minimal Flask app

Here is a minimal Flask app that exposes a single GET endpoint at `"/cars"`:

```python theme={null}
from flask import Flask

app = Flask(__name__)

@app.get("/cars")
def get_cars():
    return ["toyota", "honda", "mazda", "lexus"]

if __name__ == "__main__":
    app.run(port=5001)
```

Focus on the decorator `@app.get("/cars")`: any GET request to `"/cars"` will execute the `get_cars` function. The app is started on port `5001`.

## Install the Prometheus client

Install the Python client library:

```bash theme={null}
pip install prometheus_client
```

## Add a Counter metric

Import and create a Prometheus `Counter` to track total requests:

```python theme={null}
from prometheus_client import Counter

REQUESTS = Counter("http_requests_total", "Total number of requests")
```

## Increment the counter in a handler

Increment the counter inside the request handler so it increases on every request:

```python theme={null}
from flask import Flask
from prometheus_client import Counter

REQUESTS = Counter("http_requests_total", "Total number of requests")

app = Flask(__name__)

@app.get("/cars")
def get_cars():
    REQUESTS.inc()
    return ["toyota", "honda", "mazda", "lexus"]

if __name__ == "__main__":
    app.run(port=5001)
```

## Expose metrics with a separate HTTP server

The simplest way to expose metrics is to use `start_http_server` from the Prometheus client. This starts a separate HTTP server that serves all registered metrics (including the default Python metrics):

```python theme={null}
from prometheus_client import Counter, start_http_server
from flask import Flask

REQUESTS = Counter("http_requests_total", "Total number of requests")

app = Flask(__name__)

@app.get("/cars")
def get_cars():
    REQUESTS.inc()
    return ["toyota", "honda", "mazda", "lexus"]

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    # Start Flask app on port 5001
    app.run(port=5001)
```

When run this way:

* Flask App: port `5001`
* Prometheus metrics endpoint: port `8000`

You can fetch the metrics with curl:

```plaintext theme={null}
$ curl 127.0.0.1:8000
