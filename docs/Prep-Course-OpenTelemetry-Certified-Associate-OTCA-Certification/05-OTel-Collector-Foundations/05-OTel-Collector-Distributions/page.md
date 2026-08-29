# OTel Collector Distributions

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/OTel-Collector-Distributions/page

Overview of OpenTelemetry Collector distributions, comparing Core and Contrib, when and how to build custom collectors with OCB, support models, releases, best practices, and Kubernetes deployment patterns

This lesson explains OpenTelemetry Collector distributions: how they’re packaged, extended, and when to build a custom collector. You’ll learn the differences between Collector Core and Contrib, how to pick components safely, how to create a tailored build with the OpenTelemetry Collector Builder (OCB), and high-level Kubernetes deployment patterns.

Here’s the big-picture outline: compare Collector Core vs Contrib, decide when to build a custom collector, review support and releases, and preview Kubernetes deployment patterns.

<Frame>
  <img alt="The image outlines the key aspects of &#x22;OTel Collector Distributions: The Big Picture,&#x22; including comparing OTel Collector Core vs Contrib, deciding when to build a custom collector, and understanding support and release." />
</Frame>

## Collector Core — minimal, stable foundation

The Collector Core distribution is intentionally conservative and small. It contains the officially maintained components required to build predictable telemetry pipelines: receivers, processors, exporters, and extensions. Core’s limited surface area and slower cadence make it easier to audit, upgrade, and operate safely in production.

<Frame>
  <img alt="The image outlines the OTel Collector Core, highlighting a lean set of components: Receivers, Exporters, Processors, and Extensions." />
</Frame>

What Core typically includes

* Receivers: `otlp` and simple/no-op receivers for testing or when no external input is required.
* Exporters: `otlp`, no-op, debug/logging exporters.
* Processors: `batch`, `memory_limiter`, and other stability-focused processors.
* Extensions: `health_check`, `pprof`, `zpages`, etc.

Keeping your runtime close to Core reduces upgrade risk and simplifies security reviews.

<Frame>
  <img alt="The image shows a table describing components of a &#x22;Collector Core,&#x22; divided into &#x22;Core Data Flow&#x22; and &#x22;Stability & Extensions,&#x22; listing different types of receivers, exporters, processors, and extensions. It emphasizes that a minimal core ensures predictable upgrades." />
</Frame>

## Collector Contrib — broad integrations, faster change

Contrib extends Core with community- and vendor-contributed components. It includes integrations for Prometheus, Kafka, Jaeger, cloud providers (AWS, Azure, GCP), and many other systems. Contrib is feature-rich and moves faster, but many components are experimental or community-maintained—validate maturity before production use.

<Frame>
  <img alt="The image is an educational slide titled &#x22;Understanding Contrib&#x22; featuring logos and names of various technologies like Prometheus, Kafka, Jaeger, AWS, Azure, and GCP. It includes notes stating &#x22;Not default for production&#x22; and &#x22;Validate maturity first.&#x22;" />
</Frame>

Component stability

Contrib components typically progress through these stability stages: Development → Alpha → Beta → Stable. Use Development/Alpha/Beta for experimentation. Only promote a component to production once it is declared Stable and validated in your environment. Stability may vary across signals (traces/metrics/logs) and across different features of the same component.

<Frame>
  <img alt="The image depicts a bar diagram showing stages of component stability: Development, Alpha, Beta, and Stable, progressing from testing to production. It illustrates how stability can vary per signal or feature." />
</Frame>

Feature gates

Experimental features are often controlled by feature gates (runtime toggles). Only enable feature gates after testing. Feature gates can be set via CLI or environment variables; check each component’s documentation for exact gate names and semantics.

Example usage patterns:

```bash theme={null}
