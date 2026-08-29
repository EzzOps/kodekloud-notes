# Example snippet to pass as controller args (varies by deployment method)
args:
  - --background-scan-interval=30m
```

Summary

* Background scanning audits resources that predate your policies and fills the visibility gap left by admission-only reporting.
* `spec.background` controls whether a policy participates in background scans (default: `true`).
* The Reports Controller periodically wakes, evaluates resources, produces ephemeral reports, and aggregates them into durable `PolicyReport` / `ClusterPolicyReport` objects.
* Avoid using admission-time data (e.g., `request.userInfo`) in policies you expect to run during background scans.

<Frame>
  <img alt="The image is a summary of a background scanning process that consists of three points: the goal of auditing pre-existing resources, the process of scanning and aggregating reports, and the limitations regarding the use of admission-time data." />
</Frame>

Links and references

* Kyverno documentation: [https://kyverno.io/](https://kyverno.io/)
* Kubernetes API concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Kyverno GitHub: [https://github.com/kyverno/kyverno](https://github.com/kyverno/kyverno)

That's it for this section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/360718cb-5ab8-44a1-bcd2-beae95ede7c9/lesson/e4413c2a-0367-48c6-9c22-cefe2add1c72" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/360718cb-5ab8-44a1-bcd2-beae95ede7c9/lesson/d946034a-f14b-4e2f-a904-343871ed4094" />
</CardGroup>


# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Reporting/Section-Introduction/page

Explains Kyverno reporting using PolicyReport and ClusterPolicyReport to convert policy evaluations into structured, queryable compliance reports with audit-mode entries and background scans.

So far we've written policies to enforce rules, mutate resources, and perform cleanup. A critical question remains: how do we get a clear, consolidated view of the cluster's compliance status?

To understand your security posture you need a reporting system that converts raw policy evaluations into structured, queryable results. In this lesson we'll explore Kyverno's reporting capabilities and how they solve Alex's visibility problem.

Common obstacles Alex faces:

* Log overload: every audit violation becomes a log entry, but logs are raw and hard to query.
* Blind spots: Audit policies only evaluate new or updated resources, leaving existing resources unassessed.
* No formal reporting: security teams require compliance reports, but Alex lacks a way to generate them.

<Frame>
  <img alt="The image outlines &#x22;Alex's New Challenge&#x22; with three problems: Log Overload, Pre-Existing Resources, and Compliance Reporting, each with a brief description." />
</Frame>

Alex needs to move from reactive log-checking to proactive compliance reporting. He asks: how do I get a consolidated view of my cluster's compliance status that includes both new and pre-existing resources? Kyverno's reporting system is designed to answer exactly that.

What we’ll cover

* Core concepts: PolicyReport and ClusterPolicyReport as Kubernetes custom resources.
* Real-time reporting: how Audit-mode policies generate structured report entries.
* Background scans: how to evaluate existing resources and close the visibility gap so you can produce formal compliance reports.

<Callout icon="lightbulb">
  PolicyReport and ClusterPolicyReport are standard Kubernetes custom resources. That means they can be queried with `kubectl`, watched by controllers, and exported to external systems via existing Kubernetes integrations.
</Callout>

Why PolicyReport and ClusterPolicyReport matter

* Structured data: reports convert noisy audit logs into typed, queryable objects.
* Integrations: because they're Kubernetes resources, you can use existing exporters, controllers, and tooling to collect and persist them.
* Visibility: reports capture evaluation results so you can answer questions like “How many pods are violating the image tag policy right now?”

Quick commands (querying reports)

```bash theme={null}
