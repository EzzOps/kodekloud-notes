# Authenticate with Google Cloud
gcloud auth login

# Set the active project
gcloud config set project PROJECT_ID

# Interact with Cloud Storage
gsutil ls gs://my-bucket

# Interact with BigQuery
bq query 'SELECT COUNT(*) FROM `my_dataset.my_table`'

# Interact with Kubernetes clusters (GKE)
kubectl get pods
```

Tip: Use scripts and CI/CD steps that call these commands to automate repetitive tasks and reduce manual errors.

## 3) Cloud Build — serverless CI/CD for GCP

Cloud Build is Google Cloud’s serverless CI/CD engine. It executes build steps defined in a `cloudbuild.yaml` or `cloudbuild.json` to build, test, push, and deploy artifacts. Cloud Build integrates with source repos (GitHub, Cloud Source Repositories) and triggers automated pipelines on events like push or pull request.

What Cloud Build does for you:

* Builds container images and other artifacts.
* Runs automated tests and linters.
* Pushes images to Artifact Registry or Container Registry.
* Deploys artifacts to Cloud Run, GKE, App Engine, or other targets.

<Callout icon="lightbulb">
  Exam and practical tip: focus on three areas — the SDK and its specialized tools, mastery of `gcloud` for everyday tasks, and how Cloud Build uses `cloudbuild.yaml` to automate build/test/deploy pipelines. Knowing how these pieces connect is key to reliable CI/CD on GCP.
</Callout>

## Practical example: Deploying a Streamlit app with Cloud Build

Scenario: a data scientist stores a Streamlit app in GitHub and wants an automated deploy to Cloud Run. As the platform engineer or data engineer, you’d implement a repeatable workflow that builds, tests, stores the image, and deploys.

Typical workflow:

* Store app code in a GitHub repo.
* Create `cloudbuild.yaml` to:
  * Build a Docker image.
  * Run tests (if any).
  * Push the image to Artifact Registry or Container Registry.
  * Deploy to Cloud Run.
* Configure a Cloud Build trigger on the GitHub repo to run builds on push/PR.
* Use `gcloud` for initial setup and troubleshooting.

High-level commands to run locally or in automation:

```bash theme={null}
# Log in and set project (run locally once)
gcloud auth login
gcloud config set project PROJECT_ID

# Submit a local build using the cloudbuild.yaml (optional)
gcloud builds submit --config=cloudbuild.yaml .

# Deploy a built image to Cloud Run
gcloud run deploy my-streamlit-app \
  --image=gcr.io/PROJECT_ID/my-streamlit-image \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated
```

This represents the typical flow:
source code → Cloud Build (build & test) → Artifact/Container Registry → Cloud Run (deploy).

## References and further reading

* [Google Cloud SDK (gcloud) Documentation](https://cloud.google.com/sdk/docs)
* [Cloud Build Overview](https://cloud.google.com/build/docs/overview)
* [Cloud Run Documentation](https://cloud.google.com/run/docs)
* [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
* [Cloud Storage (gsutil) docs](https://cloud.google.com/storage/docs/gsutil)

That’s it for this summary — see you next time.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/02c15300-8e2a-455b-9032-0d4630391b66/lesson/8da6f2c1-80dd-436b-9fd2-57a3b17eeb1c" />
</CardGroup>


# Google Cloud SDK Components gcloud CLI

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Development-CICD/Google-Cloud-SDK-Components-gcloud-CLI/page

Guide to Google Cloud SDK and gcloud CLI covering components, authentication, configuration, example commands, and best practices for automation, security, and multi project workflows

Hello everyone — welcome back.

In this lesson/article we dive into the Google Cloud SDK and its command-line interface, the gcloud CLI. This guide covers the core SDK components you’ll use most often, how to configure gcloud for day-to-day workflows, and example commands to get started quickly.

Key topics:

* Google Cloud SDK components and when to use them
* gcloud authentication and configuration best practices
* Example commands for common tasks
* Tips for automation and security

Why use gcloud? The CLI gives speed, repeatability, and automation — ideal for DevOps, data engineering, CI/CD pipelines, and interactive administration.

Components overview

| Component |                                                                                                                 Purpose | Example command                                                            |
| --------- | ----------------------------------------------------------------------------------------------------------------------: | -------------------------------------------------------------------------- |
| gcloud    |                             Primary CLI for managing Compute, Storage, Networking, IAM, Projects and other GCP services | `gcloud compute instances create vm-1`                                     |
| gsutil    |                                      Manage objects and buckets in Google Cloud Storage (GCS) — similar to AWS S3 tools | `gsutil cp file.txt gs://my-bucket/`                                       |
| bq        |                                                    BigQuery command-line tool for running queries and managing datasets | `bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM mydataset.mytable'` |
| kubectl   | Kubernetes CLI for managing clusters (including GKE) and workloads. Often installed via gcloud or an OS package manager | `kubectl get pods`                                                         |

<Frame>
  <img alt="A slide titled &#x22;Google Cloud SDK Components and gcloud CLI&#x22; showing four tool cards: gcloud, gsutil, bq, and kubectl. Each card has an icon and a short description of the tool's purpose (manage compute/storage, Cloud Storage, BigQuery, and Kubernetes respectively)." />
</Frame>

Core usage: authenticate and configure gcloud

Before running most gcloud commands you typically:

1. Authenticate your user or service account
2. Set the default project
3. Optionally set default compute region/zone

Authentication

* For interactive use, run:

```bash theme={null}
gcloud auth login
```

This opens a browser to sign in and stores credentials locally.

* For headless or scripted environments:

```bash theme={null}
gcloud auth login --no-launch-browser
```

* For service accounts (recommended for automation/CI):

```bash theme={null}
gcloud auth activate-service-account --key-file=KEY.json
```

* To obtain Application Default Credentials (for local code using Google client libraries):

```bash theme={null}
gcloud auth application-default login
```

<Callout icon="warning">
  Protect service account keys. Use Workload Identity (GKE) or short-lived credentials in CI when possible. Avoid committing `KEY.json` into source control.
</Callout>

Set the default project and region/zone

* Set your active project so you don’t need `--project` on every command:

```bash theme={null}
gcloud config set project PROJECT_ID
```

* Optionally set a default compute region or zone:

```bash theme={null}
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

These configurations tell gcloud which account and project to use and provide sensible defaults for resource creation.

Example: authenticate and configure, then create resources

```bash theme={null}
