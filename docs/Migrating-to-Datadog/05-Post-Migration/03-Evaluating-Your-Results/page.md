# Evaluating Your Results

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Post-Migration/Evaluating-Your-Results/page

Guidance for post-migration verification and stabilization, covering monitoring parity, telemetry, user feedback, observability adjustments, documentation, and a checklist to finalize and optimize a platform migration

This final lesson reviews your migration outcomes and outlines practical next steps to stabilize operations after cutover.

At this point your migration is complete and you have two environments running in parallel: the legacy environment and the modern environment. That’s an important milestone — now perform a thorough evaluation to ensure the new platform operates as intended and improves (or at least matches) the legacy behavior.

Core post-migration verification

* Confirm dashboards, monitors, queries, and alerts are firing and presenting expected results.
* Validate that reliability and functionality are maintained or improved compared to the legacy platform.
* Ensure visibility parity: don’t lose monitoring coverage, alerting fidelity, or key observability signals.

<Callout icon="lightbulb">
  Collect structured telemetry and incident data during the first few weeks after cutover so you can quantify differences between the old and new environments.
</Callout>

Gather end-user feedback

* Solicit feedback from users who now interact with the modern environment — they will surface operational issues you might not have seen during migration (for example: misconfigured alerts, permission gaps, or degraded user experiences).
* Triage and prioritize fixes based on impact: safety/stability issues first, followed by usability and performance improvements.
* Close the feedback loop: communicate resolved issues and expected timelines to stakeholders.

<Frame>
  <img alt="The image outlines post-migration best practices, emphasizing collecting feedback from end users and addressing any reported issues like misconfigured alerts or degraded experiences." />
</Frame>

Re-evaluate observability architecture
Now that the full system runs in production, revisit your observability design to optimize cost, signal quality, and future maintainability:

* Reassess data retention, collection granularity, and sampling to balance cost with signal fidelity.
* Add enhancements or new features that were deferred during migration (for example: more granular traces, additional dashboards, or enriched context in logs).
* Remove redundant or low-value metrics, tags, and dashboards to reduce noise and storage costs.

Inventory, documentation, and governance
One commonly overlooked but critical activity is updating your inventory and documentation. Accurate, versioned records make future troubleshooting, audits, and migrations predictable and less error-prone.

<Callout icon="warning">
  Keep an authoritative, versioned inventory of services, hosts, dashboards, monitors, and alerting policies. This prevents repeating past mistakes and makes future migrations smoother.
</Callout>

Post-migration checklist
Use the table below as a concise checklist to guide your post-cutover evaluation and stabilization work.

| Area                 | Key actions                                                                       |
| -------------------- | --------------------------------------------------------------------------------- |
| Monitoring parity    | Confirm alerts, dashboards, and queries match or improve upon legacy behavior     |
| Telemetry collection | Validate metrics, logs, and traces are complete and correctly correlated          |
| Incident data        | Collect structured incident and on-call data for the first 2–4 weeks post-cutover |
| User feedback        | Aggregate and prioritize user-reported issues and usability regressions           |
| Cost & sampling      | Reassess retention and sampling to optimize cost without losing signal fidelity   |
| Housekeeping         | Remove redundant metrics/tags and clean up stale dashboards                       |
| Documentation        | Update inventories, runbooks, diagrams, and configuration repositories            |

Links and references

* [Observability and monitoring best practices](https://www.datadoghq.com/solutions/observability/)
* [Incident response and postmortem practice](https://www.atlassian.com/incident-management/postmortems)
* [Metrics retention and sampling strategies](https://www.datadoghq.com/blog/metrics-storage/)

That concludes this lesson. Use these steps to validate your migration, prioritize follow-ups, and keep your monitoring and operations predictable and resilient.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/9add8e22-a057-4808-880b-be8b91e0d5f2/lesson/6278c35c-3b6a-4bfa-880b-45ebdca39a56" />
</CardGroup>
