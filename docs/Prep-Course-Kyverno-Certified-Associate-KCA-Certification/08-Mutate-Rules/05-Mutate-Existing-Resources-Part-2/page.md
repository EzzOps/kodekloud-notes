# Mutate Existing Resources Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Mutate-Rules/Mutate-Existing-Resources-Part-2/page

Explains advanced Kyverno mutate-existing policies including immediate application, label selectors, per-target variables, and preconditions for precise resource mutations

Previously we introduced the concept of mutating existing resources: how it differs from admission-time mutation and how to configure the required permissions.

In this article we build on that foundation and explore advanced techniques to make these policies more powerful and precise. We'll cover:

* How to trigger mutate-existing rules immediately on policy creation.
* How to select targets more dynamically with label selectors.
* How to reference data from each target resource in the mutation.
* How to further narrow the set of targets using preconditions.

Let's get started.

## Controlling when a mutate-existing rule runs

By default, a mutate-existing policy runs when the trigger resource specified in the `match` block is created or updated. If you want the policy to apply mutations to all matching existing targets immediately when the policy is created (instead of waiting for a trigger event), set `mutateExistingOnPolicyUpdate: true` inside the `mutate` block.

Example:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: mutate-secret-on-configmap-event
spec:
  rules:
    - name: mutate-secret-on-configmap-event
      match:
        any:
          - resources:
              kinds:
                - ConfigMap
              names:
                - dictionary-1
      mutate:
        mutateExistingOnPolicyUpdate: true
        targets:
          # target definitions go here
```

<Callout icon="lightbulb">
  Setting `mutateExistingOnPolicyUpdate: true` forces the background controller to immediately list and mutate matching targets when the policy is created or updated. This is useful when you need policy changes to take effect across existing resources right away.
</Callout>

Kyverno also runs a default background reconciliation loop (once per hour) that scans resources and reapplies mutate-existing rules to repair missed or reverted changes over time. You can customize that interval by changing the background scan interval environment variable on the background controller deployment — see the Kyverno documentation for details and recommended settings: [https://kyverno.io/](https://kyverno.io/).

## Targeting multiple resources with selectors

Targeting a resource by name is useful for single resources, but in most real-world scenarios you want to mutate a set of related resources. Use a `selector` inside a `targets` entry to find resources by labels.

Example: this policy is triggered by any `Secret` change and mutates all `ConfigMap`s that have the label `should-match: "yes"`.

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: mutate-configmap-on-secret-event
spec:
  rules:
    - name: mutate-configmap-on-secret-event
      match:
        any:
          - resources:
              kinds:
                - Secret
      mutate:
        targets:
          - apiVersion: v1
            kind: ConfigMap
            selector:
              matchLabels:
                should-match: "yes"
            patchStrategicMerge:
              metadata:
                labels:
                  foo: bar
```

## Using data from each target: the `target` variable

Kyverno exposes a special variable named `target` that represents the resource currently being mutated by the background controller. This enables patches that incorporate data read from the target itself, so each target can be mutated using its own values.

Consider a trigger on a ConfigMap named `cmone`. Kyverno targets `cmtwo` and `cmthree`. Each target is mutated using a JSON6902 patch that takes a value from the target's own `data.key` and stores it in the `env` label:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: copy-key-to-label
spec:
  rules:
    - name: copy-configmap-key-to-label
      match:
        any:
          - resources:
              kinds:
                - ConfigMap
              names:
                - cmone
      mutate:
        targets:
          - apiVersion: v1
            kind: ConfigMap
            name: cmtwo
          - apiVersion: v1
            kind: ConfigMap
            name: cmthree
        patchesJson6902: |-
          - op: add
            path: "/metadata/labels/env"
            value: "{{ target.data.key }}"
```

Notes on how this behaves:

* When Kyverno processes `cmtwo`, `{{ target.data.key }}` is evaluated against `cmtwo` and the value from `cmtwo.data["key"]` is used to set `/metadata/labels/env`.
* Kyverno then processes `cmthree` separately; `{{ target.data.key }}` is evaluated against `cmthree` and its value is used for that mutation.
* When referring to template expressions in prose, keep them in inline code (for example, `{{ target.data.key }}`) so MDX treats them as code snippets.

## Two-stage filtering with preconditions

A selector can produce a broad set of potential targets. If you want to mutate only a subset of those (for example, Deployments whose names match a specific pattern), add a `preconditions` block inside the `targets` definition. Think of `preconditions` as a second-stage filter: Kyverno first finds resources by `kind`, `namespace`, and `selector`, then evaluates `preconditions` to narrow the list further.

<Frame>
  <img alt="The image presents a comparison between a problem and solution, explaining that if a selector finds too many potential targets, preconditions can be used as a solution." />
</Frame>

The `preconditions` block supports logical operators such as `all` and `any`, and comparison operators such as `Equals`, `NotEquals`, `Matches`, etc. Use `Matches` with a regular expression when you need pattern matching. In the example below the `targets` entry initially finds all `Deployment`s in the namespace from the admission request (`request.namespace`), and the precondition keeps only deployments whose name starts with `testing-`:

<Frame>
  <img alt="The image illustrates a two-stage filtering process for deployments, involving an initial broad identification followed by further filtering with preconditions." />
</Frame>

```yaml theme={null}
mutate:
  targets:
    - apiVersion: apps/v1
      kind: Deployment
      namespace: "{{request.namespace}}"
      preconditions:
        all:
          - key: "{{target.metadata.name}}"
            operator: Matches
            value: "^testing-.*"
      patchStrategicMerge:
        spec:
          template:
            # patch contents here
            metadata:
              labels:
                mutated-by: kyverno
```

Only the deployments that pass the `preconditions` check will proceed to the mutation step.

<Callout icon="warning">
  Be cautious when using broad selectors together with `mutateExistingOnPolicyUpdate: true`. A policy can affect many resources immediately—test in a safe environment before applying to production clusters.
</Callout>

## Quick reference table

|               Feature | Purpose                                                        | Example / Notes                                   |
| --------------------: | -------------------------------------------------------------- | ------------------------------------------------- |
| Immediate application | Apply mutations to existing targets when the policy is created | `mutateExistingOnPolicyUpdate: true`              |
|     Dynamic targeting | Find targets by labels instead of hard-coded names             | Use `selector.matchLabels` inside `targets`       |
|       Per-target data | Use data from each target when computing a mutation            | Inline code: `{{ target.data.key }}`              |
|   Two-stage filtering | Narrow down selector results further                           | Use `preconditions` with operators like `Matches` |

## Recap

* Use `mutateExistingOnPolicyUpdate: true` to apply mutations immediately to existing targets when a policy is created or updated.
* Kyverno performs background reconciliation (default every hour); you can customize the scan interval in the background controller deployment.
* Use `selector` inside `targets` to dynamically locate resources by labels instead of hard-coding names.
* Use the `target` variable (for example `{{ target.data.key }}`) to read data from each target during mutation so each mutation can be context-aware.
* Use `preconditions` inside `targets` as a second-stage filter to ensure you mutate only the exact resources you intend.

<Frame>
  <img alt="The image is a summary slide listing four key points related to policy events, dynamic targeting, context-aware mutations, and advanced filtering, each with a brief description." />
</Frame>

## Further reading

* Kyverno documentation: [https://kyverno.io/](https://kyverno.io/)
* Guidance on writing safe mutate-existing policies and testing strategies: [https://kyverno.io/docs/writing-policies/](https://kyverno.io/docs/writing-policies/)

That's it for this article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/e8eb8eaa-5ede-4ede-8f58-e9a575b67b56" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/cfb70d7b-d3f0-4584-85c5-3db33cd63a12" />
</CardGroup>
