# Section Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Tooling/Section-Introduction/page

Overview comparing Kubernetes manifests, Helm, and Glasskube, assessing reproducibility, templating, lifecycle operations, and operational complexity to help choose the right package management tool.

Welcome to the tooling section.

This article examines the primary tools for managing packages and applications in Kubernetes clusters. Over the past decade Kubernetes has grown rapidly: each release adds features, and the ecosystem of installable packages keeps expanding. However, package-management tooling has not always kept pace—many teams still rely on raw Kubernetes manifests or Helm charts authored and maintained by hand.

Here we'll compare three approaches—plain Kubernetes manifests, Helm, and Glasskube—covering their common use cases, strengths, and trade-offs. The intent is to help you choose the right tool for your workflow, whether you prioritize simplicity, templating power, or an opinionated package manager.

> **lightbulb** This section focuses on trade-offs you should consider: reproducibility, templating and parameterization, lifecycle operations (install/upgrade/rollback), and operational complexity. Keep these dimensions in mind as you evaluate each tool.

<Frame>
  <img alt="The image is a section overview with a gradient background, listing three topics: Kubernetes Manifests, Helm, and Glasskube, each numbered sequentially." />
</Frame>

The diagram above summarizes the three topics we'll cover: Kubernetes manifests, Helm, and Glasskube. Below are concise descriptions and comparisons to help you decide which approach best matches your team’s needs.

Summary comparison

| Tool                 | Typical use case                                                                                  |                                                                                               Strengths | Limitations                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------: | -------------------------------------------------------------------------------- |
| Kubernetes manifests | Small deployments, simple clusters, or when you want fully explicit resources                     |                                        Minimal tooling, directly readable YAML, no templating surprises | Repetition across environments, harder to parameterize and manage upgrades       |
| Helm                 | Medium-to-large deployments requiring templating, reusable charts, and release management         | Powerful templating, dependency management, `helm` release lifecycle (`install`, `upgrade`, `rollback`) | Template complexity can grow, learning curve, potential for subtle template bugs |
| Glasskube            | Opinionated package manager focused on curated, consistent installs (primary focus of this guide) |                         Simplified package management, consistent lifecycle semantics, curated packages | Requires buy-in to Glasskube conventions and ecosystem                           |

Key examples and commands

* Raw manifests: apply with `kubectl apply -f <manifest.yaml>`
* Helm: install with `helm install <release> <chart>`; upgrade with `helm upgrade <release> <chart>`
* Glasskube: covered in depth later—we’ll show installation, configuration, and package lifecycle commands in dedicated sections.

What follows

* A closer look at plain Kubernetes manifests: when they make sense and how to keep them maintainable.
* Helm deep dive: templating patterns, chart best practices, and common pitfalls.
* Glasskube walkthrough: features, workflow examples, and why it may be a better fit for teams that want a curated package experience.

References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm — The Kubernetes Package Manager](https://helm.sh/)

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/140a6ea0-1539-4d23-9aa6-0d07654a4526/lesson/4cae76fc-e196-4dad-8127-0aaef2569f5a)
