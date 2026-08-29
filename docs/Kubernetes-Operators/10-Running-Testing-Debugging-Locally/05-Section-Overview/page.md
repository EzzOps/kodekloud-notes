# Install the CRD so the API server recognizes the WebApp type
make install

# Run the controller manager locally (connects to the cluster using your kubeconfig)
make run

# Apply a sample WebApp to exercise reconcile behavior
kubectl apply -f config/samples/webapp_v1alpha1_webapp.yaml
```

Think of the manager as a local process that hosts your controller and talks to the API server using the kubeconfig on your machine. To the cluster it is just another API client; to you it is an easily stoppable, restartable, and observable process.

Use the following quick-reference to map steps to their intent:

| Command / Action                       | What question it answers                                             |
| -------------------------------------- | -------------------------------------------------------------------- |
| `make install`                         | Does the cluster know this API type (is the CRD installed)?          |
| `make run`                             | Can my controller watch that type and react (is reconcile wired up)? |
| `kubectl apply -f config/samples/...`  | What does my controller do with a real resource?                     |
| `kubectl get` / logs / manager console | What actually happened — resource state and runtime evidence?        |

When running locally, you will typically check the manager output in your terminal (where `make run` runs) and use `kubectl get` to inspect resource state. For cluster-side evidence, use `kubectl` (for example `kubectl get webapp -A`) and for in-cluster components inspect Pod logs once you deploy the packaged controller.

> **lightbulb** Use local mode for fast feedback on reconcile logic and resource reads/writes. Treat it as a development workbench: quick, iterative testing to validate behavior before you move on to packaging and in-cluster validation.

Local mode is powerful, but it has limits. It can validate reconcile behavior, confirm reads and writes against real objects, and produce log evidence. It cannot prove final production concerns such as the exact deployment shape, service account permission boundaries (your kubeconfig user can be more privileged than the controller's in-cluster identity), leader election behavior, webhook admission controllers, or production networking and RBAC interactions.

<Frame>
  <img alt="The image lists the capabilities and limitations of local mode, highlighting what it can and cannot prove about system behavior. It includes items like reconciled behavior, object reads and writes, and log evidence on the left, while limitations such as final deployment shape and service account permissions are noted on the right." />
</Frame>

Those checks belong in subsequent stages of testing and CI. For now, use local mode for what it does best: rapid iteration and evidence-driven debugging. Later, the workbench output becomes the raw material for deeper debugging, packaging, and production verification.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/245c1684-705c-4a53-9f56-897dfaf25c71/lesson/c597f5fe-d6ad-4c91-8b27-2cb6c9bbdb28)


# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Running-Testing-Debugging-Locally/Section-Overview/page

How to run, test, and debug a Kubernetes operator locally using a fast iterate loop to observe reconcile behavior, logs, events, and diagnose issues before packaging

Section five is where the operator stops being just a diagram and becomes a diagnosable machine.

A controller is only useful when you can run it, observe it, and explain what it did. Think of the local development loop like testing a smoke detector before you install it in an entire building: you don’t need the final packaging yet. You need a quick way to press the button, hear the beep, and confirm the wiring is alive.

<Frame>
  <img alt="The image shows a circular button with the text &#x22;TEST&#x22; surrounded by dotted lines, with instructions to &#x22;Press&#x22; and &#x22;Beep&#x22; indicating a fast feedback loop without final packaging." />
</Frame>

For this operator, that "button" is a WebApp resource, and the "beep" is the reconciled evidence you can observe in logs and cluster state.

You already have the critical first win: a WebApp produces a Deployment, a Service, and a ConfigMap. That proves the controller has a useful reconcile path.

<Frame>
  <img alt="The image is a diagram showing the components of a web application, including WebApp, Deployment, Service, and ConfigMap, suggesting a proven path for deployment with matching pods, stable addresses, and configuration. It is titled &#x22;The First Win You Already Have&#x22; and credits KodeKloud." />
</Frame>

Make that path a repeatable habit: install the API shape, run the manager locally, apply a WebApp, read events and logs, stop, change something, and run again.

<Frame>
  <img alt="The image depicts a diagram titled &#x22;The Repeatable Loop&#x22; illustrating a &#x22;Local dev loop&#x22; with steps including &#x22;Run manager,&#x22; &#x22;Apply WebApp,&#x22; &#x22;Read evidence,&#x22; &#x22;Stop,&#x22; and &#x22;Change,&#x22; along with a setup prompt to &#x22;install the API shape.&#x22;" />
</Frame>

Start in local run mode: the manager runs as a regular process on your workstation and talks to the cluster through your kubeconfig instead of running as a Pod. This makes the loop fast and gives you a clear boundary between controller logic and packaging/runtime concerns.

<Frame>
  <img alt="The image is a slide about the limitations of local mode, highlighting its suitability for reconciling logic and logs, but not for packaging, service account permissions, webhooks, or production deployments." />
</Frame>

> **lightbulb** Local run mode is ideal for iterating on reconcile logic, observing logs, and validating controller behavior quickly. It does not validate packaging, Pod ServiceAccount permissions, webhook configurations, or production deployment nuances.

How to observe what matters

* Focus on three diagnostic questions when reading logs and events:
  1. Which WebApp instance was handled? (namespace/name)
  2. What did the controller attempt to do? (created/updated/deleted child resources)
  3. Did the cluster accept the change? (events, API errors, resource state)
* Use `kubectl describe` and `kubectl get` together with controller logs to correlate events and state changes.

Quick checklist for the local dev loop

| Step                | Purpose                               | Example                                       |
| ------------------- | ------------------------------------- | --------------------------------------------- |
| Install API shape   | Make the CRD available in the cluster | `kubectl apply -f config/crd/bases/`          |
| Run manager locally | Fast iterate on reconcile logic       | `make run` or `go run ./main.go`              |
| Apply a WebApp      | Trigger reconciliation                | `kubectl apply -f testdata/webapp.yaml`       |
| Read evidence       | Events, logs, and resource status     | `kubectl describe webapp` and controller logs |
| Change something    | Introduce a drift or bug              | edit `testdata/webapp.yaml` and reapply       |
| Repeat              | Confirm fix or behavior               | re-run manager and observe results            |

Diagnosing a noisy controller

* A noisy terminal is not the goal — you want the few lines that answer the three diagnostic questions above.
* Look for symptoms like: repeated reconciles, resources that never reach the desired state, or missing events.
* Key fields to compare when debugging the reconcile lifecycle:
  * `metadata.generation` vs `status.observedGeneration`
  * Event counts and repeated reconcile logs
  * API errors that may have been swallowed by higher-level code

Common debugging story (what you will practice)

* The controller appears alive, but the resource never settles.
* Compare `metadata.generation` and `status.observedGeneration` to find reconciliation gaps.
* Count repeated reconcile attempts to detect hot loops.
* Uncover swallowed API errors by looking at the controller logs and event stream.
* Fix issues such as a label that changes every reconcile (causing continuous reconciliation) or a transient API rejection.

Scope and boundary testing

* The lab asks you to prove the current boundary of your reconciler: what it can and cannot repair.
* Example: the reconciler may recreate a missing child resource (restoring a missing part from the blueprint), but it might not repair every drifted field on an existing child resource.
* Use status updates and events to document what the controller actually guarantees.

> **warning** Local mode helps you validate controller logic quickly but does not replicate production packaging, RBAC, admission webhook behavior, or Pod-level runtime permissions. Always validate those aspects in a realistic cluster deployment before production rollout.

References and next steps

* When you’ve mastered the local loop, move on to tests that validate controller behavior (unit and integration), then package and deploy the manager as a Pod to exercise ServiceAccount, RBAC, and webhook interactions.
* Useful links:
  * [Kubernetes Controllers and Operators](https://kubernetes.io/docs/concepts/architecture/controller/)
  * [Writing Kubernetes Controllers](https://book.kubebuilder.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/245c1684-705c-4a53-9f56-897dfaf25c71/lesson/62a94d81-f1dd-4719-b63c-6d8c1f12db2f)
