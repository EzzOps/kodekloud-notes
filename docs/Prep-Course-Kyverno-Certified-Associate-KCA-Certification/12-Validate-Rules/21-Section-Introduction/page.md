# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Section-Introduction/page

Teaching Kyverno validate rules to enforce Kubernetes policies, rejecting noncompliant resources using patterns, deny CEL expressions, podSecurity, foreach, and autogen for cluster enforcement.

In this lesson we move beyond filtering resources and focus on actively enforcing policies with Kyverno. Instead of just locating resources with `match`, `exclude`, and preconditions, you'll learn how to stop insecure or non-compliant objects from being admitted to your Kubernetes cluster.

We'll start with Kyverno's core validation primitive: the validate rule. Validate rules are used to reject resources that violate declarative patterns or conditional checks before those resources are persisted.

Alex, our platform engineer, already understands resource selection. Now he needs to enforce policies that:

* Block containers running as root.
* Require specific labels for tracking and billing.
* Prevent accidental creation of expensive `LoadBalancer` Services in development namespaces.

He can't just find these resources — he needs to stop them at the door. Validate rules enable exactly that behavior.

> **lightbulb** The validate rule is Kyverno's primary mechanism for rejecting resources that don't meet policy. It supports declarative patterns, conditional denial, and expressive checks via CEL.

<Frame>
  <img alt="The image depicts a challenge where Alex needs to move from selecting resources to actively enforcing policies. It includes icons for Alex, enforcement, and policies." />
</Frame>

What you'll learn in this lesson

| Topic                                | Purpose                                                                 | When to use                                                                |
| ------------------------------------ | ----------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Pattern-based validation (`pattern`) | Require labels, annotations, or specific field values                   | Enforce fixed structure or mandatory fields (e.g., require `app` label)    |
| Flexible matching (`anyPattern`)     | OR-style validation where one of several patterns is acceptable         | Allow multiple valid shapes (e.g., either `team` or `owner` label present) |
| Conditional denial (`deny` block)    | Use CEL expressions to reject resources when complex conditions are met | Complex or computed checks that can't be expressed as simple patterns      |
| Pod security (`podSecurity` subrule) | Enforce the Kubernetes Pod Security Standards (PSS)                     | Align with Kubernetes' official Pod Security admission guidance            |

<Frame>
  <img alt="The image outlines four topics to learn in a section: using 'pattern', using 'anyPattern', the 'deny' block, and the 'podSecurity' subrule, with brief descriptions of each." />
</Frame>

Advanced validation capabilities you'll also explore

* CEL expressions inside validate rules for expressive logic and conditional checks.
* `foreach` loops to inspect collections, such as ensuring every container in a pod uses an approved image registry.
* Autogen rules so your pod-level validations are applied automatically to workload controllers (Deployments, StatefulSets, etc.).

<Frame>
  <img alt="The image outlines a learning section with three topics: the Common Expression Language subrule, 'foreach' loops, and autogen for Pod controllers, focusing on advanced validation logic and automation in Kubernetes." />
</Frame>

> **warning** Validate rules actively reject resources. Test policies first in non-production namespaces or with `policyreport`/`dry-run` modes to avoid accidental disruption.

By the end of this lesson you'll have a practical toolkit for writing robust Kyverno validation policies that enforce security and operational requirements across your cluster.

Links and references

* [Kyverno Documentation](https://kyverno.io/docs/)
* [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/1bf911d6-b4b3-4ebf-b492-73da503e45ce)
