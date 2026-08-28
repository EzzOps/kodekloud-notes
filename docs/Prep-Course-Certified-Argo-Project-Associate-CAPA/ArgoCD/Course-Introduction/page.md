# Course Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Course-Introduction/page

Explains how GitOps and the Argo Project (Argo CD, Workflows, Rollouts, Events) solve Kubernetes operational problems like configuration drift, security risks, and unreliable recovery

We begin by identifying common DevOps challenges and then show how GitOps—and specifically the Argo project—resolves them.

Before examining what Argo does, let's start with why this approach matters. The following story about a fictional company, Dasho, illustrates the typical pitfalls teams encounter when moving to Kubernetes and infrastructure-as-code.

The situation will feel familiar to many.

Dasho believed they were doing things correctly. They were migrating to a modern multi-cloud Kubernetes platform and wanted an infrastructure-as-code mindset. Their first attempt, however, was incomplete.

A few developers applied changes manually against the cluster, while a few others committed changes to a single Git branch. With little automation and inconsistent version control, it quickly became impossible to track who changed what and when.

They recognized the problem and added a CI/CD pipeline, which was a step forward — but it had a major flaw: it was a push-based pipeline, and the team’s culture did not shift. Developers still found it faster to run kubectl commands directly on the live cluster, bypassing the pipeline. For example, several different manifests were manually applied to the cluster:

```bash theme={null}
