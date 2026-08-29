# Learned lessons

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Learned-lessons/page

Practical lessons for planning and executing system migrations focusing on scope control, contingency, early escalation, and stakeholder visibility.

In this lesson I share practical lessons learned from migration projects that can help you save time and avoid common pitfalls.

Migration is often the most challenging phase of a project. Deadlines, a steep learning curve, parallel workstreams, production incidents, training, reporting, and legacy orchestration can quickly overwhelm teams if not managed. Below are the key takeaways I wish I'd applied sooner — phrased as concrete actions you can adopt immediately.

* Allow for a bigger delivery window\
  Add contingency—days or even weeks—beyond your optimistic estimate. Even with careful risk mapping, unexpected problems will surface. Build buffer into your schedule, include time for discovery spikes, and explicitly define rollback and mitigation plans before you start.

* Prevent migration scope creep\
  Maintain a documented migration scope and an explicit inventory of systems, services, and observability components to migrate. Assign an owner for each item and use a checklist with clear acceptance criteria so nothing gets left behind. Regularly confirm scope with both engineers and their managers.

* Escalate crucial issues early\
  If you hit blockers outside your team’s control, escalate immediately. Engage management to resolve cross-team dependencies, resource constraints, or organizational blockers. Let managers handle political negotiations so engineers can focus on execution.

* Provide and maintain visibility\
  Share regular status updates (progress, blocked items, risks) with stakeholders and managers. Provide dashboards or tracking boards so everyone sees the same information. Proactive visibility reduces miscommunication and prevents last-minute surprises.

<Frame>
  <img alt="The image lists four learned lessons: allowing for bigger delivery time, ensuring migration control, escalating crucial issues, and providing visibility, each with a brief explanation." />
</Frame>

Keep stakeholders posted on progress and on items blocking you. Frequent, concise updates reduce friction and help managers prioritize or resolve issues that impact delivery.

| Lesson                             | Why it matters                                                             | Practical steps                                                               |
| ---------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Allow for a bigger delivery window | Unforeseen technical and organizational risks are common in migration work | Add contingency time, plan discovery spikes, and document rollback strategies |
| Prevent migration scope creep      | Untracked components create post-migration firefights and gaps             | Create a migration inventory, assign owners, and use acceptance checklists    |
| Escalate crucial issues early      | Cross-team dependencies can block progress and delay go-lives              | Escalate blockers to managers immediately and track resolution SLAs           |
| Provide and maintain visibility    | Lack of shared context breeds confusion and last-minute issues             | Use dashboards, regular status updates, and an agreed-upon escalation path    |

<Callout icon="lightbulb">
  A consistent communication strategy—regular updates, clear owners, and a documented scope—resolves most common migration problems before they escalate.
</Callout>

Action checklist (quick reference)

* Define migration scope and inventory before kickoff.
* Assign owners and acceptance criteria for each component.
* Build contingency into timelines and plan rollback paths.
* Establish an escalation path and involve management for cross-team issues.
* Publish a single source of truth (dashboard or tracking board) and send concise, regular updates.

Further reading and references

* [Change management & migration practices — Atlassian](https://www.atlassian.com/team-playbook/change-management)
* [Cloud migration strategies — AWS](https://aws.amazon.com/cloud-migration/)
* [Runbooks and incident playbooks — Google SRE guidance](https://sre.google/sre-book/incident-response/)

That's it — these are the core lessons learned from migration work. With good planning, disciplined communication, and clear ownership, most of these issues are avoidable. I hope you found this useful.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/a67ddb0f-7fec-484f-92ea-a9a13eb4df7e" />
</CardGroup>
