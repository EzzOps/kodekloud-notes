# Common Transformers

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Common-Transformers/page

This article explores Kustomizes Common Transformers for applying shared modifications to Kubernetes manifests efficiently.

In this lesson, we’ll explore Kustomize’s built-in Common Transformers. They let you apply shared modifications—such as labels, prefixes/suffixes, namespaces, and annotations—to all of your Kubernetes manifests without touching each file manually.

## The Challenge

Imagine you have these two resource definitions:

```yaml theme={null}
