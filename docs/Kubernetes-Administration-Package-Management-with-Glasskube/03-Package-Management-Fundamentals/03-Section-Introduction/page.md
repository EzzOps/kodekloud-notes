# Section Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Management-Fundamentals/Section-Introduction/page

Foundations of Kubernetes package management, tooling survey and practical guidance for packaging, lifecycle, and installing networking, ingress, storage, observability, and cluster addons

Welcome to the first section. This lesson lays the foundation for Kubernetes package management and prepares you to evaluate and operate package tooling in real clusters.

We will:

* Explain why package managers are essential for Kubernetes operations.
* Describe the problems package managers solve and the constraints they must work within.
* Review how existing tools behave when managing cluster components and control-plane adjacent software.

This section assumes you have a basic familiarity with Kubernetes concepts. We'll start with a concise Kubernetes refresher to align terminology and expectations. Then we'll define what we mean by a "package" in the Kubernetes context, break down its common components, and survey the tools commonly used today (Helm, Kustomize, Operators, OCI-based bundles, and GitOps workflows). Finally, we will introduce the five packages that will be configured and installed in later lessons—covering the key categories of networking, ingress, storage, observability, and cluster lifecycle addons—so you can follow along with hands-on examples.

| Topic                  |                                                         What you'll learn | Why it matters                                              |
| ---------------------- | ------------------------------------------------------------------------: | ----------------------------------------------------------- |
| Kubernetes refresher   |                                             Core concepts and terminology | Ensures consistent understanding across readers             |
| Package definition     |    What constitutes a Kubernetes package (manifests, CRDs, images, hooks) | Helps you reason about packaging patterns and compatibility |
| Problems & constraints |  Dependency management, idempotency, upgrade safety, environment overlays | Frames the operational trade-offs of different tools        |
| Tool survey            | How Helm, Kustomize, Operators, OCI bundles, and GitOps address packaging | Enables informed tool selection for teams                   |
| Hands-on packages      |               The five categories of packages we'll install and configure | Practical, reproducible experience for cluster management   |

> **lightbulb** This section is geared toward operators and engineers who know basic Kubernetes primitives (Pods, Deployments, Services). If you need a quick refresher, see the [Kubernetes documentation](https://kubernetes.io/docs/). We'll keep examples focused on package composition and lifecycle, not introductory cluster setup.

We will evaluate whether current tooling meets the needs of modern Kubernetes operations, considering aspects like reproducibility, distribution formats (OCI), extensibility (CRDs and operators), and GitOps-driven lifecycle management. Throughout, pay attention to practical constraints—upgrade sequencing, resource ownership, and multi-environment overlays—that commonly drive toolchoice.

<Frame>
  <img alt="The image is a section overview slide with a gradient background on the left, listing two topics: &#x22;A Kubernetes Overview&#x22; and &#x22;Current State of Package Management.&#x22;" />
</Frame>

Further reading and references:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm — The Kubernetes Package Manager](https://helm.sh/)
* [Kustomize — Template-free customization](https://kustomize.io/)
* [GitOps Principles and Practices](https://www.weave.works/technologies/gitops/)
* [OCI Image Specification](https://github.com/opencontainers/image-spec)

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/60afaf37-3ea5-4474-b262-dc8c13c3afd4/lesson/a2a6a7b0-066c-4227-9037-a344a963acbe)
