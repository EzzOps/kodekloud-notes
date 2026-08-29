# What is gRPC vs HTTP

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Advanced-Concepts/What-is-gRPC-vs-HTTP/page

Compares gRPC and HTTP, showing how gRPC leverages HTTP/2, protobuf, and generated stubs for efficient, low‑latency microservice communication versus HTTP/1.1 and JSON.

Let's break down how [gRPC](https://grpc.io/) differs from standard HTTP protocols and why it matters for modern microservices. One key point to be clear about: [gRPC](https://grpc.io/) does not replace HTTP — it runs on top of [HTTP/2](https://developer.mozilla.org/en-US/docs/Web/HTTP/2).

<Callout icon="lightbulb">
  [gRPC](https://grpc.io/) uses [HTTP/2](https://developer.mozilla.org/en-US/docs/Web/HTTP/2) as its transport layer. Knowing how HTTP/2 works explains many of gRPC's performance and operational advantages.
</Callout>

Example scenario: an Uber-style rider app

Consider the backend of a ride-hailing app. When a rider taps "Request a ride," the trip service fans out multiple calls: it queries the driver service for nearby cars, the pricing service for a fare estimate, the location service for live tracking, and the notification service to alert drivers. One user action can generate many internal service calls per request.

<Frame>
  <img alt="The image illustrates a comparison between gRPC and HTTP, featuring an Uber-style ride app diagram with various service components like driver, location, trip service, pricing, and notification. It highlights that a single &#x22;Request a Ride&#x22; tap can result in 15-20 calls." />
</Frame>

At production scale, services like this may exchange thousands of RPC/external calls per second. The underlying protocol you choose affects latency, bandwidth, CPU usage, and developer ergonomics.

Why HTTP/1.1 can be inefficient for high-volume service-to-service traffic

* HTTP/1.1 often requires separate TCP connections (or a very limited number of simultaneous connections) to achieve parallelism. Clients and browsers typically limit concurrent connections.
* New connections imply fresh TCP and TLS handshakes, adding tens to hundreds of milliseconds of latency depending on network conditions.
* Head-of-line blocking on a connection can delay subsequent requests if one is slow.
* Each request sends repeated plain-text headers (authorization tokens, trace IDs, etc.), which can be hundreds of bytes per request and waste bandwidth at scale.

<Frame>
  <img alt="The image illustrates HTTP/1.1 problems, including head-of-line blocking and header repetition as plain text. It shows issues like one request per connection, slow queue waits, and a maximum of six connections." />
</Frame>

How HTTP/2 improves things

* Multiplexing: a single TCP/TLS connection carries many concurrent streams (lightweight channels), so you avoid many parallel handshakes.
* Header compression (HPACK): repeated headers are compressed using a shared state table, so subsequent requests send far fewer header bytes.
* Better utilization of an existing secure connection reduces CPU and latency overhead for many short-lived calls.

Note: HTTP/2 eliminates application-level head-of-line blocking by multiplexing streams, but it can still suffer from TCP-level head-of-line blocking if packets are lost. [HTTP/3 (QUIC)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#http3) addresses that by using UDP-based independent streams.

<Frame>
  <img alt="The image illustrates how HTTP/2 improves performance by using a single connection with multiple parallel streams and header compression." />
</Frame>

What gRPC adds on top of HTTP/2

gRPC combines HTTP/2 transport with two main features that make it compelling for internal APIs and microservices:

1. Compact binary serialization — Protocol Buffers (protobuf)
   * Protobuf is a binary, strongly typed serialization format. Binary encodings are smaller on the wire and faster for machines to parse than verbose JSON.
   * Example JSON:
     ```json theme={null}
     {
       "lat": 37.77,
       "lon": -122.41,
       "user": 4827
     }
     ```
   * Equivalent protobuf bytes (hex view):
     ```text theme={null}
     0A 08 B8 17 95 41
     12 08 5A 8F C2 41
     1A 04 D3 12
     ```
   * Smaller payloads and cheaper parsing reduce latency and CPU usage at scale.

2. Strongly typed service contract in a `.proto` file
   * A single `.proto` file defines your service, RPC methods, and message types. From that file, code generators produce client and server stubs in many languages, ensuring both sides share the same contract.
   * Example service definition:
     ```proto theme={null}
     // ride.proto
     service DriverService {
       rpc FindNearby(Location) returns (DriverList);
     }
     ```
   * Generated client code makes a remote call look like a local function:
     ```javascript theme={null}
     client.FindNearby({ lat: 37.77, lon: -122.41 });
     ```
   * gRPC handles serialization, HTTP/2 transport, and deserialization under the hood.

Quick comparison: HTTP/1.1 vs HTTP/2 vs gRPC

| Feature                       |                   HTTP/1.1 |                       HTTP/2 |                         gRPC (on HTTP/2) |
| ----------------------------- | -------------------------: | ---------------------------: | ---------------------------------------: |
| Multiplexing                  |                         No |                          Yes |                                      Yes |
| Header compression            |                         No |                  Yes (HPACK) |                              Yes (HPACK) |
| Serialization format          |        Typically JSON/text |          Typically JSON/text |                        Protobuf (binary) |
| Strong typed service contract |                         No |                           No |                             Yes (.proto) |
| Client/server code generation |                         No |                           No |                    Yes (stub generation) |
| Best for                      | Browsers, simple REST APIs | Mixed workloads, better perf | Internal microservices, low-latency RPCs |

Where gRPC is a good fit

<Callout icon="lightbulb">
  Use [gRPC](https://grpc.io/) for internal service-to-service communication where you need high throughput, low latency, compact binary payloads, and a strong typed contract across languages. For public-facing APIs (browsers, third-party integrations), REST/HTTP+JSON remains widely supported and easier for clients without gRPC tooling.
</Callout>

Summary

* gRPC runs on top of HTTP/2 and gains multiplexing and header-compression benefits from that transport.
* gRPC adds protobuf binary encoding (smaller/faster) and a `.proto` service contract that generates client/server code.
* For high-volume internal microservices, gRPC often outperforms HTTP/JSON solutions in latency, bandwidth, and developer productivity. For public, human-facing APIs, REST/JSON is still common due to broad client support.

Links and references

* [gRPC official site](https://grpc.io/)
* [Protocol Buffers (protobuf)](https://developers.google.com/protocol-buffers)
* [HTTP/2 overview (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/2)
* [HTTP/1.1 (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/1.1)
* [HTTP/3 and QUIC (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#http3)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/5de176de-dc0d-4961-bac5-a735e7d70eda/lesson/9e8999af-647c-49fd-b84f-b37005be6667" />
</CardGroup>
