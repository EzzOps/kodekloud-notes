# ParentBased uses the parent's decision if present; otherwise it falls back to TraceIdRatioBased.
provider = TracerProvider(sampler=ParentBased(root=TraceIdRatioBased(0.2)))
```

Agent / auto-instrumentation environment variables

For auto-instrumentation or agent-based setups you can change sampling without modifying application code. Example to set trace-id-ratio sampling to 20%:

```bash theme={null}
OTEL_TRACES_SAMPLER=traceidratio
OTEL_TRACES_SAMPLER_ARG=0.2
```

<Callout icon="lightbulb">
  Head-based sampling makes the decision at span creation time (in the SDK). Tail-based sampling can make decisions later based on whole-trace information; tail-based sampling is typically implemented in the OpenTelemetry Collector.
</Callout>

<Callout icon="warning">
  Avoid AlwaysOn in high-volume production unless you have capacity for the inbound throughput, storage, and query costs. Use rate-limited or ratio-based sampling for scalable production environments.
</Callout>

Recap — best practices and recommendations

* Use AlwaysOn for complete visibility during development and troubleshooting.
* Use AlwaysOff to disable tracing while keeping instrumentation code intact.
* Use TraceIdRatioBased or ParentBased with a ratio fallback for production to reduce telemetry volume while preserving representative traces.
* Prefer making sampling decisions as close to the source as possible to minimize unnecessary network and backend load. If you need whole-trace signals (for anomaly detection or root-cause across entire traces), consider tail-based sampling implemented in the Collector.

<Frame>
  <img alt="The image contains key takeaways in a colorful sidebar format, discussing observability, SDK configuration, and visibility in production." />
</Frame>

Tail-based sampling

Tail-based sampling uses whole-trace attributes (durations, error rates, aggregated metrics) to decide which traces to keep. It typically runs in the OpenTelemetry Collector or a dedicated backend to avoid making suboptimal head-based decisions when trace-wide context is required. Tail-based approaches incur higher upfront collection cost but can yield more targeted sampling decisions for complex production use cases.

Links and references

* OpenTelemetry Tracing Concepts: [https://opentelemetry.io/docs/concepts/signals/traces/](https://opentelemetry.io/docs/concepts/signals/traces/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* SDK sampling configuration: [https://opentelemetry.io/docs/reference/specification/sdk-environment-variables/](https://opentelemetry.io/docs/reference/specification/sdk-environment-variables/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/5f36117a-7eed-41a5-b698-a4d5b22cb5f4" />
</CardGroup>


# Zero Code Instrumentation in Java

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Zero-Code-Instrumentation-in-Java/page

Describes zero code Java instrumentation with the OpenTelemetry Java agent, configuration options, extensions, and use of manual spans.

In this lesson we'll examine zero-code instrumentation for Java applications: how it works, how to configure it, when to use manual spans, and how to extend the agent without changing application source.

Bytecode instrumentation is the core technique behind zero-code approaches. Instead of editing source code, an agent modifies compiled Java bytecode at class load or runtime. This injection of behavior lets you capture telemetry automatically — for example, timing HTTP requests or recording database calls — without cluttering business logic.

<Frame>
  <img alt="The image illustrates &#x22;How Bytecode Instrumentation Works&#x22; with a person at a laptop, surrounded by binary code, alongside figures representing code modification. It explains that bytecode instrumentation involves modifying compiled code at runtime or load time for additional behavior." />
</Frame>

Think of bytecode instrumentation as a behind-the-scenes upgrade that adds observability to your app without touching the source. For Java, the primary implementation is the OpenTelemetry Java agent.

What the OpenTelemetry Java agent provides

* Automatic instrumentation for many common libraries and frameworks
* Out-of-the-box traces and metrics for typical app building blocks
* Minimal or no code changes required to obtain telemetry

Typical capabilities include:

* Tracing incoming and outgoing HTTP requests
* Capturing database queries and connection metadata
* Tracking messaging events (Kafka, JMS, RabbitMQ, etc.)

<Frame>
  <img alt="The image illustrates what the OTel Java Agent covers, highlighting three areas: HTTP Requests, Database Queries, and Messaging Events, each represented by distinct icons." />
</Frame>

With the agent you immediately cover the major building blocks of most enterprise applications: web requests, persistence, and messaging.

Where to get the Java agent

* Repository: [open-telemetry/opentelemetry-java-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
* Releases page (download the `opentelemetry-javaagent.jar`): [https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases)

Basic JVM startup with the agent
A minimal JVM startup using the Java agent looks like:

```bash theme={null}
java -javaagent:opentelemetry-javaagent.jar -jar myapp.jar
```

This attaches the agent and enables automatic instrumentation. In practice you should also configure resource metadata (for example, service name) and the exporter so telemetry is sent to the backend you use.

Configure the agent with JVM properties or environment variables
Two common and recommended ways to configure the agent:

1. JVM system properties (`-D` flags) — useful for direct JVM launches and fine-grained control.
2. Environment variables (`OTEL_*`) — recommended in containerized environments (Docker, Kubernetes).

JVM system properties example (set service name and use Zipkin exporter):

```bash theme={null}
java -javaagent:path/to/opentelemetry-javaagent.jar \
  -Dotel.resource.attributes=service.name=my-app \
  -Dotel.traces.exporter=zipkin \
  -jar myapp.jar
```

Environment variables example (recommended for containers):

```bash theme={null}
OTEL_SERVICE_NAME=your-service-name \
OTEL_TRACES_EXPORTER=zipkin \
java -javaagent:path/to/opentelemetry-javaagent.jar \
  -jar myapp.jar
```

<Callout icon="lightbulb">
  For container deployments, environment variables (`OTEL_*`) are generally preferable to JVM `-D` properties because they integrate cleanly with container orchestration, secrets, and configuration management.
</Callout>

Two primary configuration channels:

* System properties using `-Dotel.*` JVM flags
* Environment variables using `OTEL_*` names

<Frame>
  <img alt="The image is a table outlining ways to configure an agent, including criteria such as system properties, environment variables, and custom spans, with corresponding usage examples." />
</Frame>

Manual / custom spans
Automatic instrumentation covers many common interactions, but you’ll still need manual (code-based) instrumentation for business logic sections that are not automatically instrumented. Manual spans require using the OpenTelemetry API in your application to create spans and set attributes at the points you choose.

Common configuration options (quick reference)
Below are commonly used environment variables and JVM properties to tune the Java agent. These are not exhaustive but cover the most important settings you’ll encounter.

| Setting                                                 | Purpose                                                      | Example                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| `OTEL_SERVICE_NAME`                                     | Service name shown in backends                               | `OTEL_SERVICE_NAME=my-service`                              |
| `otel.resource.attributes` / `OTEL_RESOURCE_ATTRIBUTES` | Additional resource key=value attributes                     | `-Dotel.resource.attributes=environment=prod,team=payments` |
| `OTEL_TRACES_EXPORTER`                                  | Choose traces exporter (e.g., `otlp`, `zipkin`, `jaeger`)    | `OTEL_TRACES_EXPORTER=otlp`                                 |
| `OTEL_PROPAGATORS`                                      | Configure context propagation (e.g., `tracecontext,baggage`) | `OTEL_PROPAGATORS=tracecontext,baggage`                     |
| `OTEL_TRACES_SAMPLER`                                   | Sampling strategy (`always_on`, `traceidratio`, etc.)        | `OTEL_TRACES_SAMPLER=traceidratio`                          |
| `OTEL_TRACES_SAMPLER_ARG`                               | Sampler argument (e.g., ratio)                               | `OTEL_TRACES_SAMPLER_ARG=0.1`                               |
| `OTEL_SDK_DISABLED`                                     | Disable the SDK entirely (useful for tests)                  | `OTEL_SDK_DISABLED=true`                                    |

Batch span processor and cardinality limits are also configurable (queue sizes, schedule delays, max attributes/events/links). Fine-tune these when optimizing performance and storage.

<Frame>
  <img alt="The image is a table outlining OpenTelemetry (OTel) Java environment variables and system properties related to propagation and sampling. It lists categories, properties, environment variables, descriptions, and defaults for each entry." />
</Frame>

Batch span processor controls and tuning
Performance-sensitive settings—such as batch processor queue size, schedule delay, and export timeout—help balance throughput and memory/latency trade-offs.

<Frame>
  <img alt="The image is a table detailing OpenTelemetry (OTel) Java environment variables and system properties for the Batch Span Processor, including categories, properties, environment variables, descriptions, and default values." />
</Frame>

From an exam or conceptual perspective, remember the major ones: service name, resource attributes, propagators, sampler, and exporter.

Supported libraries and frameworks
The Java agent supports a large number of libraries and frameworks. Check the instrumentation repository for the exhaustive list and to confirm coverage for your application’s dependencies.

<Frame>
  <img alt="The image lists various libraries supported by OpenTelemetry Java instrumentation, including Akka, Apache CXF, AWS Lambda, and more. It also provides a GitHub link for further details." />
</Frame>

Java agent extensions: customize without changing app code
Agent extensions let you enhance or change agent behavior without modifying the main agent distribution or your application code. Extensions are useful to keep the zero-code promise while adding custom logic.

Capabilities of extensions

* Add or configure span processors, exporters, samplers, or propagators
* Inject new instrumentation modules for libraries not yet supported
* Modify or filter span attributes (for example, mask sensitive data)
* Disable or override existing instrumentation behavior

Building and loading extensions
Package your extension as a JAR (for example, with Gradle):

```bash theme={null}
./gradlew build
