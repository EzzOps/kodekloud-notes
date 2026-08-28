# OTel Col Contrib Exporters

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/OTel-Col-Contrib-Exporters/page

Guide to community and vendor OpenTelemetry Collector contrib exporters, their use cases, configuration options, and YAML examples for sending traces metrics and logs to various backends.

This guide reviews commonly used contrib exporters available for the OpenTelemetry Collector. Contrib exporters are community- and vendor-provided integrations that convert and forward telemetry (traces, metrics, logs) to various backends or protocols. Use this reference to choose the right exporter for your backend, understand common configuration options, and see practical YAML examples.

Below is a quick summary of the most common exporters covered in this article.

| Exporter                | Primary Use Case                                        | Typical Integration                                  |
| ----------------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| Prometheus (scrape)     | Expose metrics endpoint to be scraped                   | Prometheus + Grafana                                 |
| Prometheus Remote Write | Push metrics to Prometheus-compatible long-term storage | Cortex, Thanos, remote Prometheus stores             |
| Zipkin                  | Send spans to Zipkin over HTTP                          | Zipkin UI/collector                                  |
| Jaeger                  | Send spans to Jaeger collector (gRPC/HTTP)              | Jaeger backend                                       |
| Kafka                   | Stream telemetry to Kafka topics                        | Large-scale pipelines, downstream consumers          |
| File                    | Write OTLP payloads to local files                      | Debugging, offline analysis                          |
| Vendor-specific         | Proprietary protocols or auth                           | Vendor-managed backends (API keys, custom encodings) |

<Callout icon="lightbulb">
  Check the OpenTelemetry Collector contrib repository for a complete list of exporters and examples: [https://github.com/open-telemetry/opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib). There are many vendor and community exporters beyond the ones shown here.
</Callout>

<Frame>
  <img alt="The image is a list titled &#x22;Community and Vendor Exporters&#x22; with options like Prometheus, Zipkin, Jaeger, Kafka, file, and vendor-specific exporters, each describing its function." />
</Frame>

## Prometheus exporter

The Prometheus exporter exposes an HTTP endpoint from the Collector so a Prometheus server can scrape metrics directly. Configure listening endpoint, metric namespace, and constant labels to integrate seamlessly with an existing Prometheus stack.

When to use:

* You run Prometheus as the primary metrics scraper.
* You want Prometheus/Grafana to scrape metrics directly from the Collector rather than using a push model.

Example configuration:

```yaml theme={null}
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: "otel"
    const_labels:
      environment: "production"

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

## Prometheus Remote Write exporter

The Prometheus Remote Write exporter converts OTLP metrics into Prometheus Remote Write format and pushes them to a remote backend (for example, Cortex or Thanos). Use this when you need centralized, long-term metrics storage or to offload historical metrics to a remote store.

When to use:

* Centralized storage and long-term retention are required.
* You want to run PromQL over a remote store.

Example configuration:

```yaml theme={null}
exporters:
  prometheusremotewrite:
    endpoint: "https://prom.example.com/api/v1/push"
    tls:
      insecure: false
    external_labels:
      cluster: "production"

processors:
  batch: {}

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheusremotewrite]
```

After you push data, query the remote store with PromQL (for example, `rate(http_requests_total[5m])`) and visualize with Grafana or use alerting rules as usual.

## Jaeger exporter

The Jaeger exporter converts OTLP spans to Jaeger’s native format and sends them to a Jaeger collector (gRPC or HTTP). This is helpful for organizations that already use Jaeger for trace visualization or are migrating to OTLP.

Example configuration:

```yaml theme={null}
exporters:
  jaeger:
    endpoint: "jaeger.example.com:14250"
    # For gRPC transport you may specify:
    # tls:
    #   insecure: false

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
```

## Zipkin exporter

The Zipkin exporter sends spans to a Zipkin backend over HTTP and supports JSON or Protobuf encodings to maintain compatibility with different Zipkin receivers and versions.

Example configuration:

```yaml theme={null}
exporters:
  zipkin:
    endpoint: "http://zipkin.example.com:9411/api/v2/spans"
    format: "proto"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [zipkin]
```

## Using multiple trace exporters

The Collector can deliver the same traces to multiple exporters in parallel. This is useful for gradual migrations, duplicating traces to different backends, or mixing SaaS and self-hosted observability.

Example — send traces to both Zipkin and Jaeger:

```yaml theme={null}
exporters:
  zipkin:
    endpoint: "http://zipkin.example.com:9411/api/v2/spans"
  jaeger:
    endpoint: "jaeger.example.com:14250"

processors:
  batch: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [zipkin, jaeger]
```

## Kafka exporter

The Kafka exporter forwards telemetry to Kafka topics and supports per-signal topics (traces, metrics, logs), encoding options, partitioning, and authentication/TLS settings. Kafka is a good fit for large-scale, decoupled pipelines where multiple downstream consumers process raw OTLP payloads.

When to use:

* You need durable, scalable streaming of telemetry.
* Downstream consumers expect telemetry on Kafka topics (e.g., for enrichment, storage, or reprocessing).

Example configuration with authentication, batching, and per-signal topics:

```yaml theme={null}
exporters:
  kafka:
    brokers:
      - "kafka-1:9092"
      - "kafka-2:9092"
      - "kafka-3:9092"
    protocol_version: "2.8.0"
    client_id: "otel-collector"
    # Signal-specific topics and encodings
    traces:
      topic: "otlp-traces"
      encoding: "otlp_proto"
    metrics:
      topic: "otlp-metrics"
      encoding: "otlp_proto"
    logs:
      topic: "otlp-logs"
      encoding: "otlp_proto"
    # Partitioning options
    partition_traces_by_id: true
    partition_metrics_by_resource_attributes: true

    auth:
      sasl:
        mechanism: "PLAIN"
        username: "${KAFKA_USER}"
        password: "${KAFKA_PASSWORD}"
      tls:
        insecure: false

processors:
  batch:
    send_batch_size: 1024
    timeout: 10s

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [kafka]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [kafka]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [kafka]
```

<Callout icon="warning">
  Do not hard-code secrets (for example, `KAFKA_PASSWORD`) directly in Collector YAML. Use environment variables, secret mounts, or your orchestration platform's secret management to protect sensitive credentials.
</Callout>

## File exporter

The file exporter writes telemetry to local files (commonly OTLP JSON). This exporter is useful for debugging, snapshots, or offline analysis when no remote backend is available. File rotation parameters help manage disk usage.

Example configuration:

```yaml theme={null}
exporters:
  file:
    path: "/var/log/otel/data.json"
    rotation:
      max_megabytes: 100
      max_backups: 10
      max_days: 7

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [file]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [file]
```

## Vendor-specific exporters

Many observability vendors provide custom exporters that implement proprietary protocols, required authentication, or additional features (for example, API keys, custom headers, or non-OTLP encodings). Use vendor exporters when integrating with a managed backend to ensure compatibility and to leverage vendor-specific optimizations.

When to use:

* A vendor-managed backend requires a specific protocol or authentication method.
* You want to use vendor-supported features like enhanced metadata enrichment, sampling controls, or billing-aware routing.

## Closing notes

* Choose exporters that match your backend and operational model (scrape vs push, long-term storage, streaming).
* Use `batch` and `retry` processors to improve reliability and reduce network overhead.
* Keep secrets out of config files — use environment variables or secret mounts.
* For examples and a comprehensive list of exporters, consult the OpenTelemetry Collector contrib repository: [https://github.com/open-telemetry/opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)

Links and references

* OpenTelemetry Collector contrib repository: [https://github.com/open-telemetry/opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* PromQL basics: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* Cortex: [https://cortexmetrics.io/](https://cortexmetrics.io/)
* Thanos: [https://thanos.io/](https://thanos.io/)
* Kafka: [https://kafka.apache.org/](https://kafka.apache.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/acbb5dd7-b27b-4109-a6c6-eaf92c79e6cb" />
</CardGroup>
