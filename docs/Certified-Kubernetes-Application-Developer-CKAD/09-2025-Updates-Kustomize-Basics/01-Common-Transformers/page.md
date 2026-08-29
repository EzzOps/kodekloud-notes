# Common Transformers

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Common-Transformers/page

Learn to modify and manage Kubernetes manifests efficiently using Kustomize's Common Transformers for consistent changes across multiple YAML files.

In this lesson, you'll learn how to efficiently modify and manage your Kubernetes manifests using Kustomize. Kustomize streamlines the process of updating common configurations across multiple YAML files by leveraging built-in transformers. This article focuses on a subgroup known as Common Transformers, which help you apply consistent changes such as labels, namespaces, prefixes/suffixes, and annotations without manually updating each resource.

Consider an example where you have a basic Deployment and Service defined in separate YAML files:

```yaml theme={null}
