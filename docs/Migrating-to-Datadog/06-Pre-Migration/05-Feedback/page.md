# Feedback

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Feedback/page

Defining roles, responsibilities, and escalation paths among platform engineers, DevOps, and end users to streamline observability migration, feedback flows, and incident resolution.

This lesson describes how feedback moves between teams during an observability rollout and clarifies what each persona is responsible for. Defining clear responsibilities and an agreed escalation path reduces risk during migration and accelerates incident resolution.

There are three primary personas involved: Platform Engineers, DevOps Engineers, and End Users. Below we define each role, show the relationships between them, and provide a recommended feedback loop.

## Platform engineers

Platform engineers design, implement, and maintain the enterprise observability platform. They own platform-wide configuration, shared integrations, and architecture decisions. Because their changes affect many teams, validation and careful change management are critical.

<Frame>
  <img alt="The image illustrates a feedback process involving Platform Engineers, DevOps Engineers, and End Users, highlighting the responsibilities of Platform Engineers." />
</Frame>

## DevOps engineers

DevOps engineers operate the environments where business applications run. They configure observability components for specific services, maintain application stability, and coordinate closely with both platform engineers and end users during migration and incidents.

<Frame>
  <img alt="The image visually represents the roles of Platform Engineers, DevOps Engineers, and End Users, highlighting the functions of DevOps Engineers in setting up observability components, ensuring app stability, and bridging between platforms and users." />
</Frame>

## End users

End users are the developers and business teams who rely on the platform day to day. They create dashboards and alerts relevant to their services and provide practical feedback about what works — and what doesn’t — in real scenarios.

<Frame>
  <img alt="The image shows a feedback flow diagram with three sections: Platform Engineers, DevOps Engineers, and End Users, with a note encouraging active platform use by end users." />
</Frame>

Putting the three personas together clarifies responsibilities and impact:

* Platform Engineers receive requests and incident reports from many teams. Their changes are high-impact: a misconfiguration can affect the whole company.
* DevOps Engineers manage the specific environments that will adopt the observability platform. Configuration errors can directly disrupt business services, and they often coordinate fixes with both platform and business teams.
* End Users generally do not change platform configuration. They report issues and depend on DevOps and platform teams to remediate them.

<Frame>
  <img alt="The image categorizes different types of engineers and users by their impact: Platform Engineers affect everybody, DevOps Engineers affect only their environment, and End Users have no effect." />
</Frame>

Summary table — responsibilities and scope

| Persona            | Primary responsibilities                                                                         | Scope / impact                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Platform Engineers | Platform architecture, shared integrations, global configs, enterprise policies                  | Company-wide — changes can affect all teams                      |
| DevOps Engineers   | Environment-specific observability setup, service-level debugging, coordination during incidents | Team- or environment-scoped — impacts specific business services |
| End Users          | Build dashboards/alerts, report real-world issues, validate monitoring relevance                 | Consumer role — informs platform and DevOps teams                |

A typical feedback path during migration or incident handling looks like this:

1. An end user discovers a problem (missing metric, alert noise, dashboard gap) and notifies their DevOps team.
2. The DevOps engineer investigates. If the issue stems from environment configuration or requires platform-wide changes, they escalate to platform engineering.
3. The platform engineer reviews platform-wide settings, corrects platform-level misconfigurations, and communicates remediation steps back to DevOps.
4. DevOps engineers validate the fix in the affected environment and confirm resolution with the end user.

This loop emphasizes why clear communication, defined responsibilities, and an agreed escalation path are essential for a stable observability migration.

<Frame>
  <img alt="The image shows a feedback loop among Platform Engineers, DevOps Engineers, and End Users, highlighting communication issues like platforms not working and metrics not being shown." />
</Frame>

> **lightbulb** Collaboration is essential. Define roles, responsibilities, and escalation paths up front. Use standardized configurations, automated validation checks, and clear documentation to minimize risky changes and speed up resolution. For platform-specific guidance, consult your provider's observability docs (for example, `https://docs.datadoghq.com/`) and align on change management processes before migration.

That's it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/8c4a3624-9a6d-49ad-a294-983fbc61ba81)
