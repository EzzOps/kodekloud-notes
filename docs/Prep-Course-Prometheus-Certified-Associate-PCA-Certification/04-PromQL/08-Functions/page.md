# Functions

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/Functions/page

Overview of PromQL functions with examples and practical tips covering math, time, conversions, sorting, presence checks, and counter rate calculations such as rate and irate.

PromQL includes many built-in functions for common needs: numeric transformations, time/date extraction, label and metric manipulation, sorting, presence checking, and computing rates for counters. Below we walk through important categories with concise examples and practical tips for queries and alerts.

<Frame>
  <img alt="The image contains a text description of PromQL functions, highlighting features like sorting, math, label transformation, and metric manipulation, with colorful highlights on certain words." />
</Frame>

Below we cover math-based functions, date/time helpers, scalar/vector conversions, sorting, presence checks, and counter-rate calculations.

## Quick reference: common function categories

|        Category | Purpose                                                       | Examples                                   |
| --------------: | ------------------------------------------------------------- | ------------------------------------------ |
|  Math & numeric | Basic numeric transformations                                 | `ceil(v)`, `floor(v)`, `abs(v)`            |
|       Time/date | Extract components of evaluation time                         | `time()`, `minute()`, `hour()`             |
|     Conversions | Convert between scalar and instant vector                     | `scalar(v)`, `vector(s)`                   |
|         Sorting | Sort instant vectors by value                                 | `sort(v)`, `sort_desc(v)`                  |
| Presence checks | Detect missing or present series                              | `absent(v)`, `present_over_time(v[range])` |
|   Counter rates | Convert monotonically increasing counters to per-second rates | `rate(v[range])`, `irate(v[range])`        |

## Math-based functions

These functions operate on each sample value in an instant vector.

| Function   | Behavior                                        |
| ---------- | ----------------------------------------------- |
| `ceil(v)`  | Round each sample up to the next integer.       |
| `floor(v)` | Round each sample down to the previous integer. |
| `abs(v)`   | Convert each sample to its absolute value.      |

Example (instant vector values and results shown inline):

```bash theme={null}
