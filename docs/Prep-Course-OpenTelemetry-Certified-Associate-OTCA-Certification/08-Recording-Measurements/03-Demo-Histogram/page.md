# main.py
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
```

This returns a meter named `shopping-app` which you'll use to create instruments.

## 2. Create a Counter metric

A Counter is appropriate for values that only increase over time (like request counts). Create a Counter and store it:

```python theme={null}
requests_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of requests processed by the application",
    unit="1"  # dimensionless count
)
```

Use unit strings like `"1"` for counts, `"By"` for bytes, or `"s"` for seconds when appropriate.

## 3. Instrument routes by incrementing the counter

A simple approach is to call `requests_counter.add(1)` in every route handler. Example handlers:

```python theme={null}
app = Flask(__name__)

@app.get("/products")
def get_products():
    requests_counter.add(1)
    return "Get All Products"

@app.get("/products/<int:id>")
def get_product(id):
    requests_counter.add(1)
    return "Getting product detail"

@app.post("/products")
def create_product():
    requests_counter.add(1)
    return "Creating Products"

@app.patch("/products/<int:id>")
def update_product(id):
    requests_counter.add(1)
    return "Updating Product"

@app.delete("/products/<int:id>")
def delete_product(id):
    requests_counter.add(1)
    return "Deleting Product"

@app.get("/cart")
def get_cart():
    requests_counter.add(1)
    return "Get Cart"

@app.patch("/cart/<int:id>")
def update_cart(id):
    requests_counter.add(1)
    return "Update Cart"
```

When the app runs, the `PeriodicExportingMetricReader` collects metrics and the `ConsoleMetricExporter` prints them every 5 seconds.

Example run output for the Flask dev server:

```bash theme={null}
$ python main.py
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## 4. Add attributes to break metrics down by route and method

To see per-route and per-method counts while retaining a single canonical metric name, add attributes when calling `.add(...)`. Attributes attach metadata to metric data points. Example:

```python theme={null}
@app.get("/products")
def get_products():
    requests_counter.add(1, {"route": "/products", "method": request.method})
    return "Get All Products"

@app.get("/products/<int:id>")
def get_product(id):
    requests_counter.add(1, {"route": "/products", "method": request.method})
    return "Getting product detail"

@app.post("/products")
def create_product():
    requests_counter.add(1, {"route": "/products", "method": request.method})
    return "Creating Products"

@app.get("/cart")
def get_cart():
    requests_counter.add(1, {"route": "/cart", "method": request.method})
    return "Get Cart"
```

When the console exporter prints JSON, you'll see the counter broken out by attribute combinations such as `route="/products"` and `method="POST"`. Example (abridged):

```json theme={null}
{
  "resource_metrics": [
    {
      "resource": {
        "attributes": {
          "telemetry.sdk.language": "python",
          "telemetry.sdk.name": "opentelemetry",
          "telemetry.sdk.version": "1.37.0",
          "service.name": "unknown_service"
        }
      },
      "scope_metrics": [
        {
          "scope": {
            "name": "shopping-app",
            "version": "0.1.2"
          },
          "metrics": [
            {
              "name": "http_requests_total",
              "description": "Total number of requests processed by the application",
              "unit": "1",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "route": "/cart",
                      "method": "GET"
                    },
                    "value": 1
                  },
                  {
                    "attributes": {
                      "route": "/products",
                      "method": "GET"
                    },
                    "value": 2
                  },
                  {
                    "attributes": {
                      "route": "/products",
                      "method": "POST"
                    },
                    "value": 4
                  }
                ],
                "is_monotonic": true
              }
            }
          ]
        }
      ]
    }
  ]
}
```

Most metrics backends (Prometheus, observability platforms, etc.) allow grouping or summing across attributes, so you can compute the total while retaining per-route detail.

## 5. Why use attributes instead of separate metrics per route?

Creating separate metrics like `products_requests_total` and `cart_requests_total` is possible but has downsides:

| Approach                                                  | Pros                                                                         | Cons                                                            |
| --------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `http_requests_total` with attributes (`route`, `method`) | Single canonical metric; easy aggregation across routes; flexible breakdowns | Requires careful attribute cardinality control                  |
| Separate metrics per route (`products_requests_total`)    | Simple per-route metric names                                                | Proliferation of metrics, harder to aggregate across all routes |

Attributes are the recommended pattern because they enable both detailed breakdowns and straightforward aggregation.

## 6. Centralize instrumentation with a before\_request hook

Instead of invoking `requests_counter.add(...)` in every handler, increment the counter once for all requests using Flask's `before_request` hook. This reduces duplication and ensures consistent instrumentation:

```python theme={null}
@app.before_request
def instrument_request():
    # Use the registered route pattern (url_rule.rule) to avoid high-cardinality values
    # Fallback to request.path if url_rule is not available
    route = request.url_rule.rule if request.url_rule else request.path
    requests_counter.add(1, {"route": route, "method": request.method})
```

This hook runs before each request handler, counting the request centrally.

## 7. Complete example (main.py)

A minimal, complete example showing configuration, centralized instrumentation, and a couple of routes:

```python theme={null}
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

requests_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of requests processed by the application",
    unit="1"
)

app = Flask(__name__)

@app.before_request
def instrument_request():
    # Centralized instrumentation for every incoming request
    route = request.url_rule.rule if request.url_rule else request.path
    requests_counter.add(1, {"route": route, "method": request.method})

@app.get("/products")
def get_products():
    return "Get All Products"

@app.post("/products")
def create_product():
    return "Creating Products"

if __name__ == "__main__":
    app.run()
```

Run the app and make some requests (curl, REST client, browser). Every 5 seconds the console exporter will print the current metrics grouped by attribute combinations.

## 8. Summary and best practices

* Use a Counter (`http_requests_total`) to count incoming HTTP requests.
* Attach attributes such as `route` and `method` (`{"route": route, "method": request.method}`) to break metrics down while preserving a single canonical metric name.
* Centralize counting with `@app.before_request` to avoid repeating instrumentation across handlers.
* During development, `ConsoleMetricExporter` + `PeriodicExportingMetricReader` helps you see metric output. For production, configure a proper exporter/backend.
* Avoid using high-cardinality attribute values (e.g., raw user IDs or full URLs). Prefer route patterns (`/products/<int:id>`) to keep cardinality manageable.

## Links and References

* OpenTelemetry Python Metrics: [https://opentelemetry.io/](https://opentelemetry.io/)
* Flask Documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Gunicorn (production WSGI server): [https://gunicorn.org/](https://gunicorn.org/)
* Prometheus (metrics backend): [https://prometheus.io/](https://prometheus.io/)

Additional examples and exporter integrations are available in the OpenTelemetry Python repository and documentation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/88f4a488-ce0b-4115-82b5-719479110363" />
</CardGroup>


# Demo Histogram

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Demo-Histogram/page

Guides adding OpenTelemetry histograms to a Flask app to measure and bucket request latency, with counters, concurrent tracking, custom bucket configuration, and ConsoleMetricExporter examples.

In this lesson we instrument a Flask application with a histogram metric to measure request latency. A histogram groups observations into buckets so you can see how many requests fall into each latency range (for example: under 50ms, under 100ms, under 1s, over 2s). This helps detect latency regressions and identify when requests negatively impact user experience.

Keywords: OpenTelemetry, histogram, Flask, request latency, metrics, buckets, instrumentation

<Callout icon="lightbulb">
  All timings and bucket boundaries in this article are expressed in milliseconds (ms). Python's `time.time()` returns seconds — multiply by 1000 to get milliseconds before recording to a histogram that uses `"ms"` as its unit.
</Callout>

## What we'll add

* A MeterProvider and Meter configured with a ConsoleMetricExporter (for local testing).
* Instruments:
  * a counter for total requests,
  * an up-down counter for concurrent in-flight requests,
  * a histogram to record request durations.
* A minimal Flask app that records durations in `after_request` and updates the concurrent counter in `before_request`.
* How to customize histogram bucket boundaries using a View and `ExplicitBucketHistogramAggregation`.

## Basic meter and instruments

Create the meter and instruments used by the Flask app. Save this as `metrics_setup.py`.

```python theme={null}
