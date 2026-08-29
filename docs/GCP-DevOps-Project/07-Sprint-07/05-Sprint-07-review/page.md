# List current namespaces
kubectl get namespaces

# Create a new namespace for development
kubectl create namespace development

# Confirm the namespace was created
kubectl get namespaces
```

## 2. Update the gke.yaml Manifest

Open your `gke.yaml` file. This manifest defines both the Service and Deployment for your application. Modify it to point at the `development` namespace and use your development Docker image.

### 2.1 Resource Overview

| Kind       | Purpose                           | Key Changes                                  |
| ---------- | --------------------------------- | -------------------------------------------- |
| Service    | Exposes your app via LoadBalancer | Set `namespace: development`, port 80 → 5000 |
| Deployment | Manages application pods          | Use `-dev:latest` image tag, replicas = 1    |

### 2.2 Updated Manifest Snippet

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: gcp-devops-gke-service
  namespace: development
  labels:
    app: gcp
spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  selector:
    app: gcp
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gcp-devops-gke
  namespace: development
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
          image: gcr.io/kodekloud-gcp-training/gcpdevops-dev:latest
          ports:
            - containerPort: 5000
          env:
            - name: PORT
              value: "5000"
```

Save your changes and push to the `development` branch:

```bash theme={null}
git add gke.yaml
git commit -m "chore: update manifests for development namespace"
git push origin development
```

This push will trigger your Cloud Build configuration.

## 3. Verify the Cloud Build Trigger

After pushing, open your GitHub repository to confirm that a Cloud Build trigger has started on the `development` branch.

![This image shows a GitHub repository page for a project named "gcp-devops-project" under the user "learnwithraghu." The repository contains files like Dockerfile, README.md, and app.py, and it mentions a Docker Flask application written in Python.](https://kodekloud.com/kk-media/image/upload/v1752875522/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-02/gcp-devops-project-github-repo-docker-flask.jpg)

## 4. Review Build and Deployment Logs

Go back to the GCP Console and navigate to **Cloud Build**. You’ll see logs for steps including:

* Building the Docker image
* Pushing to Container Registry
* Deploying to GKE

![The image shows a Google Cloud Build interface displaying the details of a successful build process, including steps and logs related to deploying a project using Docker and GKE.](https://kodekloud.com/kk-media/image/upload/v1752875523/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-02/google-cloud-build-successful-deploy.jpg)

All steps should complete without errors.

## 5. Inspect the Deployment in GKE

1. In the GCP Console, go to **Kubernetes Engine > Workloads** and filter by the `development` namespace.
   * Workload: `gcp-devops-gke`
2. Then select **Services & Ingress**, keeping the `development` filter applied.
3. Copy the external LoadBalancer IP and open it in your browser to verify your app is running.

![The image shows the Google Cloud Console interface, specifically the Kubernetes Engine section, with a focus on Services & Ingress. A filter dropdown for selecting namespaces is open.](https://kodekloud.com/kk-media/image/upload/v1752875524/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-02/google-cloud-console-kubernetes-services-ingress.jpg)

***

You’ve successfully set up a dedicated development namespace, updated your Kubernetes manifests for development artifacts, and confirmed an automated CI/CD pipeline. Future commits to the `development` branch will automatically build and deploy your application to GKE.

## Links and References

* [Kubernetes Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
* [Google Kubernetes Engine Documentation](https://cloud.google.com/kubernetes-engine/docs)
* [Cloud Build Triggers](https://cloud.google.com/build/docs/automating-builds)
* [kubectl CLI Reference](https://kubernetes.io/docs/reference/kubectl/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/c8ea3a0c-6c88-4c7d-8317-f50354bae0e6/lesson/7dc805aa-a32a-4340-b706-9448f2e85e70)


# Sprint 07 review

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-07/Sprint-07-review/page

This article recaps automating replica scaling in a DevOps pipeline, highlighting streamlined delivery, reduced manual toil, and increased team confidence.

In this article, we’ll recap how we rolled out a configuration change—namely, increasing our application replicas to five—through an automated DevOps lifecycle. You’ll learn how we streamlined development-to-production delivery, reduced manual toil, and boosted team confidence.

## Why Automate Replica Scaling?

Automating replica updates ensures consistency across environments, accelerates delivery, and minimizes human error. By embedding this change in our CI/CD pipeline, we maintained full traceability from commit to production.

> **lightbulb** Automated scaling is crucial for handling traffic spikes. Always couple replica changes with resource monitoring to validate performance.

## CI/CD Workflow for Configuration Changes

Below is the end-to-end process we followed for Sprint 07:

| Stage           | Action                                           | Environment | Outcome                                 |
| --------------- | ------------------------------------------------ | ----------- | --------------------------------------- |
| 1. Commit       | Update replica count from 3 to 5 in `dev` branch | Development | Trigger CI build                        |
| 2. Build & Test | CI pipeline builds Docker image and runs tests   | Development | Validation of configuration change      |
| 3. Deploy (Dev) | Deploy new image with 5 replicas                 | Development | QA sign-off                             |
| 4. Promote      | Merge `dev` → `main`, trigger CD to production   | Production  | Live application now running 5 replicas |

### Pipeline Details

1. **Code Commit**\
   Developers update the `replicas:` field in the Kubernetes manifest on the `development` branch.

2. **Continuous Integration**
   * Build Docker image
   * Run unit tests and linters
   * Push image to container registry
   * [Learn more about CI/CD](https://www.atlassian.com/continuous-delivery/ci-vs-ci-vs-cd)

3. **Development Deployment**
   * Helm chart or `kubectl apply` deploys the image
   * Automated smoke tests validate the rollout

4. **Quality Assurance**
   * QA engineers perform functional and performance tests
   * Approval triggers the merge into the `main` branch

5. **Production Promotion**
   * CD pipeline deploys the change to production clusters
   * Monitoring alerts confirm stable operation

> **triangle-alert** Before promoting to production, ensure your alerting and auto-scaling policies are configured, or you may experience resource constraints under load.

## Benefits Realized

* **Faster Feedback Loops**\
  Immediate testing in dev environments catches issues early.
* **Consistent Environments**\
  The same manifest promotes through all stages, reducing drift.
* **Reduced Manual Overhead**\
  Teams focus on feature work rather than repetitive deployments.

## Next Steps

* Integrate automated performance tests in the pipeline.
* Explore [Infrastructure as Code](https://www.terraform.io/) for managing cluster configuration.
* Implement horizontal pod auto-scalers to dynamically adjust replicas based on metrics.

***

## References

* [GitFlow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)
* [Continuous Delivery Best Practices](https://martinfowler.com/bliki/ContinuousDelivery.html)
* [Kubernetes Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/c8ea3a0c-6c88-4c7d-8317-f50354bae0e6/lesson/9b4e0c9f-7331-4e9c-8bb6-fefdeb1c6123)
