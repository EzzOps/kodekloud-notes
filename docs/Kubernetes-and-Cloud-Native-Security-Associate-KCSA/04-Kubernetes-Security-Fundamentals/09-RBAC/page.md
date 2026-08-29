# RBAC

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/RBAC/page

This tutorial explains managing permissions in Kubernetes using RBAC, covering roles, bindings, and permission verification.

In this tutorial, you’ll learn how to manage permissions in Kubernetes using RBAC. We’ll cover:

1. Defining a Role
2. Binding a Role to a User
3. Inspecting Roles and RoleBindings
4. Verifying Permissions with `kubectl auth can-i`
5. Restricting Access to Specific Resource Names

Along the way, you’ll see code examples, handy tables, and useful callouts to help reinforce best practices.

***

## 1. Defining a Role in a Namespace

A **Role** grants a set of permissions within a single namespace. Each Role rule comprises:

| Field           | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| apiGroups       | API group of the resource (empty string `""` for core group) |
| resources       | Kubernetes resources (e.g., `pods`, `configmaps`)            |
| verbs           | Allowed actions (e.g., `get`, `list`, `create`, `delete`)    |
| resourceNames\* | Restrict operations to specific resource names               |

\*Optional field to scope rules to named resources only.

Example: create a Role named **developer** that can manage Pods and create ConfigMaps.

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["list", "get", "create", "update", "delete"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["create"]
```

Save as `role-developer.yaml` and apply:

```bash theme={null}
kubectl apply -f role-developer.yaml
```

> **lightbulb** Roles are namespace-scoped by default. To apply this Role in another namespace, add `namespace: your-namespace` under `metadata:`.

***

## 2. Binding a Role to a User with RoleBinding

A **RoleBinding** associates one or more subjects (users, groups, or service accounts) with a Role.

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
  - kind: User
    name: dev-user
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

Save as `rolebinding-devuser.yaml` and run:

```bash theme={null}
kubectl apply -f rolebinding-devuser.yaml
```

> **triangle-alert** Ensure your Role and RoleBinding share the same namespace unless you intend to bind across namespaces.

***

## 3. Inspecting Roles and RoleBindings

Use `kubectl` to list or describe your RBAC resources:

* List all Roles in the current namespace
  ```bash theme={null}
  kubectl get roles
  ```

* List all RoleBindings in the current namespace
  ```bash theme={null}
  kubectl get rolebindings
  ```

* Describe a specific Role to view its rules
  ```bash theme={null}
  kubectl describe role developer
  ```
  Sample output:
  ```text theme={null}
  Name:         developer
  PolicyRule:
    Resources      Verbs
    ---------      -------------------------------
    pods           [get list create update delete]
    configmaps     [create]
  ```

* Describe a RoleBinding to see bound subjects
  ```bash theme={null}
  kubectl describe rolebinding devuser-developer-binding
  ```
  Sample output:
  ```text theme={null}
  Name:         devuser-developer-binding
  Role:
    Kind:  Role
    Name:  developer
  Subjects:
    Kind   Name
    ----   ----
    User   dev-user
  ```

***

## 4. Verifying Permissions with kubectl auth can-i

Check whether a user can perform specific actions:

```bash theme={null}
