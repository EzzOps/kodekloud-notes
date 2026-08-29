# Demo Status Codes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Status-Codes/page

Explains how to set OpenTelemetry span status to OK or ERROR for HTTP calls, record attributes like http.status_code, propagate context, and handle exceptions for accurate tracing.

This lesson explains how to set the status code on OpenTelemetry spans to reflect success or failure of operations (for example, outgoing HTTP calls). By default OpenTelemetry leaves a span's status as `UNSET` until your application or instrumentation sets it explicitly. When an application crash occurs, instrumentation often marks the span as `ERROR` automatically. For normal request flows you should explicitly set status to `OK` for success and `ERROR` for handled failures.

<Callout icon="lightbulb">
  Spans default to `UNSET`. To represent success or failure in traces, explicitly set the span status to `OK` or `ERROR` and record relevant attributes like `http.status_code`.
</Callout>

Below is an example trace timeline from Jaeger showing a payment service with a failed request span (image preserved from original content):

<Frame>
  <img alt="The image shows a trace timeline from the Jaeger UI, detailing operations of a payment service. It includes spans for validating a card and a failed request to the charge API with an error message related to a connection issue." />
</Frame>

Why set span status?

* Communicates high-level outcome of an operation to downstream analysis tools.
* Helps filtering and alerting in tracing backends (errors vs. successful traces).
* Augments other attributes (like `http.status_code`) for richer context.

Recommended steps for an outgoing HTTP call

1. Add semantic attributes to the span: HTTP method, URL.
2. Propagate context (inject headers) before making the request.
3. Record events for request lifecycle (sending, sent, received).
4. Set `http.status_code` as a span attribute using the HTTP response.
5. Explicitly set span status to `OK` or `ERROR` depending on the outcome.

Example: minimal, corrected Python instrumentation and status handling

* First, configure tracing (tracer provider, resource, and exporter):

```python theme={null}
