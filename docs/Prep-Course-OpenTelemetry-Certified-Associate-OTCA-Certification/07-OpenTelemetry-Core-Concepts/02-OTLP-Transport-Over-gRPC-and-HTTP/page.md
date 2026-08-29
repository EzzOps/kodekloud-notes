# OTLP Transport Over gRPC and HTTP

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OTLP-Transport-Over-gRPC-and-HTTP/page

Explains OTLP telemetry transport over gRPC and HTTP, comparing encodings, endpoints, performance, and recommended use cases for traces, metrics, and logs.

Once telemetry is structured and serialized, it still needs to travel from the application to a collector or backend. OTLP (OpenTelemetry Protocol) supports two transport methods—gRPC and HTTP—that carry the same OTLP payloads (traces, metrics, logs) but use different transport layers and encodings.

* OTLP over gRPC — the default, streaming-based approach (recommended for production).
* OTLP over HTTP — a request-based alternative often easier to traverse firewalls and HTTP-only gateways.

<Frame>
  <img alt="The image is a diagram describing two transport protocols used by OTLP: OTLP over gRPC and OTLP over HTTP." />
</Frame>

Both transports carry the same OTLP data model; the primary differences are transport and encoding choices.

## gRPC (recommended)

For production communication between SDKs and the OpenTelemetry Collector (or other backends), gRPC is usually the best choice because of its streaming and multiplexing capabilities.

Typical layer stack:

* OTLP signals: traces, metrics, logs.
* Protobuf binary encoding (compact, schema-driven).
* gRPC framework (RPC methods, streaming semantics).
* HTTP/2 transport (multiplexing, flow control, header compression).

<Frame>
  <img alt="The image illustrates the OTLP over gRPC, showing layers from HTTP/2 Transport and gRPC Framework down to Protobuf Binary Encoding and OTLP Signals, which include Traces, Metrics, and Logs." />
</Frame>

Key properties of OTLP over gRPC:

* Requires HTTP/2 as the transport protocol.
* Default port: `4317` (configurable).
* Persistent connections with multiplexed streams over a single TCP connection.
* Bidirectional streaming, built-in flow control, and header compression (HPACK).
* Efficient, low-latency; often the best choice for SDK-to-collector communication.

<Frame>
  <img alt="The image is a diagram titled &#x22;OTLP Over gRPC&#x22; highlighting key features like multiplexing, bidirectional streaming support, and built-in flow control with header compression." />
</Frame>

<Callout icon="warning">
  gRPC requires HTTP/2. If your environment, proxy, or gateway does not support HTTP/2 (or enforces HTTP/1.x only), prefer OTLP over HTTP.
</Callout>

## OTLP over HTTP (Protobuf encoding)

When gRPC is not available or desired, OTLP payloads can be sent over HTTP POST requests using Protobuf binary encoding. This preserves the compact, schema-driven serialization while using familiar HTTP semantics.

Typical flow:

* OTLP signals → Protobuf binary encoding.
* HTTP POST with `Content-Type: application/x-protobuf`.
* Transport over HTTP/1.1 or HTTP/2 (HTTP/2 is optional).
* Endpoints: `/v1/traces`, `/v1/metrics`, `/v1/logs`.
* Default port: `4318` (configurable).

Use cases: firewalls or proxies that favor plain HTTP traffic, or environments where gRPC is blocked.

## OTLP over HTTP (JSON encoding)

HTTP transport can also send Protobuf-defined messages encoded as JSON. JSON payloads are human-readable and useful for debugging, but they are larger and slower to parse than binary Protobuf.

Flow for JSON encoding:

* OTLP signals → Protobuf → JSON encoding.
* HTTP POST with `Content-Type: application/json`.
* Transport over HTTP/1.1 or HTTP/2.
* Same endpoints: `/v1/traces`, `/v1/metrics`, `/v1/logs`.

<Frame>
  <img alt="The image illustrates the process of OTLP (OpenTelemetry Protocol) over HTTP with JSON encoding, highlighting HTTP transport layers and endpoint mapping for traces, metrics, and logs." />
</Frame>

JSON example (OTLP-like structure) — useful for debugging and inspection:

```json theme={null}
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          { "key": "service.name", "value": { "stringValue": "my-service" } }
        ]
      },
      "scopeSpans": [ /* ... */ ]
    }
  ]
}
```

## Routing and endpoints

Routing differs between gRPC and HTTP:

* gRPC: a single endpoint (for example `collector.example.com:4317`) exposes multiple RPC services and methods (as defined in the OTLP protobuf). All signals share the same connection and are routed by gRPC service/method names.
* HTTP: the SDK/client constructs full URLs by appending specific paths to a base endpoint (for example `https://collector.example.com:4318/v1/traces`).

From a configuration perspective:

* gRPC — typically configure just the endpoint host and port (e.g., `collector.example.com:4317`).
* HTTP — configure the base endpoint and let the SDK append `/v1/traces`, `/v1/metrics`, `/v1/logs`.

<Frame>
  <img alt="The image compares gRPC and HTTP endpoint routing, highlighting gRPC's use of a single endpoint for multiple services and HTTP's use of separate URL paths and endpoints. It includes configuration details and examples for both protocols." />
</Frame>

## End-to-end transport flow

A succinct view of the telemetry journey:

1. Application generates telemetry (traces, metrics, logs).
2. OTLP SDK structures data (resource → scope → signals).
3. Serialization: data encoded as binary Protobuf or JSON-encoded Protobuf.
4. Transport:
   * gRPC: binary Protobuf over HTTP/2 (default port `4317`).
   * HTTP: Protobuf binary (`application/x-protobuf`) or JSON (`application/json`) over HTTP/1.1 or HTTP/2 (default port `4318`).
5. Backend (collector or observability backend) receives, processes, and optionally forwards/exports the data.

<Frame>
  <img alt="The image illustrates the OTLP (OpenTelemetry Protocol) transport flow from application telemetry generation to backend processing, detailing steps like SDK data structuring, Protobuf serialization, transport via gRPC or HTTP, and final backend reception and processing." />
</Frame>

## Comparison at a glance

|            Feature |                                      gRPC + Protobuf |                                                          HTTP + Protobuf |                                                     HTTP + JSON |
| -----------------: | ---------------------------------------------------: | -----------------------------------------------------------------------: | --------------------------------------------------------------: |
|       Default port |                                               `4317` |                                                                   `4318` |                                                          `4318` |
| Transport protocol |                                      Requires HTTP/2 |                                                       HTTP/1.1 or HTTP/2 |                                              HTTP/1.1 or HTTP/2 |
|           Encoding |                                    Protobuf (binary) |                                                        Protobuf (binary) |                                          Protobuf → JSON (text) |
|   Endpoint routing |     Single endpoint, routed by gRPC services/methods |              Distinct URL paths: `/v1/traces`, `/v1/metrics`, `/v1/logs` |     Distinct URL paths: `/v1/traces`, `/v1/metrics`, `/v1/logs` |
|      Request shape |                       RPC calls / persistent streams |                                                               HTTP POSTs |                                                      HTTP POSTs |
|       Content-Type |                                Handled by gRPC layer |                                                 `application/x-protobuf` |                                              `application/json` |
|        Compression |                                Built-in gRPC support |                                                  HTTP-level (e.g., gzip) |                                         HTTP-level (e.g., gzip) |
|        Performance |                     Best (lowest latency, efficient) |                                                Slightly slower than gRPC |                             Slowest (larger payloads & parsing) |
|           Best fit | Production SDK-to-collector when HTTP/2 is available | Environments where gRPC is not feasible but binary efficiency is desired | Debugging, demos, or when human-readable payloads are preferred |

## Best use cases & recommendations

* gRPC: preferred for SDK-to-collector or high-throughput production setups when HTTP/2 is supported.
* HTTP + Protobuf: choose when gRPC is blocked or unsupported but you still want compact binary encoding.
* HTTP + JSON: use for debugging, quick manual inspection, or environments that require text payloads.

<Callout icon="lightbulb">
  Choose transports based on environment constraints (HTTP/2 availability), performance needs (low-latency streaming vs. request-based), and debugging requirements (binary vs. human-readable).
</Callout>

<Frame>
  <img alt="The image is a comparison chart for OTLP transport and encoding, comparing gRPC + Protobuf, HTTP + Protobuf, and HTTP + JSON across features like content-type, compression, performance, and best use cases." />
</Frame>

Core takeaway: the same OTLP data model (resource → scope → signals) flows through all transports and encodings. Pick gRPC or HTTP (with Protobuf/JSON) to match your deployment environment, performance targets, and operational constraints.

That's everything about OTLP transport options.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/4a28a358-0f6c-41db-b273-5de50a0942d2" />
</CardGroup>
