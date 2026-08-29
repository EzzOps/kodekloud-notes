# flightticket-custom-definition.yml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: flighttickets.flights.com
spec:
  scope: Namespaced
  group: flights.com
  names:
    kind: FlightTicket
    singular: flightticket
    plural: flighttickets
    shortnames:
      - ft
  versions:
    - name: v1
      served: true
      storage: true
```

```go theme={null}
package flightticket

import (
    "k8s.io/api/apps/v1"
)

var controllerKind = v1.SchemeGroupVersion.WithKind("Flightticket")

// Run begins watching and syncing.
func (dc *FlightTicketController) Run(workers int, stopCh <-chan struct{}) {
    // Controller logic goes here.
}

// callBookFlightAPI initiates the flight booking process.
func (dc *FlightTicketController) callBookFlightAPI(obj interface{}) {
    // API call implementation.
}
```

```bash theme={null}
kubectl create -f flight-operator.yaml
```

The operator framework offers extensive automation capabilities beyond simple deployments. A notable real-world example is the etcd operator—which deploys and manages an etcd cluster within Kubernetes. It includes a CRD for defining the etcd cluster and a custom controller that continuously monitors etcd resources. This operator also simplifies advanced operations like backups and restores by enabling these actions with the creation of dedicated CRDs.

The diagram below visualizes an operator framework structure that includes CRDs and custom controllers such as EtcdCluster, EtcdBackup, EtcdRestore, ETCD Controller, and Backup Operator:

![The image illustrates an Operator Framework with Custom Resource Definitions (CRD) and Custom Controllers, including EtcdCluster, EtcdBackup, EtcdRestore, ETCD Controller, and Backup Operator.](https://kodekloud.com/kk-media/image/upload/v1752871289/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Operator-Framework/frame_80.jpg)

> **lightbulb** Operators simplify complex processes by bundling CRDs and controllers, making tasks like deployment, backup, and recovery more efficient. However, keep in mind that understanding CRDs remains essential, especially for certification exams.

Deploying an operator typically involves three main steps:

1. Installing the Operator Lifecycle Manager (OLM).
2. Installing the operator.
3. Verifying the installation.

For instance, to deploy the etcd operator, you might use the following commands:

```bash theme={null}
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.19.1/install.sh | bash -s v0.19.1
```

```bash theme={null}
kubectl create -f https://operatorhub.io/install/etcd.yaml
```

```bash theme={null}
kubectl get csv -n my-etcd
```

> **triangle-alert** While operators offer significant advantages in automating deployment and management tasks, ensure that you have a solid understanding of CRDs, as they are a core component of Kubernetes and a primary focus of the exam curriculum.

Thank you for reading, and stay tuned for the next lesson to further enhance your Kubernetes expertise.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/637f50cb-d931-4f42-a4c7-c099bce4ac3a)


# Role Based Access Controls

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Role-Based-Access-Controls/page

This article explains how to create and manage Role-Based Access Control in Kubernetes, including roles, role bindings, and verifying user permissions.

In this lesson, we dive into Kubernetes Role-Based Access Control (RBAC), providing step-by-step instructions on how to create and manage roles and role bindings within a namespace. You'll learn how to define specific permissions for users, bind these permissions to users, and verify their access using kubectl commands.

## Creating a Role

To start, you need to define a Role object. Create a YAML file (e.g., developer-role.yaml) and set the API version to `rbac.authorization.k8s.io/v1` and the kind to `Role`. In this example, we define a role named "developer" with permissions that allow developers to manage pods and create configmaps. Each permission rule contains three key sections: API groups, resources, and verbs. For resources in the core API group, leave the API group field blank.

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

Create the role using the following command:

```bash theme={null}
kubectl create -f developer-role.yaml
```

> **lightbulb** Remember that roles in Kubernetes are namespace-specific. Ensure the YAML definition targets the correct namespace if needed.

## Binding a User to the Role

Once the role is defined, you need to link a user to this role by creating a RoleBinding. A RoleBinding associates a user with the specified role within a given namespace. In this example, we'll create a role binding named `devuser-developer-binding` that assigns the "developer" role to the user `dev-user` in the default namespace.

Below is the YAML definition for the role binding (e.g., devuser-developer-binding.yaml):

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

Create the role binding with the command:

```bash theme={null}
kubectl create -f devuser-developer-binding.yaml
```

## Verifying Roles and Role Bindings

After creating the role and role binding, you can verify them using the following kubectl commands:

* To list roles:

  ```bash theme={null}
  kubectl get roles
  ```

  Example output:

  ```text theme={null}
  NAME         AGE
  developer    4s
  ```

* To list role bindings:

  ```bash theme={null}
  kubectl get rolebindings
  ```

  Example output:

  ```text theme={null}
  NAME                        AGE
  devuser-developer-binding   24s
  ```

To get detailed information about the role, run:

```bash theme={null}
kubectl describe role developer
```

Sample output:

```text theme={null}
Name:         developer
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources      Non-Resource URLs  Resource Names  Verbs
  --------       ------------------  ---------------  ----
  configmaps    []                  []               [create]
  pods          []                  []               [get watch list create delete]
```

Similarly, to examine the role binding details, use:

```bash theme={null}
kubectl describe rolebinding devuser-developer-binding
```

Expected output:

```text theme={null}
Name:                   devuser-developer-binding
Labels:                 <none>
Annotations:            <none>
Role:
  Kind:                Role
  Name:                developer
Subjects:
  Kind   Name       Namespace
  ----   ----       ---------
  User   dev-user
```

## Testing Access Permissions

You can test whether a user has access to specific Kubernetes resources using the `kubectl auth can-i` command:

```bash theme={null}
kubectl auth can-i create deployments
```

Expected output:

```text theme={null}
yes
```

And if you test deleting nodes:

```bash theme={null}
kubectl auth can-i delete nodes
```

Expected output:

```text theme={null}
no
```

If you need to simulate actions as another user, use the `--as` flag. Even though the developer role does not have permission to create deployments, it can create pods:

```bash theme={null}
kubectl auth can-i create deployments --as dev-user
```

Expected output:

```text theme={null}
no
```

```bash theme={null}
kubectl auth can-i create pods --as dev-user
```

Expected output:

```text theme={null}
yes
```

You can also specify a particular namespace using the `--namespace` flag if the permissions are scoped accordingly.

## Granting Access to Specific Resources

In some cases, you might want to restrict a user's permissions to specific resources. For instance, if you need to allow a user to manage only two pods named "blue" and "orange" within a namespace, refine the role rule by including the `resourceNames` field:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "create", "update"]
  resourceNames: ["blue", "orange"]
```

> **triangle-alert** Be cautious when specifying resource names. Only include the exact resources you intend to allow access to, as this will restrict access to other resources of the same type.

## Conclusion

This lesson has demonstrated how to set up and manage RBAC in Kubernetes. By creating roles and role bindings, you can control user permissions precisely within a namespace. For further practice, refer to Kubernetes' official documentation and experiment with real RBAC configurations in your environment.

For additional resources, consider these links:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes RBAC Concepts](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

Happy coding and secure your Kubernetes clusters with effective RBAC management!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/585c7ebe-dfca-4838-8150-e3eabf711941)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/3e098e78-e040-4af7-babd-e21a95eb668f)
