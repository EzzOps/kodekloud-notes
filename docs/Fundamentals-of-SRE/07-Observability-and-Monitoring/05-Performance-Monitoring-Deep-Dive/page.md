# From the repository root
docker-compose --env-file .env.dev up -d
```

You should see containers start. Example service logs (truncated):

```text theme={null}
2025-09-24T02:56:46.427879511Z caller=lifecycler.go:576 msg="instance not found in ring, adding with no tokens" ring=ingester
2025-09-24T02:56:46.474503928Z caller=scheduler.go:634 msg="scheduler is ACTIVE in the ring"
2025-09-24T02:56:52.082655597Z logger=plugin.angulardetectorsprovider.dynamic level=info msg="Restored cache from database"
2025-09-24T02:56:52.111130847Z logger=plugin.store level=info msg="Loading plugins..."
```

Generate test traffic and logs:

```bash theme={null}
# Generate test traffic (products, orders, errors)
./test_traffic.sh

# Generate logs for correlation testing
./scripts/generate_logs.sh

# Run synthetic monitoring
./black_box_monitor.sh
```

Example output from the log-generation script (trimmed and cleaned):

```text theme={null}
KodeKloud Records Store - Generating Test Data for Observability
===============================================
Generating logs with trace context...
{"message":"Test spans created","trace_id":"eddcac3a6ecc42d4c8d11afb427633a0","span_id":"65c2a13799c66d7f"}
Generating error logs...
{"error":"Simulated error","trace_id":"fa9effa8010ed5787d7195da925e7efc","span_id":"cd8bd7e6a2391fcd"}
Generating 404 error...
{"detail":"Not Found"}
Creating a product...
{"name":"Vinyl Record","price":19.99,"id":4}
Creating an order...
{"message":"Order received, processing in the background","order_id":6,"task_id":"e96f86f1-6351-4e56-aa0e-03543d9379c5"}
Generating slow operation with nested spans...
```

## The three pillars of observability

Observability generally stands on three pillars:

* Metrics — tell you "what" is happening (counts, latencies, throughput).
* Logs — explain "why" (context, errors, enriched fields).
* Traces — show "where" time is spent across distributed services.

<Frame>
  <img alt="A slide titled &#x22;The Three Pillars – A Deep Dive&#x22; showing three colored pillar icons labeled Metrics (What happened), Logs (Why it happened), and Traces (Where it happened). The icons are blue/purple, orange, and green respectively." />
</Frame>

## Metrics: instrument, expose, scrape, visualize

Typical flow:

* Define counters, histograms, and gauges in the application.
* Expose them on /metrics.
* Have Prometheus scrape them.
* Visualize in Grafana and evaluate rules with Prometheus (Alertmanager).

Minimal example (metrics.py):

```python theme={null}
from prometheus_client import Counter, Histogram

# Basic HTTP metrics
REQUEST_COUNT = Counter(
    "http_requests_total",           # metric name
    "Total HTTP Requests",           # description
    ["method", "endpoint", "status_code"]  # labels
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",  # metric name
    "HTTP Request Duration",         # description
    ["method", "endpoint"],           # labels
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]  # bucket boundaries
)

ERROR_COUNT = Counter(
    "http_request_errors_total",     # metric name
    "Total HTTP Request Errors",     # description
    ["method", "endpoint", "error_type"]  # labels
)
```

Application-specific metrics (excerpt from the Record Store):

```python theme={null}
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry

METRICS_REGISTRY = CollectorRegistry()

# Business-specific traffic metric
orders_operations_total = Counter(
    name='kodekloud_records_operations_total',
    documentation='Total number of record operations (CRUD)',
    labelnames=['operation', 'status'],  # operation: create, read, update, delete
    registry=METRICS_REGISTRY
)

# HTTP request duration (default buckets are suitable for most web apps)
http_request_duration_seconds = Histogram(
    name='kodekloud_http_request_duration_seconds',
    documentation='Time spent processing HTTP requests in seconds',
    labelnames=['method', 'route'],
    registry=METRICS_REGISTRY
)

# Business process latency with custom buckets
order_processing_duration_seconds = Histogram(
    name='kodekloud_order_processing_duration_seconds',
    documentation='Time taken to process an order from start to completion',
    labelnames=['order_type'],  # e.g. standard, express
    registry=METRICS_REGISTRY
)
```

Middleware centralizes recording metrics for each HTTP request instead of scattering metric code through business logic.

Example FastAPI middleware (records counts, durations, and annotates OpenTelemetry spans):

```python theme={null}
# main.py (middleware excerpt)
import time
from fastapi import Request
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from api.telemetry import normalize_route  # helper to normalize dynamic route segments
from api.metrics import http_requests_total, http_request_duration_seconds, http_errors_total

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    method = request.method
    route = normalize_route(request)  # e.g., /products/{id} instead of /products/123

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span(f"{method} {route}") as span:
        try:
            response = await call_next(request)
            status_code = response.status_code
            # Add response attributes to span
            span.set_attribute("http.status_code", status_code)
            span.set_attribute("http.response.size", int(response.headers.get("content-length", 0)))
            if status_code >= 400:
                span.set_status(Status(StatusCode.ERROR))

            # Calculate duration and record metrics
            duration = time.time() - start_time
            http_requests_total.labels(method=method, route=route, status_code=str(status_code)).inc()
            http_request_duration_seconds.labels(method=method, route=route).observe(duration)

            return response

        except Exception as exc:
            span.set_status(Status(StatusCode.ERROR))
            # Record an error metric and re-raise
            http_errors_total.labels(method=method, route=route, error_type=type(exc).__name__).inc()
            raise
```

<Callout icon="lightbulb">
  Normalize dynamic route segments (e.g., /products/) for metric labels to avoid high-cardinality label explosions.
</Callout>

<Callout icon="warning">
  Avoid tagging metrics with high-cardinality values (user IDs, raw UUIDs). High-cardinality labels can cause large memory and storage usage in Prometheus.
</Callout>

PromQL examples:

```promql theme={null}
# Request rate by endpoint (per 5 minutes)
sum(rate(http_requests_total[5m])) by (endpoint)

# 95th percentile response time
histogram_quantile(
  0.95,
  rate(http_request_duration_seconds_bucket[5m])
)
```

You can view these metrics in Grafana dashboards for latency, throughput, error rate, and availability.

<Frame>
  <img alt="A presentation slide titled &#x22;The Three Pillars – A Deep Dive&#x22; showing icons for Metrics, Logs, and Traces and a flow from Python Code → Prometheus Metrics → Dashboards. The slide includes a Grafana dashboard screenshot displaying user-facing metrics like response time, throughput, error rate, and availability." />
</Frame>

If you open the project in your editor you'll find the API source files, Docker Compose, and telemetry code.

<Frame>
  <img alt="A screenshot of Visual Studio Code showing the Welcome page and Explorer sidebar for a project (kodekloud-records-store-web-app) with files like docker-compose.yaml, Dockerfile, and test_traffic.sh. The right pane displays Start options and Walkthroughs/tutorial cards." />
</Frame>

A typical set of imports in main.py (cleaned and corrected):

```python theme={null}
# main.py (imports excerpt)
from fastapi import FastAPI, Request
from api.routes import router
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import logging
import json
import time
from api import models  # ensure models imported so tables exist
from api.database import engine
from api.telemetry import (
    setup_telemetry, get_tracer,
    # Metric names imported from metrics module
    http_requests_total,
    http_request_duration_seconds,
    http_errors_total,
    application_errors_total,
    active_connections,
    custom_registry,
    # helpers
    normalize_route,
    get_error_class,
)
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
```

Prometheus configuration (prometheus.yaml) — consolidated example:

```yaml theme={null}
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'kodekloud-record-store-api'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['api:8000']

  - job_name: 'pushgateway'
    honor_labels: true
    static_configs:
      - targets: ['pushgateway:9091']

  - job_name: 'blackbox-exporter'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['blackbox-exporter:9115']

  - job_name: 'blackbox-health'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - http://api:8000/health
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
      - source_labels: [__param_target]
        regex: ':.*\/(.*)'
        replacement: /$1
        target_label: endpoint
```

You can view what Prometheus will scrape at the metrics endpoint, e.g. [http://localhost:8000/metrics](http://localhost:8000/metrics). Example output (truncated and cleaned):

```text theme={null}
# HELP kodekloud_http_errors_total Total number of HTTP errors
# TYPE kodekloud_http_errors_total counter
kodekloud_http_errors_total{error_code="5xx",method="GET",route="/error-test"} 1.0
kodekloud_http_errors_total{error_code="4xx",method="GET",route="/products/{id}"} 1.0
# HELP kodekloud_http_request_duration_seconds Time spent processing HTTP requests in seconds
# TYPE kodekloud_http_request_duration_seconds histogram
# HELP kodekloud_active_connections_current Current number of active connections
# TYPE kodekloud_active_connections_current gauge
kodekloud_active_connections_current 1.0
```

## Logs: structured, enriched, and correlated

Structured JSON logs are critical for filtering, searching, and correlating with traces and metrics. Include trace\_id and span\_id in logs so you can join traces and logs for root-cause analysis.

Example structured log entry:

```json theme={null}
{
  "timestamp": "2023-07-15T14:32:15.321Z",
  "level": "ERROR",
  "message": "Product not found during checkout",
  "trace_id": "4fd9662137ced86f5b6f59ab578c",
  "span_id": "7f42e1ca2a1d5f8b",
  "method": "POST",
  "endpoint": "/checkout",
  "product_id": 999,
  "operation": "checkout",
  "error_type": "HTTPException",
  "status_code": 404,
  "duration_ms": 1247
}
```

The app uses a small structured logger that enriches messages with trace context and extra fields:

```python theme={null}
# structured_logger.py
import logging
import json
from opentelemetry import trace

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def _span_context_ids(self):
        span = trace.get_current_span()
        span_context = span.get_span_context() if span is not None else None
        trace_id = format(span_context.trace_id, "032x") if span_context and span_context.trace_id else None
        span_id = format(span_context.span_id, "016x") if span_context and span_context.span_id else None
        return trace_id, span_id

    def info(self, msg, **kwargs):
        trace_id, span_id = self._span_context_ids()
        log_data = {
            "message": msg,
            "level": "INFO",
            "trace_id": trace_id,
            "span_id": span_id,
            **kwargs
        }
        self.logger.info(json.dumps(log_data))

    def error(self, msg, **kwargs):
        trace_id, span_id = self._span_context_ids()
        log_data = {
            "message": msg,
            "level": "ERROR",
            "trace_id": trace_id,
            "span_id": span_id,
            **kwargs
        }
        self.logger.error(json.dumps(log_data))

# Usage (in main app)
structured_logger = StructuredLogger(__name__)
structured_logger.info("database_init", status="starting", action="check")
models.Base.metadata.create_all(bind=engine)
structured_logger.info("database_init", status="complete", action="tables_created")

# Initialize OpenTelemetry
setup_telemetry()
```

Container logs are collected by Fluent Bit (via Docker Fluentd/Fluent Bit driver), which attaches container metadata and forwards structured logs to Grafana Loki. Loki stores labeled log streams efficiently and LogQL allows queries that correlate logs to metrics and traces.

<Frame>
  <img alt="A presentation slide titled &#x22;The Three Pillars – A Deep Dive&#x22; with three pillar icons on the left labeled Metrics, Logs, and Traces. On the right it lists four structured-logging benefits: machine-parsable for analysis, consistent fields across services, rich context for debugging, and correlation with traces and metrics." />
</Frame>

## Traces: visualize the request journey

Traces show the request journey across services. Each span is a timed operation with attributes and events. Example checkout trace (summary):

```text theme={null}
Trace ID: 4fd9662137ced86f5b6f59ab578c
├─ POST /checkout: 1,347ms
│  ├─ verify_product: 134ms
│  │  └─ database-query: 128ms
│  ├─ processing_delay: 800ms ⚠ (simulated latency)
│  ├─ create_order_record: 89ms
│  │  └─ database-insert: 67ms
│  ├─ queue_background_processing: 22ms
│  └─ send_order_confirmation: 45ms
```

Traces combined with structured logs and metrics let you pinpoint bottlenecks and errors. Jaeger is used here for trace visualization: search by service, operation, tags, or trace ID.

<Frame>
  <img alt="A screenshot of the Jaeger UI showing a timeline scatter/bubble chart of trace durations with a search/filter sidebar on the left. Below the chart is a list of 20 traces for the service &#x22;kodekloud-record-store-api-dev,&#x22; including operations like GET /health and GET /metrics." />
</Frame>

Generate test traces:

```bash theme={null}
# Create a test trace
curl http://localhost:8000/trace-test
# Create a test error (trace will include error span)
curl http://localhost:8000/error-test
```

Example responses:

```json theme={null}
{"message":"Test spans created","trace_id":"25d7f03dbacb55e428525dcbaa0cf081","span_id":"8434d8b79e486d12"}
{"error":"Simulated error","trace_id":"b3ebdb35dc22f6c451f823ba44025d7a","span_id":"488b6eada0e79420"}
```

Click a trace in Jaeger to inspect span timings, tags, and process details.

<Frame>
  <img alt="A screenshot of the Jaeger UI showing a distributed trace for &#x22;kodekloud-record-store-api-dev: GET /trace-test,&#x22; with a timeline of spans, durations, and a highlighted &#x22;test-span&#x22; containing tags and process info. The view displays span bars, timing markers, and trace details like start time and total duration." />
</Frame>

When an error occurs, expand the trace to find the error span and related logs.

<Frame>
  <img alt="A browser screenshot of the Jaeger UI showing a trace for &#x22;kodekloud-record-store-api-dev: GET /error-test&#x22; with a timeline of spans, durations, and span details. The panel shows an &#x22;error-span&#x22; entry and a warning about a duplicate tag &#x22;error:true&#x22;." />
</Frame>

## The observability stack wiring

All components are wired together in Docker Compose: application services (API, worker), DB, message broker, Prometheus, Pushgateway, Grafana, Alertmanager, Loki, Fluent Bit, Jaeger, and Blackbox Exporter.

<Frame>
  <img alt="A diagram titled &#x22;Implementing Observability at KodeKloud Records Store&#x22; showing the observability stack: application services (API/FastAPI, Worker/Celery, DB/PostgreSQL, RabbitMQ), metrics & monitoring tools (Prometheus, Pushgateway, Grafana, Alertmanager, Blackbox Exporter), logging (Loki, Fluent Bit) and distributed tracing (Jaeger)." />
</Frame>

Example Compose fragments showing environment and logging driver configuration:

```yaml theme={null}
services:
  api:
    environment:
      OTEL_TRACES_SAMPLER: ${OTEL_TRACES_SAMPLER}
      OTEL_PROPAGATORS: "tracecontext,baggage"
      DEBUG: ${DEBUG}
      LOG_LEVEL: ${LOG_LEVEL}
      ENVIRONMENT: ${ENVIRONMENT}
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: "docker.{{.Name}}"
        fluentd-async: "true"
    networks:
      - kodekloud-record-store-net

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kodekloud-record-store-worker
    command: ["celery", "-A", "api.worker", "worker", "--loglevel=info"]
    restart: always
    depends_on:
      - rabbitmq
      - db
      - pushgateway
      - jaeger
    environment:
      POSTGRES_HOST: ${POSTGRES_HOST}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      RABBITMQ_HOST: ${RABBITMQ_HOST}
      PROMETHEUS_PUSHGATEWAY: ${PROMETHEUS_PUSHGATEWAY}
      PYTHONPATH: ${PYTHONPATH}
      OTEL_SERVICE_NAME: kodekloud-record-store-worker
      DEBUG: ${DEBUG}
      LOG_LEVEL: ${LOG_LEVEL}
      ENVIRONMENT: ${ENVIRONMENT}
    networks:
      - kodekloud-record-store-net
```

From a tooling perspective, the stack includes:

|          Resource Type | Use Case                                          |
| ---------------------: | ------------------------------------------------- |
|             Prometheus | Metrics collection, rule evaluation, and alerting |
|            Pushgateway | Short-lived/one-off jobs push metrics             |
|                Grafana | Dashboards and visualization for metrics and logs |
|           Alertmanager | Alert routing (Slack, PagerDuty, email)           |
|      Blackbox Exporter | External synthetic probes and health checks       |
|             Fluent Bit | Container log collection and forwarding           |
|                   Loki | Efficient label-based structured log storage      |
| Jaeger / OpenTelemetry | Distributed tracing and trace visualization       |

<Frame>
  <img alt="A screenshot of an &#x22;Observability Tools&#x22; slide listing a metrics stack (Prometheus, Pushgateway, Grafana, Alertmanager, Blackbox Exporter) with their ports and brief descriptions. On the right is a Jaeger-like UI panel for searching and filtering traces." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Observability Tools&#x22; listing a logging stack: Fluent Bit (Port 24224) to collect Docker logs, Loki (Port 3100) to store structured logs, and Grafana to display logs with metrics. On the right is a Jaeger UI trace search panel." />
</Frame>

Putting it all together: a user request reaches FastAPI; middleware and instrumentation generate metrics, structured logs, and traces; Prometheus scrapes metrics and evaluates alerts; logs flow to Loki via Fluent Bit; traces flow to Jaeger via OpenTelemetry exporters. Alertmanager routes alerts to the right channels. Grafana ties metrics, logs, and traces together to support fast investigation.

<Frame>
  <img alt="A presentation slide titled &#x22;The Three Pillars – A Deep Dive&#x22; showing three pillar icons labeled Metrics, Logs, and Traces on the left and a boxed summary on the right titled &#x22;What This Trace Reveals&#x22; with notes: Total Request Time 1.35s, Bottleneck: Processing delay → 800ms, Database <150ms, and Investigation Focus: Optimize background tasks." />
</Frame>

## Wrap-up

Thanks for sticking with this practical lesson. We covered how metrics, logs, and traces are produced, collected, stored, and visualized in a concrete stack, and how they combine to help you detect, investigate, and resolve problems faster. For deeper exploration, check the resources below.

## Links and references

* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Loki: [https://grafana.com/oss/loki](https://grafana.com/oss/loki)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Fluent Bit: [https://fluentbit.io/](https://fluentbit.io/)
* Blackbox Exporter: [https://github.com/prometheus/blackbox\_exporter](https://github.com/prometheus/blackbox_exporter)

You can also explore data sources and visualization fundamentals in the accompanying material.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/92f39ae4-b287-4850-93aa-3f0119393754/lesson/afb59a4a-566c-4e8b-bfae-9065c0c2b7d8" />
</CardGroup>


# Performance Monitoring Deep Dive

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Observability-and-Monitoring/Performance-Monitoring-Deep-Dive/page

Guidance on modern performance monitoring focusing on user-facing metrics, tail latency, baselines, bottleneck diagnosis, and alerting to improve reliability and business outcomes.

Welcome back. This lesson drills into performance monitoring with practical guidance you can apply to production systems. Performance is not just raw speed — it directly affects reliability, user trust, and revenue. Slow or unpredictable systems frustrate users, cause churn, and often indicate deeper reliability problems. Performance and reliability are tightly coupled; monitoring should reflect both.

At Amazon, engineers measured that adding 100 ms of latency correlated with about a 1% drop in sales. At scale this became tens of millions of dollars per year in lost revenue — a clear example of how performance directly maps to business outcomes.

<Frame>
  <img alt="A slide titled &#x22;The Performance–Reliability Connection&#x22; featuring the Amazon logo and a three-box flow: &#x22;100ms latency&#x22; → &#x22;1% sales lost&#x22; → &#x22;$10M/year lost.&#x22; It illustrates the estimated revenue impact of added latency." />
</Frame>

When performance and reliability are both high, users are happy and revenue grows. Different combinations produce different business outcomes:

* High performance + high reliability → strong user satisfaction and growth.
* High performance + low reliability → intermittent disasters and eroded trust.
* Low performance + high reliability → stable but slow experience and steady revenue leakage.
* Low performance + low reliability → business “death spiral.”

A real-world example: the Pokémon GO launch in July 2016 experienced \~50× traffic than expected, overwhelming databases and backends, causing multi-day outages and major revenue impact. That incident shows how performance problems can quickly cascade into reliability failures if capacity and scaling triggers are not in place.

<Frame>
  <img alt="A slide titled &#x22;The Performance–Reliability Connection&#x22; summarizing the Pokémon GO July 2016 launch failure, showing Problem (50x traffic spike, DB couldn't handle load), Impact (3 days downtime, ~$35M lost revenue) and Lesson (need capacity limits and scaling triggers). The slide includes icons for server errors, distributed load, and scaling." />
</Frame>

## What traditional monitoring misses

Traditional monitoring often relies on averages and infrastructure metrics that can hide real problems:

* Averages mask tail behavior (p95/p99).
* Synthetic tests may not reflect real user workflows.
* Infrastructure metrics alone (CPU/memory) do not reveal business impact.
* Alerts that only fire after customers are affected are too late.

Modern observability addresses these blind spots by focusing on user-facing metrics, tail latency, and correlating system indicators to customer impact.

## Layered approach to performance monitoring

Think in layers when instrumenting systems:

* Primary, user-facing metrics: response time, throughput, error rate, availability — these are what customers experience.
* System performance indicators: CPU, memory, database latency, queue depth — these explain why user-facing metrics behave as they do.

<Frame>
  <img alt="A slide titled &#x22;Essential Performance Metrics&#x22; showing a performance-metrics hierarchy split into User-Facing Metrics (marked Primary) — Response Time, Throughput, Error Rate, Availability — and System Performance Indicators — CPU & memory usage, database response time, and queue depth." />
</Frame>

### Why percentiles matter

Averages can be misleading. Consider a system with average latency = 100 ms. That sounds excellent, but if p95 ≈ 2,000 ms and p99 ≈ 5,000 ms, a small subset of users experience severe delays — often high-value users with complex workflows. Tail latencies (p95/p99) are critical for user-facing reliability decisions.

<Frame>
  <img alt="A slide titled &#x22;Essential Performance Metrics&#x22; showing three cylindrical bars: Average Response Time ~100ms, P95 Response Time ~2,000ms, and P99 Response Time ~5,000ms. Each bar has a short caption about typical user experience, 5% waiting 2+ seconds, and 1% having a terrible experience." />
</Frame>

<Callout icon="lightbulb">
  Prioritize p95 and p99 when SLAs, SLOs, or high-value user experiences are critical. Use averages for capacity planning and long-term trends, but let tail metrics drive user-facing reliability decisions.
</Callout>

## Finding bottlenecks

Once you detect slow performance (via p95/p99 or user reports), narrow down the root cause. Common bottlenecks:

* Database: slow queries, connection pool exhaustion, lock contention, missing indexes.
* Network & external dependencies: third-party APIs, DNS latency, network saturation.
* Application code: N+1 queries, inefficient algorithms, memory leaks.
* Infrastructure saturation: CPU, memory, disk I/O limits.

<Frame>
  <img alt="A presentation slide titled &#x22;Common Performance Bottlenecks&#x22; showing four categories: Database Performance (80%), Network & External Dependencies, Application Code Issues, and Infrastructure Constraints. Each category includes brief causes like slow queries and lock contention, third‑party API/DNS latency, N+1 queries and memory leaks, and CPU/memory/I/O saturation." />
</Frame>

Correlating metric patterns often points quickly to the likely area to investigate:

* High DB query time with normal CPU → database bottleneck.
* Spiking CPU with stable DB times → CPU-bound application work or inefficient code.
* Rising memory over time with increasing latency → memory pressure or leaks.
* High error rates + high latency → overload or cascading failures.

<Frame>
  <img alt="An infographic titled &#x22;Common Performance Bottlenecks&#x22; listing metric patterns (high DB query time, high CPU, high memory usage, high error rate) alongside their likely causes: database bottleneck, application bottleneck, memory pressure, and system overload." />
</Frame>

## Baselines and trends: defining “normal”

Performance monitoring becomes actionable when you know what “normal” is. Baselines capture typical behavior over different time scales so that deviations are meaningful:

* Daily patterns: peak login times and evening lull.
* Weekly patterns: weekday vs weekend differences.
* Seasonal patterns: holiday shopping or periodic campaigns.
* Growth trends: gradual changes as user base increases.

<Frame>
  <img alt="A slide titled &#x22;Performance Baselines and Trends&#x22; showing a line chart with three colored trend lines, a magnifying glass highlighting the top lines, and a caption saying you can't distinguish between &#x22;normal slow&#x22; and &#x22;broken slow&#x22; without baselines." />
</Frame>

<Frame>
  <img alt="An infographic titled &#x22;Performance Baselines and Trends&#x22; showing a timeline with four numbered markers. Each marker lists a baseline: Daily Patterns (morning traffic spike, evening lull), Weekly Patterns (weekend vs weekday behavior), Seasonal Patterns (holiday shopping, back-to-school), and Growth Trends (gradual increase as user base grows)." />
</Frame>

Example: if today’s p95 = 450 ms vs last week’s p95 = 280 ms (≈ 61% increase), that deviation merits investigation. Likely causes include a recent deployment, database maintenance (VACUUM/REINDEX), sudden traffic that missed autoscaling triggers, or external dependency degradation.

<Frame>
  <img alt="A presentation slide titled &#x22;Performance Baselines and Trends&#x22; showing a bar chart where today's P95 response time rose to 450ms from last week's 280ms (about a 61% increase). To the right is a &#x22;Possible causes&#x22; list: recent deployment, database maintenance (VACUUM/REINDEX), increased traffic without scaling, and external dependency degradation." />
</Frame>

## Alerts that reduce noise and improve actionability

Baselines enable smarter alerting. Use a mix of immediate, trend, capacity, and SLO alerts tied to error budgets.

| Alert type       | Purpose                              | Example trigger                |
| ---------------- | ------------------------------------ | ------------------------------ |
| Immediate alerts | Detect sudden spikes                 | Response time > 2× baseline    |
| Trend alerts     | Catch gradual degradation            | >20% degradation over 24 hours |
| Capacity alerts  | Warn before limits are hit           | Connection pool > 80% used     |
| SLO alerts       | Protect user promises & error budget | Monthly error budget at risk   |

<Frame>
  <img alt="A presentation slide titled &#x22;Performance Baselines and Trends&#x22; showing four colored alert boxes: Immediate Alerts, Trend Alerts, Capacity Alerts, and SLO Alerts. Each box lists trigger conditions (e.g., response time >2x baseline; performance degrading >20% over 24 hours; approaching system limits; monthly error budget at risk)." />
</Frame>

Practical alerting tips:

* Use dynamic thresholds relative to baselines rather than static numbers.
* Combine multiple signals (latency + error rate + saturation) to reduce false positives.
* Route alerts based on ownership and runbooks to speed remediation.
* Tie alerts to SLOs and error budgets to prioritize work.

## Quick checklist to shift from reactive to proactive

* Instrument user-facing metrics (latency, throughput, errors, availability).
* Track tail latency (p95, p99) in addition to averages.
* Establish baselines for expected daily/weekly/seasonal patterns.
* Correlate system metrics to user impact for faster diagnosis.
* Configure targeted, SLO-driven alerts and maintain runbooks.

## Useful references

* Google SRE resources: [https://sre.google/books/](https://sre.google/books/)
* Prometheus monitoring: [https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)
* Kubernetes concepts (for capacity and autoscaling): [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

That concludes this lesson on performance monitoring. Next: advanced visualization and reporting — how to present monitoring data so it’s actionable without overwhelming teams.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/92f39ae4-b287-4850-93aa-3f0119393754/lesson/3592e762-6ac2-4294-b54a-4e13937748e6" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/92f39ae4-b287-4850-93aa-3f0119393754/lesson/e3104654-4009-4303-b34b-212fa2da3115" />
</CardGroup>
