# CNPE Certification Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Course-Introduction/CNPE-Certification-Overview/page

Overview of the Certified Cloud Native Platform Engineer exam covering format, domain weights, common tooling, allowed resources, remote exam environment, and study and preparation guidance

This lesson explains everything you need to know about the Certified Cloud Native Platform Engineer (CNPE) exam before you begin studying or taking the test. You’ll learn the exam format, domain weights, common tooling, allowed resources, and what the remote exam environment looks like.

Below is a concise overview to help you prioritize your study time and build the right hands‑on practice.

## Quick facts — exam format and logistics

| Item               | Details                                                          |
| ------------------ | ---------------------------------------------------------------- |
| Exam style         | Performance-based (live tasks in a real Kubernetes environment)  |
| Tasks              | 15–20 hands‑on tasks                                             |
| Duration           | 2 hours (≈6–8 minutes per task)                                  |
| Passing score      | 64% (published)                                                  |
| Validity           | Certification valid for 2 years from exam date                   |
| Proctoring         | Remotely proctored via the PSI secure browser                    |
| Language           | English only                                                     |
| Kubernetes version | Typically current; updated within 4–8 weeks of upstream releases |

<Frame>
  <img alt="The image provides a summary of the CNPE exam format, including details on questions, duration, passing score, validity, proctoring, language, and the Kubernetes version used." />
</Frame>

At the time this lesson was recorded, the exam uses Kubernetes v1.32. Expect the exam environment to track upstream releases closely.

## Exam domains and weights

The CNPE exam covers five domains. Use the domain weights below to focus your study time and hands‑on practice:

| Domain                | Weight | Focus areas                                                                                  |
| --------------------- | -----: | -------------------------------------------------------------------------------------------- |
| GitOps                |    25% | Reconciliation, manifests, automation, Git workflow for platform delivery                    |
| Platform APIs         |    25% | CRDs, controllers, service APIs, platform extension and automation                           |
| Observability         |    20% | Monitoring, logging, tracing, incident response (Prometheus, Grafana, Jaeger, OpenTelemetry) |
| Platform Architecture |    15% | Networking, storage, cost considerations, RBAC, design patterns                              |
| Security              |    15% | Policy engines, service mesh, access control (OPA, Kyverno, Gatekeeper, Istio, Linkerd)      |

GitOps and Platform APIs together account for 50% of the exam, so allocate proportionally more time to these domains while studying.

<Frame>
  <img alt="The image displays a pie chart and a list of five exam domains with corresponding percentages and descriptions. Each domain covers aspects such as Platform Architecture, GitOps, APIs, Observability, and Security." />
</Frame>

## Tooling you may encounter

CNCF publishes example tooling that commonly appears in tasks. Typical tools include:

* Observability: Prometheus, Grafana, Jaeger, OpenTelemetry, OpenCost
* Policy & security: Gatekeeper, OPA, Kyverno
* Service mesh: Istio, Linkerd

Key points about tooling and exam expectations:

* The exam does not test memorization of tool internals or every CLI flag.
* Each task provides a quick reference box with links to relevant tool documentation.
* You should be comfortable reading documentation quickly and applying concepts.
* Hands‑on familiarity with these tools speeds you through tasks.

<Frame>
  <img alt="The image lists tools related to observability (Prometheus, Grafana, Jaeger, OpenTelemetry, OpenCost) and security & policy (Gatekeeper, OPA, Kyverno, Istio, Linkerd)." />
</Frame>

## Resources allowed during the exam

You may access the documentation linked in each question and the official Kubernetes docs:

* `https://kubernetes.io/docs` (Kubernetes docs)
* `https://kubernetes.io/blog` (Kubernetes blog)
* Tool-specific documentation linked in each task’s quick reference box

You may follow those allowed links during the exam, but navigating to unrelated external sites or unauthorized resources is not permitted.

## Exam environment and tooling

The CNPE exam runs in a browser‑based Linux remote desktop. Typical aspects of the environment:

* Each task will specify a host to `ssh` into; those hosts have `kubectl` preconfigured.
* Common conveniences are set up: `k` alias for `kubectl` and Bash auto-completion.
* Standard CLI tools and required tool-specific CLIs are preinstalled — you will not be asked to install software.
* Firefox is available for accessing web UIs and documentation links.
* The exam evaluates operational competence and usage, not software installation or environment setup.

<Frame>
  <img alt="The image provides guidelines for an exam, listing allowed resources such as certain Kubernetes documentation and describing the exam environment, including tools and software setup." />
</Frame>

## Preparation strategy

* Complete all available labs and mock exams to build speed and confidence.
* Practice real tasks in Kubernetes clusters, focusing on the domains and tooling listed above.
* Practice reading documentation quickly and applying examples — each task gives quick reference links, so speed and comprehension matter more than memorization.
* During practice, time yourself on representative tasks to get comfortable with the 6–8 minute cadence per task.

<Callout icon="lightbulb">
  Focus study time proportionally to the domain weights, practice hands‑on labs and mock exams, and build the habit of quickly reading and applying documentation. This combination gives the best chance of success on the CNPE exam.
</Callout>

## Links and references

* CNCF CNPE certification: [https://www.cncf.io/certification/cnpe/](https://www.cncf.io/certification/cnpe/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/cde3e2ef-28b1-4c9a-988b-49cbeb851f45/lesson/bafb1557-c12c-42d6-91ad-f14384292b11" />
</CardGroup>
