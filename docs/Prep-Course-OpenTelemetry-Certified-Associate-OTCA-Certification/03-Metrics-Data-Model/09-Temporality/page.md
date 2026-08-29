# Temporality

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Temporality/page

Explains metric temporality, contrasting cumulative versus delta measurements and their implications for aggregation, storage, resets, backend compatibility, and accurate alerting in observability systems.

Temporality describes how a metric's reported value relates to time — whether it represents a running total since some origin (cumulative) or the observed change over an interval (delta). Correctly understanding and choosing temporality is essential for accurate aggregation, alerting, and storage in observability systems like OpenTelemetry.

<Frame>
  <img alt="The image explains temporality in metrics, defining it as how a value relates to time, either as a cumulative total or a change over an interval." />
</Frame>

Put simply:

* Cumulative — a monotonically increasing value (a running total) from a start point. Each reported point is the total so far.
* Delta — the change observed during a specific reporting interval (current − previous). Each point represents the amount for that interval.

Example — bank account
Track the same activity in two ways: deltas (each transaction) and cumulative (account balance).

* Start: balance = 0
* Deposit: +1000 → delta = +1000, cumulative = 1000
* Salary: +500 → delta = +500, cumulative = 1500
* Groceries: −200 → delta = −200, cumulative = 1300

If you sum all deltas (+1000 + 500 − 200) you get the net change equal to the final cumulative balance (1300).

| Date   | Transaction |   Delta | Cumulative |
| ------ | ----------- | ------: | ---------: |
| Jan 1  | Deposit     | `+1000` |     `1000` |
| Jan 5  | Salary      |  `+500` |     `1500` |
| Jan 15 | Groceries   |  `-200` |     `1300` |

<Frame>
  <img alt="The image shows a table illustrating a bank account's transactions over time, detailing changes in balance with each transaction from January 1 to January 15." />
</Frame>

Practical example — AstroShop

* Cumulative metric: total checkouts recorded over time (e.g., 100 at 1 PM, 150 at 2 PM).
* Delta metric: checkouts during each interval (e.g., 100 during the first interval, 50 during the second interval).

To derive per-interval throughput from cumulative values you compute differences between successive points (e.g., `150 - 100 = 50`). If the instrument emits deltas directly, each reported point already represents the throughput for that interval.

<Frame>
  <img alt="The image shows a comparison of cumulative and delta metrics for checkouts over time in AstroShop, illustrating total checkouts and checkouts per hour." />
</Frame>

Why temporality matters

* Backend expectations: Observability backends may require either delta or cumulative inputs. Sending the wrong temporality can cause rejection or incorrect aggregation.
* Process restarts and resets: A cumulative counter that resets (e.g., due to a process restart) must be detected and handled. Without handling, difference calculations can yield negative deltas.
* Storage and efficiency: Delta metrics avoid storing long sequences of ever-increasing values but require reliable interval emission from the instrument or exporter.
* Alerting and interpretation: Using the wrong temporality can lead to double counting, missed events, or inaccurate alert triggers.
* Accurate conversions: Converting between cumulative and delta requires correct detection of resets and careful difference computation.

| Concern                      | Cumulative                | Delta                     |
| ---------------------------- | ------------------------- | ------------------------- |
| Ideal for long-term totals   | Yes                       | No                        |
| Easier per-interval analysis | No (requires diffing)     | Yes                       |
| Sensitive to resets          | Yes (must detect resets)  | Less sensitive            |
| Backend compatibility        | Some backends expect this | Some backends prefer this |

<Frame>
  <img alt="The image is a comparison chart explaining the differences and considerations between cumulative and delta metrics in data interpretation, storage efficiency, backend behavior, alerting accuracy, and avoiding data skew." />
</Frame>

> **lightbulb** Choose the temporality that matches your backend and use case. If you send cumulative metrics, ensure exporters and the backend handle resets; if you send delta, ensure your instrument produces interval deltas reliably. Misaligned temporality can produce incorrect aggregates and alerts.

Recommended practices

* Confirm backend expectations before choosing temporality (check ingestion docs).
* If using cumulative counters:
  * Ensure the backend or exporter can detect resets and compensate.
  * Record reliable timestamps and monotonicity where possible.
* If emitting deltas:
  * Guarantee consistent reporting intervals or include interval metadata.
  * Handle missed intervals or out-of-order deliveries in the exporter/collector.
* For conversions:
  * Always compute `delta = current_cumulative − previous_cumulative`, but detect negative results as resets.
  * When a reset is detected, treat the first post-reset delta as the value since restart (or follow backend-specific behavior).

Links and references

* [OpenTelemetry Metrics Specification](https://opentelemetry.io/docs/specs/otel/metrics/)
* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
* [Observability Best Practices: Metrics](https://www.usenix.org/conference/osdi20/presentation/mann)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/5fb1eabd-3a92-4c9b-ae75-5f2c609c2495)
