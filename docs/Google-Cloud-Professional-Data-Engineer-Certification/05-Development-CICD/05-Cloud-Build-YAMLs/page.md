# Cloud Build YAMLs

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Development-CICD/Cloud-Build-YAMLs/page

Explains a Cloud Build YAML example to build a Docker image, push to Google Container Registry, and deploy to Cloud Run as a simple CI/CD pipeline with best practices.

Welcome back.

In this lesson we examine a Cloud Build configuration file and walk through a compact, practical `cloudbuild.yaml` example. A single Cloud Build file (you can also use `cloudbuild.json`) defines the ordered steps your CI/CD pipeline executes—build, test, push, and deploy. This example reads source from the current directory, builds a Docker image, pushes it to Google Container Registry (GCR), and deploys the image to Google Cloud Run.

```yaml theme={null}
steps:
  # Build the Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-image:$BUILD_ID', '.']

  # Push the Docker image to Google Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-image:$BUILD_ID']

  # Deploy the Docker image to Google Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/my-image:$BUILD_ID'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
```

How to read this file

* steps: Cloud Build executes each listed step in order. Each step runs inside its own container image, so you can pick the best tooling image for each task.
  * Build step (docker build): Uses the `gcr.io/cloud-builders/docker` image to run Docker build commands in the build environment. The `-t` flag tags the image using Cloud Build substitution variables like `$PROJECT_ID` and `$BUILD_ID`.
  * Push step (docker push): Pushes the tagged image to Google Container Registry so it can be stored and referenced by downstream services.
  * Deploy step (gcloud run deploy): Uses the `gcr.io/cloud-builders/gcloud` image to run the `gcloud` CLI and deploy the pushed image to Cloud Run. The `--platform managed` flag targets fully managed Cloud Run in the specified region.

Why separate build and push steps?

* Cloud Build treats each step as an independent, containerized action. Separating build and push:
  * Stops the pipeline early if the image build fails.
  * Produces clearer logs per action.
  * Allows reusing a successfully built image in other steps (e.g., scan, test) before pushing.

Common Cloud Build substitution variables

| Variable     | Description                                                   | Example          |
| ------------ | ------------------------------------------------------------- | ---------------- |
| `PROJECT_ID` | GCP project identifier where images and services are created  | `my-gcp-project` |
| `BUILD_ID`   | Unique ID assigned to each build by Cloud Build               | `abcd-1234-ef56` |
| `SHORT_SHA`  | Shortened commit SHA (useful for image tags)                  | `3f7c8b2`        |
| `REPO_NAME`  | Cloud Source Repository or mirrored repo name (if applicable) | `my-repo`        |

> **lightbulb** Cloud Build substitution variables like `$PROJECT_ID` and `$BUILD_ID` are provided by the build environment. Steps share the same workspace (the source is mounted at `/workspace`), but each step runs in its own container image.

Best practices and tips

* Keep steps small and focused: one major action per step helps with debugging and logging.
* Use the appropriate builder image for the task: use `gcr.io/cloud-builders/docker` for Docker actions and `gcr.io/cloud-builders/gcloud` for `gcloud` invocations.
* Tag images with immutable identifiers: use `$BUILD_ID` or `SHORT_SHA` for reproducible deployments.
* Mount or fetch secrets securely (use Secret Manager and Cloud Build’s secret features) instead of hardcoding credentials.

Quick reference: When to use Cloud Run vs alternatives

* Cloud Run: serverless containers for stateless workloads, fully managed runtime, scales to zero.
* GKE / Compute Engine: use for stateful workloads, custom networking, or when you need fine-grained infrastructure control.
* Cloud Functions: event-driven serverless functions for small units of work.

Resources and links

* [Cloud Build documentation](https://cloud.google.com/build)
* [Cloud Run documentation](https://cloud.google.com/run)
* [Google Container Registry (GCR)](https://cloud.google.com/container-registry)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

This YAML automates a simple CI/CD flow: build → push → deploy. It’s suitable as a starting point for many containerized application pipelines and can be extended with tests, linting, vulnerability scans, and blue/green or canary deployments.

End of lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/02c15300-8e2a-455b-9032-0d4630391b66/lesson/76c53527-e917-4a70-8ce9-ec077aee8e0f)
