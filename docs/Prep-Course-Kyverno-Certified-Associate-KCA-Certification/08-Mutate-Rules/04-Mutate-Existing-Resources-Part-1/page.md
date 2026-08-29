# Mutate Existing Resources Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Mutate-Rules/Mutate-Existing-Resources-Part-1/page

Explains Kyverno's mutate existing feature that uses admission created UpdateRequests and the background controller to asynchronously mutate existing resources and required RBAC setup.

So far, the Kyverno policies we've written act as gatekeepers during resource creation or update: they validate and mutate the resource that is being admitted. But what about resources already running in the cluster? How can an event on one resource cause a change to a different existing resource?

In this lesson we explore Kyverno's mutate-existing capability — a pattern that moves beyond the synchronous Admission Controller and uses the background controller to mutate already-deployed resources.

Problem statement: Alex's challenge

Alex needs a simple audit automation: whenever his application's main ConfigMap is updated, the Secret used by that same application should automatically receive a `config-version` label. A standard mutate rule cannot reach across resources because it only mutates the incoming resource in the admission request. That prevents him from updating the Secret directly during admission.

<Frame>
  <img alt="The image presents Alex's challenge, which involves automatically adding a config-version label to an app-secret when a ConfigMap is updated. It outlines problems, such as the inability of a standard mutate rule to modify different resources." />
</Frame>

The solution: mutate-existing policies

Mutate-existing policies run differently: the Admission Controller creates a small request object describing a desired change (an UpdateRequest), and the background controller performs the actual mutation on existing resources. This lets you trigger cross-resource automation (e.g., ConfigMap -> Secret) while keeping admission fast and synchronous.

Admission Controller vs Background Controller

Use this quick comparison to understand when each controller runs and what it can change.

| Controller            | When it runs                            | Primary role                                                | Mutates which resources                    |
| --------------------- | --------------------------------------- | ----------------------------------------------------------- | ------------------------------------------ |
| Admission Controller  | Synchronously at API server admission   | Validate/mutate the incoming request                        | Only the resource in the admission request |
| Background Controller | Asynchronously (watches trigger events) | Processes UpdateRequests and performs background automation | Any existing resources the policy targets  |

<Frame>
  <img alt="The image describes the functionality of the Background Controller in Kyverno, comparing it with the Admission Controller in terms of when they run and what they do." />
</Frame>

Key implications

* Asynchronous timing — mutations happen shortly after the trigger event; there may be a small, variable delay.
* Additional permissions — because the background controller modifies existing resources, it needs RBAC permissions to `get`, `update`, or otherwise operate on those resources.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;The Background Controller,&#x22; highlighting two key implications: &#x22;Asynchronous,&#x22; indicating a short delay between the trigger and the change, and &#x22;Requires Permissions.&#x22;" />
</Frame>

Granting background-controller permissions safely

Do not edit Kyverno's built-in ClusterRoles directly. Instead, create a dedicated ClusterRole that grants the minimal verbs needed (for example, `get` and `update` on Secrets), and label it with `rbac.kyverno.io/aggregate-to-background-controller: "true"`. Kyverno will aggregate this role into the background controller's effective permissions.

> **lightbulb** Create a ClusterRole with the precise permissions you need and add the aggregation label. Do not edit Kyverno's default ClusterRoles directly.

Example ClusterRole granting `get` and `update` on Secrets:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kyverno:mutate-secrets
  labels:
    rbac.kyverno.io/aggregate-to-background-controller: "true"
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "update"]
```

This is the recommended, least-privilege method to extend the background controller's abilities.

Policy structure for mutate-existing

A mutate-existing rule cleanly separates the trigger from the target:

* `match` (or `exclude`) defines the trigger — the admission events that cause an UpdateRequest to be created (e.g., updates to a specific ConfigMap).
* `mutate.targets` lists the existing resources to be modified (the background controller will process these).

Example: match a ConfigMap update and mutate an existing Secret by applying a strategic merge patch:

```yaml theme={null}
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
      targets:
        - apiVersion: v1
          kind: Secret
          name: secret-1
          patchStrategicMerge:
            metadata:
              labels:
                config-version: "v1"
```

Notes on the example

* `match` is the trigger: when an admission event matches this filter, Kyverno will create an UpdateRequest.
* `mutate.targets` is the set of existing resources to patch. You can use `patchStrategicMerge` to describe the mutation.
* For dynamic values, replace the static `"v1"` with templating or variables as required by your workflow.

How it works behind the scenes (workflow)

This capability uses a two-step handoff between Kyverno controllers:

1. Admission phase (fast)
   * The ConfigMap update triggers the policy in the Admission Controller.
   * Instead of mutating another resource immediately, Kyverno creates an UpdateRequest (UR) describing the intended mutation.
   * The admission request is allowed quickly so `kubectl apply` remains responsive.

2. Background mutation (asynchronous)
   * The background controller watches for UpdateRequest resources.
   * It reads the UR, locates the target resource(s) (for example, the Secret), and applies the mutation.
   * The mutation occurs asynchronously; expect a small delay.

<Frame>
  <img alt="The image illustrates the internal workflow of a process involving &#x22;Admission Request,&#x22; &#x22;The Handoff,&#x22; and &#x22;Background Mutation,&#x22; explaining how a ConfigMap update is handled by a system. It describes steps involving controllers and update requests to manage changes." />
</Frame>

This design keeps the API fast and lets Kyverno perform richer automations without blocking admission.

Recap

* Why: Standard mutate rules only affect the resource in the admission request. Mutate-existing policies let events on one resource trigger changes to other existing resources.
* Who does the work: The Admission Controller creates an UpdateRequest; the Background Controller executes the mutation asynchronously.
* Policy layout: Use a `match` block for the trigger and `mutate.targets` for the resources to patch.
* Mechanism: Admission -> UpdateRequest -> Background Controller processes UR -> Target resource updated.
* Prerequisite: Grant background-controller permissions via a ClusterRole labeled with `rbac.kyverno.io/aggregate-to-background-controller: "true"` so Kyverno can aggregate permissions safely.

<Frame>
  <img alt="The image presents a summary with highlights on a handoff mechanism involving an Admission Controller and Background Controller, and a prerequisite about RBAC permissions for the Background Controller." />
</Frame>

What's next

With these fundamentals in place, you can build more advanced mutate-existing policies:

* Use label or field selectors in `match` to scope triggers precisely.
* Target multiple resources in `mutate.targets`.
* Combine conditionals or JMESPath expressions (where supported) to compute dynamic patch content.
* Monitor UpdateRequests and Kyverno logs when debugging asynchronous mutations.

Links and references

* [Kyverno Mutate Existing Resources (docs)](https://kyverno.io/docs/writing-policies/mutate-existing-resources/)
* [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [Kyverno RBAC aggregation guide](https://kyverno.io/docs/installation/#rbac-aggregation)

With this understanding, you're ready to implement mutate-existing policies that automate cross-resource changes safely and reliably.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/c967815e-519d-419b-8413-d0acd9144b6a/lesson/d26e9974-2c98-4446-83b4-6ef56d7916ba)
