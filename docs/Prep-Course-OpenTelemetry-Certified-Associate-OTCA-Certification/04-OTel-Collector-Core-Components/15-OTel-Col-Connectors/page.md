# No scrape_configs are required if the collector pushes metrics directly.
# The remote-write receiver is enabled via the Prometheus process flag:
# --web.enable-remote-write-receiver
```

Why no `remote_write` section? The `remote_write` stanza in Prometheus is for sending metrics out to remote storage. In this setup, Prometheus acts as the receiver — the HTTP endpoint `/api/v1/write` — which is enabled by the CLI flag above, not by `prometheus.yml`.

Helpful reference:

* Prometheus remote write receiver docs: [https://prometheus.io/docs/prometheus/latest/storage/#remote-endpoints-and-storage](https://prometheus.io/docs/prometheus/latest/storage/#remote-endpoints-and-storage)

## 3) Configure the OpenTelemetry Collector to export metrics via Prometheus remote\_write

Add a `prometheusremotewrite` exporter to your Collector configuration (example filename: `collector-config.yaml` or `otel-collector-config.yaml`) and include it in the metrics pipeline.

Example Collector config:

```yaml theme={null}
receivers:
  prometheus:
    # default Prometheus receiver config that scrapes instrumented targets
  otlp:
    protocols:
      grpc:
      http:

exporters:
  prometheusremotewrite:
    # Prometheus service hostname as visible from Docker Compose network
    endpoint: "http://prometheus:9090/api/v1/write"

  otlp/jaeger:
    # Forward traces to Jaeger (gRPC)
    endpoint: "jaeger:14250"
    tls:
      insecure: true

  debug:
    # Debug exporter that prints pipeline output to the Collector logs
    verbosity: detailed

processors:
  attributes:
    actions:
      - action: insert
        key: environment
        value: "dev"
  filter:
    # configure metric/log filters as needed
  batch:
    timeout: 10s

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [attributes, batch]
      exporters: [debug, otlp/jaeger]
    metrics:
      receivers: [prometheus, otlp]
      processors: [filter, batch]
      exporters: [prometheusremotewrite, debug]
    logs:
      receivers: [otlp]
      processors: [filter, batch]
      exporters: [debug]
```

Key points:

* Exporter name: `prometheusremotewrite` (this is the Collector exporter that POSTs to Prometheus' `/api/v1/write`).
* Endpoint: `http://prometheus:9090/api/v1/write`. When running under Docker Compose, the Collector can resolve the `prometheus` hostname (service name) on the default network.
* Keep a `debug` exporter if you want to inspect metrics in the Collector logs while simultaneously pushing them to Prometheus.
* The `otlp/jaeger` exporter forwards traces to Jaeger on port `14250`.

## 4) Bring up the stack

Start the services in detached mode:

```bash theme={null}
docker-compose up -d
```

Verify containers are running:

```bash theme={null}
docker-compose ps
```

Useful container logs and checks:

| Action                  | Command                                        |
| ----------------------- | ---------------------------------------------- |
| Prometheus logs         | `docker-compose logs prometheus`               |
| Collector logs          | `docker-compose logs <collector-service-name>` |
| Show running containers | `docker-compose ps`                            |

Prometheus UI: [http://localhost:9090](http://localhost:9090)\
Jaeger UI: [http://localhost:16686](http://localhost:16686)

## 5) Validate metrics in Prometheus UI

1. Open [http://localhost:9090](http://localhost:9090).
2. In the "Expression" input, search for metrics emitted by your application. Example metric names from a sample app:
   * `current_temperature_fahrenheit_degF`
   * `current_humidity_percentage`
3. Run queries to confirm metrics are visible and being updated.

<Callout icon="lightbulb">
  If metrics are missing, check:

  * The Collector is running and its metrics pipeline includes the `prometheusremotewrite` exporter.
  * The `endpoint` in the Collector exporter is `http://prometheus:9090/api/v1/write`.
  * Prometheus was started with `--web.enable-remote-write-receiver` and the mounted `prometheus.yml` is valid.
  * Services are on the same Docker Compose network so hostnames resolve between containers.
</Callout>

Troubleshooting tips

* Use the Collector debug exporter (configured above) to see metric payloads in logs.
* Inspect Prometheus logs for errors related to `/api/v1/write`.
* Confirm the Collector and Prometheus containers can reach each other by running a quick `curl` from within the Collector container:
  * Enter the container: `docker exec -it <collector-container> /bin/sh`
  * Test connectivity: `curl -v http://prometheus:9090/api/v1/write`
* Ensure no firewall or host port conflicts exist on `9090`.

References and further reading

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Prometheus remote write docs: [https://prometheus.io/docs/prometheus/latest/storage/](https://prometheus.io/docs/prometheus/latest/storage/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)

This completes the end-to-end setup for pushing metrics from an OpenTelemetry Collector to Prometheus using Prometheus' remote write receiver.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/bd50c58e-2742-4b53-80d7-95063578edc4" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/c9d44c13-fd59-4f7b-978a-75c136505053" />
</CardGroup>


# OTel Col Connectors

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/OTel-Col-Connectors/page

Explains OpenTelemetry Collector connectors, their placement, use cases, and configuration examples for deriving, routing, aggregating, and forwarding telemetry without changing application code

Connectors in the OpenTelemetry Collector enable cross-pipeline telemetry flows and lightweight transformations without changing application SDKs. This article explains what connectors are, where they sit in Collector pipelines, why they’re useful, and how to configure common connectors: count, spanmetrics, servicegraph, routing, forward, sum, and exceptions. Each example uses YAML for the Collector configuration and includes typical use cases and wiring patterns.

<Frame>
  <img alt="The image shows an agenda with four items related to connectors, covering their introduction, placement, usefulness, and configuration." />
</Frame>

What is a connector?

* A connector acts as an exporter on a source pipeline and as a receiver on a target pipeline.
* This lets the Collector derive new telemetry (for example, metrics from traces) or route/fan out data without changing application or SDK code.
* Connectors are useful for SRE metrics (RED/SLIs), topology graphs, routing, aggregation, and error extraction.

<Frame>
  <img alt="The image illustrates an OpenTelemetry Collector setup, showing two pipelines—Traces and Metrics—connected by a connector. Each pipeline includes Receivers, Processors, and Exporters." />
</Frame>

<Callout icon="lightbulb">
  Connectors bridge pipelines by appearing as an exporter on the source pipeline and as a receiver on the target pipeline. This allows the Collector to derive new telemetry (for example, metrics from spans) without changing application or SDK code.
</Callout>

Connector placement and flow

* A connector receives telemetry already processed by a pipeline, optionally performs computation (derive metrics, count, sum, build graphs), and emits data into another pipeline for further processing/export.
* Typical flow: receiver → processors → connector (acts as exporter) → metrics/other pipeline (connector acts as receiver) → exporters.

<Frame>
  <img alt="The image illustrates the placement of connectors within a data pipeline, showing the flow from receivers to processors and exporters, and emphasizing the connector's role in emitting derived metrics." />
</Frame>

Common use cases

* Fan-out / reuse telemetry across multiple pipelines.
* Derive metrics from traces (RED metrics, SLIs, latency histograms).
* Build service dependency graphs and detect unexpected edges.
* Conditionally route telemetry based on attributes.
* Aggregate counts or sums into time-series for KPIs.

Common connectors

* spanmetrics — derive latency, error, and rate metrics from spans.
* servicegraph — build service dependency/topology metrics.
* routing — OTTL rules to route telemetry to pipelines.
* count — convert span events/logs into simple counts.
* sum — aggregate numeric attributes into time-series.
* forward — merge/split pipelines without transforming telemetry.
* exceptions — extract exception data for logging/alerting.

<Frame>
  <img alt="The image lists four common connectors: SpanMetrics, ServiceGraph, Routing, and Count, each with a brief description of their functions related to metrics and traces." />
</Frame>

Connector comparison (quick reference)

| Connector    |                           Primary purpose | Typical source signal          | Example outcome                     |
| ------------ | ----------------------------------------: | ------------------------------ | ----------------------------------- |
| spanmetrics  | Derive RED metrics, histograms, exemplars | Traces                         | Latency histograms, error rates     |
| servicegraph |            Build service dependency graph | Traces                         | Service-to-service edge metrics     |
| routing      |         Route/fan-out based on OTTL rules | Any (resource/span/log/metric) | Environment-based pipelines         |
| count        |                      Count matched events | Spans / Logs                   | Time-series pulse metrics           |
| sum          |              Aggregate numeric attributes | Spans                          | KPI time-series (order totals)      |
| forward      |                     Merge/split pipelines | Any                            | Combined or branched pipelines      |
| exceptions   |                    Extract exception data | Traces (exceptions)            | Correlated logs with trace/span IDs |

***

## Count connector (example)

The Count connector converts span events or logs into simple time-series counts based on matching conditions. It operates as an exporter on the traces/logs pipeline and as a receiver on the metrics pipeline.

Example: count span events named "prodevent" coming from environment "prod" and emit metrics to the metrics pipeline, which exports to `debug`:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc: {}
      http: {}

exporters:
  debug: {}

connectors:
  count:
    spanevents:
      my.prod.event.count:
        description: "The number of span events from prod"
        conditions:
          - 'attributes["env"] == "prod"'
          - 'name == "prodevent"'

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [count]
    metrics:
      receivers: [count]
      exporters: [debug]
```

How it works:

* Traces arrive via OTLP → processed → exported to `count`.
* The connector checks each span event against the `conditions`.
* Matches generate a metric `my.prod.event.count` emitted into the metrics pipeline and exported by `debug`.

<Frame>
  <img alt="The image is a flowchart illustrating a process for generating pulse metrics using a count connector, with data flowing from a &#x22;Spans/Logs Stream&#x22; through &#x22;conditions&#x22; to a &#x22;Time Series Output.&#x22;" />
</Frame>

***

## SpanMetrics connector

SpanMetrics derives SRE-style metrics (rate, errors, latency histograms) and exemplars from spans. It is commonly used to produce RED metrics and latency histograms for Prometheus.

Example: receive traces via OTLP, apply spanmetrics with explicit histogram buckets, dimensions, and exemplars, and export to Prometheus:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc: {}
      http: {}

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889

connectors:
  spanmetrics:
    histogram:
      explicit:
        buckets: [2ms, 8ms, 50ms, 100ms, 200ms, 500ms, 1s, 5s, 10s]
      dimensions:
        - name: http.method
        - name: http.status_code
      exemplars:
        enabled: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [spanmetrics, otlp]
    metrics:
      receivers: [spanmetrics]
      exporters: [prometheus]
```

Use cases:

* SLIs and RED metrics (requests, error rates, durations).
* Latency histograms with exemplars for trace-level correlation.
* Error trend analysis by dimensions (status code, method).

***

## ServiceGraph connector

ServiceGraph computes a service dependency graph from trace spans, identifying client→service and service→service edges and generating related metrics to highlight hotspots or unexpected dependencies.

<Frame>
  <img alt="The image is a diagram showing a &#x22;ServiceGraph&#x22; that maps service dependencies in real time from traces, depicting connections between a client and services A, B, C, and D, highlighting specific issues like &#x22;Hotspot&#x22; and &#x22;Unexpected edge.&#x22;" />
</Frame>

Configuration example: route traces through `servicegraph` and expose dependency metrics to Prometheus:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc: {}
      http: {}

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889

connectors:
  servicegraph: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [servicegraph]
    metrics:
      receivers: [servicegraph]
      exporters: [prometheus]
```

What it produces:

* Metrics showing edges and counts between services.
* Can highlight hotspots and unexpected edges for dependency analysis.

***

## Routing connector (OTTL-based routing)

The Routing connector evaluates OTTL (OpenTelemetry Transformation Language) expressions to dispatch telemetry to different pipelines. Use cases include environment isolation, tenant routing, error pipelines, and fan-out.

Key options:

* `default_pipelines` — where to send unmatched items.
* `match_once` — stop after first match (reduce duplication).
* `error_mode` — how to handle OTTL evaluation errors.

Example: route traces to `traces/prod` if resource has `env=prod`, route error spans (status >= 400) to `traces/errors`, and use a default pipeline for others:

```yaml theme={null}
connectors:
  routing:
    default_pipelines: [traces/default]
    error_mode: ignore
    match_once: true
    table:
      - context: resource
        statement: 'route() where resource.attributes["env"] == "prod"'
        pipelines: [traces/prod]
      - context: span
        statement: 'route() where attributes["http.status_code"] >= 400'
        pipelines: [traces/errors]

service:
  pipelines:
    traces/in:
      receivers: [otlp]
      exporters: [routing]
    traces/prod:
      receivers: [routing]
      exporters: [otlp/prod]
    traces/errors:
      receivers: [routing]
      exporters: [otlp/errors]
    traces/default:
      receivers: [routing]
      exporters: [otlp/default]
```

Example: routing logs from a single `filelog` receiver that contains multiple environments:

```yaml theme={null}
receivers:
  filelog:
    include: ["/var/log/app/*.log"]

exporters:
  otlp/prod:
    endpoint: prod-obsv:4317
  otlp/dev:
    endpoint: dev-obsv:4317

connectors:
  routing/env:
    default_pipelines: [logs/default]
    table:
      - statement: 'attributes["deployment.environment"] == "production"'
        pipelines: [logs/prod]
      - statement: 'attributes["deployment.environment"] == "staging"'
        pipelines: [logs/dev]

service:
  pipelines:
    logs:
      receivers: [filelog]
      exporters: [routing/env]
    logs/prod:
      receivers: [routing/env]
      exporters: [otlp/prod]
    logs/dev:
      receivers: [routing/env]
      exporters: [otlp/dev]
    logs/default:
      receivers: [routing/env]
      exporters: [otlp/dev] # fallback exporter example
```

Routing tips:

* Use `match_once` to avoid duplicates when you only want one destination.
* Use `default_pipelines` to ensure unmatched telemetry still gets processed.
* Test rules with a small dataset to avoid misrouting production telemetry.

***

## Forward connector

The Forward connector is a lightweight bridge that forwards telemetry between pipelines without transformation. It’s useful for merging sources, splitting for multiple downstream destinations, or creating parallel processing branches.

Example: merge logs from two receivers into a single merged logs pipeline, and branch traces into sampled vs all:

```yaml theme={null}
connectors:
  forward: {}

service:
  pipelines:
    logs/blue:
      receivers: [foo/blue]
      processors: [attributes/blue]
      exporters: [forward]
    logs/green:
      receivers: [foo/green]
      processors: [attributes/green]
      exporters: [forward]
    logs/merged:
      receivers: [forward]
      processors: [batch]
      exporters: [otlp]

    traces:
      receivers: [otlp]
      processors: [resourcedetection]
      exporters: [forward]
    traces/sampled:
      receivers: [forward]
      processors: [tail_sampling]
      exporters: [otlp/hot]
    traces/all:
      receivers: [forward]
      exporters: [otlp/cold]
```

When to use forward:

* When you need to combine multiple inputs into one pipeline.
* When you need to create parallel downstream processing (fan-out).

***

## Sum connector

The Sum connector aggregates numeric attributes from spans into time-series sums, optionally grouping by attributes (labels). Useful for business KPIs like revenue, order totals, or counters derived from attributes.

Example: sum order totals and discounts from span attributes, grouped by `promo.code`:

```yaml theme={null}
connectors:
  sum/totals:
    spans:
      purchase.order.total:
        source_attribute: order.total
        conditions:
          - 'attributes["order.total"] != null'
        attributes:
          - key: promo.code
            default_value: none
  sum/discounts:
    spans:
      purchase.discount.total:
        source_attribute: discount.total
        conditions:
          - 'attributes["discount.total"] != null'
        attributes:
          - key: promo.code
            default_value: none
```

Result:

* Time-series `purchase.order.total` and `purchase.discount.total` containing sums of numeric attributes.
* Labels from `promo.code` let you split KPIs by campaign or promotion.

***

## Exceptions connector

The Exceptions connector extracts exception information found in spans and converts that data into logs or log-like telemetry including trace/span IDs for correlation. This is valuable for building error-focused pipelines and alerting.

Example: send traces through `exceptions` to produce logs consumed by a logs pipeline:

```yaml theme={null}
connectors:
  exceptions: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [exceptions, otlp]
    logs:
      receivers: [exceptions]
      processors: [batch]
      exporters: [otlp]
```

What to expect:

* The connector emits structured logs for exceptions that include trace and span IDs.
* Use these logs for alerting, storage in a log backend, or further enrichment.

***

Wrap-up

Connectors let you transform, route, and enrich telemetry inside the Collector without touching application code. They help you:

* Produce SRE metrics and SLIs from traces (spanmetrics, count, sum).
* Build dependency/topology metrics (servicegraph).
* Route and isolate telemetry (routing, forward).
* Extract errors and exceptions for dedicated pipelines (exceptions).

Start small, validate outputs in a staging environment, and monitor for duplicate telemetry or overload when enabling multiple connectors that might fan out signals.

<Callout icon="warning">
  Be careful with fan-out and overlapping rules. Multiple connectors or routing rules can cause duplicated metrics/logs if match conditions overlap. Test configurations and use `match_once` when appropriate.
</Callout>

<Frame>
  <img alt="The image is a slide labeled &#x22;Wrap-up&#x22; that outlines four key points related to telemetry, metrics, and performance. Each point has a number and highlights functions like connectors, common metrics, and strategic guidelines." />
</Frame>

Links and references

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OTTL (OpenTelemetry Transformation Language): [https://opentelemetry.io/docs/collector/transformations/](https://opentelemetry.io/docs/collector/transformations/) (refer to your Collector distribution docs for exact syntax)
* Collector Connectors (see your Collector distribution / contrib docs for supported connector names and options)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/ddb4f7cf-8fdb-46e7-b492-7fdecee52d52" />
</CardGroup>
