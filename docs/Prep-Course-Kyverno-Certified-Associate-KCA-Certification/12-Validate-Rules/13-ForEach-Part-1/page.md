# ForEach Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/ForEach-Part-1/page

Explains Kyverno's forEach loop to validate each list item in Kubernetes resources, using JMESPath expressions to enforce container image policies like trusted-registry.io.

In this lesson we cover Kyverno's forEach loop—a concise, declarative way to validate every item in a list inside a Kubernetes resource (for example, `spec.containers` and `spec.initContainers` in a Pod).

Why use forEach?

* Kubernetes objects often include arrays (containers, initContainers, volumeMounts, etc.). Writing index-specific rules for each element is error-prone and unscalable.
* Kyverno’s `forEach` evaluates a JMESPath expression that selects a list from the admission request, then applies a validation clause to each element in that list.

Use case: Alex and the registry policy

* Alex, a platform engineer, must enforce a security requirement: every container image must come from the internal registry `trusted-registry.io`.
* A Pod can contain multiple `initContainers` and `containers`, both of which must be validated.

Example Pod to validate:

```yaml theme={null}
apiVersion: v1
kind: Pod
spec:
  initContainers:
    - name: init-myservice
      image: bad-registry.com/sidecar:1.0 # <--- INVALID
  containers:
    - name: myapp-container
      image: trusted-registry.io/myapp:2.5 # <--- VALID
    - name: another-container
      image: docker.io/nginx:latest # <--- INVALID
```

Without a loop you'd need separate rules for each index. forEach handles this cleanly in a single rule.

Example Kyverno validate rule using forEach

* The rule below checks both `initContainers` and `containers` by looping over each list and validating the `image` field:

```yaml theme={null}
spec:
  rules:
  - name: check-registry
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "All images must come from trusted-registry.io"
      foreach:
      - list: "request.object.spec.initContainers"
        pattern:
          image: "trusted-registry.io/*"
      - list: "request.object.spec.containers"
        pattern:
          image: "trusted-registry.io/*"
```

How forEach works

1. Kyverno evaluates the `list` JMESPath expression (a string) against the admission request (for example: `"request.object.spec.containers"`).
2. If the expression returns an empty array or is missing, that loop entry is skipped.
3. If items exist, Kyverno iterates them and exposes the current item as the implicit variable `element`.
4. The validation clause (`pattern`, `anyPattern`, or `deny`) is evaluated against that `element` object—so fields on the container (like `image`) are referenced directly.

Condensed forEach example (two loops: initContainers and containers):

```yaml theme={null}
foreach:
  # Loop 1: Checks all initContainers
  - list: "request.object.spec.initContainers"
    pattern:
      image: "trusted-registry.io/*"

  # Loop 2: Checks all containers
  - list: "request.object.spec.containers"
    pattern:
      image: "trusted-registry.io/*"
```

Important details and validation options

* The `list` value is a JMESPath expression written as a string. Do not wrap it in double curly braces.

> **lightbulb** Write [JMESPath](https://jmespath.org/) expressions directly as strings, for example: `"request.object.spec.containers"`. Do not use `{{ }}`.

* `element` is the implicit variable representing the current item in the iteration (e.g., a single container object).
* Validation clauses available inside a `forEach` entry:

| Clause       | When to use                                                                     | Example                                                                              |
| ------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `pattern`    | To assert the element matches a given structure or values                       | `pattern:\n  image: "trusted-registry.io/*"`                                         |
| `anyPattern` | When an element may match one of multiple allowable patterns                    | `anyPattern:\n  - image: "trusted-registry.io/*"\n  - image: "another-trusted.io/*"` |
| `deny`       | To explicitly block a request when a condition evaluates to true for an element | `deny:\n  conditions: ...`                                                           |

Skeleton showing the different styles:

```yaml theme={null}
foreach:
  - list: "request.object.spec.containers"
    pattern:
      image: "trusted-registry.io/*"

---

foreach:
  - list: "request.object.spec.containers"
    anyPattern:
      - image: "trusted-registry.io/*"
      - image: "another-trusted.io/*"

---

foreach:
  - list: "request.object.spec.containers"
    deny:
      # deny logic that evaluates the 'element' and blocks the request
      # (deny structure depends on the specific condition syntax you need)
```

Summary

* Use `forEach` to iterate lists inside Kubernetes resources (e.g., `spec.containers`, `spec.initContainers`) using JMESPath expressions.
* For each iteration Kyverno exposes the current item as `element`, and you validate that element using `pattern`, `anyPattern`, or `deny`.
* A single rule with `forEach` can validate every item in a list, keeping policies concise, maintainable, and scalable.

<Frame>
  <img alt="The image provides a summary of &#x22;forEach Fundamentals,&#x22; detailing the purpose, list, element, and logic related to validation logic application." />
</Frame>

Links and references

* Kyverno documentation: [https://kyverno.io/](https://kyverno.io/)
* JMESPath specification: [https://jmespath.org/](https://jmespath.org/)
* Kubernetes Pods: [https://kubernetes.io/docs/concepts/workloads/pods/containers/](https://kubernetes.io/docs/concepts/workloads/pods/containers/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/34ddbb12-7fd1-4012-be31-118bc0751688)
