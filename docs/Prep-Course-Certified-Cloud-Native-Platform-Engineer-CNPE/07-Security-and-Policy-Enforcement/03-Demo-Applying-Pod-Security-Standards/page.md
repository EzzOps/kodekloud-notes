# Demo Applying Pod Security Standards

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Demo-Applying-Pod-Security-Standards/page

Explains using Kubernetes Pod Security Standards to enforce baseline restricted and privileged profiles via namespace labels and modes warn audit enforce, with examples and remediation steps.

[Gatekeeper](https://open-policy-agent.github.io/gatekeeper/) and [Kyverno](https://kyverno.io/) are powerful admission controllers, but both require installing extra tooling. Pod Security Standards (PSS) are built into Kubernetes and let cluster administrators enforce security baselines at the namespace level without deploying operators or CRDs.

PSS provides three predefined profiles and three enforcement modes. Use PSS when you want a simple, auditable, label-driven way to validate or block Pod specs at admission time.

## Pod Security profiles and modes

| Profile    |                                                                                Purpose | Typical use                                          |
| ---------- | -------------------------------------------------------------------------------------: | ---------------------------------------------------- |
| privileged |                                    Essentially "anything goes" — minimal restrictions. | System and infra workloads that require host access. |
| baseline   | Blocks the most dangerous privilege escalations while minimizing application breakage. | General-purpose application workloads.               |
| restricted |                                             Hardened, follows security best practices. | Sensitive workloads, strict compliance environments. |

| Mode      | Behavior                                              |
| --------- | ----------------------------------------------------- |
| `enforce` | Blocks creations/updates that violate the profile.    |
| `audit`   | Records violations to audit logs (doesn't block).     |
| `warn`    | Prints admission-time warnings but allows the object. |

<Frame>
  <img alt="The image shows a webpage from the Kubernetes documentation discussing Pod Security Standards. It outlines different policy levels: Privileged, Baseline, and Restricted, with a navigation sidebar on the left." />
</Frame>

You can review the exact checks and rationale for each profile in the [Kubernetes Pod Security Standards documentation](https://kubernetes.io/docs/concepts/security/pod-security-standards/).

<Frame>
  <img alt="The image shows a webpage from the Kubernetes documentation discussing baseline security policies for containerized workloads, with a focus on managing Windows Pods and HostProcess configurations." />
</Frame>

<Callout icon="lightbulb">
  Pod Security Standards are label-driven: a namespace's enforcement behavior is determined solely by labels on that namespace (for example `pod-security.kubernetes.io/enforce=baseline`). Labels make policy auditable and easily reversible.
</Callout>

<Callout icon="warning">
  Applying or changing PSS labels requires permission to modify namespaces (typically cluster-admin). Test changes in a non-production cluster or dedicated namespaces before rolling higher-level enforcement.
</Callout>

## Typical workflow

The common progression is:

* Inspect namespaces and labels.
* Label a namespace with PSS modes (`warn`/`audit` first to surface issues).
* Attempt non-compliant workloads to capture warnings/audit entries.
* Fix workloads to meet the profile.
* Switch to `enforce` when ready to block non-compliant Pods.

Follow the steps below.

1. Check current namespaces and labels

```bash theme={null}
kubectl get namespaces --show-labels
```

Example output (trimmed):

```bash theme={null}
NAME            STATUS   AGE   LABELS
default         Active   137m  kubernetes.io/metadata.name=default
kube-flannel    Active   137m  k8s-app=flannel,kubernetes.io/metadata.name=kube-flannel,pod-security.kubernetes.io/enforce=privileged
pss-baseline    Active   9m    kubernetes.io/metadata.name=pss-baseline
pss-privileged  Active   9m    kubernetes.io/metadata.name=pss-privileged
pss-restricted  Active   9m    kubernetes.io/metadata.name=pss-restricted
```

2. Label a namespace to enforce the `baseline` profile but also `audit`/`warn` the `restricted` profile so you can see what would fail under stricter rules:

```bash theme={null}
kubectl label namespace pss-baseline \
  pod-security.kubernetes.io/enforce=baseline \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
