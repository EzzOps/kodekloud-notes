# Validate our deployment on GKE

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-05/Validate-our-deployment-on-GKE/page

This guide explains how to verify the correct operation of a containerized application on Google Kubernetes Engine using both the Google Cloud Console and `kubectl`.

In this guide, you’ll learn how to confirm that your containerized application is running correctly on Google Kubernetes Engine (GKE). We cover both the Google Cloud Console and the `kubectl` command-line interface.

***

## 1. Verifying via the GCP Console

1. Navigate to **Kubernetes Engine > Clusters** in the Google Cloud Console.
2. Select your cluster (for example, **gcp-devops-project**).
3. In the cluster overview, click **Workloads** in the left menu to see all Deployments.
4. Choose the correct namespace (e.g., `gcp-devops-prod`). You’ll see your Deployment, the number of ready pods, and its status.
5. Click the Deployment name for detailed metrics on CPU, memory, and more.

![The image shows a Google Cloud Platform Kubernetes Engine dashboard displaying deployment details, including CPU, memory, and disk usage metrics. It also includes options for configuration and documentation links on the right side.](https://kodekloud.com/kk-media/image/upload/v1752875504/notes-assets/images/GCP-DevOps-Project-Validate-our-deployment-on-GKE/google-cloud-kubernetes-dashboard-deployment.jpg)

> **triangle-alert** Avoid editing your Deployment manifest directly in the Console. Since changes aren’t tracked in your GitHub-backed CI/CD pipeline, this can lead to configuration drift.

### Editing via the Console

When you click **Edit**, you’ll see a client-side apply patch like this:

```yaml theme={null}
apiVersion: apps/v1
manager: kubectl-client-side-apply
operation: Update
time: "2023-02-25T15:21:43Z"
fieldType: FieldsV1
fieldsV1:
  f:metadata:
    f:annotations:
      f:kubectl.kubernetes.io/last-applied-configuration: {}
  f:spec:
    f:template:
      f:spec:
        f:containers:
        - f:name: my-app
          f:image: gcr.io/my-project/my-image:latest
          f:ports:
          - f:containerPort: 5000
            f:protocol: TCP
          f:resources:
            f:requests:
              f:cpu: "100m"
              f:memory: "128Mi"
```

![The image shows a Google Cloud Platform interface for editing a Kubernetes Engine deployment, displaying YAML configuration details.](https://kodekloud.com/kk-media/image/upload/v1752875505/notes-assets/images/GCP-DevOps-Project-Validate-our-deployment-on-GKE/google-cloud-kubernetes-engine-yaml.jpg)

### Viewing Logs, Revisions, and Observability

* **Logs**: Monitor container output filtered by severity or time.
* **Revision History**: Track Deployment rollouts and rollbacks.
* **Observability**: Access extended metrics, charts, and health checks.

![The image shows a Google Cloud Platform Kubernetes Engine dashboard displaying deployment details and observability metrics for a project named "gcp-devops-gke." It includes sections for CPU and memory usage, container restarts, and documentation links.](https://kodekloud.com/kk-media/image/upload/v1752875506/notes-assets/images/GCP-DevOps-Project-Validate-our-deployment-on-GKE/gcp-devops-gke-kubernetes-dashboard.jpg)

#### Exposure & Actions

| Action                  | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| Scale Replicas          | Increase or decrease the number of pod replicas.           |
| Expose via LoadBalancer | Create a Service of type LoadBalancer for external access. |
| Configure Ingress       | Set up Ingress rules for host/path-based routing.          |
| Edit Configuration      | Modify your Deployment manifest via CI/CD to avoid drift.  |

> **lightbulb** Because no Service resource exists yet, the **Exposure** section will be empty.\
  We recommend using your CI/CD pipeline for all changes to ensure auditability.

***

## 2. Verifying via the Command Line

### a. Configure `kubectl` Credentials

Open Cloud Shell (or your local terminal) and run:

```bash theme={null}
gcloud container clusters get-credentials gcp-devops-project \
    --zone us-central1-c \
    --project kodekloud-gcp-training
```

This command retrieves cluster credentials and configures `kubectl` to use your GKE context.

### b. Check Pods in the Default Namespace

By default, `kubectl` queries the `default` namespace:

```bash theme={null}
kubectl get pods
