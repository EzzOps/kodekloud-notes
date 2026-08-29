# Controller Runtime Concepts Manager Controller Reconciler

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Controller-Runtime-Concepts-Manager-Controller-Reconciler/page

Explains Manager, Controller, and Reconciler roles in controller-runtime Kubernetes operators and how they coordinate to reconcile desired cluster state using shared cache, informers, and workqueues.

You will see three words appear over and over in operator code: Manager, Controller, and Reconciler.

They can sound interchangeable at first, but each has a distinct responsibility. Once you can tell them apart, the rest of the codebase stops looking like a pile of helpers. This article builds a clear mental model for each piece and shows how they fit together in a controller-runtime based operator.

Let's start with the manager.

<Frame>
  <img alt="The image describes three roles—Manager, Controller, and Reconciler—each with distinct functions in system management. It emphasizes the importance of distinguishing these roles to improve codebase clarity." />
</Frame>

What the manager is (and is not)

* The manager is the front desk of the building your operator runs in: one process-wide owner of shared infrastructure.
* Exactly one manager runs inside your operator binary. It bootstraps and owns the shared pieces that all controllers use.

<Frame>
  <img alt="The image illustrates a process flow from an &#x22;Operator binary&#x22; to a &#x22;Manager,&#x22; indicating there is exactly one manager. It includes a command-line icon and a block labeled &#x22;MANAGER&#x22; with a crown symbol." />
</Frame>

Core manager-owned resources

* Shared client — the single connection used to read and write Kubernetes objects.
* Shared cache — an in-memory, continuously-updated view of the objects your controllers care about (so you don't query the API server for every read).
* Scheme, logger, metrics server, health probes, webhook server, leader election — all registered and owned by the manager so controllers can share them.

<Frame>
  <img alt="The image illustrates a manager's responsibilities, including a &#x22;SHARED CACHE&#x22; with services labeled as &#x22;Running&#x22; or &#x22;Pending.&#x22; An HQ icon is also shown." />
</Frame>

<Frame>
  <img alt="The image is a diagram titled &#x22;The Manager Owns the Shared Machinery,&#x22; highlighting components such as Scheme, Logger, Metrics server, Health probes, Webhook server, and Leader election around a central &#x22;Manager.&#x22;" />
</Frame>

Because controllers share the manager-owned cache and client, multiple controllers watching the same resource type do not each open individual watches against the API server. They read from the same shared cache instead.

<Frame>
  <img alt="The image illustrates a setup with two controllers, A and B, both monitoring pods in a shared cache. The shared cache shows the status of three pods: two are running, and one is pending." />
</Frame>

Next: the controller

If the manager is the front desk, a controller is a staff member assigned to watch a specific set of rooms. You tell the controller: "watch WebApp objects and also watch the Deployments and Services I own."

Under the hood, a controller wires up informers and workqueues:

* Informer: a live feed — a subscription that streams changes from the API server into the shared cache (no periodic polling required).
* Predicate: a true/false filter (think of it as a bouncer). Only events that pass predicates get queued.
* Workqueue: an ordered queue of work items with retries and rate-limiting. Items are typically just `namespace/name` keys — not the full object or the event payload.

<Frame>
  <img alt="The image illustrates a system where an API server watches and streams changes to an &#x22;Informer,&#x22; which provides a live feed subscription to update a shared cache, replacing the need for frequent API polling." />
</Frame>

Reconciler: the single method you implement

You almost never instantiate a controller directly. Instead, you implement a reconciler that provides one method: `Reconcile`. The controller runtime calls this method with a context and a request; your job is to make the cluster match the desired state.

Example Reconcile signature in Go:

```go theme={null}
func (r *WebAppReconciler) Reconcile(
    ctx context.Context,
    req ctrl.Request,
) (ctrl.Result, error) {
    // the reconciliation loop:
    // 1. read current state from the cache/client
    // 2. compute desired state
    // 3. create/update/delete resources so the cluster matches desired state
    return ctrl.Result{}, nil
}
```

Important: `req` is just a namespaced name (`namespace/name`) — no object, no event, no diff. This is deliberate.

<Frame>
  <img alt="The image explains a reconciler method called &#x22;Reconcile,&#x22; showing a request with a namespace &#x22;webapp-ns&#x22; and name &#x22;webapp-a,&#x22; along with notes saying &#x22;No object,&#x22; &#x22;No event,&#x22; &#x22;No diff,&#x22; and &#x22;That is deliberate.&#x22;" />
</Frame>

Think of the `req` like a kitchen ticket at a restaurant: it has a table number, not the meal. The controller gives you the table number; your Reconcile must look up the current state and ensure the right resources are present.

If you return an error or a `ctrl.Result` that requests requeueing (for example, `return ctrl.Result{RequeueAfter: time.Minute}, nil`), the workqueue will schedule the request again.

Putting it all together: the operator heartbeat

* The manager starts and registers controllers.
* Each controller's informer keeps the shared cache fresh.
* An API server change triggers an event; predicates filter it; the namespaced key is enqueued.
* A worker pulls the key off the workqueue and calls your Reconcile.
* Your Reconcile reads from the cache, uses the client to write, and returns a result.

<Frame>
  <img alt="The image is a flowchart titled &#x22;The Full Loop – The Heartbeat of an Operator,&#x22; illustrating a sequence of steps in an operator's process, from &#x22;Manager&#x22; starting the controller to updating the &#x22;API Server.&#x22;" />
</Frame>

This cycle repeats indefinitely; it is the heartbeat of every operator.

Three essential rules for writing Reconcile

* Reconcile is level-based, not edge-based — read the current state and make it match the desired state. You may be called once for many rapid events; that's okay.
* Reconcile must be idempotent — running it multiple times should be safe and converge to the same result.
* Reconcile should be fast — long-running tasks belong in a goroutine, background job, or separate controller. Blocking Reconcile delays the workqueue.

<Frame>
  <img alt="The image illustrates the reconciliation process, showing that multiple changes trigger a single Reconcile function, which then reads the current state. It highlights three rules for writing reconcile: level-based, idempotent, and fast." />
</Frame>

> **lightbulb** Three quick tips: 1) Design Reconcile to read current state (level-based). 2) Make it idempotent. 3) Keep it short — move long tasks out of the reconcile loop.

Quick reference: Manager vs Controller vs Reconciler

| Component  | Responsibility                                                                                | Example / Notes                                                         |
| ---------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Manager    | Bootstraps and owns shared infrastructure (client, cache, scheme, logger, webhooks, metrics). | Single per operator process.                                            |
| Controller | Wires informers, predicates, and the workqueue for a specific resource set.                   | Registers with manager; sets up watches.                                |
| Reconciler | Implements the `Reconcile(ctx, req)` method to make cluster state match desired state.        | `req` is a `namespace/name` key. Reconcile must be idempotent and fast. |

Links and references

* [Controller Runtime (sigs.k8s.io/controller-runtime)](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* [Kubernetes: Writing an Operator (official docs)](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
* [Client-go Informers and Workqueues](https://github.com/kubernetes/client-go)
* [Design Patterns for Kubernetes Operators](https://kubernetes.io/blog/2019/03/06/building-operators-with-kubernetes/)

That's it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/6567c490-0938-44e5-9c4e-b55ba843d46a)
