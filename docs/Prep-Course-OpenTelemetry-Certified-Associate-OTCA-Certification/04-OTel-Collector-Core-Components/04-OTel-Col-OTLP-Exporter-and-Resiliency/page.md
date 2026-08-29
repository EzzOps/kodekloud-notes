# Example routing_key choices (pick one)
# 1) traceID - traces (default for traces)
exporters:
  loadbalancing:
    routing_key: "traceID"   # Keep all spans of a trace together

# 2) service - traces/metrics (default for metrics)
exporters:
  loadbalancing:
    routing_key: "service"   # Group by service.name

# 3) resource - traces/metrics
exporters:
  loadbalancing:
    routing_key: "resource"  # Group by resource attributes

# 4) metric - metrics only
exporters:
  loadbalancing:
    routing_key: "metric"    # Group by metric name

# 5) streamID - metrics only (most granular)
exporters:
  loadbalancing:
    routing_key: "streamID"

# 6) attributes - custom attribute routing
exporters:
  loadbalancing:
    routing_key: "attributes"
    routing_attributes:
      - "span.kind"
      - "http.method"
```

Resolvers — how the exporter discovers backend collectors

Resolvers determine how the load-balancing exporter discovers its backend pool. Select a resolver that matches your infrastructure and operational model.

|                       Resolver | Typical use case                            | Notes                                                                                   |
| -----------------------------: | ------------------------------------------- | --------------------------------------------------------------------------------------- |
|                       `static` | Small or fixed deployments                  | Use when backend hostnames are known and stable.                                        |
|                          `dns` | Cloud load-balancers or DNS-based discovery | Resolve a DNS name to multiple IPs; the exporter can poll DNS at a configured interval. |
|                          `k8s` | Kubernetes headless services                | Discover pods from a headless K8s service by name and port(s).                          |
| Other cloud-specific resolvers | Vendor/cloud integrations                   | Some Collector builds include additional resolvers (check your distribution docs).      |

Example: resolver types

```yaml theme={null}
# Static resolver - fixed backends
exporters:
  loadbalancing:
    routing_key: "traceID"
  resolver:
    static:
      hostnames:
        - backend-1.example.com:4317
        - backend-2.example.com:4317
        - backend-3.example.com:4317

# DNS resolver - dynamic discovery
exporters:
  loadbalancing:
    routing_key: "service"
  resolver:
    dns:
      hostname: collectors.svc.cluster.local
      port: 4317
      interval: 5s   # poll interval for DNS updates
      timeout: 1s

# Kubernetes resolver - K8s service discovery
exporters:
  loadbalancing:
    routing_key: "traceID"
  resolver:
    k8s:
      service: otel-collector-headless
      ports:
        - 4317
        - 4318
```

How the exporter maintains consistency and reliability

* Per-backend sub-exporters: the load-balancing exporter instantiates an OTLP sub-exporter per backend so each backend maintains independent queues and retry behavior.
* Consistent mapping: the exporter hashes the selected routing key to consistently route items with the same key to the same backend.
* Resilience: combined with exporter-level queues and retry\_on\_failure settings, this delivers robust forwarding even during transient backend issues.

<Frame>
  <img alt="The image presents information about a &#x22;Load-Balancing Exporter&#x22; and explains the importance of consistent routing for distributing traffic and ensuring data consistency across backends." />
</Frame>

The load-balancing exporter guarantees stickiness using the selected routing key (for example, trace ID or service name). Choose a resolver type that matches your environment to discover the backend pool either statically or dynamically.

<Frame>
  <img alt="The image describes how a load-balancing exporter achieves consistent routing, using a routing key, supporting various resolvers, creating sub-exporters per backend, and maintaining consistent routing." />
</Frame>

Tail-based sampling with a load-balancing exporter

Tail-based sampling often runs on downstream collectors. If the load-balancing exporter keeps all spans of a trace on the same backend, downstream tail samplers can see the entire trace without cross-node coordination, enabling accurate sampling decisions.

<Frame>
  <img alt="The image is a slide titled &#x22;Load-Balancing Exporter: Tail Sampling Setup with Load Balancing,&#x22; showing a typical setup involving tail-based sampling on downstream collectors and routing all spans for a trace to the same backend." />
</Frame>

Illustration of consistent routing

Within the load-balancing collector, spans (or metric streams) that share the same routing key are hashed or consistently mapped to the same backend so each backend receives all data for that key.

<Frame>
  <img alt="The image illustrates consistent routing using LB Exporter, showing a circular node diagram directing packets with different resolver badges to various server collectors." />
</Frame>

Typical exporter configuration (production-minded)

The example below shows a production-oriented configuration using OTLP transport, a `static` resolver, exporter-level queuing, and retry settings. Adjust `routing_key`, resolver type, and timeouts to fit your deployment.

```yaml theme={null}
exporters:
  loadbalancing:
    routing_key: "traceID"   # pick routing key appropriate for your use case

    protocol:
      otlp:
        timeout: 1s
        tls:
          insecure: false

    resolver:
      static:
        hostnames:
          - backend-1.example.com:4317
          - backend-2.example.com:4317
          - backend-3.example.com:4317

# Exporter-level resilience
sending_queue:
  enabled: true
  queue_size: 20000

retry_on_failure:
  enabled: true
  max_elapsed_time: 5m

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [loadbalancing]
```

Notes and caveats

* `metric` and `streamID` routing keys are valid only for metrics; they are not applicable to traces or logs.
* Select `static` for fixed backend pools, `dns` for DNS-based discovery in cloud deployments, and `k8s` for Kubernetes headless services.
* Downstream backends must be able to handle the grouped load and any tail-sampling processors you plan to run.
* Monitor and tune per-backend queue sizes, retry settings, and OTLP timeouts to avoid dropped telemetry during spikes.

Links and references

* [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
* [OTLP Protocol Overview](https://github.com/open-telemetry/opentelemetry-proto)
* [Kubernetes Services (headless)](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/824c4579-1751-4525-9ebb-6b47f45af0e4" />
</CardGroup>


# OTel Col OTLP Exporter and Resiliency

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/OTel-Col-OTLP-Exporter-and-Resiliency/page

Overview of configuring and hardening the OpenTelemetry Collector OTLP exporter for secure, resilient production exports of traces metrics and logs including TLS compression retry queuing and timeouts

Now let's examine the OTLP exporter in the OpenTelemetry Collector and the configuration options you can use to make it resilient and production-ready.

The OTLP exporter sends telemetry using the OpenTelemetry Protocol (OTLP) and supports all signal types—traces, metrics, and logs. It can transport data over gRPC (the default) or HTTP, and supports features such as TLS/mTLS, gzip compression, retry, queuing, and timeouts to reduce data loss risk.

<Frame>
  <img alt="The image describes the OTLP Exporter (gRPC) and its functionalities, including exporting via OpenTelemetry Protocol, supporting traces, metrics, logs, ensuring zero data loss with full fidelity export, and using gzip compression." />
</Frame>

Key capabilities:

* Exports traces, metrics, and logs with full fidelity (best-effort delivery).
* Supports compression (gzip) to reduce bandwidth.
* Common use cases: forward data to another collector or to an OTLP-compatible backend.

Transport: gRPC vs HTTP

* gRPC (OTLP/gRPC): typical choice for efficient binary transport and streaming RPCs.
* HTTP (OTLP/HTTP): use when gRPC is blocked by firewalls, proxies, or when backends only support HTTP. OTLP/HTTP supports both Protocol Buffers (`proto`) and JSON encodings and also supports gzip if both client and server accept it.

Example OTLP/HTTP exporter:

```yaml theme={null}
exporters:
  otlphttp:
    endpoint: https://backend.example.com:4318
    encoding: proto
    compression: gzip
    headers:
      api-key: "your-api-key"
```

Exporter configuration commonly includes:

* `endpoint`: destination host:port or URL
* TLS settings: TLS, mTLS, or `insecure` (only for testing)
* `headers` or authenticator extension references for authentication
* Resiliency/backpressure controls: `retry_on_failure`, `sending_queue`, and `timeout`

<Frame>
  <img alt="The image outlines the components of an exporter configuration, including details on endpoints, TLS certificates, headers, authentication extensions, and resilience features like retry and timeout." />
</Frame>

Example configuration demonstrating TLS, sending queue, retry behavior, and RPC timeout:

```yaml theme={null}
exporters:
  otlp/primary:
    endpoint: export.vendorname.example.com:4317
    tls:
      insecure: false
    sending_queue:
      queue_size: 2048
    retry_on_failure:
      enabled: true
      max_elapsed_time: 10m
    timeout: 10s
```

How these fields behave:

* `timeout`: per-RPC timeout (here 10s) — how long each export attempt can take before being cancelled.
* `retry_on_failure`: enables exponential/backoff retries; `max_elapsed_time` caps total retry duration (here 10 minutes).
* `sending_queue.queue_size`: number of telemetry items buffered while retrying or during backpressure.

Exporter configuration quick reference

| Configuration key  | Purpose                                   | Example                                                       |
| ------------------ | ----------------------------------------- | ------------------------------------------------------------- |
| `endpoint`         | Destination for exported telemetry        | `export.vendorname.example.com:4317`                          |
| `tls`              | TLS or mTLS settings for secure transport | `tls:\n  insecure: false`                                     |
| `sending_queue`    | Buffer telemetry during spikes/outages    | `sending_queue:\n  queue_size: 2048`                          |
| `retry_on_failure` | Control retries and max retry duration    | `retry_on_failure:\n  enabled: true\n  max_elapsed_time: 10m` |
| `timeout`          | Per-RPC export timeout                    | `timeout: 10s`                                                |
| `compression`      | Reduce bandwidth (gzip)                   | `compression: gzip`                                           |

Authentication and secrets
Exporters often require credentials or tokens. Common approaches:

* Static headers (quick tests; not recommended for production).
* Authenticator extensions (e.g., OAuth2/OIDC flows) the exporter can reference to retrieve tokens.
* Environment variables or secret stores (recommended) to avoid embedding secrets in config.

<Frame>
  <img alt="The image illustrates authentication options for exporters, detailing static headers, authenticator extensions, and environment variables for handling secrets." />
</Frame>

<Callout icon="lightbulb">
  For production, avoid hard-coding secrets in config. Externalize tokens (for example, via a secrets manager or Vault) and reference them through an auth extension or environment variables so the exporter can attach bearer tokens without secrets in plaintext.
</Callout>

Resiliency best practices

* Batch telemetry before exporting to reduce overhead and round trips.
* Use a queued retry (`sending_queue` + `retry_on_failure`) to buffer spikes and survive brief outages.
* Set realistic `timeout` values aligned with network latency and backend performance.
* Enable compression (gzip) to reduce bandwidth usage.

<Frame>
  <img alt="The image outlines core settings for exporter resilience, including batching, queued-retry, timeouts, and compression/encoding. These elements are presented in colorful blocks with descriptions." />
</Frame>

Batching configuration example (use the batch processor to coalesce telemetry into larger payloads):

```yaml theme={null}
processors:
  batch:
    send_batch_size: 8192
    timeout: 5s
```

* Increase `send_batch_size` to send fewer, larger payloads while tuning `timeout` so batches flush regularly.
* Batching reduces per-item overhead and lowers the number of outbound requests.

Debugging and troubleshooting
Use the debug exporter (or logging exporter) to print outgoing telemetry to the collector logs. This is useful during development and troubleshooting to inspect what the Collector is sending.

Basic debug exporter and enabling debug logs:

```yaml theme={null}
exporters:
  debug:
    verbosity: normal

service:
  telemetry:
    logs:
      level: "debug"
```

More detailed logging with sampling:

```yaml theme={null}
exporters:
  debug:
    verbosity: detailed
    sampling_initial: 5
    sampling_thereafter: 200
```

* `verbosity`: `basic`, `normal`, or `detailed`
* `sampling_initial` / `sampling_thereafter`: limit log volume on chatty exporters

Enable the debug exporter early in development to validate pipeline behavior and surface processing errors.

Links and references

* OpenTelemetry Protocol (OTLP) overview: [https://github.com/open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification)
* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OAuth2: [https://oauth.net/2/](https://oauth.net/2/)
* OpenID Connect (OIDC): [https://openid.net/connect/](https://openid.net/connect/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/cb69236b-8517-4e0c-9adc-52aa97517d91" />
</CardGroup>
