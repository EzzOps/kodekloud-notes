# OpenTelemetry API

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-API/page

Overview of the OpenTelemetry API, a language agnostic contract for generating traces metrics and logs, contrasts with SDK, and offers instrumentation best practices and examples

Hello, OTel architecture experts.

In this lesson/article we'll take a focused look at the OpenTelemetry API: what it is, how it differs from the SDK, and best practices for instrumenting applications and libraries. This article preserves the original diagrams and their order so you can follow the architecture visually as you read.

Why a language-agnostic telemetry API?

Modern systems are polyglot: Java, Go, Python, PHP, Ruby, Swift, JavaScript and more all produce telemetry. Language-specific approaches (for example, print statements or ad-hoc logging) are not portable across ecosystems. OpenTelemetry provides a vendor-neutral, cross-language standard API so you can generate traces, metrics, and logs without coupling instrumentation to a particular backend or SDK.

<Frame>
  <img alt="The image illustrates how OpenTelemetry acts as a cross-language bridge, supporting multiple programming languages like C++, Python, and JavaScript, and connecting them to a standard telemetry API." />
</Frame>

What is the OpenTelemetry API?

The OpenTelemetry API is the language-agnostic specification for generating telemetry data—traces, metrics, and logs. It defines the interfaces and data types (the contract) that application code and libraries call. Each supported language exposes an idiomatic API that implements that contract.

<Frame>
  <img alt="The image explains the OpenTelemetry API as a vendor-neutral tool for handling traces, metrics, and logs, with standardized specifications for language-specific APIs." />
</Frame>

Specification vs implementation

The OpenTelemetry specification describes the data model and operations for telemetry and can evolve to include additional signals (such as profiling). Language-specific APIs and SDKs implement the spec; find the current status and releases in the project documentation.

<Frame>
  <img alt="The image shows a section of the OpenTelemetry documentation focusing on &#x22;Status and Releases&#x22; with a table listing various programming languages and their component statuses. The sidebar features a menu with links to related documentation sections." />
</Frame>

Quick Python example (install + basic tracer provider)

To try OpenTelemetry in Python, install the API and SDK packages, configure a tracer provider, and add a span processor/exporter:

```bash theme={null}
pip install opentelemetry-api
pip install opentelemetry-sdk
```

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
