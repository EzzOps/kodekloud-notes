# Span Kind

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Kind/page

Explains span kinds in OpenTelemetry and how to classify spans (CLIENT, SERVER, INTERNAL, PRODUCER, CONSUMER) to ensure correct tracing and dependency visualization

This lesson explains Span Kind — the semantic classification that tells tracing systems what role a span plays in a distributed trace (is it making a request, handling one, or processing a message?). Correct span kinds give observability tools the context they need to link spans, build dependency graphs, and surface meaningful service relationships.

<Frame>
  <img alt="The image explains the concept of &#x22;Span Kind,&#x22; which classifies a span's role in a distributed interaction using a network diagram of connected blue circles. It mentions that it clarifies the direction of the call and its communication style." />
</Frame>

Why span kind matters

* It provides semantic information that tracing backends use to interpret relationships between spans (for example, to connect outgoing requests to the service that received them).
* It indicates whether an interaction is synchronous (request/response) or asynchronous (message-based), which affects how traces are visualized and analyzed.
* It helps maintain correct parent-child relationships across process or service boundaries when context is propagated.

<Frame>
  <img alt="The image explains why span kind matters for tracing systems, highlighting its role in identifying if a span is initiating or processing a request and distinguishing between request/response and deferred execution models." />
</Frame>

OpenTelemetry span kinds

OpenTelemetry defines five span kinds to cover common interaction models: `CLIENT`, `SERVER`, `INTERNAL`, `PRODUCER`, and `CONSUMER`. Use the kind that best represents the role of the span so tracing tools can correctly link and display causal relationships.

<Frame>
  <img alt="The image illustrates the five types of span kind in OpenTelemetry: Client, Server, Internal, Producer, and Consumer, using labeled arrows to show their relationships." />
</Frame>

Summary table of span kinds

| Span Kind  |          Direction | Communication style                    | Typical use case                                   |
| ---------- | -----------------: | -------------------------------------- | -------------------------------------------------- |
| `CLIENT`   |           Outgoing | Synchronous request/response           | HTTP requests, RPC calls, DB queries               |
| `SERVER`   |           Incoming | Synchronous request/response           | Web server handling an HTTP request                |
| `INTERNAL` |              Local | In-process work (no boundary crossing) | Computations, helper functions, local processing   |
| `PRODUCER` | Outgoing (message) | Asynchronous/message-based             | Publishing to a Kafka topic or message queue       |
| `CONSUMER` | Incoming (message) | Asynchronous/message-based             | Processing messages consumed from a queue or topic |

Why use span kinds correctly?

* Correct kinds enable accurate trace analysis and visualization (dependency maps, service flow graphs).
* They reduce ambiguity: each span should represent a single, clear purpose.
* They ensure propagation and linking work as intended across service boundaries.

<Frame>
  <img alt="The image explains the importance of span kind in trace analysis, highlighting correct interpretation, visualization benefits, and prevention of ambiguous instrumentation. It advises creating a new client span for each call." />
</Frame>

Concrete examples

* `CLIENT`: Outgoing calls (HTTP requests, RPC, DB queries). Create a new `CLIENT` span for each external call so each request is represented individually.
* `SERVER`: Incoming requests handled by a service. When context is propagated, the `SERVER` span becomes a child of the originating `CLIENT` span.
* `PRODUCER`: Enqueuing or publishing a message (e.g., writing to a Kafka topic).
* `CONSUMER`: Receiving and processing a message from a broker or queue.
* `INTERNAL`: Local in-process operations that do not cross service boundaries (default kind when none is set).

<Frame>
  <img alt="The image is a table explaining different &#x22;Span Kinds&#x22; with columns for call direction, communication style, and a brief description of each type, including CLIENT, SERVER, PRODUCER, CONSUMER, and INTERNAL categories." />
</Frame>

HTTP example

* Client side: creating an outgoing HTTP request should produce a `CLIENT` span.
* Server side: receiving that request produces a `SERVER` span.
* When headers (or another propagation mechanism) carry trace context, the server span becomes a child of the client span, forming a clear client→server causal link in the trace.

<Frame>
  <img alt="The image is a diagram explaining client-server roles in HTTP, showing &#x22;Browser → Backend&#x22; as a CLIENT sending an HTTP GET request, and &#x22;Backend&#x22; as the Server handling the request." />
</Frame>

Messaging example

* `PRODUCER` spans represent the act of publishing or enqueueing a message.
* `CONSUMER` spans represent the processing of that message by consumers.
* Any additional local work done while processing a message (parsing, business logic) should use `INTERNAL` spans to reflect in-process operations.

<Frame>
  <img alt="The image is a table explaining &#x22;Messaging with Span Kind,&#x22; outlining three roles: Producer, Consumer, and Internal, with corresponding examples and functions." />
</Frame>

Best practices

* Give each span one clear role — do not mix `CLIENT` and `SERVER` responsibilities in a single span.
* When a call crosses a process or service boundary, set the appropriate span kind to help tracing backends visualize relationships.
* Create separate `CLIENT` spans for each outgoing operation (e.g., multiple DB calls should each have their own `CLIENT` span).
* For async flows, use `PRODUCER` and `CONSUMER` and preserve causal links via context propagation or explicit span links.

<Frame>
  <img alt="The image lists &#x22;Span Kind Best Practices,&#x22; highlighting &#x22;Avoid multi-role spans&#x22; and &#x22;Chain correctly&#x22; with brief explanations and icons." />
</Frame>

Key takeaways

* Span kinds are essential for meaningful tracing: they indicate direction, communication style, and clarify cause-effect relationships.
* Use `CLIENT`/`SERVER` for synchronous request/response; use `PRODUCER`/`CONSUMER` for messaging; default to `INTERNAL` for local operations.
* Avoid overloading spans with multiple roles; create distinct spans for separate outgoing operations to keep traces clear and accurate.

<Frame>
  <img alt="The image is a slide titled &#x22;Key Takeaways&#x22; outlining four points about SpanKinds and semantic rules for meaningful tracing, emphasizing trace direction, semantic rules, and efficient span creation." />
</Frame>

<Callout icon="lightbulb">
  Most spans you create locally will be `INTERNAL`. Reserve `CLIENT`, `SERVER`, `PRODUCER`, and `CONSUMER` for interactions that cross process or service boundaries.
</Callout>

Further reading and references

* OpenTelemetry Spec — Span Kind semantic conventions: [https://opentelemetry.io/docs/reference/specification/trace/semantic\_conventions/span-kind/](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/span-kind/)
* Kafka documentation (example messaging system): [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)

That's it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/a81a2fc6-a27f-47eb-8e22-1160b4b16672" />
</CardGroup>
