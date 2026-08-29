# ArgoCD Application Specifications

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/ArgoCD-Application-Specifications/page

Explains Argo CD Application resource structure and key fields, creating applications, and how Argo CD syncs and deploys Kubernetes manifests from Git.

In this lesson we’ll cover the structure and key fields of an Argo CD Application resource — the core Kubernetes Custom Resource that describes a deployable software instance under GitOps control.

An Argo CD Application ties together:

* the source of truth for your desired state (Git repository, path, branch/tag, or chart),
* and the destination where those manifests should be applied (Kubernetes API server and namespace).

This document explains how to create an Application (CLI and manifest), what Argo CD does after creation, and a concise reference for the most important fields.

## Create an Application (CLI)

A common way to create an application is with the `argocd` CLI. The example below creates an application that points to a Git repository and a path inside that repo:

```bash theme={null}
argocd app create color-app \
  --repo https://github.com/sid/app-1.git \
  --path team-a/color \
  --dest-namespace color \
  --dest-server https://kubernetes.default.svc
