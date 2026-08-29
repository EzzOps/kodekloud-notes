# Demo OTel Collector Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/Demo-OTel-Collector-Installation/page

How to download, configure, and run OpenTelemetry Collector otelcol-contrib on Linux ARM64 to receive OTLP traces and metrics with a minimal config.

This lesson shows how to download, extract, configure, and run the OpenTelemetry Collector binary (`otelcol-contrib`) on a Linux ARM64 host. You'll learn how to pick the right release, place a minimal config file, and start the collector to receive OTLP telemetry (traces and metrics).

Overview

* Select the correct release for your OS/architecture from the OpenTelemetry Collector Releases on GitHub: [https://github.com/open-telemetry/opentelemetry-collector-releases/releases](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)
* Download the appropriate tarball (example used in this lesson: `otelcol-contrib_0.135.0_linux_arm64.tar.gz`)
* Extract the tarball and run `otelcol-contrib` with a configuration file (`--config`)

<Callout icon="lightbulb">
  Ensure you download the binary that matches your OS and CPU architecture (for example, `linux/amd64` vs `linux/arm64`). This lesson demonstrates the Linux/ARM64 tarball.
</Callout>

## Quick commands (summary)

| Step             | Command / Action                                      | Notes                                            |
| ---------------- | ----------------------------------------------------- | ------------------------------------------------ |
| Download release | See the Releases page above                           | Pick the tarball for your platform               |
| Extract tarball  | `tar -xzf otelcol-contrib_0.135.0_linux_arm64.tar.gz` | Produces the `otelcol-contrib` binary (and docs) |
| Start collector  | `./otelcol-contrib --config=config.yaml`              | `--config` points to the collector config file   |
| Validate config  | `./otelcol-contrib validate --config=config.yaml`     | Validate config without running                  |

## 1) Download and extract the release tarball

From the GitHub Releases page, download the tarball matching your platform. Example filename used in this lesson:

`otelcol-contrib_0.135.0_linux_arm64.tar.gz`

Extract the tarball (run from the directory containing the downloaded file):

```bash theme={null}
user1@prometheus1:~/opentelemetry$ tar -xzf otelcol-contrib_0.135.0_linux_arm64.tar.gz
```

After extraction you will have the `otelcol-contrib` binary (plus documentation). The binary is all that’s required for this demo.

## 2) Check flags and required config

If you run the collector without a configuration file, it will exit with an error:

```bash theme={null}
user1@prometheus1:~/opentelemetry$ ./otelcol-contrib
Error: at least one config flag must be provided
2025/09/29 21:59:02 collector server run finished with error: at least one config flag must be provided
```

To view available flags and commands:

```bash theme={null}
user1@prometheus1:~/opentelemetry$ ./otelcol-contrib --help
Usage:
  otelcol-contrib [flags]
  otelcol-contrib [command]

Available Commands:
  completion            Generate the autocompletion script for the specified shell
  components            Outputs available components in this collector distribution
  featuregate           Display feature gates information
  help                  Help about any command
  print-initial-config  Prints the Collector's configuration in YAML format after all config sources are resolved and merged
  validate              Validates the config without running the collector

Flags:
      --config string       Locations to the config file(s), e.g. --config=file:/path/to/first --config=file:/path/to/second
  -v, --version             Print version for otelcol-contrib
  ... [other flags omitted for brevity]
```

Note: the important flag is `--config` (or `--config=file:/path/to/config.yaml`), which tells the collector where to load its configuration.

## 3) Minimal configuration example

Create a minimal `config.yaml` that accepts OTLP telemetry (traces and metrics) and uses the `debug` exporter (prints telemetry to the console). Save this file in the same directory as the `otelcol-contrib` binary:

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
```

This minimal config is useful for testing and local development. For production deployments you will typically add processors, exporters (e.g., OTLP/gRPC to backends), and security settings.

## 4) Start the collector with the config

Run the collector and point it at the config file:

```bash theme={null}
user1@prometheus1:~/opentelemetry$ ./otelcol-contrib --config=config.yaml
```

Representative startup logs:

```bash theme={null}
2025-09-29T22:01:13.368Z  info  service@v0.135.0/service.go:211    Starting otelcol-contrib {"service.name":"otelcol-contrib","service.version":"0.135.0","NumCPU":2}
2025-09-29T22:01:13.368Z  info  extensions/extensions.go:41       Starting extensions {"version":"0.135.0","service.name":"otelcol-contrib"}
2025-09-29T22:01:13.368Z  info  otlpreceiver/otlp.go:121          Starting OTLP receiver {"version":"0.135.0","service.name":"otelcol-contrib"}
2025-09-29T22:01:13.368Z  info  otlptracereceiver/otlp.go:179     Starting HTTP server {"service.name":"otelcol-contrib","endpoint":"[::]:4318"}
2025-09-29T22:01:13.368Z  info  otlpreceiver/otlp.go:279          Starting gRPC server {"service.name":"otelcol-contrib","endpoint":"[::]:4317"}
2025-09-29T22:01:13.368Z  info  service.go:234                     Everything is ready. Begin running and processing data.
```

From the config and logs you can verify:

* OTLP gRPC is listening on port `4317`
* OTLP HTTP is listening on port `4318`
* The `debug` exporter logs telemetry to stdout for inspection

Ports and endpoints

| Protocol  | Endpoint                | Use case                |
| --------- | ----------------------- | ----------------------- |
| OTLP gRPC | `localhost:4317`        | gRPC-based OTLP clients |
| OTLP HTTP | `http://localhost:4318` | HTTP-based OTLP clients |

## 5) Validate and troubleshoot

* Validate configuration without running the collector:

```bash theme={null}
./otelcol-contrib validate --config=config.yaml
```

* If the collector fails to start, check:
  * Binary architecture vs OS/CPU (ARM64 vs AMD64)
  * File permissions (make binary executable: `chmod +x otelcol-contrib`)
  * Config syntax and indentation (YAML errors)
  * Port conflicts on `4317` / `4318`

<Callout icon="warning">
  If you see startup errors related to configuration or ports, use the `validate` command and inspect the logs printed by the `debug` exporter. Also confirm the downloaded binary matches your system architecture.
</Callout>

## 6) Next steps

* Send telemetry to the collector:
  * gRPC OTLP clients -> `localhost:4317`
  * HTTP OTLP clients -> `http://localhost:4318`
* For production usage, extend the configuration with processors (batching, sampling), secure receivers (TLS/auth), and exporters to your backend (e.g., OTLP/gRPC to an observability platform).
* Explore `otelcol-contrib components` to list available receivers/exporters/processors in the binary.

Links and references

* OpenTelemetry Collector Releases: [https://github.com/open-telemetry/opentelemetry-collector-releases/releases](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)
* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/a779bfd1-4ebf-4c16-9717-66ac2b81ba3d" />
</CardGroup>
