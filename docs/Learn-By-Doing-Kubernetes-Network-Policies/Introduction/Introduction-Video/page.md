# Introduction Video

Source: https://notes.kodekloud.com/docs/Learn-By-Doing-Kubernetes-Network-Policies/Introduction/Introduction-Video/page

Hands-on course teaching Kubernetes NetworkPolicies, CNIs, Flannel versus Canal, default-deny baselines, egress controls, and practical labs culminating in a final challenge.

Hello and welcome.

My name is Vijin Palazhi, and I'm a trainer at KodeKloud.

In this lesson, I'm excited to introduce our new Learn by Doing Kubernetes Network Policies course.

At KodeKloud, our philosophy is learn by doing. This course is purpose-built to teach Kubernetes Network Policies through practical, hands-on labs so you can apply what you learn immediately.

What this course covers:

* What a NetworkPolicy is and why it matters in Kubernetes.
* Container Network Interfaces (CNIs): why they exist and how they work.
* Installing two popular network plugins across separate Kubernetes clusters.
* Comparing two commonly used network plugins: Flannel and Canal — features, differences, and when to choose each.
* Dissecting a NetworkPolicy YAML file to learn every component.
* Implementing the default-deny NetworkPolicy to enforce a secure baseline.

<Frame>
  <img alt="The image outlines a curriculum for Kubernetes network policies, including topics like CNIs, Flannel vs Canal, and security postures with default deny policies." />
</Frame>

Beyond the default-deny baseline, you'll create targeted NetworkPolicies for fine-grained access control and learn how to isolate applications across namespaces using practical scenarios. We also cover egress NetworkPolicies to control outbound traffic.

Course format — how you’ll learn:

* Every topic is delivered as a lab. Labs start with a concise description of objectives and key concepts.
* You work directly in hands-on environments to implement NetworkPolicies that solve real-world problems.
* Each lab includes a step-by-step instructions page with commands and explanations to guide you to a working solution.

Table: Topics, outcomes, and lab focus

| Topic                        | What you'll learn                                                      | Lab outcome                                       |
| ---------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------- |
| NetworkPolicy fundamentals   | Purpose, scope, and default behaviors                                  | Apply a basic NetworkPolicy to allow/deny traffic |
| CNIs explained               | Role of CNIs and how they affect network policies                      | Install and validate CNI behavior                 |
| Flannel vs Canal             | Architecture, pros/cons, and use cases                                 | Deploy both plugins and compare traffic behavior  |
| NetworkPolicy YAML breakdown | `podSelector`, `namespaceSelector`, `ingress`, `egress`, `policyTypes` | Read and author NetworkPolicy manifests           |
| Default-deny posture         | Why baseline deny is important for security                            | Implement default-deny and open necessary ports   |
| Egress controls              | How to limit outbound traffic from pods                                | Enforce egress policies for external access       |

<Callout icon="lightbulb">
  This course is suitable for beginners and practitioners who want hands-on practice with Kubernetes network security. If you already know Kubernetes basics (pods, services, namespaces), you'll get the most value.
</Callout>

Final challenge

* The course ends with a cumulative challenge that combines the key skills from the labs — designing and implementing NetworkPolicies that meet realistic security requirements.

How this course differs from traditional tutorials:

* Action-first labs rather than long theory sections.
* Immediate feedback in real environments to reinforce learning.
* Guided instructions with curated commands and explanations to build confidence.

References and further reading:

* [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Kubernetes CNIs](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
* [Flannel GitHub](https://github.com/flannel-io/flannel)
* [Project Calico (for Canal context)](https://projectcalico.docs.tigera.io/)

Whether you are just starting with Kubernetes or want to strengthen your cluster network security skills, this course will give you practical, repeatable experience with NetworkPolicies.

If you're ready, let's jump into the very first lab, where we'll learn why NetworkPolicies are essential and how they protect cluster network traffic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-by-doing-kubernetes-network-policies/module/fc6339e3-ce19-45d1-b542-71f47f691275/lesson/65cc748e-060d-4f9b-9284-4ea0163b4db9" />
</CardGroup>
