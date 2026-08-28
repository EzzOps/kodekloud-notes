# (hanging — no further progress)
```

The old pods keep serving traffic and the new pods never become `Available`. The rollout is stuck.

The instinct for some engineers is to delete the Deployment, redeploy, or wipe the namespace. Please don't — that will likely cause a real outage by removing currently serving pods.

<Callout icon="warning">
  Do not delete the Deployment or namespace to "unstick" a rollout. Deleting running resources is likely to create downtime. Instead, gather diagnostic data and fix the root cause.
</Callout>

This guide walks through a calm, methodical diagnosis you can follow to find the root cause and safely recover.

## Quick checklist (what to inspect)

* Deployment Conditions (`kubectl describe deployment`)
* Pod statuses (`kubectl get pods`)
* Recent events (`kubectl get events --sort-by='.lastTimestamp'`)
* Container logs (`kubectl logs <pod> [-c <container>]`)
* ReplicaSet details (`kubectl describe rs <replicaset>`)
* Probes, image names/credentials, resource requests/limits, node selectors/taints, and ConfigMap/Secret references

Useful references:

* [Kubernetes: Describe Resources](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe)
* [Kubernetes: Pods and Containers](https://kubernetes.io/docs/concepts/workloads/pods/)

## Step 1 — Describe the Deployment

Start with `kubectl describe deployment <name>` and review the Conditions section. A common symptom is `Progressing: False` with `Reason: ProgressDeadlineExceeded`. That tells you the rollout timed out, but it doesn't say why.

Example:

```bash theme={null}
$ kubectl describe deployment myapp
Name:                   myapp
Namespace:              default
Replicas:               3 desired | 3 updated | 2 available | 1 unavailable
Conditions:
  Type:           Status    Reason
  ----            ------    ------
  Available       True      MinimumReplicasAvailable
  Progressing     False     ProgressDeadlineExceeded
```

When you see this, move on to check the Pods and events for the failing ReplicaSet.

## Step 2 — Check the Pods

List pods with `kubectl get pods` and find the new ReplicaSet pods. The `STATUS` is your first clue:

* `Pending`: Pod cannot be scheduled (insufficient resources, node selectors, or taints).
* `ImagePullBackOff`: Image not found or registry/auth issues.
* `CrashLoopBackOff`: Container starts and exits — check logs and probes.
* `Running` but not `Ready`: often a readiness probe problem.

Example output:

```bash theme={null}
$ kubectl get pods
NAME                READY   STATUS             RESTARTS   AGE
myapp-v1-abc123     1/1     Running            0          2d
myapp-v1-def456     1/1     Running            0          2d
myapp-v1-ghi789     1/1     Running            0          2d
myapp-v2-jk1012     0/1     ImagePullBackOff   0          5m
myapp-v2-mno345     0/1     Pending            0          5m
myapp-v2-pqr678     0/1     CrashLoopBackOff   3          5m
```

If a pod is `Pending`, use `kubectl describe pod <pod>` to see scheduling failures; if `ImagePullBackOff`, describe the pod to see the pull error details.

## Step 3 — Read the Events (do not skip this)

Events tell the story of what happened and in what order. Use:

```bash theme={null}
kubectl get events --sort-by='.lastTimestamp'
```

Example:

```text theme={null}
LAST      REASON             OBJECT          MESSAGE
5m        FailedScheduling   myapp-v2-mno    0/3 nodes: Insufficient memory
4m        Failed             myapp-v2-jkl    Failed to pull image "myapp:v2"
3m        Unhealthy          myapp-v2-pqr    Readiness probe failed: HTTP 404
2m        BackOff            myapp-v2-pqr    Back-off restarting failed container
```

From these events you can immediately see scheduling issues, image pull failures, and probe failures. Events often contain the exact hint you need — read the latest ones first.

## Step 4 — Check your Probes

Misconfigured readiness or liveness probes are a surprisingly common cause of stuck rollouts:

* Readiness probe points to the wrong path or port — pod is not marked `Ready` and receives no traffic.
* Liveness probe is too aggressive — container gets killed before it finishes starting.
* HTTP probe returns the wrong status code or uses the wrong scheme (http vs https).

If pods are serving traffic but not marked `Ready`, the Deployment controller will not move Traffic to them and the rollout stalls.

<Frame>
  <img alt="The image features instructions for checking probes, highlighting issues with a readinessProbe using the wrong port and a livenessProbe with a timeout that is too short. There is a note stating, &#x22;Pods are fine.&#x22;" />
</Frame>

Common probe troubleshooting steps:

* Verify probe `path`, `port`, `scheme`, `initialDelaySeconds`, and `timeoutSeconds`.
* Temporarily remove or relax the probe to verify whether it’s the cause.
* `kubectl logs <pod>` and `kubectl exec -it <pod> -- curl -sv http://localhost:<port>/<path>` to test locally inside the container.

## Common pod statuses and suggested actions

| Pod STATUS                | Likely cause                                                       | Action                                                                                                |
| ------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `Pending`                 | Scheduling issues: insufficient CPU/memory, taints, node selectors | `kubectl describe pod <pod>` → check `Events`; adjust requests/limits or taints/selectors             |
| `ImagePullBackOff`        | Image missing or registry auth failure                             | `kubectl describe pod <pod>` → check image and ImagePullSecret; try `docker pull` locally             |
| `CrashLoopBackOff`        | Application crashes on start                                       | `kubectl logs <pod> [-c <container>]` and `kubectl describe pod <pod>`; check startup/liveness probes |
| `Running` but `0/1 Ready` | Readiness probe failing                                            | Inspect probe config and container logs; test endpoint inside pod                                     |

## Example debugging commands

* Describe deployment: `kubectl describe deployment myapp`
* List pods: `kubectl get pods -o wide`
* Describe pod: `kubectl describe pod myapp-v2-abc123`
* Show events: `kubectl get events --sort-by='.lastTimestamp'`
* View logs: `kubectl logs myapp-v2-abc123 [-c container]`
* Exec into pod: `kubectl exec -it myapp-v2-abc123 -- /bin/sh`

What this question is testing
This scenario is not about memorizing commands—it's about structured debugging:

* Inspect Deployment conditions.
* Check pod status and ReplicaSet details.
* Read recent events for failure sequence.
* Verify probes, image names/credentials, resource requests/limits, node selectors/taints, and ConfigMap/Secret references.

I've seen teams waste hours on a rollout that failed because of a tiny typo in a ConfigMap reference — the relevant event was there in the first ten seconds, but nobody read it.

<Frame>
  <img alt="The image highlights the notion that what's being tested is not memorizing commands, but calmly debugging step by step, with an example of a true story involving 3 hours of debugging a stuck rollout." />
</Frame>

<Callout icon="lightbulb">
  Read the events — they usually tell the full story. Debug step-by-step rather than deleting resources. For persistent issues, collect logs, events, and resource descriptions before making changes so you can roll back or apply fixes with minimal risk.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/60905e58-3a8e-4423-9743-081b4959f0a0/lesson/1407017f-1993-4385-ad39-737b601c3826" />
</CardGroup>


# Pod Cant Reach Cluster DNS

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Networking/Pod-Cant-Reach-Cluster-DNS/page

Troubleshooting Kubernetes pod DNS failures by checking CoreDNS health and configuration and verifying network connectivity and NetworkPolicy egress rules allowing UDP and TCP on port 53.

If `nslookup` inside a pod returns nothing, the pod usually cannot reach cluster DNS. Use this guide to quickly diagnose whether the issue is CoreDNS itself or cluster networking (for example, a NetworkPolicy blocking DNS).

Start by checking the DNS provider. In Kubernetes, pods use CoreDNS (running in the `kube-system` namespace) which is exposed via a Service commonly named `kube-dns`. When DNS fails, the two primary areas to investigate are:

* Is CoreDNS healthy and configured correctly?
* Can the pod reach CoreDNS across the network (e.g., no NetworkPolicy or firewall blocking egress)?

Below is a concise troubleshooting flow and examples to inspect CoreDNS and common networking causes.

## 1) Check CoreDNS pods and logs

List CoreDNS pods and look at their status:

```bash theme={null}
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

Example output:

```text theme={null}
NAME                          READY   STATUS             RESTARTS
coredns-5d78c9b7-abcd         1/1     Running            0
coredns-5d78c9b7-fghij        0/1     CrashLoopBackOff   7
```

If any CoreDNS pod is crashing or failing to become ready, fetch its logs and describe the pod to find the cause:

```bash theme={null}
kubectl logs -n kube-system coredns-5d78c9b7-fghij
kubectl describe pod -n kube-system coredns-5d78c9b7-fghij
```

Crashes are often caused by an invalid Corefile configuration.

## 2) Inspect the Corefile (CoreDNS configuration)

CoreDNS uses a Corefile composed of plugins. Typical plugins include:

* `kubernetes` — resolves in-cluster services and pod names to IPs (e.g., `orders.default`).
* `forward` — forwards external queries (e.g., `google.com`) to upstream resolvers.
* `cache` — caches responses for a configurable TTL.
* `loop` — detects and prevents forwarding loops.

Minimal example Corefile:

```text theme={null}
.:53 {
    kubernetes cluster.local       # Service names → IP
    forward . /etc/resolv.conf    # External names → upstream resolver(s)
    cache 30                      # Remember answers for 30s
}
```

If CoreDNS forwards queries to an upstream that resolves back to CoreDNS (an accidental loop), it may detect the loop and exit. To protect CoreDNS from such misconfiguration, include the `loop` plugin:

```text theme={null}
.:53 {
    kubernetes cluster.local       # Service names → IP
    forward . /etc/resolv.conf    # External names → upstream resolver(s)
    cache 30                       # Remember answers for 30s
    loop                           # Guard against forwarding loops
}
```

<Callout icon="warning">
  If CoreDNS logs indicate a forwarding loop and pods are shutting down, correct the Corefile (fix upstream addresses or add `loop`) and then roll the CoreDNS pods to apply the fix.
</Callout>

## 3) If CoreDNS is healthy, check network access (NetworkPolicy / firewall)

When CoreDNS pods are `Running` but pods still cannot resolve names, the next likely cause is blocked network traffic. By default, pods can egress anywhere. But if a namespace has a default-deny egress NetworkPolicy (or other firewall rules), you must explicitly allow DNS traffic.

<Frame>
  <img alt="The image illustrates a network policy check showing a blocked connection from a pod to CoreDNS with the message &#x22;DEFAULT-DENY EGRESS,&#x22; indicating the use of a firewall or network policy." />
</Frame>

What to allow:

* Egress to CoreDNS pods (select by pod labels) or to the cluster DNS IP block (`IPBlock`).
* Both UDP and TCP on port `53` (DNS primarily uses UDP; TCP is used for large responses and zone transfers).

Example egress rule (YAML fragment) allowing egress to CoreDNS pods in `kube-system` by namespace + pod labels:

```yaml theme={null}
egress:
  - to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: kube-system
        podSelector:
          matchLabels:
            k8s-app: kube-dns
    ports:
      - protocol: UDP
        port: 53
      - protocol: TCP
        port: 53
```

Notes:

* NetworkPolicy cannot target a `Service` directly. Allow traffic to the CoreDNS pods (via podSelector and namespaceSelector) or to the DNS IP range.
* If your cluster uses a single cluster DNS IP (ClusterIP Service), you can also allow the cluster IP via an `IPBlock` if you prefer allowing IPs rather than pod selectors.

<Callout icon="lightbulb">
  Always allow both UDP and TCP on port `53` in egress rules to ensure full DNS functionality.
</Callout>

## Quick troubleshooting checklist

| Step                  | What to check                                                               | Example command                                                                                                                                          |
| --------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CoreDNS pods          | Are CoreDNS pods Running / not CrashLoopBackOff?                            | `kubectl get pods -n kube-system -l k8s-app=kube-dns`                                                                                                    |
| CoreDNS logs          | Any errors (Corefile parse errors, forward loops)?                          | `kubectl logs -n kube-system <coredns-pod>`                                                                                                              |
| Corefile              | Is `forward` pointing to a correct upstream? Is `loop` present?             | View ConfigMap: `kubectl -n kube-system get configmap coredns -o yaml`                                                                                   |
| NetworkPolicy         | Are there namepace-level or pod-level deny policies blocking egress to DNS? | `kubectl get networkpolicy -A` and inspect relevant policies                                                                                             |
| Connectivity from pod | Can the pod reach CoreDNS IP or service on port 53?                         | `kubectl exec -it <pod> -- nc -vz <coredns-cluster-ip> 53` or `kubectl exec -it <pod> -- dig @<coredns-cluster-ip> kubernetes.default.svc.cluster.local` |

## Summary

* If a pod can't reach cluster DNS, either CoreDNS is unhealthy (check pods, logs, and the Corefile) or network rules (NetworkPolicies) are blocking DNS traffic.
* Check CoreDNS pod status and logs first. If CoreDNS is healthy, verify NetworkPolicies allow UDP/TCP port `53` to the CoreDNS pods or the DNS IP address range.

A related scenario is when DNS is working but the pod resolves names incorrectly.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/c1eb3967-23d3-4a34-b23d-14a892f95e1d/lesson/69f2b039-aeec-4385-92c7-994129fa4886" />
</CardGroup>
