# Define metrics
REQUESTS = Counter('myapp_requests_total', 'Total HTTP requests')
IN_PROGRESS = Gauge('myapp_inprogress_requests', 'In-progress requests')
REQUEST_LATENCY = Histogram('myapp_request_duration_seconds', 'Request latency seconds')

# Start the metrics HTTP server on port 8000 (exposes /metrics)
start_http_server(8000)

def handle_request():
    REQUESTS.inc()
    IN_PROGRESS.inc()
    with REQUEST_LATENCY.time():
        # Simulate request processing
        sleep(random() * 0.5)
    IN_PROGRESS.dec()

if __name__ == '__main__':
    while True:
        handle_request()
        sleep(0.1)
```

Notes:

* In web frameworks (Flask, FastAPI, Django), you typically attach middleware or decorators that update metrics around each request.
* For production, use an appropriate host/port and avoid exposing `/metrics` to the public internet; use network policies or authentication as needed.

## Best practices for application instrumentation

* Name metrics clearly and consistently: use lowercase, underscores, and include units where applicable (e.g., `_seconds`, `_bytes`).
* Use labels sparingly to avoid high cardinality (many unique label combinations). Labels are great for dimensions like `method` or `status_code` but not for unbounded values (e.g., user IDs).
* Prefer histograms for latency distributions and calculating percentiles in Prometheus queries. Use summaries when you need client-side quantiles.
* Expose `/metrics` on a dedicated port or path, and secure access if it includes sensitive information.
* Document what each metric means and how it should be used in dashboards and alerts.

## Official client libraries (examples)

| Language family | Official client library |
| --------------- | ----------------------- |
| Go              | `client_golang`         |
| Java / Scala    | `client_java`           |
| Python          | `prometheus_client`     |
| Ruby            | `prometheus-client`     |

## Links and references

* [Prometheus: Instrumenting Applications](https://prometheus.io/docs/instrumenting/writing_clientlibs/)
* [prometheus\_client (Python) GitHub repository](https://github.com/prometheus/client_python)
* [Prometheus documentation: Exposition formats](https://prometheus.io/docs/instrumenting/exposition_formats/)
* [Prometheus best practices for naming metrics](https://prometheus.io/docs/practices/naming/)

In the next lesson we'll integrate these metrics into Prometheus scrape configuration and build a few example Grafana dashboards and alerts.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/0c0155c7-00c8-4ca2-a061-e66baa1a3216/lesson/761f13d4-68d6-45ca-87d4-db480fdc0204" />
</CardGroup>


# Labels

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Application-Instrumentation/Labels/page

Explains using Prometheus labels to track per-path and per-method HTTP request metrics, advantages over per-path metrics, aggregation examples, and warnings about label cardinality.

As your application grows to expose multiple endpoints—for example, endpoints for cars (`/cars`) and boats (`/boats`)—you may want both a global request count and per-path counts. Incrementing a single global counter for every endpoint tracks total traffic, but it doesn't tell you how that traffic is distributed across paths.

Example endpoints:

```python theme={null}
@app.get("/cars")
def get_cars():
    REQUESTS.inc()
    return ["toyota", "honda", "mazda", "lexus"]

@app.post("/cars")
def create_cars():
    REQUESTS.inc()
    return "Create Car"

@app.get("/boats")
def get_boats():
    REQUESTS.inc()
    return ["boat1", "boat2", "boat3"]

@app.post("/boats")
def create_boat():
    REQUESTS.inc()
    return "Create Boat"
```

If you want per-path totals, one naive solution is creating a distinct Counter for each path and incrementing the appropriate one:

```python theme={null}
from prometheus_client import Counter

CAR_REQUESTS = Counter(
    "requests_cars_total",
    "Total number of requests for /cars path"
)
BOATS_REQUESTS = Counter(
    "requests_boats_total",
    "Total number of requests for /boats path"
)

@app.get("/cars")
def get_cars():
    CAR_REQUESTS.inc()
    return ["toyota", "honda", "mazda", "lexus"]

@app.post("/cars")
def create_cars():
    CAR_REQUESTS.inc()
    return "Create Car"

@app.get("/boats")
def get_boats():
    BOATS_REQUESTS.inc()
    return ["boat1", "boat2", "boat3"]

@app.post("/boats")
def create_boat():
    BOATS_REQUESTS.inc()
    return "Create Boat"
```

This approach works, but it scales poorly. You end up with one metric name per path, making application-wide aggregations awkward: queries must reference every metric name and you must remember to update instrumentation whenever you add or remove endpoints. This increases maintenance overhead and makes queries error-prone.

A better practice is to use labels (also called dimensions). Define a single metric and add a `path` label at metric creation time. Then, when incrementing, provide the label value.

```python theme={null}
from prometheus_client import Counter

REQUESTS = Counter(
    "http_requests_total",
    "Total number of requests",
    ["path"]
)

@app.get("/cars")
def get_cars():
    REQUESTS.labels("/cars").inc()
    return ["toyota", "honda", "mazda", "lexus"]

@app.post("/cars")
def create_cars():
    REQUESTS.labels("/cars").inc()
    return "Create Car"

@app.get("/boats")
def get_boats():
    REQUESTS.labels("/boats").inc()
    return ["boat1", "boat2", "boat3"]

@app.post("/boats")
def create_boat():
    REQUESTS.labels("/boats").inc()
    return "Create Boat"
```

With this pattern, each distinct `path` value produces a separate time series under the same metric name `http_requests_total`. That makes filtering and aggregation simple and reliable.

<Frame>
  <img alt="The image shows a dark-themed command-line interface with a text input area and the label &#x22;Labels&#x22; at the top. There is a small icon of an eye on the bottom right." />
</Frame>

Prometheus will expose each labeled time series. For example:

```bash theme={null}
$ http_requests_total{path="/cars"}
http_requests_total{path="/cars"} 5.0

$ http_requests_total{path="/boats"}
http_requests_total{path="/boats"} 2.0
```

Listing the metric without selectors returns all label variations:

```bash theme={null}
$ http_requests_total
http_requests_total{path="/cars"} 5.0
http_requests_total{path="/boats"} 2.0
```

To compute the total across all paths use PromQL aggregation:

```bash theme={null}
$ sum(http_requests_total)
