# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Mutate-Rules/Section-Introduction/page

Using Kyverno mutate rules to automatically modify Kubernetes resources to enforce policies, add missing metadata like cost center labels, reduce developer friction and ensure cluster compliance.

Validate rules act as powerful gatekeepers for your cluster: they reject resources that don't meet policy. But validation alone can create friction for developers when required metadata or configuration is missing.

Mutation moves beyond passive checks. With Kyverno mutate rules, you can automatically modify resources—either at admission or by updating existing objects—so they meet organizational standards without blocking developers.

<Frame>
  <img alt="The image illustrates Kyverno's &#x22;Mutate Rules,&#x22; describing a process where standards are enforced, and roles are shown as a gatekeeper and an assistant." />
</Frame>

> **lightbulb** Mutation lets Kyverno modify resources—either as they're admitted or by updating existing cluster resources—to automatically bring them into compliance without blocking developers.

To make this concrete, consider Alex, a platform engineer responsible for enforcing cluster standards.

Alex must ensure every Deployment contains a `cost-center` label so finance can bill and report accurately. Developers, focused on shipping code, often forget this administrative label.

<Frame>
  <img alt="The image illustrates &#x22;Alex's New Challenge,&#x22; depicting two groups: the Finance Team, requiring cost-center labels for billing, and Developers." />
</Frame>

One option is a validation rule that blocks any Deployment missing the label. But blocking requests forces developers to update YAML and retry, which slows delivery and increases support overhead.

<Frame>
  <img alt="The image presents a challenge faced by someone named Alex, who needs to write a validation rule to block deployments without a specific label. It includes an illustration of Alex and a document icon." />
</Frame>

Alex asks: instead of denying the request, can I fix the resource automatically—add the missing label at admission?

<Frame>
  <img alt="The image shows a challenge titled &#x22;Alex's New Challenge&#x22; with an illustration of a person named Alex. Below, there's a question about automatically adding a missing label instead of denying a request." />
</Frame>

Yes — Kyverno mutation is built for exactly this use case. Kyverno can add, modify, or remove fields so resources conform to policies, reducing developer friction and ensuring consistency.

This lesson covers the core mutation techniques you’ll use to automate standards across your cluster:

<Frame>
  <img alt="This image outlines a learning path for mastering Kyverno Mutate Rules, detailing five key components: Strategic Merge Patch, JSONPatch, Conditional Logic with Anchors, Mutating Existing Resources, and Looping with forEach." />
</Frame>

* Strategic Merge Patch — a simple way to add or update fields (common for adding labels or annotations).
* JSON Patch (RFC 6902) — precise, surgical updates such as removing fields or inserting items at a specific index.
* Conditional logic with preconditions — apply mutations only when certain conditions are met (for example, only add the label if it’s missing).
* Mutating existing resources — find and fix objects that are already running in the cluster.
* forEach syntax — iterate over lists (e.g., inject a sidecar or mutate each container in a Deployment).

Why use mutation instead of blocking validation?

* Improves developer experience by fixing policy issues automatically.
* Ensures consistent metadata and configuration across workloads.
* Reduces support load and accelerates delivery while keeping compliance intact.

Quick example — Strategic Merge Patch to add a `cost-center` label

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-cost-center-label
spec:
  rules:
  - name: add-cost-center
    match:
      resources:
        kinds:
        - Deployment
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            cost-center: "finance"
```

This policy adds `metadata.labels.cost-center=finance` to Deployments that arrive without the label. For more surgical operations—like removing specific keys—use JSON Patch (RFC 6902).

Resources and further reading

* Kyverno: [https://kyverno.io/](https://kyverno.io/)
* JSON Patch (RFC 6902): [https://tools.ietf.org/html/rfc6902](https://tools.ietf.org/html/rfc6902)
* Kubernetes Policies and Admission Controllers: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

> **warning** Mutation is powerful and can overwrite fields. Test policies in a staging environment and use `validation` rules or rigorous preconditions where you need to avoid unintended changes.

By the end of this lesson you’ll be able to author Kyverno policies that automatically enforce standards, reduce developer friction, and keep your cluster compliant and manageable.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/0d589a60-4265-4482-98b1-68c9544f07fd)
