# Manual Scheduling

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Scheduling/Manual-Scheduling/page

This article explains methods for manually scheduling pods on nodes in Kubernetes without using the built-in scheduler.

Welcome to this lesson on manually scheduling pods on a node. In this guide, we explore methods for assigning pods to nodes without relying on Kubernetes' built-in scheduler, which can help in scenarios where you need greater control over pod placement.

## Understanding Pod Scheduling

When you create a pod, its manifest typically contains a field called `nodeName`. By default, this field is left unset, allowing the Kubernetes scheduler to assign the pod automatically. Consider the following manifest:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    name: nginx
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 8080
  nodeName:
```

Under normal circumstances, the Kubernetes scheduler scans for pods without a specified `nodeName`, determines the appropriate node based on its scheduling algorithm, and creates a binding object to assign the pod to that node.

<Callout icon="lightbulb">
  Without an active scheduler, pods will remain in the **Pending** state. You can confirm this by executing:
</Callout>

```bash theme={null}
kubectl get pods
