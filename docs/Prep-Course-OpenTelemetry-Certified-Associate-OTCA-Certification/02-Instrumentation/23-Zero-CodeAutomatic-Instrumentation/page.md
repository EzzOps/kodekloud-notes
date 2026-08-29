# Exclude health/metrics endpoints from tracing
export OTEL_PYTHON_EXCLUDED_URLS="/health,/metrics"

# Trace specific Django request attributes
export OTEL_PYTHON_DJANGO_TRACED_REQUEST_ATTRS="path_info,content_type"

# Enable log correlation and format logs to include trace/span ids
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_FORMAT="%(msg)s [trace_id=%(trace_id)s span_id=%(span_id)s]"
export OTEL_PYTHON_LOG_LEVEL=debug

# Disable specific auto-instrumentations when needed
export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=redis,grpc,kafka
```

You can control sampling, exporters, and many other settings via environment variables—most are consistent across languages, with some Python-only options shown above.

<Frame>
  <img alt="The image shows a list of OpenTelemetry agent settings with their descriptions, including service name, traces exporter, metrics exporter, and endpoint details. It appears to be from a tutorial or guide by KodeKloud." />
</Frame>

## Supported libraries (auto-instrumentation)

OpenTelemetry Python provides many built-in instrumentations and community-contributed packages. Typical coverage includes web frameworks, HTTP clients, database libraries, and messaging systems.

|               Category | Examples                                     |
| ---------------------: | -------------------------------------------- |
|         Web frameworks | Flask, Django, FastAPI, Starlette            |
|           HTTP clients | `requests`, `urllib3`                        |
|              Databases | SQLAlchemy and DB drivers (e.g., `psycopg2`) |
| Messaging & Background | Kafka, Celery                                |

This coverage gives immediate visibility across web requests, outbound HTTP calls, DB queries, and messaging layers.

<Frame>
  <img alt="The image lists popular libraries with built-in instrumentation categorized as Web, HTTP, DB, and Messaging, featuring Flask, Django, FastAPI, Starlette, urllib3, SQLAlchemy, psycopg2, Kafka, and Celery." />
</Frame>

## Debugging automatic instrumentation

If a library isn’t being instrumented or spans/attributes are missing, enable debug logging to see detailed messages about what instrumentations are applied and any errors:

```bash theme={null}
export OTEL_LOG_LEVEL=debug
export OTEL_PYTHON_LOG_LEVEL=debug
```

Run your app under the instrument wrapper and inspect logs to identify missing hooks, import order issues, or conflicts between instrumentations.

## Repository & documentation

Key resources:

* Instrumentation libraries and contrib repo: [https://github.com/open-telemetry/opentelemetry-python-contrib](https://github.com/open-telemetry/opentelemetry-python-contrib)
* Auto-instrumentation CLI docs: [https://opentelemetry.io/docs/instrumentation/python/auto-instrumentation/](https://opentelemetry.io/docs/instrumentation/python/auto-instrumentation/)
* PyPI instrumentation package: [https://pypi.org/project/opentelemetry-instrumentation/](https://pypi.org/project/opentelemetry-instrumentation/)
* SDK configuration docs: [https://opentelemetry.io/docs/reference/specification/sdk-configuration/](https://opentelemetry.io/docs/reference/specification/sdk-configuration/)

Useful commands referenced in docs:

```text theme={null}
opentelemetry-bootstrap [-a|--action=][install|requirements]
opentelemetry-instrument python program.py
```

Installation via pip examples:

```bash theme={null}
pip install opentelemetry-instrumentation
pip install opentelemetry-distro opentelemetry-exporter-otlp
```

<Frame>
  <img alt="The image shows a documentation page for &#x22;General SDK Configuration&#x22; in OpenTelemetry, detailing configuration settings like OTEL_SDK_DISABLED and OTEL_ENTITIES with descriptions, default values, and notes. The page includes a navigation sidebar and various configuration details for developers." />
</Frame>

## Python vs Java (brief comparison)

| Topic                  | Python (auto-instrumentation)                                                 | Java (javaagent)                                                        |
| ---------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Mechanism              | Monkey patching — wrap/replace functions at runtime                           | Bytecode instrumentation — modify classes at JVM startup (`-javaagent`) |
| Tooling                | `opentelemetry-instrument`, `opentelemetry-distro`, `opentelemetry-bootstrap` | `opentelemetry-javaagent.jar`                                           |
| Configuration          | CLI flags or environment variables (e.g., `OTEL_*`, `OTEL_PYTHON_*`)          | JVM agent flags and environment variables                               |
| Manual instrumentation | Optional via SDK APIs for custom spans                                        | Optional via SDK APIs for custom spans                                  |
| Log correlation        | `OTEL_PYTHON_LOG_CORRELATION=true` and log formatter support                  | Supported via JVM logging frameworks and agent config                   |

## Summary

OpenTelemetry Python zero-code instrumentation (auto-instrumentation) provides immediate observability for many common libraries without modifying application source code. Workflow summary:

1. Install distro + exporters + instrumentation packages.
2. Run `opentelemetry-bootstrap -a install` to add relevant instrumentations.
3. Start your app with `opentelemetry-instrument` or use equivalent environment variables.
4. Tune Python-specific options (exclusions, log correlation, disabled instrumentations) as needed.

These steps let you quickly capture telemetry (traces and metrics) across web, HTTP client, DB, and messaging layers with minimal operational overhead.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/712825de-6ca0-4b88-8032-9a1f628f5560)


# Zero CodeAutomatic Instrumentation

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Zero-CodeAutomatic-Instrumentation/page

Zero-code automatic instrumentation using agents to add OpenTelemetry traces metrics and logs at runtime without source changes via bytecode manipulation monkey patching or eBPF for rapid observability

Code-based and library-based instrumentation require changing application source code: you need access to the code and knowledge of where to add instrumentation. In many real-world situations you may not have source access or permission to modify the application. In those cases, automatic (zero-code) instrumentation is often the fastest and least intrusive way to add observability.

In zero-code instrumentation, an agent injects telemetry at runtime so an application begins producing traces, metrics, and logs without any source changes. You do not need to learn the OpenTelemetry API/SDKs or modify the application to get basic observability.

<Frame>
  <img alt="The image illustrates &#x22;Automatic / Zero-Code Instrumentation&#x22; with a person examining code on a computer screen and others working on a syringe-like instrument. It conveys the concept of automatic telemetry data generation without code changes." />
</Frame>

What does zero-code instrumentation look like in practice? Here are two common, practical examples for JVM and Python applications.

* Java (JVM): attach the OpenTelemetry Java agent when starting the JVM:

```bash theme={null}
java -javaagent:/path/to/opentelemetry-javaagent.jar -jar myapp.jar
```

The Java agent instruments supported frameworks and libraries at class-load time by modifying bytecode. No source changes are required.

* Python: use the OpenTelemetry CLI wrapper to instrument supported libraries at runtime:

```bash theme={null}
opentelemetry-instrument python app.py
```

The CLI performs monkey-patching of common libraries (Flask, Django, Requests, etc.) so the running process emits telemetry without modifying `app.py`.

Both examples turn an existing application into a telemetry-producing source with no code edits. This makes automatic instrumentation a fast way to add observability—often in minutes.

The main advantage is speed: enable it quickly without touching the code. It's ideal for legacy apps, third-party binaries, or environments where developers cannot modify source. The trade-off is that domain-specific or business-logic spans are generally not created automatically; automatic instrumentation covers widely used frameworks and libraries but cannot infer custom business operations.

<Frame>
  <img alt="The image shows a comparison of pros and cons for a concept. Pros include zero code changes and compatibility, while cons mention limitations with domain-specific operations." />
</Frame>

How does the agent inject instrumentation without changing source code? Common techniques include:

* Monkey patching: used in dynamic languages such as Python and JavaScript. At runtime, the agent replaces or wraps library functions to call telemetry APIs.
* Bytecode manipulation: used in statically compiled runtimes such as Java and .NET. The agent modifies bytecode as classes/assemblies are loaded to insert telemetry before/after method execution.
* eBPF-based instrumentation: OpenTelemetry’s eBPF initiative observes system-level events (network, syscalls) from the kernel, providing language-agnostic and non-intrusive telemetry—useful in containerized or polyglot environments (see [https://github.com/open-telemetry/opentelemetry-ebpf](https://github.com/open-telemetry/opentelemetry-ebpf)).

Each technique has different trade-offs in terms of fidelity, overhead, and visibility into application internals.

<Frame>
  <img alt="The image outlines three techniques used in zero-code instrumentation: monkey patching (Python, JavaScript), bytecode manipulation (Java, .NET), and OpenTelemetry eBPF instrumentation (OBI)." />
</Frame>

When these techniques run, agents typically provide the OpenTelemetry API and SDK implementations at runtime (or hook into existing ones). That means exporters, processors, and resource configuration become available so spans, metrics, and logs can be produced and exported without touching application source code.

<Frame>
  <img alt="The image shows a diagram of injected OpenTelemetry capabilities at runtime, featuring the OpenTelemetry API and SDK." />
</Frame>

What parts of an application get instrumented automatically? Typical coverage includes:

|          Category | Typical Examples                    |
| ----------------: | ----------------------------------- |
|      HTTP clients | Requests, `http.client`, axios      |
|    Web frameworks | Flask, Django, Express, Spring Boot |
|  Database clients | SQLAlchemy, JDBC drivers            |
| Messaging systems | Kafka, RabbitMQ, AMQP libraries     |

Automatic instrumentation usually does not capture application-specific business logic—those spans must be added with code-based instrumentation if you need fine-grained, domain-specific traces.

<Frame>
  <img alt="The image depicts categories of services that are instrumented automatically: HTTP Clients, Web Frameworks, Database Clients, and Messaging Systems. It notes that custom business logic requires code-based instrumentation." />
</Frame>

Configuration: even without source access, zero-code instrumentation still offers flexibility. Typical mechanisms include:

* Environment variables (most common)
* System properties (common for Java/.NET)
* Startup arguments (runtime customization)

Using these you can set service metadata, exporters, propagators, resource attributes, sampling, and other runtime behaviors. Example configuration options you might set via environment variables:

* Service name (so traces are grouped under a logical service in your observability backend)
* Exporter (OTLP, console, etc.)
* Propagators (W3C trace-context, B3)
* Resource attributes (environment, region, team, etc.)

Example environment variable snippets:

```bash theme={null}
