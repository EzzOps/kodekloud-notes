# OpenTelemetry Client Design Principles

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-Client-Design-Principles/page

Explains OpenTelemetry client design principles, API versus SDK separation, modular signal packages, exporters, and how clients integrate into observability architectures and distributions

A concise guide for developers and architects explaining why OpenTelemetry (OTel) clients are structured the way they are. This article focuses on the design intent behind language-specific OTel libraries (the "client" you install in your application), how the API/SDK separation works, and how clients fit into an observability ecosystem.

## What we mean by "client"

When we say "client" we mean the language-specific OpenTelemetry library embedded in your application (for example, the Python, Java, or JavaScript OTel packages). The client is responsible for enabling your code to generate telemetry (traces, metrics, logs) and typically exposes a stable API while delegating runtime behavior to a pluggable SDK.

Quick example (Python):

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
