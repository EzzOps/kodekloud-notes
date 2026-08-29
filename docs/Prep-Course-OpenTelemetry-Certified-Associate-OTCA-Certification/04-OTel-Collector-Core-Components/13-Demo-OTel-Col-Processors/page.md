# collectors-config.yaml
extensions:
  health_check: {}

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  prometheus:
    config:
      scrape_configs:
        - job_name: "python-app"
          scrape_interval: 15s
          static_configs:
            - targets: ["python-app:8000"]

processors:
  batch:
    timeout: 15s
    send_batch_size: 512
  attributes/add_env:
    actions:
      - key: deployment.environment
        value: production
        action: insert
      - key: service.region
        value: us-west-2
        action: upsert

exporters:
  debug:
    verbosity: detailed
  otlp/jaeger:
    endpoint: http://jaeger:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [attributes/add_env, batch]
      exporters: [debug, otlp/jaeger]
    metrics:
      receivers: [prometheus, otlp]
      processors: [attributes/add_env, batch]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

Key points:

* The `prometheus` receiver uses Prometheus-style `scrape_configs` so the Collector behaves like Prometheus and pulls metrics from `python-app:8000`.
* The `otlp` receiver accepts OTLP over both gRPC and HTTP (useful for client push exporters).
* For metrics ingestion, make sure the receiver(s) are listed under `service.pipelines.metrics.receivers`.

## Quick comparison: Push vs Pull

| Aspect             |                                               Push (OTLP) | Pull (Prometheus scrape)                                               |
| ------------------ | --------------------------------------------------------: | ---------------------------------------------------------------------- |
| How metrics arrive |                  Application pushes to Collector via OTLP | Collector scrapes `/metrics` endpoint                                  |
| Typical endpoint   |                        `http://collector:4318/v1/metrics` | `http://your-app:8000/metrics`                                         |
| Use case           | Instrumented apps pushing telemetry (e.g., SDK exporters) | Existing Prometheus exporters or instrumented apps exposing `/metrics` |
| Collector role     |                                 OTLP receiver (HTTP/gRPC) | Prometheus receiver (scraper)                                          |
| Good for           |                  Short-lived batches, centralized pushing | Long-lived services with Prometheus exposition                         |

## Push-based metrics (OTLP)

For push-based metrics, configure an OTLP metrics exporter in your application to send metrics to the Collector. When using the HTTP OTLP exporter, provide the full URL including `/v1/metrics`.

Example Python configuration using OTLP HTTP metrics exporter and a periodic metric reader:

```python theme={null}
# metrics_push.py
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

def configure_meter_push() -> metrics.Meter:
    export_url = "http://localhost:4318/v1/metrics"  # Collector OTLP HTTP endpoint
    otlp_exporter = OTLPMetricExporter(endpoint=export_url)

    # Export every 5 seconds
    reader = PeriodicExportingMetricReader(otlp_exporter, export_interval_millis=5000)

    provider = MeterProvider(resource=Resource.create({}), metric_readers=[reader])
    metrics.set_meter_provider(provider)

    return metrics.get_meter(name="cooling-heating", version="0.1.2")
```

Create observable gauges in the app (example):

```python theme={null}
# inside your application startup
import random
from opentelemetry.metrics import Observation

meter = configure_meter_push()

def temperature_callback(options):
    return [Observation(random.uniform(60.0, 90.0))]

def humidity_callback(options):
    return [Observation(random.uniform(0.0, 1.0))]

meter.create_observable_gauge(
    "current_temperature_fahrenheit",
    description="Current Temperature",
    unit="degF",
    callbacks=[temperature_callback],
)

meter.create_observable_gauge(
    "current_humidity_percentage",
    description="Current Humidity",
    unit="1",  # fraction 0.0 - 1.0
    callbacks=[humidity_callback],
)
```

Run the application:

```bash theme={null}
python scripts/metrics-push.py
```

Collector debug output when receiving pushed metrics (cleaned and truncated for clarity):

```text theme={null}
otel-collector | 2025-09-30T00:12:22.523Z info service@v0.135.0/service.go:211 Starting otelcol-contrib...
otel-collector | 2025-09-30T00:12:22.523Z info extensions/extensions.go:41 Starting extensions..
otel-collector | 2025-09-30T00:12:22.523Z info otlpreceiver@v0.135.0/otlpreceiver.go:121 Starting GRPC server {"endpoint":"[::]:4317"}
otel-collector | 2025-09-30T00:12:22.524Z info otlpreceiver@v0.135.0/otlpreceiver.go:179 Starting HTTP server {"endpoint":"[::]:4318"}
otel-collector | 2025-09-30T00:12:22.534Z info service@v0.135.0/service.go:234 Everything is ready. server
```

When the Collector's `debug` exporter prints pushed metrics it may show:

```text theme={null}
ResourceMetrics #0
Resource attributes:
  telemetry.sdk.language: Str(python)
  telemetry.sdk.name: Str(opentelemetry)
  telemetry.sdk.version: Str(1.0.0)
ScopeMetrics #0
InstrumentationScope cooling-heating 0.1.2
Metric #0
Descriptor:
  - Name: current_temperature_fahrenheit
  - Description: Current Temperature
  - Unit: degF
  - DataType: Gauge
NumberDataPoints #0
Timestamp: 2025-09-30T00:14:45.251669000 UTC
Value: 78.554979
Metric #1
Descriptor:
  - Name: current_humidity_percentage
  - Description: Current Humidity
  - Unit: 1
  - DataType: Gauge
NumberDataPoints #0
Timestamp: 2025-09-30T00:14:45.251669000 UTC
Value: 0.407680
```

This verifies successful push-based ingestion: the app exported metrics to `http://localhost:4318/v1/metrics`, the Collector received them via its OTLP HTTP receiver, and the `debug` exporter printed them.

## Pull-based metrics (Prometheus scraping)

For Prometheus-style scraping, your application exposes an HTTP endpoint that returns Prometheus-formatted metrics (commonly using the `prometheus_client` library). The Collector scrapes that endpoint using the Prometheus receiver.

Example Python configuration using `PrometheusMetricReader`:

```python theme={null}
# metrics_pull.py
from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader

def configure_meter_pull():
    # Expose metrics at http://localhost:8000/metrics for Prometheus scraping
    start_http_server(port=8000, addr="localhost")

    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=Resource.create({}), metric_readers=[reader])
    metrics.set_meter_provider(provider)
    return metrics.get_meter(name="cooling-heating", version="0.1.2")
```

Observable gauges and Flask integration example:

```python theme={null}
# inside your application startup
import random
from opentelemetry.metrics import Observation
from flask import Flask

meter = configure_meter_pull()

def temperature_callback(options):
    return [Observation(random.uniform(60.0, 90.0))]

def humidity_callback(options):
    return [Observation(random.uniform(0.0, 1.0))]

meter.create_observable_gauge(
    "current_temperature_fahrenheit",
    description="Current Temperature",
    unit="degF",
    callbacks=[temperature_callback],
)

meter.create_observable_gauge(
    "current_humidity_percentage",
    description="Current Humidity",
    unit="1",
    callbacks=[humidity_callback],
)

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, metrics!"
```

Start the app:

```bash theme={null}
python3 scripts/metrics-pull.py
```

Collector logs when starting and scraping (important parts):

```text theme={null}
otel-collector | 2025-09-30T10:09:45Z info otlpreceiver@v0.135.0/otlpreceiver.go:121 Starting gRPC server {"endpoint":"[::]:4317"}
otel-collector | 2025-09-30T10:09:45Z info otlpreceiver@v0.135.0/otlpreceiver.go:179 Starting HTTP server {"endpoint":"[::]:4318"}
otel-collector | 2025-09-30T10:09:45Z info service@v0.135.0/service.go:234 Everything is ready. Begin running and processing data
```

After scraping (every 15s as configured), the `debug` exporter prints scraped metrics. Example (truncated):

```text theme={null}
2025-09-30T00:24:49.424Z info Metrics {"otelcol.component.kind":"exporter","otelcol.signal":"metrics"}
ResourceMetrics #0
Resource attributes:
  -> service.name: Str(python-app)
  -> service.address: Str(python-app)
  -> service.instance.id: Str(python-app:8000)
  -> server.port: Str(8000)
  -> url.scheme: Str(http)
ScopeMetrics #0
InstrumentationScope github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheus 0.135.0
Metric #0
Descriptor:
  -> Name: python_gc_objects_collected_total
  -> Description: Objects collected during gc
  -> DataType: Sum
  -> IsMonotonic: true
  -> AggregationTemporality: Cumulative
NumberDataPoints #0
  Value: 415.000000
...
Metric #4
Descriptor:
  -> Name: current_humidity_percentage
  -> Description: Current Humidity
  -> DataType: Gauge
NumberDataPoints #0
  Timestamp: 2025-09-30T00:24:49.412Z
  Value: 0.157135
```

This confirms successful scraping: the Prometheus receiver pulled the `/metrics` endpoint from `python-app:8000` and the `debug` exporter displayed the metrics.

## Common pitfalls and fixes

| Symptom                            | Likely cause                                                  | Fix / Tip                                                              |
| ---------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------- |
| No metrics in pipeline             | Receiver defined but not added to `service.pipelines.metrics` | Add the receiver name to `service.pipelines.metrics.receivers`         |
| OTLP HTTP exporter fails to send   | Incorrect endpoint path                                       | Use full path: `http://host:4318/v1/metrics`                           |
| Prometheus static target not found | Missing port or wrong address                                 | Ensure `static_configs.targets` includes port, e.g., `python-app:8000` |
| Scraped metrics missing labels     | Prometheus exposition missing metadata                        | Confirm exporter/library sets desired labels (e.g., `service.name`)    |

Tips:

* You can enable both OTLP push and Prometheus scraping simultaneously by listing both `otlp` and `prometheus` in the `metrics` pipeline.
* When troubleshooting, the `debug` exporter is very helpful to observe exactly what the Collector receives.

## Summary

* Push-based (OTLP): App pushes metrics to the Collector using an OTLP exporter (often HTTP to `/v1/metrics`). See the OTLP protocol docs: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/)
* Pull-based (Prometheus): App exposes a `/metrics` endpoint and the Collector scrapes it via the Prometheus receiver. See Prometheus: [https://prometheus.io/](https://prometheus.io/)
* The Collector can accept both approaches simultaneously—configure both receivers and add them to `service.pipelines.metrics.receivers`.

With the configuration and code snippets above you can validate both ingestion models and observe metrics via the Collector's `debug` exporter.

## Links and References

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OTLP protocol: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/)
* Prometheus docs: [https://prometheus.io/](https://prometheus.io/)
* Python prometheus\_client: [https://github.com/prometheus/client\_python](https://github.com/prometheus/client_python)
* OpenTelemetry Python metrics: [https://opentelemetry.io/docs/instrumentation/python/metrics/](https://opentelemetry.io/docs/instrumentation/python/metrics/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/54ccbea1-d07d-4179-acf5-34d70e93fa5c" />
</CardGroup>


# Demo OTel Col Processors

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Demo-OTel-Col-Processors/page

Configuring OpenTelemetry Collector processors, especially the batch processor, to batch, filter, and modify telemetry to reduce exporter load and network chattiness while balancing latency and throughput.

This guide shows how to configure a processor in the OpenTelemetry Collector to change how telemetry is exported. We'll focus on the batch processor to reduce exporter load and network chattiness by grouping items and flushing them on a timeout or when a batch size threshold is reached.

Why this matters

* By default, each telemetry signal (traces, metrics, logs) is forwarded to exporters immediately when received.
* High-volume telemetry can create excessive network traffic or overwhelm an exporter.
* The Collector can batch, filter, modify, or sample telemetry between receivers and exporters using processors.

<Callout icon="lightbulb">
  Processors operate between receivers and exporters. They can modify, filter, sample, or batch telemetry before it is sent to exporters.
</Callout>

What processors do

* Receive data from a receiver.
* Modify, enrich, filter, sample, aggregate, or batch that data.
* Forward the processed data to configured exporter(s).

Example: current (simple) service pipelines configuration

```yaml theme={null}
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug, otlp/jaeger]
    metrics:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

Common processors and when to use them
Below are some processors the Collector supports. Multiple processors can be applied to a single pipeline and will execute in series (processor 1 -> processor 2 -> ...).

| Processor    | Use case                                            | Example / notes                                                                      |
| ------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `attributes` | Enrich, remove, or mask attributes on telemetry     | See the `attributes` example below for `insert`, `update`, `delete`, `hash` actions. |
| `batch`      | Buffer telemetry and flush on timeout or batch size | Useful to reduce exporter load and network chatter.                                  |
| `filter`     | Keep or drop telemetry based on expressions         | Fine-grained filtering for traces, metrics, logs.                                    |

Processors run in the order listed in a pipeline; the output of one processor becomes the input of the next.

Attributes processor (example actions)

```yaml theme={null}
processors:
  attributes:
    actions:
      - action: insert
        key: environment
        value: production
      - action: insert
        key: db.statement
        value: '{query}'
      - action: delete
        key: email
      - action: hash
        key: ssn
```

Filter processor (example usage)

```yaml theme={null}
processors:
  filter:
    error_mode: ignore
    traces:
      span:
        - 'attributes["container.name"] == "app_container_1"'
        - 'resource.attributes["host.name"] == "localhost"'
        - 'name == "app_3"'
      span_event:
        - 'attributes["grpc"] == true'
        - 'ISMatch(name, .*grpc.*)'
    metrics:
      metric:
        - 'name == "my_metric" and resource.attributes["my_label"] == "abc123"'
        - 'type == METRIC_DATA_TYPE_HISTOGRAM'
      datapoint:
        - 'metric.type == METRIC_DATA_TYPE_SUMMARY'
        - 'resource.attributes["service.name"] == "my_service_name"'
    logs:
      log_record:
        - 'ISMatch(body, *password.*)'
        - 'severity_number >= SEVERITY_NUMBER_WARN'
```

Batch processor: behavior and configuration
The batch processor buffers telemetry and will flush the buffer when either:

* A timeout elapses (e.g., 15s), or
* A configured `send_batch_size` is reached (e.g., 512 items).

This protects exporters from bursts and reduces chattiness, but it can introduce buffering latency.

Minimal Receiver + Batch configuration

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 15s

exporters:
  # exporters...
```

Add a batch size threshold

```yaml theme={null}
processors:
  batch:
    timeout: 15s
    send_batch_size: 512
```

Explanation

* `timeout: 15s` — flush at most every 15 seconds (since first item in the batch).
* `send_batch_size: 512` — flush sooner if the batch reaches 512 items.
* The buffer flushes when either condition is met (whichever happens first).

Important: batching increases latency for individual telemetry items; tune `timeout` and `send_batch_size` to balance latency and throughput.

<Callout icon="warning">
  Batches reduce exporter load but introduce buffering delay. If you need near-real-time telemetry, set lower timeouts or avoid batching for that pipeline.
</Callout>

Enabling processors in service pipelines
After defining processors under `processors:`, reference them in the `service.pipelines` section where you want them applied. Processors listed for a pipeline execute sequentially.

Example: enabling `batch` for traces

```yaml theme={null}
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug, otlp/jaeger]
    metrics:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

Multiple processors

* When multiple processors are specified, they run in series:
  receiver -> processor A -> processor B -> exporter(s)

Generate telemetry to compare behaviors
First, observe behavior without the batch processor (immediate export).

Using telemetrygen to generate traces and logs:

```bash theme={null}
clear
$GOBIN/telemetrygen traces --otlp-http --otlp-insecure --traces 3
$GOBIN/telemetrygen logs --otlp-http --otlp-insecure --logs 3
```

Sample output you might see when exporters are writing immediately (debug exporter prints to console):

```text theme={null}
jaeger
{"level":"info","ts":1759188297.295914,"caller":"grpc@v1.75.0/balancer_wrapper.go:122","msg":"[core] [Channel #1] Channel switches to new LB policy \"pick_first\""}
jaeger
{"level":"info","ts":1759188297.296026,"caller":"gracefulSwitch/gracefulswitch.go:194","msg":"[pick-first-leaf-lb] Received new config {...}"}
jaeger
[Channel #1] SubChannel #9 SubChannel created
jaeger
[Channel #1] SubChannel #9 Connectivity change to CONNECTING
jaeger
[Channel #1] SubChannel #9 picks a new address "127.0.0.1:4317" to connect
jaeger
[Channel #1] SubChannel #9 Connectivity change to READY
jaeger
{"level":"info","ts":1759188297.296145,"caller":"grpc@v1.75.0/clientconn.go:563","msg":"[core] [Channel #1] Channel Connectivity change to READY"}
```

With no batch processor enabled, traces and logs are forwarded and printed immediately.

Enable the batch processor
Example configuration that enables batching for traces and sends to Jaeger:

```yaml theme={null}
processors:
  batch:
    timeout: 15s
    send_batch_size: 512

exporters:
  otlp/jaeger:
    endpoint: http://jaeger:4317
    tls:
      insecure: true
```

Behavior with batch enabled

* If you generate three traces and the batch `timeout` is 15s, they will be buffered and will not reach exporters (or appear in the debug console) until:
  * 15 seconds have elapsed since the first item in the batch, or
  * 512 items have been collected.
* Collector logs will show the receiver starting and the service becoming ready; after the timeout elapses the buffer is flushed and you’ll see debug exporter output.

Collector log sample (startup and flush)

```text theme={null}
otel-collector | 2025-09-29T23:33:17.065Z    info    otlpreceiver@v0.135.0/otlp.go:179    Starting HTTP server {"resource": {"service.instance.id": "4bcade82-9fb4-4fb9-9361-9b14efe2a42c", "service.name": "otelcol-contrib", "service.version": "0.135.0", "otelcol.component.id": "otlp", "otelcol.component.kind": "receiver"}}
otel-collector | 2025-09-29T23:33:17.065Z    info    service@v0.135.0/service.go:234    Everything is ready. {"resource":{"service.instance.id":"4bcade82-9fb4-4fb9-9361-9b14efe2a42c","service.name":"otelcol-contrib","service.version":"0.135.0"}}
...
