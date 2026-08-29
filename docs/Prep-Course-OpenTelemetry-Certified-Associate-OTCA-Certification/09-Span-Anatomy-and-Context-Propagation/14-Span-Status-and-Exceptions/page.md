# Define your own resource attributes
resource = Resource.create({
    "service.name": "image-processor",
    "deployment.environment": "staging",
    "team": "ml-platform"
})

# Set up the tracer provider with the resource
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Set up a console exporter to see spans in stdout (example)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(span_processor)

# Create and use a tracer; spans will inherit the resource attributes
tracer = trace.get_tracer("custom.resource.tracer")
with tracer.start_as_current_span("process_image"):
    print("Processing image...")
```

## Configure Resources via Environment Variables

In many deployments, especially with automatic instrumentation, configuring resources using environment variables is easier because it requires no code changes and works across CI/CD and orchestration tooling.

Example (bash):

```bash theme={null}
export OTEL_SERVICE_NAME="payment-service"
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production,cloud.provider=aws,team=ml-platform"
```

Using environment variables enforces consistent resource attributes across deployments and allows updates from CI/CD pipelines or orchestration tools.

<Frame>
  <img alt="The image describes four use cases for adding resource attributes related to telemetry: CI/CD pipeline integration, filtering and grouping, tracing across services, and supporting multi-cloud or multi-environment setups." />
</Frame>

## Common Use Cases

* Configure attributes from CI/CD or infrastructure without modifying code.
* Filter and group telemetry in the backend (for example, show only traces from `production`).
* Facilitate cross-service tracing by consistently tagging spans.
* Support multi-cloud or multi-environment setups by tagging `cloud.provider` or `region`.

## Summary

* A Resource in OpenTelemetry defines the origin of telemetry data (service, host, container, environment).
* Configure the resource once during SDK initialization; it is automatically applied to all spans, metrics, and logs produced by that SDK instance.
* Default attributes include `service.name` (defaults to `unknown_service`), `telemetry.sdk.name`, `telemetry.sdk.language`, and `telemetry.sdk.version`.
* Resource detectors can automatically collect metadata (host, process, container, Kubernetes, cloud provider).
* You can add additional attributes manually via `Resource.create(...)` in code or via the `OTEL_RESOURCE_ATTRIBUTES` environment variable.
* Follow semantic conventions for attribute names to ensure consistency across telemetry.

<Frame>
  <img alt="The image is a summary of OpenTelemetry resource configuration, highlighting key points about defining telemetry data origins, SDK initialization, default attributes, and resource detectors." />
</Frame>

<Callout icon="lightbulb">
  For consistent and searchable telemetry, set `service.name` and other domain-specific attributes using OpenTelemetry semantic conventions. Prefer environment variables for deployment-wide defaults and let resource detectors populate infrastructure-level attributes automatically.
</Callout>

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Semantic Conventions for Resources: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/semantic\_conventions/](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/semantic_conventions/)

That's it for this section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/ce08725b-eb7c-4f0a-b00b-38eb399793b7" />
</CardGroup>


# Span Status and Exceptions

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Status-and-Exceptions/page

Explains OpenTelemetry span status and exceptions, describing UNSET OK ERROR values, how exceptions set ERROR, and guidance on when to use OK or leave UNSET

In this lesson we’ll explain span status: what it is, why it matters, and how exceptions affect it in distributed tracing (OpenTelemetry).

What is span status?

A span status indicates the result or outcome of a traced operation. When you run multiple services, they can emit hundreds or thousands of spans per minute. At scale, span status helps you quickly answer questions such as: Did an operation succeed? Are errors concentrated in a single service or spread across many?

<Frame>
  <img alt="The image explains the concept of &#x22;Span Status,&#x22; indicating the result of an operation tracked by a span, with a graphic of an upward trend on a monitor. It poses the question of whether the operation succeeded, failed, or was unspecified." />
</Frame>

Why status matters

* It highlights the success or failure of individual spans within a trace.
* It enables error detection and filtering in observability platforms (for example: show all spans with `status = ERROR` between 09:00–10:00).
* It supports root-cause diagnostics across distributed systems by indicating which service, application, or environment is experiencing problems.

<Frame>
  <img alt="The image explains why status matters with three points: highlighting span success or failure, enabling error detection in observability platforms, and supporting diagnostics across systems." />
</Frame>

Span status values

Span status is represented by one of three values:

* `UNSET` (default)
* `ERROR`
* `OK`

<Frame>
  <img alt="The image shows a Venn diagram with three intersecting circles labeled &#x22;UNSET (default)&#x22;, &#x22;ERROR&#x22;, and &#x22;OK&#x22;, each containing a number (01, 02, 03). It represents the three possible status values of a span." />
</Frame>

Use this summary table to choose the right status:

| Status  | When to use                                                          | Notes                                                                                |
| ------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `UNSET` | Default for most spans; nothing noteworthy from an error perspective | Implies implicit success — common and usually preferred                              |
| `ERROR` | When an exception, timeout, or HTTP 4xx/5xx is observed              | Instrumentation or application code can set this to surface failures                 |
| `OK`    | When you explicitly want to mark a span as successful                | Useful to override the default when handled errors should not be considered failures |

How exceptions set status

Tracing instrumentation commonly creates exception events on spans and sets the span `status` to `ERROR`. A typical span payload with an exception event and an `ERROR` status looks like:

```json theme={null}
{
  "status": {
    "status_code": "ERROR",
    "description": "404 Client Error: NOT FOUND for url: http://httpbin.org/delay"
  },
  "events": [
    {
      "name": "exception",
      "timestamp": "2025-05-01T12:58:08.969805Z",
      "attributes": {
        "exception.type": "HTTPError",
        "exception.message": "404 Not Found",
        "exception.stacktrace": "raise_for_status() -> HTTPError",
        "exception.escaped": "False"
      }
    }
  ]
}
```

<Callout icon="lightbulb">
  The attributes `exception.type`, `exception.message`, and `exception.stacktrace` follow the OpenTelemetry semantic conventions for exceptions. These attributes let observability tools display error details and group similar errors. See the OpenTelemetry spec for exceptions for more details: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]\_conventions/exceptions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/exceptions/)
</Callout>

When a span contains an exception event like the example above, the tracing SDK or instrumentation typically sets `status` to `ERROR` and includes a summary description. This makes it straightforward to filter traces for failures and inspect the associated exception attributes.

When to use `OK` versus leaving status `UNSET`

* Keep `UNSET` when nothing noteworthy has occurred (the implicit success path). This is the common default.
* Use `OK` when you intentionally want to mark a span as successful despite non-standard conditions. Examples:
  * Your application handles certain errors internally (e.g., a cache miss producing an HTTP 404 that is expected) and you do not want these spans to appear as failures.
  * A span represents a step in a multi-step or asynchronous process where success is only known later; set `OK` explicitly when the overall operation completes successfully.

<Frame>
  <img alt="The image is a table detailing use cases and reasons for using &#x22;OK&#x22; instead of &#x22;Unset&#x22; in certain coding contexts. It lists scenarios like handling internal errors, overriding default behavior, and signaling completeness in asynchronous operations." />
</Frame>

Recap

* Span events (especially exception events) carry attributes such as `exception.type`, `exception.message`, and `exception.stacktrace`.
* Span status offers an at-a-glance indication of success (`OK`), failure (`ERROR`), or implicit/unspecified success (`UNSET`).
* Most spans remain `UNSET`. Use `ERROR` for detected failures and set `OK` explicitly only when you need to override default behavior.

<Frame>
  <img alt="The image outlines a recap of span status with three main points: span events provide details, span status indicates success or failure, and explicit &#x22;OK&#x22; usage is not usually necessary." />
</Frame>

Further reading and references

* OpenTelemetry Tracing: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* OpenTelemetry Semantic Conventions — Exceptions: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]\_conventions/exceptions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/exceptions/)

That covers span status and how exceptions affect it.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/7d493c36-e9fc-4df7-bdf4-e49bb5039860" />
</CardGroup>
