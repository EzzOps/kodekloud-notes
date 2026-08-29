# CEL Expressions Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/CEL-Expressions-Part-2/page

Guidance on advanced CEL usage in Kyverno to create configurable, content aware, and maintainable validation policies using params, celPreconditions, and variables.

In the previous lesson we learned how to write basic CEL expressions for Kyverno validation rules. In this installment we expand that foundation and demonstrate practical patterns that make CEL-based policies maintainable, configurable, and content-aware.

Quick recap:

* CEL is the standard language Kyverno uses for validation logic.
* Common built-in variables include `object`, `oldObject`, `namespaceObject`, and `request`.
* You can write `validate.cel` expressions to block or allow admission requests.

<Frame>
  <img alt="The image is a &#x22;Quick Recap&#x22; slide summarizing key points about CEL language in Kubernetes, including writing a basic rule and exploring core variables." />
</Frame>

## 1) Use parameter resources (`params`) to separate policy logic from environment configuration

Hard-coding environment-specific values inside policy expressions makes policies brittle and operationally expensive. For example, this simple enforce rule restricts Deployment replicas to fewer than 4:

```yaml theme={null}
validate:
  failureAction: Enforce
  cel:
    expressions:
      - expression: "object.spec.replicas < 4"
        message: "Deployment spec.replicas must be less than 4."
```

Problem: different environments (dev, staging, prod) often require different replica limits. With the hard-coded approach you must maintain multiple policy manifests or reapply changes each time limits change.

Kyverno supports parameter resources plus the `params` variable so you can keep logic in the policy and supply environment-specific configuration separately.

Refactor the previous rule to use a parameter resource:

```yaml theme={null}
validate:
  failureAction: Enforce
  cel:
    paramKind: # Defines the GroupVersionKind of the config resource
      apiVersion: rules.example.com/v1
      kind: ReplicaLimit
    paramRef: # Binds to a specific config resource by name
      name: "replica-limit"
    expressions:
      # The 'params' variable holds the data from our config resource
      - expression: "object.spec.replicas < params.maxReplicas"
        messageExpression: '"Deployment spec.replicas must be less than " + string(params.maxReplicas)'
```

Example parameter resource referenced by the policy:

```yaml theme={null}
apiVersion: rules.example.com/v1
kind: ReplicaLimit
metadata:
  name: "replica-limit"
maxReplicas: 4
```

Benefits:

* Adjust deployment limits by editing a single parameter resource — policy manifests remain unchanged.
* Use different parameter resources per namespace or environment and bind policies accordingly.
* You can use native Kubernetes resources (for example, a `ConfigMap`) as the parameter resource as long as Kyverno can read it.

<Callout icon="lightbulb">
  Parameter resources can be a custom resource or native types like `ConfigMap`. Kyverno exposes the selected resource to CEL via the `params` variable so your policy logic remains environment-agnostic.
</Callout>

## 2) Filter by content with CEL preconditions

`match` and `exclude` select resources by metadata (kinds, names, labels), but they are limited when you need to inspect nested fields. Use `celPreconditions` as a content-aware gate: they evaluate after `match` and before the main `validate` logic runs.

Goal: enforce that any `Service` of type `NodePort` must set `externalTrafficPolicy: Local`.

```yaml theme={null}
rules:
  - name: validate-nodeport-trafficpolicy
    match:
      any:
        resources:
          kinds:
            - Service
    celPreconditions:
      - expression: "object.spec.type == 'NodePort'"
    validate:
      cel:
        expressions:
          - expression: "object.spec.externalTrafficPolicy == 'Local'"
            message: "NodePort Services must use externalTrafficPolicy: Local."
```

How this flows:

1. `match` selects all `Service` resources.
2. `celPreconditions` evaluates; only Services with `object.spec.type == 'NodePort'` proceed to validation.
   * Services that are `ClusterIP` or `LoadBalancer` will skip the rule entirely (no error).
3. `validate.cel` runs for resources that pass preconditions and enforces the required field.

This lets you write concise validation expressions and avoid applying rules to irrelevant resources.

<Frame>
  <img alt="The image is a slide titled &#x22;Fine-Grained Matching: CEL Preconditions&#x22; with a goal stating that for service resources of type NodePort, the externalTrafficPolicy should be enforced as Local." />
</Frame>

## 3) Reduce repetition with `variables` to build reusable expressions

Complex policies often need to aggregate fields like all containers in a Pod spec (containers, initContainers, ephemeralContainers). Repeating the same aggregation in multiple expressions makes rules verbose and error-prone.

Example (repetitive, hard to read):

```yaml theme={null}
validate:
  cel:
    expressions:
      # Check 1: No 'latest' tag
      - expression: >
          (object.spec.containers + object.spec.?initContainers.orValue([]) +
          object.spec.?ephemeralContainers.orValue([])).all(c, !c.image.endsWith(':latest'))
      # Check 2: All images from my-registry
      - expression: >
          (object.spec.containers + object.spec.?initContainers.orValue([]) +
          object.spec.?ephemeralContainers.orValue([])).all(c, c.image.startsWith('my-registry/'))
```

Solution: define the aggregation once with `variables` and reference it in expressions. This improves readability and maintainability.

<Frame>
  <img alt="The image explains the concept of a 'variables' block, which helps define an expression once and give it a name, enhancing readability, reusability, and maintainability. It includes text from KodeKloud." />
</Frame>

Refactored using `variables`:

```yaml theme={null}
cel:
  variables:
    # Define the complex logic ONCE and give it a clean name.
    - name: allContainers
      expression: >-
        object.spec.containers +
        object.spec.?initContainers.orValue([]) +
        object.spec.?ephemeralContainers.orValue([])
  expressions:
    # Now our validation checks are simple, clean, and easy to read!
    - name: "check-for-latest-tag"
      expression: "variables.allContainers.all(c, !c.image.endsWith(':latest'))"
    - name: "check-registry"
      expression: "variables.allContainers.all(c, c.image.startsWith('my-registry/'))"
```

Advantages:

* Single source of truth for the container aggregation logic.
* Validation expressions become concise and self-documenting.
* Changes (e.g., include/exclude ephemeral containers) require a single edit in `variables`.

## Quick reference: common CEL/Kyverno built-ins

| Variable          | Description                                               | Example usage                            |
| ----------------- | --------------------------------------------------------- | ---------------------------------------- |
| `object`          | The new resource being admitted                           | `object.spec.replicas`                   |
| `oldObject`       | The existing resource stored in the cluster (for updates) | `oldObject.spec.template`                |
| `namespaceObject` | The Namespace resource of the object's namespace          | `namespaceObject.metadata.labels['env']` |
| `request`         | Admission request metadata (user, operation)              | `request.operation == 'CREATE'`          |
| `params`          | Parameter resource bound via `paramKind` / `paramRef`     | `params.maxReplicas`                     |
| `variables`       | User-defined named expressions within the `cel` block     | `variables.allContainers`                |

## Summary — Patterns to make CEL policies robust and maintainable

| Feature                                | Purpose                                                    | When to use                                                                           |
| -------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Parameter resources (`params`)         | Decouple configuration from policy logic                   | When limits or environment-specific settings vary across clusters/namespaces          |
| CEL preconditions (`celPreconditions`) | Filter resources by content before validation              | When `match`/`exclude` are insufficient because the decision depends on nested fields |
| Variables block (`variables`)          | Factor complex CEL expressions into named, reusable pieces | When multiple expressions share the same complex logic (e.g., container aggregation)  |

<Frame>
  <img alt="The image is a summary of key concepts related to Kubernetes validation using Kyverno, including details about validate.cel, core variables, parameters, and preconditions, presented with a colorful numbered design." />
</Frame>

Helpful links and references

* Kyverno documentation: [https://kyverno.io/documentation/](https://kyverno.io/documentation/)
* CEL (Common Expression Language) spec: [https://github.com/google/cel-spec](https://github.com/google/cel-spec)
* Kubernetes admission control concepts: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

<Callout icon="warning">
  When using `paramKind` with custom resources, ensure the referenced resource exists and Kyverno has permission to read it. A missing or inaccessible parameter resource will prevent the policy from evaluating as intended.
</Callout>

That's it for this lesson — with `params`, `celPreconditions`, and `variables` you can author Kyverno CEL policies that are configurable, precise, and easy to maintain.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/a2f7ecdd-5b80-48ac-bfdd-ae5c16309bbe" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/3d530bb8-e36f-4d61-b886-6d088dfd808f" />
</CardGroup>
