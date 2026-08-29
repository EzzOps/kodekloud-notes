# Patterns Anchors Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Patterns-Anchors-Part-1/page

Explains Kyverno anchors, demonstrating conditional and equality anchors to express if-then validation logic across sibling fields or child fields with examples and tips

In this lesson we cover one of Kyverno’s most powerful features: anchors. Anchors let you express "if-then" logic inside Kyverno validate rules, so you can write policies like:

```text theme={null}
IF image tag == "::latest"
THEN imagePullPolicy = "Always"
```

or

```text theme={null}
IF pod.spec.volumes.type == "hostPath"
THEN metadata.labels.security == "xyz"
```

This is Part 1 of a two-part deep dive. Here we focus on the two anchors most useful for building conditional logic: the Conditional Anchor and the Equality Anchor. Part 2 will cover Existence, Negation, and Global anchors.

Let’s meet our platform engineer Alex: basic block/allow policies aren’t enough for real-world requirements. Anchors let you enforce conditional rules such as “if a container uses the latest image tag, ensure imagePullPolicy is Always” or “if a Pod uses a hostPath volume, ensure a specific security label exists.”

<Frame>
  <img alt="" />
</Frame>

## Anchor fundamentals: decision points in a rule

Think of anchors as decision points — forks in the policy processing flow. When an anchor matches, Kyverno either evaluates sibling fields (sideways) or children fields (downwards), depending on the anchor type. Choosing the wrong anchor changes the direction of the logic and can break your intent.

Two anchors covered here:

* Conditional Anchor — looks sideways to peer/sibling elements (if X, then check peer Y).
* Equality Anchor — looks downwards to children (if parent exists, evaluate its children).

We’ll explore both with real examples and step-by-step processing.

***

## Conditional Anchor — parentheses `( )`

The Conditional Anchor is the classic if-then pattern. Marked with parentheses, it defines an "if" condition inside the YAML tree and makes the rule evaluate peer elements as the "then" clause.

Use case: If an image uses the `latest` tag, then the `imagePullPolicy` must not be `IfNotPresent`.

Example pattern (conditional anchor on `image`):

```yaml theme={null}
spec:
  containers:
    - (image): "*:latest"
      imagePullPolicy: "!IfNotPresent"
```

Explanation and processing flow:

1. The anchor `(image)` marks the image field as the if-clause.
2. If the container image matches `*:latest`, Kyverno proceeds to evaluate peer elements of the anchored element — in this case the `imagePullPolicy` sibling.
3. The rule enforces that `imagePullPolicy` is not `IfNotPresent` (so `Always` is typically expected).

When the anchor appears higher in the structure, the peer resolution still applies. For example, use a conditional anchor on `spec` to connect checks deep in `spec` to a sibling `metadata`:

```yaml theme={null}
validate:
  failureAction: Enforce
  message: "If a hostPath volume exists and is set to `/var/run/docker.sock`, the label `allow-docker` must equal `true`."
  pattern:
    metadata:
      labels:
        allow-docker: "true"
    (spec):
      (volumes):
        - (hostPath):
            path: "/var/run/docker.sock"
```

Processing steps:

* Kyverno sees `(spec)`: this starts the if-clause.
* It drills down to `(volumes)` and then `(hostPath)` looking for a hostPath with `path: "/var/run/docker.sock"`.
* If that entire nested if-condition is true, Kyverno looks at peers of the anchored top-level element `(spec)`.
* `metadata` is a sibling of `spec`, so Kyverno evaluates the `metadata.labels.allow-docker` requirement as the then-clause.

Read the rule as: If pod.spec contains a hostPath volume with `path: /var/run/docker.sock`, then the pod metadata must include `allow-docker: "true"`.

Key point: Conditional anchors connect elements sideways — they let a condition located deep in `spec` enforce a requirement on a sibling like `metadata`.

***

## Equality Anchor — `=( )`

The Equality Anchor is denoted by `=` followed by parentheses. Its logic is different: the if-clause is the existence of the field itself, and the then-clause applies to the children of that field (the check flows downwards).

Use case: If a `hostPath` volume is defined, ensure its `path` is not `/var/lib`.

Example pattern (equality anchor on `hostPath`):

```yaml theme={null}
spec:
  volumes:
    - =(hostPath):
        path: "!/var/lib"
```

Another full rule example:

```yaml theme={null}
validate:
  failureAction: Enforce
  message: "If a hostPath volume exists, it must not be set to `/var/run/docker.sock`."
  pattern:
    =(spec):
      =(volumes):
        - =(hostPath):
            path: "!/var/run/docker.sock"
```

Processing flow:

1. Equality anchors on `spec` and `volumes` tell Kyverno to continue only if those fields exist.
2. When Kyverno reaches `=(hostPath)`, the presence of the `hostPath` field is the if-clause.
3. With equality anchors, the then-clause is the children of the anchored element — so Kyverno evaluates `path` inside `hostPath`.
4. The rule enforces that `path` must not equal `/var/run/docker.sock`.

Key point: Equality anchors look downwards — a parent field’s presence triggers validation of its child fields, staying inside the same block rather than crossing to sibling fields.

<Frame>
  <img alt="" />
</Frame>

## Side-by-side summary

| Anchor Type        | Syntax     | Direction                 | If-clause                                        | Then-clause (what gets evaluated)             | Typical use                                                      |
| ------------------ | ---------- | ------------------------- | ------------------------------------------------ | --------------------------------------------- | ---------------------------------------------------------------- |
| Conditional Anchor | `(field)`  | Sideways (peers/siblings) | Value match at the anchored field or nested test | Sibling/peer elements of the anchored element | Cross-block rules (e.g., spec → metadata)                        |
| Equality Anchor    | `=(field)` | Downwards (children)      | Existence of the anchored field                  | Child fields inside the anchored element      | Enforce constraints inside the same object (e.g., hostPath.path) |

> **lightbulb** Choose your direction before writing a rule: conditional anchors validate sibling fields (sideways), while equality anchors validate children (downwards). Picking the wrong anchor changes the meaning of the rule.

## Practical tips and gotchas

* Conditional anchors connect a nested condition to requirements in sibling objects. Use them when you need cross-field/sibling enforcement (e.g., spec -> metadata).
* Equality anchors are for validating the children of a field when that field exists (e.g., hostPath -> path).
* Anchors can be combined and nested, but make sure to reason about directionality — anchors determine where Kyverno looks next.
* Test policies with representative manifests to confirm matching behavior (anchors that seem correct conceptually can still mismatch if the YAML hierarchy is different).

<Frame>
  <img alt="" />
</Frame>

> **warning** Using the wrong anchor breaks the intention of your rule. If your rule should enforce a sibling requirement but you used an equality anchor, the check will remain inside the same block and won’t validate the sibling field.

## Quick reference and links

* Kyverno anchors: conditional `( )` vs equality `=( )` — choose sideways vs downward validation.
* Example scenarios: ensure `imagePullPolicy` when `image` tag is latest; enforce labels when a hostPath volume is present.

Further reading:

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes volumes (hostPath): [https://kubernetes.io/docs/concepts/storage/volumes/#hostpath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath)

That concludes Part 1. In Part 2 we’ll cover Existence anchors, Negation anchors, and the Global anchor to complete the anchor toolkit.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/058330cd-c47c-4cb9-8001-f5555ce6fff9)
