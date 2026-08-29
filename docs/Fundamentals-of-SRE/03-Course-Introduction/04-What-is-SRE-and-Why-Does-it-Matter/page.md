# Clone the Record Store app repository
git clone https://github.com/jakepage91/kodekloud-records-store-web-app.git

# Clone the Terraform infrastructure repository (optional: for IaC labs)
git clone https://github.com/jakepage91/kodekloud-records-terraform-infrastructure.git
```

Why this sample app is effective for SRE practice

* It models a realistic microservice-style application with synchronous endpoints and asynchronous background processing.
* Labs target operational concerns: performance, reliability, monitoring, alerting, scaling, and incident response.
* Source code + infra examples let you practice development, deployment, and infrastructure-as-code workflows end-to-end.

Core architecture components and learning opportunities:

| Component           | Purpose                                                        | SRE-focused examples                                                   |
| ------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Core App            | Routes for products, orders, and processing triggers           | Functional testing, endpoint-level observability, load-testing         |
| Async Processing    | Background workers and message broker for long-running tasks   | Queueing behavior, worker autoscaling, backpressure handling           |
| Persistent Storage  | Relational DB for product/order data                           | Backups, migrations, storage tuning, consistency concerns              |
| Observability Stack | Monitoring, logging, and tracing tools integrated with the app | Dashboards, alerting rules, distributed traces for root-cause analysis |

Below is a visual summary of the Record Store architecture used across the labs.

<Frame>
  <img alt="A system architecture diagram titled &#x22;Introducing the KodeKloud Record Store App&#x22; with a central &#x22;KodeKloud Record Store&#x22; box connected to four modules. The modules are Observability (Prometheus, Grafana, Jaeger, Loki, etc.), Storage (PostgreSQL), Core App (orders, process orders, products) and Async Processing (RabbitMQ, Celery workers)." />
</Frame>

The course also includes a Terraform-based infrastructure repository that demonstrates provisioning cloud resources for this app — an essential skill for reproducible environments and reliable release pipelines:

* [https://github.com/jakepage91/kodekloud-records-terraform-infrastructure](https://github.com/jakepage91/kodekloud-records-terraform-infrastructure)

<Frame>
  <img alt="A presentation slide titled &#x22;Introducing the KodeKloud Records Terraform Infrastructure&#x22; showing a GitHub repository screenshot and the GitHub cat logo. A URL to the repo (https://github.com/jakepage91/kodekloud-records-terraform-infrastructure) is displayed at the bottom." />
</Frame>

<Callout icon="warning">
  Running Terraform or cloud-deploying the example infrastructure may create billable cloud resources. Review the Terraform README and your cloud provider's free-tier or cost controls before applying changes.
</Callout>

Welcome to the KodeKloud Record Store app SRE team — consider this course your onboarding from development to operations. By completing the labs and exercises you’ll gain practical SRE skills, including:

* Creating SLIs and SLOs and calculating error budgets
* Building observability dashboards and defining alerts
* Provisioning infrastructure using Terraform (IaC)
* Designing and testing reliable release pipelines
* Performing incident investigation using logs and distributed traces

<Frame>
  <img alt="A welcome slide titled &#x22;You Are the Newest Member of the KodeKloud Record Store App SRE Team&#x22; listing five tasks: SLI and SLO creation, error budget calculation, observability dashboard creation, IaC provisioning, and release pipelines. A small illustration of a person using a laptop appears at the left." />
</Frame>

Next steps

* Clone the repositories and follow the README setup to start the labs.
* Begin with basic observability labs (metrics, logging, tracing) before moving to scaling and incident simulation exercises.
* Use the app and infra code as a sandbox to experiment with SRE practices in a controlled environment.

Further reading and references

* KodeKloud Record Store app repo: [https://github.com/jakepage91/kodekloud-records-store-web-app](https://github.com/jakepage91/kodekloud-records-store-web-app)
* KodeKloud Terraform infra repo: [https://github.com/jakepage91/kodekloud-records-terraform-infrastructure](https://github.com/jakepage91/kodekloud-records-terraform-infrastructure)

Get ready to dive in, experiment, and gain hands-on SRE experience through the course playgrounds and labs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/2ed55f19-4a35-40be-9509-e57187ab4866/lesson/8c56deb7-265c-4bfa-8f9c-89c968b03a19" />
</CardGroup>


# What is SRE and Why Does it Matter

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Course-Introduction/What-is-SRE-and-Why-Does-it-Matter/page

Describes Site Reliability Engineering applying software engineering to operations, balancing velocity and reliability through SLOs, error budgets, automation, observability, and blameless postmortems.

Site Reliability Engineering (SRE) applies a software engineering mindset to operations. As Ben Treynor Sloss — a Google engineering leader — put it: “SRE is what happens when you ask a software engineer to design an operations team.” In practice, that means solving reliability challenges with code, data, and repeatable processes rather than ad-hoc firefighting.

<Frame>
  <img alt="A presentation slide titled &#x22;Site Reliability Engineering — Definition&#x22; showing a blue quote box. The quote defines SRE as &#x22;what happens when you ask a software engineer to design an operations team,&#x22; attributed to a Google engineering executive." />
</Frame>

## The central tradeoff: velocity vs. reliability

SRE is fundamentally a balancing act between two forces:

* Velocity: delivering features, shipping changes, and innovating quickly.
* Reliability: maintaining uptime, acceptable latency, low error rates, and a good user experience.

Change introduces risk; SRE aims to move fast while keeping stability within defined bounds. That tradeoff is often visualized as a continuous loop between shipping and stabilizing.

<Frame>
  <img alt="A slide titled &#x22;Site Reliability Engineering – Definition&#x22; showing that SRE balances two interconnected forces: Velocity (e.g., releases, features, innovation) and Reliability (e.g., uptime, latency, SLOs). A two-colored circular diagram with numbered markers and a small icon in the center illustrates the continuous tradeoff." />
</Frame>

## Ask the right operational questions up front

SREs start by anticipating failure modes and documenting responses. Common operational questions include:

* How can this application fail?
* What mitigations and runbooks exist?
* What service levels does the business and users require?
* How will we detect, measure, and alert on failures?

Answering these before incidents occur is key to reducing downtime and time-to-recovery.

<Frame>
  <img alt="A presentation slide titled &#x22;Site Reliability Engineering – Definition&#x22; with an illustration of three people and a speech bubble on the left and a boxed bullet list on the right. The bullets ask SRE questions like how the application can break, what to do when it does, acceptable service levels, and how to know if the app isn't working." />
</Frame>

## Where SRE sits in the organization

SRE bridges traditional IT operations and DevOps practices. It narrows the gap between system design and production behavior by treating operations as an engineering problem: build for failure, measure behavior, automate responses, and continually iterate.

Core SRE practices include:

|                        Resource | Purpose                                     | Example outcome                         |
| ------------------------------: | ------------------------------------------- | --------------------------------------- |
| SLIs (Service Level Indicators) | Quantify user-facing behavior               | Request latency p50/p95, error rate     |
| SLOs (Service Level Objectives) | Target ranges for SLIs to guide decisions   | 99.9% availability over a month         |
|                   Error budgets | Allow controlled risk-taking for releases   | Use remaining budget to approve deploys |
|                      Automation | Eliminate repetitive manual work (toil)     | Automated rollbacks, CI/CD pipelines    |
|                   Observability | Detect and diagnose issues quickly          | Metrics, logs, distributed tracing      |
|           Blameless postmortems | Learn from incidents and prevent recurrence | Action items with owners and timelines  |

<Frame>
  <img alt="A presentation slide titled &#x22;Site Reliability Engineering – Definition&#x22; that lists five numbered principles with small icons. The points summarize SRE as the intersection of traditional IT and DevOps, bridging design and runtime, ensuring reliability and performance, embracing risk and anticipating failure, and relying on automation to build resilient systems." />
</Frame>

<Callout icon="lightbulb">
  Error budgets are central to SRE risk management: they make reliability a measurable tradeoff, letting teams decide when to prioritize feature velocity versus stability.
</Callout>

## Why SRE matters — three perspectives

* Business: Reliability is a baseline requirement. Users and customers abandon unreliable services, so uptime and performance affect revenue, retention, and reputation.
* Technical: SRE transforms reactive firefighting into proactive engineering — designing systems that fail gracefully and recover automatically.
* Cultural: SRE fosters a blameless learning culture where teams analyze incidents, share knowledge, and continuously improve processes and systems.

<Frame>
  <img alt="A slide titled &#x22;Why SRE Matters&#x22; showing three colored panels: Business Perspective, Technical Perspective, and Cultural Perspective. Each panel has an icon and a short message about reliability as a business requirement, SRE turning firefighting into proactive engineering, and fostering a blame-free learning culture." />
</Frame>

## Historical context and influential practices

SRE evolved through real-world demands at large-scale companies. Key influences include:

* Google: Pioneered SRE as a discipline and popularized SLOs and error budgets.
* Netflix: Advanced chaos engineering and resilience testing to validate system behavior under failure.
* Airbnb and other companies: Demonstrated that SRE principles (automation, observability, cross-team collaboration) apply broadly — not just at hyperscale.

<Frame>
  <img alt="A slide titled &#x22;SRE – The Gold Standard: Google, Netflix, and AirBnB&#x22; showing the Google, Netflix, and Airbnb logos with short bullet points about each company's role in developing and advancing Site Reliability Engineering. Google is labeled &#x22;The Pioneer,&#x22; Netflix &#x22;The Innovator,&#x22; and Airbnb &#x22;The Example.&#x22;" />
</Frame>

## Summary

SRE is a pragmatic engineering discipline that balances speed and stability. It emphasizes anticipating failure, measuring what matters, automating toil, and learning continuously through blameless processes. Applying SRE practices helps teams ship faster with predictable risk and recover more quickly when things go wrong.

In the next lesson we'll dive deeper into specific SRE practices and tools — including how to define SLIs/SLOs, structure error budgets, and implement observability and automation in production systems.

## Links and references

* [Site Reliability Engineering: How Google Runs Production Systems (book)](https://sre.google/books/)
* [Google SRE resources](https://sre.google/)
* [Chaos Engineering principles (Netflix-inspired)](https://principlesofchaos.org/)
* [Observability vs Monitoring](https://www.oreilly.com/library/view/observability-principles-and/9781492063446/)
* [Kubernetes documentation (deploy and observe cloud-native systems)](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/2ed55f19-4a35-40be-9509-e57187ab4866/lesson/10168440-9b64-42b6-a6cb-076eed1e403a" />
</CardGroup>
