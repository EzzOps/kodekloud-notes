# Demo OTel Col Jaeger Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Demo-OTel-Col-Jaeger-Exporter/page

Guide to configure an OpenTelemetry Collector to export traces to Jaeger via OTLP, run Collector and Jaeger with Docker Compose, generate test telemetry and verify traces in Jaeger UI

This guide shows how to configure an OpenTelemetry Collector to export traces to Jaeger using OTLP, run both the Collector and Jaeger locally with Docker Compose, and generate test telemetry to verify traces appear in the Jaeger UI.

What you'll see here:

* Overview of Collector core components
* Minimal Collector config that prints telemetry to console
* Docker Compose to run Collector + Jaeger locally
* Collector configuration updated to export to Jaeger via OTLP
* Commands to run the stack and generate telemetry
* Verification steps in Jaeger UI

OpenTelemetry Collector core components

* receivers: how the collector receives telemetry from applications
* processors: how the collector processes telemetry
* exporters: where the collector forwards telemetry for storage/analysis
* service pipelines: connect receivers → processors → exporters (configurable per-signal: traces, metrics, logs)

Minimal Collector configuration (OTLP receiver + debug exporter)
This minimal config accepts OTLP and prints received telemetry to the console via the debug exporter:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

Wire the Collector to Jaeger
In this lesson we'll send traces to Jaeger so they are stored and viewable in the Jaeger UI. We'll run Jaeger's all-in-one image and configure the Collector to export traces to Jaeger over OTLP.

Docker Compose (recommended local stack)
Use this Docker Compose fragment to run the Collector and Jaeger on a shared Compose network. The Collector reads OTLP on 4317 (gRPC) and 4318 (HTTP). Jaeger supports OTLP ingest and listens on its OTLP gRPC port (exposed here for convenience).

```yaml theme={null}
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.135.0
    container_name: otel-collector
    volumes:
      - ./otel-collector-config.yaml:/etc/otelcol-contrib/config.yaml
    ports:
      - "4317:4317" # OTLP gRPC
      - "4318:4318" # OTLP HTTP

  jaeger:
    image: jaegertracing/all-in-one
    container_name: jaeger
    ports:
      - "6831:6831/udp"  # Jaeger agent - thrift compact
      - "6832:6832/udp"  # Jaeger agent - thrift binary
      - "5778:5778"      # Configs
      - "16686:16686"    # Jaeger UI (http://localhost:16686)
      - "14268:14268"    # Collector (OTLP HTTP / thrift)
      - "14250:14250"    # gRPC
```

Ports summary

| Service            | Purpose                             | Port(s)                |
| ------------------ | ----------------------------------- | ---------------------- |
| Collector OTLP     | OTLP ingest from apps (gRPC / HTTP) | `4317` / `4318`        |
| Jaeger UI          | Web UI to view traces               | `16686`                |
| Jaeger OTLP/gRPC   | Jaeger ingest endpoints             | `14250`                |
| Jaeger agent (UDP) | Thrift-based agent ports            | `6831/udp`, `6832/udp` |

Notes

* When running both services in Docker Compose the Collector can reach Jaeger at `jaeger:4317` (the Compose service name resolves on the network).
* You do not have to expose port `4317` to the host unless you need external access to Jaeger's OTLP port.

Update the Collector configuration to export to Jaeger
Because you may have multiple OTLP exporters (to different backends), give each OTLP exporter a unique name using the `otlp/<name>` pattern. The example below defines `otlp/jaeger` and retains the console `debug` exporter:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

  debug:
    verbosity: detailed

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

> **lightbulb** When you require multiple OTLP exporters (for example, one to Jaeger and another to a different backend), name them like `otlp/jaeger` and `otlp/backend2`. Use those exact names in your pipeline exporter lists.

Start and stop the Compose stack
Start the stack in detached mode:

```bash theme={null}
docker compose up -d
```

Stop and remove containers:

```bash theme={null}
docker compose down
```

Generate test telemetry
Use the telemetrygen tool to send sample traces and logs to the Collector over OTLP HTTP. Example:

```bash theme={null}
export GOBIN=${GOBIN:-$(go env GOPATH)/bin}
$GOBIN/telemetrygen traces --otlp-http --traces 3
$GOBIN/telemetrygen logs --otlp-http --logs 3
```

Sample trimmed output (telemetrygen and Collector logs) when sending traces and logs:

```plaintext theme={null}
2025-09-29T17:09:51.954-0600  INFO  traces/traces.go:40 starting HTTP exporter
2025-09-29T17:09:56.958-0600  INFO  traces/traces.go:115 traces generated {'worker': 0, 'traces': 3}
2025-09-29T17:11:21.712-0600  INFO  logs/logs.go:30 logs generated {'worker': 0, 'logs': 3}
```

Collector console (debug exporter) output will include received span details, for example:

```plaintext theme={null}
otel-collector   Name: lets-go
otel-collector   Kind: Client
otel-collector   Start time: 2025-09-29 23:24:22.852015 +0000 UTC
otel-collector   End time: 2025-09-29 23:24:22.852138 +0000 UTC
otel-collector   Status code: Unset
otel-collector   Attributes:
otel-collector     - network.peer.address: Str(1.2.3.4)
otel-collector   ScopeSpans #0
otel-collector   InstrumentationScope telemetrygen
otel-collector   Span #0
otel-collector     Trace ID: 753fca97b9ccbc450bf4707477771b
otel-collector     Kind: Server
otel-collector     Start time: 2025-09-29 23:24:22.852288 +0000 UTC
otel-collector     End time: 2025-09-29 23:24:24.852411 +0000 UTC
otel-collector     Attributes:
otel-collector       - network.peer.address: Str(1.2.3.4)
otel-collector       - peer.service: Str(telemetrygen-client)
```

Verification in Jaeger

* Open the Jaeger UI: [http://localhost:16686](http://localhost:16686)
* Under "Services" find your service (for example, `telemetrygen`)
* Click "Find Traces" to view the traces exported by the Collector

<Frame>
  <img alt="The image shows the Jaeger UI displaying trace results for the service &#x22;telemetrygen,&#x22; including a graph of trace durations and a list of three traces with their respective details and timestamps." />
</Frame>

Links and references

* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Jaeger OTLP documentation: [https://www.jaegertracing.io/docs/1.43/deployment/#opentelemetry-collector](https://www.jaegertracing.io/docs/1.43/deployment/#opentelemetry-collector)
* telemetrygen project (example generator): [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/1e0e8bd2-7cb9-41fd-86e1-0361110b418f)
