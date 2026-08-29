# Check your current branch
git branch
# Example output:
# Create and switch to a new feature branch
git checkout -b minor/cloudbuild
# Example output:
# Verify you’re on the new branch
git branch
# Example output:
# * minor/cloudbuild
#   main
```

***

## 2. Add the Cloud Build Configuration

In the root of your repository, create a `cloudbuild.yaml` file. Cloud Build uses this file to define build steps, images to push, and other options.

```yaml theme={null}
steps:
  - name: 'docker'
    args:
      - build
      - '-t'
      - 'gcr.io/$PROJECT_ID/gcpdevops'
      - '.'
images:
  - 'gcr.io/$PROJECT_ID/gcpdevops'
```

| Field      | Description                                                   |
| ---------- | ------------------------------------------------------------- |
| steps.name | Docker builder image used for the build                       |
| steps.args | Arguments passed to `docker build` (tagging and context path) |
| images     | Destination(s) in Container/Artifact Registry to push to      |

> **lightbulb** Ensure the **Cloud Build API** and **Artifact Registry API** are enabled in your Google Cloud project.

***

## 3. Commit and Push Changes

Once your `cloudbuild.yaml` is in place, commit and push your changes:

```bash theme={null}
git add cloudbuild.yaml
git commit -m "Add Cloud Build configuration for Docker images"
git push origin minor/cloudbuild
```

Then open a pull request targeting the `main` branch and merge it once approved.

***

## 4. Configure and Verify Your Cloud Build Trigger

In the [Google Cloud Console](https://console.cloud.google.com/), navigate to **Cloud Build › Triggers** and confirm:

* **Event**: Push to the `main` branch
* **Source**: Your repository
* **Build Configuration**: Use `cloudbuild.yaml` in the root of the repository

![The image shows a Google Cloud Build interface where a trigger is being edited. It includes options for event types, source repository, branch, and configuration settings.](https://kodekloud.com/kk-media/image/upload/v1752875461/notes-assets/images/GCP-DevOps-Project-Automate-Docker-build-using-Cloud-Build/google-cloud-build-trigger-edit-interface.jpg)

***

## 5. Merge and Monitor the Build

After merging your PR, Cloud Build will automatically start a build. To track progress:

1. Go to **Cloud Build › Dashboard**.
2. Click on the latest build in **History** to view real-time logs.

![The image shows the Google Cloud Build interface with a trigger set up for a project named "gcp-devops-project." The trigger is configured to run on a push to a branch event.](https://kodekloud.com/kk-media/image/upload/v1752875463/notes-assets/images/GCP-DevOps-Project-Automate-Docker-build-using-Cloud-Build/google-cloud-build-trigger-gcp-devops.jpg)

Example log output:

```text theme={null}
FETCHSOURCE
  hint: Using 'main' as the name of the initial branch...

BUILD
  Pulling image: docker
  Starting build...
  Building default tag: latest
  ...

PUSH
  Pushing gcr.io/...
```

> **triangle-alert** Merging directly to `main` triggers a build. Make sure your `cloudbuild.yaml` is correct to avoid broken pipelines.

***

## 6. Inspect Your Artifacts

Once the build completes, open **Artifact Registry**:

1. Enable Artifact Registry if prompted (may take a minute).
2. Click **Container Registry** to view your `gcr.io` repositories.

![The image shows a Google Cloud Platform (GCP) console interface for Artifact Registry, with options to turn on vulnerability scanning and a list of container registry hostnames and their locations.](https://kodekloud.com/kk-media/image/upload/v1752875464/notes-assets/images/GCP-DevOps-Project-Automate-Docker-build-using-Cloud-Build/gcp-artifact-registry-console-vulnerability-scanning.jpg)

You should see a `gcpdevops` repository:

![The image shows a Google Cloud Console interface for Container Registry, highlighting a transition to Artifact Registry with a repository named "gcpdevops" listed as private.](https://kodekloud.com/kk-media/image/upload/v1752875465/notes-assets/images/GCP-DevOps-Project-Automate-Docker-build-using-Cloud-Build/google-cloud-console-container-registry.jpg)

Drill into the repository to view tags, sizes, and timestamps:

![The image shows a Google Cloud Container Registry interface displaying a list of container images. It includes details like image name, tags, virtual size, and timestamps for creation and upload.](https://kodekloud.com/kk-media/image/upload/v1752875467/notes-assets/images/GCP-DevOps-Project-Automate-Docker-build-using-Cloud-Build/google-cloud-container-registry-images-list.jpg)

***

## Recap and Next Steps

You’ve now:

* Set up a feature branch and added `cloudbuild.yaml`
* Configured a Cloud Build trigger on pushes to `main`
* Monitored build logs and verified successful pushes to Artifact Registry

In the next lesson, we’ll integrate testing steps and deploy these images to a Kubernetes cluster as part of a full CI/CD pipeline.

***

## Further Reading

* [Cloud Build Documentation](https://cloud.google.com/build/docs/)
* [Artifact Registry Overview](https://cloud.google.com/artifact-registry/docs)
* [Docker Official Images](https://hub.docker.com/_/docker)
* [Kubernetes CI/CD Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/cloud-controller-manager/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/f84d8c20-935f-462e-9503-94408617064a/lesson/fa0ed760-ba86-4c44-a074-b6404b10f8c4)


# Cloud Build trigger

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-04/Cloud-Build-trigger/page

Cloud Build triggers automate build jobs in Google Cloud Build based on specific events in your GitHub repository.

Cloud Build triggers let you automatically start build jobs in Google Cloud Build whenever specific events occur in your GitHub repository—just like webhooks in Jenkins. By connecting your repo to Cloud Build through a trigger, you can ensure consistent, repeatable builds for your CI/CD pipeline.

## Why Use a Cloud Build Trigger?

In Jenkins, you configure webhooks to detect pushes or pull requests in GitHub. Cloud Build provides the same capability natively with **Cloud Build triggers**, which listen for repository events and kick off builds defined in your `cloudbuild.yaml`.

> **lightbulb** Before you begin, make sure you’ve granted Cloud Build access to your GitHub repository. See [Create and Manage Triggers](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers) for detailed steps.

![The image is a flow diagram showing a process from GitHub to Cloud Build via a Cloud Build Trigger.](https://kodekloud.com/kk-media/image/upload/v1752875468/notes-assets/images/GCP-DevOps-Project-Cloud-Build-trigger/github-cloud-build-trigger-flow-diagram.jpg)

## Common Trigger Events

When creating a trigger, you specify which events should start a build. Typical events include:

| Event Type                   | Description                                              |
| ---------------------------- | -------------------------------------------------------- |
| Push to `main` or `master`   | Ideal for deploying from the primary branch              |
| Push to a specific branch    | Build feature or release branches on demand              |
| Pull request creation/update | Test code before merging changes into protected branches |

![The image shows a document icon with three location markers and text stating that any push on the main/master branch will trigger a Cloud Build.](https://kodekloud.com/kk-media/image/upload/v1752875469/notes-assets/images/GCP-DevOps-Project-Cloud-Build-trigger/document-icon-location-markers-cloud-build.jpg)

## How It Works

1. **Define the trigger**\
   In the Cloud Console or via `gcloud`, link your GitHub repo and select the event and branch filters.

2. **Provide your build configuration**\
   Cloud Build looks for a `cloudbuild.yaml` at the repo root. Each step runs in its own container image, in sequence:

   ```yaml theme={null}
   steps:
     - name: 'gcr.io/cloud-builders/docker'
       args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA', '.']
     - name: 'gcr.io/cloud-builders/docker'
       args: ['push', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA']
   images:
     - 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
   ```

3. **Trigger execution**\
   When GitHub detects your specified event (e.g., `push` to `main`), it notifies Cloud Build, which then runs your pipeline automatically.

> **triangle-alert** Ensure your `cloudbuild.yaml` is valid and located at the repository root. Otherwise, triggers will fail with a configuration error.

## Next Steps

* Configure and test your Cloud Build trigger.
* Monitor build history in the Cloud Console under **Cloud Build > History**.
* Integrate additional notifications or approvals as needed.

***

## References

* [Cloud Build Triggers Documentation](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers)
* [cloudbuild.yaml Reference](https://cloud.google.com/build/docs/build-config-file-schema)
* [GitHub Integration Guide](https://cloud.google.com/build/docs/automating-builds/github-builds)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/f84d8c20-935f-462e-9503-94408617064a/lesson/ba8b5efa-8408-4633-b747-8f384d8089a4)
