# At the rule or policy level, set validationFailureAction to "enforce" if required
validationFailureAction: enforce
validate:
  message: "Updating/deleting the resource is not allowed"
  deny: {}
```

> **warning** Use an empty `deny: {}` with caution. It will unconditionally block any request that reaches the rule, so ensure `match` and `exclude` are precise.

Best practices and tips

* Use `match` and `exclude` to narrowly target the resources and users affected by the rule.
* Prefer specific deny conditions (using `any`/`all`) over an unconditional `deny: {}` unless you truly want a default-deny behavior.
* Test deny rules in a staging cluster before enforcing them in production.
* Reference admission fields using JMESPath: common keys include `request.operation`, `request.userInfo.username`, `request.userInfo.groups`, and fields inside `request.object` or `request.oldObject`.

Links and references

* [Kyverno documentation — Validation](https://kyverno.io/docs/writing-policies/validate/)
* [JMESPath tutorial](https://jmespath.org/tutorial.html)

That's it for deny rules — they let you express powerful, context-aware policies by evaluating the full admission request in real time.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/79efb0c3-d76b-42e8-b9b5-27ec7a2c4e85)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/59f7d445-cee2-4113-a806-95f1cefd076f)


# Failure Action Overrides

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Failure-Action-Overrides/page

Explains Kyverno's failureActionOverrides for ClusterPolicies, allowing namespace specific enforcement or audit of validation rules to avoid duplicating policies.

Kyverno policies operate in two primary modes: `Audit` and `Enforce`. In many clusters you’ll want a single ClusterPolicy to behave differently depending on the target namespace—for example, strict enforcement in production but only auditing elsewhere. The `failureActionOverrides` field enables exactly that by letting you override a rule’s default `failureAction` for specific namespaces.

> **lightbulb** Use `failureActionOverrides` to keep one ClusterPolicy that adapts per-namespace behavior instead of duplicating policies. This reduces policy sprawl and makes intent clearer.

What is `failureActionOverrides`?

* It’s an optional block you add inside a rule’s `validate` section.
* It creates namespace-specific exceptions to the rule’s default `failureAction`.
* It is only supported for `ClusterPolicy` objects because those policies span multiple namespaces.

<Frame>
  <img alt="The image is a slide introducing &#x22;failureActionOverrides,&#x22; explaining that it allows creating exceptions for &#x22;failureAction&#x22; in specific namespaces, available for &#x22;ClusterPolicies.&#x22;" />
</Frame>

How it works

* Define a default `failureAction` for the rule (commonly `Audit` or `Enforce`).
* Use `failureActionOverrides` to list namespaces and the alternate `action` to apply there.
* Kyverno evaluates the rule and, if the resource’s namespace matches an override entry, applies the override action instead of the default.

Example: require an `app` label, audit by default, but enforce in `production`:

```yaml theme={null}
rules:
  - name: check-label-app
    match:
      any:
        - resources:
            kinds:
              - Pod
    validate:
      failureAction: Audit
      failureActionOverrides:
        - action: Enforce   # Action to apply for these namespaces
          namespaces:       # List of affected namespaces
            - "production"
      message: "The label `app` is required."
      pattern:
        metadata:
          labels:
            app: "?*"
```

Behavior examples

* Production namespace: When a Pod is created in `production`, Kyverno finds the matching `failureActionOverrides` entry. The effective action becomes `Enforce`. If the Pod lacks the `app` label, admission is blocked and the request fails.

<Frame>
  <img alt="The image explains the behavior of a pod creation in a 'production' namespace, emphasizing that requests are blocked if the label is missing, given the 'failureAction' is set to 'Enforce'." />
</Frame>

* Non-overridden namespaces (e.g., `development`): Kyverno applies the rule’s default `failureAction` (`Audit` in the example). A missing `app` label is recorded as a violation but the Pod is admitted.

Quick summary

|                   Namespace type | Effective action | Result when `app` label is missing   |
| -------------------------------: | ---------------- | ------------------------------------ |
|      `production` (in overrides) | `Enforce`        | Admission is blocked                 |
| `development` (not in overrides) | `Audit`          | Violation is logged, request allowed |

Deprecated top-level syntax
You may encounter an older, deprecated pattern where validation failure action overrides were defined at the policy `spec` level. Avoid this in new ClusterPolicies:

```yaml theme={null}
spec:
  validationFailureActionOverrides:   # <-- deprecated at top level
    namespaces:
      - production
    action: Enforce
  rules:
    ...
```

> **warning** The top-level `validationFailureActionOverrides` is deprecated. Prefer placing `failureActionOverrides` inside each rule for finer-grained control and clearer intent.

Best practices

* Prefer rule-scoped `failureActionOverrides` for precise, readable policies.
* Use `Audit` as the default for safer rollouts, and enable `Enforce` only where needed (e.g., `production`).
* Keep override lists minimal and documented so reviewers can quickly understand exceptions.

References

* Kyverno policies and validation: [https://kyverno.io/docs/writing-policies/validate/](https://kyverno.io/docs/writing-policies/validate/)
* Kubernetes admission control concepts: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

That's it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/8be9924f-5d88-4597-a2f0-51138214d91d)
