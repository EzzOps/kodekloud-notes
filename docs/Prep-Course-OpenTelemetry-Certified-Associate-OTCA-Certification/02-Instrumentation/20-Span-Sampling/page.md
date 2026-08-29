# Set up the tracer provider and console exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure the processor to print spans to the console
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

def call_slow_api():
    with tracer.start_as_current_span("call_httpbin_delay"):
        url = "http://httpbin.org/delay/2"
        response = requests.get(url)
        return response.text

def main():
    with tracer.start_as_current_span("main_function_span"):
        print("Calling slow API...")
        result = call_slow_api()
        print("Done! Response length:", len(result))

if __name__ == "__main__":
    main()
```

When you run the script, the application output might show the usual program prints:

```plaintext theme={null}
Done! Response length: 358
```

And the ConsoleSpanExporter will emit JSON representations of spans, for example:

```json theme={null}
{
  "name": "call_httpbin_delay",
  "context": {
    "trace_id": "0x4998946a263b30828807138967d73",
    "span_id": "0x46dad3e62ea2b0"
  },
  "kind": "SpanKind_INTERNAL",
  "start_time": "2025-06-10T11:57:19.783180Z",
  "end_time": "2025-06-10T11:57:22.079506Z",
  "status_code": "UNSET",
  "attributes": {},
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.31.1"
    }
  },
  "schema_url": ""
}
```

```json theme={null}
{
  "name": "main_function_span",
  "context": {
    "trace_id": "0x4998946a263b30828807138967d73",
    "span_id": "0x2e4bcac22113"
  },
  "kind": "SpanKind_INTERNAL",
  "start_time": null,
  "end_time": null,
  "status_code": "UNSET",
  "attributes": {},
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.31.1",
      "service.name": "unknown_service"
    }
  },
  "schema_url": ""
}
```

How processors and exporters fit together
A span processor lives between the TracerProvider and an exporter. It receives lifecycle callbacks (typically onStart and onEnd) so it can observe spans when they start and finish. Processors generally only act on spans that are recording — i.e., `span.is_recording()` — to avoid unnecessary work on non-recording spans.

<Frame>
  <img alt="The image illustrates a three-step process of how span processors work, involving hooking into span start and end, running if the span is recording, and processing spans before export." />
</Frame>

Processor types: immediate vs. batched
OpenTelemetry SDKs provide two common processor implementations:

* SimpleSpanProcessor
  * Forwards each finished span immediately to the configured exporter.
  * Great for local development and debugging because spans appear right away.
  * Not ideal for high-volume production workloads: every finished span triggers an export call.

* BatchSpanProcessor
  * Buffers spans in memory and exports them as batches (on a timer or when buffer thresholds are met).
  * Much more efficient for production and recommended as the default.

Think of SimpleSpanProcessor as a firehose (direct and immediate) and BatchSpanProcessor as a postal service (batching and scheduled delivery).

> **lightbulb** BatchSpanProcessor is generally recommended for production because it minimizes export overhead. Use SimpleSpanProcessor for learning, debugging, or when you need immediate visibility of spans.

Exporters: destinations and responsibilities
A span exporter takes span data and delivers it to an external destination (console, OTLP endpoint, or a vendor backend). The exporter is responsible for converting span objects into the expected wire/transport format and transmitting them.

Common exporters and when to use them:

|            Exporter | Purpose / Use case                   | Notes / Examples                                                                                                         |
| ------------------: | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| ConsoleSpanExporter | Print spans to stdout for debugging  | Quick feedback during development                                                                                        |
|      OTLP exporters | Send spans using the `OTLP` protocol | Use with OpenTelemetry Collector or OTLP-compatible backends ([OTLP protocol](https://opentelemetry.io/protocols/otlp/)) |
|      JaegerExporter | Send spans to Jaeger                 | Use when your observability backend is Jaeger ([Jaeger](https://www.jaegertracing.io/))                                  |
|      ZipkinExporter | Send spans to Zipkin                 | Use when your backend is Zipkin ([Zipkin](https://zipkin.io/))                                                           |

Exporter lifecycle and important methods
Exporters expose a small set of behaviors application authors should understand:

1. export(spans): Send a batch of spans to the configured destination (BatchSpanProcessor calls this automatically).
2. shutdown(): Stop exporting and release resources. Call during application termination to avoid losing telemetry.
3. force\_flush() / forceFlush(): Attempt to immediately export any buffered spans, bypassing normal batching.

<Frame>
  <img alt="The image describes three key exporter behaviors: &#x22;export()&#x22; to send a batch of spans, &#x22;shutdown()&#x22; to clean up and stop exporting, and &#x22;forceFlush()&#x22; to try exporting pending spans immediately." />
</Frame>

Putting the pieces together

* Tracer: creates spans as your application instrumentations run.
* Processor: observes span lifecycle events (onStart/onEnd). SimpleSpanProcessor exports immediately; BatchSpanProcessor buffers and exports in batches (recommended for production).
* Exporter: formats and transmits spans to a destination (console, OTLP, Jaeger, Zipkin, etc.). Use `force_flush()` and `shutdown()` to ensure reliable delivery at shutdown.

<Frame>
  <img alt="The image is a recap of span processors and exporters, explaining their roles and recommending the use of BatchSpanProcessor in production." />
</Frame>

Best practices and production guidance

* Use BatchSpanProcessor for production to reduce network and CPU overhead.
* Configure exporter timeouts and retry policies (when supported) to handle transient failures.
* Always call `shutdown()` (or ensure the SDK does so) during graceful shutdown to minimize data loss.
* If you need telemetry routing, enrichment, or buffering across services, send spans to an OpenTelemetry Collector using OTLP and let the Collector forward to your backends.

> **warning** Be sure to call exporter `shutdown()` or use `force_flush()` on application shutdown. Failing to flush buffered spans can result in lost telemetry.

Collector and typical deployment patterns
Many deployments route telemetry from applications to an OpenTelemetry Collector using OTLP. The Collector centralizes processing, sampling, batching, and routing to one or more backends — improving flexibility and operational control.

Links and references

* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
* [OTLP protocol](https://opentelemetry.io/protocols/otlp/)
* [Kubernetes Observability patterns and the OpenTelemetry Collector](https://opentelemetry.io/docs/)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* [Zipkin](https://zipkin.io/)

That concludes this lesson on span processors and exporters.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/0a375888-a1fc-452e-889e-7380e7b4de65)


# Span Sampling

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Span-Sampling/page

Explains OpenTelemetry span sampling, timing, common samplers, and head versus tail sampling, plus configuration to control telemetry volume, cost, and trace consistency.

In this lesson, we explain span sampling in OpenTelemetry: what it is, why it matters, where it applies, common samplers, and how to configure head-based sampling. Sampling controls which spans are recorded and exported so you can retain meaningful telemetry while reducing cost, load, and noise.

A span is the basic unit of a trace. Sampling is the mechanism that decides whether a span (and usually its associated trace) is recorded or dropped. Effective sampling improves signal-to-noise, lowers network and storage costs, and keeps backend systems performant.

<Frame>
  <img alt="The image is an overview of sampling techniques with three sections that focus on span decisions, controlling data volume, and span creation time, each represented with icons and gradient colors." />
</Frame>

Why sampling timing matters

* Sampling decisions are normally made at span creation time (head-based sampling). Making decisions at the source reduces the amount of telemetry transmitted and processed.
* The sampling decision affects child spans and downstream services—propagating a consistent decision prevents partial traces from being stored.
* Delaying decisions (tail-based sampling) allows using whole-trace attributes to make smarter sampling choices but requires collecting more data up-front and is typically implemented in the Collector.

<Frame>
  <img alt="The image emphasizes the importance of sampling in large systems, highlighting issues like backend overload, increased network and storage costs, and added latency or CPU usage." />
</Frame>

Where sampling applies

* The sampler evaluates the current span at creation time and decides whether it should be recorded.
* Sampling decisions commonly propagate to child spans: if a parent is not sampled, child spans are typically dropped to keep trace consistency.
* Trace flags (for example, the sampled bit in the trace context) carry the sampling choice across process boundaries so the distributed system respects the decision end-to-end.

<Frame>
  <img alt="The image illustrates where sampling applies, featuring three categories: Current Span, Child Spans, and TraceFlags, each represented by a colored icon." />
</Frame>

Built-in samplers (OpenTelemetry SDKs)

The following samplers are commonly available across OpenTelemetry SDKs. Use the option that best balances visibility and cost for your environment.

| Sampler                  | Purpose / Use Case                                                                                                                                                              | Example                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| AlwaysOnSampler          | Records every span. Best for development, debugging, or short-lived environments where full visibility is required.                                                             | `AlwaysOnSampler()`                        |
| AlwaysOffSampler         | Records no spans. Useful to keep instrumentation hooks enabled while disabling telemetry.                                                                                       | `AlwaysOffSampler()`                       |
| TraceIdRatioBasedSampler | Samples a fixed fraction of traces (head-based). Good for scalable production sampling (e.g., 10% or 20%).                                                                      | `TraceIdRatioBased(0.2)`                   |
| ParentBasedSampler       | Adopts the parent's sampling decision if present; otherwise falls back to a configured root sampler. Useful for distributed systems to maintain consistent downstream behavior. | `ParentBased(root=TraceIdRatioBased(0.2))` |

<Frame>
  <img alt="The image lists built-in sampling strategies including AlwaysOnSampler, AlwaysOffSampler, TraceIdRatioBasedSampler, and ParentBasedSampler, with descriptions and use cases for each." />
</Frame>

Configuring head-based sampling (SDK and environment)

Python SDK examples:

* Configure TraceIdRatioBased sampler at the SDK level for 20% sampling:

```python theme={null}
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

provider = TracerProvider(sampler=TraceIdRatioBased(0.2))  # 20% sampling
```

* Combine ParentBased with TraceIdRatioBased as a fallback (parent decision preferred):

```python theme={null}
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
