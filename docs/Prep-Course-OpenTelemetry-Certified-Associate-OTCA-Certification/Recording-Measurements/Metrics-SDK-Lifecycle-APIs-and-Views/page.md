# Good: descriptive name + version
meter = provider.get_meter("http-client", version="1.2.0")

# Bad: empty name (SDK may fallback but attribution is lost)
bad_meter = provider.get_meter("", version="0.1")
```

## A full lifecycle example

The example below illustrates a typical end-to-end setup: initialize a MeterProvider with a Resource and meter configurator, attach a periodic MetricReader with a Console exporter, create a Meter and instrument, record measurements, and register a runtime View to filter attributes.

```python theme={null}
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider, MeterConfig
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

# 1) Initialize provider with resource and a meter configurator
resource = Resource({"service.name": "cart", "env": "staging"})

def disable_beta(scope):
    # Disable meters whose scope name ends with ".beta"
    return MeterConfig(enabled=not scope.name.endswith(".beta"))

provider = MeterProvider(
    resource=resource,
    meter_configurator=disable_beta
)

# 2) Attach a periodic reader and exporter (export every 5 seconds)
exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5000
)
provider.register_metric_reader(reader)

# 3) Create a Meter & Counter and record a measurement
meter = provider.get_meter("cart.checkout", version="0.9")
counter = meter.create_counter("items.checked_out")
counter.add(3, {"currency": "USD"})

# 4) Register a View at runtime to filter attributes (drop "currency")
provider.register_view(
    instrument_name="items.checked_out",
    attribute_filter=lambda kv: kv[0] != "currency"
)
```

Sequence explained

* Initialize MeterProvider with a `Resource` (for example, `service.name` and `env`) and optionally supply a `meter_configurator` to enable/disable meters by scope.
* Attach a `PeriodicExportingMetricReader` and a `MetricExporter` (Console in this demo) to control export timing and serialization.
* Create a `Meter` with a descriptive name and version, then create Instruments and record Measurements with attributes.
* Register an optional `View` at runtime to transform or filter attributes before export (this keeps instrumentation code untouched while applying policy).

## Pipeline summary

Think of the MeterProvider as your metrics factory and central configurator. The main pipeline stages are:

| Stage                     | Role                                                             |
| ------------------------- | ---------------------------------------------------------------- |
| Provider (MeterProvider)  | Orchestrates Meters, resources, Views, Readers, and Exporters    |
| Meter                     | Instrumentation scope that creates Instruments                   |
| Instrument                | Counters, Histograms, UpDownCounters used to emit Measurements   |
| View (optional)           | Transformation layer: aggregation, attribute filtering, renaming |
| Reader (MetricReader)     | Controls collection timing and triggers aggregation/export       |
| Exporter (MetricExporter) | Serializes and sends aggregated metrics to a backend             |

Mnemonic: "Please Make Insight Via Reliable Exports"\
(P = Provider, M = Meter, I = Instrument, V = View, R = Reader, E = Exporter)

Links and references

* OpenTelemetry Metrics specification and SDKs: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* OTLP (OpenTelemetry Protocol) details: [https://github.com/open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification)

## Summary

This should give you a clear understanding of how metric data moves from your application to a collector or backend, the role of each component in the pipeline, and practical tips for configuring MeterProvider, Meter names, Views, Readers, and Exporters. That's it for the Metrics pipeline section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/9705cf40-60fa-4c98-8f33-a0e1b27bf7b3" />
</CardGroup>


# Metrics SDK Lifecycle APIs and Views

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Metrics-SDK-Lifecycle-APIs-and-Views/page

Explains metrics SDK lifecycle, MetricReaders and MetricExporters, push versus pull exports, and Shutdown and ForceFlush behaviors and best practices for reliable metric delivery.

You now understand the high-level metrics pipeline. This article examines the lifecycle of key metrics components — MetricExporters and MetricReaders — and explains how metrics are delivered (pushed or pulled), how shutdowns are handled, and when to use ForceFlush.

Metric exporters are lightweight plugins whose sole responsibility is to transmit metrics to a destination (a backend, collector, or monitoring system). They always work in tandem with a MetricReader: the reader handles aggregation and temporality, while the exporter packages and sends already-summarized metrics. Keep exporters simple — if an exporter receives a format or timing it cannot support, it should log a clear error so users know why data was not exported.

<Callout icon="warning">
  Exporters should not perform aggregation or alter temporality. If a destination requires a custom metric format that the SDK does not natively support, the exporter must surface this clearly in logs and documentation.
</Callout>

<Frame>
  <img alt="The image is an infographic about &#x22;Metric Exporter,&#x22; explaining its role as a plug-in for sending metrics, its collaboration with a MetricReader, and its operation principles like simplicity, error logging, and scheduling." />
</Frame>

Why separate MetricReaders and MetricExporters?

* MetricReaders decide when and how to collect metrics (periodic, on-demand) and perform aggregation and temporality.
* MetricExporters remain agnostic of aggregation logic; they receive the reader's summarized metrics and transmit them.
* This separation makes SDKs flexible: you can attach multiple exporters (push and/or pull) to a MeterProvider, each with its own reader configuration.

Key export modes at a glance

| Mode          | Who initiates export                              | Typical use cases                                     | Effect of ForceFlush                                      |
| ------------- | ------------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------- |
| Push          | MetricReader (periodic or on demand)              | Exporters that send to collectors/backends directly   | ForceFlush triggers immediate collection + export         |
| Pull (scrape) | External scraper (e.g., `https://prometheus.io/`) | Instrumentation that exposes an endpoint for scrapers | ForceFlush has no effect — scrapes happen only on request |

Push-based exporters

In push workflows, a MetricReader controls collection cadence (for example, periodic polling). The reader collects and aggregates the in-memory metrics, then calls the exporter to transmit that summarized data to its destination. Push exporters can also be triggered by immediate requests such as `ForceFlush` or direct application signals (for example, when an application logs a critical incident and requests an immediate export).

Typical push flow:

* Instrument data is recorded in in-memory state.
* MetricReader collects and summarizes those metrics from the SDK.
* MetricExporter packages and sends the summarized metrics to an external process (collector or backend).

<Frame>
  <img alt="The image explains a push-based metric exporter system, detailing how it sends metrics autonomously and works with a paired MetricReader to send data, with periodic or immediate options during errors. The diagram shows the flow from in-memory state to metric exportation and another process." />
</Frame>

Pull-based exporters

Pull-based exporters (commonly called "scrape" exporters) expose an HTTP endpoint that an external scraper requests to retrieve metrics. The exporter is passive and only responds to scrape requests; it does not push data autonomously. Because the scraper controls timing, operations such as ForceFlush do not trigger an immediate push — scrapes occur only when the external system requests them.

Typical pull flow:

* Instrument data remains in in-memory state.
* The pull exporter exposes summarized data on an endpoint.
* An external scraper periodically requests (scrapes) the endpoint and forwards metrics to the backend.

<Frame>
  <img alt="The image is a diagram explaining a Pull Metric Exporter, highlighting its passive nature of waiting to be scraped by a process like Prometheus. It shows an in-memory state providing metrics to a PrometheusExporter, which is then accessed by another scraping process." />
</Frame>

Shutdown and ForceFlush — lifecycle control APIs

Two lifecycle APIs are critical for reliable metric delivery: Shutdown and ForceFlush. Understand their responsibilities and limitations so you can ensure final metrics are delivered during application termination.

Shutdown (MeterProvider)

* `Shutdown` is the termination API on the MeterProvider. It should be called exactly once to perform cleanup and to stop metric processing.
* On shutdown the provider should cascade the `shutdown` call to all registered MetricReaders and MetricExporters.
* SDKs may block synchronously up to a timeout and should report whether shutdown succeeded, failed, or timed out.
* After shutdown, the provider should refuse to create functional meters. Returning no-op meters is preferred so the application can keep running while preventing new metrics from being recorded.

<Frame>
  <img alt="The image is a flow diagram comparing processes before and after a &#x22;Shutdown&#x22; event, with &#x22;ForceFlush&#x22; and &#x22;Metric creation&#x22; involved. It is sourced from KodeKloud." />
</Frame>

ForceFlush

* `ForceFlush` asks push-based MetricReaders (and, transitively, their exporters) to immediately collect and export any buffered metrics.
* It is intended for push-based workflows where you want to ensure buffered metrics are delivered before shutdown or at critical moments.
* Pull exporters (scrape-based) are unaffected by `ForceFlush`; they only expose metrics in response to scrapes. For scrape-based setups, ensure the external scraper performs a final scrape if you need the last metrics exported.

<Callout icon="lightbulb">
  ForceFlush is intended for push-based workflows (e.g., ensuring buffered metrics are sent before shutdown). For scrape-based setups (Prometheus), ensure the scraper scrapes the endpoint at least once before shutdown if you need the final data exported.
</Callout>

Lifecycle summary and best practices

* Call `Shutdown` on the MeterProvider once to terminate metric processing cleanly and cascade cleanup to all MetricReaders and MetricExporters.
* After shutdown, the provider should return no-op meters to prevent further metric creation while allowing the app to continue running.
* Push exporters:
  * Attempt to `ForceFlush` any pending data during shutdown.
  * Stop timers/background threads, clear buffers, and release resources.
* Pull exporters:
  * Stop exposing the scrape endpoint so subsequent scrapes return no data.
  * Document how consumers should perform a final scrape if they require last-minute metrics.
* Provide explicit feedback about shutdown outcome (success, failure, timeout) to orchestration or monitoring systems.

<Frame>
  <img alt="The image is a summary of instructions related to shutting down a MeterProvider, including its effects on MetricReaders and MetricExporters, as well as guidance for push and pull exporters." />
</Frame>

References and further reading

* OpenTelemetry Metrics: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/) (see Metrics SDK and exporter guidelines)
* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)

This article covered metrics SDK lifecycle topics: MetricExporters (push and pull), MetricReaders, `ForceFlush`, and `Shutdown` semantics, including best practices for ensuring final metrics are reliably exported.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/6fce855c-4275-48c0-9297-a7f98a292285/lesson/4a118783-522b-4895-8327-fb598928db7c" />
</CardGroup>
