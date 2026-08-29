# Pseudocode: simple circuit breaker logic (illustrative)
class CircuitBreaker:
    def __init__(self, failure_threshold, timeout_seconds):
        self.failures = 0
        self.state = "CLOSED"
        self.failure_threshold = failure_threshold
        self.open_since = None
        self.timeout_seconds = timeout_seconds

    def record_failure(self):
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            self.open_since = now()

    def reset(self):
        self.failures = 0
        self.state = "CLOSED"
        self.open_since = None

    def is_allowed(self):
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if now() - self.open_since >= self.timeout_seconds:
                self.state = "HALF_OPEN"
                return True  # allow limited requests
            return False
        if self.state == "HALF_OPEN":
            return True  # allow test requests

# Usage:
cb = CircuitBreaker(failure_threshold=5, timeout_seconds=30)
if cb.is_allowed():
    try:
        response = call_dependency()
        cb.reset()
    except Exception:
        cb.record_failure()
        return fallback_response()
else:
    return fallback_response()
```

Fallbacks and graceful degradation

Fallbacks offer alternative behaviors when dependencies fail so your service can preserve core value. Key concepts:

* Graceful degradation — keep core functionality even if enhancements fail.
* Partial availability — serve essential data or simplified UI.
* Functional core vs enhancement shell — separate must-haves from optional features.
* Progressive enhancement — enable extras only when resources permit.

Common fallbacks:

* Return cached data when a backend is unavailable.
* Provide simplified functionality or default values.
* Queue work for later processing (retry/queueing).
* Route to manual processes or notifications when automation fails.

<Frame>
  <img alt="A presentation slide titled &#x22;Fallbacks and Graceful Degradation&#x22; that shows four colored panels describing strategies—Graceful Degradation, Partial Availability, Functional Core vs Enhancement Shell, and Progressive Enhancement—with short definitions. It outlines approaches for keeping services functioning or degrading gracefully when parts of a system fail." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Fallbacks and Graceful Degradation&#x22; showing a service that can't reach a dependency and routes to an &#x22;Alternative behavior&#x22; box. The alternative then branches to options like cached data, simplified functionality, default values, queue for later, and manual processing." />
</Frame>

Bulkheads

Bulkheads isolate resources and failure domains so problems in one area don’t sink the whole system. Implementations include:

* Separate thread pools for different dependencies.
* Deploying critical functions as independent services.
* Dedicated databases or connection pools by domain.
* Partitioning requests by user type or criticality.

These approaches reduce resource contention and limit blast radius.

<Frame>
  <img alt="A presentation slide titled &#x22;Dependency Management Strategies&#x22; that lists four bulkhead implementation options: Separate Thread Pools, Separate Services, Separate Databases, and Request Partitioning, each with a short description and circular icon. The items are arranged horizontally with simple line art and brief explanatory text." />
</Frame>

Benefits of bulkheads:

* Prevents resource exhaustion from spreading.
* Allows partial system functionality during outages.
* Creates clear isolation boundaries.
* Simplifies testing and deployment and improves overall resilience.

<Frame>
  <img alt="A presentation slide titled &#x22;Dependency Management Strategies&#x22; showing a circular &#x22;Benefits of Bulkheads&#x22; graphic connected to four labeled boxes. The boxes list: prevents resource exhaustion from spreading; allows partial system functionality during failures; creates clear isolation boundaries; and simplifies testing and deployment." />
</Frame>

Bulkhead examples:

* Separate task queues for different workloads.
* Independent connection pools per domain or service.
* Per‑dependency resource limits (CPU, threads).
* Isolated failure domains for critical vs non‑critical services.

Real‑world example: Amazon S3 outage (Feb 28, 2017)

What happened: an engineer debugging a billing issue executed a command intended to remove a small set of servers from an S3 subsystem. Due to incorrect input, a much larger set was removed. The removal forced two critical subsystems (index and placement) to restart, making S3 unavailable in the US‑East‑1 region for about 3.5 hours. The outage’s blast radius extended to services that relied on S3 metadata and storage.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example: Amazon's 2017 S3 Outage&#x22; showing the Amazon S3 logo, two short text callouts describing an engineer debugging a billing issue, and a cartoon of a person working at a desk with a computer." />
</Frame>

<Frame>
  <img alt="A presentation slide about Amazon's 2017 S3 outage showing two critical subsystems. The &#x22;Index Subsystem&#x22; manages metadata and locations for S3 objects (for GET, LIST, PUT, DELETE) and the &#x22;Placement Subsystem&#x22; handles storage for new objects, relying on the index." />
</Frame>

Removing significant capacity forced a full restart and caused S3 to be unavailable for approximately 3.5 hours. The outage affected multiple AWS services that depended on S3.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example: Amazon's 2017 S3 Outage&#x22; with a computer icon showing a circular restart symbol. The caption explains that removing capacity forced a full restart and caused S3 to be unavailable for about 3.5 hours in the US‑EAST‑1 region." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example: Amazon's 2017 S3 Outage&#x22; with the subheading &#x22;For reaching blast radius&#x22; and three AWS service icons labeled Amazon EC2, Amazon EBS, and AWS Lambda. It appears to illustrate which services were in the outage's blast radius." />
</Frame>

Lessons learned and mitigations

Even mature systems are vulnerable to simple human error. Amazon implemented several mitigations after the incident:

* Throttle capacity-removal operations to avoid large accidental removals.
* Add safeguards to block removals that would violate minimum capacity rules.
* Improve operational tooling and guardrails to reduce human error.
* Strengthen dashboards and health checks for faster, safer recovery.
* Harden dependency and failover management to reduce blast radius.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example: Amazon's 2017 S3 Outage&#x22; noting that human error can cause large-scale outages. It lists two fixes Amazon made: remove capacity more slowly, and add safeguards to block removals below minimum capacity." />
</Frame>

Wrap up

Managing dependencies requires deliberate mapping, prioritization, and design for failure. Apply these steps:

* Map dependencies and classify them by criticality and blast radius.
* Prioritize investments where risk and impact are highest.
* Use patterns—circuit breakers, fallbacks, bulkheads, graceful degradation—to contain failures.
* Automate guards and deploy operational tooling and observability to detect and recover quickly.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example: Amazon's 2017 S3 Outage.&#x22; It shows a horizontal sequence of colored arrows illustrating major changes like improved operational safety, faster safer recovery, a more resilient service health dashboard, and stronger dependency/failover management." />
</Frame>

In the next lesson, we'll explore change management and safe deployment practices.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/5863d35a-6f2f-4453-9961-85eeb243c287/lesson/0dd159f9-6b6b-4048-9808-c48284bf1391" />
</CardGroup>


# Managing Operational Toil

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Managing-Complexity-Risk-and-Toil/Managing-Operational-Toil/page

Describes SRE operational toil, how to identify and measure repetitive manual work, and strategies to eliminate or automate it to improve reliability, team velocity, and reduce costs.

In this lesson we cover operational toil: the manual, repetitive work that keeps systems running but creates no lasting value. Every Site Reliability Engineer (SRE) should be able to identify, measure, and remove toil so teams can focus on engineering improvements rather than constant firefighting.

Toil typically appears as frequent restarts, repeated manual fixes, or routine steps that require human attention. Left unchecked, toil grows with your service and becomes a blocker to reliability, team velocity, and long-term sustainability.

<Frame>
  <img alt="A presentation slide titled &#x22;Toil in SRE&#x22; that defines toil as repetitive manual work that grows with scale and adds no lasting value. Below the text is an illustration of two people arranging cards on a Kanban-style board with gears above it." />
</Frame>

## What is toil?

* In SRE, toil is manual, repetitive operational work that provides no enduring value and tends to increase linearly as a system scales.
* Toil consumes engineer time and energy without improving the system. Without deliberate automation or design changes, toil grows with the service.

## Common signs that work is toil

Look for these characteristics to determine whether a task is toil:

* Requires direct human involvement to execute.
* Repetitive tasks that could be automated.
* No cumulative value — doing it again tomorrow yields the same result.
* Triggered repeatedly by the same conditions or occurs on a schedule.
* Tactical focus: addresses symptoms rather than root causes.
* Workload grows proportionally with the service.

If several of these apply, prioritize addressing the task as toil.

## Concrete examples

* Manual deployment processes with many manual steps or frequent interventions.
* Repetitive alert responses where incidents require the same manual actions.
* Routine configuration changes performed by hand.
* Regular data cleanup tasks conducted manually.
* User access management without self-service tooling.
* Certificate renewals that are not automated.

Ask: Could this be a script, scheduled job, or CI/CD action? Often the answer is yes.

<Frame>
  <img alt="A presentation slide titled &#x22;Toil in SRE.&#x22; It lists examples of operational toil such as manual deployment processes, repetitive alert responses, routine configuration changes, regular data cleanup tasks, user access management, and certificate renewals." />
</Frame>

## Impact of toil

Toil affects engineering teams, business outcomes, and long-term competitiveness.

### Engineering impacts

* Burnout: Repetitive, unrewarding work leads to fatigue and lower morale.
* Opportunity cost: Time spent on toil is time not spent building improvements.
* Technical debt: Short-term manual fixes accumulate as long-term cruft.
* Skills atrophy: Teams focused on firefighting lose practice in development and design.
* Career stagnation: Engineers trapped in operational routines miss growth opportunities.

Toil steals the capacity to build better, more reliable systems.

<Frame>
  <img alt="A presentation slide titled &#x22;The Impact of Toil&#x22; showing five engineering impacts—Burnout, Opportunity Cost, Technical Debt Accumulation, Skills Atrophy, and Career Stagnation—each in a rounded box with a colorful icon and brief explanatory text." />
</Frame>

### Business impacts

* Slower time to market: Manual processes create bottlenecks.
* Higher operational costs: More headcount required as systems grow.
* Reduced reliability: Human steps are error-prone.
* Scaling limitations: Manual operations do not scale effectively.
* Competitive disadvantage: Teams burdened by toil innovate more slowly.

<Frame>
  <img alt="A presentation slide titled &#x22;The Impact of Toil&#x22; showing five cards: Slower Time-to-Market, Higher Operational Costs, Reduced Reliability, Scaling Limitations, and Competitive Disadvantage. Each card has an icon and a short note explaining how manual processes create bottlenecks, raise costs, and limit growth." />
</Frame>

## Measuring and identifying toil

Use a mix of quantitative and qualitative signals to locate and size toil. Combining both approaches helps prioritize which processes to eliminate or automate first.

| Measurement type |                                                                                          Examples | Purpose                                            |
| ---------------- | ------------------------------------------------------------------------------------------------: | -------------------------------------------------- |
| Quantitative     | Time tracking; toil ratio; number of operational tickets; automation gap analysis; on-call burden | Estimate scale and cost of toil                    |
| Qualitative      |      Toil surveys; job satisfaction tracking; toil amnesty; value stream mapping; shadow programs | Surface hidden, contextual, and low-frequency toil |

Quantitative details:

* Time tracking: Log hours by category (deployments, incident response, manual maintenance).
* Toil ratio: Percentage of time spent on purely operational tasks vs. engineering.
* Toil tickets: Count tickets classified as pure operational work.
* Automation gap analysis: Document manual steps in workflows.
* On-call burden: Measure manual alert response hours.

Qualitative practices:

* Toil surveys: Ask engineers for their primary pain points.
* Job satisfaction tracking: Correlate morale with toil metrics.
* Toil amnesty: Provide a safe way to report embarrassing or overlooked toil.
* Value stream mapping: Visualize handoffs and manual steps.
* Shadow programs: Observe and document undocumented operational work.

Combine these signals to prioritize reduction efforts.

<Frame>
  <img alt="A presentation slide titled &#x22;Measuring and Identifying Toil&#x22; that contrasts two approaches. The left box lists Quantitative Measurement items (time tracking, toil ratio, toil tickets, automation gap analysis, on-call burden) and the right box lists Qualitative Assessment items (toil surveys, job satisfaction tracking, toil amnesty, value stream mapping, shadow program)." />
</Frame>

## Hierarchy of approaches to reduce toil

Prioritize changes from most to least effective:

| Priority | Strategy  | Example                                                           |
| -------: | --------- | ----------------------------------------------------------------- |
|        1 | Eliminate | Replace a flaky service rather than endlessly restarting it       |
|        2 | Automate  | Automatic certificate renewal or CI-driven deployments            |
|        3 | Simplify  | Consolidate dashboards and reduce steps                           |
|        4 | Delegate  | Provide self-service portals or move work to the appropriate team |
|        5 | Batch     | Reduce frequency by batching tasks (weekly vs daily)              |

<Callout icon="lightbulb">
  Prefer elimination or automation where possible. Batching and delegation are last-resort options when elimination or automation are not feasible immediately.
</Callout>

## Calculating the true cost of toil

To get budget and team buy-in, quantify direct and indirect costs.

Direct costs:

* Labor hours: engineer time × hourly rate.
* Incident costs: downtime and remediation resulting from manual errors.

<Frame>
  <img alt="A presentation slide titled &#x22;Calculating the True Cost of Toil&#x22; showing a &#x22;Direct Costs&#x22; table. It lists Cost Factors and Descriptions with entries for &#x22;Labor Hours — Engineer time × hourly cost&#x22; and &#x22;Incident Costs — Downtime due to manual errors.&#x22;" />
</Frame>

Indirect costs:

* Opportunity cost: engineering improvements deferred because of toil.
* Attrition cost: turnover, recruitment, and lost tribal knowledge.
* Velocity impact: slower feature delivery and reduced competitiveness.

Example math:

* Team size: 8 engineers
* Toil per engineer: 15 hours/week
* Hourly rate: \$75/hour

Annual cost = 15 hours/week × 8 engineers × $75/hr × 52 weeks = $468,000 per year.

<Frame>
  <img alt="A presentation slide titled &#x22;Calculating the True Cost of Toil&#x22; showing a centered grey box with input values. It calculates annual toil as 15 hours × 8 engineers × 75/hr × 52 weeks = 468,000." />
</Frame>

## Culture and process for sustainable reduction

Making toil reduction enduring requires process, incentives, and psychological safety:

* Value engineering over heroics: Reward automation, refactoring, and systems thinking rather than heroic firefighting.
* Dedicated time budget: Allocate explicit time (e.g., an “engineering improvement” sprint) for removing toil.
* Psychological safety: Encourage raising and solving toil without blame.
* Knowledge sharing: Make runbooks and automation common knowledge, not tribal information.
* Continuous improvement: Treat toil reduction as an ongoing investment in reliability and velocity.

<Callout icon="warning">
  Do not treat toil as a rite of passage or a badge of honor. Normalizing manual firefighting hides systemic problems and increases long-term cost and risk.
</Callout>

## Final thoughts

Toil is a symptom, not pride. Use measurement to prioritize elimination and automation, and build cultural practices that make toil reduction sustainable. This frees engineering capacity for durable improvements and better reliability.

That concludes the lesson on managing complexity, risk, and toil. Next: incident management — change introduces instability, and effective incident practices determine how well a team recovers and learns.

## Links and references

* [Site Reliability Engineering (SRE) concepts](https://sre.google/)
* [Kubernetes documentation — concepts overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [CI/CD best practices](https://about.gitlab.com/topics/continuous-integration/)
* [Automation patterns and practices](https://martinfowler.com/articles/automation.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/5863d35a-6f2f-4453-9961-85eeb243c287/lesson/25aed780-577e-4aa9-836b-3584ce00c690" />
</CardGroup>
