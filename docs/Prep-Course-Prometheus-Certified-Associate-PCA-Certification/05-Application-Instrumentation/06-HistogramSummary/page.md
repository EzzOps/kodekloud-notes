# HistogramSummary

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Application-Instrumentation/HistogramSummary/page

How to instrument a Flask app with Prometheus histograms and summaries to measure and expose per-path per-method request latencies, customize buckets, and choose between histogram and summary

This guide shows how to instrument a Flask web application with Prometheus histogram and summary metrics to measure request latency per path and method. It walks through:

* Creating a histogram metric
* Recording per-request timings using Flask's `before_request` and `after_request` hooks
* Inspecting the generated Prometheus metrics (including default buckets)
* Customizing histogram buckets
* Using a summary metric and the Python-client limitation for quantiles

> **lightbulb** Tip: Use per-path and per-method labels to slice latency metrics in Prometheus and visualize percentiles in Grafana or another dashboard.

## Basic histogram example

Create a histogram metric and observe latency for each request. Place the timing logic in Flask's `before_request` and `after_request` hooks so every request is measured automatically.

```python theme={null}
from prometheus_client import Histogram, start_http_server
from flask import Flask, request
import time

app = Flask(__name__)

LATENCY = Histogram(
    'request_latency_seconds',
    'Request Latency',
    labelnames=['path', 'method']
)

def before_request():
    request.start_time = time.time()

def after_request(response):
    request_latency = time.time() - request.start_time
    LATENCY.labels(
        request.path,
        request.method
    ).observe(request_latency)
    return response

if __name__ == '__main__':
    start_http_server(8000)
    app.before_request(before_request)
    app.after_request(after_request)
    app.run()
```

How it works:

* `before_request()` records the timestamp when the request arrives (`time.time()`).
* `after_request()` computes the latency by subtracting the start time from the current time, then calls `observe()` on the histogram with the appropriate labels.
* `start_http_server(8000)` exposes metrics on port 8000 for Prometheus to scrape.

> **lightbulb** Note: You can store the `start_time` on the `request` object because Flask exposes a request-local proxy for each incoming request.

## Example metric output

When you scrape or query the histogram metric in Prometheus, the client creates buckets and count metrics. A scraped output may look like:

```plaintext theme={null}
