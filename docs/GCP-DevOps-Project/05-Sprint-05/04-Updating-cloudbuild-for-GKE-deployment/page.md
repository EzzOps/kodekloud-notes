# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
```

Apply it in your pipeline or manually:

```bash theme={null}
kubectl apply -f namespace.yaml
```

## 2. Prepare the Deployment Manifest

Create `deployment.yaml` to describe your application pods and replicas:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
  namespace: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: gcr.io/PROJECT_ID/my-app:latest
        ports:
        - containerPort: 8080
```

## 3. Update Your Cloud Build Configuration

Modify your `cloudbuild.yaml` to include steps for namespace creation and manifest application:

```yaml theme={null}
steps:
  - name: gcr.io/cloud-builders/kubectl
    args:
      - apply
      - -f
      - namespace.yaml
  - name: gcr.io/cloud-builders/kubectl
    args:
      - apply
      - -f
      - deployment.yaml
images:
  - gcr.io/PROJECT_ID/my-app:$SHORT_SHA
```

For more details on Cloud Build, see the [Cloud Build documentation](https://cloud.google.com/build).

## 4. Validate the Deployment

After Cloud Build finishes, confirm that your pods and services are up:

```bash theme={null}
kubectl get all -n my-app
```

***

![The image lists four steps for a deployment process: creating a namespace in a GKE cluster, creating a deployment file, updating Cloud Build code for deployment, and validating the deployment.](https://kodekloud.com/kk-media/image/upload/v1752875501/notes-assets/images/GCP-DevOps-Project-Sprint-05/gke-deployment-process-steps-2.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/c1a43d47-87cb-459f-a9bf-2000d6223395/lesson/bf9647fa-4994-46ce-a7c7-53f8439e711b)


# Updating cloudbuild for GKE deployment

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-05/Updating-cloudbuild-for-GKE-deployment/page

This guide explains how to automate Docker image deployment to Google Kubernetes Engine using Cloud Build.

Deploying your Docker image to Google Kubernetes Engine (GKE) can be fully automated using **Cloud Build**. In this guide, we’ll update our CI/CD pipeline by extending `cloudbuild.yaml` to:

1. Build the Docker image
2. Push it to Google Container Registry (GCR)
3. Deploy to a GKE cluster with a Kubernetes manifest

***

## Prerequisites

* A GKE cluster up and running
* `gcloud` CLI configured with your project and zone
* Cloud Build API enabled
* Service account with the following roles:
  * `roles/container.developer`
  * `roles/storage.admin`

> **lightbulb** Ensure your Cloud Build service account has the **Kubernetes Engine Developer** and **Storage Admin** roles. Without these, build or deploy steps may fail.

***

## Kubernetes Deployment Manifest

We’ve already created a Kubernetes Deployment manifest (`gke.yaml`) for our sample app:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gcp-devops-gke
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gcp
  template:
    metadata:
      labels:
        app: gcp
    spec:
      containers:
        - name: gcp-devops-gke
          image: gcr.io/kodekloud-gcp-training/test-gcpdevops:latest
          ports:
            - containerPort: 5000
          env:
            - name: PORT
              value: "5000"
```

This Deployment exposes port **5000** and pulls the image from GCR. Next, let’s configure Cloud Build.

***

## Initial cloudbuild.yaml

Our starting `cloudbuild.yaml` only built and pushed the Docker image:

```yaml theme={null}
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      ['build', '-t', 'gcr.io/$PROJECT_ID/gcpdevops', '.']
images:
  - 'gcr.io/$PROJECT_ID/gcpdevops'
```

***

## Extending cloudbuild.yaml for GKE Deployment

We’ll add a third step to invoke the `gke-deploy` builder, which applies our Kubernetes manifest directly to GKE:

```yaml theme={null}
steps:
  # 1. Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      ['build', '-t', 'gcr.io/$PROJECT_ID/gcpdevops', '.']

  # 2. Push the container image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      ['push', 'gcr.io/$PROJECT_ID/gcpdevops']

  # 3. Deploy to GKE
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      [
        'run',
        '--filename=gke.yaml',
        '--image=gcr.io/$PROJECT_ID/gcpdevops',
        '--location=us-central1-c',
        '--cluster=gke-gcp-devops',
        '--namespace=gcp-devops-prod'
      ]

images:
  - 'gcr.io/$PROJECT_ID/gcpdevops'
```

***

### Step-by-Step Overview

| Step | Builder Image                    | Arguments                                                                                                                                    | Purpose                                 |
| ---- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| 1    | gcr.io/cloud-builders/docker     | `build -t gcr.io/$PROJECT_ID/gcpdevops .`                                                                                                    | Build the container image               |
| 2    | gcr.io/cloud-builders/docker     | `push gcr.io/$PROJECT_ID/gcpdevops`                                                                                                          | Push image to Google Container Registry |
| 3    | gcr.io/cloud-builders/gke-deploy | `run --filename=gke.yaml --image=gcr.io/$PROJECT_ID/gcpdevops --location=us-central1-c --cluster=gke-gcp-devops --namespace=gcp-devops-prod` | Deploy manifest to your GKE cluster     |

***

## References

* [Cloud Build Quickstart](https://cloud.google.com/build/docs/quickstart-build)
* [gke-deploy GitHub Repository](https://github.com/GoogleCloudPlatform/cloud-run-hello)
* [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)

***

## Next Steps

1. Commit and push your updated `cloudbuild.yaml` to a feature branch.
2. Open a pull request for review.
3. Merge into `main`.

Once merged, Cloud Build will automatically execute the pipeline, build and push your container, then deploy the updated manifest to your GKE cluster. Finally, use:

```bash theme={null}
kubectl get pods --namespace gcp-devops-prod
```

to verify your application is running successfully.

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/c1a43d47-87cb-459f-a9bf-2000d6223395/lesson/013ab2a5-3092-4ce9-90d3-ee84d9c51ce2)
