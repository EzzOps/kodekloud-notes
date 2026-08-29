# metrics.py
# Metrics are exposed at /metrics endpoint
REQUEST_COUNT.labels(method="POST", endpoint="/checkout").inc()
REQUEST_DURATION.labels(method="POST", endpoint="/checkout").observe(0.234)
```

Prometheus scrapes the /metrics endpoint on a configured interval (for example, every 15s). The TSDB stores series as timestamped samples:

```text theme={null}
# Data stored as time series (example)
http_requests_total{method="POST", endpoint="/checkout"} 1024 @1699123456
http_requests_total{method="POST", endpoint="/checkout"} 1127 @1699123471
```

Logs and traces complement metrics: Loki collects logs (with optional trace IDs), and Jaeger stores traces for distributed request analysis. Grafana can be provisioned to surface all three data sources automatically on startup.

<Frame>
  <img alt="A slide titled &#x22;Grafana Data Source Configuration&#x22; showing a four-step query flow: Grafana sends a PromQL query, Prometheus returns time-series data, Grafana renders the visualization, and the dashboard refreshes automatically (5s, 30s, 1m). The top row lists configuration steps: data source configuration, Prometheus data source setup, multiple data sources, and Grafana query flow." />
</Frame>

Provisioning Grafana with datasources and dashboards is typically done by mounting a provisioning folder (so Grafana loads it at startup). Example docker-compose snippet:

```yaml theme={null}
# docker-compose.yml (excerpt)
services:
  grafana:
    image: grafana/grafana:11.5.1
    container_name: kodekloud-record-store-grafana
    restart: always
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
      GF_USERS_ALLOW_SIGN_UP: "false"
      GF_PATHS_PROVISIONING: /etc/grafana/provisioning
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/monitoring/grafana-provisioning:/etc/grafana/provisioning
    networks:
      - kodekloud-record-store-net
    depends_on:
      - prometheus
      - loki
      - jaeger
```

A typical Grafana provisioning file (config/monitoring/grafana-provisioning/datasources.yml) that registers Prometheus, Loki, and Jaeger:

```yaml theme={null}
# config/monitoring/grafana-provisioning/datasources.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100

  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    editable: true
```

> **lightbulb** Provision Grafana via GF\_PATHS\_PROVISIONING so datasources and dashboards are available at startup. Keep these provisioning files in version control for reproducible dashboards and consistent environments.

How Grafana and Prometheus interact:

* Grafana panels issue PromQL queries to Prometheus.
* Prometheus returns time-series samples.
* Grafana renders those samples as line charts, stat panels, heatmaps, tables, etc.
* Dashboards refresh on configured intervals (5s, 30s, 1m...), forming the core query-response loop of observability.

Data source roles (quick reference):

| Data Source | Role                                         | Grafana Type |
| ----------- | -------------------------------------------- | ------------ |
| Prometheus  | Time-series metrics collection and TSDB      | prometheus   |
| Loki        | Logs with structured context and trace IDs   | loki         |
| Jaeger      | Distributed traces for request flow analysis | jaeger       |

When designing dashboards, follow three pragmatic laws:

<Frame>
  <img alt="A presentation slide titled &#x22;Dashboards – Basic Design Principles&#x22; with a header &#x22;The Three Laws of SRE Dashboards.&#x22; It shows three colored panels labeled &#x22;Clarity Over Beauty,&#x22; &#x22;Context Over Data,&#x22; and &#x22;Action Over Information,&#x22; each with a short explanation about readability, baselines/targets, and enabling decision-making." />
</Frame>

* Clarity over beauty: during an incident, readability matters more than aesthetics.
* Context over raw data: include baselines, SLOs, and trend lines to interpret numbers.
* Action over information: every chart should help make a decision (link to runbooks, show drilldowns).

The dashboard layout should be layered so an engineer can answer "Is everything okay?" in about 10 seconds:

* Top row: high-level service health overview.
* Middle rows: performance trends and comparisons.
* Bottom rows: root-cause drilldowns and detailed logs/traces.

<Frame>
  <img alt="A presentation slide titled &#x22;Dashboards – Basic Design Principles&#x22; showing a Grafana dashboard. It displays a &#x22;Level 1: Service Health Overview&#x22; with large green panels and charts indicating overall service health and metrics." />
</Frame>

If the top-level status indicates an issue, drill into performance details: request rate trends, latency percentiles, error rates, and resource utilization.

<Frame>
  <img alt="A presentation slide titled &#x22;Dashboards – Basic Design Principles&#x22; with the subtitle &#x22;Level 2: Service Performance Details — Investigate trends and issues.&#x22; It shows a dark monitoring dashboard with charts for request rate by endpoint, error rate by status code, and response time (P50, P95)." />
</Frame>

Choose chart types deliberately — pick visuals that clarify trends and enable decisions.

<Frame>
  <img alt="A slide titled &#x22;Chart Types for SRE Metrics&#x22; recommending time-series (line) charts for request rates, latency and error rates because they show trends and spikes. On the right is a monitoring dashboard screenshot with response-time and CPU/memory usage graphs." />
</Frame>

Use this quick mapping to choose visuals:

| Chart Type          | Best For                                        | Why                                    |
| ------------------- | ----------------------------------------------- | -------------------------------------- |
| Time series (line)  | Request rates, latency percentiles, error rates | Shows trends and spikes clearly        |
| Stat / single-value | Uptime, SLO compliance, P95                     | Immediate at-a-glance status           |
| Histogram / heatmap | Response-time distributions                     | Reveals outliers that percentiles hide |
| Bar chart           | Comparative error rates or request volumes      | Simple comparison across groups        |

<Frame>
  <img alt="A slide titled &#x22;Chart Types for SRE Metrics&#x22; with a &#x22;Status/Health&#x22; list showing Best Chart: Stat panel, Use Case: Service health/SLOs, and Why: Immediate visual status. To the right is a green tiled dashboard showing multiple P95 response time panels (95.0 ms)." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Chart Types for SRE Metrics&#x22; recommending heatmap/histogram for distribution data, with use case &#x22;response times&#x22; and reason &#x22;reveals real user experience.&#x22; On the right is a dark-themed heatmap showing response time percentiles (average, P95, P99) over time." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Chart Types for SRE Metrics&#x22; showing a left panel of comparative data (01 Best Chart: Bar chart; 02 Use Case: Error rates by service; 03 Why: Easy comparison) and a right-side dark dashboard widget labeled &#x22;Error Rate SLO&#x22; with 0% error bars for several time windows." />
</Frame>

Avoid charts that obscure trends: pie charts for time series, 3D effects, excessive color palettes, and tiny fonts make dashboards difficult to read during incidents.

<Frame>
  <img alt="A presentation slide titled &#x22;Chart Types for SRE Metrics&#x22; showing &#x22;What NOT to Use&#x22; with four numbered boxes warning against pie charts (not for time series), 3D charts (confusing), too many colors (hard to distinguish), and tiny fonts (unreadable during incidents)." />
</Frame>

Start a dashboard with a clear purpose. For the KodeKloud record store, the target is a service health overview that helps engineers quickly identify services needing attention. Critical metrics: availability, request rate, error rate, and response time (P95). Example PromQL queries for these metrics:

```promql theme={null}
# Availability (up = 1 means target is reachable)
up{job="kodekloud-record-store-api"}

# Request rate (per second over 5m)
rate(http_requests_total[5m])

# Error rate (5xx responses per second)
rate(http_requests_total{status_code=~"5.."}[5m])

# Response time (P95) from histogram buckets
histogram_quantile(
  0.95,
  rate(kodekloud_http_request_duration_seconds_bucket[5m])
)
```

Layout guidance:

* Top row: large status numbers and SLO indicators.
* Middle rows: trends, comparisons, and resource usage.
* Bottom rows: detailed breakdowns, tables, logs, and trace links.
  Add SLO overlays and threshold-based coloring so panels are green/yellow/red according to SLO boundaries.

<Frame>
  <img alt="A presentation slide titled &#x22;Building Your First Effective Dashboard&#x22; listing three steps (Define Your Purpose; Choose Your Metrics; Layout and Organization) with the third highlighted. To the right is a mock dashboard showing top metrics (99.8% uptime, 1.2K RPS, 120ms) and panels for Request Rate, Error Rate, Response Times, and Error Breakdown." />
</Frame>

Example SLO targets for the record-store service:

```yaml theme={null}
# SLO Targets
availability: 99.9%
latency:
  p95: "< 500ms"
error_rate: "< 1%"
```

Validate dashboards under realistic load—generate synthetic traffic and errors to ensure alerts, color thresholds, and drilldowns behave as intended.

To generate logs and traces for local testing:

```bash theme={null}
# Generate comprehensive test data including errors and traffic
./scripts/generate_logs.sh
```

Example output after running the test generator (trimmed):

```bash theme={null}
$ ./scripts/generate_logs.sh
KodeKloud Records Store - Generating Test Data for Observability
========================================
Generating logs with trace context...
{"message":"Test spans created","trace_id":"23e3b9c0012b79fe8e15de6d5babaef5","span_id":"e1cca1933c5ac72d"}
Generating error logs...
{"error":"Simulated error","trace_id":"eb29cf3893f8a137d5b1e47d2d482961","span_id":"5a6d3185f84fc29f"}
Generating 404 error...
{"detail":"Not Found"}
Generating product listing logs...
[{"name":"Vinyl Record","price":19.99,"id":1},{"name":"Vinyl Record","price":19.99,"id":2},{"name":"Abbey Road","price":25.99,"id":3}]
```

Open Grafana at [http://localhost:3000](http://localhost:3000) to explore provisioned dashboards. The demo dashboards include observability overviews, user-experience widgets, and an end-to-end purchase journey with links to detail dashboards.

<Frame>
  <img alt="A screenshot of the Grafana web UI showing the Dashboards menu and a list of KodeKloud dashboard entries. Large metric panels with big numeric values (e.g., 0.00351, 100, 0.0739) are visible along the bottom." />
</Frame>

Logs often include trace context so you can pivot from a log line into a Jaeger trace and back to metrics. Example structured log line (JSON):

```json theme={null}
{
  "log":"{\"message\":\"http_error\",\"level\":\"ERROR\",\"trace_id\":\"7392f0da7857dbb33b493e4be7a9ba21\",\"span_id\":\"08d85bde2a104cf7\",\"method\":\"GET\",\"route\":\"/products/{id}\",\"status_code\":404,\"error_class\":\"4xx\",\"duration_ms\":5.0}",
  "container_id":"b9b82e5e5af0b6794b809f86c44953f3fbf08344c322dc58c371997d3d87576",
  "container_name":"/kodekloud-records"
}
```

<Frame>
  <img alt="A screenshot of a Grafana dashboard showing performance metrics with multiple P95 response-time tiles, a requests-per-second panel, a red &#x22;100%&#x22; panel and a green &#x22;UP&#x22; panel with a checkmark. A response-time line chart is visible at the bottom and a dark navigation sidebar is on the left." />
</Frame>

The P95 panel uses a PromQL expression like:

```promql theme={null}
# P95 response time in milliseconds
histogram_quantile(0.95, rate(kodekloud_http_request_duration_seconds_bucket[5m])) * 1000
```

Grafana dashboards and panels are stored in the provisioning folder (datasources and dashboards). Inspect the JSON to see how queries, thresholds, units, links, and alerts are configured. Example panel field configuration (thresholds and unit):

```json theme={null}
"panels": [
  {
    "fieldConfig": {
      "defaults": {
        "thresholds": {
          "steps": [
            { "color": "green", "value": null },
            { "color": "yellow", "value": 0.02 },
            { "color": "red", "value": 0.05 }
          ]
        },
        "unit": "percent"
      },
      "overrides": []
    },
    "gridPos": { "h": 8, "w": 6, "x": 12, "y": 0 }
  }
]
```

Explore the provisioning folder, copy panels into your own dashboards, tweak units and thresholds, and validate under synthetic load to ensure panels and alerts behave as expected during incidents.

> **warning** Do not store plaintext credentials in provisioning files. Use environment variables or a secrets manager (for example, GF\_SECURITY\_ADMIN\_PASSWORD via Docker Compose) and restrict access to provisioning folders.

Links and references

* Prometheus: [https://prometheus.io](https://prometheus.io)
* Grafana docs — Provisioning: [https://grafana.com/docs/grafana/latest/administration/provisioning/](https://grafana.com/docs/grafana/latest/administration/provisioning/)
* Loki: [https://grafana.com/oss/loki/](https://grafana.com/oss/loki/)
* Jaeger: [https://www.jaegertracing.io](https://www.jaegertracing.io)
* PromQL basics: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)

Further reading and examples:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Grafana Labs](https://grafana.com/)

Use these patterns to build reproducible, testable dashboards that surface the right signals at the right time.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/92f39ae4-b287-4850-93aa-3f0119393754/lesson/442c5b74-ef58-4257-ac5d-00af5cfd121f)


# Observability in Practice

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Observability-and-Monitoring/Observability-in-Practice/page

Practical guide to implementing observability with metrics, logs, and traces using a sample app and a Prometheus Grafana Loki Jaeger stack

Hey there — welcome back.

In this lesson we move from theory into practice. Observability is more than collecting logs, metrics, and traces — it’s using those signals to answer real operational questions when systems misbehave: what happened, where, when, and why. This guide shows how to connect signals to real problems and turn dashboards and alerts into actionable investigations. By the end you’ll see how observability becomes actionable insight, not just data.

Systems will fail in unexpected ways. Traditional monitoring (is the server up? is CPU \< 80%?) often doesn’t help when users report that checkout is broken. Observability goes deeper: it lets you ask and answer new diagnostic questions using combined metrics, structured logs, and distributed traces.

<Frame>
  <img alt="A slide titled &#x22;Observability – Overview&#x22; showing a person at a laptop with an alert &#x22;Checkout page broken&#x22; alongside an iceberg diagram that contrasts shallow monitoring (server up, CPU, requests) above the water with deeper observability (what/when/where/why) below the surface. The observability section lists details like error rate spike, time after deployment, payment DB connection, and missing index in query." />
</Frame>

Internalizing an observable mindset is essential for effective SRE work: assume unknown failures, enable unexpected questions, and focus on system behavior (not just simplistic health checks).

<Frame>
  <img alt="A presentation slide titled &#x22;Observability – Overview.&#x22; It shows an &#x22;Observability Mindset&#x22; circle linked to three principles: assume unknown failures; enable unexpected questions; and understand behavior, not just health." />
</Frame>

## Hands-on: spin up the KodeKloud Record Store

We’ll run the Record Store app locally, generate traffic, and inspect the metrics, logs, and traces.

Start the Compose stack (from repo root):

```bash theme={null}
