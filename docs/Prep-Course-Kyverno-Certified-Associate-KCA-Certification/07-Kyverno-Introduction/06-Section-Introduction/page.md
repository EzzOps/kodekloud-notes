# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-Introduction/Section-Introduction/page

Introduction to Kyverno explaining its purpose, Kubernetes integration, installation, and rule types for codifying cluster policies and governance

In this lesson we begin a focused journey to master Kyverno — a Kubernetes-native policy engine for policy-as-code. This section establishes the foundation you'll need for the rest of the course. By the end you’ll understand what Kyverno is, the problems it solves for Kubernetes operations and security, how it integrates with Kubernetes, how to install it, and the types of policies you can author.

Why this matters: Kyverno lets cluster operators and platform teams codify security, governance, and operational best practices as Kubernetes resources. It operates as an admission controller, so policies are applied consistently at resource creation and mutation time, helping reduce manual drift and policy gaps.

Roadmap for this section:

| Topic                              |                                                                 What you’ll learn | Outcome                                                           |
| ---------------------------------- | --------------------------------------------------------------------------------: | ----------------------------------------------------------------- |
| What is Kyverno and why it matters |     The real-world problems Kyverno solves for Kubernetes operations and security | Understand the role of a policy engine and when to use Kyverno    |
| Kyverno architecture               | How Kyverno integrates with Kubernetes (admission controller, webhook flow, CRDs) | Visualize where policies run and how they affect resources        |
| Installation                       |                 Step-by-step instructions to deploy a working Kyverno environment | Get a cluster with Kyverno installed and ready for policy testing |
| Rule types                         |     Overview of `validate`, `mutate`, and `generate` rule categories and examples | Know which rule type to use for common governance tasks           |

<Frame>
  <img alt="The image outlines learning objectives related to Kyverno, including its importance, architecture, installation, and rule types. The objectives are numbered from one to four with brief descriptions." />
</Frame>

> **lightbulb** Recommended prerequisites: a local or remote Kubernetes cluster (kind, minikube, or managed), `kubectl` configured to the target context, and basic familiarity with Kubernetes resources such as Deployments, Services, and ConfigMaps. These will let you follow the hands-on examples in this section.

Throughout this section we’ll move from conceptual overviews to hands-on examples so you can immediately apply what you learn. Start here to build a strong foundation before moving on to advanced Kyverno policies and workflows.

Links and references

* [Kyverno Official Documentation](https://kyverno.io/docs/)
* [Kubernetes Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* [KCA — Kyverno Certified Associate (reference)](https://kyverno.io/certification/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/8cf118e1-7ca8-49b6-be5a-af80c331f394/lesson/88f6e4a0-4ecd-4d00-a0c1-dc34d46a934e)
