# Designing Effective Alerts

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Incident-Management/Designing-Effective-Alerts/page

How to design actionable, SLO-driven alerts prioritizing user-impact symptoms, routing, escalation, and a practical implementation checklist

Now that we've covered preparation, let's focus on one of the most critical tools during incidents: alerts.

Not all alerts are equal. Some wake you up at 3 AM for no reason; others only trigger once customers are already furious. Effective alerts wake you up for a real problem — not noise. In this article we'll cover what makes an alert actionable, how to prioritize alert types, using SLOs as an alerting foundation, routing and escalation, and a practical implementation checklist.

What makes an alert effective?

Good alerts share several key attributes:

* They require human intervention — if no one needs to act, they shouldn't page.
* They focus on specific, user-impacting problems rather than only background metrics.
* They are concise and include enough context for an on-call engineer to triage quickly.
* They are routed to the proper owner and include links to dashboards and playbooks.

<Frame>
  <img alt="A presentation slide titled &#x22;Alert Design Principles&#x22; with a target and several arrows on the left. On the right are four actionable alerting criteria: requires human intervention, specific and precise, contains clear context, and has a defined owner." />
</Frame>

An alert that only says "CPU usage is high on server prod-api-03" is noisy and non-actionable. An actionable alert names the service impact, quantifies the problem, and points to remediation resources.

<Frame>
  <img alt="A slide titled &#x22;Alert Design Principles&#x22; showing two example alerts: a purple &#x22;Non-Actionable&#x22; alert saying &#x22;CPU usage high on server prod-api-03&#x22; and an orange &#x22;Actionable&#x22; alert describing &#x22;Order Processing API latency exceeding 2s SLO (current 5.2s) — affecting checkout flow; see dashboard and playbook [links].&#x22;" />
</Frame>

Actionable example summary:
"Order Processing API latency is exceeding the 2 s SLO; current p95 = 5.2 s; checkout flow affected; see dashboard and playbook." This tells the on-call engineer what is broken, who is affected, and where to look.

Alert types: symptom-based vs cause-based

Alerts generally fall into two categories:

* Symptom-based alerts: measure user-facing behavior — latency, error rates, availability. These map directly to business impact and tell you what is broken for users.
* Cause-based alerts: track implementation or infrastructure signals such as CPU, memory, or disk. They suggest why something might fail but don't necessarily indicate immediate user impact.

Both have a role, but they serve different purposes and should be used intentionally.

<Frame>
  <img alt="A presentation slide titled &#x22;Symptom-Based vs Cause-Based Alerting&#x22; that compares two alert types side-by-side. The left column describes symptom-based alerts (user-facing, focus on errors/latency and business impact) and the right column describes cause-based alerts (internal metrics like CPU/memory, suggesting why something broke)." />
</Frame>

Comparison table: symptom vs cause

| Alert Type    | Primary Goal               | Example                         | When to use                                                    |
| ------------- | -------------------------- | ------------------------------- | -------------------------------------------------------------- |
| Symptom-based | Detect user impact         | "Users cannot play songs"       | Always preferred for paging and prioritization                 |
| Cause-based   | Surface root-cause signals | "Disk usage trending above 95%" | Use for predictive or diagnostic value before symptoms surface |

YAML-style mapping (illustrative):

```yaml theme={null}
