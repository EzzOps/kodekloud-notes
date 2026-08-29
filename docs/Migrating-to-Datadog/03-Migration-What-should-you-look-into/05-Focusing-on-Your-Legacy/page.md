# Focusing on Your Legacy

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-What-should-you-look-into/Focusing-on-Your-Legacy/page

Guidance for migrating observability systems, managing legacy components and technical debt, organizing teams and roles, and best practices for decommissioning, instrumentation, dashboards, and alerting

When planning a migration, technical debt is the single most important risk you need to manage. Any legacy component that isn’t migrated—or at least integrated into the new solution—becomes technical debt and will almost certainly create problems later. Keep stakeholders and teams informed about the deactivation plan for legacy components and build contingency into your schedule.

> **lightbulb** Document every legacy component and its owner as early as possible. A simple control log (Excel, Kanban board, or an issue tracker) that lists component state, owner, and deactivation date will save significant time and risk down the line.

<Frame>
  <img alt="The image illustrates the concept of technical debt, showing a diagram where a legacy component that wasn't migrated or integrated leads to technical debt." />
</Frame>

Flexibility is essential: migrations often diverge from the original plan. Keep management apprised of delays and risks related to technical debt, and decide upfront which debt you will accept and which must be remediated before cutover.

<Frame>
  <img alt="The image outlines three strategies related to managing technical debt: keeping the team updated on legacy components, staying flexible and informing management of delays, and aligning with leadership on technical debt decisions." />
</Frame>

Your migration should start with discovery: catalog every component that interacts with your observability stack and that users rely on. With that inventory you can evaluate migration approaches and prioritize work.

Break this phase into three core elements:

* Legacy components: the concrete list of items to be migrated or retired.
* Coordinator(s): typically the project manager (PM) who tracks progress, ownership, deadlines, and blockers.
* Engineering teams: the squads that implement integrations, instrument services, and troubleshoot issues.

You’ll work with all three groups throughout the migration.

With components and teams identified, organize engineers into squads that focus on specific parts of the observability architecture. Many organizations find it effective to group teams by function. A common functional split is shown below.

<Frame>
  <img alt="The image depicts a diagram titled &#x22;Migration&#x22; showing a team selection process, with roles like Manager and Project Manager and categories such as Core, Dashboards, Alerts, Applications, and Others." />
</Frame>

Core team

* Owns backbone observability components: agent configuration, cloud-provider integrations, internal libraries, Helm charts, host/cluster agents, and platform-level tooling.
* Provides shared configuration and support that other teams rely on.

<Frame>
  <img alt="The image shows an organizational chart linking a &#x22;Core Team&#x22; to a software logo, which is connected to components like &#x22;Cluster Agent,&#x22; &#x22;Agent,&#x22; &#x22;Lambda Instrumentation,&#x22; and &#x22;Helm Chart.&#x22;" />
</Frame>

Dashboard team

* Converts telemetry into actionable views for both engineering and business stakeholders.
* Responsible for migrating legacy dashboards, improving visualizations, and building views that track availability, latency, and business metrics.

<Frame>
  <img alt="The image is a flowchart illustrating how a dashboard team uses dashboards to turn data into insights for various business and technical categories, such as business, technical, availability, and latency." />
</Frame>

Alerting team

* Ensures teams are notified when problems occur so they don’t need to constantly watch dashboards.
* Migrates existing alerts and creates new ones for business, technical, availability, latency, and anomaly detection to reduce manual monitoring overhead.

Application team

* Implements deep application-level observability: logging libraries across languages, custom application metrics, OpenTelemetry instrumentation, and APM enablement.
* Because instrumentation is often the most involved work, this should often be the largest team.

<Frame>
  <img alt="The image outlines the components and importance of an &#x22;Application Team,&#x22; highlighting tasks like logging, custom metrics, OTel instrumentation, and APM, suggesting it should be your largest team due to task complexity." />
</Frame>

Make the application team cross-functional. They should take on proofs of concept for new solutions, triage complex issues, and participate in a Center of Excellence (CoE) for observability.

<Frame>
  <img alt="The image is a diagram describing a cross-functional team's role, handling issues beyond other squads' scope, focusing on new components adoption, support/troubleshooting, and a Center of Excellence (CoE). The group also sets standards, supports issues, and leads on observability." />
</Frame>

Center of Excellence (CoE)

* A CoE is a multi-disciplinary group of subject-matter experts who define best-practice patterns, help troubleshoot hard problems, run knowledge-sharing, and guide observability strategy.

Project management and coordination

* The PM ensures the migration progresses: setting deadlines, communicating with management, coordinating teams, and protecting engineering squads from unrelated interrupts.
* The PM manages prioritization, handles urgent issues, resolves inter-team conflicts, and removes blockers.
* Reserve capacity for unplanned operational work and incident response during migration.

Table: Team responsibilities at a glance

| Team             | Primary responsibilities                                         | Key outputs                                 |
| ---------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| Core             | Agent configs, cloud integrations, Helm charts, shared libraries | Stable agent deployments, platform charts   |
| Dashboard        | Migrate and improve dashboards, business/technical views         | Business-facing dashboards, SLA views       |
| Alerting         | Migrate/create alerts, anomaly detection                         | Alerting rules, escalation policies         |
| Application      | Logging, custom metrics, OTel, APM                               | Instrumented services, libraries, tracing   |
| CoE              | Best practices, training, troubleshooting                        | Playbooks, templates, workshops             |
| PM / Coordinator | Track progress, remove blockers, communication                   | Control log, timelines, stakeholder updates |

Best practices and practical tips

* Prioritize high-risk legacy components first—those with no owner or those that have been patched repeatedly.
* Start simple: migrate basic telemetry before advanced features like distributed tracing and anomaly detection.
* Use the migration as an opportunity to improve observability: replace brittle dashboards, reduce alert noise, and standardize instrumentation.
* Keep documentation and runbooks updated as you migrate components.
* Measure progress with clear milestones and a control log of deactivations.

> **warning** Do not leave legacy components “running and forgotten.” Each unmanaged component is ongoing technical debt—plan explicit decommission dates and accountabilities before cutover.

Migration projects are opportunities to add value beyond parity. Good engineers will replicate functionality; great engineers will migrate and enhance monitoring so it better supports the business. Aim to study, migrate, and improve—deliver migrations that reduce risk and increase visibility.

Links and references

* [OpenTelemetry](https://opentelemetry.io/)
* [Datadog Documentation](https://docs.datadoghq.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

That's it for this lesson. I hope you enjoyed it.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/d7aaa833-22da-4f94-af5c-5d196f04ab31/lesson/af3093de-aea1-48ab-8bd1-0938e3a05a40)
