# Windowing in Dataflow

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Windowing-in-Dataflow/page

Explains windowing in Google Cloud Dataflow, covering fixed sliding session and global windows, watermarks triggers allowed lateness and Apache Beam examples for streaming aggregation.

Hello and welcome back.

In this lesson we explore one of the most important topics for streaming data in Google Cloud Dataflow: windowing.

Why windowing matters

* Streaming data is unbounded: events may arrive continuously and out of order. Windowing gives us a way to group events into finite, time-based segments so we can compute aggregates, metrics, and other results.
* Windowing is normally used with event time (when the event actually occurred), watermarks (estimates of event-time progress), and triggers (when to emit results). Together these let you compute correct, timely results from late or out-of-order events.

This lesson builds on data transformations and how they appear in a Dataflow pipeline. Windowing answers a different question: how do we group and process an unbounded, continuous stream of events? Do we process every single event as it arrives, or aggregate events into time-based chunks and process them periodically? Windowing provides the mechanisms to group streaming data into manageable time windows so we can compute near-real-time results.

Below are the main windowing strategies you will use in Google Cloud Dataflow.

Fixed windows

* Fixed windows divide the event stream into equal-length, non-overlapping intervals. Each event belongs to exactly one fixed window.
* Example use case: hourly counts of cars passing a toll booth. When the hour ends, the window is closed and the next window begins.

<Frame>
  <img alt="An infographic titled &#x22;Grouping Streaming Data by Time&#x22; showing a continuous stream of events across a timeline and a diagram of fixed, non-overlapping time windows (Window 01–04) at 0s, 5s, 10s, 15s, and 20s. It notes use cases like hourly analytics and daily reports." />
</Frame>

Sliding windows

* Sliding windows have a fixed duration (window length) but advance by a smaller step (the slide). Windows therefore overlap and an event can belong to multiple windows.
* Example use case: a 10-second moving average updated every 2 seconds. This provides more frequent insight while considering a longer interval.

<Frame>
  <img alt="A presentation slide titled &#x22;Grouping Streaming Data by Time&#x22; showing a continuous stream of data points along a timeline and an illustration of overlapping sliding windows (Window-01 to Window-04) used for moving averages and trend analysis. The slide labels the windows as 2s side intervals and notes unbounded data events over time." />
</Frame>

Session windows

* Session windows are dynamic: they group events based on activity, not fixed time boundaries. A session continues while events keep arriving within a defined inactivity gap; when the gap is exceeded, the session closes and a new one begins.
* Example use case: web browsing sessions. If a user is continuously active, events remain in the same session; after an inactivity gap (for example, 30 seconds), the next activity starts a new session.

<Frame>
  <img alt="A diagram titled &#x22;Grouping Streaming Data by Time&#x22; showing a continuous timeline of data points and an example of session windows (Session 01–04) separated by activity gaps. It illustrates dynamic session-based windows for grouping unbounded streaming events, with a use case of user sessions/activity bursts." />
</Frame>

Global window

* The global window places all data into a single, long-lived window that spans the entire pipeline execution.
* In batch (bounded) pipelines this effectively groups the full dataset and processes it to completion.
* In streaming, a global window groups all events indefinitely, so you must use triggers (with watermarks and allowed lateness) to decide when to emit intermediate and final results because the input never naturally completes.

Quick summary

* Fixed windows: equal, non-overlapping time ranges.
* Sliding windows: overlapping time ranges for more frequent updates.
* Session windows: dynamic windows based on activity gaps.
* Global window: all data in one bucket (common for batch; requires triggers for streaming).

Windowing strategies at a glance

| Window Type      | Key characteristics                                           | Typical use cases                                   |
| ---------------- | ------------------------------------------------------------- | --------------------------------------------------- |
| Fixed (tumbling) | Equal-length, non-overlapping windows                         | Hourly/daily aggregates, time-bucketed metrics      |
| Sliding          | Fixed length, overlapping (advance/slide smaller than length) | Moving averages, frequent trend updates             |
| Session          | Dynamic length defined by inactivity gap                      | User sessions, bursty activity grouping             |
| Global           | Single window for entire pipeline                             | Batch aggregation; streaming with explicit triggers |

Example: Apache Beam windowing snippets

* These examples show how to apply common windows in Apache Beam (the SDK Dataflow uses). Replace `PCollection` and transforms with your pipeline’s elements.

Fixed window (Python):

```python theme={null}
from apache_beam.transforms.window import FixedWindows
pcoll | "FixedWindow" >> beam.WindowInto(FixedWindows(60))  # 60-second windows
```

Sliding window (Python):

```python theme={null}
from apache_beam.transforms.window import SlidingWindows
pcoll | "SlidingWindow" >> beam.WindowInto(SlidingWindows(size=10, period=2))  # 10s window, every 2s
```

Session window (Python):

```python theme={null}
from apache_beam.transforms.window import Sessions
pcoll | "SessionWindow" >> beam.WindowInto(Sessions(gap_size=30))  # session gap = 30s
```

When to emit results: watermarks, triggers, and lateness

* Windowing groups events, but emission (when results are output) is controlled by triggers and coordinated with watermarks that estimate event-time progress.
* Common trigger choices:
  * On watermark (default): emit when the watermark passes the end-of-window.
  * Processing-time timers: emit periodically based on wall-clock time.
  * Repeated/accumulating triggers for early/late firings.
* Always consider allowed lateness to accept late events into already-closed windows or to drop them.

> **warning** Global windows don’t close on their own in streaming mode. If you choose a global window for a streaming pipeline, explicitly configure triggers and allowed lateness; otherwise intermediate or final results will not be emitted as expected.

Grouping by time is necessary but not sufficient: you also need to decide when to emit results to external sinks (for example, `BigQuery` or `Cloud Storage`). Emission is controlled by watermarks and triggers, which govern lateness handling and output timing. Watermarks and triggers are covered in a separate lesson.

> **lightbulb** Windowing operates in the context of event time (the time an event occurred) and is coordinated with watermarks that indicate how far event time has progressed. Triggers control when the pipeline emits results for a window (on watermark progress, on processing-time timers, or on other conditions).

Links and references

* [Apache Beam Windowing Concepts](https://beam.apache.org/documentation/programming-guide/#windowing)
* [Dataflow Streaming Engine and Windowing](https://cloud.google.com/dataflow/docs/guides/windowing)
* [BigQuery documentation](https://cloud.google.com/bigquery)
* [Cloud Storage documentation](https://cloud.google.com/storage)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/df0edb08-86a3-4ed7-9c13-914853f9f655)
