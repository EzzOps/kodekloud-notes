# Role Based Access Controls

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Security/Role-Based-Access-Controls/page

This article explains how to implement Role-Based Access Controls in Kubernetes, including creating roles, role bindings, and verifying permissions.

In this lesson, we dive into Kubernetes Role-Based Access Controls (RBAC) to help you manage permissions effectively. You'll learn how to create roles, bind them to users, and verify permissions within a namespace.

## Creating a Role

To define a role, create a YAML file that sets the API version to `rbac.authorization.k8s.io/v1` and the kind to `Role`. In this example, we create a role named **developer** to grant developers specific permissions. The role includes a list of rules where each rule specifies the API groups, resources, and allowed verbs. For resources in the core API group, provide an empty string (`""`) for the `apiGroups` field.

For instance, the following YAML definition grants developers permissions on pods (with various actions) and allows them to create ConfigMaps:

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
  resources: ["ConfigMap"]
  verbs: ["create"]
```

Create the role by running:

```bash theme={null}
kubectl create -f developer-role.yaml
```

<Callout icon="lightbulb">
  Both roles and role bindings are namespace-scoped. This example assumes usage within the default namespace. To manage access in a different namespace, update the YAML metadata accordingly.
</Callout>

## Creating a Role Binding

After defining a role, you need to bind it to a user. A role binding links a user to a role within a specific namespace. In this example, we create a role binding named **devuser-developer-binding** that grants the user `dev-user` the **developer** role.

Below is the combined YAML definition for both creating the role and its corresponding binding:

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
  resources: ["ConfigMap"]
  verbs: ["create"]
---
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

Create the role binding using the command:

```bash theme={null}
kubectl create -f devuser-developer-binding.yaml
```

## Verifying Roles and Role Bindings

After applying your configurations, it's important to verify that the roles and role bindings have been created correctly.

To list all roles in the current namespace, execute:

```bash theme={null}
kubectl get roles
```

Example output:

```bash theme={null}
NAME        AGE
developer   4s
```

Next, list all role bindings:

```bash theme={null}
kubectl get rolebindings
```

Example output:

```bash theme={null}
NAME                      AGE
devuser-developer-binding 24s
```

For detailed information about the **developer** role, run:

```bash theme={null}
kubectl describe role developer
```

Sample output:

```bash theme={null}
Name:         developer
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources           Non-Resource URLs   Resource Names   Verbs
  -----------         ------------------   --------------   ----
  ConfigMap           []                   []               [create]
  pods                []                   []               [get watch list create delete]
```

To view the specifics of the role binding:

```bash theme={null}
kubectl describe rolebinding devuser-developer-binding
```

Example output:

```bash theme={null}
Name:         devuser-developer-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:    Role
  Name:    developer
Subjects:
  Kind     Name      Namespace
  ----     ----      ---------
  User     dev-user
```

## Testing Permissions with kubectl auth

You can test whether you have the necessary permissions to perform specific actions by using the `kubectl auth can-i` command. For example, to check if you can create deployments, run:

```bash theme={null}
kubectl auth can-i create deployments
```

This command might return:

```bash theme={null}
yes
```

Similarly, to verify if you can delete nodes:

```bash theme={null}
kubectl auth can-i delete nodes
```

Expected output:

```bash theme={null}
no
```

To test permissions for a specific user without switching user contexts, use the `--as` flag. Although the **developer** role does not permit creating deployments, it does allow creating pods:

```bash theme={null}
kubectl auth can-i create deployments
