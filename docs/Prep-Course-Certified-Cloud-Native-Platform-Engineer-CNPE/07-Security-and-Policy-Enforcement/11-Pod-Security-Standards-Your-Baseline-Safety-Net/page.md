# Pod Security Standards Your Baseline Safety Net

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Pod-Security-Standards-Your-Baseline-Safety-Net/page

Explains Kubernetes Pod Security Standards, the three profiles, enforcement modes, and namespace label configuration to enforce baseline runtime protections and layer custom policies.

Pod Security Standards (PSS) are Kubernetes' built‑in mechanism for restricting what Pods may do at runtime. PSS enforces a baseline safety net directly in the API server—no installation required—making it a lightweight, reliable first line of defense. It replaces the deprecated PodSecurityPolicy removed in Kubernetes 1.25.

In this article you'll learn the three PSS levels, how enforcement modes are applied and combined, and how to enable PSS using only namespace labels.

<Frame>
  <img alt="The image lists learning objectives related to Pod Security, including understanding security levels, applying enforcement modes, configuring security with namespace labels, and implementing security settings for compliance." />
</Frame>

## The three security levels

PSS defines three named profiles that express increasing restrictions. Use them to scope what pod configurations are allowed in a namespace.

* Privileged — no restrictions. Pods may use host network, hostPID, privileged containers, run as root, etc. Reserve this for cluster infrastructure namespaces (for example `kube-system`), CNI plugins, or monitoring agents that genuinely require host access.

<Frame>
  <img alt="The image outlines the first of three security levels, labeled &#x22;Privileged.&#x22; It describes the level as having maximum risk with no restrictions, allowing pods extensive actions such as running as root and accessing the host network." />
</Frame>

* Baseline — the recommended default for most application namespaces. Baseline blocks dangerous host-level privileges (for example, `hostNetwork`, `hostPID`, `privileged` containers) while remaining compatible with typical containerized applications.

<Frame>
  <img alt="The image depicts a diagram of three security levels: Privileged, Baseline, and another unspecified level, with a focus on the Baseline level, which describes its moderate risk and security features for typical web apps and microservices." />
</Frame>

* Restricted — the strictest profile. Restricted includes Baseline restrictions and additionally requires pods to run as non-root users, disables privilege escalation, limits Linux capabilities, and encourages read-only root filesystems and selinux/seccomp profiles where appropriate. Use Restricted for sensitive workloads that must satisfy strong runtime controls.

<Frame>
  <img alt="The image shows a diagram of three security levels labeled as Privileged, Baseline, and Restricted, with details under Restricted about minimizing risk and maximizing security." />
</Frame>

Key guidance: use `baseline` as your default for application namespaces, `restricted` for high‑security workloads, and `privileged` only where host access is required.

| Level      | Summary                                                       | Use case                                                       |
| ---------- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| Privileged | No runtime restrictions; highest risk                         | Cluster infra (CNI, monitoring agents), kube-system components |
| Baseline   | Blocks host-level privileges; compatible with most apps       | Default application namespaces                                 |
| Restricted | Enforces non-root, minimal capabilities, seccomp/read-only fs | Sensitive workloads, compliance zones                          |

<Frame>
  <img alt="The image is a table showing the configurations blocked at each security level (Privileged, Baseline, Restricted) for pod specifications, such as privileged containers, host networking, and running as root." />
</Frame>

Memorize the distinction: Baseline prevents dangerous host access; Restricted additionally locks down the container runtime and user/privileges.

## Enforcement modes — how to apply the levels

PSS supports three independent enforcement modes that you can set per namespace. Best practice is to stack modes so teams can iterate toward stricter profiles without breaking running workloads.

* `enforce` — hard blocker. Pods that violate the specified level are rejected during admission.
* `audit` — log only. Violations are recorded in audit logs but pods are allowed.
* `warn` — user-visible warning. Pods are allowed, but API responses include a warning message.

| Mode      | Effect                            | Typical usage                                |
| --------- | --------------------------------- | -------------------------------------------- |
| `enforce` | Rejects non-compliant pods        | Apply to `baseline` for app namespaces       |
| `audit`   | Records violations in audit logs  | Monitor `restricted` impact before enforcing |
| `warn`    | Returns warnings in API responses | Educate developers about upcoming changes    |

A common pattern: enforce `baseline` to immediately block host-level risks, and use `audit`/`warn` for `restricted` so teams can remediate before you enable enforcement.

<Frame>
  <img alt="The image illustrates three enforcement modes: &#x22;Enforce&#x22; (hard block), &#x22;Warn&#x22; (visible warning), and &#x22;Audit&#x22; (silent logging), for handling pod violations. Each mode is depicted with a brief description of its function." />
</Frame>

<Callout icon="lightbulb">
  Recommended practice: Enforce `baseline` for all application namespaces. Use `audit`/`warn` at `restricted` to surface work needed to move workloads to the stricter profile without breaking them.
</Callout>

## Applying Pod Security Standards with namespace labels

PSS is label-driven: no CRDs, no external admission controllers required. You apply levels and modes by labeling namespaces with the `pod-security.kubernetes.io/*` keys.

Example labels:

```yaml theme={null}
pod-security.kubernetes.io/enforce: baseline   # blocks pods that violate baseline
pod-security.kubernetes.io/audit: restricted   # logs restricted violations
pod-security.kubernetes.io/warn: restricted    # warns about restricted violations
```

To set these labels, use `kubectl label`. Example — apply `restricted` for `enforce` and `warn` on the `payments` namespace:

```bash theme={null}
kubectl label namespace payments \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/warn=restricted
```

Verify labels:

```bash theme={null}
kubectl get namespace payments --show-labels
