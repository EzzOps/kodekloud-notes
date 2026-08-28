# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Policy-Exceptions/Section-Introduction/page

Explains Kyverno policy exceptions to allow scoped, auditable exceptions for workloads while preserving cluster security, with examples and best practices.

You can enforce cluster policies using Kyverno's `validate`, `mutate`, and `generate` rules. In practice, though, there are always exceptions—applications or third‑party tools that legitimately cannot comply with a rule. Kyverno provides a built‑in mechanism to handle those cases: policy exceptions.

This lesson explains Kyverno policy exceptions and demonstrates a safe, auditable workflow to allow exceptional workloads without weakening cluster security.

Alex's story: a real-world example

* Alex implemented a `validate` rule to ensure all new Pods run as a non‑root user — a common and important security best practice.
* The security team is happy and the cluster is locked down.
* Then the operations team needs to deploy a high‑priority monitoring agent (Alloy). The agent is a third‑party binary Alex cannot modify and it requires root privileges to operate.
* Because of the `validate` rule, Kyverno blocks the workload. Alex cannot change the agent, and he must avoid disabling the policy cluster‑wide.

<Frame>
  <img alt="The image presents a challenge where a policy was implemented to prevent pods from running as the root user, but this has caused an issue because a critical monitoring agent needs to run as root, resulting in Kyverno blocking the workload." />
</Frame>

Temporarily disabling the policy to allow the agent is an option — but it introduces a security gap and is error‑prone. Policy exceptions provide a better approach: allow a narrowly scoped exception that is auditable and does not weaken the policy for other workloads.

<Frame>
  <img alt="The image details a challenge faced by Alex, involving a security policy that prevents pods from running as the root user, which creates a problem needing resolution because a critical monitoring agent requires root access." />
</Frame>

What this section covers

* What a policy exception is and the custom resource used to create one.
* A step‑by‑step hands‑on example: create an exception that allows Alloy’s monitoring agent to run as root while keeping the global non‑root `validate` rule in place.
* How to use exceptions specifically for Pod Security exemptions and other targeted cases.
* Best practices for safely creating, reviewing, and auditing exceptions.

<Frame>
  <img alt="The image outlines a learning agenda titled &#x22;What We'll Learn&#x22; with two main topics: &#x22;Policy Exceptions&#x22; and &#x22;Pod Security Exemptions,&#x22; each with specific learning objectives." />
</Frame>

This article defines the Exception CRD, shows how to author an exception resource, and walks through managing exceptions safely (scoping, approval, and audit trails).

<Callout icon="lightbulb">
  Policy exceptions are implemented via a custom resource (the Exception CR). Use exceptions sparingly: prefer narrowly scoped rules that target specific namespaces, labels, or service accounts before resorting to exceptions.
</Callout>

Key benefits of using Kyverno policy exceptions

* Granular: scope exceptions to a particular namespace, workload, or label.
* Auditable: exceptions are Kubernetes resources and can be reviewed, versioned, and tracked.
* Reversible: remove the exception when it is no longer needed; global policies remain intact.
* Safe: avoids the risky practice of disabling policies cluster‑wide.

Recommended reading and references

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes Pod Security admission: [https://kubernetes.io/docs/concepts/security/pod-security-admission/](https://kubernetes.io/docs/concepts/security/pod-security-admission/)

Table — What you’ll learn in this section

| Topic                   | Description                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------- |
| What is an exception?   | How Kyverno models exceptions and why they’re safer than disabling policies.                       |
| Exception CRD           | The custom resource used to create and manage exceptions.                                          |
| Hands‑on example        | Step‑by‑step: allow Alloy’s monitoring agent to run as root without disabling the non‑root policy. |
| Pod Security exemptions | How exceptions relate to Pod Security and best practices for exemptions.                           |

<Callout icon="warning">
  Avoid blanket exceptions. Always scope exceptions as narrowly as possible (namespace, label selector, or specific workload) and follow an approval process to minimize risk.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/26478d8e-69b0-4b48-bc9a-173ba8b28d7b/lesson/a834303b-643e-4579-856d-3cb4f9617b26" />
</CardGroup>
