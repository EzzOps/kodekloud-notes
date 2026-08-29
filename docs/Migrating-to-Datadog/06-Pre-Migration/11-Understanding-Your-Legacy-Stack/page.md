# Understanding Your Legacy Stack

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Understanding-Your-Legacy-Stack/page

Guide to planning a safe phased migration from legacy monitoring systems by mapping inventories, integrations, user needs, compliance constraints, and designing a sustainable target platform

Migrating a monitoring or observability platform requires a careful study of your current (legacy) technology stack. Successful migrations keep systems connected and functional while moving teams to a more sustainable platform. This guide helps you plan a safe, predictable migration by understanding what you have, why it matters, and how to prioritize work.

Start by inventorying the legacy systems and integrations. That early context reduces risk and lets you design a migration approach that aligns with business needs, deadlines, and compliance constraints.

<Frame>
  <img alt="The image is a slide titled &#x22;Migration Planning – Challenges&#x22; with two numbered boxes describing challenges: 1) aligning multiple elements, and 2) ensuring solutions meet all needs." />
</Frame>

> **lightbulb** Understanding your legacy environment uncovers risks early and helps you select a target platform that supports your business needs, integrations, and compliance constraints.

Why collect legacy information early?

* Reveal actual business needs and whether the current stack provides them.
* Surface shadow IT and undocumented systems for proper support and security.
* Document customizations to reproduce or improve them in the new platform.
* Expose application-level issues and environmental gaps that migrations must address.

Keep users at the center. The migration exists to make teams more effective — faster incident response, more reliable deploys, and better outcomes for customers. Replacing a useful tool with one that slows teams will reduce adoption and productivity.

Not knowing existing integrations or undocumented systems is a common migration failure point. Systems that have been left to drift often include critical but unseen dependencies. Map these before cutover, so you don’t accidentally remove visibility into essential workflows.

That’s why you don’t jump straight into migrating a solution — you plan and map first.

<Frame>
  <img alt="The image depicts a person working on a laptop with a graphic illustrating cloud migration, labeled &#x22;Migration Planning – Challenges&#x22; and &#x22;Understand Your Company's Legacy.&#x22;" />
</Frame>

If teams fail to understand these areas, common consequences include poor adoption, unsupported hidden systems, slowed engineering velocity, and failed outcomes.

<Frame>
  <img alt="The image is a diagram titled &#x22;Know Your Legacy Before Migration,&#x22; illustrating risks such as failed migrations, poor user adoption, unsupported hidden systems, and slowed engineering productivity." />
</Frame>

Always leave room to improve. Perform a legacy stack study to map what’s running and why before you migrate.

Legacy can mean many things: technology left behind, long-standing integrations, systems with few users but high impact, or tools that began as experiments and became production. Each of these needs special attention during planning.

<Frame>
  <img alt="The image is a diagram titled &#x22;Understand the Legacy Before Migration,&#x22; highlighting aspects like technology left behind, long-standing integrations, test tools in production, and few but important users." />
</Frame>

Expect migration timelines to be measured in months for large environments. Plan phased rollouts, validation windows, and time for teams to adopt the new platform.

<Frame>
  <img alt="The image outlines three steps for understanding the legacy before migration: understanding the environment, acknowledging the time it takes for migration, and emphasizing planning and team awareness." />
</Frame>

## Practical to-do list for mapping legacy systems

Below is a concise migration discovery checklist followed by detailed steps you can follow.

| Step                              | Goal                                         | Key actions                                                                 |
| --------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------- |
| 1. Gather existing knowledge      | Capture institutional memory and constraints | Interview long-time users, read docs, pull config from running systems      |
| 2. Map deployments & environments | Know where services run and how they differ  | Inventory dev/stage/prod, regional differences, and config drift            |
| 3. Interview users & owners       | Understand day-to-day usage and priorities   | Capture feature gaps, runbooks, and pain points to address during migration |
| 4. Identify legacy integrations   | Find critical data and control flows         | Trace APIs, message buses, scripts, and note fragile or undocumented links  |
| 5. Understand environment nuances | Ensure compliance and operational continuity | Document network topology, compliance zones, data residency, and limits     |

Detailed steps:

1. Gather existing knowledge
   * Interview long-time users and operators who understand historical decisions.
   * Retrieve available documentation and extract configuration directly from existing systems.
   * Collect feedback on pain points and common workarounds that you should address in the migration.

2. Map current deployments and environments
   * Inventory where each solution is deployed (dev, stage, prod) and regional variations.
   * Identify multiple implementations of the same product and where configuration drift exists.
   * Record operational runbooks, maintenance schedules, and escalation paths.

3. Interview users and owners
   * Understand how each tool is used daily and which features are critical.
   * Capture feature gaps and prioritize which issues the migration should resolve.
   * Use migration windows to deliver immediate value (e.g., fix known pain points during cutover).

4. Identify legacy integrations
   * Trace integrations between systems: APIs, message buses, mainframes, custom scripts, and scheduled jobs.
   * Mark integrations that are business-critical and need continuity during migration.
   * Document undocumented or fragile connections that require careful migration handling.

> **warning** Undocumented integrations are a major risk—map them before cutover. Migrating without this knowledge can break essential business functionality.

5. Understand environment nuances
   * Capture environment-specific constraints: network topology, compliance zones, data residency, and resource limits.
   * Confirm the target architecture accommodates these constraints and remains maintainable long-term.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Understand the Legacy Before Migration&#x22; outlining a five-step process: gather existing info, map current deployments, interview users, identify legacy integrations, and understand environment nuances." />
</Frame>

## Design principles for the target platform

Apply these guiding principles when designing the new platform so your migration delivers sustainable value:

* Users first: Prioritize developer and operator experience. The platform should make teams faster and more confident.
* Technology alignment: Align with company standards so performance, cost, and maintainability are predictable.
* Security and compliance: Involve security and compliance teams early; noncompliance can invalidate the migration outcome.
* Sustainability: Design for maintainability and future migrations. Expect platforms to evolve; make future moves cheaper and faster.

Quick reference: How each principle maps to action

| Principle             | Example actions                                                |
| --------------------- | -------------------------------------------------------------- |
| Users first           | Provide clear runbooks, dashboards, and simple onboarding      |
| Tech alignment        | Use standard images, automation, and policy-as-code            |
| Security & compliance | Map data residency, encryption, and access control needs early |
| Sustainability        | Build modular integrations and document migration patterns     |

## Next steps and resources

* Start with the discovery checklist and schedule interviews with platform owners.
* Build a phased rollout plan with validation windows and rollback criteria.
* Prioritize integrations and high-impact, low-effort fixes for early wins.

Further reading and references:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Datadog Migration Resources](https://docs.datadoghq.com/) (for tool-specific guidance)
* [Terraform Registry](https://registry.terraform.io/) (example for automation modules)

That concludes this material. Use this guidance to plan a safer, more predictable migration that preserves visibility, supports users, and meets compliance needs.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/52685b0c-fc05-4f88-ab43-e33e0b562b94)
