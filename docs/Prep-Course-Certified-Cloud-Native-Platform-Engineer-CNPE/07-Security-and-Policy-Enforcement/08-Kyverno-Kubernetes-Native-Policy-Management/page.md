# Kyverno Kubernetes Native Policy Management

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Kyverno-Kubernetes-Native-Policy-Management/page

Guide to Kyverno, a Kubernetes-native policy engine explaining validate, mutate, and generate rules, examples, comparisons with Gatekeeper, debugging, and rollout best practices.

Kyverno is a Kubernetes-native alternative to Gatekeeper that expresses policy using pure Kubernetes YAML. If you can write Kubernetes manifests, you can author Kyverno policies — no new language to learn.

In this guide we explain Kyverno’s three rule types (validate, mutate, generate), show concise policy examples and patterns, explain when to choose Kyverno over Gatekeeper, and cover debugging and common issues.

<Frame>
  <img alt="The image is a diagram listing learning objectives related to Kyverno, including understanding rule types, implementing policy patterns, and comparing Kyverno with Gatekeeper." />
</Frame>

## Overview: Kyverno rule types

A single `Policy` or `ClusterPolicy` resource can contain multiple rules of three types:

* validate — check resources and reject non-compliant objects (similar to Gatekeeper, but expressed in YAML pattern matching instead of Rego).
* mutate — modify resources (add defaults, labels, env vars, etc.) via a mutating admission webhook.
* generate — create related resources automatically when a matching resource is created (for example, create a default-deny `NetworkPolicy` when a Namespace is created).

<Frame>
  <img alt="The image outlines the three rule types in a Kyverno policy: Validate, Mutate, and a third unspecified type, emphasizing that Kyverno uses pure Kubernetes YAML." />
</Frame>

## Validate, Mutate, Generate — concise explanation

* Validate: Uses YAML pattern matching and wildcards to assert required fields and values. Rejections occur when the resource does not match the allowed pattern.
* Mutate: Runs as a mutating admission webhook and modifies the incoming resource before it is persisted. Useful for adding default labels, setting `imagePullPolicy`, injecting environment variables, etc.
* Generate: Automatically creates another resource in response to a matching resource creation (common for guardrails like `NetworkPolicy`, `ResourceQuota`, `LimitRange`, or service accounts).

<Frame>
  <img alt="The image outlines three types of rules in a Kyverno policy: Validate, Mutate, and Generate, emphasizing that Kyverno uses pure Kubernetes YAML with no new language to learn." />
</Frame>

## Examples

Below are minimal, copy-ready policy examples that illustrate common patterns.

### 1) Validation example — restrict image registries

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-registries
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: >
          Images must be from
          registry.company.com
        pattern:
          spec:
            containers:
              - image: "registry.company.com/*"
```

Key points:

* A single `ClusterPolicy` holds all rules (no templates, no Rego).
* `spec.validationFailureAction: Enforce` causes non-compliant objects to be rejected. Use `Audit` while testing.

<Callout icon="lightbulb">
  Use `validationFailureAction: Audit` during rollout to collect violations without blocking resources. Review `PolicyReport` and `ClusterPolicyReport` entries before switching to `Enforce`.
</Callout>

### 2) Mutate example — add a default label

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  rules:
    - name: add-team-label
      match:
        any:
          - resources:
              kinds: ["Deployment", "Service"]
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              managed-by: platform-team
```

Notes:

* `patchStrategicMerge` merges labels and will not overwrite an existing label value; it adds the label only if missing.
* Use `patchJson6902` for precise add/remove/replace operations at JSON paths.

### 3) Combine mutate + validate in one policy (pattern)

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: enforce-managed-by-label
spec:
  validationFailureAction: Enforce
  rules:
    - name: add-managed-by-label
      match:
        any:
          - resources:
              kinds: ["Deployment", "Service"]
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              managed-by: platform-team

    - name: require-managed-by-label
      match:
        any:
          - resources:
              kinds: ["Deployment", "Service"]
      validate:
        message: "The 'managed-by=platform-team' label is required"
        pattern:
          metadata:
            labels:
              managed-by: "platform-team"
```

Behavior:

* Resources without the label will have it added automatically by the mutate rule.
* If the label is removed later, the validate rule will reject updates that do not match (subject to webhook ordering and timing).

<Callout icon="warning">
  Mutations run before validations. Be aware of webhook ordering and timing: a validate rule may rely on a prior mutate rule to add required fields. Test to ensure the intended behavior.
</Callout>

### 4) Generate example — create a default-deny NetworkPolicy per Namespace

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: default-deny-ingress
spec:
  rules:
    - name: generate-default-netpol
      match:
        any:
          - resources:
              kinds: ["Namespace"]
      generate:
        kind: NetworkPolicy
        apiVersion: networking.k8s.io/v1
        name: default-deny-ingress
        namespace: "{{request.object.metadata.name}}"
        data:
          spec:
            podSelector: {}
            policyTypes: ["Ingress"]
```

Notes:

* The `namespace` field references the created Namespace using the expression `{{request.object.metadata.name}}`.
* Use `generate` to ensure guardrails are created automatically for new namespaces.

## Kyverno vs Gatekeeper — when to choose what

| Aspect          | Kyverno                                                     | Gatekeeper (OPA / Rego)                                          |
| --------------- | ----------------------------------------------------------- | ---------------------------------------------------------------- |
| Policy language | Pure Kubernetes YAML                                        | Rego                                                             |
| Rule types      | Validate, Mutate, Generate (in a single policy)             | Validate only                                                    |
| Best fit        | Mutation, simple-to-moderate validation using YAML patterns | Very complex validation logic requiring full Rego expressiveness |
| Learning curve  | Low for Kubernetes users                                    | Higher — must learn Rego                                         |
| Coexistence     | Can coexist with Gatekeeper (separate webhooks)             | Can coexist with Kyverno                                         |

Links and references:

* [Kyverno documentation](https://kyverno.io/docs/)
* [Gatekeeper / OPA documentation](https://www.openpolicyagent.org/)
* [Kubernetes admission controllers overview](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

<Frame>
  <img alt="The image is a comparison chart between Kyverno and OPA Gatekeeper, evaluating them based on complex logic, architecture, and exam weight. It highlights Kyverno's limited pattern matching and simpler YAML policies against OPA Gatekeeper's full Rego language and deeper Rego questions." />
</Frame>

Kyverno and Gatekeeper can run in the same cluster because they register independent admission webhooks.

## Debugging, status and common commands

* `kubectl get clusterpolicy` shows Kyverno ClusterPolicy objects and the READY column (policy loaded and valid).
* Kyverno emits `PolicyReport` and `ClusterPolicyReport` resources for audit-mode violations.
* Check controller logs when webhook errors occur.

Commands quick reference:

```bash theme={null}
