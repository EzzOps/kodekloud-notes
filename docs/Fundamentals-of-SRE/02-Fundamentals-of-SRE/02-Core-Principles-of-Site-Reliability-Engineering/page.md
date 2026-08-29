# Core Principles of Site Reliability Engineering

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Fundamentals-of-SRE/Core-Principles-of-Site-Reliability-Engineering/page

Overview of core Site Reliability Engineering principles balancing reliability and velocity with SLOs and error budgets, automating toil, investing in observability, fostering blameless learning, and preferring simplicity.

Site Reliability Engineering (SRE) turns reliability into an engineering problem. These core principles are practical rules-of-thumb SRE teams use to design, operate, and evolve reliable systems at scale. Different organizations may phrase them differently, but the concepts below capture what SRE practitioners rely on daily: managing risk, measuring user-facing behavior, reducing manual work, investing in observability, fostering a learning culture, and keeping systems simple.

## Manage risk with error budgets (balance innovation and reliability)

SRE accepts that 100% uptime is impractical and typically too expensive. Instead, teams set Service Level Objectives (SLOs) that define acceptable reliability and use error budgets to quantify allowable failure. When a service is within its error budget, teams can safely ship features; when the budget is spent, the priority shifts to stability and remediation.

<Frame>
  <img alt="A presentation slide titled &#x22;Innovation and Reliability — The Balancing Act&#x22; showing a cartoon person with a giant pencil next to a checklist clipboard and three numbered points about uptime, SLOs, and error budgets." />
</Frame>

## Ask the right questions early (influence design and reduce surprises)

SREs get involved at design and planning stages to influence trade-offs and reduce operational risk. Useful, repeatable questions to ask service owners include:

* How can this service fail?
* How will we detect that it failed?
* What actions must be taken when it fails?
* What context and runbook steps are required to respond effectively?

Clear answers drive better instrumentation, alerting, and runbooks that reduce mean time to resolution (MTTR).

<Frame>
  <img alt="A presentation slide titled &#x22;SRE Is About Asking Questions&#x22; showing a profile-style headshot card on the left and a boxed list on the right with four SRE questions: how it breaks, how you know it broke, what to do when it breaks, and what actions/context are needed to respond effectively." />
</Frame>

## Measure reliability: the SLI → SLO → SLA model

SRE quantifies reliability with a three-part model:

* Service Level Indicators (SLIs): metrics that reflect user experience (latency, error rate, availability).
* Service Level Objectives (SLOs): internal targets for SLIs that guide trade-offs.
* Service Level Agreements (SLAs): external, contractual commitments tied to customer expectations or penalties.

Use SLIs that map to user experience, set realistic SLOs, and reserve SLAs for formal commitments.

<Frame>
  <img alt="A presentation slide titled &#x22;The SLI/SLO/SLA Framework&#x22; showing that SRE aligns technical performance (gauge icon) to end-user experience (thumbs-up and stars) with a rightward arrow. The slide includes a short caption about quantifying reliability and a copyright notice from KodeKloud." />
</Frame>

| Resource | Purpose                              | Example SLI                                    |
| -------- | ------------------------------------ | ---------------------------------------------- |
| SLI      | Measures user-facing behavior        | 99th percentile request latency                |
| SLO      | Target for an SLI over a time window | 99.9% successful responses per month           |
| SLA      | Customer-facing contract             | 99.95% uptime with financial credits on breach |

> **lightbulb** Use SLIs to reflect actual user experience, and let SLOs guide trade-offs between feature velocity and reliability—this is what the error budget enforces.

<Frame>
  <img alt="A presentation slide titled &#x22;The SLI/SLO/SLA Framework&#x22; showing three best-practice tips. It advises tracking SLIs that matter to users, using percentiles (e.g., 99th) instead of averages, and revisiting/adjusting SLOs as systems and user expectations evolve." />
</Frame>

## Eliminate toil through automation (free time for engineering)

Toil is manual, repetitive work that scales with the system and yields little long-term value. SREs aim to automate recurring operational tasks—backups, routine incident tasks, and deployment steps—to reduce toil and free engineers for design and reliability improvements. A common target is to keep toil below 50% of SRE time to maintain capacity for engineering work.

Automation is iterative: automating tasks reveals deeper system behaviors and drives further automation opportunities.

<Frame>
  <img alt="A slide titled &#x22;Eliminating Toil Through Automation&#x22; that defines toil as manual, repetitive work and lists points about it. To the left is an illustration of a person on a ladder adjusting large gears alongside an hourglass and books." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Eliminating Toil Through Automation&#x22; listing three points: automate recurring tasks, aim to keep toil under 50% of an SRE's time, and free engineers for high-value work. The footer adds &#x22;Toil is a tax on your time and morale.&#x22;" />
</Frame>

> **warning** Automate thoughtfully. Blind automation of poorly understood processes can create hard-to-debug failures. Ensure automation is observable, tested, and reversible.

## Invest in monitoring and observability (see how systems behave in production)

Monitoring shows how systems actually behave under real load. Focus on symptoms (what the user experiences) as well as causes, and prioritize observable signals that map to user impact.

A practical starting point is Google's four golden signals: latency, traffic, errors, and saturation. Measure the right things—if you don't measure them, you can't improve them.

<Frame>
  <img alt="The image titled &#x22;Monitoring and Observability&#x22; shows an illustrated developer working on a laptop on the left and, on the right, an SRE-like figure examining monitoring dashboards and charts on a large screen. Captions note that developers design how applications should behave, while SREs rely on monitoring to see real performance." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Monitoring and Observability&#x22; showing three colorful triangular icons arranged in a triangle under the heading &#x22;Core concepts.&#x22; The slide includes the phrases &#x22;Monitor symptoms, not just causes&#x22; and &#x22;Observe from the user's perspective,&#x22; with a © Copyright KodeKloud note." />
</Frame>

## Foster a blameless culture (enable learning and improvement)

Psychological safety is a prerequisite for learning. Blameless postmortems focus on system and process weaknesses rather than individual fault. This encourages open knowledge sharing, surfaces systemic fixes, and reduces repeat incidents.

Look to other safety-critical industries (e.g., aviation) for proven incident investigation and learning practices.

<Frame>
  <img alt="A slide titled &#x22;Blameless Culture&#x22; showing three people assembling large puzzle pieces alongside three cultural norms about focusing on how failures happened, conducting blameless postmortems, and encouraging open sharing of lessons. The header reads &#x22;Psychological safety precedes learning.&#x22;" />
</Frame>

## Prefer simplicity (reduce failure modes and speed recovery)

Simple systems are easier to reason about, fail less often, and recover more quickly. Simplicity means avoiding unnecessary complexity, preferring composition over reinvention, and evaluating design decisions from the user's perspective.

Simplicity improves safety for change and makes incident response more effective.

<Frame>
  <img alt="A presentation slide titled &#x22;Simplicity&#x22; with the subtitle &#x22;Simple systems fail less and recover faster.&#x22; It lists four points: 01 Simplicity enables change, 02 Simplicity aids in debugging and incident response, 03 Composition over reinvention, and 04 Define simplicity by the user's perspective." />
</Frame>

## Summary — how these principles work together

These core principles are not isolated rules; they form a coherent approach:

* Use SLOs and error budgets to balance reliability with product velocity.
* Instrument systems and ask the questions that reveal failure modes.
* Automate routine work to focus on engineering improvements.
* Observe production using meaningful SLIs and the four golden signals.
* Build a blameless culture to learn from failures.
* Keep architecture and operational practices simple.

Apply these principles iteratively to improve reliability, reduce operational risk, and keep teams productive.

Key resources and further reading:

* [Google SRE Book — Monitoring Distributed Systems (Four Golden Signals)](https://sre.google/sre-book/monitoring-distributed-systems/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)

Key takeaways:

* Define SLIs that matter to users, set SLOs to guide priorities, and treat SLAs as contractual obligations.
* Keep toil low through deliberate automation and make automation observable and reversible.
* Monitor symptoms from the user's point of view and cultivate a blameless culture for continuous improvement.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/df29fdca-b56b-4828-a8cc-abd0bb37ed70/lesson/51b3cafa-2e09-42e0-9189-1ea9cb6653bf)
