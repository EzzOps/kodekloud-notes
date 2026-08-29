# Solution Resource Quotas Limits

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Solution-Resource-Quotas-Limits/page

This guide demonstrates Kubernetes resource constraints using example pods to identify requests, diagnose failures, and update specifications.

In this guide, we demonstrate how Kubernetes enforces CPU and memory constraints using two example pods, **rabbit** and **elephant**. You will learn how to:

* Identify resource requests and limits
* Diagnose pod failures caused by insufficient resources
* Update pod specifications to prevent OOM kills

## Pod "rabbit": Identifying CPU Requests

First, confirm that the **rabbit** pod is running and examine its resource settings:

```bash theme={null}
kubectl get pod rabbit
kubectl describe pod rabbit
```

Excerpt from the description shows:

```text theme={null}
Containers:
  cpu-stress:
    Limits:
      cpu: 2
    Requests:
      cpu: 1
```

Here, the **rabbit** pod requests **1 CPU** and caps at **2 CPUs**.

To clean up:

```bash theme={null}
kubectl delete pod rabbit
