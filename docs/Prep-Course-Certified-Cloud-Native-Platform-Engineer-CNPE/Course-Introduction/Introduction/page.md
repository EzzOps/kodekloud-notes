# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Course-Introduction/Introduction/page

A hands on course preparing candidates for the Certified Cloud Native Platform Engineer exam, teaching platform architecture, GitOps, APIs, observability, security, and practical labs with mock exams.

Did you know organizations such as Spotify, Intuit, and Mercedes‑Benz reduced release cycles from months to minutes by adopting cloud‑native technologies and platform engineering practices? Platform engineers design and operate the systems that make those outcomes possible. The Certified Cloud Native Platform Engineer (CNPE) certification is the industry credential that proves you can deliver scalable, reliable platforms using modern cloud‑native patterns.

Welcome to the Certified Cloud Native Platform Engineer course. I’m Nourhan Mohamed, and in this lesson I’ll guide you through the practical skills required to design, build, and operate stable, scalable platforms. Having completed the CNPE myself, I’ll share targeted exam preparation strategies and hands‑on approaches that reflect real‑world platform engineering tasks.

<Callout icon="lightbulb">
  This lesson assumes familiarity with Kubernetes fundamentals, CI/CD concepts, and daily use of `kubectl`. If you haven’t yet completed those basics, take the [Certified Kubernetes Administrator (CKA)](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator) or an equivalent Kubernetes course first, then return here.
</Callout>

CNPE is a performance‑based exam that mirrors production scenarios: you won’t be choosing multiple‑choice answers. Instead, you’ll demonstrate how you make engineering decisions, choose appropriate tools, and get a platform working under time pressure. This course follows that model with demos and hands‑on labs for every major topic.

<Frame>
  <img alt="The image shows a webpage for the Certified Cloud Native Platform Engineer (CNPE) course offered by the Linux Foundation. It includes details about the certification benefits, pricing, and options to enroll, with a small circular inset of a person in the corner." />
</Frame>

Below are the core domains covered in this course, with concise descriptions of what you’ll learn and why each area matters for platform engineering.

## Course domains — what you’ll learn

Platform architecture and infrastructure

* Build the foundation for a modern platform: compute, storage, networking, multi‑tenancy, and cost controls.
* Learn patterns and guardrails that enable predictable, safe, repeatable platform operations.

<Frame>
  <img alt="The image shows a diagram labeled &#x22;The Guardrails Stack&#x22; with colorful concentric rings, alongside text describing concepts like Pod Security Standards, NetworkPolicies, ResourceQuotas, RBAC, and Namespaces. A small inset shows a person speaking." />
</Frame>

GitOps and continuous delivery

* Implement GitOps workflows and integrate CI/CD with Kubernetes for fully declarative platform management.
* Apply progressive delivery strategies (canary, blue‑green, feature flags) to reduce risk during releases.

<Frame>
  <img alt="The image illustrates &#x22;The Reconciliation Loop,&#x22; showing a cycle with three stages: Watch, Compare, and Sync. There's also a person in the bottom right corner speaking into a microphone." />
</Frame>

Platform API and self‑service

* Design Custom Resource Definitions (CRDs), author operators, and enable developer self‑service.
* Explore dynamic composition and function pipelines to make extensible, composable platform APIs.

<Frame>
  <img alt="The image displays a flowchart illustrating &#x22;Dynamic Composition via Function Pipeline&#x22; with steps including input, rendering base, patching and transforming, applying custom logic, and managing resources. There's also a person speaking in a small circular inset at the bottom right." />
</Frame>

Observability and operations

* Instrument platforms for monitoring, logging, alerting, and distributed tracing.
* Learn operational runbooks, incident response practices, and techniques to diagnose platform health.

<Frame>
  <img alt="The image is an informational graphic explaining &#x22;The Trace Data Model&#x22; with sections on Trace, Span, and Context, each detailing its components and purpose. It also includes a note that &#x22;Trace ID is the thread that ties all spans together—context propagation keeps it flowing across services.&#x22;" />
</Frame>

Security and policy enforcement

* Implement Role‑Based Access Control (RBAC), secure service‑to‑service communication, and policy management.
* Apply compliance guardrails and admission controls to protect workloads and data.

After each domain you’ll complete quizzes to validate core concepts. The course also includes timed mock exams that simulate CNPE’s real test environment and time constraints so you can practice under pressure.

## Quick domain overview

| Domain                                   | Focus                                  | Example topics                                                 |
| ---------------------------------------- | -------------------------------------- | -------------------------------------------------------------- |
| Platform architecture and infrastructure | Foundation and guardrails              | Compute, storage, networking, multi‑tenancy, cost optimization |
| GitOps & continuous delivery             | Declarative delivery and safe rollouts | Reconciliation loops, CI/CD integration, progressive delivery  |
| Platform API & self‑service              | Extensible platform APIs               | CRDs, operators, dynamic composition, function pipelines       |
| Observability & operations               | Platform health and incident response  | Monitoring, logging, tracing, runbooks                         |
| Security & policy enforcement            | Access control and compliance          | RBAC, network policies, admission controls, encryption         |

## Community, support, and exam preparation

Community learning accelerates progress. Join our forums, office hours, and community channels to ask questions, review labs, and learn from peers and instructors.

<Frame>
  <img alt="The image shows a chat application interface with a selection of channels, specifically highlighting the channel &#x22;#office-hours-with-community.&#x22; There are profile pictures of users and a text message on the right side." />
</Frame>

Are you ready to earn one of the most respected platform engineering certifications in the cloud‑native ecosystem? Let’s get started.

## Links and references

* [Certified Kubernetes Administrator (CKA) course — KodeKloud](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator)
* [Kubernetes documentation — Concepts overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Linux Foundation Training — CNPE program](https://training.linuxfoundation.org/)
* [GitOps resources and best practices](https://www.gitops.tech/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/cde3e2ef-28b1-4c9a-988b-49cbeb851f45/lesson/4e0e11af-efbf-4f94-b7ad-2b9d0161da33" />
</CardGroup>
