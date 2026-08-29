# Sampling Strategies

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Sampling-Strategies/page

Explains tracing sampling strategies across SDK and Collector, comparing SDK, head, and tail sampling and when to use transforms and sampling processors.

In this lesson we’ll compare sampling points and strategies across the OpenTelemetry stack: starting inside the application (SDK) and moving outward to the Collector. Each diagram is preserved in order and annotated so the flow and decision points are clear.

The OpenTelemetry SDK runs inside your application and is the first—most immediate—place to make sampling decisions for spans and traces.

<Frame>
  <img alt="The image is a diagram illustrating tracing in an application using an OTel SDK, noting &#x22;Tracing Begins: SDK Samplers at the Source.&#x22;" />
</Frame>

Why sample at the SDK?

* Lowers network and backend load by discarding unneeded spans early.
* Enables consistent per-process sampling configured without code changes.
* Limited by the local view: SDK sampling decisions occur at span creation time and cannot use eventual trace outcomes.

Below is a more focused view showing the SDK and the SDK Sampler component inside an application process.

<Frame>
  <img alt="The image is a diagram illustrating the reintroduction of the SDK Sampler in an app, featuring an &#x22;Application&#x22; box with &#x22;OTel SDK&#x22; and &#x22;SDK Sampler&#x22; highlighted." />
</Frame>

Common SDK sampler types and when to use them:

| Sampler                      | What it does                                                      | Use case                                      |
| ---------------------------- | ----------------------------------------------------------------- | --------------------------------------------- |
| AlwaysOn                     | Records all traces                                                | Debugging, development, short-lived tests     |
| AlwaysOff                    | Records no traces                                                 | Disable telemetry in specific runs            |
| TraceIdRatio (probabilistic) | Records a fixed percentage of traces using a hash of the trace ID | Control volume with predictable sampling rate |
| ParentBased                  | Follows the parent span's decision                                | Preserve trace consistency across services    |

<Frame>
  <img alt="The image shows a diagram of an &#x22;SDK Sampler&#x22; with different types: AlwaysOn, AlwaysOff, TraceIdRatio, and ParentBased. It is part of an application using the OTel SDK." />
</Frame>

Example: configure SDK sampling via environment variables (spec follows the OpenTelemetry specification and is cross-language):

```bash theme={null}
