# Updated deployment snippet for demo-c
spec:
  containers:
    - name: example-container
      image: ngheith/no-entry-point:v5
      command: ["sleep", "3600"]
      imagePullPolicy: IfNotPresent
```

After applying this change, checking the pod statuses should reveal that the container runs without errors:

```plaintext theme={null}
NAME                                     PF   READY  STATUS         RESTARTS  CPU   MEM   %CPU/R  %CPU/L  %MEM/R  %MEM/L  IP              NODE   AGE
demo-a-deployment-75bf694876-vcftr      ▢    1/1    Running        0         0     17    n/a     n/a     n/a       10.244.192.4    node01  8m25s
demo-b-deployment-9cbbbd944f-l2xsc      ▢    1/1    Running        0         0     0     n/a     n/a     n/a       10.244.192.23   node01  4m34s
demo-c-deployment-5f47f7f795c-ghkl4     ▢    0/1    Terminating    4         0     0     n/a     n/a     n/a       n/a              node01  10s
demo-c-deployment-86d746c6f9-sbss9      ▢    1/1    Running        0         0     0     n/a     n/a     n/a       10.244.192.24   node01  2s
```

## Final Status Summary

Below is a summary of the final pod status after troubleshooting all container creation steps:

```plaintext theme={null}
Context: kubernetes-admin@kubernetes
Cluster: kubernetes
User: kubernetes-admin
K9s Rev: v0.32.5
K8s Rev: v1.30.0
CPU: 0%
MEM: 1%

NAME                                     PF   READY   STATUS      RESTARTS   CPU   MEM   %CPU/R   %CPU/L   %MEM/R   %MEM/L   IP               NODE    AGE
demo-a-deployment-75bf694876-vctf       ●    1/1     Running     0          0     17    n/a      n/a      n/a      n/a      10.244.192.4    node01  8m45s
demo-b-deployment-9cbbdb94f-l2xsc       ●    1/1     Running     0          0     0     n/a      n/a      n/a      n/a      10.244.192.23   node01  4m54s
demo-c-deployment-86d746c6f9-sbss9      ●    1/1     Running     0          0     0     n/a      n/a      n/a      n/a      10.244.192.24   node01  22s
```

By understanding the container lifecycle and the specific error messages, you can more effectively narrow down troubleshooting efforts in Kubernetes environments.

For more detailed troubleshooting techniques, check out the [Kubernetes Documentation](https://kubernetes.io/docs/) and resources on [Container Runtime Troubleshooting](https://kubernetes.io/docs/tasks/debug/debugging-pod/).

<Frame>
  ![The image shows a terminal interface for managing Kubernetes pods using K9s, displaying two pods with errors: "CreateContainerConfigError" and "CreateContainerError."](https://kodekloud.com/kk-media/image/upload/v1752880430/notes-assets/images/Kubernetes-Troubleshooting-for-Application-Developers-Create-Container-Errors/k9s-kubernetes-pods-errors-terminal.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-troubleshooting-for-application-developers/module/143d3913-caef-4dab-bde6-b77e96dbb161/lesson/470a8d46-0969-412e-96d8-e9765579f763" />
</CardGroup>


# Endlessly Terminating Pods

Source: https://notes.kodekloud.com/docs/Kubernetes-Troubleshooting-for-Application-Developers/Troubleshooting-Scenarios/Endlessly-Terminating-Pods/page

This article explores reasons and solutions for pods and namespaces in Kubernetes that remain stuck in the terminating state.

When managing Kubernetes clusters, you may need to delete resources such as pods, deployments, or namespaces. In many cases, you can remove a pod using a simple command:

```bash theme={null}
kubectl delete pod NAME
```

For example:

```bash theme={null}
controlplane ~ ➜ k delete pod NAME
```

This command typically works as expected. However, sometimes a resource may not terminate correctly. In this article, we will explore the reasons behind such issues and provide methods to resolve them.

## Example: Pod Stuck in Termination

Consider a pod named `shipping-api-57cdd984bc-grq7g`. Deleting it might initially return:

```bash theme={null}
controlplane ~ ➜ k delete pod shipping-api-57cdd984bc-grq7g
pod "shipping-api-57cdd984bc-grq7g" deleted
```

Yet, when you inspect the pod list:

```bash theme={null}
controlplane ~ ⚠ k get pods
NAME                                READY   STATUS      RESTARTS   AGE
api                                 1/1     Terminating 0          19m
shipping-api-57cdd984bc-grq7g      1/1     Terminating 0          19m
```

Some pods remain in the **Terminating** state. This behavior is often due to background operations or cleanup tasks (similar to garbage collection) that must complete before the resource is fully removed.

## Using the --force Flag

One approach to handle this issue is to force delete the resource using the `--force` flag. Note that force deletion does not wait for confirmation that the underlying resource has been terminated:

```bash theme={null}
controlplane ~ ➜ k delete pod shipping-api-57cdd984bc-grq7g --force
Warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
pod "shipping-api-57cdd984bc-grq7g" force deleted
```

After executing the forced deletion, if you check for remaining pods, there is a possibility that the resource may still be present or continue running if the underlying dependencies have not been cleaned up.

<Callout icon="triangle-alert">
  Using the `--force` flag can lead to unintended side effects. Use this option sparingly and only when necessary.
</Callout>

## Removing Finalizers

Another effective method involves removing finalizers manually. Finalizers ensure that specific cleanup tasks—such as persistent volume or namespace protection actions—are completed before the resource is deleted.

When editing a pod stuck in termination, you might notice a finalizer in its configuration. For example:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"finalizers":["example.com/block-deletion"],"name":"api","namespace":"default"},"spec":{"containers":[{"image":"httpd","name":"pod-with-finalizer"}]}}
  creationTimestamp: "2024-07-07T22:01:14Z"
  deletionGracePeriodSeconds: 30
  deletionTimestamp: "2024-07-07T22:05:05Z"
  finalizers:
    - example.com/block-deletion
  name: api
  namespace: default
  resourceVersion: "2265"
  uid: 2a4a592c-7bd2-4a17-a123-1337c8fc1bff
spec:
  containers:
    - image: httpd
      imagePullPolicy: Always
      name: pod-with-finalizer
      resources: {}
      terminationMessagePath: /dev/termination-log
      terminationMessagePolicy: File
      volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-4bxj
          readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: node01
```

To allow the pod to be fully deleted, remove or set the finalizers to `null` and save the changes. This method is not just limited to pods; it can also be applied to other Kubernetes resources such as PersistentVolumeClaims (PVCs) and namespaces.

## Handling Stuck Namespaces

Sometimes, the issue isn’t limited to pods. Entire namespaces may get stuck in the terminating state. For example, you might have a namespace called `stable` that does not delete as expected.

You could try force deletion:

```bash theme={null}
controlplane ~ ➜ k delete ns stable --force
Warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
namespace "stable" force deleted
```

If the namespace remains stuck, remove the finalizers from its manifest. An edited namespace manifest might appear as follows:

```yaml theme={null}
apiVersion: v1
kind: Namespace
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Namespace","metadata":{"annotations":{},"finalizers":["example.com/finalizer"],"name":"stable"}}
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2024-07-07T22:04:35Z"
  labels:
    kubernetes.io/metadata.name: stable
  name: stable
  resourceVersion: "3669"
  uid: 40848036-5014-47eb-9c75-25c4847f8b03
spec: {}
status:
  conditions:
    - lastTransitionTime: "2024-07-07T22:04:40Z"
      message: All resources successfully discovered
      reason: ResourcesDiscovered
      status: "False"
      type: NamespaceDeletionDiscoveryFailure
    - lastTransitionTime: "2024-07-07T22:04:40Z"
      message: All legacy kube types successfully parsed
      reason: ParsedGroupVersions
      status: "False"
      type: [SECRET_REDACTED]
    - lastTransitionTime: "2024-07-07T22:04:40Z"
      message: All content successfully deleted, may be waiting on finalization
      reason: ContentDeleted
```

After removing (or nullifying) the finalizers and saving your changes, re-check the namespaces. The `stable` namespace should be successfully deleted once Kubernetes completes the finalization step.

## Verifying Resource Deletion

After using either forced deletion or manually removing finalizers, it is important to verify that the resource is no longer present. For example, check the status of pods with:

```bash theme={null}
controlplane ~ ➜ k get pods
```

Similarly, verify namespace deletion:

```bash theme={null}
controlplane ~ ➜ k get ns
```

<Callout icon="lightbulb">
  Always investigate further if resources remain stuck in the terminating state. Relying solely on forced deletion or removal of finalizers can mask underlying issues that require a deeper investigation.
</Callout>

## Final Thoughts

Managing resources in Kubernetes can sometimes lead to challenges such as lingering terminating pods or namespaces. By understanding the role of finalizers and the implications of force deletion, you can better troubleshoot and resolve these issues.

For more information on Kubernetes resource management, consider exploring the following resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

Happy troubleshooting!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-troubleshooting-for-application-developers/module/143d3913-caef-4dab-bde6-b77e96dbb161/lesson/d579e5e5-da72-4ab9-baba-9a56918ad4ef" />
</CardGroup>
