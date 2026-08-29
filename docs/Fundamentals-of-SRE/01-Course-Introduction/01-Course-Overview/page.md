# Course Overview

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Course-Introduction/Course-Overview/page

Practical Site Reliability Engineering course teaching SLIs, SLOs, error budgets, observability, incident response, automation, release engineering, chaos experiments through labs and real-world exercises.

Welcome to the Site Reliability Engineering (SRE) course.

I'm Jake Page, and I’ll guide you through practical, hands-on lessons that teach how to design, operate, and improve reliable systems at scale. SRE originated at Google to help teams build and run reliable, scalable systems despite constant change. Today, organizations such as LinkedIn, Netflix, Twitter, and Microsoft apply SRE principles to maintain availability while moving fast.

As teams migrate to the cloud and scale rapidly, SRE practices are essential for balancing rapid innovation with dependable operations. The skills you gain from this course—SLIs/SLOs, error budgets, observability, incident response, automation, and chaos experiments—are some of the most in-demand in engineering today.

<Frame>
  <img alt="A minimalist chart on a black background shows a rising green line inside a rounded green box labeled &#x22;Advanced Operational Strategies,&#x22; with the x-axis labeled &#x22;Foundational Concepts.&#x22; Dashed axes emphasize progression from foundations to advanced strategies." />
</Frame>

This course emphasizes applied learning: labs, real-world examples, and exercises let you practice concepts, make mistakes, and iterate — preparing you to handle production incidents and reliability challenges.

> **lightbulb** This course emphasizes practical labs and exercises so you can apply SRE concepts in realistic environments.

What you will learn (high level)

* Fundamental SRE concepts and history
* How to design and measure reliability with SLIs, SLOs, and error budgets
* Reducing toil through automation and sound system design
* Incident response, on-call best practices, and blameless postmortems
* Release engineering and infrastructure-as-code for safe deployments
* Observability, monitoring, and alerting patterns
* Advanced topics: chaos engineering, cost-aware reliability, and trade-offs

Course modules at a glance

| Module                        | Focus                                | Outcomes                                                                 |
| ----------------------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| SRE Origins & Principles      | History, culture, and team structure | Understand what differentiates SRE from DevOps and how SRE teams operate |
| SLIs, SLOs & Error Budgets    | Defining and measuring reliability   | Create meaningful SLIs/SLOs and use error budgets to guide priorities    |
| Toil & System Design          | Reducing repetitive operational work | Identify toil and automate or redesign systems to reduce it              |
| Incident Management & On-Call | Alerts, response, and postmortems    | Run effective incident responses and create blameless learnings          |
| Release Engineering           | CI/CD, IaC, and rollout strategies   | Assess readiness and build safer release pipelines                       |
| Observability & Monitoring    | Telemetry, dashboards, and alerting  | Implement monitoring and design actionable alerts                        |
| Advanced Reliability          | Chaos, cost-aware architecture       | Run safe chaos experiments and balance reliability vs. cost              |

Course detail and sequence

1. Origins, culture, and core principles
   * We begin by tracing how SRE evolved and the core philosophies that guide it.
   * Compare SRE and DevOps in practice and learn how teams are organized to support reliability.
   * Useful reference: [DevOPS and SRE Basics](https://learn.kodekloud.com/user/courses/devops-basics).

2. SLIs, SLOs, and error budgets
   * Learn to design Service Level Indicators (SLIs), set meaningful Service Level Objectives (SLOs), and implement error budgets to balance feature velocity and system stability.
   * SLO-driven decisions help prioritize work and make trade-offs visible to stakeholders.

<Frame>
  <img alt="A presentation slide titled &#x22;Site Reliability Engineering&#x22; with a bullet list of related topics on the left. On the right, a mustachioed man with tattoos speaks into a microphone while seated at a wooden table." />
</Frame>

3. Foundations of reliability engineering
   * Deep-dive on designing SLIs, setting SLO targets, and measuring outcomes.
   * Learn approaches for visualizing reliability metrics and using them to drive operational decisions.

4. Managing complexity, risk, and toil
   * We’ll look at how system complexity increases failure modes and how to manage dependencies and scale.
   * Techniques to reduce operational toil include automation, thoughtful APIs, and simplified runbooks.

<Frame>
  <img alt="A presentation slide titled &#x22;Toil in SRE&#x22; showing four characteristics—Human Intervention, No Enduring Value, Automatable Potential, and Repetitive Tasks—arranged around a colorful concentric diagram. A presenter appears in a circular webcam inset at the bottom-right." />
</Frame>

5. Incident management and on-call operations
   * Prepare for and respond to incidents with proven processes: alerting strategy, incident command, and scalable communication.
   * We emphasize blameless postmortems as a continuous improvement mechanism.

<Frame>
  <img alt="A presentation slide titled &#x22;On-Call Preparation&#x22; showing key principles for on-call systems (sustainable rotations, primary/secondary engineers, recovery time, and follow-the-sun models) arranged around a colorful gear graphic. A small circular video of a presenter appears in the lower-right corner." />
</Frame>

> **warning** On-call rotations and incident response can be stressful. Prioritize sustainable rotations, clear runbooks, and automation to reduce human load and burnout.

6. Release engineering and deployment readiness
   * Learn readiness checks, automated pipelines, and configuration management to ensure safe releases.
   * Topics include feature flags, canary rollouts, and rollback strategies.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Example: Automating AWS IAM User Creation&#x22; explaining the need to automate creating IAM users and showing step 1: &#x22;Log in to AWS Console.&#x22; A small circular video feed of the presenter appears in the bottom-right." />
</Frame>

7. Observability, monitoring, and telemetry
   * Learn to collect, store, and visualize telemetry (logs, metrics, traces).
   * Design alerts that are actionable and aligned with SLOs to avoid alert fatigue.

Example command outputs and a sample observability repo (used in course labs):

```bash theme={null}
root@controlplane ~ ➜ ls -a
.npm
.nvm
.terraform.d
kodekloud-records-store-web-app-main
.wget-hsts
.bashrc

root@controlplane ~ ➜
```

Repository contents (observability-focused project used in labs):

```bash theme={null}
➜ kodekloud-records-store-web-app git:(main) ls
black_box_monitor.sh
config
deploy
docker-compose.yaml
Dockerfile
generate_end_to_end_traffic.sh
OBSERVABILITY_GUIDE.md
README.md
scripts
src
test_traffic.sh

➜ kodekloud-records-store-web-app git:(main) docker-compose --env-file .env.dev up -d
```

These exercises show how to instrument services, replay traffic, and validate dashboards and alerts in a controlled environment.

8. Advanced reliability: Chaos engineering and cost-aware design
   * Learn to plan and execute safe chaos experiments that uncover hidden failure modes.
   * Design reliability with cost trade-offs in mind so systems remain resilient and economically sustainable.

<Frame>
  <img alt="A presentation slide titled &#x22;Running Safe Chaos Experiments&#x22; showing three safety measure cards — Blast Radius, Time Limits, and Kill Switch — and a small presenter video inset in the bottom-right. The cards note limiting impact to 10% of the system, keeping experiments to minutes, and allowing immediate termination." />
</Frame>

Community and ongoing learning

* Join the forums and peer groups to ask questions, share solutions, and collaborate on hands-on labs.
* Continuous learning and community feedback are key to becoming an effective SRE.

Links and resources

* [SRE Workbook and Resources (Google)](https://sre.google/workbook/)
* [DevOps and SRE Basics — KodeKloud](https://learn.kodekloud.com/user/courses/devops-basics)
* [Chaos Engineering — KodeKloud](https://learn.kodekloud.com/user/courses/chaos-engineering)
* [Kubernetes Documentation — Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

If you’re ready, proceed to the first module where we explore SRE history, team structures, and core principles.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/2ed55f19-4a35-40be-9509-e57187ab4866/lesson/8cc9ea80-ea8d-47be-b526-3b143ee02041)
