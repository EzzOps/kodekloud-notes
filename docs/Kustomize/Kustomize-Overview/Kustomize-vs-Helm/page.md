# Kustomize vs Helm

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Overview/Kustomize-vs-Helm/page

This article compares Helm and Kustomize, two tools for managing Kubernetes manifests, highlighting their strengths, workflows, and trade-offs.

In this article, we’ll compare **Helm** and **Kustomize**—two popular methods for managing Kubernetes manifests across different environments. Understanding their strengths, workflows, and trade-offs will help you select the best fit for your project.

## How Helm Works: Go-Templating in YAML

Helm uses Go templates to inject dynamic values into your Kubernetes manifests. Placeholders in the form of `{{ .Values.variable }}` are replaced at deploy time based on a `values.yaml` file.

```yaml theme={null}
