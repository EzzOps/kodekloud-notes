# Kyverno Policies

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-Introduction/Kyverno-Policies/page

Introduction to Kyverno policies for automating Kubernetes governance, explaining rule types validate mutate generate verifyImages and how platform engineers enforce and auto-correct cluster-wide policies

In earlier lessons we covered what Kubernetes is and how to install a cluster. Now we move to the most powerful part of Kyverno: policies.

Kyverno policies express the rules you want Kubernetes to enforce across your cluster. This article introduces the main building blocks, shows how policies are structured, and demonstrates how a platform engineer (Alex) uses them to automate governance at scale.

<Frame>
  <img alt="The image illustrates the concept of &#x22;Heart of Kyverno,&#x22; showing a progression from policies on the left to an icon representing infrastructure or systems on the right, linked by a simple arrow." />
</Frame>

We won’t exhaust every option here, but you’ll learn the core pieces and how they fit together so you can start writing effective policies.

Meet Alex — platform engineer

Alex manages multiple Kubernetes clusters and must keep them secure, consistent, and easy for developers to use. Developers continuously push new workloads, so manual checks are impractical. Kyverno lets Alex codify and automate the guardrails.

<Frame>
  <img alt="The image shows a person named Alex managing Kubernetes clusters with a note indicating he wants to automate governance." />
</Frame>

Common governance goals Alex needs to enforce:

* Ensure resources include a `cost-center` label for chargeback and tracking.
* Inject annotations automatically when missing.
* Block insecure or unsigned container images.
* Auto-create a default `NetworkPolicy` for every new namespace.

<Frame>
  <img alt="The image is a slide titled &#x22;Meet Alex Again&#x22; that lists challenges, including ensuring resources have labels for cost tracking, adding annotations, blocking insecure container images, and generating default resources like namespaces." />
</Frame>

Manually enforcing these policies across dozens or hundreds of clusters is error-prone — Kyverno automates it.

Policy structure overview

A Kyverno policy is a YAML object containing one or more rules. Each rule has two main responsibilities:

* Target selection — decide which resources the rule applies to (via `match` and optional `exclude` blocks).
* Action — choose a single action type per rule: `validate`, `mutate`, `generate`, or `verifyImages`.

<Frame>
  <img alt="The image illustrates the structure of a policy with a focus on target selection, detailing components like match and exclude rules, and actions such as validate, mutate, generate, and verify images." />
</Frame>

A rule's `match`/`exclude` determines the scope (kinds, namespaces, label selectors, users, operations), and then the rule performs exactly one action on those matched resources.

<Frame>
  <img alt="The image is a diagram illustrating the structure of a policy, focusing on defining rules and actions like validating, mutating, and generating resources. It includes elements such as matching, excluding, and verifying images, and lists related components like resources, operations, and user roles." />
</Frame>

Quick summary table of rule types

| Rule Type      | Purpose                                               | Common use case                                     |
| -------------- | ----------------------------------------------------- | --------------------------------------------------- |
| `validate`     | Enforce conditions and reject non-compliant resources | Block running containers as root                    |
| `mutate`       | Modify resources or inject fields on admission        | Add missing labels or annotations                   |
| `generate`     | Create new resources in response to events            | Create a default `NetworkPolicy` for new namespaces |
| `verifyImages` | Verify container image signatures and attestors       | Enforce image provenance from CI/CD                 |

Validate rules (gatekeeping)

`validate` rules act as admission checks. If a resource does not meet the rule’s criteria, the API server rejects it with a clear error message.

Example: disallow containers that run as root. This `validate` rule matches Pods on creation/update and enforces `securityContext.runAsNonRoot: true`:

```yaml theme={null}
rules:
  - name: check-for-non-root
    match:
      any:
        - resources:
            kinds:
              - Pod
    validate:
      message: "Running as root is not allowed."
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
```

<Frame>
  <img alt="The image highlights a challenge involving &#x22;validating resources,&#x22; with an issue where developers deploy containers as the 'root' user, posing a security risk." />
</Frame>

Mutate rules (automatic corrections)

`mutate` rules let Kyverno modify an incoming resource so it conforms to your policies — without blocking the developer.

Example: automatically add a `cost-center` label to Deployments if it’s missing:

```yaml theme={null}
rules:
  - name: add-cost-center-label
    match:
      any:
        - resources:
            kinds:
              - Deployment
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            cost-center: research
```

<Frame>
  <img alt="The image illustrates a challenge related to forgetting to add required labels, like a 'cost-center' label, which makes tracking spending difficult. It features an icon labeled &#x22;Alex&#x22; along with this challenge description." />
</Frame>

When a developer submits the Deployment, Kyverno injects the label before the object is persisted.

Generate rules (provision defaults)

`generate` rules create resources automatically in response to other events — ideal for provisioning default guardrails.

Example: create a default `NetworkPolicy` whenever a Namespace is created. This ensures namespaces are created with network restrictions without relying on each team to add them.

<Frame>
  <img alt="The image shows a challenge involving a task for creating a default network policy to restrict traffic when a new namespace is created for a team. It includes an icon labeled &#x22;Alex&#x22; and a checkmark indicating the requirement." />
</Frame>

Generate rules are commonly used for: `NetworkPolicy`, `ResourceQuota`, `LimitRange`, service accounts, or other namespace-level defaults.

VerifyImages rules (supply-chain protection)

One of the strongest defenses against supply-chain attacks is to verify container images at admission. `verifyImages` rules check signatures and attestors (trusted signers) so only images built and signed by your CI/CD are allowed.

Example: require signed images from `ghcr.io/my-org/*` and validate signatures using a trusted public key:

```yaml theme={null}
rules:
  - name: check-image-signature
    match:
      any:
        - resources:
            kinds:
              - Pod
    verifyImages:
      - imageReferences:
          - "ghcr.io/my-org/*"
        attestors:
          - name: trusted-attestor
            key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

<Frame>
  <img alt="The image features a question about ensuring the integrity of container images built by a CI/CD pipeline, asked by a character named Alex, under the heading &#x22;Verifying Images.&#x22;" />
</Frame>

<Callout icon="warning">
  Image verification is a critical security control. Misconfiguration can block valid deployments or fail to prevent unsigned images. Test `verifyImages` policies in a staging cluster and ensure your CI/CD signs images with the correct keys before enforcing in production.
</Callout>

Policy scope: Policy vs ClusterPolicy

Kyverno provides two policy object types to control scope:

* `Policy` (namespaced): The policy only applies to resources inside the namespace where it’s created. Use for team-specific rules, e.g., a payments team policy defined in the `payments` namespace.
* `ClusterPolicy` (cluster-wide): The policy applies across all namespaces in the cluster. Use for global security or compliance checks, e.g., blocking privileged containers or enforcing image signature verification cluster-wide.

The rules, `match`/`exclude` syntax, and actions are identical between `Policy` and `ClusterPolicy` — only the scope differs.

<Frame>
  <img alt="The image compares &#x22;Policy&#x22; and &#x22;ClusterPolicy.&#x22; &#x22;Policy&#x22; is a namespaced resource applying within a specific namespace, while &#x22;ClusterPolicy&#x22; is a cluster-wide resource applying across all namespaces." />
</Frame>

Best practices (brief)

* Start with `Policy` in a staging namespace to test rules, then promote to `ClusterPolicy`.
* Use clear `message` fields in `validate` rules so developers get actionable errors.
* Prefer `mutate` and `generate` when you can auto-correct without blocking developer velocity.
* Use `verifyImages` to enforce image provenance; integrate signing into CI/CD pipelines.

<Callout icon="lightbulb">
  Tip: Use labels and selectors in `match` blocks to target only the workloads you intend to manage (for example, `match.resources.kinds: ["Deployment"]` and `match.resources.namespaces: ["production"]`).
</Callout>

Resources and further reading

* Kyverno documentation: [https://kyverno.io/](https://kyverno.io/)
* Kubernetes admission controllers overview: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* Image signing and verification best practices: refer to your signing tool (e.g., Cosign, Notary) and integrate with CI/CD

This lesson gave you a concise introduction to Kyverno’s core rule types: `validate`, `mutate`, `generate`, and `verifyImages`. In subsequent lessons we'll dive deeper into each rule type with hands-on examples, real-world patterns, and production-ready configurations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/8cf118e1-7ca8-49b6-be5a-af80c331f394/lesson/7bd9d913-7289-4fa0-98b6-bc8d63300981" />
</CardGroup>
