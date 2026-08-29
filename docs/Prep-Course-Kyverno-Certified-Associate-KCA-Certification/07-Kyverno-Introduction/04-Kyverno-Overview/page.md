# Kyverno Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-Introduction/Kyverno-Overview/page

Overview of Kyverno, a Kubernetes-native policy engine that validates, mutates, and generates resources to enforce security, compliance, and standardization across clusters

This article answers two fundamental questions: what is Kyverno, and why use it to secure and standardize Kubernetes clusters?

Meet Alex.

Like many platform engineers, Alex is responsible for keeping Kubernetes clusters secure and predictable while enabling developer velocity. They want to enforce best practices without disrupting normal workflows.

<Frame>
  <img alt="The image illustrates a platform engineer named Alex managing Kubernetes clusters, with a note indicating that developers frequently deploy new services." />
</Frame>

Common risks Alex faces include missing labels, untrusted images, containers running as root, and non-standard ConfigMaps.

Developers sometimes deploy containers running as root — a major security risk that can lead to privilege escalation.

<Frame>
  <img alt="The image illustrates a sequence starting with developers, leading to container pods, and ending with containers running as the root user. It highlights a security concern with containers running as root." />
</Frame>

Other challenges are using images from unvetted registries and removing resource limits to make an application work. Both can destabilize clusters and impact critical workloads.

<Frame>
  <img alt="The image illustrates a process flow where developers remove memory and CPU limits, leading to outages, titled &#x22;Chaos in the Cluster.&#x22;" />
</Frame>

Configuration mistakes — for example, placing team ConfigMaps in the wrong namespace — can break deployments and create outages.

<Frame>
  <img alt="The image illustrates issues in a cluster, highlighting &#x22;Chaos in the Cluster&#x22; with steps from &#x22;Exposing secrets in ConfigMaps&#x22; to &#x22;Failed App Configuration,&#x22; accompanied by symbols indicating errors." />
</Frame>

Left unchecked, Alex spends most of their time in reactive firefighting, repeatedly fixing configurations with `kubectl`. This is where Kyverno becomes valuable.

Kyverno is a Kubernetes-native policy engine that uses admission webhooks to intercept create and update requests. It evaluates resources before they are persisted and provides three core capabilities:

* Validate — block or allow requests based on rules.
* Mutate — modify incoming resources to conform to standards (for example, add labels or set `securityContext`).
* Generate — create new resources automatically (for example, create a ConfigMap or Role when a namespace is created).

<Frame>
  <img alt="The image is an illustration titled &#x22;Kyverno to the Rescue&#x22; describing a Kubernetes-native policy engine. It highlights three key functions: validating resources, mutating resources, and generating resources." />
</Frame>

Before a Pod, Deployment, or ConfigMap is created, Kyverno checks it against your policies. For example, Kyverno can:

* Block containers that run as root.
* Require labels on resources.
* Mutate ConfigMaps to meet naming conventions.

Kyverno can also evaluate generic JSON payloads using JMESPath expressions when necessary. This guide focuses on Kyverno's native YAML policy features.

<Frame>
  <img alt="The image is a presentation slide about &#x22;Kyverno to the Rescue&#x22; and highlights its features like blocking containers running as root, ensuring resources have labels, mutating ConfigMaps for naming conventions, and working with generic JSON payloads." />
</Frame>

<Callout icon="lightbulb">
  Kyverno policies are plain Kubernetes YAML (no new DSL). They follow familiar `apiVersion`, `kind`, `metadata`, and `spec` structures, so teams can adopt policies quickly and integrate them into existing GitOps pipelines.
</Callout>

How Kyverno works in practice

* Validation: enforce security and compliance by rejecting nonconforming resources.
* Mutation: auto-remediate resources to meet cluster conventions.
* Generation: provision helper resources automatically to reduce manual steps.

Below are concise YAML examples that show each capability in action.

Validate example — block containers running as root

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-root-containers
spec:
  validationFailureAction: enforce
  rules:
  - name: validate-no-root
    match:
      resources:
        kinds: ["Pod", "Deployment"]
    validate:
      message: "Running as root is not allowed. Set securityContext.runAsNonRoot: true"
      pattern:
        spec:
          containers:
          - securityContext:
              runAsNonRoot: true
```

Mutate example — add a required label automatically

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-required-label
spec:
  rules:
  - name: add-team-label
    match:
      resources:
        kinds: ["Pod", "Deployment"]
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            team: platform
```

Generate example — create a namespace ConfigMap when a namespace is created

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-namespace-config
spec:
  rules:
  - name: create-configmap
    match:
      resources:
        kinds: ["Namespace"]
    generate:
      kind: ConfigMap
      name: team-config
      synchronize: true
      data:
        owner: "platform"
```

<Callout icon="warning">
  Policies enforced cluster-wide can block legitimate workloads if misconfigured. Start in `audit` mode (`validationFailureAction: audit`) to observe changes before switching to `enforce`.
</Callout>

Summary — Kyverno capabilities at a glance

| Capability | Purpose                                                          | Example                                                             |
| ---------: | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
|   Validate | Enforce policies by blocking noncompliant create/update requests | `disallow-root-containers` (reject Pods with `runAsNonRoot: false`) |
|     Mutate | Automatically modify resources to comply with standards          | `add-required-label` (inject `team` label)                          |
|   Generate | Create auxiliary resources to reduce manual setup                | `generate-namespace-config` (create ConfigMap per namespace)        |

Links and references

* Kyverno official docs: [https://kyverno.io/](https://kyverno.io/)
* Kyverno GitHub: [https://github.com/kyverno/kyverno](https://github.com/kyverno/kyverno)
* Kubernetes `kubectl` reference: [https://kubernetes.io/docs/reference/kubectl/overview/](https://kubernetes.io/docs/reference/kubectl/overview/)
* JMESPath: [https://jmespath.org/](https://jmespath.org/)

Next steps

1. Try a simple validation policy in audit mode to see violations without blocking deployments.
2. Add safe mutation policies (labels, resource requests/limits) to enforce standards.
3. Use generation to automate standard ConfigMaps, Roles, or Secrets when namespaces are created.

Kyverno fits naturally into Kubernetes-native workflows, helping platform teams like Alex move from reactive fixes to proactive governance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/8cf118e1-7ca8-49b6-be5a-af80c331f394/lesson/8d6e1ffe-6a27-498c-9534-60b0ac726d2d" />
</CardGroup>
