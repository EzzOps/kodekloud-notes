# Configuration Templating Parameterization and Environment Management

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/GitOps-and-Continuous-Delivery/Configuration-Templating-Parameterization-and-Environment-Management/page

Comparison of Helm and Kustomize for templating and patching Kubernetes manifests across environments.

We designed a clean repo layout with `base/` and `overlays/` directories, but the YAML files in `base/` are static and contain hard-coded values. When you need the same application deployed across multiple environments with different replicas, images, or resource limits, copying and pasting manifests is the naive — and fragile — approach.

In this lesson we compare two practical approaches to parameterize and manage environment differences: Helm (template-driven) and Kustomize (patch-driven). Both solve the copy‑paste problem differently, and both integrate with GitOps tools such as Argo CD and Flux.

* Why copy-and-paste YAML does not scale
* How Helm templates and Kustomize overlays address parameterization
* When to choose Helm vs. Kustomize and how they fit into GitOps workflows

<Frame>
  <img alt="The image outlines three learning objectives related to YAML, Helm, and Kustomize. It includes points about understanding YAML's limitations, Helm templates, and comparing Helm with Kustomize." />
</Frame>

## Why copy–paste configuration is a problem

Imagine a healthcare platform team running three microservices across three environments (dev, staging, prod). For each service and environment they maintain separate Deployment, Service, and Ingress YAML files — dozens of nearly identical manifests.

One engineer updates a health-check path in most files but misses three files for the staging payment service. Staging health checks silently fail for two weeks because the alerting channel was archived. The root cause: manual copy-and-paste configuration. This pattern causes:

* Configuration drift across environments
* Tedious, error-prone updates
* Hard-to-audit differences and silent failures

> **warning** Avoid maintaining environment-specific manifests by copying files. Copy‑paste leads to drift, missed updates, and increased operational risk.

<Frame>
  <img alt="The image depicts a platform infrastructure configuration with three environments: Dev, Staging, and another Dev, each containing services for Patient, Appointment, and Payment. Each service consists of multiple microservices labeled &#x22;ms&#x22; with corresponding numbers." />
</Frame>

When manifests are 90% identical, the meaningful 10% difference is hard to spot — like finding a needle in a haystack. Typos, missed updates, and inconsistent naming are common and costly.

<Frame>
  <img alt="The image outlines issues related to &#x22;Copy-Paste Configuration,&#x22; including drift between environments, tedious updates, hard-to-audit differences, and human error." />
</Frame>

## Why YAML alone isn't enough

YAML is a data serialization format, not a programming language. It lacks variables, conditionals, loops, and cross-file references. Anchors and aliases can reduce duplication inside a single file, but they cannot:

* Reference values from other files or environments
* Provide conditional logic or iteration across manifests

To manage differences between environments, use external tooling that either generates or patches YAML based on parameters.

> **lightbulb** YAML anchors and aliases reduce repetition within a single file, but they are not a replacement for templating or overlay tools when managing multiple environments.

<Frame>
  <img alt="The image explains that YAML does not have variables but uses anchors and aliases, which only work within a single file and cannot reference external values." />
</Frame>

## Two pragmatic solutions: Helm (templating) and Kustomize (patching)

Both Helm and Kustomize transform a canonical manifest into environment-specific manifests, but they take different approaches. Both are supported by GitOps platforms:

* Argo CD: [https://learn.kodekloud.com/user/courses/gitops-with-argocd](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* Flux CD: [https://learn.kodekloud.com/user/courses/gitops-with-fluxcd](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)

## Helm (template-driven)

* Helm uses Go templates to generate Kubernetes YAML. You author template files with placeholders and logic, and you supply `values.yaml` files for environment-specific values.
* Helm Charts are packageable and versioned. A large ecosystem of community charts is available via Artifact Hub: [https://artifacthub.io/](https://artifacthub.io/)
* Templates support loops, conditionals, and functions, making Helm expressive for complex parameterization.
* Downside: Go template syntax (curly braces, pipelines, dot notation) can be tricky to read and debug in complex charts.

Minimal Helm chart example:

```yaml theme={null}
