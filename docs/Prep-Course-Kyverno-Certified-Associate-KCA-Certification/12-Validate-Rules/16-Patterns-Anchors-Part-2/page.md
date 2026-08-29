# Patterns Anchors Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Patterns-Anchors-Part-2/page

Explains Kyverno anchors for policy patterns, showing existence, negation, and global gates with examples to require nginx, forbid hostPath, and enforce registry secrets.

In the previous lesson we met Alex and introduced conditional and equality anchors to express if-then logic across peer and child elements. In this follow-up, Alex must solve three new, more nuanced problems. Each requires a different Kyverno anchor:

* Ensure every Pod includes at least one container using the `nginx` image (presence within a list).
* Forbid use of `hostPath` volumes entirely (absolute negation).
* Enforce that images pulled from the corporate registry require a specific `imagePullSecret`, but skip the rule for public images (rule-level gating).

This article explains the three anchors tailored for those needs, with practical examples and a comparison to common wildcard patterns.

> **lightbulb** This guide focuses on Kyverno anchors: existence (`^`), negation (`X`), and global (`<()`), showing how each solves a specific policy requirement. Use the examples as starting points and adapt patterns to your organization’s naming and image conventions.

## Quick anchor summary

| Anchor                   | Purpose                                                                            | Typical use case                                                           |
| ------------------------ | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `^` (existence anchor)   | Check that at least one element in an array matches the following pattern          | Ensure a Pod contains at least one container using `nginx`                 |
| `X` (negation anchor)    | Fail if the named key exists                                                       | Forbid `hostPath` volumes                                                  |
| `<(...)` (global anchor) | Gate the remainder of the pattern: only evaluate the rule if the condition matches | If an image matches `corp.reg.com/*`, require a specific `imagePullSecret` |

For full reference, see the Kyverno docs: [Kyverno Policy Patterns](https://kyverno.io/docs/writing-policies/).

***

## 1) Existence anchor: ensure at least one container uses nginx

Alex wants to guarantee that each Pod contains at least one container using the `nginx` image, but he does not want to force all containers to use it.

Use the existence anchor (`^`) to treat the `containers` list as a set and require at least one element to match the following pattern.

Example pattern (snippet used inside a `validate` rule's `pattern`):

```yaml theme={null}
spec:
  # Check AT LEAST ONE container
  ^(containers):
    - image: nginx:latest
```

Behavior:

* Kyverno iterates the `containers` array and passes validation as soon as it finds one container whose `image` equals `nginx:latest`.
* Other containers may use any image; they are not required to match.

Contrast with a wildcard-based pattern that inadvertently requires every container to match:

```yaml theme={null}
pattern:
  spec:
    containers:
      - name: "*"
        image: nginx:latest
```

Behavior:

* This pattern uses a wildcard for `name`, but it still enforces that each array item (every container) must match `image: nginx:latest`.
* If any container uses a different image (e.g., a Python app), the Pod will fail validation.

Use the existence anchor when you want a flexible presence check; use the wildcard pattern only when you want every element to conform.

***

## 2) Negation anchor: forbid hostPath volumes

To outright ban `hostPath` volumes (a critical security rule), use the negation anchor `X`. This anchor fails the validation when the named key exists in the object being checked.

Example pattern that iterates all volumes and forbids `hostPath`:

```yaml theme={null}
spec:
  volumes:
    - name: "*"
      # Forbid hostPath from being defined (value is a YAML placeholder)
      X(hostPath): "null"
```

Notes:

* The `X(hostPath): "null"` line means: if the `hostPath` key exists on any volume, fail.
* The anchor does not evaluate the value of `hostPath` (e.g., `/data`); it only checks the presence of the key.
* This produces a deterministic deny: `hostPath` cannot be used at all.

> **warning** Forbidding `hostPath` is a common hardening practice. Make sure you coordinate with app owners because legitimate workloads that require node-local access might need alternate approaches (e.g., CSI drivers).

***

## 3) Global anchor: gate the rule itself for corporate registry images

Alex wants a rule that applies only when a Pod pulls images from the corporate registry (`corp.reg.com`). If the Pod uses public images (Docker Hub, etc.), the rule should be skipped.

Use the global anchor `<(...)` to create a gate — evaluate the rest of the pattern only when the condition is true.

Pattern example:

```yaml theme={null}
validate:
  failureAction: Enforce
  message: Images coming from corp.reg.com must use the correct imagePullSecret.
  pattern:
    spec:
      containers:
        - name: "*"
          # IF this condition is true...
          <(image): "corp.reg.com/*"
      imagePullSecrets:
        - name: my-registry-secret
```

How it works:

1. Kyverno first evaluates the condition in the global anchor: does the container `image` match `corp.reg.com/*`?
2. If the condition is false (e.g., `redis:latest` from Docker Hub), Kyverno skips this pattern for that container — no failure.
3. If the condition is true, Kyverno enforces the rest of the pattern — in this case, the Pod must include `imagePullSecrets` with `name: my-registry-secret`.

This creates an explicit “if and only if” rule: only images from the corporate registry trigger the secret requirement.

***

## Example: a Pod that will be rejected

Trace a failing request to see the global anchor in action:

Example Pod that will be blocked:

```yaml theme={null}
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: web
      image: corp.reg.com/nginx   # condition is TRUE
  imagePullSecrets:
    - name: other-secret        # required secret is missing / wrong
```

Evaluation:

* Step 1: The global anchor matches because the container image is from `corp.reg.com`.
* Step 2: The gate opens and Kyverno checks for `imagePullSecrets` with `name: my-registry-secret`.
* The Pod only has `other-secret`, so the pattern fails and Kyverno rejects the Pod with the configured message.

***

## Putting it all together

Use the right anchor for each scenario:

* Existence anchor (`^`) — presence in arrays without overconstraining: ensure at least one `nginx` container.
* Negation anchor (`X`) — absolute denial for sensitive keys: forbid `hostPath`.
* Global anchor (`<()` ) — gate the rule so it only applies when a condition is met: require an `imagePullSecret` for corporate-registry images.

Example policy skeletons and the pattern snippets above are designed to be embedded inside a full Kyverno `ClusterPolicy` or `Policy` `validate` rule. Test policies in a staging cluster and iterate with clear `message` fields so developers get actionable feedback.

***

## Links and references

* Kyverno documentation — policies and patterns: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes Pod spec: [https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/4d9072ac-f12b-4914-954b-16af513c3026)
