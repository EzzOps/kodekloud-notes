# gRPC vs RESTful API

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Advanced-Concepts/gRPC-vs-RESTful-API/page

Comparison of gRPC versus RESTful APIs using a ride‑sharing backend, covering performance, payload formats, streaming, tooling, browser support, and when to choose each

Let's compare gRPC and RESTful APIs using a concrete example from a ride‑sharing backend.

Imagine a rider taps "Request Ride". TripService then calls several other services:

* DriverService — find nearby cars
* PricingService — compute fare estimate
* LocationService — stream driver GPS coordinates
* NotificationService — notify the driver

Below we show how the same interactions look with a RESTful API versus gRPC, and when each approach is a better fit.

## RESTful example: simple, human‑readable, but verbose

With a RESTful API, TripService might POST to DriverService:

* Endpoint: `POST /drivers/nearby`
* Payload: JSON with the rider's location and search radius
* Response: a JSON array of nearby drivers

JSON is easy to inspect and debug on a laptop using curl, and its human readability is REST’s biggest strength.

Example request payload:

```json theme={null}
{ "lat": 37.77, "lon": -122.41, "radius_km": 2 }
```

Example curl:

```bash theme={null}
$ curl -X POST https://api.example.com/drivers/nearby \
  -H "Content-Type: application/json" \
  -d '{"lat":37.77,"lon":-122.41,"radius_km":2}'
```

But JSON is verbose. A list of fifty nearby drivers can be several kilobytes of text. Each HTTP call also resends common metadata (auth headers, trace IDs, user IDs), typically a few hundred bytes per request. Multiply this by thousands of requests per second and you incur significant network and CPU overhead.

<Frame>
  <img alt="The image discusses the bulkiness of JSON data for 50 drivers, equating to 10 KB, and highlights repeated request headers adding around 500 bytes, multiplied by thousands of requests per second." />
</Frame>

## gRPC + Protobuf: compact, typed, and efficient

[gRPC](https://grpc.io) typically uses [Protocol Buffers (Protobuf)](https://developers.google.com/protocol-buffers) instead of JSON. The same response with 50 drivers is usually much smaller in binary Protobuf form — often only a couple of kilobytes instead of ten.

Because gRPC runs over [HTTP/2](https://http2.github.io/), it benefits from features like header compression ([HPACK](https://httpwg.org/specs/rfc7541.html)) which reduces repeated metadata overhead across a connection after the initial handshake. At large scale (think Uber or Lyft), these bandwidth and CPU savings matter.

<Frame>
  <img alt="The image compares JSON text format, which is 10 KB, with Protobuf binary format, which is 2 KB, as a feature of gRPC." />
</Frame>

## API contracts and tooling

* RESTful APIs often rely on documentation (OpenAPI specs, Confluence pages). Docs can drift from code if not kept in sync.
* gRPC centralizes the contract in a `.proto` file. Services and messages (for example, `DriverService` with `FindNearby(Location) returns (stream Driver)`) are defined in one place and compiled into generated client/server stubs.

This means:

* For strongly typed languages, contract changes surface at compile time.
* Teams generate consistent client libraries from the same source-of-truth `.proto` files, reducing mismatch risk.

## Streaming and real‑time updates

A common use case in the ride app is streaming GPS coordinates from LocationService to the rider every few seconds. Approaches:

* REST: poll the endpoint frequently (inefficient) or use WebSockets (a separate protocol and stack from your REST endpoints).
* gRPC: native support for streaming (server-, client-, and bidirectional). LocationService can open a long‑lived stream and push updates efficiently over the same HTTP/2 connection.

<Frame>
  <img alt="The image is a diagram comparing streaming methods for a Location Service with sections for REST and gRPC, highlighting polling intervals, resource usage, and WebSockets." />
</Frame>

> **warning** Browsers don't expose the raw bidirectional HTTP/2 streams that "raw" gRPC relies on, so browser JavaScript cannot speak plain gRPC directly. Use bridging options such as `gRPC-Web` or deploy a proxy/gateway if you need browser clients to access gRPC backends. Many teams still expose REST for public/client‑facing APIs while using gRPC internally.

> **lightbulb** Best practice: Use the right tool for the job. Choose gRPC for high‑performance, internal service-to-service calls and streaming. Use REST/HTTP+JSON for public APIs or when human readability and broad compatibility matter.

## Quick comparison table

| Aspect          |                                 REST (HTTP/JSON) | gRPC (HTTP/2 + Protobuf)                                  |
| --------------- | -----------------------------------------------: | --------------------------------------------------------- |
| Payload format  |                              Human‑readable JSON | Binary Protobuf (compact)                                 |
| Overhead        |      Higher per-request (headers + verbose JSON) | Lower (HTTP/2 header compression + compact payloads)      |
| API contract    |                      OpenAPI or docs (can drift) | `.proto` files (single source of truth, generated code)   |
| Streaming       |           Polling or WebSockets (separate stack) | First‑class streaming (server/client/bidirectional)       |
| Browser support |                              Native (fetch, XHR) | Requires `gRPC‑Web` or proxy                              |
| Best for        | Public APIs, simple integrations, easy debugging | Internal high‑throughput services, low latency, streaming |

## When to choose which

* Use REST when:
  * You need wide compatibility with browsers and third‑party clients.
  * Human‑readable payloads and simplicity/debuggability matter.
  * You expose a public API or want to support many clients without generated stubs.

* Use gRPC when:
  * You need efficient, low‑latency service‑to‑service communication.
  * You want strong typing and auto‑generated client/server code.
  * You require native streaming (e.g., real‑time location updates).

In practice, most organizations use both: gRPC for internal, high‑performance comms (TripService ↔ DriverService ↔ PricingService), and REST for client-facing endpoints and public APIs.

## Links and references

* [gRPC](https://grpc.io)
* [Protocol Buffers (Protobuf)](https://developers.google.com/protocol-buffers)
* [OpenAPI Specification](https://www.openapis.org/)
* [HTTP/2 specification](https://http2.github.io/)
* [gRPC‑Web](https://grpc.io/docs/platforms/web/)
* [WebSockets API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/5de176de-dc0d-4961-bac5-a735e7d70eda/lesson/10c95ec3-f150-4125-b537-1220fbeb6c39)
