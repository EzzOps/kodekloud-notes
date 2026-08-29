# CEL Expressions Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/CEL-Expressions-Part-1/page

Introducing CEL usage in Kyverno for concise admission-time validation rules and namespace aware policies

Kyverno makes it straightforward to implement Pod Security Standards and other admission-time controls. In this lesson we introduce the `validate.cel` sub-rule to create concise, powerful validation logic using CEL (Common Expression Language).

What is CEL?

CEL (Common Expression Language) is an open-source, embeddable expression language from Google. It is designed for safe, fast evaluation inside critical components like admission controllers and API servers. CEL deliberately avoids Turing-completeness so expressions are guaranteed to terminate quickly, preventing runaway CPU or memory usage. Its guiding principles are simplicity, security, portability, and performance—qualities that make it a natural fit for policy and validation in Kubernetes.

<Frame>
  <img alt="The image lists reasons for using the Common Expression Language (CEL): open-source, non-Turing complete, and designed for safety." />
</Frame>

CEL is being adopted across the Kubernetes ecosystem for CRD validation, validating admission policies, and mutating admission policies. Learning CEL for Kyverno gives you a transferable skill set for writing policies across Kubernetes tooling.

Using CEL in Kyverno

Kyverno exposes CEL via the `validate.cel` sub-rule. Inside a rule's `validate` block you add a `cel` block containing a list of expressions. Each expression must include:

* `expression`: a CEL expression that must evaluate to `true` for the request to be allowed.
* `message`: the user-facing error message shown when the expression evaluates to `false`.

Example — require Deployment replicas to be less than 4:

```yaml theme={null}
rules:
  - name: deployment-replicas-limit
    match:
      resources:
        kinds:
          - Deployment
    validate:
      failureAction: Enforce
      cel:
        expressions:
          - expression: "object.spec.replicas < 4"
            message: "Deployment spec.replicas must be less than 4."
```

This example uses the `object` variable, which represents the full resource being submitted to the API server. We access `object.spec.replicas` to inspect the Deployment replica count.

<Callout icon="lightbulb">
  CEL expressions must evaluate to a boolean. If an expression returns `false` (or a non-boolean that cannot be interpreted as true), the request is rejected and the provided `message` is shown.
</Callout>

Namespace-aware validation

Policy decisions often depend on where a resource will be created. Kyverno exposes `namespaceObject` to make namespace-aware checks straightforward. While `object` is the resource being created (for example, a StatefulSet), `namespaceObject` contains the full Namespace resource where the object will live.

Example — allow StatefulSets only in the `production` namespace:

```yaml theme={null}
rules:
  - name: statefulset-namespace
    match:
      any:
        - resources:
            kinds:
              - StatefulSet
    validate:
      failureAction: Enforce
      cel:
        expressions:
          - expression: "namespaceObject.metadata.name == 'production'"
            message: "StatefulSets must be in the 'production' namespace."
```

If a user attempts to create a StatefulSet in a different namespace (e.g., `default`), that expression evaluates to `false` and the request is blocked.

CEL variables available in Kyverno

The most commonly used variables in Kyverno CEL expressions provide runtime context for expressive policies:

<Frame>
  <img alt="The image lists available CEL variables with descriptions for each, including object, oldObject, request, namespaceObject, params, and authorizer." />
</Frame>

* object\
  The incoming resource manifest being created or updated. Example: `object.spec.replicas`.
  <Callout icon="lightbulb">
    Note: For delete operations, `object` is `null` because there is no incoming resource body.
  </Callout>

* oldObject\
  The current cluster version of the resource (available for updates). Use this to compare previous and new state.

* request\
  Metadata about the admission request (user identity, operation type, `dryRun` flag, etc.). Useful for policies that depend on who performed the action or how it was requested.

* namespaceObject\
  The Namespace resource where the object will be created. Useful to read labels, annotations, or the namespace name itself.

* params\
  External parameters injected into the policy (for example, via a ConfigMap or Kyverno params binding). Use `params` to avoid hard-coding values and make policies reusable.

* authorizer\
  Provides on-the-fly authorization checks (advanced). For example, validate that the requester has permission to `get` a referenced Secret. See Kyverno docs for details: [https://kyverno.io/docs/](https://kyverno.io/docs/)

Quick reference table

|          Variable | What it contains                                   | Common example usage                                                            |
| ----------------: | -------------------------------------------------- | ------------------------------------------------------------------------------- |
|          `object` | Incoming resource being created or updated         | `object.metadata.labels.owner == 'team-a'`                                      |
|       `oldObject` | Resource version stored in cluster (for updates)   | `object.spec.replicas > oldObject.spec.replicas`                                |
|         `request` | Admission request metadata                         | `request.userInfo.username == 'admin'`                                          |
| `namespaceObject` | The Namespace resource for the target namespace    | `namespaceObject.metadata.labels.environment == 'prod'`                         |
|          `params` | External parameters passed into the policy         | `object.spec.replicas <= params.maxReplicas`                                    |
|      `authorizer` | Authorization helper for dynamic permission checks | `authorizer.resourceAllowed('get', 'v1', 'Secret', object.spec.tls.secretName)` |

Summary

* CEL is a safe, performant expression language well-suited for admission-time validation.
* Kyverno exposes CEL through `validate.cel`, letting you author concise validation rules that run on admission.
* Use variables like `object`, `oldObject`, `request`, `namespaceObject`, `params`, and `authorizer` to write context-aware policies.
* Keep expressions simple and boolean-returning; use `params` for reusable policies and `namespaceObject` for namespace-scoped constraints.

<Frame>
  <img alt="The image is a summary slide with four points about CEL and its use in Kubernetes, specifically regarding Kyverno's validation, object variables, and update operations. Each point is marked with a numbered header in a colored label on the right." />
</Frame>

Further reading and references

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes CRD validation and CEL: [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation)

That's it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/f9c71d88-0851-4308-b17a-1fd3917f571b" />
</CardGroup>
