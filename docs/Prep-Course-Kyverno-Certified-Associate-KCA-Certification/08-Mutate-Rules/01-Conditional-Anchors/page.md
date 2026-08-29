# Conditional Anchors

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Mutate-Rules/Conditional-Anchors/page

Explains Kyverno patchStrategicMerge anchors for conditional and safe mutations of Kubernetes resources, including conditional, add-if-not-present, and global anchors with examples and processing order.

`patchStrategicMerge` is a powerful overlay mechanism in Kyverno that restores auto-generated fields while letting you mutate resources. However, simple unconditional patches will apply a change to every matched resource, potentially overwriting intentional settings.

Below we show how anchors add conditional logic to `patchStrategicMerge`, enabling safe, context-aware mutations — for example, setting secure defaults only when a field is absent.

Alex's example: enforce non-root Pods

Alex wants to enforce the security best practice of ensuring Pods don't run as root by setting `runAsNonRoot: true`.

<Frame>
  <img alt="The image presents &#x22;Alex's New Problem: The Overwrite Dilemma&#x22; with a goal to enforce a security best practice by ensuring all Pods run as non-root users (runAsNonRoot: true)." />
</Frame>

His first attempt is an unconditional patch like this:

```yaml theme={null}
mutate:
  patchStrategicMerge:
    spec:
      securityContext:
        runAsNonRoot: true
```

That will set `runAsNonRoot: true` on every Pod, overwriting any explicit `false` values and possibly breaking workloads. Alex needs a safer pattern: only add a default when the field is missing, and only modify when a clear condition is met.

What anchors do

Anchors are markers inside `patchStrategicMerge` that act like inline `if` statements. They let Kyverno decide when to apply a mutation. Anchors only work with `patchStrategicMerge`. There are three anchor patterns:

<Frame>
  <img alt="The image is a table explaining &#x22;if&#x22; statements for patches, listing anchor types (Conditional, Add If Not Present, Global) along with their corresponding tags and behaviors." />
</Frame>

<Frame>
  <img alt="The image explains how anchors in &#x22;if&#x22; statements for patches support wildcards, specifically the asterisk symbol, which matches zero or more alphanumeric characters flexibly." />
</Frame>

Anchor summary (quick reference)

| Anchor type                       | Syntax example      | Behavior                                                                                                      |
| --------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------- |
| Conditional (strict "if")         | `(field): "value"`  | Applies the mutation only when the adjacent `field` exists and matches the value.                             |
| Add-if-not-present (safe default) | `+(field): value`   | Adds `field` only if it is missing; never overwrites an existing value.                                       |
| Global                            | `<(field): "cond">` | Scans the resource/list for the condition anywhere and — if found — applies mutation at a different location. |

Anchors support wildcards: use `*` to match zero or more characters and `?` to match exactly one character. This is useful for matching names or images that follow patterns (e.g., `"secure*"` or `"corp.reg.com/*"`).

Basic conditional anchor

Use a conditional anchor when you want to change a sibling field only if a specific field exists and matches. Example: locate any port whose `name` begins with `secure` and set its `port` number to `6443`.

<Frame>
  <img alt="The image shows a directive about using a conditional anchor, aimed at altering port settings for endpoints by finding ports with names starting with &#x22;secure&#x22; and setting their port number to 6443." />
</Frame>

Policy example:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: policy-set-port
spec:
  rules:
    - name: set-port
      match:
        any:
          resources:
            kinds:
              - Endpoints
      mutate:
        patchStrategicMerge:
          subsets:
            ports:
              - (name): "secure*"
                port: 6443
```

Here `(name): "secure*"` acts like an `if`: Kyverno checks each port object for a `name` matching the pattern; only then it sets the sibling `port` field.

Add-if-not-present anchor (safe defaults)

The `+(...)` anchor provides a safe, non-destructive way to add defaults. It only adds the field when it does not already exist, preserving any intentional settings by developers.

Example: ensure a ConfigMap contains a specific label without overwriting an existing value:

```yaml theme={null}
spec:
  rules:
    - name: lfx-mentorship
      match:
        any:
          resources:
            kinds:
              - ConfigMap
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              +(lfx-mentorship): kyverno
```

Kyverno adds `lfx-mentorship: kyverno` only if that label key is absent.

Use add-if-not-present anchors across multiple sibling fields to establish defaults for a resource. For Pod-level defaults (note the distinction between pod-level and container-level securityContext below):

```yaml theme={null}
spec:
  rules:
    - name: add-default-securitycontext
      match:
        any:
          resources:
            kinds:
              - Pod
      mutate:
        patchStrategicMerge:
          spec:
            securityContext:
              +(runAsNonRoot): true
              +(runAsUser): 1000
              +(runAsGroup): 3000
              +(fsGroup): 2000
```

Kyverno evaluates each `+(...)` independently: if `runAsUser` exists but `runAsGroup` does not, only `runAsGroup` is added. This preserves explicit developer settings while filling in missing safe defaults.

> **lightbulb** Note: `runAsNonRoot` is commonly set at the container level (`container.securityContext`). Pod-level `securityContext` typically includes `runAsUser`, `runAsGroup`, and `fsGroup`. Adapt the example to container-level `securityContext` if you need `runAsNonRoot` enforced per container.

Global anchor

Use the global anchor when the matching condition lives in one part of the resource but the mutation should be applied elsewhere. The global anchor `<(...)>` searches across lists/fields and, if any match is found, enables the mutation in a different location.

<Frame>
  <img alt="The image contains a title &#x22;The Global Anchor <()>&#x22; with a use case description: &#x22;When the condition is in a different part of the resource from the mutation.&#x22;" />
</Frame>

Example: add an `imagePullSecrets` entry when any container uses an image from `corp.reg.com/*`:

```yaml theme={null}
spec:
  rules:
  - name: add-imagepullsecret
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - <(image): "corp.reg.com/*"
          imagePullSecrets:
          - name: my-secret
```

Here `<(image): "corp.reg.com/*">` is evaluated across all `containers`. If any container image matches, Kyverno adds `imagePullSecrets` at the Pod spec level. Think of the global anchor as: “if this condition exists anywhere in this list, then apply this patch somewhere else.”

Combining anchors for multi-stage logic

You can combine global and add-if-not-present anchors for staged logic: first gate the mutation with a conditional/global check, then add defaults only when missing.

Example: add an annotation if the Pod uses an `emptyDir` volume and the annotation does not already exist:

```yaml theme={null}
spec:
  rules:
  - name: annotate-empty-dir
    match:
      any:
        resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        metadata:
          annotations:
            +(cluster-autoscaler.kubernetes.io/safe-to-evict): 'true'
        spec:
          volumes:
          - <(emptyDir): {}
```

Processing order Kyverno follows

1. Kyverno evaluates strict conditional anchors first: the conditional anchor `(…)` and the global anchor `<(…)>`. Treat these as gatekeepers — if any of these checks fail, the mutation does not run.
2. If the resource passes those checks, Kyverno applies add-if-not-present anchors `+(...)` and overlays the patch values.

In the `annotate-empty-dir` example:

* Kyverno scans `spec.volumes` for an `emptyDir` via `<(emptyDir): {}>`. If none exists, the whole mutation is skipped.
* If an `emptyDir` exists, Kyverno then applies the `+(...)` annotation only if that annotation key is missing.

<Frame>
  <img alt="The image explains how Kyverno processes anchors, detailing steps for checking conditional anchors and applying additions. It also includes a tip on enabling API warnings for mutations." />
</Frame>

You can set `spec.emitWarnings: true` in a policy to have Kyverno emit a warning to the user when it mutates a resource — a helpful visibility feature during `kubectl apply`.

> **lightbulb** Set `spec.emitWarnings: true` in your policy to notify users when a mutation occurred — a helpful way to preserve developer awareness.

Summary

* `(field)`: conditional anchor — apply the mutation only if the adjacent field exists and matches the value.
* `+(field)`: add-if-not-present anchor — add a default only when the field is missing; never overwrite.
* `<(field)>`: global anchor — evaluate the condition anywhere in a list/resource and apply a mutation in a different location.

Mastering anchors helps you write Kyverno mutate policies that are powerful, predictable, and respectful of existing developer intent.

This is it for this lesson.

Links and references

* Kyverno mutate policies: [https://kyverno.io/docs/writing-policies/mutate/](https://kyverno.io/docs/writing-policies/mutate/)
* Kyverno anchors and `patchStrategicMerge`: [https://kyverno.io/docs/writing-policies/mutate/#patchstrategicmerge](https://kyverno.io/docs/writing-policies/mutate/#patchstrategicmerge)
* Kubernetes securityContext reference: [https://kubernetes.io/docs/tasks/configure-pod-container/security-context/](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/7e4a391e-a0ac-4dba-bede-0cfc6e41cefc)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/a560c6f5-7b1e-4656-9666-2dd8f21c6336)
