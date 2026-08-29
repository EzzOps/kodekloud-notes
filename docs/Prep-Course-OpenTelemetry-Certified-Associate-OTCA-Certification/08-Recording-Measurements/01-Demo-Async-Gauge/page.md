# Demo Async Gauge

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Recording-Measurements/Demo-Async-Gauge/page

Demonstrates adding an observable gauge to a Flask app using OpenTelemetry and psutil to poll memory usage, with MeterProvider setup and periodic console metric exporting.

In this lesson we add a new metric to track memory usage for a Flask API ("shopping-app") using OpenTelemetry for Python. We choose an observable (polled) gauge implemented with psutil and export metrics to the console via a PeriodicExportingMetricReader. This demonstrates setting up a MeterProvider, registering a polled gauge callback, and using synchronous counters to instrument requests.

Why choose an observable gauge?

* Counters only increase; they are not suitable for values that go up and down.
* Up-down counters are for values your code explicitly increments/decrements (e.g., concurrent requests).
* Memory usage fluctuates and is independent of prior values, so a gauge is the correct metric type.
* An observable (async) gauge lets the SDK poll the current memory values periodically, so you do not need to manually update the metric inside your application code.

> **lightbulb** Observable gauges are polled by the metrics SDK (via the metric reader). You must provide a callback function that returns the current observations; the SDK will call that callback periodically according to the metric reader's export interval.

## Example: Flask app with an observable gauge (polled memory)

This self-contained example shows:

* Meter/provider setup with a ConsoleMetricExporter and 5s periodic exporting.
* Synchronous metrics: request counters and an up-down counter for concurrent requests.
* An observable gauge that reports RSS and VMS memory values for the running process.

```python theme={null}
