# Metrics API and SDK

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Metrics-API-and-SDK/page

Explains OpenTelemetry Metrics API and SDK components and how to create, configure, record, aggregate, and export metrics using MeterProvider, Meter, and Instruments

You've already learned core metrics concepts — temporality, monotonicity, aggregation, and more. In this article we convert theory into practice: how to define, create, and record metrics in your application using the Metrics API and its SDK implementation.

The Metrics API defines stable interfaces used by libraries and applications to create and record metrics. The SDK implements those interfaces, performing collection, aggregation, and exporting to observability backends.

At a high level the Metrics API comprises three core components:

* MeterProvider — the entry point and factory for Meters.
* Meter — a factory that creates instruments for a specific instrumentation scope (a library or component).
* Instrument — the metric primitives (counters, histograms, gauges, etc.) used to record measurements.

The SDK wires these abstractions together so measurements are aggregated and exported to your telemetry backend.

<Frame>
  <img alt="The image provides an overview of &#x22;Metrics API and SDK,&#x22; highlighting their components: MeterProvider, Meter, Instrument, and Telemetry." />
</Frame>

This separation between API and SDK mirrors the tracing model: it keeps a stable public API for instrumentation while allowing multiple SDK implementations and flexible configuration.

## Core components: MeterProvider, Meter, Instrument

Think of the MeterProvider as the top-level factory and configuration point; it produces Meters for each instrumentation scope. Each Meter then creates and owns Instruments that your code uses to record telemetry.

<Frame>
  <img alt="The image illustrates the components of a Metrics API, including &#x22;MeterProvider,&#x22; &#x22;Meter,&#x22; and &#x22;Instrument,&#x22; with the &#x22;MeterProvider&#x22; labeled as the entry point." />
</Frame>

A Meter focuses only on creating instruments — not on configuration. That separation keeps ownership and configuration consistent: instruments are tied to the Meter that created them, and that Meter is tied to a MeterProvider.

<Frame>
  <img alt="The image shows a diagram of the &#x22;Metrics API Components,&#x22; which includes &#x22;Metrics API,&#x22; &#x22;MeterProvider,&#x22; &#x22;Meter,&#x22; and &#x22;Instrument.&#x22;" />
</Frame>

Meters create instruments (counters, histograms, gauges, synchronous and asynchronous instruments) and manage their lifetime.

<Frame>
  <img alt="The image is a diagram about a &#x22;Meter&#x22; with sections labeled &#x22;Responsibility&#x22; and &#x22;Functions,&#x22; listing tasks like &#x22;createCounter,&#x22; &#x22;createGauge,&#x22; &#x22;createAsynchronousCounter,&#x22; and &#x22;createHistogram.&#x22; It emphasizes creating instruments, not configuration." />
</Frame>

Configuration — processors, exporters, views, aggregation rules, resource attributes — is handled by the MeterProvider. Because each instrument is associated with the Meter that created it, and each Meter is associated with a MeterProvider, ownership and configuration linkage remain clear and predictable.

<Frame>
  <img alt="The image is a flowchart depicting the responsibilities of creating instruments and not configuration, with elements such as &#x22;Instrument,&#x22; &#x22;Meter,&#x22; &#x22;Configuration,&#x22; and &#x22;MeterProvider,&#x22; along with arrows indicating relationships and ownership." />
</Frame>

<Callout icon="lightbulb">
  Using the global default MeterProvider is convenient for most applications. Create a custom MeterProvider only when you need separate configuration or isolation (for example, to separate business metrics from runtime or platform metrics).
</Callout>

## MeterProvider in detail

The MeterProvider is the API/SDK entry point that exposes `getMeter(...)` to obtain a Meter for an instrumentation scope. Typical `getMeter` arguments are:

* `name` (required) — identifies the instrumentation scope (usually a library or component name).
* `version` (optional) — the version of the library or component.
* `schema_url` (optional) — the semantic conventions schema URL.

`version` and `schema_url` are optional, but including them gives downstream processors and exporters richer context for interpretation and mapping.

<Frame>
  <img alt="The image is a diagram of Metrics API components, showing the flow from Metrics API to MeterProvider, Meter, and Instrument, with an &#x22;Application&#x22; and a &#x22;Central Configuration Point&#x22; noted." />
</Frame>

<Frame>
  <img alt="The image is a flowchart titled &#x22;MeterProvider&#x22; with boxes describing components such as &#x22;getMeter,&#x22; &#x22;name,&#x22; &#x22;version,&#x22; &#x22;schema_url,&#x22; and &#x22;attributes,&#x22; along with annotations &#x22;Enhance Context&#x22; and &#x22;Flexible.&#x22;" />
</Frame>

## Meter responsibilities

A Meter's role is instrument creation and lifetime management. Common factory methods include:

* Synchronous Counter and UpDownCounter
* Asynchronous counters and gauges (callback-driven)
* Histogram
* Gauge-like instruments

Each instrument stays linked to its Meter, enabling traceability to the instrumentation scope and MeterProvider.

<Frame>
  <img alt="The image is a diagram about a &#x22;Meter&#x22; with sections labeled &#x22;Responsibility&#x22; and &#x22;Functions,&#x22; listing tasks like &#x22;createCounter,&#x22; &#x22;createGauge,&#x22; &#x22;createAsynchronousCounter,&#x22; and &#x22;createHistogram.&#x22; It emphasizes creating instruments, not configuration." />
</Frame>

## Instruments: properties and typing

An Instrument represents a metric you record and is defined by several properties:

* Name (for example, `payments.processed_total`, `http.server.duration`)
* Kind (counter, histogram, gauge, asynchronous counter, etc.)
* Unit (for example, `ms`, `kB`, `1`)
* Description (human-readable purpose)
* Data type (integer vs floating point)

Instruments are strongly typed: you must create and use an instrument with the matching data type (e.g., integer Counter vs. double Histogram). This guarantees type safety and consistent aggregation semantics.

<Frame>
  <img alt="The image is a diagram titled &#x22;Instrument&#x22; with a blue header labeled &#x22;Properties&#x22; and four gray boxes underneath labeled &#x22;Name,&#x22; &#x22;Kind,&#x22; &#x22;Unit,&#x22; and &#x22;Description.&#x22;" />
</Frame>

### Typical instrument types and use cases

| Instrument type      | Typical use case                                                 | Notes                            |
| -------------------- | ---------------------------------------------------------------- | -------------------------------- |
| Counter              | Count events that only increase (e.g., requests processed)       | Monotonic                        |
| UpDownCounter        | Track values that can increase/decrease (e.g., concurrent users) | Non-monotonic                    |
| Histogram            | Measure distributions (e.g., request latency)                    | Produces buckets & summary       |
| Asynchronous Gauge   | Periodic measurements (e.g., free memory)                        | Uses callbacks to observe values |
| Asynchronous Counter | Periodic monotonic totals (e.g., cumulative bytes sent)          | Uses callbacks                   |

## Example process hierarchy

Below is a concrete example of how a MeterProvider can produce multiple Meters, each with typed, named Instruments. This structure isolates metrics by instrumentation scope and makes them traceable to their origin.

```yaml theme={null}
MeterProvider (default)
├── Meter (name="io.opentelemetry.runtime", version="1.0.0")
│   ├── Instrument <Asynchronous Gauge, int>
│   │   ├── - name: "cpython.gc"
│   │   ├──   attributes: ["generation"]
│   │   └──   unit: "kB"
│   └── ...
├── Meter (name="io.opentelemetry.contrib.mongodb.client", version="2.3.0")
│   ├── Instrument <Counter, int>
│   │   ├── - name: "client.exception"
│   │   ├──   attributes: ["type"]
│   │   └──   unit: "1"
│   └── Instrument <Histogram, double>
│       ├── - name: "client.duration"
│       ├──   attributes: ["server.address", "server.port"]
│       └──   unit: "ms"

MeterProvider (custom)
│
├── Meter (name="bank.payment", version="23.3.5")
└── ...
```

Because each instrument is strongly typed, retrieving and using it in code requires matching its declared type and name.

## How metrics flow (SDK responsibilities)

Once your application records measurements, the SDK handles:

* Aggregation (via Aggregators) — summarizing raw measurement points (sum, last value, histograms)
* Views — a configuration layer that can rename metrics, change aggregation, or filter instruments without changing instrumentation code
* Exporting — shipping metrics to a backend using exporters (commonly OTLP)
* Resource detection — adding contextual attributes (service name, host, container)
* Optional sampling and filters — used to reduce cardinality or volume when necessary

Common export flow:
instrumentation -> Meter -> MeterProvider (SDK config) -> Collector (receivers → processors → exporters) -> backend

Recap: core components and their purpose

* OpenTelemetry API: stable interfaces for metrics, traces, and logs.
* SDK: concrete implementation that collects, aggregates, and exports telemetry.
* MeterProvider: factory + central configuration for metrics.
* Meter: instrumentation scope and instrument factory.
* Instruments: the primitives used to record measurements.
* View: configuration layer to reshape metrics collection and aggregation without changing the code.
* Aggregator: converts raw measurements into summarized metrics.
* Exporter: ships metrics to backends (see OTLP for a common protocol).
* Resource detectors: capture environment/contextual attributes.
* Sampling/filters: reduce cardinality or volume when needed.

<Frame>
  <img alt="The image provides an overview of &#x22;Metrics API and SDK,&#x22; highlighting their components: MeterProvider, Meter, Instrument, and Telemetry." />
</Frame>

That covers the Metrics API and SDK: how Meters and Instruments are structured, how the MeterProvider configures behavior, and how the SDK aggregates and exports the telemetry you record.

## Links and references

* [OTLP Protocol](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/)
* [OpenTelemetry Metrics SDK & API docs](https://opentelemetry.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/4666522a-059d-44c3-a197-35a49c72c511" />
</CardGroup>
