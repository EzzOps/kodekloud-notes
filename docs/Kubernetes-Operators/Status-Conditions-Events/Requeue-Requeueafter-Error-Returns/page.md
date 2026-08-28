# Requeue Requeueafter Error Returns

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Requeue-Requeueafter-Error-Returns/page

Explains how controller-runtime Reconcile return values (ctrl.Result and error) control requeues, retries, timed wakes, and best practices for operator behavior, status reporting, and minimizing noisy retries.

The return line at the bottom of a controller's `Reconcile` function is the controller-runtime's dispatch board. It tells controller-runtime whether this request is finished for now, should be retried because something failed, or should be requeued at a specific time. That single decision shapes how noisy, calm, and reliable your operator behaves.

<Frame>
  <img alt="The image is a flow diagram titled &#x22;The Return Line Is Dispatch,&#x22; showing a process from &#x22;Reconcile returns&#x22; to options including &#x22;Done,&#x22; &#x22;Retry,&#x22; and &#x22;Wake later.&#x22; It includes a note saying, &#x22;The choice shapes the operator.&#x22;" />
</Frame>

Think of `Reconcile` as a technician closing a work ticket. At the end of the ticket the technician must leave one clear instruction for dispatch: work completed for now, the work failed and should be retried, or check back at a specific time. In controller code, the `ctrl.Result` plus the `error` returned are that instruction — they are not just Go bookkeeping.

Key behaviors:

* An empty result and `nil` error: work done for now; rely on watches to enqueue the object later.
* A non-nil error: something truly failed; route the request into a rate-limited retry.
* `RequeueAfter`: schedule a timed wake-up without treating the current pass as a failure.
* `Requeue` (boolean): request another pass soon but without a precise delay.

Examples and guidance

* Clean path: no retry requested now. This means the controller has completed what it can; future reconciles should be driven by watches or external triggers:

```go theme={null}
// Work handled for now.
// Watches will re-enqueue this WebApp when relevant changes occur.
return ctrl.Result{}, nil
```

* Real operation failure: return a non-nil error so controller-runtime retries with backoff. Use this for API failures, transient client errors, or any write/read failure that should be retried:

```go theme={null}
if err := r.Status().Update(ctx, &webapp); err != nil {
    // Real write failure: retry through controller-runtime (rate-limited).
    return ctrl.Result{}, err
}
```

<Callout icon="lightbulb">
  Do not use errors to represent normal, in-progress states. For example, a Deployment still rolling out or a status field that hasn't reached its desired value is not a failure — record that state in status/events and let watches or timed requeues drive the next reconcile.
</Callout>

<Frame>
  <img alt="The image explains that normal waiting is not an error, using examples of &#x22;Still rolling out&#x22; and &#x22;Below desired count,&#x22; both marked as &#x22;Not broken.&#x22; An arrow indicates &#x22;Error for progress.&#x22;" />
</Frame>

* Timed reminders: when you need the controller to wake at a particular time (e.g., poll an external API, renew a certificate before expiry), use `RequeueAfter`. This requests a scheduled requeue without marking the current pass as failed:

```go theme={null}
return ctrl.Result{
    RequeueAfter: 10 * time.Minute,
}, nil

// Not a failure: just check again later.
```

* Unspecified requeue: set `Requeue: true` if you want another pass soon but don't need to specify an exact delay. This is less precise than `RequeueAfter`:

```go theme={null}
// Need a specific delay.
return ctrl.Result{RequeueAfter: d}, nil

// Need another pass soon, but no clear delay.
return ctrl.Result{Requeue: true}, nil

// Prefer watches and a clean return when timing doesn't matter.
return ctrl.Result{}, nil
```

When to prefer each option

* If timing matters (you need to check at a specific future time): use `ctrl.Result{RequeueAfter: <duration>}, nil`.
* If an operation failed and should be retried: return the error (non-nil `err`) so controller-runtime handles retry/backoff.
* If the state is handled for now and future reconciles will be triggered by resource watches: return `ctrl.Result{}, nil`.

Quick reference table

|                                            Situation | Return value                                 | When to use                                             |
| ---------------------------------------------------: | -------------------------------------------- | ------------------------------------------------------- |
|                   Work done for now; rely on watches | `ctrl.Result{}, nil`                         | Default, clean path; avoids extra traffic and log noise |
| Transient or real failure (API error, write failure) | `ctrl.Result{}, err`                         | Let controller-runtime retry with rate limiting         |
|                  Need to re-check at a specific time | `ctrl.Result{RequeueAfter: <duration>}, nil` | Scheduled follow-up (polling, renewal)                  |
|           Want another pass soon, delay not critical | `ctrl.Result{Requeue: true}, nil`            | Less precise than `RequeueAfter`; use sparingly         |

Best practices

* Report waiting states honestly in Status and Events. If a web app is waiting for replicas, set status to reflect that rather than returning an error to force reconciliation.
* Prefer watches (owner/field/annotation watches) to trigger reconciles automatically when possible — it's more efficient and produces cleaner logs and metrics.
* Use `RequeueAfter` when timing matters. Avoid returning errors for expected progress, which overloads retries and hides real failures.

Treat the `Reconcile` return value as part of your operator's behavior, not as an afterthought. It controls retry noise, API server traffic, log quality, and how quickly users see status settle.

<Callout icon="warning">
  Returning errors for expected, in-progress states (for example, a rolling update) will generate unnecessary retries, increase API traffic, and can obscure real failures. Use status + watches or `RequeueAfter` instead of errors for normal waiting.
</Callout>

Links and references

* [controller-runtime: Manager and Reconciler patterns](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* [Kubernetes: Controllers and operator patterns](https://kubernetes.[AWS_SECRET_ACCESS_KEY]/)
* Best practices for operator status, events, and requeue behavior are covered across operator frameworks and Kubernetes docs — prefer documentation that matches your controller-runtime version and operator SDK.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/eb820e30-d0dc-43c7-939a-7628da88a8a8" />
</CardGroup>
