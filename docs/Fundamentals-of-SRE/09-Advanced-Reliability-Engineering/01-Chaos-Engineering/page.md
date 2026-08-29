# Chaos Engineering

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Advanced-Reliability-Engineering/Chaos-Engineering/page

Chaos Engineering using controlled failure experiments to reveal hidden system weaknesses, improve resilience, and build operational confidence while practicing safe, observable, reversible tests

Welcome to the Advanced Reliability Engineering module.

This lesson expands on reliability fundamentals with a practical introduction to Chaos Engineering and the cost of reliability. It’s not an exhaustive catalog of tools or configurations; instead, it focuses on the concepts and practices that matter when operating at scale—how to find hidden failure modes and build repeatable, safe experiments that increase system confidence.

<Frame>
  <img alt="A presentation slide titled &#x22;Advanced Reliability Engineering&#x22; featuring two panels: &#x22;Chaos Engineering — Relevant at large-scale orgs&#x22; and &#x22;Cost of Reliability — Links engineering decisions to business impact.&#x22; A caption below reads, &#x22;An expansion of fundamentals to broaden your SRE perspective, not daily details.&#x22;" />
</Frame>

## What is Chaos Engineering?

Traditionally, teams measure and fix systems after incidents occur. Chaos Engineering flips that process: it treats failures as hypotheses to test. Instead of hoping systems will behave under stress, you run controlled experiments—often in production-like environments—to discover weaknesses before customers notice. Large organizations (for example, Netflix and Amazon) use chaos experiments to gain confidence that systems will recover automatically during real outages.

<Frame>
  <img alt="A presentation slide titled &#x22;Chaos Engineering&#x22; showing a central blue circle and icons/text comparing &#x22;System Weaknesses&#x22; (failures impact user experience) on the left with &#x22;System Confidence&#x22; (systems handle outages effectively) on the right. It notes practices like intentionally introducing system failures to identify vulnerabilities before users are affected." />
</Frame>

Chaos Engineering is not “breaking things for fun.” It’s a scientific practice: define a hypothesis about system behavior, inject a controlled failure, measure outcomes against success criteria, and iterate. When teams automate experiments and instrument systems well, incident response improves—teams learn which automated remediations and fallback behaviors actually work.

<Frame>
  <img alt="A presentation slide titled &#x22;Chaos Engineering&#x22; showing a laptop with a gear on its screen and an overlaid warning triangle. To the right are icons labeled &#x22;Worst Moments&#x22; and &#x22;Unexpected Failures,&#x22; and the caption reads &#x22;Your systems WILL FAIL—the question is when.&#x22;" />
</Frame>

The reality is simple: your system will fail. Failures often happen at high-impact moments—product launches, peak shopping periods, or off-hours—and the most damaging ones are unpredictable. Chaos Engineering provides a way to stress the system, reveal hidden weaknesses, and build mitigations before those chaotic moments arrive.

<Frame>
  <img alt="A slide titled &#x22;Chaos Engineering&#x22; that contrasts traditional testing (shown as a fire drill) with chaos engineering (shown as an actual building fire). It uses colored arrows and short text to say traditional testing verifies ideal conditions while chaos engineering validates behavior under real-world chaos." />
</Frame>

## Resilient testing vs. Chaos Engineering

Resilient testing and chaos engineering complement each other. Use resilient testing to verify expected behaviors, and use chaos engineering to discover unknown failure modes.

|          Practice | Goal                                | Typical Examples                                                                                                   |
| ----------------: | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Resilient testing | Verification of known failure modes | Kill a pod to verify failover; disconnect a DB to test fallback; simulate latency to check timeouts                |
| Chaos Engineering | Discovery of unknown failures       | Random network partitions under peak load; memory pressure causing DB slowdown; multiple small faults that cascade |

<Frame>
  <img alt="A presentation slide titled &#x22;Resilience Testing vs Chaos&#x22; showing a &#x22;Resilience Testing&#x22; panel with three bullet points: &#x22;Kill a pod to verify failover works,&#x22; &#x22;Disconnect database to check fallback,&#x22; and &#x22;Simulate latency to test timeouts.&#x22; The slide is © KodeKloud." />
</Frame>

Mindset difference:

* Resilient testing = verification: confirm designed behaviors under known conditions.
* Chaos Engineering = discovery: introduce unexpected or compound failures to learn about previously unseen modes.

<Frame>
  <img alt="A presentation slide titled &#x22;Resilience Testing vs Chaos&#x22; highlighting &#x22;Chaos Engineering&#x22; with bullets: random network partitions during peak traffic, memory pressure with database slowdown, and multiple small failures cascading into big ones. The slide has a purple header and a © KodeKloud copyright notice." />
</Frame>

Both approaches are necessary: verification proves your designs, chaos finds the gaps.

<Frame>
  <img alt="A presentation slide contrasting &#x22;Resilience Testing&#x22; (proves designs work) with &#x22;Chaos Engineering&#x22; (reveals hidden weaknesses). It notes that Netflix moved from resilience testing to chaos engineering after unpredictable outages and shows the Netflix logo." />
</Frame>

## How to run chaos experiments safely

A safe rollout follows a gradual progression from low-risk environments to production canaries:

| Phase                         | Environment                                              | Scope / Risk                                                |
| ----------------------------- | -------------------------------------------------------- | ----------------------------------------------------------- |
| Phase 1 — Development         | Developer machines / local env                           | Affects only developers; lowest risk                        |
| Phase 2 — Staging             | Staging environment that mirrors production              | Safe replica for broader tests                              |
| Phase 3 — Production canaries | Small subset of production (e.g., 1% of servers/traffic) | Minimal user impact if something goes wrong                 |
| Phase 4 — Gradual expansion   | Progressive increase after validating safety             | Grow scope only after observability and rollback are proven |

Start small, limit risk, and expand only after observing expected behavior.

<Frame>
  <img alt="A presentation slide titled &#x22;Running Safe Chaos Experiments&#x22; showing a four-step rollout (1: Development environment, 2: Staging environment, 3: Production (canary), 4: Production (expanded)) with brief test actions and risk scopes under each step. A banner reads &#x22;Start Small, Think Big&#x22; and each step notes the target audience or exposure level (only developers to broader but controlled)." />
</Frame>

A safe chaos experiment follows a clear, repeatable sequence:

1. Define a hypothesis (what you expect to happen).
2. Set the blast radius (who or what is affected).
3. Establish success criteria and metrics.
4. Plan rollback and communication paths.
5. Execute the experiment.
6. Monitor real-time metrics and alerts.
7. Evaluate results and iterate.

<Frame>
  <img alt="A slide titled &#x22;Running Safe Chaos Experiments&#x22; showing a nine-step &#x22;Experiment Execution Sequence.&#x22; It lists steps from defining a hypothesis and setting a blast radius to executing the experiment, monitoring the system, evaluating results, and rolling back if needed." />
</Frame>

## Guardrails — keep experiments controlled

Common safety measures:

| Guardrail     | Recommendation                                            |
| ------------- | --------------------------------------------------------- |
| Blast radius  | Keep it small—common rule of thumb ≤ 10% of capacity      |
| Time limits   | Run experiments for minutes, not hours                    |
| Kill switch   | Always have an immediate rollback or automated cutoff     |
| Monitoring    | Instrument with clear metrics, dashboards, and alerts     |
| Communication | Notify stakeholders before, during, and after experiments |

<Frame>
  <img alt="A slide titled &#x22;Running Safe Chaos Experiments&#x22; that lists five experiment safety measures. The measures are Blast Radius, Time Limits, Kill Switch, Monitoring, and Communication, each with a brief description." />
</Frame>

> **lightbulb** Design experiments to be reversible, observable, and time-bounded. If you can’t observe the impact or rollback quickly, pause the experiment until those controls exist.

> **warning** Never run an experiment without a tested kill switch and real-time monitoring. Unobserved or irreversible tests can create major outages.

These guardrails separate disciplined chaos from reckless disruption. Instrumentation, observability, and communication are prerequisites—not optional extras.

## Real-world origin: Netflix and Chaos Monkey

Netflix’s migration to AWS exposed production failures that weren’t reproducible in traditional tests. In response, they created [Chaos Monkey](https://github.com/Netflix/chaosmonkey), a tool that randomly terminated instances during business hours to force teams to build services that recover automatically.

<Frame>
  <img alt="A slide titled &#x22;Real-World Example - Netflix&#x22; showing the Chaos Monkey logo in the center with an alert labeled &#x22;Production failures.&#x22; It also shows a &#x22;Data centers&#x22; icon on the left and an &#x22;aws&#x22; icon on the right with the caption &#x22;Pull the plug.&#x22;" />
</Frame>

The cultural shift was significant: engineers began designing services explicitly to tolerate failures rather than being surprised by them. Netflix expanded Chaos Monkey into a broader “[Simian Army](https://github.com/Netflix/SimianArmy)” that tests instances, networking, security, and data reliability. Over time, chaos experiments helped prevent more outages than they caused.

<Frame>
  <img alt="A horizontal timeline infographic titled &#x22;Real-World Example – Netflix: The Results&#x22; with colored chevron arrows marking milestones from 2010 to 2020 (e.g., 2010 Chaos Monkey finds failures; 2012 Simian Army expands; 2014 Chaos prevents outages; 2016 survives AWS outage; 2020 99.97% uptime)." />
</Frame>

Key outcomes from Netflix’s experience:

1. Chaos reveals problems that traditional testing misses.
2. Small, controlled failures reduce the risk of large uncontrolled outages.
3. Regular experiments build engineering confidence—teams stop fear-driven avoidance of production.
4. The best experiments are invisible to users: customers don’t notice, but systems become more robust.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example – Netflix: Key Insights&#x22; with a lightbulb graphic. It lists four numbered chaos-engineering takeaways: chaos reveals real problems, small controlled failures prevent big ones, chaos builds engineer confidence, and the best experiments are invisible to users." />
</Frame>

## Operational principles and maturity

Netflix codified several operational principles to make chaos practical:

* Run chaos during business hours (failures happen then).
* Integrate chaos into deployment pipelines.
* Treat chaos as a continuous practice, not a one-off stunt.
* Measure everything—without metrics you cannot build confidence.

<Frame>
  <img alt="A slide titled &#x22;Real-World Example – Netflix Chaos Principles&#x22; showing four numbered cards with guidelines: run chaos during business hours; make chaos part of every deployment; treat chaos as a practice, not an event; and measure everything. The slide includes a © Copyright KodeKloud notice." />
</Frame>

Netflix’s chaos maturity model gives teams a path from manual experiments to a resilience-driven culture:

| Level | Name             | Description                                    |
| ----: | ---------------- | ---------------------------------------------- |
|     1 | Manual chaos     | Engineers trigger failures by hand             |
|     2 | Automated chaos  | Tools inject failures automatically            |
|     3 | Continuous chaos | Experiments run as part of daily operations    |
|     4 | Chaos as code    | Tests are versioned and integrated into CI/CD  |
|     5 | Chaos culture    | Resilience thinking is embedded across the org |

<Frame>
  <img alt="A colorful five-level pyramid titled &#x22;Real-World Example – Netflix: Chaos Maturity Model&#x22; with tiers labeled from Level 1: Manual chaos (top) down to Level 5: Chaos culture (base). Each layer is a different color and represents increasing chaos-maturity stages." />
</Frame>

Advancing maturity means shifting from ad hoc experiments to measurable, repeatable practices that are part of standard engineering workflows.

## Summary

Chaos Engineering is a disciplined, scientific practice for discovering failure modes and improving resilience. When done safely—using small blast radii, defined hypotheses, strong observability, and tested rollback plans—chaos experiments become a powerful tool to reduce outage risk and raise operational confidence.

A related advanced topic is the trade-off between cost efficiency and reliability, which ties engineering decisions to business impact and requires its own set of practices and measurements.

## Links and References

* [Chaos Monkey (Netflix) — GitHub](https://github.com/Netflix/chaosmonkey)
* [Simian Army (Netflix) — GitHub](https://github.com/Netflix/SimianArmy)
* [Kubernetes Documentation — Basics & Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Chaos Engineering resources — Principles and best practices](https://principlesofchaos.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/a99a992c-6f58-4523-9167-833ab08686dc/lesson/07437622-457c-4de8-a6b0-b373b68209e1)
