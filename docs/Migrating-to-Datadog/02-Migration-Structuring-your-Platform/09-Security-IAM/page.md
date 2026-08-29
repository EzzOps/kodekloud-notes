# Security IAM

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Security-IAM/page

Guidance on designing scalable Identity and Access Management for observability platforms, covering RBAC, IdP integration, automation, least privilege, lifecycle management, segregation of duties, and auditing

In this lesson we cover Identity and Access Management (IAM): what it is, why it matters for enterprise platforms, and how to design scalable, secure access control for your observability stack.

When you operate an organization-wide platform, the most frequent security challenge is provisioning and managing access for employees and third-party contractors without exposing sensitive data or hindering people from doing their jobs. A well-architected IAM program solves this by combining clear policies, automation, and enforcement.

Why IAM matters:

* Minimize risk by enforcing the principle of least privilege.
* Reduce operational overhead with automated provisioning and revocation.
* Improve compliance and auditability through consistent role definitions and access logs.
* Limit blast radius by granting only the resources required for a role.

A robust IAM program should include:

* Role-based access control (RBAC) with clearly documented roles and permissions.
* Segregation of Duties (SoD) to separate responsibilities and avoid conflicts of interest.
* Automation and self-service access requests so provisioning and revocation scale reliably.
* Monitoring and alerts for anomalous access or policy violations.

Sensitive data must be protected by explicit access policies and enforced controls. Map access to business roles and team responsibilities rather than to individuals whenever possible to simplify administration and audits.

<Frame>
  <img alt="The image outlines three access control best practices: implementing a strong IAM process, practicing segregation of duties, and securing sensitive data." />
</Frame>

Implementing access control for your observability platform

* Integrate your observability platform (for example, [Datadog](https://www.datadoghq.com)) with your Identity Provider (IdP) to centralize authentication and group membership.
* Design an IdP group structure that maps to organizational teams, role scopes, and environments (prod, staging, dev).
* Automate user lifecycle events (onboarding, transfers, offboarding) so access is granted and revoked consistently.

Example: employee mobility across teams

* Consider an engineer who moves between three teams in a single year. Instead of giving them ad-hoc access, manage permissions through groups that represent team scopes.
* Groups can be named to reflect team and tool (example groups below). As the employee transfers, you update group membership in the IdP and the observability platform inherits the correct permissions automatically.

| Group       | Purpose                   | Typical Permissions                                            |
| ----------- | ------------------------- | -------------------------------------------------------------- |
| `Group A`   | Primary Team A membership | Dashboard read/write, metrics query, alert acknowledgement     |
| `GRP-DDT-A` | Datadog access for Team A | Dashboards, logs, monitors limited to Team A resources         |
| `GRP-DDT-B` | Datadog access for Team B | Metrics, logs, alerts scoped to Team B                         |
| `GRP-DDT-C` | Datadog access for Team C | Read-only for some dashboards, write for team-owned dashboards |

These canonical group mappings ensure consistent access as the employee moves between teams.

<Frame>
  <img alt="The image depicts an &#x22;Employee Access Lifecycle with Datadog,&#x22; illustrating how an employee interacts with different teams (A, B, and C) over time, including implementing Datadog, leaving, and being promoted as a manager, with associated timelines and group codes." />
</Frame>

Permissions, lifecycle, and enforcement

* Define permissions per group for metrics, logs, dashboards, monitors/alerts, feature access, and administration.
* Use environment-scoped groups (for example, `team-prod`, `team-staging`) to reduce accidental access to production systems.
* Implement approval workflows for elevated access and temporary roles; time-bound access reduces long-term exposure.
* Log access changes and review membership periodically to detect stale privileges.

<Callout icon="lightbulb">
  Use the principle of least privilege: automate lifecycle events (onboarding, transfers, offboarding), and provide self-service requests with approval workflows. These measures help ensure access is granted only when needed and removed promptly when it is not.
</Callout>

<Callout icon="warning">
  Failing to automate offboarding or relying on manual access changes significantly increases security risk. Ensure offboarding workflows are integrated with HR events and the IdP to avoid orphaned accounts and lingering access.
</Callout>

Recommended checklist for IAM in observability platforms

* Integrate your IdP with the observability provider for single-source user management.
* Model groups by team and environment; avoid ad-hoc user permissions.
* Document RBAC roles and SoD policies; keep change history for audits.
* Automate approvals and time-bound elevated access.
* Regularly audit group membership and permissions; remove stale groups and rules.
* Monitor for anomalous access and set up alerts on permission changes.

Links and references

* [Datadog Identity and Access Management](https://docs.datadoghq.com/account_management/) — platform-specific IAM guidance.
* [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) — concepts for role-based permissions.
* [NIST Identity and Access Management](https://csrc.nist.gov/topics/identity-access-management) — standards and best practices.

Adopting strong IAM processes, RBAC with clear SoD, and protecting sensitive data will help your organization scale securely while maintaining control over access and auditability.

That's it for this lesson. I hope you found it useful.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/7342e054-4b25-4a1e-a3cb-d4dcb00e378e" />
</CardGroup>
