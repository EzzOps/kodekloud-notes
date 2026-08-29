# Demo OTel Col Metrics

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Demo-OTel-Col-Metrics/page

Configuring the OpenTelemetry Collector to ingest metrics via OTLP push and Prometheus scrape with example configs, application code, logs, and troubleshooting tips

This guide demonstrates how to configure the OpenTelemetry Collector to receive metrics using two common approaches:

* Push-based (OTLP) — your application pushes metrics to the Collector.
* Pull-based (Prometheus-style) — the Collector scrapes your application for metrics.

Below are compact, corrected Collector configuration and application examples used in the demo, followed by representative Collector console output showing metrics ingestion. Use these snippets to validate both ingestion models and to troubleshoot common issues.

> **lightbulb** This article shows two common ways to get metrics into the Collector: OTLP push and Prometheus scrape. You can enable both simultaneously by configuring both receivers and adding them to your metrics pipeline.

## Collector: common pieces

The Collector configuration below contains attribute enrichment, an OTLP receiver, a Prometheus receiver (for scraping), processors, and exporters. The critical parts for metrics are the `receivers` and the `service.pipelines.metrics` section that wires receivers into the metrics pipeline.

```yaml theme={null}
