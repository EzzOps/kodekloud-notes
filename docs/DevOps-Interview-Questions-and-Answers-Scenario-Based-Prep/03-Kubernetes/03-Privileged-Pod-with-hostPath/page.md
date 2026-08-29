# Privileged Pod with hostPath

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Kubernetes/Privileged-Pod-with-hostPath/page

Risks and mitigations for Kubernetes pods with privileged hostPath mounts, showing attack vectors, containment steps, and staged hardening and policy enforcement to prevent node and cluster compromise.

Let's walk through a common Kubernetes security scenario you might encounter in an interview, audit, or post-incident review.

You're auditing a production cluster and discover a pod running as root with a `hostPath` mount of the node's root filesystem (`/`). That pod can read and write anything on the host. Your manager asks:

1. How bad is this?
2. How do we fix it without breaking production?

Short answer: a privileged pod with an unrestricted `hostPath` can lead to full node compromise and often cluster-wide escalation. Below we explain why, show the attack surfaces, and give a pragmatic, low-friction mitigation plan you can roll out safely.

## Why this is so dangerous (attack vectors)

A pod with access to the node’s root filesystem can extract secrets and operational credentials from the node, then impersonate node-level components to escalate access.

* Kubelet credentials: The pod can read kubelet credentials on the node and use them to talk to the API server. Depending on RBAC rules and kubelet privileges, an attacker could read secrets, create resources, or escalate further.
* Container runtime socket: The pod can access the container runtime socket (for example, `/var/run/docker.sock` or `/run/containerd/containerd.sock`) and control the runtime directly to spawn privileged containers on the node — bypassing the API server entirely.

<Frame>
  <img alt="The image is a diagram illustrating a Kubernetes security vulnerability, showing an attack chain where kubelet credentials are stolen, the kubelet is impersonated to access the API, and all secrets are pulled from etcd." />
</Frame>

If an attacker compromises such a pod, it’s not just a pod-level incident — you can have a fully compromised node and, in many clusters, that can lead quickly to a cluster-wide compromise.

<Frame>
  <img alt="The image illustrates a security vulnerability in a Kubernetes cluster setup, highlighting an attack chain involving credential theft and secret extraction. It emphasizes the risk with the phrase &#x22;Why So Bad?&#x22; and details an attack chain on the right." />
</Frame>

## Immediate containment (short-term actions)

> **warning** If you suspect a pod is compromised: cordon the node, isolate the workload, and avoid restarting containers on the same node until you investigate. Collect forensic artifacts (logs, filesystem snapshots) before making further changes.

## How to fix this without causing an outage

Follow a cautious, staged approach: discover what the workload truly needs, reduce scope, harden the pod, and then roll out cluster-wide guardrails in audit mode first.

1. Figure out what the workload actually needs

* Many workloads do not need the entire host filesystem; they may only require a specific directory such as `/var/log`. Confirm requirements with the workload owner.
* Some components legitimately need broader access (e.g., CSI drivers or certain system agents). Coordinate with owners before making changes.

<Frame>
  <img alt="The image shows a slide with the heading &#x22;Fix it w/o Outage,&#x22; discussing the needs of a pod, with options for a &#x22;Log Collector&#x22; and &#x22;CSI Driver&#x22; related to access requirements." />
</Frame>

2. Reduce scope and apply a restrictive securityContext

* Replace `hostPath: /` with a single specific path the app needs.
* Mark mounts `readOnly: true` when possible.
* Disable `privileged` and set `allowPrivilegeEscalation: false`.
* Run the container as a non-root user (`runAsNonRoot: true`).
* Use `seccompProfile: RuntimeDefault`.
* Drop all capabilities and only add the minimal set required (for example, `NET_BIND_SERVICE` if binding to ports \< 1024).
* Set `readOnlyRootFilesystem: true` if supported.

Example container spec snippet:

```yaml theme={null}
spec:
  containers:
  - name: app
    image: your-image:tag
    volumeMounts:
    - mountPath: /var/log
      readOnly: true
    securityContext:
      privileged: false
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      seccompProfile:
        type: RuntimeDefault
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
      readOnlyRootFilesystem: true
```

3. Enforce cluster-wide controls (carefully)

* Start with Pod Security Admission (PSA) and apply the `restricted` profile for namespaces that don’t need exceptions.
* For fine-grained policies use OPA Gatekeeper or Kyverno to:
  * Block `hostPath` mounts targeting root (`/`).
  * Block privileged containers.
  * Block pods running as UID 0 (root).
  * Deny access to container runtime sockets from user workloads.
* Run policies in audit (log-only) mode for at least a week to detect false positives and understand legitimate exceptions. Remediate those exceptions with workload owners before switching to enforce mode.

> **lightbulb** Run new policies in audit mode first. Monitor violations, remediate legitimate cases, and only then move to enforce to avoid unexpected outages.

## Quick remediation checklist

| Action                          |                       Why it matters | Example / Notes                                              |
| ------------------------------- | -----------------------------------: | ------------------------------------------------------------ |
| Narrow hostPath mounts          |    Reduces filesystem attack surface | Mount only `\`/var/log\``instead of`/\`                      |
| Make mounts read-only           |     Prevents tampering of host files | use `readOnly: true` in `volumeMounts`                       |
| Harden securityContext          |         Prevent privilege escalation | `privileged: false`, `runAsNonRoot: true`                    |
| Use seccomp & drop capabilities |     Limits syscalls and capabilities | `seccompProfile: RuntimeDefault`, `capabilities.drop: [ALL]` |
| Enforce policies audit-first    |           Avoids breaking production | PSA/OPA/Gyverno in audit mode for 7+ days                    |
| Coordinate with owners          | Avoid outages and undocumented needs | Schedule changes with app teams                              |

## SecurityContext recommended fields

| Field                      | Recommended setting                           |
| -------------------------- | --------------------------------------------- |
| `privileged`               | `false`                                       |
| `runAsNonRoot`             | `true`                                        |
| `allowPrivilegeEscalation` | `false`                                       |
| `seccompProfile.type`      | `RuntimeDefault`                              |
| `capabilities.drop`        | `["ALL"]`                                     |
| `capabilities.add`         | `[]` or minimal (e.g. `["NET_BIND_SERVICE"]`) |
| `readOnlyRootFilesystem`   | `true` if supported by the app                |

## References and further reading

* [Kubernetes Pod Security Admission (PSA)](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
* [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
* [Kyverno](https://kyverno.io/)

Final takeaway: a privileged pod mounting the host filesystem is a node- (and often cluster-) level risk. The practical mitigation path is: discover real workload needs, narrow the `hostPath`, harden the pod `securityContext`, and deploy cluster policy guardrails in audit mode before enforcing.

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/60905e58-3a8e-4423-9743-081b4959f0a0/lesson/f7cfab9f-3d00-4882-8e36-16fc8dc5bdc5)
