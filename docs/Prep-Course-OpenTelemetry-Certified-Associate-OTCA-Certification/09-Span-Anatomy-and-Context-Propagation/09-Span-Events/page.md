# Add a point-in-time event when the virus is detected
span.add_event("virus_detected")

# Attach descriptive metadata about the file to the span
span.set_attribute("file.type", "pdf")
span.set_attribute("file.size_kb", 328)
```

Note that even if a virus is not detected, you still usually want to record file details on the span; those belong as attributes because they describe the span regardless of whether the event occurred.

> **lightbulb** Use span events for time-specific occurrences and span attributes for persistent metadata describing the span.

Key distinctions and guidance

* Timestamps
  * Span events include timestamps — they represent something that happened at a particular instant.
  * Span attributes do not carry separate timestamps; the span’s start/end times provide the temporal context.
* Use cases for span events
  * Exceptions, errors, retries, milestones, logs — anything you want to mark at a specific moment.
  * Events can include their own attributes (for example, `error.type`, `message`).
* Use cases for span attributes
  * Persistent metadata and context for the entire span — e.g., `db.system`, `http.method`, `http.response.status_code`, `user.id`, `payment.method`, `file.type`, `file.size_kb`.
* Durations
  * If you need to represent an interval, rely on span start/end timestamps or a nested child span. Span events are single instants and cannot represent durations by themselves.
* Exceptions
  * Exceptions are typically captured as events (many telemetry SDKs provide `record_exception` or an equivalent that generates an event).

Comparison table

| Concept           | Use When                                             | Example attributes / events                                  |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Span event        | You need a timestamped occurrence inside the span    | `span.add_event("error", {"type":"TimeoutError"})`           |
| Span attribute    | You need persistent contextual metadata for the span | `span.set_attribute("http.method", "GET")`                   |
| Interval/duration | You need to express a time range                     | Use span start/end or create a child span                    |
| Error reporting   | Capture the exact time of the error                  | `record_exception()` or `span.add_event("exception", {...})` |

Summary

* Use span events for time-specific actions, errors, or logs that matter at a precise instant.
* Use span attributes for contextual, persistent details about a span that apply for its whole duration.

References and further reading

* [OpenTelemetry Tracing Concepts](https://opentelemetry.io/docs/concepts/signals/traces/)
* [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/)

This concludes the explanation of span events vs span attributes.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/af5a1bca-aa16-4e9b-87af-3ed6ba4a969d)


# Span Events

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Events/page

Explains span events as timestamped annotations inside spans that record exceptions, milestones, and contextual attributes to aid debugging, correlation, and latency analysis.

Span events let you record discrete, timestamped moments inside a span. They enrich a trace with point-in-time annotations that go beyond the span's start and end timestamps, making it easier to debug, correlate errors, and understand latency.

A span event is a timestamped annotation — a point-in-time marker inside a span that highlights when something specific occurred.

<Frame>
  <img alt="The image explains a &#x22;Span Event&#x22; as a timestamped annotation within a span marking a specific point in time, with an illustration of a person and clocks." />
</Frame>

What makes a span event unique:

* Each event belongs to a span; it cannot exist independently.
* An event has a single timestamp (there is no start/end time).
* Events can carry structured attributes to provide contextual detail.

<Frame>
  <img alt="The image lists the key characteristics of Span Events, which include belonging to a span, having a timestamp without a start or end time, and the ability to include attributes (structured data)." />
</Frame>

Quick reference: Characteristics and common attributes

| Characteristic        |                                     Why it matters | Typical attributes                                     |
| --------------------- | -------------------------------------------------: | ------------------------------------------------------ |
| Belongs to a span     | Keeps events tied to trace context for correlation | `trace_id`, `span_id`                                  |
| Single timestamp      |                   Pinpoints when an event occurred | `timestamp`                                            |
| Structured attributes |          Attach context (errors, counts, metadata) | `exception.type`, `exception.message`, `result_length` |

Common uses are capturing milestones such as a DB query completion, an external API response, or an exception. When recording an exception, include attributes like `exception.type`, `exception.message`, and `exception.stacktrace`. Example JSON event:

```json theme={null}
{
  "events": [
    {
      "name": "exception",
      "timestamp": "2025-05-01T12:58:08.969805Z",
      "attributes": {
        "exception.type": "HTTPError",
        "exception.message": "404 Not Found",
        "exception.stacktrace": "raise_for_status() -> HTTPError",
        "exception.escaped": false
      }
    }
  ]
}
```

> **lightbulb** [OpenTelemetry](https://opentelemetry.io/docs/specs/otel/semantic_conventions/exceptions/) recommends recording exceptions as span events so they remain connected to the trace context and are timestamped for easier debugging.

Recording exceptions as span events keeps the error context within the trace itself, simplifying root-cause analysis and making it easier to see exactly when and where a problem happened.

<Frame>
  <img alt="The image explains why exceptions become span events, highlighting that exceptions are meaningful, timestamped moments and often include structured data." />
</Frame>

One major advantage: span events bring log-level detail into traces. This reduces the need to cross-reference separate logging systems when investigating an issue.

<Frame>
  <img alt="The image shows a person examining data on a large screen with graphs and charts, accompanied by the text &#x22;Span Events Add Log-Level Detail&#x22; and a magnifying glass icon." />
</Frame>

This approach streamlines troubleshooting: inspect a trace and view the exact message and attributes recorded at the moment the event occurred.

<Frame>
  <img alt="The image is about &#x22;Tracking with Span Events,&#x22; indicating that one can track errors, retries, or checkpoints without maintaining separate logs. It includes icons and labels for errors, retries, and checkpoints." />
</Frame>

Span events are especially useful for debugging and for identifying contributors to latency in a request’s journey.

<Frame>
  <img alt="The image is a slide titled &#x22;Debugging with Span Events&#x22; with a highlighted point stating it is &#x22;Great for debugging and understanding latency contributors&#x22; and includes icons for debugging and understanding latency contributors." />
</Frame>

Common span-event use cases:

* Capturing a stack trace or exception details when an error occurs.
* Marking retries or backoff events inside a span.
* Annotating application-specific checkpoints (e.g., parsing completed, cache miss).
* Recording important external call completions or timeouts.

<Frame>
  <img alt="The image lists common use cases for span events, including capturing exception stack traces, marking retries in a span lifecycle, and annotating application-specific actions." />
</Frame>

A single span can contain multiple events, each representing a distinct point-in-time action. Example of a span with several events:

```json theme={null}
{
  "name": "main_function_span",
  "context": {
    "trace_id": "0x6d4a0605d5d4cb37f8e117ac0069a52",
    "span_id": "0x3f73ffe9da555ea",
    "trace_state": []
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": null,
  "start_time": "2025-10-17T12:57:33.567313Z",
  "end_time": "2025-10-17T12:57:53.210426Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {},
  "events": [
    {
      "name": "Starting main function execution",
      "timestamp": "2025-10-17T12:57:33.567313Z",
      "attributes": {}
    },
    {
      "name": "Slow API call completed",
      "timestamp": "2025-10-17T12:57:53.210337Z",
      "attributes": {
        "result_length": 359
      }
    },
    {
      "name": "Main function execution complete",
      "timestamp": "2025-10-17T12:57:53.210410Z",
      "attributes": {}
    }
  ]
}
```

Each event maintains its own timestamp and attributes, letting you inspect the precise sequence of actions that took place during the span’s lifetime.

Exceptions are commonly reported automatically by tracing instrumentation as span events. To add custom events manually, call the span object's `add_event` (or equivalent) API in your SDK. Example in Python:

```python theme={null}
span.add_event(
    "Slow API call completed",
    attributes={"result_length": len(result)}
)
```

After adding the event, it will appear in the span’s trace data and show up in your tracing UI alongside other events for that span.

Links and references

* [OpenTelemetry: Exceptions semantic conventions](https://opentelemetry.io/docs/specs/otel/semantic_conventions/exceptions/)
* [OpenTelemetry: Tracing overview](https://opentelemetry.io/docs/specs/otel/overview/)
* [OpenTelemetry SDKs and APIs](https://opentelemetry.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/81cdac8a-ce21-43b3-a994-a7cda8cb9c8c)
