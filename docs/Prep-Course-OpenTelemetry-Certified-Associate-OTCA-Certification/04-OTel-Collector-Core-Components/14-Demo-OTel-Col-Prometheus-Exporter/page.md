# After timeout (batch flushed) you'll see the buffered spans/logs printed by the debug exporter
```

Summary

* Processors let you inspect, modify, filter, sample, or batch telemetry between receivers and exporters.
* The batch processor reduces exporter load and network chatter by grouping telemetry and flushing on a timeout or size threshold.
* Add processors to specific pipelines to apply them per-signal; multiple processors run sequentially.
* Tune `timeout` and `send_batch_size` to balance latency and throughput for your environment.

Links and references

* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
* [OTLP protocol specification](https://opentelemetry.io/docs/reference/specification/protocol/otlp/)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* telemetrygen (generate telemetry): [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/b601d1de-df58-4240-8dbb-f9a1bc9c2a20)


# Demo OTel Col Prometheus Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Demo-OTel-Col-Prometheus-Exporter/page

Guide to configure OpenTelemetry Collector, Prometheus and Jaeger with Docker Compose to push metrics to Prometheus using its remote write receiver and validate metrics in Prometheus UI

This guide shows how to push metrics from an OpenTelemetry Collector to Prometheus using Prometheus' remote write receiver. The stack uses Docker Compose to run the Collector, Prometheus, and Jaeger (for traces). You'll learn how to:

* Add Prometheus to Docker Compose and enable the remote write receiver
* Provide a Prometheus configuration suitable for receiving pushed metrics
* Configure the OpenTelemetry Collector to export metrics via `prometheusremotewrite`
* Start the stack and validate metrics in the Prometheus UI

> **lightbulb** This demonstration uses Prometheus' remote write API so the OpenTelemetry Collector can push metrics directly into Prometheus. Use this when you want the Collector to push metrics rather than having Prometheus scrape targets.

## Overview

* Add a Prometheus service to your Docker Compose file and enable the remote-write HTTP receiver.
* Mount a simple `prometheus.yml` that sets global intervals (no `scrape_configs` needed if the Collector pushes metrics).
* Configure the Collector with a `prometheusremotewrite` exporter that targets Prometheus at `http://prometheus:9090/api/v1/write`.
* Start the stack and verify metrics at `http://localhost:9090`.

## 1) Add Prometheus to Docker Compose

Update `docker-compose.yml` to include Jaeger and Prometheus services, and configure Prometheus to enable the remote write receiver:

```yaml theme={null}
version: "3.8"

services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    ports:
      - "6831:6831/udp"  # Jaeger agent - thrift compact
      - "6832:6832/udp"  # Jaeger agent - thrift binary
      - "5778:5778"      # Configs
      - "16686:16686"    # Jaeger UI (http://localhost:16686)
      - "14268:14268"    # Collector (HTTP)
      - "14250:14250"    # gRPC

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--web.enable-remote-write-receiver"
```

Ports exposed by the stack:

| Service    | Purpose / UI | Port (host:container)            |
| ---------- | ------------ | -------------------------------- |
| Jaeger     | UI / tracing | `16686:16686`                    |
| Prometheus | UI / metrics | `9090:9090`                      |
| Jaeger     | gRPC         | `14250:14250`                    |
| Jaeger     | HTTP         | `14268:14268`                    |
| Jaeger     | Agent (UDP)  | `6831:6831/udp`, `6832:6832/udp` |

Notes:

* The `--web.enable-remote-write-receiver` flag enables Prometheus to accept pushed metrics at `/api/v1/write`.
* We mount a local `prometheus.yml` to control Prometheus behavior from your project directory.

## 2) Create Prometheus configuration (prometheus.yml)

If the Collector is pushing metrics to Prometheus, you do not need `scrape_configs`. Create `prometheus.yml` beside your `docker-compose.yml`:

```yaml theme={null}
global:
  scrape_interval: 15s
  evaluation_interval: 15s
