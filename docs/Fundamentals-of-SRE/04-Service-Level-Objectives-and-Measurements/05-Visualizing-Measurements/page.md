# Visualizing Measurements

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Service-Level-Objectives-and-Measurements/Visualizing-Measurements/page

Guidelines for designing SLO dashboards that surface user-facing SLIs, error budgets, visual hierarchy, color coding, and actionable context to drive reliability and incident response

Defining SLIs and SLOs is only the first step — making them visible and actionable is what drives reliable systems. This article shows where reliability data belongs, how to surface the right signals, and how to design dashboards that prompt the right action across teams.

Well-designed SLO dashboards make reliability data accessible and useful beyond SREs. They turn raw metrics into a reliability story: what’s healthy, what’s risky, and what needs immediate attention.

## Focus on user experience

Prioritize user-facing SLIs. These are the signals that most directly reflect customer experience and business risk.

* Place user-facing SLIs front and center (e.g., checkout success rate, page load P95).
* Show SLI compliance status prominently (Are targets being met?).
* Surface user journey success rates so product and business stakeholders can see health at a glance.

<Frame>
  <img alt="A presentation slide titled &#x22;Designing an Effective SLO Dashboard&#x22; with the heading &#x22;01 — Focus on User Experience First&#x22; and a colorful illustration of a laptop, user avatar, stars, and gears. To the right are bullet points listing key components like user-facing SLI panels, visual SLO compliance indicators, and user journey success rates." />
</Frame>

## Visual hierarchy — guide attention, reduce noise

A clear visual hierarchy helps teams triage quickly.

Recommended layout (top → bottom):

* Highest priority: overall service-health panel (e.g., 99.95%).
* Immediately below: three critical SLOs side-by-side (availability, latency, error budget).
* Under those: short-term trend graphs (7-day or 30-day) to show emerging patterns.
* Bottom: component-level and dependency panels for troubleshooting.

Put the most critical SLOs in the largest panels and show current status (green/yellow/red) next to them. This lets anyone — engineers, product managers, executives — assess health quickly and then drill down as needed.

<Frame>
  <img alt="A slide titled &#x22;Designing an Effective SLO Dashboard&#x22; showing an illustration of a person pointing at a flowchart on a large screen. On the right is an example dashboard layout with overall service health, availability, latency, error budget, 7-day trends, and component health." />
</Frame>

## Color coding — consistent and actionable

Use a consistent color system so stakeholders immediately recognize risk levels.

| Color  | Meaning                                  | Action                                        |
| ------ | ---------------------------------------- | --------------------------------------------- |
| Green  | Comfortably meeting SLO                  | No action required; monitor                   |
| Yellow | Within SLO but trending toward threshold | Investigate, prepare mitigations              |
| Red    | SLO violated                             | Immediate action required (incident response) |

Simple, consistent color cues make dashboards readable at a glance for both technical and non-technical audiences.

<Frame>
  <img alt="A presentation slide titled &#x22;Designing an Effective SLO Dashboard&#x22; advising to &#x22;Use Color Strategically.&#x22; It shows color-coding with three triangular icons: green = comfortably meeting SLO, yellow = within SLO but trending toward threshold, and red = SLO violation." />
</Frame>

## Error budget visualizations — make abstract risk tangible

Error budgets convert SLOs into operational constraints. Show these elements so teams can reason about risk and throttle releases when needed:

* Total error budget for the measurement period (e.g., monthly).
* Percentage of budget consumed to date.
* Current burn rate (speed of budget consumption).
* Projected depletion date if the current burn rate continues.

These panels help answer: Are we safe to deploy? Do we need to pause releases? Is the system degradation transient or sustained?

<Frame>
  <img alt="A presentation slide titled &#x22;Designing an Effective SLO Dashboard&#x22; about including error budget visualizations, with bullet points listing key components like total error budget, consumption percentage, burn rate, and projected depletion date. The left side has an illustration of a person, error messages, a large red &#x22;ERROR&#x22; label and a warning icon." />
</Frame>

## Provide context — labels, windows, and links

Context makes dashboards actionable. Always include:

* Clear SLI targets (e.g., "P95 latency ≤ 300 ms").
* The measurement time window (e.g., 5m, 1h, 7d, 30d).
* Links to incident runbooks and ownership information.
* Quick drill-down paths from a high-level alert into metrics, traces, and logs.

> **lightbulb** Always label SLI targets and the time window for measurement — ambiguity is the enemy of action.

Make it easy to move from “something is wrong” to “here’s why” by providing supporting metrics and direct links to the right runbooks and dashboards.

<Frame>
  <img alt="A slide titled &#x22;Designing an Effective SLO Dashboard&#x22; showing a dark-themed SLO dashboard with gauge widgets for availability (100%), order latency P95, and error budget consumption (0% availability, 100% order processing). The panel list on the dashboard includes sections like 7-day trends, latency SLO, component health, and error budget policies." />
</Frame>

## Concrete example: latency SLI using Prometheus histograms

Example SLI: "95% of orders complete processing within 3 seconds" — i.e., the fraction of requests with latency ≤ 3s.

If your system exposes Prometheus histogram metrics following the common pattern (http\_request\_duration\_seconds\_bucket and http\_request\_duration\_seconds\_count), the following PromQL computes the percentage over a 5‑minute window:

```promql theme={null}
(
  sum(rate(http_request_duration_seconds_bucket{endpoint="/orders", le="3"}[5m]))
  /
  sum(rate(http_request_duration_seconds_count{endpoint="/orders"}[5m]))
) * 100
```

* This returns the percentage of /orders requests with latency ≤ 3s over the last 5 minutes.
* Add this expression as a dedicated panel next to availability and error-budget widgets so the team can detect latency regressions and their impact on error budgets.

## Dashboard checklist

Use this quick checklist when designing or reviewing SLO dashboards:

* Are user-facing SLIs prominently visible?
* Is the visual hierarchy clear (service health → critical SLOs → trends → components)?
* Are SLI targets and time windows labeled?
* Is color usage consistent and understood by stakeholders?
* Are error budget panels present with burn rate and projected depletion?
* Are links to runbooks, owners, and logs available for fast action?

## Wrapping up

Dashboards, error budgets, and well-chosen SLOs form the backbone of modern reliability engineering. Their value is realized when they drive appropriate action: stop risky releases, prioritize fixes, and enable continuous improvement. Real-world systems are messy — use these visualization principles to reduce risk, eliminate toil, and keep teams aligned on what matters.

## Links and references

* [Prometheus histograms and best practices](https://prometheus.io/docs/practices/histograms/)
* [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* [SRE and SLO fundamentals — further reading](https://sre.google/sre-book/table-of-contents/)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/3d28bb2c-48a0-4bb6-a79a-3b0094692e98)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/250ab753-8091-4b0c-a79c-826cc4b1684b)
