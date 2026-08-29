# Why Status Matters

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Why-Status-Matters/page

Explains why Kubernetes custom resources must expose observed status separate from spec, how to update status via the status subresource, and use conditions for reliable automation and troubleshooting.

The web app "spec" declares what a user wants. The "status" reports what the cluster actually has. These are related but distinct concepts — keeping them separate is critical for reliable operators, clear troubleshooting, and automation.

<Frame>
  <img alt="The image displays two distinct concepts that need to remain separate: &#x22;spec,&#x22; which represents &#x22;What you want&#x22; or the desired state, and &#x22;status,&#x22; which signifies &#x22;What you have&#x22; or the observed state." />
</Frame>

For example: if a user requests three replicas, that belongs in `spec`. If only two Pods are ready right now, that belongs in `status`. Without exposing status, a custom resource can look successful while hiding important details.

A WebApp object might exist and the controller might have created a Deployment, yet the Pods could still be pulling an image, a Pod could be crashing, or the Deployment might be pending due to cluster capacity.

<Frame>
  <img alt="The image illustrates a process flow with three stages: &#x22;WebApp object exists,&#x22; &#x22;Deployment exists,&#x22; and &#x22;Pods pulling or crashing,&#x22; highlighting that success may appear hidden without status indicators." />
</Frame>

If the WebApp resource does not report what the controller observed, every user must chase child resources and logs to answer a basic question: Is this thing ready?

Example troubleshooting steps users or automation would otherwise need to run:

```shell theme={null}
$ kubectl get webapp site
$ kubectl get deploy site
$ kubectl describe pod -l app=site
$ kubectl logs deploy/webapp-controller-manager
```

Kubernetes already gives a pattern for exposing observed state: built-in resources expose observed fields directly on the object. For example, a Deployment includes `status.availableReplicas` and `status.conditions` so users inspect the Deployment object when they care about the workload.

Example Deployment status:

```yaml theme={null}
kind: Deployment
status:
  availableReplicas: 2
  conditions:
    - type: Available
      status: "True"
      reason: AvailableReason
      message: "2 of 3 replicas are available"
```

Your WebApp custom resource should provide the same contract: it is not only an input for a controller; it is the public status page for the abstraction you created.

Example WebApp status:

```yaml theme={null}
kind: WebApp
status:
  readyReplicas: 2
  conditions:
    - type: Ready
      status: "True"
      reason: Available
      message: "2 of 3 replicas are ready"
```

That stable surface is important for automation as well as humans. A human can dig through `kubectl get deploy`, `kubectl describe pod`, and controller logs. Another controller, a GitOps tool, or an alerting rule needs a stable API field — such as `status.readyReplicas` or a `Ready` condition — to make decisions without understanding every child object your operator manages.

<Frame>
  <img alt="The image is a flowchart illustrating the concept &#x22;Automation Needs One Stable Field,&#x22; showing steps from using tools like Another controller, GitOps tool, and Alerting rule, to making a decision based on a stable field." />
</Frame>

The first status value we often expose is deliberately simple: ready replicas. The controller will inspect the child Deployment, read how many replicas are available, and copy that observed number onto the WebApp `status`. This enforces the core rule: status is derived from the real cluster state. Do not guess it or copy it from `spec` unless the cluster actually matches the requested state.

<Frame>
  <img alt="The image illustrates a process flow about how ready replicas are managed, starting with the controller reading child deployments, deployments reporting replicas, a web app copying the observed value, and advising not to guess readiness from specifications." />
</Frame>

Kubernetes enforces the spec/status split mechanically via the status subresource. A `spec` update changes the desired state; a `status` update reports what the controller observed. Kubernetes exposes these as separate update paths so a user changing `spec` and the controller updating `status` do not overwrite each other.

In controller code you should use the status client to write status:

```go theme={null}
webapp.Status.ReadyReplicas = deploy.Status.ReadyReplicas

if err := r.Status().Update(ctx, &webapp); err != nil {
    return ctrl.Result{}, err
}
```

Status should also be rebuildable. If the `status` block disappeared and the controller reconciled again, it must be able to inspect the cluster and write the same answer. This keeps the operator honest: the source of truth is `spec` plus the real child resources, not some ephemeral controller memory.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Status Should Be Rebuildable,&#x22; outlining a process for status rebuilding: status disappears, re-reading specifications and child resources, writing the same answer back, and highlighting that it's not controller memory." />
</Frame>

<Callout icon="lightbulb">
  Status must be derivable from cluster state alone. Avoid storing ephemeral controller memory in `status`. If a controller restarts, it should be able to recompute status from the child resources and `spec`.
</Callout>

Once you expose a basic observed number, give that number clearer meaning with conditions. Conditions are the standard way to communicate whether a resource is Ready, Progressing, or Blocked. A condition contains structured fields that explain why the resource is in a given state and when it transitioned.

Example `status` with a condition:

```yaml theme={null}
status:
  readyReplicas: 2
  conditions:
    - type: Ready
      status: "True"
      reason: Available
      message: "2 of 3 replicas are ready"
      lastTransitionTime: "2024-06-01T12:34:56Z"
```

Common condition fields and purposes:

| Field                | Purpose                                                          |
| -------------------- | ---------------------------------------------------------------- |
| `type`               | The semantic category, e.g., `Ready`, `Progressing`, `Degraded`. |
| `status`             | One of `True`, `False`, `Unknown`.                               |
| `reason`             | Short machine-readable reason, useful for automation.            |
| `message`            | Human-readable explanation, useful for debugging.                |
| `lastTransitionTime` | When the condition last changed; useful for alerts and history.  |

When the controller observes cluster state, set an appropriate condition and update `status` atomically via the status subresource. In Go, using `metav1.Condition`:

```go theme={null}
import (
    "fmt"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    ctrl "sigs.k8s.io/controller-runtime"
)

// ... inside reconcile
webapp.Status.ReadyReplicas = deploy.Status.ReadyReplicas

metav1.SetStatusCondition(&webapp.Status.Conditions, metav1.Condition{
    Type:               "Ready",
    Status:             metav1.ConditionTrue,
    Reason:             "Available",
    Message:            fmt.Sprintf("%d of %d replicas are ready", deploy.Status.ReadyReplicas, *deploy.Spec.Replicas),
    LastTransitionTime: metav1.Now(),
})

if err := r.Status().Update(ctx, &webapp); err != nil {
    return ctrl.Result{}, err
}
```

(You can use any condition helper you prefer; the important part is computing reproducible conditions from observed state and writing them via the status client.)

Summary

* Export observed state on the custom resource so humans and automation can rely on a single API surface.
* Update status via the status subresource to avoid conflicting writes with user-driven `spec` changes.
* Make status rebuildable from `spec` and child resources — the controller must be able to recompute it after restart.
* Use conditions to give numeric status fields clear, machine- and human-readable semantics.

Links and references

* [Kubernetes CustomResourceDefinition (CRD) and subresources](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [Controller pattern and best practices](https://kubernetes.io/docs/concepts/architecture/controller/)
* [Conditions and status conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#typical-status-properties)
* [sigs.k8s.io/controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/2da54413-a2fc-4423-960c-078f22559fb6" />
</CardGroup>
