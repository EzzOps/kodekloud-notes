# Lessons Learned

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Lessons-Learned/page

Pre-migration lessons for moving to Datadog — check compatibility, confirm account feature availability, and improve cross functional communication to avoid delays and rework.

To close, here are practical lessons learned from the pre-migration phase of a Datadog migration. You’ve completed the first and most important step—mapping every critical part of your environment. With that visibility, the heavy planning is done and you can now begin the migration into [Datadog](https://www.datadoghq.com). Before you start, apply these lessons to avoid common pitfalls.

## 1. Verify compatibility before committing to dates

Compatibility checks are a gating factor. Confirm that every component you plan to migrate is supported by your target technology stack. Teams often run older language runtimes, unsupported OS versions, or legacy libraries that require upgrades before they can be connected to Datadog agents or integrations. Identifying these gaps early prevents schedule slips and difficult conversations with stakeholders.

<Callout icon="lightbulb">
  Before announcing timelines, run a compatibility audit across languages, frameworks, agents, and any integration points. Document components that require upgrades, replacements, or configuration changes so deadlines are realistic.
</Callout>

## 2. Confirm Datadog feature availability for your account

Datadog is feature-rich, but not all features are bundled into every plan. Coordinate with procurement, billing, or platform owners to verify which Datadog capabilities are included in your subscription. Designing solutions around unavailable features results in rework and missed deadlines.

At one point in my project I designed a logging solution that depended on a Datadog capability we didn’t have. When I discovered the gap, I had to revise the schedule and present a new plan to leadership—an avoidable delay.

<Callout icon="warning">
  Always validate feature availability with your account manager or procurement team before designing workstreams around specific platform features. Planning for unavailable capabilities causes rework and timeline risk.
</Callout>

<Frame>
  <img alt="The image presents key lessons learned regarding feature usage for Datadog, focusing on understanding package features, avoiding inaccessible features, and maintaining schedules to prevent disappointment." />
</Frame>

## 3. Improve communication channels and cadence

Effective communication reduces surprises. Use at least two channels (for example, Slack and email, or Teams and a shared status board) and keep them active. Create a cross-functional group that includes engineering, SRE, security, and product stakeholders. Schedule a short recurring sync—15 minutes is often sufficient—to report progress and surface blockers.

Keep participants engaged by posting concise status updates, asking for help when needed, and requesting brief reports from key owners. This approach exposes issues earlier and fosters cross-team collaboration, which accelerates migration tasks.

<Frame>
  <img alt="The image summarizes key lessons learned about using multiple communication channels effectively, emphasizing creating groups, frequent messaging, and encouraging collaboration." />
</Frame>

## Quick reference: Lessons and recommended actions

| Lesson                | Why it matters                                      | Recommended action                                                      |
| --------------------- | --------------------------------------------------- | ----------------------------------------------------------------------- |
| Compatibility checks  | Prevents blocked integrations and schedule slips    | Inventory runtimes/libraries and flag unsupported items for upgrade     |
| Feature availability  | Avoids designing around inaccessible capabilities   | Verify account features with procurement/account team before design     |
| Communication cadence | Exposes issues early and keeps stakeholders aligned | Create a cross-functional channel + 15-min weekly sync and status posts |

These adjustments—verifying compatibility, confirming platform features, and improving communication—reduce surprises and keep your migration on track.

With pre-migration complete, you can begin the migration.

<Frame>
  <img alt="The image is a flowchart illustrating a migration process, consisting of three stages: &#x22;Pre-Migration,&#x22; &#x22;Migration,&#x22; and &#x22;Post-Migration.&#x22;" />
</Frame>

Further reading and references

* [Datadog — Official Site](https://www.datadoghq.com)
* [Slack — Messaging for Teams](https://slack.com)
* [Microsoft Teams](https://www.microsoft.com/en/microsoft-teams)

That's it. I hope you found it useful.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/8ad4856d-3aff-4380-b379-2445cbd30e0a" />
</CardGroup>
