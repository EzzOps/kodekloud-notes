# Sprint 04 review

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-04/Sprint-04-review/page

This article reviews Sprint 04 objectives and achievements in automating Docker builds using Google Cloud Build.

Welcome back! In this Sprint 04 review, we’ll recap our objectives and confirm that each has been met, from configuring Cloud Build to publishing container images.

## Sprint 04 Goals

| Goal ID | Objective                                | Deliverable                           |
| ------- | ---------------------------------------- | ------------------------------------- |
| 1       | Understand Google Cloud Build            | `cloudbuild.yaml` configuration files |
| 2       | Connect Cloud Build to GitHub            | Build trigger on GitHub push          |
| 3       | Automate Docker image builds             | `Dockerfile` in application repo      |
| 4       | Store Docker images in Artifact Registry | Images pushed to GCP registry         |

## Implementation Steps

### 1. Configure Google Cloud Build

We defined build steps in a `cloudbuild.yaml` file to install dependencies, run tests, and build the Docker image:

```yaml theme={null}
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA']
images:
  - 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
```

> **lightbulb** Ensure the Cloud Build service account has `roles/artifactregistry.writer` and `roles/storage.admin` for pushing images.

### 2. Link Cloud Build to GitHub

We created a trigger so that any push to the `main` branch starts a build:

```bash theme={null}
gcloud beta builds triggers create github \
  --name="on-main-commit" \
  --repo-name="my-repo" \
  --repo-owner="my-org" \
  --branch-pattern="^main$" \
  --build-config="cloudbuild.yaml"
```

### 3. Automate Docker Image Builds

Our `Dockerfile` defines how the application is containerized:

```dockerfile theme={null}
FROM node:18-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install --production
COPY . .
CMD ["node", "server.js"]
EXPOSE 8080
```

This file ensures dependencies install and the app runs on port 8080.

### 4. Publish to Artifact Registry

After building, Cloud Build pushes to Google Cloud Artifact Registry:

```bash theme={null}
gcloud artifacts repositories create my-repo \
  --repository-format=docker \
  --location=us-central1
