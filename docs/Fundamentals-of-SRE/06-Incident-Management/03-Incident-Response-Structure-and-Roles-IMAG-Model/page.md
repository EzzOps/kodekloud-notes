# Symptom (user-facing)
music_playback_failures:
  metric: 'streaming_errors / streaming_requests'
  threshold: '0.001'  # 0.1% error rate
  impact: 'Users cannot play songs'

# Cause (infrastructure)
disk_space_trending:
  metric: 'disk_usage_trend_24h'
  threshold: '> 95% in 4 hours'
  justification: 'Prevents user impact before it occurs'
```

Prioritize symptom-based alerts. Google's SRE practice recommends symptom-first alerting because it reduces unnecessary noise, keeps attention focused on user impact, and remains meaningful even when underlying failure modes are unfamiliar.

> **lightbulb** Prioritize alerts that reflect user-visible symptoms. Use cause-based alerts sparingly and only when they provide predictive value or critical diagnostics.

Cause-based alerts still matter when they predict imminent user impact (e.g., disk filling to 100%), provide critical troubleshooting signals during incidents, or detect security/resource-exhaustion conditions that could quickly degrade service. The key is to limit these to actionable, high-value signals.

SLOs as the foundation for alerting

Service Level Objectives (SLOs) tie alerting to the promises you make customers. Anchoring alerts to SLOs avoids arbitrary thresholds (e.g., "why CPU > 80%?") and aligns operational effort with business risk.

Typical SLO-based workflow:

1. Define meaningful SLOs for each service (example: 99.9% availability).
2. Create error-budget and burn-rate alerts that measure how quickly your error budget is being consumed.
3. Establish tiered thresholds for different burn rates (fast burn vs slow burn) with appropriate actions.

<Frame>
  <img alt="The slide titled &#x22;SLO-Based Alert Implementation&#x22; outlines a basic three-step structure for alert design: 1) define meaningful SLOs (e.g., 99.9% availability), 2) create &#x22;burn rate&#x22; alerts based on error budget consumption, and 3) establish varied thresholds for different consumption rates. It appears to be a presentation slide from KodeKloud about using Service-Level Objectives for alerting." />
</Frame>

Example context: if the Checkout API has a 99.9% success SLO, that implies \~0.1% failure budget (\~43.2 minutes of errors per 30 days). Alerts should focus on how quickly that budget is being consumed so you act when risk to users becomes unacceptable.

<Frame>
  <img alt="A presentation slide titled &#x22;SLO-Based Alert Implementation&#x22; explaining that Service Level Objectives provide a foundation for alert design. The example shows a Checkout API with a 99.9% SLO and a 0.1% error budget (43.2 minutes of errors per 30 days)." />
</Frame>

Tiered SLO-based alerts

Use tiered alerting to balance urgency and noise. Example tiers:

|   Severity | Error Budget Consumption | Typical Action                 |
| ---------: | -----------------------: | ------------------------------ |
|     Urgent |  100% consumed in 1 hour | Page on-call immediately       |
|       High |  25% consumed in 6 hours | Page on-call                   |
|     Medium |    50% consumed in 1 day | Email team                     |
| Low / Load |   75% consumed in 3 days | Create a ticket / backlog item |

<Frame>
  <img alt="A presentation slide titled &#x22;SLO-Based Alert Implementation&#x22; showing three alert levels (Urgent, High, Medium) with columns for error budget consumption and action triggered. Urgent = 100% in 1 hour (page on‑call); High = 25% in 6 hours (page on‑call); Medium = 50% in 1 day (email team)." />
</Frame>

Example Prometheus-style alerting rules (simplified) that show cause vs symptom and an SLO burn-rate pattern:

```yaml theme={null}
groups:
- name: example-alerts
  rules:
  - alert: HighCPU
    expr: |
      1 - avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage on instance"

  - alert: CheckoutLatencySLOViolation
    expr: |
      histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="checkout"}[5m])) by (le))
      > 0.5
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Checkout p95 latency > 500ms — conversion impact likely"
      runbook: "https://example.com/runbooks/checkout-high-latency"
```

Example error-budget burn-rate rules for the KodeKloud Record Store:

```yaml theme={null}
groups:
- name: slo-error-budget
  rules:
  # Fast burn — pages immediately
  - alert: StreamingErrorBudgetBurnFast
    expr: |
      (
        sum(rate(streaming_request_errors_total[5m]))
        /
        sum(rate(streaming_requests_total[5m]))
      ) > (0.001 * 15)  # SLO error rate * 15 -> ~budget gone in 2 days (30d/2d = 15)
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Streaming error budget burning ~15x too fast"
      action: "Page @streaming-team immediately; see runbook"

  # Slow burn — warns but does not page
  - alert: StreamingErrorBudgetBurnSlow
    expr: |
      (
        sum(rate(streaming_request_errors_total[5m]))
        /
        sum(rate(streaming_requests_total[5m]))
      ) > (0.001 * 2)  # SLO error rate * 2 -> ~budget gone in 15 days
    for: 30m
    labels:
      severity: warning
    annotations:
      summary: "Streaming error budget elevated consumption"
      action: "Review in next standup"
```

Alert routing and escalation

Routing and escalation decide who gets notified and how:

* Map severity to notification channel: pages/SMS for urgent, chat/email for non-urgent.
* Route to the team with the access and expertise to fix the issue.
* Define an escalation path for unacknowledged alerts and keep on-call rotations documented.
* Consider follow-the-sun models to balance load across time zones.
* Use deduplication, grouping, and correlation to avoid alert storms.

<Frame>
  <img alt="A slide titled &#x22;Alert Routing and Escalation&#x22; outlining routing principles for notifications. It shows five colored cards recommending aligning alert severity with notification methods, routing to the right team, clear escalation paths, time-zone-aware follow-the-sun support, and deduplication to prevent alert storms." />
</Frame>

Practical checklist for implementing alerts

1. Define the user impact: explicitly state what user behavior or business metric the alert detects.
2. Select metrics that indicate that impact (prefer service-level metrics like latency, error rates, availability).
3. Establish thresholds with historical telemetry — avoid arbitrary numbers.
4. Test sensitivity: simulate incidents and verify alerts trigger reliably and are resilient to noise.
5. Document actions: attach runbooks/playbooks that tell responders exactly what to do.
6. Review and tune regularly: remove false positives/negatives and adjust thresholds as the system evolves.

<Frame>
  <img alt="A presentation slide titled &#x22;Practical Alert Implementation&#x22; showing an &#x22;Alert Implementation checklist.&#x22; It features a horizontal timeline with six colorful pin icons listing: Define User Impact, Select Metrics, Establish Thresholds, Test Sensitivity, Document Analysis, and Review Regularly." />
</Frame>

Summary

Design alerts to reflect user impact first, use SLOs and burn rates to make alerting objective and measurable, and keep cause-based signals focused and actionable. Route alerts to the right responder, and continuously validate and refine thresholds with real telemetry.

That's it for the Designing Alerts lesson. We will cover incident response structures and roles next, including a model useful for incident response preparation.

Further reading and references

* [Google SRE](https://sre.google/) – guidance on SLOs and alerting best practices
* [Prometheus](https://prometheus.io/) – alerting rule examples and metrics collection

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/db75c0b7-05a9-41f7-b34d-762421f8b595/lesson/a379d66c-c179-4b74-a308-f2a86ee4de63)


# Incident Response Structure and Roles IMAG Model

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Incident-Management/Incident-Response-Structure-and-Roles-IMAG-Model/page

Guidance on structuring software incident response with the IMAG model, defining roles, severity, response phases, communications, documentation, and post-incident learning to reduce recovery time.

Welcome back. This lesson explains how to structure incident response using the IMAG model (Incident Management at Google). The IMAG approach applies proven incident-command principles from emergency response to software incidents, helping teams act quickly and consistently by assigning clear roles, a single source of truth, and repeatable processes.

When incidents start without structure, teams duplicate effort, documentation is missed, and leadership gets fragmented updates — all of which increase mean time to recovery (MTTR). A structured response assigns coordination, communications, and technical work to specific roles so engineers can focus on restoration.

<Frame>
  <img alt="An illustration titled &#x22;A Story of Incident Response&#x22; showing an incident commander and two engineers at desks, each with speech bubbles like &#x22;Who's fixing the database?&#x22; and &#x22;I thought you were doing it!&#x22;. The caption at the bottom reads, &#x22;Clear roles stop chaos during incidents.&#x22;" />
</Frame>

Why structure matters

* Prevents redundant work and conflicting actions.
* Establishes a single source of truth for status and decisions.
* Keeps stakeholders informed while technical responders focus on fixes.
* Shortens time to recovery through coordinated mitigation and investigation.

<Frame>
  <img alt="A presentation slide titled &#x22;Incident Management Frameworks&#x22; showing four problems organizations face without structured incident response: uncoordinated troubleshooting, unclear communication and redundant work, stakeholders left in the dark, and difficulty tracking incident progress." />
</Frame>

Core IMAG principles
IMAG imports emergency incident-command best practices and tailors them for software operations. Its goals are clarity of roles, controlled span of control, a unified command, shared terminology, and modular activation of roles depending on incident scale.

* Clear chain of command: every role has defined responsibilities.
* Span of control: limit direct reports to roughly 3–7 people to avoid overload.
* Unified command: one authoritative view for status and decisions.
* Common terminology: consistent language reduces cross-team confusion.
* Modular organization: activate only the roles you need for the incident.

<Frame>
  <img alt="A presentation slide titled &#x22;Incident Management Frameworks&#x22; that lists key principles for incident response. It names and briefly explains five items: Clear chain of command, Span of control, Unified command, Common terminology, and Modular organization, each with an icon." />
</Frame>

Common practices shared across incident frameworks
Most mature incident programs use the same building blocks: defined roles, severity classification, formal response phases, blameless postmortems, and regular practice via tabletop drills or game days.

| Resource                | Purpose                                                   | Example                                                             |
| ----------------------- | --------------------------------------------------------- | ------------------------------------------------------------------- |
| Roles                   | Define responsibilities and single points of coordination | Incident Commander, Communications Lead, Operations Lead            |
| Severity classification | Communicate impact and escalation                         | SEV-1 / SEV-2 / SEV-3                                               |
| Response phases         | Structure work from triage to postmortem                  | Detection → Mitigation → Investigation → Resolution → Post-Incident |
| Postmortems             | Learn and prevent recurrence                              | Blameless analysis and action items                                 |
| Practice                | Reduce friction under pressure                            | Tabletop drills / game days                                         |

<Frame>
  <img alt="A slide titled &#x22;Incident Management Frameworks&#x22; showing a two-column table of common practices and examples for incident response. It lists items like clear roles, severity classification, formal response phases, postmortems, and regular practice exercises with examples (Incident Commander, P0/P1/P2 or Sev-1/Sev-2, NIST/SANS, blameless culture, tabletop drills)." />
</Frame>

Key IMAG roles and responsibilities
Below are the core IMAG roles and their primary responsibilities. These roles separate coordination, communications, and technical operations so responders can work without interruption.

* Incident Commander (IC): coordinates the response, sets priorities and update cadence, makes key decisions, and protects responders from interruptions. The IC focuses on coordination and decision-making rather than hands-on technical fixes.
* Communications Lead (CL): manages stakeholder communications, prepares summaries for technical and non-technical audiences, and ensures updates are timely and clear.
* Operations Lead (OL): coordinates technical troubleshooting, organizes responders and runbooks, and provides technical status updates to the IC.

<Frame>
  <img alt="A slide titled &#x22;Key Incident Response Roles – Primary Responsibilities&#x22; showing three columns for Incident Commander (IC), Communications Lead (CL), and Operations Lead (OL). Each column lists duties like coordinating the incident and making decisions (IC), managing communications and stakeholder updates (CL), and leading technical troubleshooting and fixes (OL)." />
</Frame>

Traits that make each role effective

* IC: calm under pressure, decisive, and coordination-focused.
* CL: strong communicator, translates technical detail for broader audiences, organized and reassuring.
* OL: strong technical skills, pragmatic problem-solver, and able to coordinate across teams.

Match people to roles based on these traits so the response runs smoothly.

<Frame>
  <img alt="A slide titled &#x22;Key Incident Response Roles – Traits by Role&#x22; showing three roles—Incident Commander (calm under pressure, decisive, coordination-focused), Communications Lead (strong communicator, translates technical details, organized), and Operations Lead (strong technical skills, problem solver, coordinates teams). The slide is copyrighted by KodeKloud." />
</Frame>

Detection, declaration, and initial triage
Incident response starts with detection: an alert, monitoring signal, or user report. The first triage question is whether the event requires a formal incident response. If not, handle it via normal support channels. If yes:

1. Assign an Incident Commander.
2. Declare the incident and set a severity.
3. Assemble the response team and open the single source-of-truth (timeline/comm doc).

<Frame>
  <img alt="A flowchart titled &#x22;Incident Declaration and Classification&#x22; showing steps: Identify Potential Incident → Formal Response Required? → (yes) Assign Incident Commander → Declare Incident and Assign Severity → Assemble Response Team (or → End if no)." />
</Frame>

Severity classification
Severity indicates customer impact and required response intensity. Organizations may label severities differently (SEV-1/2/3, CEV-1/2/3). Use a clear table to align on expectations for escalation, staffing, and runbook activation.

| Severity                 | Impact                                                         | Typical Response                                               |
| ------------------------ | -------------------------------------------------------------- | -------------------------------------------------------------- |
| SEV-1 / CEV-1 (Critical) | Complete outage, major data loss, revenue-impacting failure    | Full incident command active, 24/7 response, rapid escalations |
| SEV-2 / CEV-2 (Major)    | Significant degradation or partial outage affecting many users | Core roles activated, extended coverage, focused mitigation    |
| SEV-3 / CEV-3 (Minor)    | Limited impact, non-critical features                          | Business-as-usual handling, scheduled follow-up if needed      |

<Frame>
  <img alt="A presentation slide titled &#x22;Incident Declaration and Classification&#x22; showing three columns for SEV-1 (Critical), SEV-2 (Major), and SEV-3 (Minor). Each column lists brief bullet points describing impact, response level, and escalation risk for that severity." />
</Frame>

> **lightbulb** Severity describes impact (how bad the incident is). Priority (P0, P1, etc.) describes urgency (how quickly it should be addressed). Keep them separate — for example, a low-severity bug can become high-priority if it affects a key customer.

IMAG response phases
IMAG divides response into distinct, repeatable phases to keep work organized and traceable:

1. Detection & Declaration — Triage and decide whether to declare an incident and its severity.
2. Mitigation — Reduce user impact quickly (workarounds, rollbacks, traffic shifts).
3. Investigation — Collect logs, traces, and metrics to identify root cause.
4. Resolution — Implement and verify a permanent fix; confirm service health.
5. Post-Incident — Run a blameless postmortem, document findings, and update runbooks.

Tools and channels commonly used

* Chat platforms for real-time coordination: Slack, Microsoft Teams.
* External status pages to inform customers: statuspage.io.
* Docs & wikis for the incident timeline and decisions: Google Docs, Confluence.
* Video/voice bridges for live coordination and recordings: Zoom.
* Timeline/tracking tools to maintain a single source of truth.

External communication and transparency
Public status pages and timely customer updates help preserve trust during incidents. Coordinate internal and external messages via the Communications Lead so messages are consistent and appropriately technical for each audience.

<Frame>
  <img alt="A slide titled &#x22;External Incident Communication&#x22; showing two status-page screenshots labeled AWS and Slack. Both screenshots display service health/status information (indicating no recent issues)." />
</Frame>

Capture the incident in a single source of truth
Document decisions, timestamps, actions, and responsible parties in real time. This reduces duplicated effort, speeds handoffs, and simplifies the post-incident review.

Typical documentation flow:

* Slack channels for coordination and quick context.
* Google Docs (or similar) for the incident timeline and IC notes.
* Status page entries for customer-facing updates.
* Voice/video recordings for later review.

<Frame>
  <img alt="A flowchart titled &#x22;Incident Response Communication and Documentation Flow&#x22; showing that when an incident occurs it branches to Slack channels, Google Docs, a status page, and a video bridge. Each branch lists subcomponents (Slack channel names, incident/technical docs, external customer communications, and voice/recording for review)." />
</Frame>

Example timeline — payment-processing outage (condensed)

* 14:15 — Multiple alerts trigger; potential incident identified and declared.
* 14:20 — Incident Commander assigned and severity set.
* 14:25 — Team assembles; IC sets update cadence; Communications Lead begins status updates; Operations Lead gathers technical responders.
* 14:45 — Mitigation in progress: rollback initiated, traffic routed to backups, partial service restored.
* 15:30 — Rollback completes, payments verified, full service restored.
* 16:00 — Incident closed, status page updated, stakeholders notified, and a postmortem scheduled.

This timeline demonstrates how defined roles and a single source of truth accelerate recovery and reduce confusion.

Wrap-up
A structured IMAG-based incident response reduces chaos, clarifies responsibilities, and shortens MTTR. Follow-up activities — blameless postmortems, updates to runbooks, and regular practice — are essential to improving resilience and preventing recurrence. For more on runbooks and tabletop exercises, see the related resources and vendor docs like [Kubernetes documentation](https://kubernetes.io/docs/) or [statuspage examples](https://www.atlassian.com/software/statuspage).

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/db75c0b7-05a9-41f7-b34d-762421f8b595/lesson/6c32ea05-7eeb-4bb1-b833-98c766e13b08)
