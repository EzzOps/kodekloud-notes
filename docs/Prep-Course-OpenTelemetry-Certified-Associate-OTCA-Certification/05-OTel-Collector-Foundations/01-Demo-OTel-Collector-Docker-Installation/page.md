# Demo OTel Collector Docker Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/Demo-OTel-Collector-Docker-Installation/page

Guide to run OpenTelemetry Collector locally with Docker Compose, providing minimal OTLP receiver configuration, docker-compose setup, and instructions to expose ports 4317 and 4318.

This guide shows how to run the OpenTelemetry Collector locally using Docker Compose. You'll:

* create a minimal collector configuration that listens for OTLP (gRPC and HTTP),
* write a `docker-compose.yaml` that mounts the config into the container and forwards host ports,
* start the collector with `docker compose up`.

References:

* OpenTelemetry Collector docs: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* otel/opentelemetry-collector Docker Hub: [https://hub.docker.com/r/otel/opentelemetry-collector](https://hub.docker.com/r/otel/opentelemetry-collector)
* otel/opentelemetry-collector-contrib Docker Hub: [https://hub.docker.com/r/otel/opentelemetry-collector-contrib](https://hub.docker.com/r/otel/opentelemetry-collector-contrib)

## 1) Minimal collector configuration

Save the following as `otel-collector-config.yaml`. This config enables the OTLP receiver (gRPC and HTTP) and a `debug` exporter for traces, metrics, and logs.

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

Important: the collector listens on port `4317` for OTLP/gRPC and `4318` for OTLP/HTTP. When running in Docker, these container ports must be published to the host.

## 2) Choose an image

You can pick either the core or contrib image from Docker Hub:

* Core: `otel/opentelemetry-collector` — a minimal set of components.
* Contrib: `otel/opentelemetry-collector-contrib` — includes many additional receivers, exporters and processors.

Tip: pin a tag to lock a specific version, for example:

```bash theme={null}
docker pull otel/opentelemetry-collector-contrib:0.135.0
```

## 3) docker-compose.yaml

Create a `docker-compose.yaml` next to your `otel-collector-config.yaml`. This example:

* uses the contrib image,
* mounts the local config into the container at the collector's default path,
* exposes ports `4317` and `4318`,
* sets a readable container name.

Save as `docker-compose.yaml`:

```yaml theme={null}
version: "3.8"

services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.135.0
    container_name: otel-collector
    volumes:
      - ./otel-collector-config.yaml:/etc/otelcol/config.yaml
    ports:
      - "4317:4317"
      - "4318:4318"
```

## Mount path and --config flag

<Callout icon="lightbulb">
  If you mount the config file to a non-default path inside the container, pass the `--config` flag via the `command:` field in your compose file. In the example above we mount to `/etc/otelcol/config.yaml`, which is the collector's default config path, so no `command:` is necessary.
</Callout>

## 4) Start the collector

From the directory containing both files:

```bash theme={null}
docker compose up
```

You should see the collector start and state that its gRPC and HTTP listeners are ready. Example (truncated):

```bash theme={null}
[+] Running 1/1
✔ Container otel-collector  Created
Attaching to otel-collector
otel-collector | 2025-09-29T22:23:04.586Z info  service@v0.135.0/service.go:211 Starting otelcol-contrib...{"resource": {"service.instance.id": "e2dd07fc-68be-4ba4-8ddc-a864af714095", "service.name": "otelcol-contrib", "service.version": "0.135.0"}, "NumCPUs": 16}
otel-collector | 2025-09-29T22:23:04.586Z info  extensions/extensions.go:41 Starting extensions... {"resource": {"service.instance.id": "e2dd07fc-68be-4ba4-8ddc-a864af714095", "service.name": "otelcol-contrib", "service.version": "0.135.0"}}
otel-collector | 2025-09-29T22:23:04.586Z info  otlpreceiver@v0.135.0/otlpreceiver.go:121 Starting GRPC server{"resource": {"service.instance.id": "e2dd07fc-68be-4ba4-8ddc-a864af714095", "service.name": "otelcol-contrib", "service.version": "0.135.0"}, "otelcol.component.id": "otlp", "endpoint": "[::]:4317"}
otel-collector | 2025-09-29T22:23:04.586Z info  otlpreceiver@v0.135.0/otlpreceiver.go:179 Starting HTTP server{"resource": {"service.instance.id": "e2dd07fc-68be-4ba4-8ddc-a864af714095", "service.name": "otelcol-contrib", "service.version": "0.135.0"}, "otelcol.component.id": "otlp", "endpoint": "[::]:4318"}
otel-collector | 2025-09-29T22:23:04.587Z info  service@v0.135.0/service.go:234 Everything is ready. Begin running and processing data. {"resource": {"service.instance.id": "e2dd07fc-68be-4ba4-8ddc-a864af714095", "service.name": "otelcol-contrib", "service.version": "0.135.0"}}
```

## Quick reference

| Item            | Description                                                | Example / Command                              |
| --------------- | ---------------------------------------------------------- | ---------------------------------------------- |
| Config file     | Collector config enabling OTLP receiver and debug exporter | `otel-collector-config.yaml` (see above)       |
| Collector image | Choose core or contrib from Docker Hub                     | `otel/opentelemetry-collector-contrib:0.135.0` |
| Ports           | Host-to-container forwarding for OTLP                      | `4317:4317` (gRPC), `4318:4318` (HTTP)         |
| Start command   | Bring container up with Compose                            | `docker compose up`                            |

## Troubleshooting

<Callout icon="warning">
  If you see an error about a conflicting container name (for example: "Conflict. The container name "/otel-collector" is already in use..."), either remove or rename the existing container before reusing that name:

  * Remove: `docker rm -f otel-collector`
  * Or choose a different `container_name` in the compose file.
</Callout>

That's it — your OpenTelemetry Collector is now running in Docker and ready to receive OTLP traffic on ports 4317 (gRPC) and 4318 (HTTP).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/cb582f0a-1013-4d4c-a00b-bead7ffff9c7" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/d38de21f-be62-49a6-8543-9f2980326dc2" />
</CardGroup>
