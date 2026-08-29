# Strategic Merge Patch

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Mutate-Rules/Strategic-Merge-Patch/page

Explains Kyverno's patchStrategicMerge mutation method, its declarative overlays, autogen for pod controllers, and when to use it versus JSON Patch.

We just saw how powerful JSON patches are for making precise changes. But their major limitation is the lack of auto-generation rules for Pod controllers, which often forces you to write many repetitive mutate policies for Deployments, CronJobs, ReplicaSets, and other controllers.

In this lesson we’ll cover Kyverno’s other primary mutation method that solves that exact problem: the strategic merge patch.

Let's check back in with Alex. His goal is to automatically add a security sidecar container to every pod. He used JSON Patch to add this container to Pod resources,

<Frame>
  <img alt="The image shows an illustration of Alex's experience with JSONPatch, mentioning the use of patches.Json6902 to add a container to a list, alongside four pod icons." />
</Frame>

and this worked — but to ensure the mutation applied everywhere he had to manually write separate rules for Pods, Deployments, CronJobs, and so on. He found himself managing multiple nearly identical rules — a maintenance headache.

<Frame>
  <img alt="The image features a user's experience with JSONPatch, focusing on challenges with writing rules for Pods, Deployments, and CronJobs, and expressing a desire for a better solution. It includes a quote by &#x22;Alex&#x22; and a simple avatar illustration." />
</Frame>

Isn't there an easier way to apply a mutation to all pod controllers, similar to how validate rules can target multiple controllers? Yes — the answer is `patchStrategicMerge`.

Instead of providing a list of operations like JSON Patch, `patchStrategicMerge` uses an overlay: a snippet of Kubernetes YAML that represents the desired partial state. Kyverno merges this overlay into the resource being created.

<Frame>
  <img alt="The image explains the &#x22;patchStrategicMerge&#x22; method in Kyverno, describing it as an &#x22;overlay&#x22; where a partial resource definition is merged onto the original resource." />
</Frame>

This approach is declarative — you describe what you want to add or change, not the step-by-step operations to get there. If you’ve used `kubectl patch`, this will feel familiar: Kyverno applies the overlay and creates missing fields as needed.

Example: set a default seccomp profile for all Pods
Alex wants to improve cluster security by ensuring every Pod uses the `RuntimeDefault` seccomp profile. A Kubernetes-style strategic merge patch in a Kyverno mutate rule looks like this:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-pod-default-seccomp-profile
spec:
  rules:
    - name: add-pod-default-seccomp-profile
      match:
        any:
          resources:
            kinds:
              - Pod
      mutate:
        patchStrategicMerge:
          spec:
            securityContext:
              seccompProfile:
                type: RuntimeDefault
```

When a Pod is created, Kyverno will merge this block into the Pod spec. If `securityContext` or `seccompProfile` do not exist, Kyverno will create them. The patch is concise and easy to read.

The key advantage — and the reason to prefer `patchStrategicMerge` in many cases — is autogen. Because overlays do not rely on fixed JSON paths like `/spec/containers/0`, Kyverno can auto-generate equivalent mutate rules for higher-level controllers. A single Pod-matching patch can be applied to Deployments, ReplicaSets, StatefulSets, CronJobs, and more, with Kyverno placing the overlay correctly inside their pod templates.

<Frame>
  <img alt="The image explains that autogen is back, highlighting a feature that allows mutating rules for Pods, which solves a problem by automatically generating rules for various Kubernetes resources." />
</Frame>

When to use which mutation method

* Use `patchStrategicMerge` for most common tasks: adding labels, setting defaults, or applying securityContext fields. It is declarative, readable, and works well with Kyverno autogen for pod controllers.
* Use `patchesJson6902` (JSON Patch) when you need very precise edits that overlays cannot express — for example, removing a specific field, operating on a particular list index, or performing fine-grained operations like replace/remove at an exact path.

Comparison at a glance:

| Feature                     |                                        patchStrategicMerge | patchesJson6902 (JSON Patch)                         |
| --------------------------- | ---------------------------------------------------------: | ---------------------------------------------------- |
| Style                       |                                   Declarative YAML overlay | Operation-based JSON Patch                           |
| Readability                 |                      High — looks like Kubernetes manifest | Lower — list of operations                           |
| Autogen for Pod controllers |                                                        Yes | No (requires separate rules)                         |
| Best for                    |            Defaults, labels, securityContext, adding items | Precise path edits, indexed list ops, removals       |
| Example                     | `spec.securityContext.seccompProfile.type: RuntimeDefault` | `[{ "op": "remove", "path": "/spec/containers/1" }]` |

A note about conditional logic
`patchStrategicMerge` supports conditional anchors and expressions directly within the patch. That allows patterns like “add this label only if it doesn't already exist.” JSON Patch does not support that style of inline conditional logic. We’ll cover conditional anchors and expressions in the next lesson.

Summary

* Prefer `patchStrategicMerge` as the default for most mutate rules because it’s declarative, autogen-friendly, and easier to maintain.
* Reserve `patchesJson6902` for targeted, path-based edits when overlays can’t express the required change.

<Frame>
  <img alt="The image is a summary guide for choosing a mutation method, comparing &#x22;patchStrategicMerge&#x22; for adding or overlaying data and setting defaults, and &#x22;patchesJson6902 (JSONPatch)&#x22; for precise operations and removing data." />
</Frame>

One additional important difference sets up our next lesson: conditional logic. `patchStrategicMerge` supports conditional anchors and expressions directly within the patch, letting you say things like “add this label only if it doesn't already exist.” JSON Patch does not support this style of conditional logic. Conditional anchors will be covered later.

Finally, strategic merge patches are generally simpler and easier to read, which makes them a great default choice for many mutation scenarios.

<Callout icon="lightbulb">
  Choose `patchStrategicMerge` for declarative overlays and autogen-friendly mutations. Reserve JSON Patch for targeted, path-based edits that overlays can't express.
</Callout>

<Frame>
  <img alt="The image is a slide about enforcing a default seccomp profile. It states Alex's goal to automatically apply the RuntimeDefault seccomp profile to all Pods for improved security." />
</Frame>

That's it for this lesson.

Links and references

* [Kyverno Documentation](https://kyverno.io/docs/)
* [kubectl patch reference](https://kubernetes.io/[AWS_SECRET_ACCESS_KEY]-commands#patch)
* Kyverno autogen and mutate rule behavior — see the Kyverno docs for details on how autogen maps Pod-level patches to controllers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/f82da39a-44ea-41a4-85d2-89ced827f6f0" />
</CardGroup>
