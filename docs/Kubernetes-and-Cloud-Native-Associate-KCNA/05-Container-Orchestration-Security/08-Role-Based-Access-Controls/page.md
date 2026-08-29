# Role Based Access Controls

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Container-Orchestration-Security/Role-Based-Access-Controls/page

This guide explores Role-Based Access Controls in Kubernetes, focusing on creating and managing roles and role bindings for resource access management.

In this guide, we explore Role-Based Access Controls (RBAC) in Kubernetes, including how to create and manage roles and role bindings effectively. RBAC provides a robust mechanism for managing access to resources within a Kubernetes cluster.

## Creating a Role

A Role in Kubernetes encapsulates a set of permissions for resources within a namespace. To create a role, define a role object in a YAML file with the following essential components:

* Set the API version to `rbac.authorization.k8s.io/v1`
* Specify the `kind` as `Role`
* Provide a metadata name (for example, "developer")
* List the rules that define the API groups, resources, and permitted verbs (actions)

For resources within the core group, leave the API groups field blank. For resources in other groups, specify the group name explicitly.

Below is an example YAML configuration that creates a "developer" role. This role allows actions such as listing, getting, creating, updating, and deleting pods, and includes an extra rule to create ConfigMaps:

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

Create the role using the following command:

```bash theme={null}
kubectl create -f <role-definition.yaml>
```

> **lightbulb** Both roles and role bindings in Kubernetes are namespace-scoped. In this example, the `developer` role applies only to the default namespace. To apply a role in another namespace, add the `namespace` field within the metadata section of your YAML file.

## Creating a Role Binding

After defining a role, bind it to a specific user using a RoleBinding. A role binding connects a user to a role within a namespace, thereby granting the user the permissions defined in that role.

Below is an example YAML configuration that creates a role binding named "devuser-developer-binding". This binding assigns the "developer" role to the user `dev-user`:

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

Create the role binding using the command:

```bash theme={null}
kubectl create -f <rolebinding-definition.yaml>
```

## Viewing and Verifying Roles and Bindings

### Listing Roles and Role Bindings

You can verify that your roles and role bindings have been created correctly using the `kubectl` commands below:

```bash theme={null}
kubectl get roles
```

This command outputs a list of roles, for example:

```text theme={null}
NAME       AGE
developer  4s
```

Similarly, list the role bindings:

```bash theme={null}
kubectl get rolebindings
```

Output example:

```text theme={null}
NAME                        AGE
devuser-developer-binding   24s
```

### Describing Specific Resources

To get detailed information about a specific role, use:

```bash theme={null}
kubectl describe role developer
```

Example output:

```text theme={null}
Name:               developer
Labels:             <none>
Annotations:        <none>
PolicyRule:
  Resources      Non-Resource URLs  Resource Names  Verbs
  ---------      ------------------  --------------  -----
  ConfigMap      []                  []              [create]
  pods           []                  []              [get watch list create delete]
```

Similarly, for a detailed view of a role binding, run:

```bash theme={null}
kubectl describe rolebinding devuser-developer-binding
```

Example output:

```text theme={null}
Name:                devuser-developer-binding
Labels:              <none>
Annotations:         <none>
Role:
  Kind:       Role
  Name:       developer
Subjects:
  Kind    Name      Namespace
  ----    ----      ---------
  User    dev-user
```

## Verifying User Permissions

Use the `kubectl auth can-i` command to verify if a user has permission to perform a specific action on a resource. For instance, to check if you can create deployments or delete nodes, execute:

```bash theme={null}
kubectl auth can-i create deployments
kubectl auth can-i delete nodes
