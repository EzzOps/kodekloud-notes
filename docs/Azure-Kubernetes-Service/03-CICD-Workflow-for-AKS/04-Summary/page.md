# Merged "AKS1-KodeKloudApp" as current context in /home/user/.kube/config
```

3. Verify your existing Service and Deployment:

```bash theme={null}
kubectl get service
kubectl get deployment
```

<Callout icon="lightbulb">
  Make sure your current context points to the correct AKS cluster. Use `kubectl config current-context` to check.
</Callout>

***

## 1. Export the Deployment to YAML

Run the following command to export the `kodekloudapp` Deployment manifest:

```bash theme={null}
kubectl get deployment kodekloudapp \
  --namespace default \
  --output yaml > deployment.yaml
```

A portion of the generated `deployment.yaml`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kodekloudapp
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kodekloudapp
  strategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: kodekloudapp
    spec:
      containers:
        - name: kodekloudapp
          image: <your-image>
          ports:
            - containerPort: 80
```

> Tip: Customize `replicas`, `strategy`, and container resources to match your production requirements.

***

## 2. Export the Service to YAML

Export the Service object:

```bash theme={null}
kubectl get service kodekloudapp \
  --namespace default \
  --output yaml > service.yaml
```

Remove dynamic fields from `service.yaml`:

* `clusterIP`
* `status.loadBalancer.ingress`
* `spec.ports[*].nodePort`

Your cleaned-up `service.yaml` should look like:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: kodekloudapp
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app: kodekloudapp
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
```

<Callout icon="triangle-alert">
  If you switch to `type: NodePort`, ensure `nodePort` values are in the 30000–32767 range.
</Callout>

***

## 3. Delete Imperative Resources

Remove the existing Deployment and Service:

```bash theme={null}
kubectl delete deployment kodekloudapp
kubectl delete service kodekloudapp
```

Verify they’re gone:

```bash theme={null}
kubectl get deployment  # No resources found
kubectl get service     # No resources found
```

***

## 4. Redeploy Declaratively

Apply your YAML manifests:

```bash theme={null}
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Check the status:

```bash theme={null}
kubectl get deployment
kubectl get service
```

Open the external IP in your browser to confirm the application is running.

***

## 5. Push-Based CI/CD Pipeline Overview

Below is a sample push-based pipeline in Azure DevOps. You can adapt these stages for GitHub Actions, GitLab CI, or other tools.

| Stage                  | Description                              | Example Tools                       |
| ---------------------- | ---------------------------------------- | ----------------------------------- |
| Source Control         | Push code & manifests to Git repo        | Azure Repos, GitHub, GitLab         |
| Continuous Integration | Build container image and run unit tests | Azure Pipelines, GitHub Actions     |
| Artifact Publishing    | Push Docker image to registry            | ACR, Docker Hub, ECR                |
| Continuous Deployment  | Detect new image; apply YAML to AKS      | `kubectl apply`, Helm, Flux CD      |
| Monitoring & Feedback  | Collect logs/metrics, update backlog     | Azure Monitor, Application Insights |

1. **Commit & Push** your application code and `deployment.yaml` + `service.yaml` to your repo.
2. **CI Pipeline**: Build the container image, run tests, and publish to Azure Container Registry (ACR).
3. **CD Trigger**: ACR webhook invokes the CD pipeline upon new image push.
4. **Deploy**: Execute `kubectl apply -f` on your manifests to update AKS.
5. **Monitor**: Use [Azure Monitor](https://docs.microsoft.com/azure/azure-monitor/) or [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview) for observability.

***

## References

* [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/azure/aks/)
* [Kubernetes YAML Configuration](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
* [Azure DevOps CI/CD](https://docs.microsoft.com/azure/devops/pipelines/)
* [Azure Container Registry](https://docs.microsoft.com/azure/container-registry/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/60e74513-d231-493d-90a3-71787380ae79/lesson/35e2e42a-ab83-4742-bb6b-280336043a36" />
</CardGroup>


# Summary

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/CICD-Workflow-for-AKS/Summary/page

This lesson explores managing Kubernetes resources declaratively in Azure Kubernetes Service, detailing CI/CD workflows and observability features.

In this lesson, we explore the declarative approach to managing Kubernetes resources in Azure Kubernetes Service (AKS). By adopting declarative configurations, you define *what* your infrastructure should look like, and Kubernetes ensures the cluster’s actual state matches your desired state.

Azure Kubernetes Service supports two primary CI/CD workflow patterns:

| Workflow Type                | Description                                                                                                                  | Trigger Mechanism                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Push-based workflow          | You push code or configuration changes directly to a pipeline, which then builds and deploys artifacts.                      | Manual `git push` or automated CI pipeline trigger |
| Pull-based workflow (GitOps) | A Git repository serves as the single source of truth. A GitOps operator continuously reconciles your cluster with the repo. | Operator polling or webhook-based syncing          |

## Push-based Workflow

With a **push-based** approach, your CI server (Azure DevOps, GitHub Actions, etc.) listens for changes in your application repository. When you commit or merge code, the pipeline:

```yaml theme={null}
