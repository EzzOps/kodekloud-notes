# or list all namespaces that have pod-security labels
kubectl get namespace --show-labels | grep pod-security
```

You can also pin behavior to a specific API behavior version using `pod-security.kubernetes.io/enforce-version` (for example `v1.27`) or set it to `latest`. If omitted, the cluster default behavior is used.

<Frame>
  <img alt="The image is a guide for applying PSS namespace labels in Kubernetes, detailing label format with specific prefixes, modes, and levels." />
</Frame>

> **warning** Do not casually label core system namespaces (for example `kube-system`) as `restricted` or `baseline` unless you’ve validated operator and add-on compatibility. Mislabeling control-plane or infrastructure namespaces can break cluster components.

## PSS vs Gatekeeper / Kyverno

PSS provides a zero-install baseline covering critical pod-level security fields. It is intentionally limited in scope. For organization-specific constraints you should layer a policy engine.

* PSS: built-in, minimal setup, enforces core runtime controls.
* Gatekeeper / Kyverno: support complex, custom policies (for example, image registries, required labels, resource quotas, mutation, multi-field constraints).

Use PSS as the mandatory floor across all namespaces, then add Gatekeeper or Kyverno for additional operational policies.

<Frame>
  <img alt="The image is a comparison chart of PSS, Gatekeeper, and Kyverno, highlighting aspects such as installation, scope, granularity, mutation, and use cases. It suggests using PSS as a baseline with Gatekeeper or Kyverno for custom policies." />
</Frame>

## Summary / Key takeaways

* PSS levels: `privileged` (most permissive), `baseline` (recommended default), `restricted` (most restrictive).
* Enforcement modes per-namespace: `enforce` (block), `audit` (log), `warn` (inform). Stack modes so teams can migrate safely.
* PSS uses namespace labels only—no installation required. Use `kubectl label` to manage them and consider `enforce-version` when pinning behavior.
* For `restricted` compliance, important settings include running as non-root, disabling privilege escalation, minimizing capabilities, enforcing seccomp, and using a read-only root filesystem where feasible.
* Treat PSS as your baseline safety net and layer Gatekeeper or Kyverno for organization-specific policies.

<Frame>
  <img alt="The image outlines four key security takeaways related to pod security levels, modes, namespace label application, and settings for restricted pods." />
</Frame>

## Links and references

* [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
* [Kubernetes Namespace Labels for Pod Security](https://kubernetes.io/docs/concepts/security/pod-security-standards/#enforcement)
* [Gatekeeper (Open Policy Agent)](https://open-policy-agent.github.io/gatekeeper/)
* [Kyverno](https://kyverno.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/f777f6c0-ca36-4564-9abf-6ef8f548f02f)


# RBAC You Can Live With Least Privilege Without Pain

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/RBAC-You-Can-Live-With-Least-Privilege-Without-Pain/page

Using Kubernetes RBAC to enforce least privilege, explaining Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, authoring examples, scope decisions, and debugging permissions with kubectl auth can-i

Role-Based Access Control (RBAC) is the most fundamental security layer in Kubernetes. This guide makes RBAC practical: the four RBAC resources, how to write Roles, how to bind them to users and service accounts, and how to debug permissions using `kubectl auth can-i`.

<Frame>
  <img alt="The image outlines three learning objectives related to cluster-admin roles, RBAC resources, and writing Role and ClusterRole YAML configurations. The objectives are presented in a list format with colorful numbered labels." />
</Frame>

Why RBAC matters: a real-world anti-pattern

A SaaS team gave all 40 developers cluster-admin to avoid deployment delays. A junior dev accidentally ran:

```bash theme={null}
kubectl delete ns staging
```

with a kubeconfig pointed at production. The production `staging` namespace was deleted — 32 Deployments, 15 Services, 8 StatefulSets, and all PVCs. Because the PVCs had `reclaimPolicy: Delete`, data was lost permanently. The outage lasted six hours and cost significant revenue and recovery effort.

The root cause: everyone had cluster-admin. No separation of environments. No restrictions on destructive actions.

<Frame>
  <img alt="The image illustrates the &#x22;cluster-admin Anti-Pattern&#x22; with reasons such as everyone having cluster-admin rights, no restrictions on destructive actions, and no separation between environments." />
</Frame>

Kubernetes RBAC: the four resources

Kubernetes RBAC exposes exactly four API resources. Use namespace-scoped Roles first; only escalate to cluster scope when necessary.

| Resource             | Scope                                            | Purpose                                                                                                                            |
| -------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `Role`               | Namespace-scoped                                 | Define permissions within a single namespace.                                                                                      |
| `ClusterRole`        | Cluster-scoped (or for non-namespaced resources) | Define permissions across the cluster or for cluster-scoped resources (nodes, CRDs). Also reusable in namespace via `RoleBinding`. |
| `RoleBinding`        | Namespace-scoped                                 | Grant a `Role` or `ClusterRole` within one namespace to subjects.                                                                  |
| `ClusterRoleBinding` | Cluster-scoped                                   | Grant a `ClusterRole` cluster-wide to subjects.                                                                                    |

<Frame>
  <img alt="The image illustrates the four RBAC (Role-Based Access Control) resources in Kubernetes, detailing their scope and purpose: Role, ClusterRole, RoleBinding, and ClusterRoleBinding. It explains the permissions each grants within a namespace or cluster-wide." />
</Frame>

Practical rule: start namespace-scoped — `Role` + `RoleBinding`. Only go cluster-wide when you genuinely need cluster scope or access to non-namespaced resources.

Authoring a Role (example)

Create a read-only Role that permits listing pods and reading pod logs in the `payments` namespace:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: payments
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
```

Field notes:

* `apiGroups`: `""` (empty string) is the core API group (pods, services, configmaps). Other groups include `"apps"` (Deployments) and `"batch"` (Jobs).
* `resources`: resource types for the rule. Subresources like `pods/log` are valid.
* `verbs`: operations allowed. Read-only typically uses `get`, `list`, `watch`. Add `create`, `update`, `patch` for write, and `delete` for destructive actions. Avoid wildcard `*` unless absolutely necessary.
* `resourceNames` (optional): restricts the rule to specific named resources for precise permissions.

RoleBindings — who gets the Role?

A `RoleBinding` connects subjects (who) to a `Role` or `ClusterRole` (what). Examples:

Bind the `pod-reader` Role to user `alice` in `payments`:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods-payments
  namespace: payments
subjects:
- kind: User
  name: alice
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

Bind a cluster-scoped `ClusterRole` (e.g., `edit`) to a service account in a different namespace:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cicd-deployer
  namespace: payments
subjects:
- kind: ServiceAccount
  name: deploy-bot
  namespace: cicd
roleRef:
  kind: ClusterRole
  name: edit
  apiGroup: rbac.authorization.k8s.io
```

Common subject kinds:

* `User` — human identity from your ID provider.
* `Group` — group from your ID provider.
* `ServiceAccount` — Pod identities (`system:serviceaccount:<namespace>:<name>`).

When to choose namespace vs. cluster scope

| Scenario                                                     | Recommended Resources                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Developer needs to view pods in a namespace                  | `Role` + `RoleBinding` (namespace-scoped)                                 |
| CI/CD deploys to a single namespace (reusable rule)          | Create a `ClusterRole` and bind it to that namespace with a `RoleBinding` |
| Monitoring needs cluster-wide read access                    | `ClusterRole` + `ClusterRoleBinding`                                      |
| Platform team manages cluster-scoped resources (CRDs, nodes) | `ClusterRole` + `ClusterRoleBinding`                                      |
| Emergency/root access                                        | `cluster-admin` (avoid for day-to-day)                                    |

> **warning** Use `cluster-admin` only for emergency / break-glass scenarios. Day-to-day operations should use least-privilege, namespace-scoped roles wherever possible.

<Frame>
  <img alt="The image is a table comparing namespace vs. cluster scope decisions with scenarios, role types, and binding types. It describes different levels of access and binding types for developers, CI/CD, monitoring, and admin roles." />
</Frame>

Debugging RBAC with kubectl

`kubectl auth can-i` is the primary tool to test permissions. Common usage patterns:

* Can the current identity create Deployments in `payments`?

```bash theme={null}
