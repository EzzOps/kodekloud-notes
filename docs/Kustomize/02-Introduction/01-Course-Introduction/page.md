# Course Introduction

Source: https://notes.kodekloud.com/docs/Kustomize/Introduction/Course-Introduction/page

This course teaches deploying and customizing Kubernetes resources using Kustomize, covering core features, CI/CD integration, and a capstone project.

Welcome to the **Kustomize** course! I’m **Sanjeev Thiyagarajan**, and I’ll guide you through deploying and customizing Kubernetes resources across multiple environments. By the end of this course, you’ll master Kustomize’s core features, integrate it into CI/CD pipelines, and complete a capstone project.

## What You’ll Learn

| Module                        | Description                                                                                  |
| ----------------------------- | -------------------------------------------------------------------------------------------- |
| Why Kustomize Was Created     | Understand the challenges in Kubernetes manifests and how Kustomize simplifies customization |
| Installing Kustomize          | Install Kustomize locally and configure prerequisites                                        |
| Defining `kustomization.yaml` | Learn the syntax, reference resources, and organize overlays                                 |
| Basic Resource Example        | Create a simple Deployment and Service with Kustomize                                        |
| Advanced Features             | Explore transformers, patches, components, generators (ConfigMaps & Secrets)                 |
| CLI Subcommands               | Use `kustomize edit`, `kustomize set`, and other subcommands in CI/CD                        |
| Hands-On Labs                 | Practice after each lecture with interactive challenges                                      |
| Final Project                 | Apply all features in a capstone deployment                                                  |
| Community Support             | Join our [Slack channel](https://example.com/slack) for Q\&A and peer assistance             |

> **lightbulb** Kustomize is now built into `kubectl` (v1.14+). You can run `kubectl kustomize` instead of installing a separate binary.

***

## What’s Next?

Now that you know the course structure, we’ll dive into Kustomize’s core features:

1. **Transformers & Patches** – Modify fields without touching original YAML.
2. **Overlays & Components** – Compose reusable customization layers.
3. **Generators** – Automate ConfigMap and Secret creation.
4. **CLI Workflow** – Leverage `kustomize build`, `edit`, `set`, and `apply`.

Ready to customize your first Kubernetes manifest? Let’s jump in!

***

## Links and References

* [Kustomize GitHub Repository](https://github.com/kubernetes-sigs/kustomize)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubectl Plugin: kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kustomize/module/a9725b74-2c5d-4eac-9063-caddf9d52e5a/lesson/7d0459bc-850c-4a98-ba40-2b89102ef54e)
