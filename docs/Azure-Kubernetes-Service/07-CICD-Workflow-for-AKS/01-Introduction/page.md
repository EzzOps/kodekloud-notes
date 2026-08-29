# Introduction

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/CICD-Workflow-for-AKS/Introduction/page

This article compares imperative and declarative deployment methods in Kubernetes, highlighting their pros, cons, and use cases for effective resource management.

Kubernetes supports two primary deployment methods: Imperative and Declarative. The Imperative approach relies on explicit `kubectl` commands to create and manage resources step by step. The Declarative approach uses YAML or JSON manifests to define the desired state of your cluster, which Kubernetes continuously reconciles. Choosing the right method helps teams optimize for speed, reproducibility, and maintainability in environments like [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/).

![The image compares imperative and declarative approaches to Kubernetes deployment, highlighting specific commands and defined steps for imperative, and YAML/JSON manifests for declarative.](https://kodekloud.com/kk-media/image/upload/v1752869453/notes-assets/images/Azure-Kubernetes-Service-Introduction/kubernetes-deployment-imperative-declarative-comparison.jpg)

## Imperative vs Declarative at a Glance

| Aspect           | Imperative Deployment               | Declarative Deployment                     |
| ---------------- | ----------------------------------- | ------------------------------------------ |
| Definition       | Step-by-step `kubectl` commands     | Desired-state manifests (YAML/JSON)        |
| Execution        | Immediate and manual                | Automated reconciliation via control plane |
| Idempotency      | Not guaranteed on reruns            | Always converges to desired state          |
| Common Use Cases | Prototyping, troubleshooting, demos | Production, CI/CD pipelines, GitOps        |

## Imperative Deployment

Imperative deployment gives you direct control through explicit commands. Here’s a typical workflow:

```bash theme={null}
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80
kubectl scale deployment nginx --replicas=3
kubectl delete service nginx
```

### Pros

* Granular, step-by-step control
* Instant feedback after each command
* Perfect for ad hoc tasks: debugging, prototyping, one-off operations

### Cons

* Difficult to reproduce complex setups consistently
* Lacks idempotency—rerunning commands can yield different results
* Hard to track changes in version control

> **triangle-alert** Imperative commands can introduce configuration drift if reused without validation. Always verify resource status with `kubectl get` or integrate into CI pipelines.

![The image is a comparison of the pros and cons of imperative Kubernetes deployment. Pros include fine-grained control and flexibility, while cons highlight being more error-prone and lacking idempotency.](https://kodekloud.com/kk-media/image/upload/v1752869454/notes-assets/images/Azure-Kubernetes-Service-Introduction/kubernetes-imperative-deployment-pros-cons.jpg)

## Declarative Deployment

In the declarative model, you define the desired state in a manifest file, and Kubernetes ensures the live cluster matches it. For example:

```yaml theme={null}
