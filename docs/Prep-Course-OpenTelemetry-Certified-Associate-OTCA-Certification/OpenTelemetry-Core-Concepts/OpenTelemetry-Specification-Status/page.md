# OpenTelemetry Specification Status

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-Specification-Status/page

Overview of OpenTelemetry specification maturity, component lifecycle stages, and signal status to guide production readiness

Hello OpenTelemetry users — this lesson reviews the OpenTelemetry specification status and the lifecycle used to communicate maturity and stability for components and signals.

Understanding component maturity helps set expectations for design, support, and production readiness. Below is a concise lifecycle definition followed by the official status summary for common signals.

## OpenTelemetry component lifecycle

| Stage        | What it means                                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Draft        | Design phase. Not yet part of the specification; requirements and APIs are still evolving.                                 |
| Experimental | Released for community testing. Use to validate design and provide feedback; not guaranteed stable or backward-compatible. |
| Stable       | Backward compatible and production-ready. Includes long-term support expectations.                                         |
| Deprecated   | Stable for a transition period but scheduled for removal; users should plan migration paths.                               |

<Frame>
  <img alt="The image illustrates the OpenTelemetry Component Lifecycle, showing four stages: Draft, Experimental, Stable, and Deprecated. Each stage is described with its current status and purpose in the lifecycle." />
</Frame>

<Callout icon="lightbulb">
  The specification status pages evolve over time. Check the official OpenTelemetry specs/status pages ([OpenTelemetry specification repository](https://github.com/open-telemetry/opentelemetry-specification)) for the latest maturity indicators before making production decisions.
</Callout>

## Official status summary (signals and components)

The OpenTelemetry specification provides a status summary table for each signal across these components: API, SDK, OTLP protocol, and Collector. The table below condenses the current maturity snapshot for common signals. This helps teams decide which parts are safe to rely on in production and which are still maturing.

| Signal / Component |                     API |                            SDK | OTLP protocol           | Collector                                                   |
| ------------------ | ----------------------: | -----------------------------: | ----------------------- | ----------------------------------------------------------- |
| Tracing            |                  Stable |                         Stable | Stable                  | Stable                                                      |
| Metrics            |                  Stable | Mixed (some evolving features) | Stable                  | Mostly production-ready; some pipelines remain experimental |
| Logs               |     Stable (Bridge API) |                         Stable | Stable                  | Supported                                                   |
| Baggage            | Stable (feature freeze) |                         Stable | Not applicable          | Not applicable                                              |
| Profiling          | Experimental / Maturing |        Experimental / Maturing | Experimental / Maturing | Exploring collection and instrumentation support            |

<Frame>
  <img alt="The image is a summary table showing the status of various OpenTelemetry signal components, including API, SDK, OTLP protocol, and Collector, across different signals like tracing, metrics, logs, baggage, and profile. Each component is marked as stable, mixed, experimental, or with other relevant status descriptions." />
</Frame>

Profiling remains early-stage: APIs, SDKs, and protocol definitions are still maturing, and the Collector is experimenting with continuous profiling features and related instrumentation/collection workflows.

## How to use this information

* Prefer Stable components for production workloads (e.g., tracing).
* Use Experimental components with caution and for testing or evaluation purposes.
* Track deprecation notices and migration guidance for components marked Deprecated.
* Consult the canonical status table in the specification repository before adopting or upgrading components.

Links and references

* [OpenTelemetry specification repository — status & maturity](https://github.com/open-telemetry/opentelemetry-specification)
* [OpenTelemetry documentation](https://opentelemetry.io/)
* [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)

That's it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/877fa624-b2d6-411e-8f41-fc9fba15b7c7" />
</CardGroup>
