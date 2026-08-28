# List local branches
git branch

# Ensure you're on main
git checkout main

# Pull the latest changes
git pull origin main
```

<Callout icon="lightbulb">
  Use descriptive branch names like `development` to clearly separate lifecycle stages.
</Callout>

Now create and check out `development`:

```bash theme={null}
git checkout -b development
```

Verify you’re on the new branch:

```bash theme={null}
git branch
# * development
#   main
#   ...
```

Open your project in VS Code (or your preferred IDE) to confirm the active branch.

***

## 2. Customize `cloudbuild.yaml` for Development

Your production pipeline builds, pushes, and deploys the image `gcpdevops` to the `gcp-devops-prod` namespace:

```yaml theme={null}
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/gcpdevops', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/gcpdevops']
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=gke.yaml
      - --image=gcr.io/$PROJECT_ID/gcpdevops
      - --location=us-central1-c
      - --cluster=gcp-devops-project
      - --namespace=gcp-devops-prod
```

Update it to target a development image (`-dev`) and namespace (`gcp-devops-dev`):

```yaml theme={null}
steps:
  # Build development image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/gcpdevops-dev', '.']

  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/gcpdevops-dev']

  # Deploy to GKE dev namespace
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=gke.yaml
      - --image=gcr.io/$PROJECT_ID/gcpdevops-dev
      - --location=us-central1-c
      - --cluster=gcp-devops-project
      - --namespace=gcp-devops-dev
```

### Configuration Comparison

| Attribute           | Production        | Development           |
| ------------------- | ----------------- | --------------------- |
| Docker Tag          | `gcpdevops`       | `gcpdevops-dev`       |
| GKE Namespace       | `gcp-devops-prod` | `gcp-devops-dev`      |
| Cloud Build Trigger | Branch: `main`    | Branch: `development` |

***

## 3. Commit and Push Your Changes

```bash theme={null}
git add cloudbuild.yaml
git commit -m "Customize Cloud Build for development environment"
git push -u origin development
```

***

## 4. Configure a Cloud Build Trigger for `development`

### 4.1 Select the `development` Branch in GitHub

1. Go to your GitHub repository.
2. Open the **Branch** dropdown and choose `development`.

<Frame>
  ![The image shows a GitHub repository page for a project named "gcp-devops-project" with a dropdown menu displaying different branches. The repository includes a Docker Flask application written in Python.](https://kodekloud.com/kk-media/image/upload/v1752875513/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/gcp-devops-project-github-repo-docker-flask.jpg)
</Frame>

### 4.2 Create the Trigger in Google Cloud Build

1. In the GCP Console, navigate to **Cloud Build > Triggers**.
2. Click **Create Trigger**.

<Frame>
  ![The image shows the Google Cloud Build interface with a list of triggers for repositories, displaying details like name, description, repository, event, build configuration, and status.](https://kodekloud.com/kk-media/image/upload/v1752875514/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/google-cloud-build-triggers-interface.jpg)
</Frame>

3. Fill out the **Create trigger** form:
   * **Name**: `gcp-devops-project-development`
   * **Event**: Push to a branch
   * **Source repository**: *Your GitHub repo*
   * **Branch**: `^development$`
   * **Build configuration**: Cloud Build configuration file (`cloudbuild.yaml`)

<Frame>
  ![The image shows a Google Cloud Build interface where a trigger is being created for a project, with options to specify the event type and source repository details.](https://kodekloud.com/kk-media/image/upload/v1752875516/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/google-cloud-build-trigger-creation.jpg)
</Frame>

4. (Optional) Expand **Advanced settings** to adjust substitutions, timeouts, or notifications.

<Frame>
  ![The image shows a Google Cloud Build interface for creating a trigger, with options for branch selection, configuration type, and advanced settings.](https://kodekloud.com/kk-media/image/upload/v1752875517/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/google-cloud-build-trigger-interface.jpg)
</Frame>

5. Click **Create** to finalize.

### 4.3 Run and Verify the Trigger

* **Manual Trigger**: In **Cloud Build > Triggers**, click **Run** next to `gcp-devops-project-development`.
* **Monitor**: Go to **Cloud Build > History** to see builds initiated by the `development` branch.

<Frame>
  ![The image shows a Google Cloud Build interface displaying a build history with details such as status, build ID, source, commit, trigger name, creation time, and duration.](https://kodekloud.com/kk-media/image/upload/v1752875518/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/google-cloud-build-interface-history.jpg)
</Frame>

* Since the `gcp-devops-dev` namespace likely doesn’t exist yet, the deploy step will report a failure (this is expected at this stage):

<Frame>
  ![The image shows a Google Cloud Build interface with a failed build summary, including details of the build steps and logs.](https://kodekloud.com/kk-media/image/upload/v1752875519/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/google-cloud-build-failed-summary.jpg)
</Frame>

***

## 5. Verify the Development Image in Registry

Navigate to **Artifact Registry** or **Container Registry** in the GCP Console. Under `gcr.io`, confirm that `gcpdevops-dev` is present:

<Frame>
  ![The image shows a Google Cloud Container Registry interface with a list of repositories, each marked as private. There's also a notification about transitioning to Artifact Registry.](https://kodekloud.com/kk-media/image/upload/v1752875520/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-01/google-cloud-container-registry-repositories.jpg)
</Frame>

***

Congratulations! Your Cloud Build trigger for the `development` branch is live. In the next lesson, you’ll learn how to create the dev namespace and finalize automatic deployments.

***

## Links and References

* [Google Cloud Build Triggers Docs](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers)
* [GKE Deploy Builder](https://github.com/GoogleCloudPlatform/cloud-builders/tree/master/gke-deploy)
* [Kubernetes Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-devops-project/module/c8ea3a0c-6c88-4c7d-8317-f50354bae0e6/lesson/d813711c-ac3f-4ec9-b1e9-b65856c37e18" />
</CardGroup>


# Extending development environment 02

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-07/Extending-development-environment-02/page

This guide enhances your Google Kubernetes Engine development workflow covering cluster access, namespace isolation, manifest updates, automated builds, and deployment verification.

In this guide, you’ll continue enhancing your development workflow on Google Kubernetes Engine (GKE). We’ll cover cluster access, namespace isolation, manifest updates, automated builds, and deployment verification.

## Prerequisites

* A GCP project with a running GKE cluster
* `gcloud` CLI and `kubectl` installed and configured
* A GitHub repository connected to Cloud Build triggers

## 1. Connect to the Cluster and Create a Namespace

### 1.1 Launch Cloud Shell

1. Navigate to Google Cloud Console > Kubernetes Engine > Clusters.
2. Select your cluster and click **Connect** to open Cloud Shell.
3. Press **Enter** to run the pre-populated `kubectl` authentication command.

<Frame>
  ![The image shows a Google Cloud Platform (GCP) Kubernetes Engine console displaying details of a cluster named "gcp-devops-project," including cluster basics, automation, and networking settings.](https://kodekloud.com/kk-media/image/upload/v1752875521/notes-assets/images/GCP-DevOps-Project-Extending-development-environment-02/gcp-kubernetes-engine-cluster-details.jpg)
</Frame>

<Callout icon="lightbulb">
  Make sure your Google Cloud SDK is up to date to avoid authentication issues:

  ```bash theme={null}
  gcloud components update
  ```
</Callout>

### 1.2 Create and Verify the Development Namespace

```bash theme={null}
