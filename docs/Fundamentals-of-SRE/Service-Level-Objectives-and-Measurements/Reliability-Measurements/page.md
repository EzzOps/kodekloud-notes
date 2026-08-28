# Availability: successful requests divided by total requests (percentage)
sum(rate(http_requests_total{service="api", handler="/catalog", status_code=~"2.."}[5m]))
/
sum(rate(http_requests_total{service="api", handler="/catalog"}[5m])) * 100

# Latency: 95th/99th percentile from a histogram
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Error rate: errors divided by total requests
sum(rate(http_requests_total{status_code=~"5.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100

# Throughput: rate of requests processed
rate(http_requests_total[5m])

# Saturation example: CPU usage as fraction of total (non-idle)
sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) /
sum(rate(node_cpu_seconds_total[5m]))
```

Choose queries that reflect your precise SLI definition — include correct labels (service, handler, endpoint) and ensure windows (e.g., 5m) match your use case. Tools like PromLens and Grafana Query Builder make constructing and validating PromQL queries easier.

White box monitoring gives the most precise SLI signals: instrument your code and infrastructure so metrics, logs, and traces flow to a centralized observability stack.

<Frame>
  <img alt="A slide diagram titled &#x22;Let's Talk White Boxes&#x22; showing Prometheus and Grafana icons feeding into a &#x22;Prometheus Exporter&#x22; component. Arrows from the exporter point to a 3D &#x22;Whitebox Monitoring&#x22; box with upward labels for Metrics, Logs, and Traces." />
</Frame>

White-box instrumentation answers questions like: how many requests succeed, how long they take, what resources they consume, and how a single request flows through services.

Availability

<Frame>
  <img alt="A slide titled &#x22;Availability SLIs&#x22; showing a dashboard with a large 100% API availability gauge and an adjacent time-series availability history chart. The subtitle reads &#x22;Percentage of valid requests that are successfully served.&#x22;" />
</Frame>

Availability SLI formula:

Successful requests / Valid requests × 100%

<Frame>
  <img alt="A presentation slide titled &#x22;Availability SLIs&#x22; that shows the formula &#x22;Successful requests / Valid requests × 100%&#x22; and a &#x22;Use Cases&#x22; box with icons for APIs and Web services." />
</Frame>

Key availability metrics to track:

* Total HTTP requests (baseline context).
* Error counts broken down by class (4xx vs 5xx).
* Success ratio (percentage of successful requests).

Prometheus examples for availability:

```promql theme={null}
# Total requests rate
sum(rate(http_requests_total[5m]))

# Server-side errors (5xx) rate
sum(rate(http_requests_total{status_code=~"5.."}[5m]))

# Success ratio (2xx / total)
sum(rate(http_requests_total{status_code=~"2.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100
```

Latency

<Frame>
  <img alt="A presentation slide titled &#x22;Latency SLIs&#x22; showing a monitoring dashboard with API latency percentile graphs and a P99 latency-by-endpoint list, highlighting response times (e.g., 99 ms and 496 ms)." />
</Frame>

Latency SLIs focus on user-perceived speed. Use histograms and percentiles (P95, P99) rather than averages to capture tail latency. A common latency SLI:

Percentage of requests faster than X ms (e.g., 300 ms)

<Frame>
  <img alt="A slide titled &#x22;Latency SLIs&#x22; showing the formula &#x22;Percentage of requests faster than threshold&#x22; and a &#x22;Use Cases&#x22; box listing user-facing applications, APIs, and database queries. The slide is from KodeKloud (copyright noted)." />
</Frame>

Common latency signals:

* Histogram buckets for request durations (http\_request\_duration\_seconds\_bucket).
* 95th/99th percentile values (histogram\_quantile).
* Counts of requests exceeding an unacceptable threshold.

Prometheus percentile example:

```promql theme={null}
# 99th percentile latency for the /search endpoint (5m window)
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket{service="api", endpoint="/search"}[5m])) by (le)
)
```

Use PromLens or Grafana Query Builder to validate percentile queries and ensure the bucket set aligns with your SLI threshold.

<Frame>
  <img alt="A presentation slide titled &#x22;Using PromLens to Learn and Practice SLI Query Formation&#x22; showing a screenshot of the PromLens website and a query builder interface. Below the image are two points saying Grafana's Query Builder lets you build PromQL queries without coding and that selecting metrics, labels, and filters helps build the final query." />
</Frame>

Error, Throughput, and Saturation

Error SLIs measure request failures. Make explicit what counts as an error (HTTP 5xx, application-level failures, retries exhausted) and track both failure rate and success rate for different audiences (engineering vs. SLO reporting).

<Frame>
  <img alt="A slide titled &#x22;Error, Throughput, and Saturation SLIs&#x22; explaining Error SLIs as the percentage of requests that fail due to server-side errors. It shows formulas for failure rate (Error responses / Total requests × 100%) and success rate (1 − (Error responses / Total requests) × 100%)." />
</Frame>

Throughput SLIs show how much work a system completes in a time window. Drops in throughput can indicate backpressure, queueing, or dropped messages.

<Frame>
  <img alt="A slide titled &#x22;Error, Throughput, and Saturation SLIs&#x22; explaining Throughput SLIs as the rate of requests successfully processed. It shows the formula: Valid requests / Time window." />
</Frame>

Saturation SLIs reveal resource headroom. Rising saturation is an early warning — as CPU, memory, or queue depth approaches limits, latency and error rates often follow. Use saturation metrics to drive autoscaling and preventive alerts.

<Frame>
  <img alt="A presentation slide titled &#x22;Error, Throughput, and Saturation SLIs&#x22; with three numbered use-case boxes. The boxes describe (01) APIs/services where request volume is a key indicator, (02) batch jobs or queue workers tracking processed items per minute, and (03) streaming platforms." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Error, Throughput, and Saturation SLIs&#x22; showing three numbered use-case panels. The panels describe monitoring for CPU/memory/disk/network exhaustion, autoscaling triggers based on CPU/memory usage, and preventive alerting, each with a corresponding icon." />
</Frame>

Applying SLIs to a real app: KodeKloud Record Store

A practical example helps anchor SLI choices. The KodeKloud Record Store API exposes endpoints like product catalog, search, order creation, order status, and background processing. Each user journey is composed of multiple steps — if one step is slow or failing, the whole journey suffers.

<Frame>
  <img alt="A presentation slide titled &#x22;Let's Get Practical: KodeKloud Record Store API&#x22; showing an &#x22;API Service&#x22; section with a highlighted box labeled &#x22;Relevant user journeys&#x22; that lists three items: Browsing records, Searching, and Viewing details, each with an icon." />
</Frame>

For the Record Store API, high-value SLIs are availability and latency. Example target: X% of search queries finish within 300 ms.

<Frame>
  <img alt="A presentation slide titled &#x22;Let's Get Practical: KodeKloud Record Store API&#x22; showing two effective SLIs. It lists Availability (percentage of catalog API requests returning successful HTTP 2xx/3xx) and Latency (percentage of search queries completing within 300 ms), each with an icon." />
</Frame>

Prometheus examples for the Record Store (availability and latency):

```promql theme={null}
# Availability SLI for the catalog endpoint (percentage of 2xx responses)
sum(rate(http_requests_total{service="api", handler="/catalog", status_code=~"2.."}[5m]))
/
sum(rate(http_requests_total{service="api", handler="/catalog"}[5m])) * 100

# Latency SLI (99th percentile) for the search endpoint
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket{service="api", endpoint="/search"}[5m])) by (le)
)
```

User journeys span endpoints (products, orders, background processing). Define SLIs for each important step to avoid blindspots: one slow endpoint can degrade the entire journey.

<Frame>
  <img alt="A slide diagram of the &#x22;KodeKloud Record Store&#x22; microservices architecture showing a central record store connected to Observability, Storage, a Core Microservice, and Async Processing. The observability stack lists Prometheus, Grafana, Jaeger, Loki, AlertManager, Blackbox Exporter and Fluent Bit; storage is PostgreSQL; the core API handles orders/products and async processing uses RabbitMQ and Celery workers." />
</Frame>

Ordering journey example

When a user places an order, typical steps include POST /orders (create), background fulfillment (e.g., Celery), and status updates. Define SLIs for each step:

* Order creation availability: percentage of POST /orders requests that succeed.
* Order creation latency: how quickly the order is accepted/confirmed.
* Order processing success rate: percentage of background tasks that complete successfully.
* End-to-end processing time: percentage of orders processed within a target timeframe.

Prometheus examples for ordering SLIs:

```promql theme={null}
# Order creation availability (percentage)
sum(rate(http_requests_total{handler="/orders", method="POST", status_code=~"2.."}[5m]))
/
sum(rate(http_requests_total{handler="/orders", method="POST"}[5m])) * 100

# Order processing success rate (Celery)
sum(rate(celery_tasks_total{task_name="process_order", status="success"}[5m]))
/
sum(rate(celery_tasks_total{task_name="process_order"}[5m])) * 100

# Percentage of orders processed within 5 seconds (example)
sum(rate(order_processing_time_seconds_bucket{job="order_processor", le="5.0"}[5m]))
/
sum(rate(order_processing_time_seconds_count{job="order_processor"}[5m])) * 100
```

Collecting SLI data

Combine collection methods for robust coverage:

* Application instrumentation — instrument code to expose metrics.
* Load balancer / proxy metrics — infrastructure-level view without code changes.
* Client-side instrumentation — browser/mobile telemetry to measure real user experience.
* Synthetic testing — automated probes simulating user flows.

<Frame>
  <img alt="A presentation slide titled &#x22;SLI Collection Methods&#x22; showing a central &#x22;Implementing SLIs&#x22; circle connected to four data collection methods: Application Instrumentation, Load Balancer/Proxy Metrics, Synthetic Testing, and Client-Side Instrumentation. The slide also includes a small © Copyright KodeKloud note." />
</Frame>

Collection methods compared

| Collection method           | Strengths                         | When to use                            |
| --------------------------- | --------------------------------- | -------------------------------------- |
| Application instrumentation | Precise, fine-grained SLI labels  | SLI definitions tied to business logic |
| Load balancer / proxy       | Easy infrastructure-level metrics | Quick availability checks              |
| Client-side telemetry       | Real user experience metrics      | Frontend performance & UX              |
| Synthetic testing           | Controlled, repeatable checks     | 24/7 availability & SLA verification   |

Application instrumentation (example)

Instrument applications to expose Prometheus metrics. Example using FastAPI and prometheus\_client:

```python theme={null}
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI()

# Track application-level SLIs
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration in seconds",
    ["endpoint"],
    buckets=[0.1, 0.5, 1.0, 5.0]
)

@app.get("/products")
def get_products():
    start_time = time.time()

    # Your business logic here
    # products = db.query(Product).all()
    products = [{"id": 1, "name": "Vinyl A"}]  # placeholder

    # Record metrics
    REQUEST_COUNT.labels(method="GET", endpoint="/products", status_code="200").inc()
    REQUEST_DURATION.labels(endpoint="/products").observe(time.time() - start_time)

    return products

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

Expose /metrics so Prometheus can scrape application metrics. This provides precise, near real-time SLI signals from inside the service.

Synthetic monitoring (example)

Synthetic checks simulate user behavior and provide continuous health and latency measurements even when real traffic is low. Example bash loop:

```bash theme={null}
#!/bin/bash

while true; do
  echo "Performing health check..."

  # Check API health endpoint
  response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

  if [ "$response" -eq 200 ]; then
    echo "API is healthy (HTTP $response)"
  else
    echo "API is unhealthy (HTTP $response)"
    # In a real environment, this would trigger an alert
  fi

  # Check response time (simulating user experience)
  start_time=$(date +%s.%N)
  curl -s http://localhost:8000/ > /dev/null
  end_time=$(date +%s.%N)

  duration=$(echo "$end_time - $start_time" | bc -l)
  printf "Response time: %.3fs\n" "$duration"

  if (( $(echo "$duration > 1.0" | bc -l) )); then
    echo "Warning: Response time exceeds 1 second"
    # In a real environment, this would trigger an alert
  fi

  echo "-------------------------------"
  sleep 30
done
```

Use synthetic tests to validate SLOs during off-peak times and to catch regressions introduced by deployments.

<Callout icon="warning">
  Do not rely on a single data source. Combine application metrics, proxy metrics, client telemetry, and synthetic checks to avoid blindspots.
</Callout>

Summary and next steps

You now have the foundations to select, define, and collect SLIs:

* Pick SLIs that reflect user experience (availability, latency, errors, throughput, saturation).
* Implement precise queries and validate them with tools like PromLens and Grafana.
* Instrument the application and combine collection methods to ensure complete coverage.
* Define SLIs for each step in important user journeys to avoid blindspots.

Next: translate SLIs into Service Level Objectives (SLOs) — actionable targets that balance user expectations with operational realities. We’ll cover SLO strategy, error budgets, and how to integrate reliability into development workflows.

Further reading and references

* Prometheus: [https://prometheus.io](https://prometheus.io)
* Grafana: [https://grafana.com](https://grafana.com)
* PromLens: [https://promlens.com](https://promlens.com)
* Celery documentation: [https://docs.celeryq.dev/en/stable/](https://docs.celeryq.dev/en/stable/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/17f10683-b61d-4369-b0fb-cb73f352d0e4" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/6682af32-bb38-45e9-aa16-afe9a9dad80d" />
</CardGroup>


# Reliability Measurements

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Service-Level-Objectives-and-Measurements/Reliability-Measurements/page

Explains measuring service reliability using SLIs SLOs and SLAs, telemetry and observability practices including metrics logs traces, monitoring techniques, golden signals, and measurement windows.

Welcome. This article explains how reliability is measured using Service Level Indicators (SLIs), Service Level Objectives (SLOs), and Service Level Agreements (SLAs). It also describes the telemetry and monitoring practices you need to collect meaningful data and act on it.

Before you monitor or improve reliability, clarify the business goals that measurements will support. Two complementary disciplines organize those measurements:

* Monitoring — provides the quantitative measurements used to check service health and SLO compliance.
* Observability — provides the context (metrics, logs, traces) required to answer why things fail.

<Frame>
  <img alt="An infographic slide titled &#x22;Monitoring vs Observability — Foundation of Reliability Measurement&#x22; comparing two approaches: Monitoring (left) with an illustration of a person checking dashboards and the caption about measurements serving business goals, and Observability (right) with a person using a magnifying glass over charts and the caption about pulling metrics, logs, and traces to explain system behavior." />
</Frame>

## Core concepts: SLIs, SLOs, SLAs

These three concepts form the foundation of reliability measurement. Keep them distinct and linked:

* SLAs (Service Level Agreements) — formal, often contractual promises to customers. SLAs frequently include financial or business consequences if missed. Because they are customer-facing, SLAs are typically less aggressive than internal targets.
  * Example: 99.9% availability guaranteed; credits issued if availability dips below that.
* SLOs (Service Level Objectives) — internal reliability targets teams set to guide engineering and operations. SLOs answer: how reliable should this service be?
  * Examples: 99.9% successful requests over a 30-day window; 95% of requests complete in under 200 ms.
  * SLOs are time-bound, measurable, and drive operational behavior (alerts, prioritization, error budgets).
* SLIs (Service Level Indicators) — the measurable signals that reflect user experience. SLIs are the raw metrics you measure to determine SLO compliance.
  * Examples: request success rate, latency percentiles, error counts, throughput.
  * SLIs must be quantitative and user-focused.

<Callout icon="lightbulb">
  SLOs are internal targets; SLAs are external promises. Set SLOs more aggressively than SLAs to maintain a buffer between internal goals and customer-facing guarantees.
</Callout>

| Resource | Purpose                                           | Example                                             |
| -------- | ------------------------------------------------- | --------------------------------------------------- |
| SLI      | Measurement that reflects user experience         | `p99_latency < 500ms`, `success_rate = 99.9%`       |
| SLO      | Internal target to drive operations and decisions | 99.9% success over 30 days                          |
| SLA      | External, contractual guarantee                   | 99.9% availability with financial credits on breach |

<Frame>
  <img alt="A slide showing a service reliability hierarchy pyramid for SLAs, SLOs, and SLIs with short definitions (SLAs: formal commitments with business consequences; SLOs: reliability targets; SLIs: metrics measuring service reliability). A color-coded legend on the right labels them as External Promises, Internal Targets, and Measurements." />
</Frame>

## How monitoring and observability work together

* Monitoring supplies the raw measurements (metrics and computed SLIs) and answers “what” — are we within thresholds, is the SLO met, is the error budget being consumed?
* Observability supplies context to answer “why” — traces and logs let you debug unknown failure modes and correlate data across systems.

Monitoring tells you if the system is healthy; observability helps you determine why it is unhealthy. Both are necessary.

<Frame>
  <img alt="A slide titled &#x22;Monitoring and Observability Working Together&#x22; showing a flow from Goal → SLI → SLO. From SLO three arrows lead to green boxes labeled &#x22;Alert,&#x22; &#x22;Use to make decisions,&#x22; and &#x22;Create a buffer relative to the SLA.&#x22;" />
</Frame>

A business goal defines direction. From that goal you pick SLIs that map to user value, define SLOs to set reliability boundaries, and then implement tooling and processes that reflect those objectives: alerts, burn-rate thresholds, error budgets, and prioritization rules balancing feature velocity and stability. Revisit SLOs as usage and application behavior evolve.

Ideally, the best observability is watching real users and understanding their goals. Where that’s not practical, three telemetry types cover most needs: metrics, logs, and traces.

<Frame>
  <img alt="A slide titled &#x22;The Three Data Types for Reliability Measurements&#x22; showing three colorful triangular icons arranged in a triangle labeled Metrics (top), Traces (left) and Logs (right). The slide also shows a small &#x22;© Copyright KodeKloud&#x22; in the bottom left." />
</Frame>

## Telemetry types and their roles

* Metrics — numerical measurements sampled over time. Metrics form the backbone of SLIs and SLO checks. Use metrics for trend detection, anomaly detection, and error-budget accounting.
  * Common SLI metrics:
    * Request success rate / availability
    * Latency percentiles (p50, p95, p99)
    * Throughput (requests/sec)
    * Error counts
  * Example Prometheus-style exposition:

```text theme={null}
