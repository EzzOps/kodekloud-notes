# The Origin and Evolution of SRE

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Fundamentals-of-SRE/The-Origin-and-Evolution-of-SRE/page

Overview of Site Reliability Engineering history, principles, SLOs and error budgets, Google origins, evolution with DevOps, adoption across industry, and modern trends like cloud native and AI for reliability

Welcome to Module Two. In this lesson we cover the fundamentals of Site Reliability Engineering (SRE), trace its origin at Google, and follow how its practices evolved into the reliability engineering methods used across industry today.

Before SRE, most organizations kept development and operations strictly separated. Development teams prioritized rapid feature delivery with limited production visibility, while operations teams focused on uptime and stability, using manual incident workflows and risk-averse practices. These silos created friction, conflicting incentives, and a lack of shared accountability—problems that magnified as systems scaled.

<Frame>
  <img alt="A slide titled &#x22;The World Before DevOps and SRE&#x22; showing Development Teams on the left and Operations Teams on the right separated by a vertical &#x22;Wall of confusion,&#x22; with bullets noting developers prioritize fast feature delivery and operations focus on uptime and stability." />
</Frame>

Common limitations of traditional IT included:

* Linear, sequential development lifecycles (development → testing → deployment) that slowed delivery and reduced agility.
* Broken feedback loops, where operations rarely gave developers timely, actionable production feedback.
* Poor scalability and adaptability: legacy architectures and manual processes struggled with rapid change and high load.

These issues were often summed up by the classic line: “It works on my machine.”

<Frame>
  <img alt="A presentation slide titled &#x22;Problems Traditional IT Failed to Solve&#x22; showing three numbered panels that list &#x22;Linear Development Cycles,&#x22; &#x22;Broken Feedback Loops,&#x22; and &#x22;Poor Scalability and Adaptability.&#x22; A small colored tag at the bottom reads &#x22;It works on my machine.&#x22;" />
</Frame>

How SRE began at Google

As Google scaled, the operational burden outpaced traditional ops practices. The company responded by applying software engineering discipline to operational problems:

* Hire software engineers to solve operations problems with engineering practices and software tooling.
* Automate manual processes and build internal tools to reduce human toil.
* Embrace measured risk: recognize that 100% uptime is usually infeasible and balance reliability with feature velocity using Service Level Objectives (SLOs) and error budgets.
* Eliminate toil: minimize repetitive manual work so engineers can focus on automation, reliability engineering, and system design.

SRE teams were encouraged to keep toil to no more than \~50% of their time, devoting the remainder to automation, tooling, and building self-healing systems.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;The Birth of SRE at Google&#x22; with a subtitle noting Google's growth outpaced traditional operations. It shows three numbered boxes: &#x22;Hire Software Engineers for Operations,&#x22; &#x22;Embrace Measured Risk,&#x22; and &#x22;Eliminate Toil,&#x22; each with a simple icon." />
</Frame>

Key SRE concepts

One of the most influential ideas SRE introduced is the error budget. Error budgets force teams to answer: What does this system need to do, and how reliable must it be for users? Because 100% SLOs are usually unrealistic, an error budget quantifies acceptable failure and creates a mechanism to balance risk, feature development, and operational effort.

<Frame>
  <img alt="A presentation slide titled &#x22;Key SRE Innovations&#x22; introducing &#x22;The Error Budget Concept&#x22; with an illustration of a person thinking and two prompt questions: &#x22;What does the system need to do?&#x22; and &#x22;How reliable does it really need to be?&#x22; It also notes that since 100% SLOs aren't realistic, error budgets help manage risk." />
</Frame>

> **lightbulb** Error budgets are operational levers: if the budget is exhausted, teams throttle risky releases and prioritize remediation; if budget remains, teams can accelerate feature work. Use error budgets to align product and reliability goals.

SRE also reframed reliability as a product feature—service-level engineering. Instead of measuring only infrastructure metrics, SRE focuses on user-facing behaviour and experience, shifting culture from reactive firefighting to proactive engineering, observability, and design.

<Frame>
  <img alt="A presentation slide titled &#x22;Key SRE Innovations&#x22; highlighting &#x22;Service-Level Engineering.&#x22; It lists three points: reframing reliability as a product feature, focusing reliability on users (not just infrastructure), and shifting from reactive to proactive work." />
</Frame>

SRE vs. DevOps: evolution and relationship

Starting from traditional operations (stability-focused and manual), the DevOps movement pushed for breaking down silos, increasing automation, and improving collaboration. SRE evolved in parallel: it formalized reliability through SLOs and error budgets, reduced toil, and introduced explicit engineering roles focused on measurable outcomes. In practice, organizations often blend DevOps culture (shared responsibility, CI/CD) with SRE engineering practices (SLOs, error budgets, reliability tooling) to get the benefits of both.

<Frame>
  <img alt="A presentation slide titled &#x22;How Did We Get Here?&#x22; showing three boxed stages: Traditional Operations, The DevOps Movement, and The SRE Approach. Each box lists key points — e.g., limited automation and stability focus; breaking down silos and more automation; then engineering-driven, data-driven SRE practices balancing reliability and innovation." />
</Frame>

Principle: Hope is not a strategy

Ben Treynor Sloss’s aphorism, “Hope is not a strategy,” encapsulates SRE’s core idea: reliability must be engineered, measured, and continuously improved—not left to chance. SRE turned reliability into a data-driven discipline and that methodology spread quickly outside Google.

<Frame>
  <img alt="A slide titled &#x22;Why SRE Was Necessary&#x22; showing three colored icons labeled &#x22;Deliberate engineering,&#x22; &#x22;Planning,&#x22; and &#x22;Measurement&#x22; under the line &#x22;They require deliberate engineering, planning, and measurement.&#x22; A footer adds &#x22;SRE was Google's fix: data-driven, deliberate, and widely adopted.&#x22;" />
</Frame>

> **warning** Reliability requires explicit targets, monitoring, and change controls. Don’t treat uptime as an afterthought—define SLOs, track error budgets, and automate rollouts and rollbacks.

SRE timeline (high-level)

<Frame>
  <img alt="A horizontal timeline titled &#x22;The Evolution of Site Reliability Engineering at Google&#x22; showing key SRE milestones from 2003 to post‑2016. It highlights events like the first SRE team founding, SLO introduction, influential publications/conferences, and SRE becoming mainstream and integrating with DevOps." />
</Frame>

| Year / Period | Milestone                                          | Notes                                                                            |
| ------------- | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| Early 2000s   | Google scales rapidly                              | Traditional ops could not keep up; engineering principles applied to operations. |
| 2003          | First official SRE team founded                    | Ben Treynor Sloss formalized the role and charter.                               |
| 2004          | Early high-availability papers                     | Laid the groundwork for SRE practices.                                           |
| 2005          | SLOs introduced                                    | Service-level objectives began to define and measure reliability targets.        |
| 2007–2008     | Public SRE presentations                           | Concepts shared in conferences and talks increased external visibility.          |
| 2016          | Google publishes Site Reliability Engineering book | A foundational, public resource as SRE reached broader adoption.                 |
| Post-2016     | Mainstream adoption                                | Many companies adopted and adapted SRE alongside DevOps.                         |

SRE adoption beyond Google

SRE practices have been adopted and adapted across the industry. Companies such as Netflix, Amazon, Microsoft, LinkedIn, and others tailored SRE to their architectures, scale, and regulatory needs. Sectors including finance, healthcare, education, and government have also embraced SRE—often with stricter compliance and security requirements.

<Frame>
  <img alt="A presentation slide titled &#x22;Spread of SRE Beyond Google&#x22; showing the logos of Netflix, Amazon, LinkedIn, and Microsoft. A caption reads &#x22;Adopted SRE and shaped it to their needs.&#x22;" />
</Frame>

Different organizational approaches

| Company / Model | Approach                                                                                                    |
| --------------- | ----------------------------------------------------------------------------------------------------------- |
| LinkedIn        | Embedded SREs inside product teams to promote developer ownership of reliability.                           |
| Meta            | Production engineering: a hybrid that combines SRE principles with infrastructure/tooling responsibilities. |
| Uber            | Adopted SRE practices to address rapid scaling and large operational complexity.                            |

Modern SRE trends (current and emerging)

* AI/ML for reliability: anomaly detection, predictive analysis, and automation-assisted remediation.
* Cloud-native SRE: containerization, microservices, and orchestrators (e.g., Kubernetes) shaping operational practices.
* Platform engineering: centralized internal platforms that provide reusable tools and abstractions for developers.
* Shift-left reliability: design-for-reliability earlier in development, with testing and observability integrated into CI/CD.
* Cost optimization and FinOps: balancing cloud costs and performance while meeting SLOs.

<Frame>
  <img alt="A presentation slide titled &#x22;Modern SRE Adoption Trends&#x22; showing five trends with icons: Integration of AI and Machine Learning, Cloud-Native SRE, Platform Engineering, Shift-Left Reliability, and Cost Optimization with FinOps. The slide is copyrighted by KodeKloud." />
</Frame>

Why SRE practices matter: a real outage example

Real incidents show the value of the SRE toolkit. On July 19, 2024, a faulty CrowdStrike Falcon sensor update for Windows hosts triggered system crashes (blue screens) across devices that checked in during a short window. An estimated 8.5 million devices were impacted, affecting airlines, healthcare, and other sectors. Recovery required manual remediation steps (safe mode boots, external recovery media), and CrowdStrike reported reaching \~99% restoration after several days. This outage highlights the importance of robust rollout verification, staged deployments, canary releases, and rapid rollback procedures.

Postmortems are a core SRE practice: they document what happened, why it happened, and—critically—what will change to reduce recurrence. Well-written postmortems help teams synthesize insights, share lessons, and turn incidents into improvements.

<Frame>
  <img alt="A presentation slide promoting a post-mortem resource, featuring a blue &#x22;POSTMORTEM&#x22; illustration and a GitHub link. To the right is a dark-themed screenshot of a README titled &#x22;A List of Post-mortems&#x22; with a table of contents and example entries." />
</Frame>

Resources and further reading

* Site Reliability Engineering (book) — [https://sre.google/books/](https://sre.google/books/)
* Collections of public postmortems and incident reports (search GitHub and engineering blogs for “postmortem” and “incident report”)
* DevOps and SRE guidance from cloud providers and standards bodies (e.g., Kubernetes docs, cloud provider reliability guides)

Looking ahead

SRE is expected to continue transforming how enterprises operate. Forecasts suggest increasing SRE adoption across industries, driven by cloud-native architectures, automation, and demands for higher availability and faster delivery. The DevOps market and related tooling will continue to grow, and SRE will keep evolving with AI/ML, platform engineering, and tighter cost-reliability tradeoffs.

Core SRE focus remains unchanged: deliberate engineering, measurable reliability, and continuous learning.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/df29fdca-b56b-4828-a8cc-abd0bb37ed70/lesson/765f6b37-e633-4905-8c80-230e86429f42)
