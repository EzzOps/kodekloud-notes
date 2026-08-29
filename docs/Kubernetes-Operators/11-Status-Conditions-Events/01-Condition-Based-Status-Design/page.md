# Condition Based Status Design

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Condition-Based-Status-Design/page

Explains using Kubernetes status conditions to report resource health, mapping gauges to machine and human friendly condition fields with best practices for Ready, Progressing, and Degraded

A number can tell you the gauge reading. A condition tells you what the reading means.

In Kubernetes controllers, numeric status fields (for example, `ReadyReplicas`) are gauges — they show measurements. Conditions are the dashboard lights beside those gauges. If a web app's spec requests three replicas but only one is ready, `ReadyReplicas` gives the count. A condition answers the human questions that follow:

* Is this still rolling out?
* Is it healthy enough?
* Or is something stuck?

Think of conditions as compact, machine- and human-friendly health signals. They belong in `status` because status is the controller’s report about the real cluster: `spec` is the user’s intent; `status` is what the controller actually observes. Kubernetes provides a shared shape for these reports via `metav1.Condition`.

<Frame>
  <img alt="The image is a flowchart illustrating the process of a controller observing what is asked and determining the conditions, with the headline &#x22;Conditions Belong in Status.&#x22;" />
</Frame>

What is a condition? At its simplest, a condition is one dashboard light with:

* Type — a name for the light
* Status — the current state (`True`, `False`, `Unknown`)
* Reason — a short, stable, machine-friendly label
* Message — a human-readable sentence explaining the observation
* LastTransitionTime — when the condition last changed
* ObservedGeneration — which `metadata.generation` the status reflects

A real-world example in Go:

```go theme={null}
metav1.Condition{
    Type:               "Ready",
    Status:             metav1.ConditionTrue,
    Reason:             "DeploymentAvailable",
    Message:            "Deployment has the requested ready replicas.",
    LastTransitionTime: metav1.Now(),
    ObservedGeneration: webapp.Generation,
}
```

Fields mapped to intent and usage:

| Field                | Purpose                                                                            | Example                            |
| -------------------- | ---------------------------------------------------------------------------------- | ---------------------------------- |
| `Type`               | The short name of the question being asked (the light).                            | `Ready`, `Progressing`, `Degraded` |
| `Status`             | The current answer: `True`, `False`, or `Unknown`.                                 | `True`                             |
| `Reason`             | Short, stable machine label for automation and alerts. Keep predictable.           | `DeploymentAvailable`              |
| `Message`            | Human-friendly explanation for operators.                                          | `1 of 3 replicas are ready.`       |
| `LastTransitionTime` | Timestamp when the condition last changed state. Do not update on every reconcile. | `2024-07-01T12:34:56Z`             |
| `ObservedGeneration` | The `metadata.generation` that the controller observed for this status.            | `webapp.Generation`                |

Do not confuse `LastTransitionTime` with frequent reconciles: it should only change when the condition flips. That allows operators to know how long a resource has been in a particular state. `ObservedGeneration` prevents stale green lights: if `Ready` is `True` but `ObservedGeneration` is older than the latest `metadata.generation`, the status refers to a previous spec.

Example YAML snippet that separates machine- and human-facing fields:

```yaml theme={null}
type: Ready
status: "False"
reason: DeploymentNotReady
message: "1 of 3 replicas are ready."
