# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Section-Overview/page

Improving a WebApp Kubernetes controller to report observed state via status fields, conditions, events, and explicit reconcile requeue decisions so users see health and progress.

The WebApp controller already creates the child resources defined by a WebApp custom resource: a Deployment, a Service, and a ConfigMap. However, from the user's perspective the controller remains largely silent — it builds the children but does not report what it observes.

<Frame>
  <img alt="The image shows a diagram illustrating a &#x22;WebApp controller&#x22; that generates &#x22;Deployment,&#x22; &#x22;Service,&#x22; and &#x22;ConfigMap&#x22; components, with the caption &#x22;It Builds the Children, but Stays Quiet.&#x22;" />
</Frame>

When you run kubectl get on the WebApp resource, the output doesn't indicate whether the Deployment is ready, whether the controller is still working, or whether anything noteworthy occurred during reconcile:

```bash theme={null}
$ kubectl get webapp web-app-sample -o yaml
spec:
  image: nginx:1.27
  replicas: 3
status: {}
```

Kubernetes resources are more helpful when they report observed state where users already look for it. Built-in controllers routinely separate intent and observation:

* `spec` holds the user's desired intent.
* `status` records observed facts.
* `conditions` summarize readiness and progress in a structured, machine-readable way.
* `events` provide a concise timeline of important actions.

For comparison, `kubectl describe` on a Deployment shows both intent and observed state:

```bash theme={null}
$ kubectl describe deploy web-app
spec.replicas          3
status.readyReplicas   2
conditions             Available=False
events                 ScalingReplicaSet
```

This lesson upgrades the WebApp API so it moves from silent creation to visible operation. The controller will populate `status` with facts it observes from the cluster — for example, how many pods are ready behind the Deployment — and will also publish conditions and events so users get immediate, actionable feedback.

<Frame>
  <img alt="The image illustrates a two-step process for custom resources: &#x22;Silent creation,&#x22; which builds and says nothing, followed by &#x22;Visible operation,&#x22; which reports what it sees." />
</Frame>

Spec is an input: it declares what the user asked for. Status is observational: it reports what the controller has seen. Conditions attach structured names, statuses, and reasons to that observation so humans and other controllers can quickly assess health and progress.

<Callout icon="lightbulb">
  Treat `spec` as the desired state (user intent) and `status` as the controller's observed facts. Conditions are a concise, machine-readable summary of that observed state.
</Callout>

Conditions let the controller communicate higher-level health states directly instead of forcing users to infer them from raw numbers. For a WebApp you might expose types such as Ready, Progressing, and Degraded with `True`/`False` statuses and machine-friendly `reason` and `message` fields. That creates a compact health report other tools can read without scraping logs.

<Frame>
  <img alt="The image displays a table of conditions with types (Ready, Progressing, Degraded), statuses (True, False), and corresponding reasons." />
</Frame>

Events add short-lived contextual information. When the controller creates a child object, encounters unexpected input, or reaches an operational milestone, emitting an Event makes that action visible through `kubectl describe`. Logs remain essential for deep debugging, but Events surface the most relevant actions to resource owners.

Requeue behavior completes the observable story: the reconcile loop should make explicit decisions about whether to

* check again after a delay,
* return an error (so controller-runtime retries), or
* stop cleanly because the current state already matches the desired state.

Explicit requeue decisions ensure status updates and events reflect intentional controller behavior rather than accidental timing.

<Frame>
  <img alt="The image describes three types of deliberate reconcile decisions: &#x22;Check again&#x22; (re-run after a delay), &#x22;Return error&#x22; (controller-runtime retries), and &#x22;Stop cleanly&#x22; (state is already correct) in a reconcile loop." />
</Frame>

Summary of what this section adds to the WebApp controller:

| Feature                 | Where recorded         | Example / purpose                                                        |
| ----------------------- | ---------------------- | ------------------------------------------------------------------------ |
| Observed replica counts | `status.readyReplicas` | Show how many pods are actually ready                                    |
| Structured readiness    | `status.conditions[]`  | `Type=Ready/Progressing/Degraded`, with `Status`, `Reason`, `Message`    |
| User-visible timeline   | Events                 | Short-lived notes that appear in `kubectl describe`                      |
| Intentional retries     | Requeue decisions      | `RequeueAfter`, return error, or no requeue to reflect controller intent |

By the end of this section, the WebApp controller will still create and manage child resources, but it will also explain what it sees and why it made particular reconcile decisions — directly where users look for that information.

<Frame>
  <img alt="The image contains text describing how a web application will eventually explain itself, with listed items like &#x22;status.readyReplicas&#x22; and &#x22;conditions[]&#x22;. There's also a button labeled &#x22;Now it explains what it sees.&#x22;" />
</Frame>

Links and references

* Kubernetes API conventions for `status` and `conditions`: [https://github.com/kubernetes/[AWS_SECRET_ACCESS_KEY]/sig-architecture/api-conventions.md#typical-status-properties](https://github.com/kubernetes/[AWS_SECRET_ACCESS_KEY]/sig-architecture/api-conventions.md#typical-status-properties)
* Best practices for kubectl and resource visibility: [https://kubernetes.io/docs/reference/kubectl/overview/](https://kubernetes.io/docs/reference/kubectl/overview/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/13e9b4c4-3ab5-46b8-90d8-13912cd3bdc4" />
</CardGroup>
