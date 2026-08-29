# List namespaces
kubectl get namespaces

# Example output
# NAME              STATUS   AGE
# default           Active   18h
# kube-flannel      Active   18h
# kube-node-lease   Active   18h
# kube-public       Active   18h
# kube-system       Active   18h
# team-alpha        Active   5m
# List service accounts in each team namespace
kubectl get sa -n team-alpha
kubectl get sa -n team-beta

# Example output
# team-alpha:
# NAME         AGE
# default      6m
# deploy-bot   6m
#
# team-beta:
# NAME         AGE
# default      6m
# readonly-sa  6m
```

## Developer Role (namespaced)

This Role grants CRUD + watch/list/get permissions for several common resources in the `team-alpha` namespace. It's scoped to the namespace so it won't affect other teams.

```yaml theme={null}
# developer-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: team-alpha
rules:
- apiGroups: [""]            # core API group
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]       # apps API group
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

Apply the Role, then create a RoleBinding that grants this Role to a user named `alice` in the `team-alpha` namespace:

```bash theme={null}
# Apply the Role manifest
kubectl apply -f developer-role.yaml
# Expected output:
# Bind the role to a user 'alice' in the team-alpha namespace
kubectl create rolebinding alice-developer --role=developer --user=alice -n team-alpha
# Expected output:
# rolebinding.rbac.authorization.k8s.io/alice-developer created
```

Test Alice's permissions using `kubectl auth can-i` with impersonation via `--as`:

```bash theme={null}
# Impersonate alice and ask if she can create pods in team-alpha
kubectl auth can-i create pods --namespace=team-alpha --as=alice
# The same check in team-beta should be denied (no binding exists there)
kubectl auth can-i create pods --namespace=team-beta --as=alice
# Expected output: no
```

This enforces least privilege: Alice can create resources only in the namespace where the RoleBinding exists.

## Cluster-wide Viewer Role (ClusterRole)

To provide read-only access across the entire cluster use a ClusterRole and ClusterRoleBinding. The following ClusterRole allows `get`, `list`, and `watch` for common cluster resources:

```yaml theme={null}
# viewer-clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: viewer
rules:
- apiGroups: [""]                 # core API group
  resources: ["pods", "services", "namespaces", "configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]             # apps API group
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch"]
```

Apply and bind cluster-wide to a user `bob`:

```bash theme={null}
kubectl apply -f viewer-clusterrole.yaml
# Expected output:
kubectl create clusterrolebinding bob-viewer --clusterrole=viewer --user=bob
# Expected output:
# clusterrolebinding.rbac.authorization.k8s.io/bob-viewer created
```

Verify Bob's permissions (impersonating Bob):

```bash theme={null}
# Bob can list pods in both team-alpha and team-beta because viewer is cluster-scoped
kubectl auth can-i list pods --as=bob -n team-alpha
kubectl auth can-i list pods --as=bob -n team-beta
# But Bob cannot create pods because viewer is read-only
kubectl auth can-i create pods --as=bob -n team-beta
# Expected output: no
```

## Binding Roles to Service Accounts

Service accounts are identities used by automation, controllers, and CI/CD systems. Bind Roles to service accounts using the `--serviceaccount` flag; the format is `namespace:serviceaccount-name`.

> **lightbulb** When impersonating a service account with `kubectl auth can-i`, use the username format:
  `system:serviceaccount:<namespace>:<serviceaccount-name>` — for example:
  `system:serviceaccount:team-alpha:deploy-bot`.

Bind the `developer` Role to the `deploy-bot` service account in `team-alpha`:

```bash theme={null}
kubectl create rolebinding deploy-bot-developer \
  --role=developer \
  --serviceaccount=team-alpha:deploy-bot \
  -n team-alpha
# Expected output:
# rolebinding.rbac.authorization.k8s.io/deploy-bot-developer created
```

Test the permissions as that service account:

```bash theme={null}
# Can the deploy-bot create deployments in team-alpha?
kubectl auth can-i create deployments \
  --as=system:serviceaccount:team-alpha:deploy-bot \
  -n team-alpha
# The readonly service account in team-beta should not be able to get pods (no binding).
kubectl auth can-i get pods \
  --as=system:serviceaccount:team-beta:readonly-sa \
  -n team-beta
# Expected output: no
```

## Default deny and RBAC debugging

Kubernetes RBAC is deny-by-default. If no binding grants a permission, it is denied — you do not need explicit deny rules.

To debug RBAC:

* Use `kubectl auth can-i` to check whether an identity can perform an action.
* Use `--as` to impersonate users or service accounts.
* For deeper debugging, increase verbosity on API calls (e.g., `kubectl --v=8`) or inspect Role/ClusterRole and RoleBinding/ClusterRoleBinding objects.

> **warning** Always review Role and ClusterRole changes carefully. Test with `kubectl auth can-i --as=...` before applying changes to production to avoid accidentally granting too much access.

## Quick comparison

| Resource Type      | Scope          | Use case                                                   | Creation command example                        |
| ------------------ | -------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| Role               | Namespaced     | Grant permissions within a single namespace                | `kubectl apply -f developer-role.yaml`          |
| RoleBinding        | Namespaced     | Attach a namespaced Role to a user/serviceaccount          | `kubectl create rolebinding ... -n <namespace>` |
| ClusterRole        | Cluster-scoped | Define cluster-wide or API-group scoped permissions        | `kubectl apply -f viewer-clusterrole.yaml`      |
| ClusterRoleBinding | Cluster-scoped | Attach a ClusterRole to a user/serviceaccount cluster-wide | `kubectl create clusterrolebinding ...`         |

## Summary / Best practices

* Roles and RoleBindings are namespaced; ClusterRoles and ClusterRoleBindings are cluster-scoped.
* Prefer namespaced Roles when access only needs to be limited to a team or project.
* Use `kubectl auth can-i` with `--as` to test permissions for users and service accounts before and after changes.
* Follow the principle of least privilege: grant only the permissions required.
* Remember: by default, Kubernetes denies actions that aren't explicitly granted.

## Links and references

* [Kubernetes RBAC docs](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [kubectl auth can-i documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#auth)
* [Managing Service Accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)

Practice these principles in a safe lab environment by creating Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings and validating access with `kubectl auth can-i`.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/cfeb58dd-916f-46fd-805a-ff58b8242fcc)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/cfac0a94-3720-4891-9aac-3f80c4454333)


# Demo Supply Chain Guardrails with Kyverno

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Demo-Supply-Chain-Guardrails-with-Kyverno/page

Guide showing how to use Kyverno to validate, mutate, and generate Kubernetes resources for supply chain guardrails, with examples and Audit mode PolicyReports

[OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/) is a powerful policy engine, but it requires learning the Rego language. Kyverno offers an alternative: policies are written as Kubernetes-native YAML, so you can author validate, mutate, and generate rules without learning a new language.

This guide verifies Kyverno is running and demonstrates three common policy patterns:

* validate — allow or deny resources
* mutate — automatically modify resources
* generate — create resources in response to events

You’ll also learn how to use Audit mode and PolicyReports to safely roll out policies.

## At a glance — Kyverno rule types

| Rule Type | Purpose                                   | Typical Use Case                                    |
| --------- | ----------------------------------------- | --------------------------------------------------- |
| validate  | Allow or deny resources based on patterns | Enforce approved image registries, required labels  |
| mutate    | Modify resources at admission             | Inject labels, set default resource requests/limits |
| generate  | Create resources in response to events    | Auto-create NetworkPolicy, ConfigMap, RoleBindings  |

Quick links:

* Kyverno docs: [https://kyverno.io](https://kyverno.io)
* Kyverno policy examples: [https://kyverno.io/docs/writing-policies/](https://kyverno.io/docs/writing-policies/)
* OPA / Rego reference: [https://www.openpolicyagent.org/docs/latest/policy-language/](https://www.openpolicyagent.org/docs/latest/policy-language/)

## Prerequisites

* A running Kubernetes cluster with Kyverno installed in the `kyverno` namespace.
* `kubectl` configured for the target cluster.

## Verify Kyverno is running

Check Kyverno pods in the `kyverno` namespace:

```bash theme={null}
kubectl get pods -n kyverno
```

Example output:

```text theme={null}
NAME                                              READY   STATUS    RESTARTS   AGE
kyverno-admission-controller-659d58644b-8jbfb     1/1     Running   0          115m
kyverno-background-controller-778fbf669-cw58      1/1     Running   0          115m
kyverno-cleanup-controller-8c8f4578-cmbj          1/1     Running   0          115m
kyverno-reports-controller-6c666d96-7xgz7         1/1     Running   0          115m
```

If any Kyverno pods are not `Running`, check pod logs and events to diagnose installation issues.

## 1) Validate rule example — restrict image registries

This example enforces that Pod container images must come from `docker.io`. The policy uses Kyverno YAML pattern overlays — no Rego required.

File: `validate-registry.yaml`

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-registries
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Image must be from docker.io"
        pattern:
          spec:
            containers:
              - image: "docker.io/*"
```

Notes:

* `validationFailureAction: Enforce` blocks requests that violate the policy. Switch to `Audit` to only record violations while allowing creation.
* Kyverno uses YAML pattern overlays so policies are readable and Kubernetes-native.

Apply the policy:

```bash theme={null}
kubectl apply -f validate-registry.yaml
