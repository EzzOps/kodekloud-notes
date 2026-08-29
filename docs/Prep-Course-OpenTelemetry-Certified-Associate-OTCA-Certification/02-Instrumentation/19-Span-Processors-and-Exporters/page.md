# Configure tracer provider and a simple console exporter
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

tracer = trace.get_tracer(__name__)

# Create a parent span and a nested child span
with tracer.start_as_current_span("parent-span"):
    with tracer.start_as_current_span("child-span"):
        print("Performing work inside child span")
```

Key steps in manual instrumentation:

* Set up a TracerProvider and exporters/processors.
* Acquire a tracer with `get_tracer(...)`.
* Use `start_as_current_span` (or equivalent) to create spans.
* Add attributes, events, and links to spans as needed for context.

## Trade-offs at a glance

| Approach             | Control                 | Effort                | Common Use Cases                                                          |
| -------------------- | ----------------------- | --------------------- | ------------------------------------------------------------------------- |
| Manual (code-based)  | High                    | High                  | Business-level spans, custom logic, precise tracing                       |
| Library-based        | Medium                  | Medium                | Framework-level coverage for web frameworks, DBs, messaging               |
| Auto-instrumentation | Lower (agent-dependent) | Low (no source edits) | Legacy apps, rapid coverage, environments where editing code is difficult |

<Frame>
  <img alt="The image is a table comparing different instrumentation approaches based on criteria like control, effort, custom logic, setup speed, and use case. The approaches compared are code-based/manual, zero-code/automatic, and instrumentation library." />
</Frame>

## Practical recommendations

* Start with library-based instrumentation for supported frameworks to get broad coverage quickly.
* Add manual spans for business-critical workflows where you need precise telemetry and contextual attributes.
* Use auto-instrumentation to bootstrap visibility in environments where changing source code is infeasible; follow up with library/manual enhancements for gaps.
* Always validate instrumentation: use console/log exporters, local tracing UIs, or sandboxed environments to confirm spans and attributes appear as expected.

> **warning** Auto-instrumentation agents may not capture all framework-specific behaviors or custom logic, and they can require permissions or configuration in production environments. Always validate agent compatibility and test in staging before rolling out to production.

## Next steps and further reading

This article is an overview. For deeper dives, review framework-specific instrumentation libraries and runtime agent docs. Practice by:

* Adding library-based instrumentation to a small service.
* Creating manual spans for a business-critical transaction.
* Testing auto-instrumentation with a sample app to understand agent configuration.

Links and references:

* [OpenTelemetry home](https://opentelemetry.io/)
* [OpenTelemetry specification](https://opentelemetry.io/docs/reference/specification/)
* [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/instrumentation/python/)
* [Auto-instrumentation guides and agents (language-specific)](https://opentelemetry.io/docs/instrumentation/)

Use these resources to explore language- and framework-specific guidance and to follow best practices for sampling, context propagation, and exporter configuration.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/f1875db1-a286-4afe-ac33-5725b585ff08)


# Span Processors and Exporters

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Span-Processors-and-Exporters/page

Explains OpenTelemetry span processors and exporters, their roles, Simple versus Batch processors, exporter behaviors, and production best practices for reliable telemetry delivery.

This lesson expands on span creation and instrumentation by explaining how span processors and span exporters interact within the OpenTelemetry SDK. You'll see how processors hook into span lifecycle events, how exporters deliver span data, and which combinations make sense for development versus production.

Quick example: print spans to the console

```python theme={null}
import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
