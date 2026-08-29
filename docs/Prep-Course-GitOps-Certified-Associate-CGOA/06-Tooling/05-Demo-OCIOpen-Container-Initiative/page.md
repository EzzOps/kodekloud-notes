# Demo OCIOpen Container Initiative

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/Demo-OCIOpen-Container-Initiative/page

How to package, push, pull, and install Helm charts as OCI artifacts to registries like Docker Hub, including authentication, commands, and GitOps integration with Argo CD and Flux

Until now we have used [Git](https://learn.kodekloud.com/user/courses/git-for-beginners) as the single source of truth for declarative manifests. This lesson shows how to store and distribute Helm charts as OCI artifacts using an OCI-compatible registry (for example, Docker Hub). Many registries implement the OCI Distribution Specification — Docker Hub can host container images and other OCI artifacts such as Helm charts, SBOMs, digital signatures, and vulnerability reports.

Below is a compact, corrected walkthrough that packages a Helm chart named `highway-chart`, pushes it to Docker Hub's OCI registry, and then pulls and installs it from the registry. The examples use the Docker Hub username `siddharth67`; replace it with your own when running commands.

> **lightbulb** Ensure you are using Helm 3.x with OCI support. Helm 3.8+ includes built-in OCI support; some older 3.x releases required experimental flags or community plugins. Also confirm your Docker Hub credentials (password or Personal Access Token) before running `helm registry login`.

## Prerequisites

* Helm 3.x installed and on your PATH.
* A Docker Hub account (or another OCI registry) and credentials.
* kubectl configured for your target cluster if you plan to install the chart.

## 1) Create and package a Helm chart

If you do not already have a chart, scaffold one:

```bash theme={null}
helm create demo
```

Package a chart into a tarball:

```bash theme={null}
helm package demo
