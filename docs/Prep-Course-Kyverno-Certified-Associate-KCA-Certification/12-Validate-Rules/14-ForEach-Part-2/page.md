# ForEach Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/ForEach-Part-2/page

Advanced Kyverno foreach techniques for validating Kubernetes resources using element, list, deny, preconditions, and JMESPath to enforce policies like blocking wildcard Ingress hosts and emptyDir storage requirements

This lesson builds on the core building blocks of the `foreach` loop and puts that knowledge into practice with real-world Kyverno validation scenarios.

Quick refresher: core `foreach` components

* `list` — the array (or JMESPath expression that produces an array) Kyverno iterates over.
* `element` — the current item inside the loop.
* Validation logic (`pattern`, `anyPattern`, or `deny`) — applied to each `element`.

| Component          | Purpose                        | Example                     |
| ------------------ | ------------------------------ | --------------------------- |
| `list`             | Specifies what to iterate      | `request.object.spec.rules` |
| `element`          | Current item in the loop       | `element.host`              |
| `deny` / `pattern` | Validation applied per element | `deny` with `conditions`    |

> **lightbulb** Use `element` to reference fields on the current item (for example, `element.host` or `element.volumeMounts[]`). Combined with JMESPath expressions, `list` can merge arrays such as `initContainers` and `containers`.

## Ingress: block wildcard hosts

Requirement: the security team wants to forbid wildcard hosts (those containing `*`) in Ingress resources. This is a good example of using `deny` inside a `foreach` to reject specific elements.

How it works:

* `list` points to `request.object.spec.rules`, so Kyverno iterates every rule in the Ingress `spec.rules` array.
* On each iteration `element` is one rule object (for example, a dictionary containing `host` and `http`).
* The `deny` condition tests `element.host` with the `contains` function and rejects the request when `*` is present.

Example policy snippet:

```yaml theme={null}
rules:
  - name: block-ingress-wildcard
    match:
      any:
        - resources:
            kinds:
              - Ingress
    validate:
      message: "Wildcards are not permitted as hosts."
      foreach:
        - list: "request.object.spec.rules"
          deny:
            conditions:
              any:
                - key: "{{ contains(element.host, '*') }}"
                  operator: Equals
                  value: true
```

Notes on the deny condition:

* The `key` is an expression in `{{ }}` and references `element.host`.
* `contains(element.host, '*')` returns `true` when `*` exists in the hostname.
* If any `element` satisfies the condition, Kyverno denies the entire request.

> **warning** Deny rules inside `foreach` will reject the whole resource if any element matches. Use them only when you intend to block the entire request for a single failing item.

## Using preconditions to filter loop items (emptyDir example)

Scenario: require containers that mount an `emptyDir` volume to declare ephemeral storage `requests` and `limits`. Pods that do not mount an `emptyDir` should not fail.

Key concepts:

* The `list` can be a JMESPath expression that merges `initContainers` and `containers` into a single list so you iterate all container objects.
* `preconditions` act as a per-element filter: Kyverno evaluates them for each `element`. If a precondition fails, that element is skipped.
* Only elements that pass preconditions are validated against the `pattern`.

Example policy snippet:

```yaml theme={null}
validate:
  message: Containers mounting emptyDir volumes must specify requests and limits for ephemeral-storage.
  foreach:
    - list: "request.object.spec.[initContainers, containers][]"
      preconditions:
        any:
          - key: "{{ element.volumeMounts[].name }}"
            operator: AnyIn
            value: "{{ emptydirnames }}"
      pattern:
        resources:
          requests:
            ephemeral-storage: "?*"
          limits:
            ephemeral-storage: "?*"
```

Explanation:

* `list: "request.object.spec.[initContainers, containers][]"` merges `initContainers` and `containers` producing a single array of container objects to iterate.
* `preconditions` checks whether any `volumeMount` name on the current container (`element.volumeMounts[].name`) appears in the `emptydirnames` variable (the names of volumes that are `emptyDir`).
* If the precondition passes, `pattern` enforces presence of `resources.requests.ephemeral-storage` and `resources.limits.ephemeral-storage` using the `"?*"` wildcard to require a non-empty value.
* Containers that do not mount an `emptyDir` are skipped and will not be validated.

## Takeaways

* Use `deny` inside `foreach` to perform element-level conditional checks that can block a request when a single list item violates policy.
* Reference the current item with the `element` variable (for example, `element.host` or `element.volumeMounts[]`).
* Use `preconditions` to filter loop items and target only relevant elements — this prevents false failures and keeps policies efficient.
* JMESPath expressions let you merge and manipulate lists (for example, combining `initContainers` and `containers`) so `foreach` covers all relevant items.

Links and references

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* JMESPath: [https://jmespath.org/](https://jmespath.org/)
* Kubernetes `emptyDir` volume: [https://kubernetes.io/docs/concepts/storage/volumes/#emptydir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)

<Frame>
  <img alt="The image is a summary of advanced &#x22;forEach&#x22; techniques, highlighting the use of &#x22;deny&#x22; in loops for validation, applying preconditions for targeted policies, and writing advanced JMESPath to merge lists." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/34c3e7c5-f13c-4af5-93fc-0c4adc97e044)
