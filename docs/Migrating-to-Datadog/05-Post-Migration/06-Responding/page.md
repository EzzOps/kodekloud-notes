# Responding

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Post-Migration/Responding/page

Guide for DevOps and SRE incident response covering monitoring, alerting, Datadog integrations, triage using metrics logs traces, collaboration, and postincident runbooks to reduce detection and resolution time

This lesson covers incident response for DevOps engineers and SREs. In production environments that run 24/7, engineers must be prepared to detect, investigate, and remediate issues quickly. Monitoring, alerting, and a reliable incident workflow reduce mean time to detection (MTTD) and mean time to resolution (MTTR).

We instrument applications and infrastructure with monitoring and an alert management solution — in this guide, [Datadog](https://www.datadoghq.com/) — so the platform’s reliability and availability can be maintained automatically rather than by constant manual observation.

<Frame>
  <img alt="The image illustrates a DevOps and SRE process for monitoring and incident response, highlighting steps: build & innovate, monitor continuously, integrate alerts, and respond to incidents. It includes a workflow diagram showing the interaction between an environment, platform monitoring, alert creation, and engineers." />
</Frame>

<Callout icon="lightbulb">
  Instrument services and infrastructure so alerts route to the right people or teams. Proper signal-to-noise tuning prevents alert fatigue and ensures critical incidents are escalated immediately.
</Callout>

When the monitoring stack is configured correctly, engineers don’t need to stare at dashboards waiting for issues. Instead, alerts notify the relevant on-call responders when signals cross thresholds, which typically triggers incident creation and mobilizes responders.

Incidents usually involve multiple teams collaborating to determine what happened. Investigation relies on telemetry — logs, metrics, traces — plus contextual data (recent deployments, configuration changes, FinOps actions, or security events). This combination provides the evidence needed to isolate root causes and mitigate impact.

<Frame>
  <img alt="The image illustrates a flowchart for &#x22;Incident Detection and Root Cause Analysis,&#x22; showing a process from data and alerts to &#x22;Incident creation&#x22; and mobilizing teams, with logs and metrics feeding into incident creation." />
</Frame>

Datadog can manage incident creation and notifications. Integrating Datadog with collaboration tools such as [Slack](https://slack.com/) or [Microsoft Teams](https://www.microsoft.com/en/microsoft-teams) ensures teams receive alerts in real time — often including direct links to dashboards, log searches, and traces.

<Frame>
  <img alt="The image illustrates an incident detection and root cause analysis process, highlighting issues like increased latency and errors, with a focus on using internal communication channels." />
</Frame>

When an incident is created, the initial data you’ll typically receive includes:

* Which thresholds were crossed and at what times.
* Related events and timeline context (deployments, config changes, infra events).
* Links to relevant dashboards, log queries, and traces.

Use this initial payload to triage quickly. A practical first step is to run focused log queries in a Log Analyzer to locate application errors or unusual events that coincide with the alert window. If telemetry doesn’t reveal a cause, widen the investigation to include ecosystem changes: third-party API updates, infrastructure migrations, recent releases, or policy/permission changes.

Table — Incident triage: what to check and actions to take

| Item                  | What to look for                                      | Typical action                                      |
| --------------------- | ----------------------------------------------------- | --------------------------------------------------- |
| Alert details         | Thresholds, metric anomalies, incident start time     | Confirm alert validity, mark incident severity      |
| Logs                  | Errors, stack traces, correlated timestamps           | Narrow log queries, capture sample events           |
| Metrics               | Latency, error rates, host/container resource usage   | Pinpoint affected services and resource constraints |
| Traces                | Slow spans, failed calls, upstream/downstream latency | Identify failing operations and service boundaries  |
| Deployment history    | Recent releases, rollbacks, config changes            | Check for bad deploys; consider rolling back        |
| External dependencies | Third‑party API changes, DNS, certificate issues      | Contact provider or apply compensating changes      |

Real-world example: an app relies on an external API that changed its response format. If your code assumes the old payload shape, the app can crash despite having followed local best practices. Detecting such issues often requires collaboration with the API provider and adding resilient parsing or contract tests.

Incident analysis is iterative: you’ll move between telemetry sources, follow leads, and reconcile findings against the incident timeline. Keep a running timeline of actions taken and observations to help coordinate responders and preserve context for the post-incident review.

<Frame>
  <img alt="The image is a flowchart showing steps after incident detection, involving incident-related data, log querying, and external events, with various metrics involved. It notes that tracking external events can be difficult and highlights the iterative nature of the debugging process." />
</Frame>

<Callout icon="warning">
  Avoid jumping to remediation without confirming cause. Rapid changes (e.g., restarts, rollbacks) can complicate forensics. Document each action and its rationale during an incident.
</Callout>

With a modern observability platform like Datadog, investigation becomes more efficient: Datadog correlates metrics, logs, and traces; links related components; and aids root cause analysis. This correlation is especially valuable as systems scale and more services or resources are added without centralized visibility.

<Frame>
  <img alt="The image depicts a diagram related to modern incident response, including steps like analyzing incidents, linking metrics, logs, and traces, correlating with other components, and performing root cause analysis. There's also an illustration of a dog holding a graph." />
</Frame>

Post-incident: runbook updates and debrief

* Perform a blameless postmortem that includes timeline, root cause, mitigations, and follow-up actions.
* Update runbooks and playbooks with the steps that helped diagnose and resolve the incident.
* Communicate changes and lessons learned to impacted teams and stakeholders.
* Implement preventative fixes (alerts, tests, automation) and monitor for recurrence.

Key takeaways

* Expect and prepare for unexpected failures — resilience is a design goal.
* Use correlated telemetry (metrics, logs, traces) to speed root cause analysis.
* Keep teams informed and document the incident timeline and actions.
* Continuously improve runbooks and monitoring to reduce future impact.

References and further reading

* [Datadog](https://www.datadoghq.com/)
* [Slack](https://slack.com/)
* [Microsoft Teams](https://www.microsoft.com/en/microsoft-teams)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/9add8e22-a057-4808-880b-be8b91e0d5f2/lesson/cc1250b3-eaaa-44ec-a106-e861a995f34c" />
</CardGroup>
