# The anyPattern OR Logic

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/The-anyPattern-OR-Logic/page

Explains using Kyverno anyPattern to accept either pod-level or per-container runAsNonRoot configurations and prevent unsafe overrides

Previously we gave Alice a set of anchors to express complex conditional logic in Kyverno. Now Alex faces a related but different problem: a resource can be correctly configured in two distinct ways. How can Kyverno accept either configuration without writing two separate rules?

This article explains how to use Kyverno's `anyPattern` to express a logical OR inside a single validation rule so the rule accepts a resource if it matches any one of the supplied patterns.

Scenario: enforce non-root containers

* Requirement: All containers must run as a non-root user.
* Two valid developer models:
  * Set `runAsNonRoot: true` at the Pod-level `securityContext` (pod default).
  * Or set `runAsNonRoot: true` on every container (container-level).

<Frame>
  <img alt="The image presents a challenge related to running containers as a non-root user, with two configuration options for developers: setting runAsNonRoot: true at the Pod level or individually for each container." />
</Frame>

Both approaches are valid, but a single Kyverno `pattern` typically describes one structural variant. Combining both structures into one `pattern` is either impossible or results in a very complex pattern. `anyPattern` solves this cleanly by providing multiple alternative patterns; Kyverno passes validation if any pattern matches.

Why this policy must handle two cases

* Problem 1 — override risk:

  * A Pod-level default (`spec.securityContext.runAsNonRoot: true`) can be overridden by a container setting `securityContext.runAsNonRoot: false`. The policy must prevent containers from disabling a safe pod default.

  Example container override:

  ```yaml theme={null}
  spec:
    securityContext:
      runAsNonRoot: true
    containers:
    - name: bad-container
      securityContext:
        runAsNonRoot: false
  ```

* Problem 2 — missing default:

  * If there is no pod-level `runAsNonRoot` default, every container (and initContainer) must explicitly set `runAsNonRoot: true`. The policy must validate per-container declarations.

  Example without pod default:

  ```yaml theme={null}
  spec:
    containers:
    - name: good-container
      securityContext:
        runAsNonRoot: true
    - name: bad-container
      securityContext:
        runAsNonRoot: false
  ```

Policy intent

* Accept the Pod if either:
  1. The Pod has `spec.securityContext.runAsNonRoot: true` and no container (or initContainer) sets `runAsNonRoot: false`, or
  2. Every container and initContainer explicitly sets `securityContext.runAsNonRoot: true`.

This either-or logic is exactly why `anyPattern` exists.

How `anyPattern` works

* Place `anyPattern` inside a rule's `validate` block.
* `anyPattern` accepts a YAML list of alternative patterns.
* Kyverno evaluates patterns sequentially; validation succeeds on the first matching pattern. The resource is rejected only if it fails to match every pattern in the list.

<Frame>
  <img alt="The image introduces &#x22;anyPattern,&#x22; explaining its behavior as a logical OR across patterns and its use case for validating fields defined in multiple locations." />
</Frame>

> **warning** A Kyverno rule must use either a single `pattern` or `anyPattern`. Do not combine `pattern` and `anyPattern` in the same rule.

Policy fragment (solution)

* The example below shows two alternative patterns inside `anyPattern`:
  * Pattern A: Enforce a pod-level default and prevent container overrides.
  * Pattern B: Require per-container `runAsNonRoot: true` when no pod default exists.

```yaml theme={null}
validate:
  failureAction: Enforce
  message: "All containers and initContainers must run as non-root. Either set pod-level securityContext.runAsNonRoot: true (and do not override it in containers), or ensure every container/initContainer defines securityContext.runAsNonRoot: true."
  anyPattern:
    # Pattern A: Pod-level default must be set to runAsNonRoot: true,
    # and if a container defines a securityContext it must also set runAsNonRoot: true.
    - spec:
        securityContext:
          runAsNonRoot: true
        containers:
          - =(securityContext):
              =(runAsNonRoot): true
        =(initContainers):
          - =(securityContext):
              =(runAsNonRoot): true

    # Pattern B: No pod-level default; every container and initContainer
    # must define securityContext.runAsNonRoot: true.
    - spec:
        containers:
          - securityContext:
              runAsNonRoot: true
        =(initContainers):
          - securityContext:
              runAsNonRoot: true
```

Pattern breakdown

| Pattern                                  | When it applies                                        | What it enforces                                                                                                                                                                             |
| ---------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pattern A (pod-level default)            | When Pod has `spec.securityContext.runAsNonRoot: true` | Ensures pod-level default exists and any container `securityContext` (if present) also has `runAsNonRoot: true`, preventing container overrides. Applies the same check to `initContainers`. |
| Pattern B (container-level declarations) | When Pod lacks a pod-level default                     | Requires every `spec.containers` entry to include `securityContext.runAsNonRoot: true`. Applies the same check to `initContainers`.                                                          |

Notes and tips

* Use the optional presence marker (`=`) when you need to express conditional requirements for keys that may or may not exist (e.g., `=(initContainers)`).
* Keep `message` descriptive so users know how to fix failures (pod-level default vs. per-container settings).
* `anyPattern` is especially useful when the same valid configuration can be expressed in multiple Kubernetes locations (e.g., pod vs container).

References

* Kyverno docs: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes securityContext: [https://kubernetes.io/docs/tasks/configure-pod-container/security-context/](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

That's it—using `anyPattern` keeps your validation rules concise while allowing multiple valid configuration models for the same requirement.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/0e34623a-687f-4761-885c-9d663882cc65)
