# Span Timings

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Timings/page

Explains span start and end timestamps, duration, and events in distributed tracing using OpenTelemetry and importance of precise timing for latency analysis.

Span timings are the core building block of distributed traces. They record when an operation began (start time), when it finished (end time), and the elapsed time between those points (duration). These values let you analyze latency, order operations, and detect bottlenecks across services.

* Start time: the instant the operation began (e.g., just before sending a request).
* End time: the instant the operation finished (e.g., after receiving an HTTP response).
* Duration: `end_time - start_time` — the elapsed time or latency for the operation.

Below is a representative OpenTelemetry span showing start and end timestamps (microsecond precision in this example) along with several in-span events:

```json theme={null}
{
  "name": "main_function_span",
  "context": {
    "trace_id": "0x6d6a406a5d5d4cb37f8e117ac8069a52",
    "span_id": "0x3f73ff9e0d455ea",
    "trace_state": []
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": null,
  "start_time": "2025-10-17T12:57:33.567131Z",
  "end_time": "2025-10-17T12:57:53.210426Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {},
  "events": [
    {
      "name": "Starting main function execution",
      "timestamp": "2025-10-17T12:57:33.567131Z",
      "attributes": {}
    },
    {
      "name": "SLOW API call completed",
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

OpenTelemetry SDKs commonly support nanosecond precision; the exact timestamp representation varies by language and export format. The timestamps above use ISO 8601 with a `Z` suffix (UTC). Depending on SDK/export, timestamps may be encoded as RFC 3339/ISO 8601 strings or as epoch-based numeric fields (for example, `time_unix_nano` in OTLP protobuf).

Here are the start and end fields shown again for clarity:

```json theme={null}
{
  "start_time": "2025-10-17T12:57:33.567131Z",
  "end_time": "2025-10-17T12:57:53.210426Z"
}
```

A compact summary:

| Field      | Definition                             | Example                       |
| ---------- | -------------------------------------- | ----------------------------- |
| Start time | When the span operation began          | `2025-10-17T12:57:33.567131Z` |
| End time   | When the span operation completed      | `2025-10-17T12:57:53.210426Z` |
| Duration   | `end_time - start_time` (elapsed time) | `19.643295 s`                 |

From the example timestamps we calculate:

* start: `2025-10-17T12:57:33.567131Z`
* end:   `2025-10-17T12:57:53.210426Z`
* duration: 19.643295 seconds (≈ 19.64 s)

Note that many backends and processing layers compute duration from the start and end timestamps rather than storing it as a separate span attribute in the payload.

> **lightbulb** Timestamps can be exported as RFC 3339/ISO 8601 strings or as epoch numeric fields (for example, `time_unix_nano` in OTLP protobuf). SDKs often provide microsecond or nanosecond precision, and observability backends derive duration from the recorded start and end times.

Span events: pinpointing moments inside a span

* Span timings describe the overall operation window. Inside that window, span events capture notable instants — for example:
  * cache miss or cache hit
  * start of a retry
  * receiving an external API response
  * recording an exception or stack trace
* In the JSON example above, three events are timestamped within the span. These events provide context that helps explain why the span took a given amount of time when you correlate them with logs, metrics, or traces.

Why accurate timings matter

* Timings drive the trace timeline and waterfall visualizations used in APM/observability UIs.
* Precise timestamps enable:
  * latency breakdowns (client → server → DB)
  * detection of ordering issues or clock skew
  * performance comparisons across releases and environments

References

* [OpenTelemetry](https://opentelemetry.io/)
* [RFC 3339 / ISO 8601 timestamps](https://www.rfc-editor.org/rfc/rfc3339.html)
* OTLP protobuf: `time_unix_nano` (see OpenTelemetry proto repository)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/8a71c7c7-1de0-424d-b7c5-51f7adbdb682)
