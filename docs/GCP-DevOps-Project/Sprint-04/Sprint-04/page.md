# Already covered by cloudbuild.yaml, but manual push example:
docker tag my-app gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA
docker push gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA
```

<Callout icon="triangle-alert">
  Verify that your Artifact Registry repository is in the same region as your Cloud Build trigger to avoid latency issues.
</Callout>

## Results and Next Steps

* All build steps in `cloudbuild.yaml` execute successfully.
* GitHub pushes to `main` automatically trigger Cloud Build.
* Docker images build without manual intervention.
* Images are stored in Artifact Registry and available for deployment.

With Sprint 04 complete, our CI/CD pipeline is fully automated on Google Cloud Platform.

Thank you, and see you in the next lesson!

***

## References

* [Google Cloud Build](https://cloud.google.com/build)
* [Artifact Registry](https://cloud.google.com/artifact-registry)
* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [GitHub integration](https://cloud.google.com/build/docs/automating-builds/github)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-devops-project/module/f84d8c20-935f-462e-9503-94408617064a/lesson/1e78b741-6429-4936-9e4b-228a21102997" />
</CardGroup>


# Sprint 04

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-04/Sprint-04/page

This article explores automating Docker image builds using Google Cloud Build and integrating it with GitHub for continuous deployment.

In this sprint, we'll explore Google Cloud Build—its core capabilities—and automate Docker image builds from GitHub into Google Artifact Registry. By the end, you will:

* Grasp Cloud Build features and benefits
* Link a GitHub repo to Cloud Build via triggers
* Automate Docker image builds on merges and push them to Artifact Registry

***

## 1. Key Features of Cloud Build

Before writing any pipelines, it’s crucial to understand what Cloud Build offers. Search the [official Cloud Build Documentation][Cloud Build Documentation] or the [Cloud Console][Cloud Console] for more details.

<Frame>
  ![The image shows a search bar with the query "What are the features of Cloud Build?"](https://kodekloud.com/kk-media/image/upload/v1752875488/notes-assets/images/GCP-DevOps-Project-Sprint-04/cloud-build-features-search-bar.jpg)
</Frame>

| Feature                              | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| Flexible Build Configurations        | Define builds in YAML or JSON                      |
| Native Artifact Registry Integration | Push and pull images directly to Artifact Registry |
| Multiple Source Repository Support   | Connect Cloud Source Repos, GitHub, Bitbucket      |
| Parallel Steps & Caching             | Speed up builds with parallelism and cache layers  |

<Callout icon="lightbulb">
  Cloud Build can also integrate with Pub/Sub, Cloud Functions, and other GCP services for advanced workflows.
</Callout>

***

## 2. Set Up a GitHub Trigger

Linking Cloud Build to your GitHub repository allows automated builds on code changes. Follow these steps:

1. **Enable the Cloud Build API**\
   In your GCP project, navigate to **APIs & Services » Library** and enable **Cloud Build API**.
2. **Create a Build Trigger**
   * Go to **Cloud Build » Triggers** in the Cloud Console.
   * Click **Create trigger** and choose **GitHub** as the source.
3. **Authorize & Select Repository**\
   Grant Cloud Build access to your GitHub account and pick the target repository.
4. **Configure Trigger Events**
   * Trigger on `push` to the `main` branch.
   * Optionally, fire on pull-request merges.

<Callout icon="triangle-alert">
  Ensure your GitHub App has the correct scopes (repo, admin:repo\_hook) to create webhooks and read repository data.
</Callout>

***

## 3. Define cloudbuild.yaml to Build & Push Docker Images

With your trigger in place, add a `cloudbuild.yaml` at the root of your repo. This file defines steps to build a Docker image and push it into Artifact Registry.

<Frame>
  ![The image illustrates a process flow from automating Docker image builds to storing them in the GCP Artifact Registry.](https://kodekloud.com/kk-media/image/upload/v1752875489/notes-assets/images/GCP-DevOps-Project-Sprint-04/docker-image-builds-gcp-artifact-flow.jpg)
</Frame>

```yaml theme={null}
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - build
      - -t
      - 'us-central1-docker.pkg.dev/my-project/my-repo/my-app:$SHORT_SHA'
      - .
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - push
      - 'us-central1-docker.pkg.dev/my-project/my-repo/my-app:$SHORT_SHA'
images:
  - 'us-central1-docker.pkg.dev/my-project/my-repo/my-app:$SHORT_SHA'
```

What happens during execution:

1. **Build**: Docker builds an image tagged with the commit's short SHA.
2. **Push**: The image is uploaded to Artifact Registry.
3. **Images**: Cloud Build tracks uploaded images for logging and metadata.

<Callout icon="lightbulb">
  Use variables like `$SHORT_SHA`, `$BRANCH_NAME`, or custom substitutions to tag images dynamically.
</Callout>

***

## Sprint 04 Goals Recap

<Frame>
  ![The image lists sprint goals related to Cloud Build, including understanding it in detail, connecting it to a GitHub repository, and automating the Docker image build process.](https://kodekloud.com/kk-media/image/upload/v1752875490/notes-assets/images/GCP-DevOps-Project-Sprint-04/cloud-build-sprint-goals-docker-automation.jpg)
</Frame>

1. Detailed understanding of Cloud Build features
2. GitHub repository integration via build triggers
3. Automated Docker image builds and storage in Artifact Registry

Congratulations—you’ve automated your CI/CD pipeline for Docker images! See you in the next sprint.

***

## Links and References

* [Cloud Build Documentation][Cloud Build Documentation]
* [Cloud Console][Cloud Console]
* [Artifact Registry Docs][Artifact Registry Docs]
* [cloudbuild.yaml Reference][YAML Reference]

[Cloud Build Documentation]: https://cloud.google.com/build/docs

[Cloud Console]: https://console.cloud.google.com

[Artifact Registry Docs]: https://cloud.google.com/artifact-registry/docs

[YAML Reference]: https://cloud.google.com/build/docs/configuring-builds/create-basic-configuration

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-devops-project/module/f84d8c20-935f-462e-9503-94408617064a/lesson/623f41ca-0c0d-40fb-8f6b-076077ff3208" />
</CardGroup>
