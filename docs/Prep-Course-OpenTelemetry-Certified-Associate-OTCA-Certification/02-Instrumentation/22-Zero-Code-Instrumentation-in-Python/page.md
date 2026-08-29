# resulting JAR: build/libs/your-extension.jar
```

Load it when starting the JVM using the `otel.javaagent.extensions` system property:

```bash theme={null}
java -javaagent:path/to/opentelemetry-javaagent.jar \
  -Dotel.javaagent.extensions=path/to/extension.jar \
  -jar myapp.jar
```

This causes the agent to load and apply your extension alongside default instrumentation.

Real-world extension examples

* Disable spans to reduce noise and storage usage
* Normalize attribute names across services
* Mask or remove PII before exporting spans
* Add support for an in-house library that the agent does not yet instrument

<Frame>
  <img alt="The image lists five practical extension use cases: disabling unnecessary spans, editing attributes, editing attributes based on database connection, removing certain attributes, and redesigning span behavior. Each use case is visually represented with icons." />
</Frame>

> **warning** Do not confuse Java agent extensions with OpenTelemetry Collector extensions — they are different concepts in different components. Collector extensions apply to the Collector pipeline, while Java agent extensions modify agent behavior inside the JVM.

Terminology and best practices

* Automatic instrumentation is ideal for broad coverage with minimal effort.
* Use manual instrumentation (OpenTelemetry API) for business-specific spans and fine-grained telemetry.
* Prefer environment variables in containerized environments for easier integration with orchestration and secrets.
* Keep an eye on sampling and cardinality limits to control backend costs and performance.

Wrapping up
The OpenTelemetry Java agent enables production-ready, zero-code observability through bytecode instrumentation. It provides immediate visibility into common frameworks and libraries, is highly configurable via environment variables or JVM properties, and can be extended with custom agent extensions when necessary. For functionality not covered automatically, use manual instrumentation with the OpenTelemetry API.

<Frame>
  <img alt="The image is a summary slide highlighting three features: Java Agent for zero-code observability, a powerful and ready-to-use tool, and its high configurability without needing source code modification." />
</Frame>

Links and references

* OpenTelemetry Java instrumentation repository: [https://github.com/open-telemetry/opentelemetry-java-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
* OpenTelemetry Java instrumentation releases: [https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases)
* Agent documentation and configuration: [https://opentelemetry.io/docs/instrumentation/java/](https://opentelemetry.io/docs/instrumentation/java/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/a2a1b13b-ea70-4348-932c-c888b08dfdee)


# Zero Code Instrumentation in Python

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Zero-Code-Instrumentation-in-Python/page

Explains OpenTelemetry Python zero-code auto-instrumentation using monkey patching to capture traces and metrics for common libraries, plus installation, configuration, and debugging steps.

Zero-code (or auto-) instrumentation lets you add observability to Python applications without modifying source code. In Python this is achieved primarily via monkey patching: at runtime, the agent replaces or wraps existing functions and methods in popular libraries so that traces and metrics are collected automatically. While other languages (like Java) commonly use bytecode manipulation, Python’s runtime patching delivers the same outcome by altering call behavior as the program runs.

<Frame>
  <img alt="The image explains monkey patching basics for instrumentation, highlighting two points: modifying existing methods at runtime and injecting logic into libraries without altering their source code." />
</Frame>

OpenTelemetry for Python provides auto-instrumentation for many widely used libraries and frameworks (Flask, Django, Requests, SQLAlchemy, Redis, etc.), making it simple to gain observability with zero code changes. See the official docs: [OpenTelemetry for Python](https://opentelemetry.io/docs/instrumentation/python/).

How zero-code instrumentation works (high level)

1. The OpenTelemetry agent applies monkey patches to supported libraries at runtime.
2. Patches wrap or modify library functions so requests, DB queries, and messaging calls generate spans and metrics automatically.
3. If your app uses supported libraries, traces and metrics appear with no manual SDK calls.

<Frame>
  <img alt="The image explains how zero-code instrumentation operates in Python, highlighting four points: using monkey patching, modifying library functions at runtime, supporting various libraries, and eliminating the need for manual instrumentation." />
</Frame>

## Installation

Install the OpenTelemetry distro and supporting packages, then let the bootstrap tool detect and install instrumentations for the dependencies in your environment.

```bash theme={null}
pip install opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-instrumentation opentelemetry-bootstrap
opentelemetry-bootstrap -a install
```

The bootstrap step scans installed packages and adds relevant instrumentation libraries. After this, you can run the OpenTelemetry Python agent.

## Running the agent

Start your app with the `opentelemetry-instrument` wrapper to enable auto-instrumentation. Example that exports traces and metrics to the console (for development) and to an OTLP endpoint (typical for sending to an OTel Collector):

```bash theme={null}
opentelemetry-instrument \
  --traces_exporter console,otlp \
  --metrics_exporter console \
  --service_name your-service-name \
  --exporter_otlp_endpoint 0.0.0.0:4317 \
  python myapp.py
```

> **lightbulb** For production, send telemetry to an OTLP Collector or backend instead of the console. Use the console exporter only for quick testing or troubleshooting.

## Configuration via environment variables

Environment variables are commonly used in containers and CI/CD pipelines. They provide the same control as CLI flags and are typically easier to manage in deployments.

Example environment variables:

```bash theme={null}
export OTEL_SERVICE_NAME=your-service-name
export OTEL_TRACES_EXPORTER=console,otlp
export OTEL_METRICS_EXPORTER=console
export OTEL_EXPORTER_OTLP_ENDPOINT=0.0.0.0:4317
```

Then start the instrumented process:

```bash theme={null}
opentelemetry-instrument python myapp.py
```

Python-specific configuration examples

```bash theme={null}
