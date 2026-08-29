# FinOps Operate Phase

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Inform-Optimize-and-Operate-Phase/FinOps-Operate-Phase/page

Guide to sustaining cloud cost optimizations via continuous FinOps operations, governance, processes, cultural change, and measurement to preserve savings and embed cost accountability across teams.

Welcome back.

The Optimize phase uses measurement and reporting to identify cost reductions. The Operate phase is where those savings are preserved and extended over time. If you stop operating—if cost alignment, budgeting, and the processes you created are abandoned—optimization gains often evaporate within months.

This article explains what the Operate phase does, how it functions, common activities, and typical pitfalls to watch for.

> **lightbulb** The Operate phase is continuous: execute improvements, align business priorities with FinOps practices, and transform culture so cost-conscious behavior becomes part of everyday engineering and product decisions.

## Why the Operate Phase matters

* Optimize implements one-time or periodic improvements.
* Operate continuously runs, measures, enforces, and institutionalizes those improvements so they stick.
* Without Operate, optimizations fade and costs drift upward.

Operate focuses on three core areas:

1. Continuous execution — keep the improvement cycle running.
2. Business-focused plans — make cost outcomes part of organizational priorities and roadmaps.
3. Cultural transformation — embed accountability and collaboration across teams so FinOps becomes how teams work, not an extra task.

<Frame>
  <img alt="The image outlines the &#x22;Operate Phase,&#x22; focusing on Execution Phase, Business-focused Phase, and Culture Transformation, emphasizing organizational change and team accountability." />
</Frame>

## Operate as a cycle: collaborative, iterative, process-driven, action-oriented

Think of Operate as a repeating loop of small improvements rather than a single project. The Operate cycle has four defining characteristics:

* Collaborative: Anyone should be able to surface cost issues and propose fixes. For example, an engineer who spots an underutilized EC2 instance — even outside their service boundary — can flag it for remediation.
* Iterative: Make a change, measure the result, incorporate the learning, and repeat. Each iteration refines both controls and outcomes.
* Process-driven: Capture actions in tracked workflows (issue trackers, runbooks), document decisions, and record realized savings so outcomes are auditable and reproducible.
* Action-oriented: Dashboards and alerts provide the signals; Operate is where teams take action on those signals, verify results, and close the feedback loop.

Typical Operate workflow:

1. Detect (alerts / dashboards)
2. Triage (who owns this?)
3. Remediate (apply right-sizing, turn off resources, adjust purchase plans)
4. Verify (measure savings and side-effects)
5. Document & celebrate (update runbooks; share wins)

<Frame>
  <img alt="The image depicts the &#x22;Operate Phase Cycle,&#x22; highlighting a cyclical process with elements of being process-driven, action-oriented, involving collaborative execution, and an iterative approach. Each segment is associated with descriptions like establishing workflows, implementing changes, teamwork, and continuous improvement." />
</Frame>

## Typical Operate-phase responsibilities

If you are part of the FinOps or cloud operations team executing the Operate phase, concentrate on these responsibility areas. The table below summarizes responsibilities, examples, and typical owners.

| Area                               | What to do                                                                                | Example tasks                                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Governance & compliance            | Define rules, guardrails, and approval flows so cost controls are effective and secure    | Tagging policies, account provisioning rules, cost allocation standards, IAM guardrails         |
| Improvement & training             | Provide onboarding and ongoing education so teams understand and adopt FinOps practices   | New-hire training, monthly refresher sessions, maintain runbooks and playbooks                  |
| Stakeholder engagement & reporting | Keep stakeholders informed and accountable with regular reports and ownership assignments | Monthly cost reviews, ownership for cost anomalies, executive summaries of savings              |
| Operational maintenance            | Day-to-day upkeep to prevent drift and correct issues quickly                             | Fix tags, currency conversions in dashboards, rightsizing, clean up abandoned test environments |

When you capture and publicize improvements (for instance, “Team X saved \$Y this month”), you reinforce the behaviors you want across the organization and increase support for ongoing effort.

> **warning** Operate requires sustained leadership support and visible metrics. Without clear ownership and measurable results, optimizations will erode and teams may deprioritize cost work.

## Common pitfalls in the Operate phase

Operate frequently runs longer than Optimize, and that longevity exposes several hazards:

* Organizational resistance: Interest and alignment can decline as teams shift to feature work. Maintain leadership sponsorship and executive visibility.
* Lack of context: New hires or reorganized teams often don’t inherit FinOps knowledge. Continuous training and accessible documentation are essential.
* Process overload: If FinOps processes are too heavy, engineers will deprioritize them. Keep workflows lightweight and clearly schedule time for cost work.
* Measurement gap: If you cannot reliably measure savings or attribution, you can’t prove what worked. Standardize measurement and attribution practices across the organization.
* Siloed execution: Uncontrolled admin access, shadow accounts, or ad hoc provisioning create hidden costs. Enforce provisioning controls and central visibility to catch these early.

<Frame>
  <img alt="The image illustrates common pitfalls during the &#x22;Operate&#x22; phase, represented as an iceberg with visible and hidden issues, such as implementation issues, organizational resistance, and siloed execution." />
</Frame>

In mature organizations, engineering teams usually bake FinOps tasks into regular development work: tagging and tracking resources, rightsizing, managing savings plans or reservations, and being accountable for the cost posture of their services. The key distinction is that these actions are part of day-to-day responsibilities, not a separate “cost project.”

## Practical checklist for Operate

* Establish and publish runbooks for common remediations.
* Assign cost owners for every major service or account.
* Automate detection and remediation where safe (e.g., scheduled shutdowns, rightsizing suggestions).
* Standardize measurement and attribution for all optimizations.
* Schedule recurring training and a quarterly review cadence.
* Celebrate and communicate savings and improvements organization-wide.

## Links and references

* [FinOps Foundation](https://www.finops.org/)
* [Cloud Cost Management best practices (AWS)](https://aws.amazon.com/answers/account-management/aws-cost-optimization/)
* [Cloud Cost Management guides (GCP)](https://cloud.google.com/architecture/operational-best-practices-for-managing-gcp-budgets)
* [Cloud Cost Management (Azure)](https://learn.microsoft.com/azure/cost-management-billing/)

That concludes this lesson on the Operate phase.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/5dec4577-7276-4a7a-8040-c172cd00f341/lesson/cd7d77cf-2c89-4236-a48d-78443348553a)
