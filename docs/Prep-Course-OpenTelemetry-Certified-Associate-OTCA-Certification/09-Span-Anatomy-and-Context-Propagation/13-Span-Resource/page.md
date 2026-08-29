# Access the span's context and print TraceFlags (example with OpenTelemetry Python API)
trace_flags = span.get_span_context().trace_flags
print(f"[main] TraceFlags: {trace_flags:#04x}")  # formatted as hex, e.g., 0x01
```

Output:

```text theme={null}
[main] TraceFlags: 0x01
```

<Frame>
  <img alt="The image is an informational graphic about TraceFlags, which are 8-bit fields controlling tracing behavior related to sampling and future use cases." />
</Frame>

<Frame>
  <img alt="The image is a slide about &#x22;TraceFlags — Size & Format,&#x22; explaining its size (8 bits), inclusion in trace context propagation, hexadecimal representation, and example values like &#x22;00&#x22; for no flags set and &#x22;01&#x22; for sampled flag set." />
</Frame>

## TraceState

TraceState carries optional, vendor-specific metadata as a list of key-value entries. It allows multiple tracing systems to cooperate without overwriting each other’s metadata.

* Format: comma- or semicolon-separated list of `key=value` entries, e.g., `vendor1=val1,vendor2=val2`.
* Size rules: keys must be unique; the overall `tracestate` length is limited (for example, 512 characters per the W3C Trace Context spec).
* OpenTelemetry note: `ot=` entries are reserved for OpenTelemetry; instrumentation libraries should not alter `ot=` entries and should use their own keys.

Illustrative `tracestate` entries:

```plaintext theme={null}
ot=p:8;r:62
ot=foo:bar;k:1:13
f4fe05b2-bd92206c@dt=fw4;3;abf102d9;c4592;0;0,apmvendor=boo,foo=bar
tenant1@vendor1=abc123,tenant2@vendor2=xyz789
```

Example JSON-style representation (for clarity):

```json theme={null}
{
  "context": {
    "trace_state": [
      "f4fe05b2-bd92206c@eg=fw4;3;abf102d9;c4592;0;0;2ee;5607;2h01",
      "apmvendor=boo",
      "foo=bar",
      "ot=rv:6e6d1a75832a2f"
    ]
  }
}
```

<Callout icon="warning">
  Do not modify reserved `ot=` entries in `trace_state`. Use vendor- or system-specific keys for your additional metadata to avoid clobbering other systems' data.
</Callout>

## Parent ID, root, and children

* Root span: the first span in a trace; it has no parent span ID (parent is unset or null).
* Child span: a span created by another span; it stores the parent span ID in its context to form the parent-child link.
* Parent ID rules:
  * Parent ID always refers to another span within the same trace.
  * Parent ID is immutable for that span (does not change after creation).

These parent-child links let tools build trace trees, waterfall charts, and dependency maps.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Parent IDs: Traces into Maps and Timelines,&#x22; focusing on the purpose of enabling visualizations like trace trees, waterfall charts, and dependency diagrams, with icons representing each type of visualization." />
</Frame>

<Frame>
  <img alt="The image is a slide titled &#x22;Parent ID Rules: Same Trace, Immutable,&#x22; explaining that a Parent ID always refers to another Span ID within the same Trace ID and does not change after the span is created." />
</Frame>

## Recap

* Span name: concise description of the operation (e.g., `processPayment`). Keep it generic and put request-specific details into attributes.
* Span context: the metadata bundle that travels with the span (`trace_id`, `span_id`, `trace_flags`, `trace_state`). This is what propagation carries across process boundaries.
* Trace ID: 16 bytes (128 bits), represented as a 32-hex-character string; same across all spans in a trace.
* Span ID: 8 bytes (64 bits), represented as a 16-hex-character string; unique per span within a trace.
* Parent span ID: the span ID of the parent that created this span; used to reconstruct the trace tree.
* Trace flags: an 8-bit field used primarily for sampling; `0x00` = not sampled, `0x01` = sampled.
* TraceState: optional vendor metadata as key-value pairs; used to pass additional context in multi-vendor environments.

<Frame>
  <img alt="The image is a summary of OpenTelemetry Span and Trace fundamentals, detailing Span Name, Span Context, Trace ID, and Span ID, along with their characteristics and examples." />
</Frame>

<Frame>
  <img alt="The image is a slide summarizing the fundamentals of OpenTelemetry span and trace, including concepts like parent span, child span, trace flag, and trace state with examples." />
</Frame>

That's it for this section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/a81ae1f1-61ba-427b-aebc-d873d216c1c6" />
</CardGroup>


# Span Resource

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Resource/page

Explains OpenTelemetry resources identifying telemetry origins via attributes, default attributes, automatic detectors, custom attributes, environment configuration, and benefits for grouping, filtering, and troubleshooting.

Hello, span explorers.

In this lesson we’ll cover resources in spans and what “resources” mean in OpenTelemetry. Resources attach identity and context to telemetry so you can tell where a span, metric, or log originated.

Why do we need resources? If you collect spans from every system in your organization, how do you distinguish spans coming from a service, a VM, a container, a pod, or an on‑prem host? Resources describe the entity producing telemetry so you can answer questions like “Which service generated this error?” or “Is this latency limited to the payments namespace?”

<Frame>
  <img alt="The image explains the need for resources to provide context to telemetry data, specifically addressing the problem of lacking metadata about data producers. It highlights the solution that resources offer in describing the entity producing the telemetry." />
</Frame>

## What is a Resource?

A Resource is a set of key/value attributes that identify the source of telemetry. Common resource attributes include service name, host/hostname, container name or ID, cloud provider, region, and deployment environment (prod/staging).

<Frame>
  <img alt="The image describes the concept of defining a resource as a collection of attributes that identify the source of telemetry data, with examples such as Service, Host, Container, Cloud, and Environment." />
</Frame>

## Why Resources Matter

Resources let you identify the producing entity for telemetry so you can ask operational questions such as:

* Was this error coming from `service B` on AWS?
* Is the latency isolated to the Kubernetes namespace `payments`?
* Which team owns the service that emitted this span?

<Frame>
  <img alt="The image explains the importance of resources in tracing services, showing how different services (A, B, C) emit spans to a telemetry backend for monitoring and error tracing." />
</Frame>

Examples of concrete resource attributes:

* `service.name = "payment-service"`
* `pod.name = "payment-api"`
* `cloud.provider = "aws"`

## Default Resource Attributes

OpenTelemetry SDKs provide default resource attributes you should know:

* `service.name` (defaults to `unknown_service` if not set)
* `telemetry.sdk.name`
* `telemetry.sdk.language`
* `telemetry.sdk.version`

<Frame>
  <img alt="The image is a table titled &#x22;Default Resource Attributes&#x22; showing various attribute keys, their example values, and their purposes. Each row lists attributes related to service name, SDK provider, language runtime, and SDK version." />
</Frame>

|            Attribute Key | Typical Value     | Purpose                                     |
| -----------------------: | ----------------- | ------------------------------------------- |
|           `service.name` | `payment-service` | Identifies the service producing telemetry  |
| `telemetry.sdk.language` | `python`          | Runtime/language of the SDK                 |
|  `telemetry.sdk.version` | `1.0.0`           | SDK version for debugging and compatibility |

<Callout icon="warning">
  If you don't set `service.name`, it will default to `unknown_service`. With many services emitting telemetry, this makes it hard to identify which trace belongs to which service—so it is a best practice to set `service.name` for every instrumented app.
</Callout>

## Automatic Resource Detection

OpenTelemetry supports automatic resource detection via detectors. Detectors gather environment metadata and populate resource attributes without manual configuration. Typical detectors can collect:

* OS type and description
* Hostname and architecture
* Process details
* Container name/ID
* Kubernetes pod and namespace
* Cloud provider and region

<Frame>
  <img alt="The image is a table listing different types of resource detectors and their provided attributes, such as OS type, host name, and container ID, to aid in adding attributes for telemetry. It highlights the benefit of reducing configuration effort and standardizing telemetry across platforms." />
</Frame>

Automatically-detected resource metadata reduces configuration effort and helps standardize telemetry across environments.

## Benefits of Resource Attributes

Adding resource attributes makes it easier to:

* Group and filter telemetry by service, pod, container, or host
* Troubleshoot incidents by narrowing scope quickly
* Correlate telemetry across services and environments
* Support multi-cloud and multi-environment setups

<Frame>
  <img alt="The image explains why adding resource attributes is beneficial, highlighting that it makes it easier to group, filter, and troubleshoot, and features a logo for Jaeger, a commercial observability backend." />
</Frame>

## Custom Resource Attributes

You can add custom resource attributes for business or operational metadata, for example the team owning a service, application grouping, or feature flags. These attributes complement auto-detected attributes and improve searchability and access control in observability backends.

<Frame>
  <img alt="The image describes &#x22;Custom Resource Attributes&#x22; which add extra information about telemetry, including &#x22;Which service,&#x22; &#x22;What environment,&#x22; and &#x22;Which team.&#x22;" />
</Frame>

To attach custom attributes in code, pass a `Resource` to the `TracerProvider` during initialization. The following Python example shows creating a custom resource and configuring a tracer provider so every span includes those attributes:

<Frame>
  <img alt="The image illustrates adding resource attributes via code, including metadata such as service.name, team, and deployment.environment. Each attribute is associated with a description and example value." />
</Frame>

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
