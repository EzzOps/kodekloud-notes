# Example events
- type: Normal
  reason: Created
  message: "Deployment web-app created"
- type: Normal
  reason: ScalingReplicaSet
  message: "Scaled replicas 1 → 3"
- type: Normal
  reason: Ready
  message: "All pods available"
```

Finalizers show how operators handle cleanup that Kubernetes cannot perform automatically. When deletion is requested, a finalizer pauses deletion until the controller can remove external state (DNS entries, cloud resources, or other dependencies). This lifecycle edge is common in production operators and one you have practiced.

<Callout icon="warning">
  Finalizers must be removed after cleanup completes. Leaving finalizers in place can permanently block resource deletion — ensure your controller handles cleanup and then removes the finalizer.
</Callout>

<Frame>
  <img alt="The image is a flowchart illustrating a &#x22;Finalizers – Clean Up Before Deletion&#x22; process with three stages: &#x22;Delete requested,&#x22; &#x22;Deletion paused,&#x22; and &#x22;Remove external state.&#x22;" />
</Frame>

Validation prevents invalid states from entering the cluster in the first place. Use CRD schema validation and admission controls to reject malformed requests early — it’s much easier to prevent bad input than to reconcile it later.

```yaml theme={null}
# Invalid request example
image: n@inx
replicas: -3
```

You also pushed the operator beyond local development: you packaged and deployed the manager, compared different toolchains, and explored real, production operators like cert-manager and the Prometheus Operator. Seeing how other operators are structured expands your mental model — the same operator pattern can appear in a custom controller, a Helm-based operator, or a mature upstream operator.

<Frame>
  <img alt="The image lists six components to consider when understanding the shape of an operator: a custom API, the reconcile loop, child resources, lifecycle edges, status signals, and the packaging path." />
</Frame>

Quick reference — core operator components and examples:

| Component        |                                     Purpose | Example / How it appears                |
| ---------------- | ------------------------------------------: | :-------------------------------------- |
| Custom API (CRD) |                       Express desired state | `spec.image`, `spec.replicas`           |
| Reconcile loop   |                       Enforce desired state | Controller `Reconcile` function         |
| Child resources  |                     Real cluster primitives | `Deployment`, `Service`, `ConfigMap`    |
| OwnerReferences  |              Ownership & garbage collection | `metadata.ownerReferences` on children  |
| Finalizers       | Clean up external resources before deletion | `metadata.finalizers`                   |
| Status & Events  |   Surface controller observations & signals | `status.conditions`, Event objects      |
| Packaging        |               Run the controller in-cluster | Deployment for the manager, Helm charts |

There is a professional layer beyond this lesson, but it should read like “next steps” — not a judgement. Teams harden operators by adding more tests, tightening RBAC and permissions, monitoring metrics and logs, planning upgrades, and authoring runbooks and support notes. These practices make an operator trustworthy in shared environments.

<Frame>
  <img alt="The image outlines a professional layer concept titled &#x22;Next, Not a Verdict,&#x22; featuring elements such as &#x22;More tests,&#x22; &#x22;Tighter permissions,&#x22; &#x22;Metrics and logs,&#x22; &#x22;Support notes,&#x22; and &#x22;Upgrade plans,&#x22; centered around a &#x22;Foundation&#x22; built on these aspects. It is copyrighted by KodeKloud." />
</Frame>

The best next steps are small and concrete. Pick one of these incremental improvements and ship it:

<Frame>
  <img alt="The image displays a sequence of four icons with labels: &#x22;New child resource,&#x22; &#x22;Status condition,&#x22; &#x22;End-to-end test,&#x22; and &#x22;An ingress, or better manifests,&#x22; with the caption &#x22;The Best Next Step Is Small.&#x22;" />
</Frame>

Suggested small improvements:

* Add a new child resource (e.g., a `HorizontalPodAutoscaler` or `Ingress`).
* Add a status condition to represent a useful operator state.
* Add one end-to-end test that verifies reconcile behavior.
* Improve example manifests so another person can try the operator quickly.

You can now explain the operator promise in plain terms: a user declares desired state in Kubernetes, and a controller keeps the real cluster aligned with that promise. You built that path with the WebApp operator — and that foundation will help you read, extend, and trust other operators in the future.

Links and references

* [CustomResourceDefinitions (CRDs)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [Owner References and Dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)
* [Events in Kubernetes](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#event-v1-core)
* [Finalizers in Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)
* [Ingress — Services and Networking](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* cert-manager: [https://cert-manager.io/](https://cert-manager.io/)
* Prometheus Operator: [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/708138ee-3fe0-42cd-b135-8e7df5f7ef59/lesson/2e3a333f-2a50-498a-b30b-1e5e35a299db" />
</CardGroup>


# Working Operator Versus Production Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Production-Readiness-Testing-Wrap-Up/Working-Operator-Versus-Production-Operator/page

Explains how to transform a working Kubernetes operator into a production-ready operator by adding testing, observability, RBAC, upgrade plans, clear status/events, and repeatable packaging for maintainability and trust

The key question at the end of an operator project is not just “does it run?” A working operator may reconcile a demo Custom Resource (CR) in a dev environment, but a production-minded operator is one that someone else can explain, observe, upgrade, and trust.

<Frame>
  <img alt="The image illustrates the transition from a &#x22;Working operator&#x22; that &#x22;reconciles a demo object&#x22; to a &#x22;Production-minded operator&#x22; that is explained, observed, upgraded, and trusted, ultimately gaining the trust of users." />
</Frame>

This distinction matters because operators usually become part of other teams’ platforms. A cluster may still accept the YAML, but if the operator is unclear, silent, or hard to recover, platform teams won’t know whether the system is healthy or how to respond.

<Frame>
  <img alt="The image shows a diagram with the title &#x22;Accepted Is Not the Same as Healthy,&#x22; illustrating a process involving &#x22;Your operator,&#x22; &#x22;Another team,&#x22; and an outcome labeled &#x22;Unclear.&#x22;" />
</Frame>

A compact web-app operator is a useful pattern to demonstrate the production shape of an operator without implying the sample project is a finished enterprise product. In this pattern:

* The Custom Resource (CR) is the contract describing user intent.
* The reconcile loop is the convergence and repair mechanism that turns intent into reality.
* Deployments, Services, ConfigMaps, and other Kubernetes resources are the managed “real-world” work.
* Status fields and Kubernetes Events are the signals that users and platform operators read to understand changes.

Production readiness wraps practical operational concerns around that core loop. The API should stay small and stable. The controller must keep making forward progress as cluster state changes. Deletion should be deliberate and recoverable. Status and events should tell a coherent story. Packaging and deployment must be repeatable so another engineer can run the operator without guessing.

<Frame>
  <img alt="The image is a diagram titled &#x22;Production Readiness Wraps the Loop,&#x22; showing a circular flow with elements indicating attributes like &#x22;API small and stable,&#x22; &#x22;Keeps making progress,&#x22; &#x22;Deletion deliberate,&#x22; and &#x22;Status tells a story.&#x22;" />
</Frame>

These production checks do not replace the code you wrote; they frame and harden it. Tests, permissions, metrics, upgrade plans, and documentation are not “extras” — they are essential practices that make the operator dependable in shared environments.

<Callout icon="lightbulb">
  Production-readiness checklist (practical items to include):

  * Unit and integration tests that validate the reconcile loop and failure cases.
  * Least-privilege RBAC and a clear, documented permissions model.
  * Metrics, liveness/readiness probes, and health endpoints for observability.
  * Upgrade and rollback strategies for both CR schemas and controller versions.
  * Intuitive status fields and user-facing Kubernetes Events that explain state changes.
</Callout>

Below is a compact reference to the operator’s core responsibilities and where to apply production practices.

| Component            |                  Role in the operator pattern | Example best practice                              |
| -------------------- | --------------------------------------------: | -------------------------------------------------- |
| Custom Resource (CR) |                      Contract for user intent | Keep schema minimal and versioned                  |
| Reconcile loop       |                  Convergence and repair logic | Test idempotency and error handling                |
| Managed resources    | Real Kubernetes objects the operator controls | Use declarative manifests and ownership            |
| Status & Events      |      Signals for users and platform operators | Populate status with actionable messages           |
| Packaging & Deploy   |      How operators are delivered and upgraded | Provide reproducible images and Helm/Trait bundles |

Helpful references:

* [Kubernetes API concepts](https://kubernetes.io/docs/concepts/overview/kubernetes-api/)
* [Operator pattern and best practices](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
* [Operators SDK](https://sdk.operatorframework.io/)

Carry forward two main ideas.

First, the web-app operator proves the core loop: desired state is expressed via a Custom Resource and the controller keeps real resources aligned with that request.

Second, production readiness is the discipline of making that loop understandable and trustworthy for the next person who will operate or inherit the system.

<Frame>
  <img alt="The image outlines two key ideas: &#x22;The core loop, proven,&#x22; which emphasizes desired to real processes kept in sync, and &#x22;Production readiness.&#x22;" />
</Frame>

Use that lens for the finish line: the web-app operator demonstrates the pattern end-to-end, and production-readiness practices make the operator maintainable, observable, and safe for operators who inherit it.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/708138ee-3fe0-42cd-b135-8e7df5f7ef59/lesson/a701472e-75cc-4b68-973e-ab1b93a76d38" />
</CardGroup>
