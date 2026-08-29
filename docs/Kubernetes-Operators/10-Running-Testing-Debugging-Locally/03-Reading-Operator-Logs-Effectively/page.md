# Apply namespace and WebApp blueprint, then wait for the deployment to become available
kubectl apply -f ../webapp-demo-namespace.yaml
kubectl apply -f config/samples/webapp-blog.yaml
kubectl -n webapp-demo wait --for=condition=Available deploy/blog --timeout=120s
kubectl -n webapp-demo get webapp blog
# NAME   AGE
kubectl -n webapp-demo get deploy blog
# Shows the deployment created by the controller (expected 3 replicas based on the WebApp spec)
```

Step 2 — Delete the Deployment (missing-child behavior)

* Deleting the Deployment demonstrates that the reconciler will recreate missing children based on the WebApp blueprint.

```bash theme={null}
kubectl -n webapp-demo get cm blog-config
# NAME         DATA AGE
kubectl -n webapp-demo delete deploy blog
# Wait for the controller to recreate the deployment from the WebApp spec
kubectl -n webapp-demo wait --for=condition=Available deploy/blog --timeout=120s
kubectl -n webapp-demo get deploy blog
# deployment restored with 3 replicas (recreated from the blueprint)
```

Step 3 — Scale the existing Deployment to zero (in-place drift)

* Scaling the existing Deployment to zero simulates spec drift while the child resource still exists. In this controller implementation, the reconciler creates missing children but does not patch existing children to match the blueprint. Therefore the controller will not change the replica count back to three when the Deployment exists but has been modified.

```bash theme={null}
kubectl -n webapp-demo scale deploy/blog --replicas=0
sleep 10

kubectl -n webapp-demo get deploy blog
# Shows the deployment with 0 replicas (the controller did not patch it back to 3)
```

Step 4 — Delete the drifted Deployment and wait for recreation

* Now delete the modified (drifted) Deployment. Because it becomes a missing child again, the controller will recreate it from the WebApp spec with three replicas, restoring the application's baseline.

```bash theme={null}
kubectl -n webapp-demo delete deploy blog
kubectl -n webapp-demo wait --for=condition=Available deploy/blog --timeout=120s
kubectl -n webapp-demo get deploy blog
# deployment restored with 3 replicas (recreated from the blueprint)
```

Summary table — behavior comparison

| Scenario                                                        |                 Controller behavior | Notes                                                                                                             |
| --------------------------------------------------------------- | ----------------------------------: | ----------------------------------------------------------------------------------------------------------------- |
| Deleted child resource (missing child)                          | Recreated from the WebApp blueprint | Controller observes no child and creates one to match the desired state.                                          |
| Existing child resource with spec drift (in-place modification) |      Not patched to match blueprint | Controller only created missing children in this implementation; it does not compare-and-patch existing children. |

> **lightbulb** This demonstrates the controller's reconciliation boundary: it heals missing child resources by recreating them from the blueprint, but it does not repair in-place drift of existing child resources (for example, it will not scale an existing Deployment back to the blueprint's replica count).

> **warning** If you need automatic correction of in-place drift (for example, enforcing replica counts, updating image fields, or reconciling any spec drift), extend the reconciler logic to compare and patch existing children to match the desired blueprint spec rather than only creating missing children.

Links and references

* [Kubernetes Controllers and Operators](https://kubernetes.io/docs/concepts/architecture/controller/)
* [Kubebuilder book — Writing a Controller](https://book.kubebuilder.io/)
* [Reconciliation Pattern (controller-runtime)](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/245c1684-705c-4a53-9f56-897dfaf25c71/lesson/2c0752f7-4e6c-43a4-bc07-1aa5fd47de98)


# Reading Operator Logs Effectively

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Running-Testing-Debugging-Locally/Reading-Operator-Logs-Effectively/page

Guide for interpreting Kubernetes operator logs to diagnose controller behavior by tracking object identity, reconcile motion, intent versus observed state, log levels, errors, and troubleshooting steps

Kubernetes operator/controller logs are not a verbatim transcript of every internal action. Instead, they are the flight recorder for your controller: concise clues that help you answer targeted questions about incidents in the cluster. By focusing on identity, motion, and intent vs. reality, you can go from noisy streams to a precise narrative of what happened.

Example controller log fragments:

```text theme={null}
INFO  leader-election  acquired
INFO  cache  synced
INFO  reconcile  webapp="demo/blog"  noticed
INFO  http  GET  /healthz  200
INFO  reconcile  tried create deployment
INFO  reconcile  requeued  -  came back
```

Ask: what did the controller notice? what did it try? why did it come back? Like a flight recorder, you only dig deep when the system shows anomalous behavior.

A typical reconcile sequence looks like:

```text theme={null}
INFO  reconcile  webapp="demo/blog"
INFO  reconcile  checked children
INFO  reconcile  no change needed
INFO  reconcile  requeue after=10s
```

Most lines are routine. Treat the stream as investigative evidence rather than prose — start with a question and use logs to answer it:

* Which object (namespace/name) is this about?
* Did the controller enter reconcile?
* Did it create, update, or skip a child resource?
* Did the API server accept any change?

A useful log line helps answer at least one of those questions:

```text theme={null}
INFO  reconcile  webapp="demo/blog"
INFO  http  GET /metrics 200
INFO  reconcile  entered loop
INFO  cache  synced
INFO  reconcile  created deployment
INFO  webhook  served request
```

Everything else is often background noise.

Look 1 — Identity
The first thing to locate is identity. In a busy controller, reconciles overlap and multiple objects appear in the same stream. The object name and namespace (e.g., `default/demo` or `webapp demo/blog`) are the case number to follow: keep each object’s timeline separate from others.

<Frame>
  <img alt="The image displays a segment titled &#x22;Look 1: Identity&#x22; explaining the use of namespaces and case numbers to differentiate stories, with folders for &#x22;default/demo&#x22; and &#x22;demo/blog&#x22; noting actions like &#x22;noticed&#x22; and &#x22;created svc.&#x22;" />
</Frame>

Look 2 — Motion
Next, observe motion: a healthy reconcile is a short arc — notice the object, check desired children, make a change if needed, then go quiet. If the same object keeps reappearing, the controller might be “chasing its own shadow”.

Watch for log lines that indicate actions which themselves generate more events: requeues, timed retries, or outgoing API calls. These entries often explain subsequent activity in the stream.

<Frame>
  <img alt="The image is a diagram illustrating a process of &#x22;Notice&#x22; → &#x22;Check&#x22; → &#x22;Change&#x22; → &#x22;Quiet,&#x22; with the text &#x22;A healthy reconcile is a small arc&#x22; under a section titled &#x22;Look 2: Motion.&#x22;" />
</Frame>

Look 3 — Intent vs. Reality (generation vs. resourceVersion)
A key signal is the gap between the user’s intent and the cluster’s observed state. In Kubernetes:

* `generation` increments when the user changes the resource spec (intent).
* `resourceVersion` changes whenever the object is written/updated in etcd (observed state).

<Frame>
  <img alt="The image compares &#x22;generation&#x22; and &#x22;resourceVersion,&#x22; indicating that the user's intent is unchanged while the cluster's record keeps changing." />
</Frame>

If `generation` is static while `resourceVersion` keeps increasing, something in the cluster is modifying the object without a user spec change. Often that “something” is your controller. That pattern helps you detect controller-driven churn or other controllers/webhooks mutating the resource.

Log levels — lights and flashlights
Think of log levels as lighting:

* INFO: overhead lighting — useful for regular operations.
* DEBUG: a flashlight — narrow, detailed illumination you enable for a targeted investigation.

Turn on DEBUG only when you need to inspect internals; otherwise it adds noise and hides the important signals.

> **lightbulb** Use INFO for day-to-day monitoring. Enable DEBUG temporarily when investigating a specific reconcile or repeated failures. Remember to disable DEBUG after the incident to avoid log overload.

Respect Errors
Errors demand attention. When non-actionable events are logged at ERROR, real faults can get buried. Differentiate between benign missing-children (controller will create them) and genuine rejections (API refuses update).

```text theme={null}
ERROR webapp="demo/blog"
```

An ERROR like the above means the cluster refused an operation — treat it as the starting point for deeper inspection.

> **warning** If you see repeated ERRORs on the same object, investigate immediately: check the resource's events, validate admission webhooks, confirm immutable-field errors, and inspect `kubectl describe` and `kubectl get -o yaml` outputs.

Quick troubleshooting checklist
Use this compact table to quickly orient any log-based investigation.

| Step              | What to check                                     | Commands / Notes                                             |
| ----------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| Identity          | Which object is involved?                         | Look for `namespace/name` or controller tag in logs.         |
| Motion            | Is there a notice → check → change → quiet arc?   | Repeated requeues indicate churn.                            |
| Intent vs Reality | Are `generation` and `resourceVersion` diverging? | Inspect resource: `kubectl get <kind> <name> -o yaml`        |
| API acceptance    | Did API accept updates or reject them?            | Check `kubectl describe` events and `kubectl get` output.    |
| Debugging         | Need internals? Enable DEBUG briefly              | Toggle controller logging level; follow logs + object state. |

How to read operator logs — a practical habit
Treat logs like evidence:

1. Find the object identity (`namespace/name` or controller-provided tag).
2. Follow the motion: did the controller notice → check → change → quiet, or did it requeue repeatedly?
3. Compare `generation` to `resourceVersion` to detect external vs. controller-driven changes.
4. Use DEBUG logging selectively when you need to see the internals.
5. Connect log lines back to the actual Kubernetes objects (inspect with `kubectl`).

Example repetition that signals a loop:

```text theme={null}
INFO  reconcile  webapp="demo/blog"
INFO  reconcile  requeued (again)
INFO  reconcile  webapp="demo/blog"
INFO  reconcile  requeued (again)
```

By following identity, motion, and intent vs. reality, you can convert noisy log streams into a concise narrative of what the controller did and why.

Further references

* [Kubernetes Concepts: Controllers](https://kubernetes.io/docs/concepts/architecture/controller/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* For designing operator logs, see best practices in structured logging and correlate entries with object keys (namespace/name) to maintain clear timelines.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/245c1684-705c-4a53-9f56-897dfaf25c71/lesson/937ee939-9950-4078-b61b-51433b3e5bbe)
