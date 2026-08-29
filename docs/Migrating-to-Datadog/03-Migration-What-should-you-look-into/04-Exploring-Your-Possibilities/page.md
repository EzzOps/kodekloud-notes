# Exploring Your Possibilities

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-What-should-you-look-into/Exploring-Your-Possibilities/page

Guidance for handling nonideal platform migrations including parallel legacy operation, missing features, stakeholder alignment, evaluating extended support, integrations, third-party tools, custom builds, and cutover planning

Migrations rarely follow a perfectly linear path. This lesson covers common non-ideal scenarios you may encounter and provides practical strategies to manage them. After reviewing ideal “happy-path” options, you should be prepared to handle parallel legacy systems, missing features on the new platform, and the trade-offs between extended vendor support, integrations, third-party tools, and custom builds.

## When you can’t fully retire the legacy system

Some migrations require the legacy platform to remain operational for a transition period. Typical reasons:

* Limited engineering capacity or competing priorities delay migration work.
* Critical integrations or capabilities don’t yet exist on the new platform.
* Regulatory or compliance constraints require a gradual cutover.

Key actions to operate legacy and new systems safely in parallel:

* Assign a small, dedicated engineering team to maintain the legacy environment — handling incidents, critical fixes, and any emergency updates.
* Continue applying security and functional patches until the legacy system is fully retired.
* Track the legacy product’s end-of-life (EOL) schedule and plan either migration, vendor extended support, or formal risk acceptance.

<Frame>
  <img alt="The image shows a diagram with two solutions: delegating engineers to handle updates and incidents, and keeping patches up-to-date until migration or accepting legacy risks." />
</Frame>

When the legacy platform reaches EOL, your organization must choose one of the following:

* Invest the resources to complete a migration before support ends.
* Purchase vendor extended support (if available) to buy time at additional cost.
* Accept the operational and security risks associated with running an unsupported system.

In many cases, maintaining a legacy system long-term is more expensive than building a targeted integration to the new platform. Evaluate total cost of ownership and operational risk when deciding between continued legacy support and integration work.

## Managing stakeholder alignment and operations

Engage support, operations, and security teams early in the migration and any interim coexistence plan. Early involvement reduces surprises during cutover and ensures playbooks, runbooks, and incident-response processes are updated for both environments.

<Frame>
  <img alt="The image presents a diagram outlining multiple solutions for managing legacy systems, including delegating engineers, keeping patches updated, extending support, and custom integrations. Each solution is accompanied by a brief description." />
</Frame>

## What to do when a required feature is missing

Before committing to a custom solution, validate the vendor’s roadmap and talk directly with sales or product teams — the capability you need might be in development or slated for general availability soon. This step can save significant time and cost.

If the feature is not planned or on a distant timeline, follow a structured evaluation:

* Survey the market for third-party tools that provide the feature.
* Speak with engineers at similar companies for real-world feedback.
* Run focused proofs of concept (PoCs) to validate functionality, performance, and operational fit.
* Evaluate pricing and long-term maintenance implications.

## Compare your options

Use the following guide when weighing extended support, integrations, third-party tools, and custom builds.

| Option                      | Best for                                                | Pros                                                         | Cons                                                        |
| --------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| Extended vendor support     | Short-term buy time to migrate                          | Buys time; vendor authors fixes                              | Higher cost; limited lifetime                               |
| Build a focused integration | Bridge a gap quickly without full custom system         | Lower long-term maintenance than full custom; targeted scope | Requires engineering time; may need ongoing updates         |
| Buy a third-party tool      | Mature functionality that integrates with your platform | Faster time-to-value; vendor support                         | Licensing cost; potential integration drift                 |
| Build custom in-house       | Unique needs that no vendor meets                       | Full control of features and roadmap                         | High development & maintenance cost; risk of long-term debt |

> **lightbulb** When evaluating options, compare total cost of ownership, time-to-value, operational risk, and the long-term maintenance burden. Prioritize solutions that reduce technical debt and align with available engineering resources.

## Quick migration checklist

* Assign a legacy-maintenance team and define responsibilities.
* Confirm EOL dates and vendor support options.
* Validate vendor roadmap and escalate feature asks when appropriate.
* Run PoCs for third-party tools and integrations.
* Produce an operations and incident-response runbook covering both legacy and new platforms.
* Create a measurable cutover plan with rollback criteria.

## Links and references

* [Datadog Documentation](https://docs.datadoghq.com/)
* Vendor roadmap and support pages (contact your vendor representative for roadmap details)
* Guides on building integrations and evaluating PoCs (search vendor or community resources for examples)

That’s it for this lesson. I hope you found it helpful.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/d7aaa833-22da-4f94-af5c-5d196f04ab31/lesson/0f796eb4-aef7-44fd-bc58-4ce9890d3a41)
