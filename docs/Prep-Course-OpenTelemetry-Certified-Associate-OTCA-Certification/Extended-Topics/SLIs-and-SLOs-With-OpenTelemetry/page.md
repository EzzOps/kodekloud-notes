# SLIs and SLOs With OpenTelemetry

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Extended-Topics/SLIs-and-SLOs-With-OpenTelemetry/page

Describes SLIs and SLOs and how OpenTelemetry captures metrics traces and logs to produce signals for SLO evaluation and observability

In this lesson we explain how Service-Level Indicators (SLIs) and Service-Level Objectives (SLOs) work together, and how OpenTelemetry (OTel) supplies the telemetry signals that feed SLI measurement and SLO evaluation.

What you'll learn:

* What SLIs and SLOs measure and why they matter
* Common SLI types and sample formulas
* How to convert raw telemetry into useful SLIs with OpenTelemetry
* Where SLO evaluation should occur in your observability stack

SLIs (Service-Level Indicators) are the primary, user-centric measurements that reflect service performance from the end-user perspective.

<Frame>
  <img alt="The image features the text &#x22;Understanding SLIs (Service-Level Indicators)&#x22; on a white background with a gradient blue geometric shape. It is credited to KodeKloud." />
</Frame>

Common SLI categories and what they represent:

| SLI category | What it measures                         | Typical user-focused question        |
| ------------ | ---------------------------------------- | ------------------------------------ |
| Availability | Whether the service is up and responding | "Is the site reachable?"             |
| Latency      | How quickly requests finish              | "How long do actions take?"          |
| Errors       | Frequency of failed requests             | "How often do users get errors?"     |
| Throughput   | Volume of handled requests               | "How much traffic do we serve?"      |
| Saturation   | Resource utilization and headroom        | "How close are resources to limits?" |

Metrics are useful raw signals, but to form meaningful SLIs you often convert counts and histograms into rates or proportions (percentages) that reflect user experience.

<Frame>
  <img alt="The image shows a simple diagram with two connected boxes labeled &#x22;Metrics&#x22; and &#x22;Rate,&#x22; illustrating the concept of using metrics to calculate rates." />
</Frame>

Quick formulas for common SLIs

* Success rate SLI:
  * Definition: Percentage of valid requests that are considered successful.
  * Formula: (good events / valid events) × 100

<Frame>
  <img alt="The image explains a formula for calculating &#x22;Success Rate SLIs,&#x22; which is the percentage of valid events that are good, defined as (good events / valid events) x 100." />
</Frame>

* Latency compliance SLI:
  * Definition: Fraction of requests finishing below a chosen latency threshold.
  * Formula: (requests below latency threshold / total requests) × 100

<Callout icon="lightbulb">
  When converting a fraction to a percentage, multiply by `× 100`. If you see diagrams showing `× 1000` in this context, that is incorrect for percentage conversion.
</Callout>

<Frame>
  <img alt="The image shows a formula for &#x22;Latency Compliance,&#x22; which measures the percentage of requests meeting a specified latency target. It calculates the proportion of requests below a latency threshold out of total requests, multiplied by 1000." />
</Frame>

* Error rate SLI:
  * Definition: How often requests fail.
  * Formula: (failed requests / total requests) × 100

From SLIs to SLOs: a practical workflow

1. Start with a user-centric goal — describe what a good user experience looks like.
2. Select an SLI that quantifies that goal (for example, latency \< 200 ms).
3. Define an SLO: how often will the SLI meet that criterion over a window? (e.g., 99% of requests under 200 ms, measured over 30 days).
4. Configure alerting for SLI trends and breaches so teams can act before SLA obligations are violated.

Example: suppose your SLO is "99% of requests under 200 ms over 30 days." If the current median response time rises to 1 second, an alert should prompt investigation and corrective actions: add capacity, roll back a release, or pause new deployments until reliability is restored.

User-centric SLIs are preferred

* Typical user-facing examples:
  * Page load P95 \< 250 ms
  * Success rate > 99.5%
* Infrastructure metrics (e.g., CPU usage) are useful for diagnostics but do not always correlate directly with perceived user experience. SLIs should focus on outcomes users care about.

OpenTelemetry and SLIs
OpenTelemetry captures the telemetry necessary to compute SLIs:

* Metrics: counters, gauges, histograms (e.g., request counts, latency histograms).
* Traces: span durations and status codes (useful for latency and success-rate calculations).
* Logs: can be parsed and converted into metrics for SLI computation.

<Frame>
  <img alt="The image shows a user-centric SLI dashboard for a web service, displaying page load time at 210 ms and a success rate of 99.5%, along with a latency histogram. The text below mentions OpenTelemetry capturing SLIs via metrics and traces." />
</Frame>

Practical notes:

* You can convert error counts observed in logs into metrics for SLI reporting.
* Use traces to derive precise latency (span duration) and success/failure indicators.

SLO analogy: tracking health metrics
Think of SLIs like blood sugar readings and SLOs like the target range you want readings to stay within over time. Individual readings may spike, but the goal is to keep the majority within range over the defined window.

<Frame>
  <img alt="The image uses a health analogy to explain Service Level Objectives (SLOs), illustrating blood sugar levels over a 7-day period within a healthy range of 4–7.8 mmol/L and highlighting a specific reading of 5.6 mmol/L." />
</Frame>

Example: latency over time

* Track latency measurements against an SLO threshold (for example, 200 ms).
* SLOs commonly allow occasional spikes as long as the overall compliance percentage meets the target (e.g., 99% over 30 days).

<Frame>
  <img alt="The image shows a line graph titled &#x22;Latency Measurements – 30 Days&#x22; with a blue line representing latency changes compared to an SLO target of 200 ms." />
</Frame>

How OpenTelemetry fits into the SLI/SLO workflow

* Applications instrumented with OpenTelemetry SDKs generate telemetry (metrics, traces, logs).
* The OpenTelemetry Collector can receive, preprocess, aggregate, and transform telemetry; it can also convert traces or logs into metrics when appropriate.
* Data is exported (OTLP or other exporters) to your backend monitoring/SLO platform where SLO evaluation, aggregation over windows, visualization, and alerting occur.

<Frame>
  <img alt="The image shows how OTel signals—metrics, traces, and logs—support SLIs by capturing counts and histograms, span duration and status, and providing supplementary context, respectively." />
</Frame>

OpenTelemetry provides standardization and transport for telemetry signals but does not itself enforce or evaluate SLOs. The Collector is useful for routing and preprocessing, but SLO computation and alerting typically happen in your backend or SLO platform.

<Frame>
  <img alt="The image lists key OpenTelemetry capabilities for SLIs, including language SDKs, metrics data models, collector pipelines, and vendor-neutral exports." />
</Frame>

Division of responsibilities

| Component            | Responsibility                                                                    |
| -------------------- | --------------------------------------------------------------------------------- |
| Application / SDK    | Generate accurate telemetry (instrument requests, spans, and events)              |
| Collector (optional) | Route, transform, pre-aggregate, and convert logs/traces to metrics where helpful |
| Backend / Platform   | Compute SLO compliance over windows, visualize SLOs, and trigger alerts           |

<Frame>
  <img alt="The image illustrates how responsibilities are divided across the stack in three stages: Application/SDK for SLI generation, OTel Collector for data routing, and Backend for SLO evaluation." />
</Frame>

OpenTelemetry does not perform SLO evaluation; it provides the signals that feed into your backend, which performs compliance calculations over the defined time windows.

<Frame>
  <img alt="The image outlines where Service Level Objectives (SLOs) are evaluated, divided into three levels: Application, Collector (optional), and Backend/Platform, with specific actions and notes for each level." />
</Frame>

<Callout icon="lightbulb">
  Avoid aggressive sampling when generating SLIs. Dropping or heavily sampling requests can reduce SLI accuracy and mask real reliability problems. If sampling is necessary, document its effect on SLI accuracy and consider adjustments in the backend.
</Callout>

Summary

* SLIs measure user-facing behavior (latency, success rate, errors, throughput) and should be defined from the user's perspective.
* SLOs are time-windowed targets applied to SLIs (e.g., 99% of requests under 200 ms over 30 days).
* OpenTelemetry standardizes and transports telemetry (metrics, traces, logs) to your backend — but SLO evaluation, rolling-window calculations, visualization, and alerting are responsibilities of your monitoring/SLO platform.
* Be cautious with sampling: it can undermine SLI accuracy if not managed carefully.

Further reading and references

* OpenTelemetry Project: [https://opentelemetry.io/](https://opentelemetry.io/)
* SLO concepts and examples: [https://landing.google.com/sre/sre-book/chapters/service-level-objectives/](https://landing.google.com/sre/sre-book/chapters/service-level-objectives/)
* Practical SLI/SLO tooling: check your monitoring vendor docs for SLO evaluation and alerting workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/b5241624-cc5d-43c9-a373-650368d82e61/lesson/966ab480-18fb-4d9f-9fd0-4d5f1a16f81f" />
</CardGroup>
