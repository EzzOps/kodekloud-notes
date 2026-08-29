# Output: statefulset.apps/mysql scaled
```

When scaling down, Kubernetes terminates the Pods in reverse order: the last Pod is removed first, followed by earlier ones. Likewise, when deleting the StatefulSet, Pods are terminated in reverse order.

## Customizing Pod Deployment Strategy

By default, StatefulSets follow an ordered approach for both deployment and termination. However, you can override this behavior by setting the `podManagementPolicy` to `Parallel`. This instructs Kubernetes to deploy and terminate all Pods simultaneously while still providing them with stable network identities.

Below is an example StatefulSet configuration that uses the `Parallel` pod management policy:

```yaml theme={null}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  serviceName: mysql-h
  podManagementPolicy: Parallel
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql
```

You can manage this StatefulSet with the following commands:

```bash theme={null}
kubectl create -f statefulset-definition.yml
kubectl scale statefulset mysql --replicas=5
kubectl scale statefulset mysql --replicas=3
kubectl delete statefulset mysql
# Output: statefulset.apps/mysql deleted
```

This configuration allows Pods to be launched or terminated in parallel, which can be advantageous when the order of operations is not a strict requirement for your application.

<Callout icon="lightbulb">
  While the `Parallel` management policy offers faster scaling, it does so at the cost of ordered deployment. Choose the appropriate policy based on your application's initialization and shutdown needs.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/cb16c9a3-1608-48cf-bfd5-2465f64b4f93/lesson/c80a8c28-80bf-4f79-8d4a-0368caf88f2b" />
</CardGroup>


# Storage Classes

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/State-Persistence/Storage-Classes/page

This guide explores Kubernetes storage classes for managing dynamic storage provisioning, covering static and dynamic provisioning methods with examples.

In this guide, we'll dive into storage classes in Kubernetes, a vital concept for managing dynamic storage provisioning. Earlier, we covered the creation of Persistent Volumes (PVs), Persistent Volume Claims (PVCs), and their integration within pod definitions. With static provisioning, you manually create and manage disks along with their corresponding PV definitions before deploying an application.

Below is an example of static provisioning using Google Cloud Persistent Disk:

```yaml theme={null}
