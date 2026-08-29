# perform the task on this host
$ exit
# then SSH into the next question host
$ ssh 000a1234
```

Discipline: SSH → complete task → exit → SSH into next host → repeat.

## 6) Troubleshoot Kubernetes primitives first

When something fails, follow a predictable, layered troubleshooting approach. Many issues are plain Kubernetes problems (pods, services, labels) rather than Istio-specific misconfigurations.

Troubleshooting checklist:

| Step                 | What to check                                           | Example commands                                                                        |
| -------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 1. Pod state         | Is the Pod Running / CrashLooping?                      | `kubectl get pods -n <namespace>`                                                       |
| 2. Service selection | Does Service selector match Pod labels?                 | `kubectl get svc -n <namespace>`; `kubectl get pods --show-labels -n <namespace>`       |
| 3. Connectivity      | Can the Service be reached from another Pod?            | `kubectl exec -n <namespace> <pod> -- curl http://svc:port`                             |
| 4. Istio resources   | Check Gateway, VirtualService, DestinationRule, Sidecar | `kubectl get virtualservice,destinationrule,gateway -n <namespace>`                     |
| 5. Logs / proxy      | Inspect app logs and Envoy sidecar logs                 | `kubectl logs -n <namespace> <pod>`; `kubectl logs -n <namespace> <pod> -c istio-proxy` |

Do not jump straight to Istio resources — verify basic Kubernetes plumbing first (ports, labels, pods running).

<Frame>
  <img alt="The image is a flowchart for troubleshooting Kubernetes (K8s) issues, showing the sequential steps of checking an app, service, and route/ingress, with elements such as route, service, and pods." />
</Frame>

## 7) Attempt questions for partial credit

The exam awards partial credit if you create resources with the correct name and namespace, even if the spec is incomplete. If a question looks complex (e.g., DestinationRule with circuit breakers), create the resource with the correct metadata first, then expand the spec.

Minimal DestinationRule example to earn partial credit:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: app-ds
  namespace: frontend
spec:
  host: app-svc
  trafficPolicy:
    connectionPool: {}
```

Create the resource quickly, then iterate to improve fields. Partial credit for correct resource names and namespaces can make a big difference.

## 8) Time management — move on, then come back

The modern ICA typically contains \~16 hands‑on questions, each with its own host. If you're stuck on a task, move to the next one and return later. Use the time to collect easier points — a final pass to improve partial answers often recovers significant marks.

## Quick exam checklist

* Know where to find relevant Istio docs and examples.
* Use a large screen if allowed; confirm proctor rules first.
* Be comfortable with an efficient text editor (Vim recommended).
* Always run `istioctl analyze` after applying resources.
* SSH into each question host, complete the task, then exit.
* Verify Pod → Service → Connectivity before Istio checks.
* Create minimally correct resources for partial credit.
* Manage time: move past blockers and review later.

## Links and references

* [Istio Documentation — Official](https://istio.io/latest/docs/)
* [istioctl analyze — Diagnostics](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/)
* [Istio Service Mesh course on KodeKloud](https://learn.kodekloud.com/user/courses/istio-service-mesh)
* [CKA Certification Course on KodeKloud](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator)

Good luck on the ICA — stay calm, follow the checklist, and iterate from minimal working resources to finalized configurations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/3b1a1d7c-b04a-4a3d-bf30-65da7d5460c3/lesson/e8f37b20-639b-44b8-93a8-0b637f88846d" />
</CardGroup>


# Cleanup Label

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Cleanup-Policies/Cleanup-Label/page

Explains Kyverno's per resource cleanup TTL label for automatic deletion, supported TTL formats, RBAC needs, reconciliation timing, and when to use label versus cluster cleanup policies.

When you need ongoing cluster housekeeping, scheduled, rule-based cleanup policies are ideal. But for resources that are known to be temporary at creation time — for example, a debug Pod, a short-lived namespace for a CI job, or a one-off test resource — Kyverno provides a simple, per-resource mechanism: the reserved label `cleanup.kyverno.io/ttl`.

How it works

* Add the `cleanup.kyverno.io/ttl` label to a resource's metadata at creation time.
* The Kyverno Cleanup Controller watches for that label, records the resource and its expiration, and deletes the resource when the TTL has passed.

<Frame>
  <img alt="The image illustrates the process of using the cleanup.kyverno.io/ttl label on Kubernetes resources, explaining how Kyverno handles cleanup by identifying the label, calculating expiration time, and deleting the resource when time is up." />
</Frame>

No policy required

Important: you do not need a cleanup policy for this to work. The presence of the `cleanup.kyverno.io/ttl` label on the resource itself is the instruction — the label triggers the Cleanup Controller to act.

TTL value formats

Kyverno supports two TTL value formats:

| Format             | Description                                                                                                                     | Examples                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Relative duration  | A duration relative to the moment Kyverno first sees the label. Uses standard duration units (s, m, h).                         | `30s`, `2m`, `1h`, `24h` |
| Absolute timestamp | An exact UTC deletion time using ISO 8601 / RFC 3339 format. Deletion occurs at that UTC timestamp regardless of creation time. | `2026-07-15T15:04:05Z`   |

<Frame>
  <img alt="The image explains two supported TTL value formats in Kyverno: &#x22;Relative Duration,&#x22; which specifies a time duration from when the label is seen, and &#x22;Absolute Timestamp (ISO 8601),&#x22; which specifies a specific UTC date and time for resource deletion." />
</Frame>

<Callout icon="lightbulb">
  Choose a relative duration when you want the countdown to start at creation time. Use an ISO 8601 timestamp when you require deletion at a precise UTC moment.
</Callout>

Practical example

A developer needs a temporary Pod to debug an issue and wants to ensure it is cleaned up automatically. Add the TTL label to the Pod manifest:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: temp-debug-pod
  labels:
    # The magic label!
    cleanup.kyverno.io/ttl: 2m
spec:
  containers:
    - name: debug-tools
      image: busybox:1.35
      args:
        - sleep
        - "1d" # The container will run longer, but Kyverno will delete the Pod per TTL
```

When created, the Cleanup Controller records the resource and schedules deletion after two minutes. The container’s internal runtime does not prevent Kyverno from deleting the Pod when the TTL expires.

Permissions and RBAC

The TTL label is a trigger; the Cleanup Controller performs the actual deletion. Therefore, the controller must have the appropriate RBAC permissions to delete the resource type you label.

* Label a Pod for deletion → the controller must have `delete` permission on `pods`.
* Label a Deployment for deletion → the controller must have `delete` permission on `deployments`.

<Frame>
  <img alt="The image is a reminder about permissions for labeling in a system. It explains that when using a TTL label, the controller requires permission to delete Pods or Deployments." />
</Frame>

<Callout icon="warning">
  Ensure the Kyverno Cleanup Controller's ClusterRole (or aggregated role) includes the `delete` verb for every resource type you want TTL-based cleanup to manage. Missing delete permission prevents Kyverno from removing labeled resources.
</Callout>

The permission model is unified: the same aggregated ClusterRole that grants delete permissions for cleanup policies also covers TTL-based deletions. Grant the appropriate permissions once and both mechanisms will work.

Reconciliation and timing guarantees

A TTL like 90 seconds is respected, but deletion may not occur at the exact second the TTL expires. For efficiency, the Cleanup Controller reconciles periodically rather than continuously scanning all labeled resources.

Example timeline:

* Controller runs at 1 minute — sees the Pod but not expired.
* TTL expires at 90 seconds — controller is not running at that exact moment.
* Next controller run (e.g., 2 minutes) — controller detects the expired Pod and deletes it.

This periodic schedule is called the reconciliation interval and is configurable on the controller (default: `1m`).

<Frame>
  <img alt="The image is titled &#x22;Fine-Tuning: The Reconciliation Interval&#x22; and features a question about TTL deletion timing, with an answer explaining that the Cleanup Controller runs on a schedule, not checking every second." />
</Frame>

You can adjust the controller behavior with the `--ttlReconciliationInterval` flag (or corresponding configuration), for example:

```text theme={null}
--ttlReconciliationInterval=30s
```

Smaller intervals yield closer-to-exact deletion timing at the cost of more frequent controller reconciliation.

<Frame>
  <img alt="The image provides technical details about the &#x22;Reconciliation Interval,&#x22; including its configuration using the --ttlReconciliationInterval flag in the Kyverno cleanup controller, and states that the default value is 1 minute." />
</Frame>

When to use each cleanup method

Use the method that best fits your workflow:

| Method                         | Trigger                                                         | Who typically applies it                               | Best use cases                                                                                                  |
| ------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| Cleanup policies               | Policy rules that find and delete resources (labels, age, etc.) | Cluster administrators                                 | Broad, ongoing housekeeping; discovering stale resources across namespaces                                      |
| `cleanup.kyverno.io/ttl` label | Per-resource label indicating deletion time/duration            | Developers or automation (CI/CD) creating the resource | Per-resource, self-contained expiration behavior; temporary debug Pods, ephemeral test namespaces, CI artifacts |

<Frame>
  <img alt="The image is a comparison table outlining when to use the methods &#x22;CleanupPolicy&#x22; and &#x22;cleanup.kyverno.io/ttl Label,&#x22; detailing aspects such as how each works, triggers, who defines them, and best use cases." />
</Frame>

Summary

* Use cleanup policies for administrator-defined, rule-driven housekeeping across the cluster.
* Use `cleanup.kyverno.io/ttl` for per-resource, explicit expiration when resources are known to be temporary at creation time.

Further reading and references

* Kyverno Cleanup Controller (docs): [https://kyverno.io/docs](https://kyverno.io/docs)
* ISO 8601 / RFC 3339 timestamps: [https://www.ietf.org/rfc/rfc3339.txt](https://www.ietf.org/rfc/rfc3339.txt)
* Kubernetes RBAC documentation: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/38c696a0-131e-44d4-9265-2e8b3c6abe20/lesson/06aa49c9-fc2f-4f26-9e16-d0c557f8fb9a" />
</CardGroup>
