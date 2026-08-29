# Gauge

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Application-Instrumentation/Gauge/page

Explains Prometheus Gauge metric type, usage patterns, Python prometheus_client examples, API methods and best practices for tracking fluctuating values like in‑progress requests

In this lesson we wrap up with Prometheus' final core metric type: the Gauge. A Gauge records a single numerical value that can go up and down over time, which makes it ideal for tracking quantities that fluctuate — for example, the number of active requests currently being processed by an application.

Key use cases:

* Current number of in-progress requests
* Free memory, queue length, or number of running jobs
* Resource values that both increase and decrease

See Prometheus docs: [Gauge metric type](https://prometheus.io/docs/concepts/metric_types/#gauge).

Example: tracking in-progress requests with the Python prometheus\_client

* Important: the order of `labelnames` must match the order of values passed to `.labels(...)`. In this example we define `['method', 'path']` and call `.labels(request.method, request.path)`.

```python theme={null}
from prometheus_client import Gauge
import time
from flask import request

IN_PROGRESS = Gauge(
    'inprogress_requests',
    'Total number of requests in progress',
    labelnames=['method', 'path']
)

def before_request():
    # increment when a request starts
    IN_PROGRESS.labels(request.method, request.path).inc()
    request.start_time = time.time()

def after_request(response):
    # decrement when a request finishes
    IN_PROGRESS.labels(request.method, request.path).dec()
    return response
```

The Gauge API highlights:

* `inc()` — increment the gauge by 1 (or a specified amount)
* `dec()` — decrement the gauge by 1 (or a specified amount)
* `set(value)` — explicitly set the gauge to `value`

> **lightbulb** Ensure every `inc()` is paired with a corresponding `dec()` (even when errors occur). In frameworks like [Flask](https://flask.palletsprojects.com/), prefer `teardown_request`, middleware, or a `try/finally` block around request handling so the gauge is always decremented when a request finishes.

Robust pattern using try/finally inside a handler:

```python theme={null}
def handle_request():
    IN_PROGRESS.labels(request.method, request.path).inc()
    try:
        # process the request...
        pass
    finally:
        IN_PROGRESS.labels(request.method, request.path).dec()
```

When exposed by your metrics endpoint, the gauge shows the current value per label combination. Example output:

```bash theme={null}
inprogress_requests{method="GET",path="/cars"} 3.0
inprogress_requests{method="POST",path="/cars"} 0.0
inprogress_requests{method="POST",path="/boats"} 18.0
inprogress_requests{method="GET",path="/boats"} 7.0
```

Gauge vs Counter — quick comparison

| Metric Type | Use Case                              | Behavior                                      | Example                   |
| ----------- | ------------------------------------- | --------------------------------------------- | ------------------------- |
| Gauge       | Current value that can go up and down | Supports `inc()`, `dec()`, and `set()`        | Number of active requests |
| Counter     | Cumulative values that only increase  | Only `inc()` (and `reset` on process restart) | Total requests served     |

Additional guidance

* Use a Gauge when you need an up-and-down metric (active jobs, queue length, free resources).
* For request duration or size distributions, prefer `Histogram` or `Summary`.
* Label cardinality: avoid high-cardinality label values (e.g., raw user IDs or long paths) to prevent memory blowups in the Prometheus server.

Links and references

* [Prometheus: Gauge metric type](https://prometheus.io/docs/concepts/metric_types/#gauge)
* [Prometheus: Counter metric type](https://prometheus.io/docs/concepts/metric_types/#counter)
* [Flask documentation](https://flask.palletsprojects.com/)

> **warning** Never allow unpaired increments. Missing decrements will inflate your gauge and produce misleading monitoring alerts. Implement error paths and teardown hooks to guarantee balanced `inc()`/`dec()` calls.

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/0c0155c7-00c8-4ca2-a061-e66baa1a3216/lesson/060795c9-183c-4239-8e3b-ec458de2780e)
