# Preparing for Incidents

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Incident-Management/Preparing-for-Incidents/page

Guidance on preparing teams for incidents through playbooks, sustainable on-call design, drills, triage, escalation, and blameless postmortems to improve recovery and prevent repeat failures

Welcome to the incident management module. Earlier we explored how SREs manage complexity, risk, and toil—skills that keep systems stable over time. Even with solid design and maintenance, failures still happen. Incident management defines what to do when reliability breaks down and, crucially, how to learn from failures so they don’t repeat.

This lesson covers:

* Preparation and practice (playbooks, drills, simulations)
* Sustainable on-call design and escalation
* Alerting and triage basics
* Incident roles, structure, and priorities
* Blameless postmortems and Root Cause Analysis (RCA)

By the end you should view incidents not just as disruptions, but as opportunities to improve system resilience and reduce repeat failures.

## Why preparation matters

Preparation builds the muscle memory teams need to act calmly and consistently during an incident. Teams that practice response patterns recover faster and make fewer costly mistakes; unprepared teams tend to scramble, extend outages, and increase business impact.

Consider a high‑stakes scenario: if a critical payment service fails at 02:47 and every minute costs \$50,000, the difference between a contained outage and a catastrophe often comes down to preparation and process. As Ben Treanor said: hope is not a strategy.

Preparedness does not eliminate outages, but it dramatically improves how you respond and recover.

### Preparedness activities

Concrete actions teams can take before incidents occur:

* Define detection, response, and recovery processes.
* Assign role-based responsibilities and clear escalation paths.
* Create concise playbooks for frequent failure modes.
* Train staff with simulations, tabletop exercises, and game days.
* Build a blameless culture of continuous improvement and post-incident learning.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Preparation Matters&#x22; showing five numbered boxes that list pre-incident preparation steps: establishing detection/response/recovery processes, defining role-based responsibilities and escalation paths, creating playbooks, training via simulations, and fostering continuous improvement. The slide is visually organized with icons and colored bordered cards for each step." />
</Frame>

### The cost of not preparing

Consequences of poor preparation include:

* Longer outages due to disorganized responses
* Larger business and customer impact
* Increased burnout and stress for engineers
* Reputational damage from repeated failures
* Knowledge silos where only a few experts can resolve certain problems

In most organizations, the investment to prepare and practice is far smaller than the cost of repeated, poorly handled incidents.

## Anti-patterns and recommended practices

Avoid these common anti-patterns and prefer the alternatives:

* Anti-pattern: Throwing a junior engineer into on-call without training.
  Recommended: Structured ramp-up, shadowing, and mentoring.
* Anti-pattern: Relying on rigid checklists without system understanding.
  Recommended: Teach reasoning, reverse engineering, and metrics-based thinking.
* Anti-pattern: Hiding outages to avoid blame.
  Recommended: Blameless postmortems and transparent learning.
* Anti-pattern: Centralizing knowledge among a few experts.
  Recommended: Rotate responsibilities, conduct role-play incidents, and spread ownership.

<Frame>
  <img alt="A slide titled &#x22;Incident Preparedness Patterns&#x22; showing two columns: &#x22;Anti-Patterns&#x22; on the left and matching &#x22;Recommended Patterns&#x22; on the right. It pairs common bad practices (e.g., &#x22;trial by fire,&#x22; hiding outages, pushing juniors into primary on‑call) with suggested fixes (e.g., concrete training, postmortems, shadowing juniors)." />
</Frame>

<Callout icon="warning">
  Avoid unstructured on-call assignments (e.g., “trial by fire”). Insufficiently prepared responders increase outage duration and risk operator error. Always pair training, shadowing, and clear playbooks with liveliness checks before assigning primary on-call duties.
</Callout>

## On-call design principles

A sustainable on-call program reduces burnout and improves response quality. Principles to apply:

* Keep shifts manageable (commonly one-week rotations).
* Use primary and secondary rotations so coverage is resilient.
* Consider follow-the-sun models for globally distributed teams.
* Provide dedicated recovery time after on-call duty (time off or lighter schedules).
* Page engineers only for services they can reasonably triage and remediate.

Below is an example on-call rotation for a fictional KodeKloud Record Store app: one-week primary shifts with 30‑minute handoff overlap, staggered secondaries, recovery time after on-call, and a defined escalation ladder.

<Frame>
  <img alt="A presentation slide titled &#x22;On-Call Preparation&#x22; featuring a colorful gear graphic and the heading &#x22;Key Principles.&#x22; Around the gear are callouts listing guidelines like sustainable rotations, primary/secondary on-call engineers, dedicated recovery time, limiting pagers to services engineers can troubleshoot, and follow-the-sun models." />
</Frame>

### Example rotation and escalation rules

Key rules for an example rotation:

* Primary shifts: no more than one week, with 30‑minute overlap for handoffs.
* Secondary shifts: staggered (e.g., three days behind) so pairs vary over time.
* Secondary acts as backup and next in the escalation ladder.
* Engineers receive at least two weeks off from on-call after serving as primary; major incidents trigger additional recovery time.
* Provide compensation or time‑off for disruptive weekend or off‑hours pages.

Escalation ladder example:

* Primary must acknowledge within 15 minutes and start remediation.
* If unresolved, secondary is engaged within 15–30 minutes.
* Escalate to team lead if the issue persists.
* Engineering manager handles the most severe incidents (P0/P1).

<Frame>
  <img alt="A presentation slide titled &#x22;On-Call Preparation&#x22; that outlines an example four-part on-call rotation—Primary Rotation, Secondary Rotation, Recovery Rotation, and Escalation Ladder—each shown with brief bullet points. The bullets summarize shift rules (e.g., max one-week primary shifts, staggered secondary, two-week recovery, and escalation response times)." />
</Frame>

## Playbooks: fast, actionable runbooks

A playbook is a concise runbook for diagnosing and resolving a recurring incident. At 2 a.m. you want short, reliable steps — not long narratives.

Effective playbooks contain:

* Trigger conditions (alerts/metric thresholds) to identify applicability
* Clear step-by-step triage (eliminate obvious causes first)
* Links to dashboards, logs, runbooks, and monitoring views
* Exact commands or scripts to reduce ambiguity
* Escalation criteria and on-call contact information
* Recovery verification steps and rollback procedures
* Preventive follow-ups to reduce recurrence

<Callout icon="lightbulb">
  Keep playbooks current and test them during drills. If a playbook step proves unclear in a real incident, update it immediately during the postmortem.
</Callout>

### Example playbook: database connection pool exhaustion

Typical playbook elements for connection pool exhaustion:

* Trigger: connection usage ≥ 90% OR log messages like "too many connections".
* Impact: transactions fail with 500 errors; dashboards show degraded performance.
* Triage: check connection pool metrics, confirm DB health, inspect recent deployments for leaks.
* Mitigation: rollback suspect deployment; restart application servers in sequence; temporarily increase pool size (include exact CLI/database commands).
* Escalation: contact DB team or on-call DBA after 15 minutes if unresolved.
* Prevention: enforce connection pooling best practices, code review for leaks, add alerts for connection thresholds.

<Frame>
  <img alt="A playbook slide titled &#x22;Database Connection Pool Exhaustion&#x22; that lists mitigation steps (rollback, restart app servers, temporarily increase pool), escalation contact info, and a prevention note to review application code for connection leaks." />
</Frame>

## Incident priority levels (P0–P3)

Use priority levels to standardize severity, response expectations, and who to involve.

| Priority | Description                                                          | Typical response                                                         |
| -------: | -------------------------------------------------------------------- | ------------------------------------------------------------------------ |
|       P0 | Critical incident: full outage, data loss, or active security breach | Immediate paging of on-call, incident commander, cross-team coordination |
|       P1 | Severe degradation: major functionality broken                       | Rapid response, escalation paths engaged, possible incident meeting      |
|       P2 | Partial impact: degraded experience, system usable                   | Triage during business hours, track remediation work                     |
|       P3 | Non‑critical issue or identified risk                                | Monitor and schedule fixes as part of backlog                            |

<Frame>
  <img alt="A presentation slide titled &#x22;Incident Declaration and Escalation&#x22; showing a table of incident priority levels. It lists P0–P3 with brief descriptions (P0: full outage/data loss/security breach; P1: severe degradation/major functionality broken; P2: partial impact/degraded experience; P3: non‑critical issue/risk identified)." />
</Frame>

### Escalation triggers

Common triggers to escalate an incident:

* It exceeds predefined time thresholds without progress.
* It requires expertise beyond the current responder’s scope.
* Multiple teams or services are involved and coordination is necessary.
* Impact increases despite remediation attempts.

<Frame>
  <img alt="A presentation slide titled &#x22;Incident Declaration and Escalation&#x22; showing four escalation triggers: 01 incident exceeds time thresholds, 02 issue requires specialized expertise, 03 problem spans multiple teams or services, and 04 incident impact increases during resolution attempts. The slide uses numbered cards with simple icons and brief descriptions." />
</Frame>

## Practice and simulations

Preparation is incomplete without practice. Exercises build experience, test playbooks, and reveal gaps in tooling and procedures.

Useful exercise types:

| Exercise Type           | Purpose                                                               |
| ----------------------- | --------------------------------------------------------------------- |
| Tabletop scenarios      | Low-stress decision-making and communication walkthroughs             |
| Game days               | Scheduled tests of specific failure modes and operational playbooks   |
| Chaos engineering       | Controlled fault injection to validate system resilience              |
| Postmortem reenactments | Walk through past incidents with new team members to retain knowledge |

Regular practice improves both systems and people, making incident responses more predictable and effective.

<Frame>
  <img alt="A presentation slide titled &#x22;Simulation and Training&#x22; that outlines how regular practice improves incident response capabilities. A semicircular diagram shows four exercise types—Tabletop Scenarios, Game Days, Chaos Engineering, and Post‑Mortem Reenactments—with brief descriptions and icons." />
</Frame>

### A practical exercise: Wheel of Misfortune

A structured simulation template to build hands-on experience:

1. Select an incident scenario.
2. Assign an incident commander.
3. Assign supporting roles (communications, triage, escalation, scribe).
4. Work the scenario end-to-end using playbooks and escalation paths, then run a short retro.

This interactive exercise helps teams practice coordination under stress and validates processes.

<Frame>
  <img alt="A presentation slide titled &#x22;Simulation and Training&#x22; showing Google's &#x22;Wheel of Misfortune&#x22; exercise with a colorful circular arrow diagram. The right side lists four steps: 01 Select Incident Scenario, 02 Assign Incident Commander, 03 Assign Roles, and 04 Work-Through Scenario." />
</Frame>

## Closing and next steps

Preparation reduces incident impact: clear processes, tested playbooks, sustainable on-call rotations, and regular practice turn outages into learning opportunities. In later lessons we'll cover alert design to reduce noise and surface meaningful signals, plus how AI can help detect and prioritize incidents.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Chaos Engineering Resources (Principles and Best Practices)](https://principlesofchaos.org/)
* [Incident Management and Postmortem Practices](https://landing.google.com/sre/workbook/chapters/incident-response/)
* [On-Call Best Practices and Burnout Prevention](https://sre.google/sre-book/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/db75c0b7-05a9-41f7-b34d-762421f8b595/lesson/d4e148a9-9f5a-473e-978d-4a7457ad7d61" />
</CardGroup>
