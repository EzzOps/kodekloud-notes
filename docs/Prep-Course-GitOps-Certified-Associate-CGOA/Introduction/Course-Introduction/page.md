# Course Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Introduction/Course-Introduction/page

Practical hands-on GitOps course teaching principles and patterns, Argo CD and tooling, secrets management, CI integration, observability, release strategies, labs, and certification preparation.

Welcome to the GitOps Certified Associate course.

I'm Siddharth, and I'll be your guide through GitOps—the modern, pull-based approach transforming how teams deploy and operate cloud-native applications. Organizations such as Spotify, Apple, Fidelity, and Intuit use GitOps to accelerate deployments, reduce human errors, and scale operations. CNCF surveys show GitOps adoption is growing across enterprises.

This course is practical and hands-on: you’ll work through labs, make mistakes safely, and learn by doing so you can apply GitOps patterns and tooling in real-world scenarios.

<Frame>
  <img alt="The image shows a split screen with a text-based task on the left explaining how to access a Gitea server and a terminal window on the right displaying a welcome message from KodeKloud. There is also a video overlay of a person speaking." />
</Frame>

<Callout icon="lightbulb">
  This course emphasizes labs and exercises so you can practice GitOps patterns and tooling in realistic scenarios.
</Callout>

## What you’ll learn (at a glance)

* GitOps fundamentals: continuous and declarative concepts, desired state, state drift, reconciliation, and feedback loops.
* GitOps principles: why Git as the single source of truth matters and the core principles that define GitOps.
* Reconciliation engines: hands-on with Argo CD and Argo Rollouts.
* Manifests and packaging: Kustomize, Helm charts, and OCI-based Git/registry workflows.
* Secrets management: working with Bitnami Sealed Secrets and `kubeseal`.
* Observability: integrating Prometheus, Grafana, and Alertmanager for metrics and alerts.
* CI integration: building pipelines that publish artifacts and update Git for pull-based delivery.
* Release patterns: rolling updates, recreate, blue/green, and canary releases.
* Metrics & best practices: DORA metrics, operational guardrails, and security-first practices.
* Mock exams and practice questions to validate readiness for certification.

## Course modules overview

| Module                    | Core Topics                                   | Example Tools                      |
| ------------------------- | --------------------------------------------- | ---------------------------------- |
| GitOps fundamentals       | Desired state, reconciliation, feedback loops | `Git`, Argo CD                     |
| Manifests & packaging     | Kustomize overlays, Helm charts               | `Kustomize`, `Helm`                |
| Secrets management        | Encrypting secrets for Git                    | Bitnami Sealed Secrets, `kubeseal` |
| Reconciliation & delivery | Pull-based deployments, rollouts              | Argo CD, Argo Rollouts             |
| CI integration            | Build, push, update Git workflow              | Jenkins, GitHub Actions            |
| Observability             | Metrics, dashboards, alerting                 | Prometheus, Grafana, Alertmanager  |
| Best practices & metrics  | DORA, security, IaC vs CaC                    | Various                            |

## Hands-on labs and learning approach

This course is lab-first. Each lesson pairs conceptual material with guided exercises so you can test patterns, iterate, and learn troubleshooting techniques that matter in production environments.

## GitOps patterns — storing secrets safely with Bitnami Sealed Secrets

A common, secure flow to keep secrets in Git using Bitnami Sealed Secrets:

1. Create a Kubernetes `Secret` manifest locally (without applying it to the cluster).
2. Encrypt that secret with `kubeseal` to produce a `SealedSecret`.
3. Commit the `SealedSecret` to Git; your GitOps controller (for example, Argo CD) will apply it and the Sealed Secrets controller will decrypt it inside the cluster.

Warning: Never commit plain `Secret` YAML (base64 or otherwise) to public repositories.

<Callout icon="warning">
  Always ensure the private key for Sealed Secrets remains secure. Only encrypted `SealedSecret` manifests belong in Git. Avoid storing unencrypted secrets or private keys in repositories.
</Callout>

Example: create a Secret manifest locally and produce a sealed secret

```bash theme={null}
