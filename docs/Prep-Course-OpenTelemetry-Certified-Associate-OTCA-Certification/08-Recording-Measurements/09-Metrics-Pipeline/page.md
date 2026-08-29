# Metrics Pipeline

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Metrics-Pipeline/page

Explains OpenTelemetry metrics pipeline components and lifecycle, including MeterProvider, Meters, Instruments, Views, Readers, Exporters, exemplars, configuration and export examples for collecting and exporting telemetry.

Great work exploring the Metrics API and SDK. This lesson explains how metric data points flow through the OpenTelemetry (OTel) metrics pipeline used by APIs and SDKs.

Core components in the OpenTelemetry metrics pipeline:

* MeterProvider: the entry point that provisions meters and configures the pipeline.
* Meter: represents an instrumentation scope (a library or component) and creates instruments.
* Instrument: counters, histograms, and up-down counters that record measurements.
* Measurement: a single recorded data point emitted by an instrument.
* View: an optional transformation layer to configure aggregation, filtering, renaming, or attribute changes without changing application code.
* MetricReader: controls collection and aggregation intervals and triggers exports.
* MetricExporter: encodes aggregated metric data (e.g., in OTLP) and sends it to a backend.
* Exemplars: sampled metric measurements that include trace/context information linking the metric to the exact trace/span that produced it.

<Frame>
  <img alt="The image is a table describing the OpenTelemetry (OTel) metrics pipeline components and their roles. It includes components like MeterProvider, Meter, Instrument, Measurement, View, MetricReader, and MetricExporter, each with a specific function in the pipeline." />
</Frame>

<Callout icon="lightbulb">
  Exemplars are sampled measurement points that include trace/span identifiers or other context. They let you jump from an interesting metric value to the trace(s) that generated it—great for root-cause analysis and drill-down.
</Callout>

## MeterProvider and how it ties the pipeline together

The MeterProvider is the root of the Metrics SDK pipeline. It:

* Owns one or more Meters (each represents an instrumentation scope such as a library or component).
* Configures pipeline behavior (views, readers, exporters, and resource attribution).
* Applies any meter configurator logic that can enable/disable meters by scope.

Meters create Instruments (counters, histograms, up-down counters) which produce Measurements. Views can transform measurements at collection time—renaming metrics, changing aggregation, filtering attributes, or remapping labels—without touching instrumentation code. MetricReaders schedule collection and trigger exports. MetricExporters serialize aggregated metric data (often OTLP) and send it to a backend or collector.

Best practice: use descriptive meter names (for example, library name + version) so metrics are properly attributed and easier to query in backends.

<Callout icon="warning">
  Avoid empty or vague meter names. The SDK may return a functional meter for an empty name (sometimes with a warning), but you'll lose important attribution metadata.
</Callout>

Example: creating meters with clear names

```python theme={null}
from opentelemetry.sdk.metrics import MeterProvider

provider = MeterProvider()
