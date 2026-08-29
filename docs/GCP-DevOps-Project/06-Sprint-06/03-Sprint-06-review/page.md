# Sprint 06 review

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-06/Sprint-06-review/page

This article recaps how to expose applications on Google Kubernetes Engine by configuring a Kubernetes Service.

Welcome back! In this article, we’ll recap how to expose applications on Google Kubernetes Engine (GKE).

## Objective

Expose the application deployed on our GKE cluster to external or internal clients.

## Configuring the Kubernetes Service

To make your application accessible, create a Service of type `LoadBalancer`. On GKE, this automatically provisions a cloud load balancer and assigns an external IP or URL.

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

Apply the manifest:

```bash theme={null}
kubectl apply -f service.yaml
```

Then check the external IP:

```bash theme={null}
kubectl get svc my-app-service
```

Wait until the `EXTERNAL-IP` field is populated, then navigate to `http://<EXTERNAL-IP>`.

> **lightbulb** Run `kubectl describe svc my-app-service` for detailed load balancer events and annotations.

## Choosing the Right Service Type

Depending on your environment and security requirements, you can select one of the following Service types:

| Service Type | Description                                                | Use Case                                     |
| ------------ | ---------------------------------------------------------- | -------------------------------------------- |
| LoadBalancer | Provisions a cloud load balancer with an external IP       | Production or public-facing services         |
| NodePort     | Exposes the Service on a static port (≥30000) on each node | Development and basic internal access        |
| ClusterIP    | Default; accessible only within the cluster                | Internal services that should not be exposed |

> **triangle-alert** ClusterIP services are not reachable from outside the cluster. Verify your network policies before switching types.

## Summary

In Sprint 0.6, we configured a Kubernetes Service on GKE to expose our application. Choose the Service type—`LoadBalancer`, `NodePort`, or `ClusterIP`—that best fits your deployment needs.

## References

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs)
* [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)
* [kubectl Documentation](https://kubernetes.io/docs/reference/kubectl/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/001eaf30-3cc6-4d71-8b48-c59ac4e5e0f8/lesson/e7edc6b3-3a23-41bc-a04a-68cf941451c5)
