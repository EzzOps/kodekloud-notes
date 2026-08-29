# Expected stdout:
# processing payment
# validating card
# charging bank
```

After running, open the Jaeger UI (usually at `http://localhost:16686`) and search for traces. In this example the traces appear, but the service is shown as `unknown_service` — we’ll fix the service/resource name in the next step.

<Frame>
  <img alt="The image shows the Jaeger UI with search parameters for tracing a service labeled &#x22;unknown_service&#x22; and displaying one trace related to a payment service." />
</Frame>

The trace shown includes spans for the payment flow (start payment, validating card, charge bank), confirming that OTLP export to Jaeger is working. In the following lesson we’ll configure the Resource (service name and attributes) so traces display with a meaningful service name in Jaeger.

## References

* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* OpenTelemetry OTLP spec: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/e2504512-2808-4370-b7a0-213355af4632" />
</CardGroup>


# Demo Instrumenting API

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Instrumenting-API/page

Demonstrates instrumenting a payment client and Flask charge API with OpenTelemetry to create, enrich, and export spans via OTLP for tracing and observability

In this lesson we continue the sample payment application and demonstrate how to instrument both the client-side payment flow and the external charge API using OpenTelemetry. You will learn how spans are created on the client, how to add useful attributes, and how to instrument a Flask service to export server spans to an OTLP endpoint.

Overview

* Client: A small script (`payment.py`) that creates spans and attributes for a payment flow.
* Server: A minimal Flask app (`charge.py`) that receives a /charge request. We'll first show the uninstrumented service, then the instrumented version that exports traces via OTLP.
* Goal: Have both client and server produce spans that are searchable in a tracing backend (Jaeger, Tempo, or any OpenTelemetry-compatible backend).

Client-side instrumentation (payment.py)
This client simulates a payment flow and creates spans plus attributes before calling the downstream charge service.

```python theme={null}
