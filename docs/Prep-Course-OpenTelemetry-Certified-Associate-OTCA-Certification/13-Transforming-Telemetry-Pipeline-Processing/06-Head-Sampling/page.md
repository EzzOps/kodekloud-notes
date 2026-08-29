# Head Sampling

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Head-Sampling/page

Describes probabilistic head sampling that deterministically retains a fixed percentage of incoming traces at the collector to reduce telemetry volume while risking dropping error and high latency traces.

Head sampling is a collector-level sampling strategy that makes the sampling decision as soon as a trace (or its first span) arrives — before most processing or exporting occurs. A head (probabilistic) sampler retains a fixed fraction of traces (for example, 10%), reducing telemetry volume early in the pipeline and lowering ingestion and storage costs.

<Frame>
  <img alt="The image explains &#x22;How Head Sampling Works,&#x22; highlighting that head sampling decides on trace processing as they arrive, and a probabilistic sampler retains a set percentage of traces, such as 10%." />
</Frame>

How the probabilistic sampler works (high level):

1. Each incoming trace is evaluated by the sampler when it first arrives at the collector.
2. The sampler deterministically hashes the trace ID together with a seed value.
3. The hash result is mapped to a numeric range and compared against a threshold derived from the configured sampling percentage.
4. If the hash-derived value falls within the threshold (for example, the `10%` bucket), the trace is retained and forwarded to downstream processors or exporters; otherwise the trace is dropped.

Key control parameters for probabilistic head sampling:

| Parameter             | Purpose                                                                             | Example / Notes                                             |
| --------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `sampling_percentage` | Fraction of traces to keep                                                          | `10` (keeps \~10% of traces)                                |
| Hash seed             | Alters which trace IDs are selected; enables consistent selection across collectors | Use same seed across collectors for deterministic selection |
| Hash algorithm        | Maps trace ID to numeric range (implementation detail)                              | Typically fixed by the sampler implementation               |

<Callout icon="lightbulb">
  Using a deterministic hash of the trace ID plus a stable seed enables consistent sampling decisions across collectors and services. If multiple collectors share the same seed and algorithm, the same trace ID will be sampled consistently.
</Callout>

Benefits and trade-offs

| Benefit                                                    | Trade-off                                                                                                         |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Predictable reduction in telemetry volume and backend cost | Sampling occurs before trace completion, so post-hoc signals (errors, long latency) cannot influence the decision |
| Reduced processing and export load early in the pipeline   | Important error or slow traces may be dropped if not selected by the probabilistic hash                           |

<Frame>
  <img alt="The image compares the benefit and trade-off of head sampling. The benefit is predictable cost control, reducing storage and backend costs, while the trade-off is potentially dropping important traces too early." />
</Frame>

Because head sampling decides before a trace completes, it cannot inspect the finished trace for error flags, latency, or other attributes. That means error traces or very slow traces may be dropped probabilistically and never forwarded to storage or analysis tools.

Example scenario:

* 100 traces arrive, including successful, failed, and slow traces (e.g., 1,500 ms).
* A probabilistic sampler configured with `sampling_percentage: 10` is applied.
* Only \~10 traces will be retained and forwarded; critical errors or slow traces may not be included unless the sampler happens to pick them.

When to use head sampling

* Use head sampling when you need early, deterministic reduction of telemetry volume to control costs and backend load.
* Avoid relying on head sampling alone when you must guarantee capture of errors or high-latency traces.

Combining strategies

* A common approach is to combine a low-rate head sampler with a tail sampler: use head sampling to reduce baseline volume, and use tail-based sampling (which evaluates traces after completion) to ensure retention of error or high-latency traces.
* Another pattern is to apply head sampling for most traffic and selectively increase retention for services or routes known to be critical.

Configuring a basic probabilistic head sampler in the OpenTelemetry Collector

```yaml theme={null}
