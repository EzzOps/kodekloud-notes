# Compute Engine
gcloud compute instances describe INSTANCE_NAME                       # Display VM instance details
gcloud compute instances list                                         # List VM instances
gcloud compute disks snapshot DISK_NAME --zone=ZONE                   # Create snapshot of a persistent disk
gcloud compute snapshots describe SNAPSHOT_NAME                       # Display a snapshot's details
gcloud compute snapshots delete SNAPSHOT_NAME                         # Delete a snapshot
gcloud compute ssh USER@INSTANCE_NAME --zone=ZONE                     # SSH to a VM instance

# App Engine / Serverless
gcloud app deploy                                                     # Deploy to App Engine
gcloud app versions list                                               # List App Engine versions
gcloud app browse                                                      # Open the current app in a browser
gcloud app create                                                      # Create an App Engine app
gcloud app logs read                                                   # Read App Engine logs

# Miscellaneous
gcloud kms decrypt --ciphertext-file CIPHERTEXT --plaintext-file PLAINTEXT  # Decrypt using KMS
gcloud logging logs list                                               # List logs
gcloud auth configure-docker                                          # Configure Docker credential helper
gcloud container clusters create CLUSTER_NAME --zone=ZONE              # Create a GKE cluster
gcloud container clusters list                                         # List GKE clusters
gcloud container clusters get-credentials CLUSTER_NAME --zone=ZONE     # Get kubectl credentials for a GKE cluster
gcloud container images list-tags IMAGE_NAME                           # List tags for a container image

# IAM & Service Accounts
gcloud iam list-grantable-roles --project=PROJECT_ID                  # List grantable IAM roles for a resource
gcloud iam roles create ROLE_ID --project=PROJECT_ID                  # Create a custom role
gcloud iam service-accounts create SA_NAME --project=PROJECT_ID       # Create a service account
gcloud iam service-accounts keys list --iam-account=SA_EMAIL         # List keys for a service account
```

> **lightbulb** Cloud Shell gives you a browser-based shell with the gcloud SDK preinstalled, so you don’t need to install anything locally. It is free to use with reasonable limits for development, but sessions are ephemeral — your home directory is persisted, but VM instances are temporary and idle sessions may be terminated.

Getting started with Cloud Shell

1. In the GCP Console click the Cloud Shell (terminal) button. The first start can take longer while the environment gets provisioned.
2. When Cloud Shell is ready you can run gcloud commands directly.

A sample Cloud Shell welcome looks like this:

```bash theme={null}
Welcome to Cloud Shell! Type "help" to get started.
Your Cloud Platform project in this session is set to kodekloud-gcp-training.
Use `gcloud config set project [PROJECT_ID]` to change to a different project.
skraghunandan11@cloudshell:~ (kodekloud-gcp-training)$
```

Verify the gcloud SDK is installed and view the version:

```bash theme={null}
skraghunandan11@cloudshell:~ (kodekloud-gcp-training)$ gcloud version
Google Cloud SDK 547.0.0
alpha 2025.11.07
app-engine-go 1.9.76
app-engine-java 3.0.1
app-engine-python 1.9.118
app-engine-python-extras 1.9.111
beta 2025.11.07
bq 2.1.25
bundled-python3-unix 3.13.7
cbt 1.24.1
cloud-datastore-emulator 2.3.1
cloud-run-proxy 0.5.0
core 2025.11.07
gsutil 5.35
kubectl 1.33.5
minikube 1.37.0
skaffold 2.16.0
...
skraghunandan11@cloudshell:~ (kodekloud-gcp-training)$
```

View current gcloud configuration

```bash theme={null}
gcloud config list
```

Set default project, zone, and region

* Set the default project:

```bash theme={null}
gcloud config set project kodekloud-gcp-training
# Output: Updated property [core/project].
```

* Set a default Compute Engine zone (example: `us-central1-a`):

```bash theme={null}
gcloud config set compute/zone us-central1-a
# Output: Updated property [compute/zone].
```

* Set a default region (example: `us-central1`):

```bash theme={null}
gcloud config set compute/region us-central1
# Output: Updated property [compute/region].
```

Authenticate the gcloud CLI

* Inside Cloud Shell you are usually already authenticated.
* From a local machine or other environment run:

```bash theme={null}
gcloud auth login
```

This opens a browser to sign in and prompts you to paste a verification code back into the terminal. Example interactive session:

```bash theme={null}
skraghunandan11@cloudshell:~ (kodekloud-gcp-training)$ gcloud auth login
You are already authenticated with gcloud when running inside the Cloud Shell and so do not need to run this command. Do you wish to proceed anyway?
Do you want to continue (Y/n)? Y

Go to the following link in your browser, and complete the sign-in prompts:
<oauth URL>

Once finished, enter the verification code provided in your browser:
# (paste verification code)
You are now logged in as [skraghunandan11@gmail.com].
Your current project is [kodekloud-gcp-training].
```

List projects you have access to

```bash theme={null}
gcloud projects list
```

Sample output:

```text theme={null}
PROJECT_ID: data-engineer-423808
NAME: data-engineer
PROJECT_NUMBER: 899718333449

PROJECT_ID: gen-lang-client-0787755513
NAME: Gemini API
PROJECT_NUMBER: 103855482290

PROJECT_ID: kodekloud-gcp-training
NAME: KodeKloud-GCP-Training
PROJECT_NUMBER: 240657367796
```

Note: you will only see projects for which your account has permission. Organization-level visibility and access depend on your IAM roles.

Interacting with Cloud Storage

Cloud Storage is comparable to Amazon S3. Common Storage commands:

* List buckets in the current project:

```bash theme={null}
gcloud storage buckets list
```

* List objects in a specific bucket:

```bash theme={null}
gcloud storage ls gs://dataproc-demo-kodekloud/
# Example output:
# gs://dataproc-demo-kodekloud/data/
# gs://dataproc-demo-kodekloud/jobs/
```

Can you build an entire infrastructure using gcloud?

Yes. The gcloud CLI can create service accounts, VPC networks and subnets, firewall rules, Compute Engine instances, GKE clusters, and more. In a follow-up demo we'll use gcloud to create an end-to-end set of resources from the command line.

Links and references

* [gcloud CLI cheat sheet (official)](https://cloud.google.com/sdk/docs/cheat-sheet)
* [Google Cloud SDK (installation & docs)](https://cloud.google.com/sdk/docs)
* [Cloud Shell overview](https://cloud.google.com/shell/docs)
* [Cloud Storage documentation](https://cloud.google.com/storage/docs)

That’s it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/02c15300-8e2a-455b-9032-0d4630391b66/lesson/3906d5a0-cdd5-4b76-bf42-98a51c59d724)


# Development and CICD Summary

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Development-CICD/Development-and-CICD-Summary/page

Guide summarizing using Google Cloud SDK and gcloud CLI, practicing commands, and using Cloud Build for automated CI/CD pipelines to build, test, and deploy applications to Cloud Run

Hello everyone — welcome back.\
Before we move on, here’s a concise, structured recap of deploying CI/CD on Google Cloud. This summary focuses on three core areas you’ll use most often: the Google Cloud SDK and its CLI, practicing the `gcloud` commands, and Cloud Build as the serverless CI/CD platform.

## 1) Google Cloud SDK and the gcloud CLI

The Google Cloud SDK is your primary toolbox for managing GCP. It bundles command-line utilities that let you configure projects, manage services, deploy applications, and inspect logs from the terminal. The `gcloud` command is the central interface for these tasks.

Why this matters:

* Centralized CLI reduces context switching between different consoles.
* Scripts and automation rely on `gcloud` for reproducible deployments and admin tasks.
* SDK includes specialized tools for common services.

Common SDK tools:

| Tool      | Purpose                                                       | Example                                                   |
| --------- | ------------------------------------------------------------- | --------------------------------------------------------- |
| `gcloud`  | Primary CLI for managing projects, IAM, deployments, and more | `gcloud config set project PROJECT_ID`                    |
| `gsutil`  | Cloud Storage operations (upload, download, list)             | `gsutil ls gs://my-bucket`                                |
| `bq`      | BigQuery queries and dataset/table management                 | `bq query 'SELECT COUNT(*) FROM `my\_dataset.my\_table`'` |
| `kubectl` | Kubernetes cluster management (GKE)                           | `kubectl get pods`                                        |

Install the SDK to get these tools locally and use them consistently across environments. See the official installation guide: [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

## 2) Practicing the gcloud CLI

Practice is essential — these are the commands you’ll use daily and during exams. Work through routine workflows (auth, project selection, storage, BigQuery, Kubernetes) until they become second nature.

Quick reference commands:

```bash theme={null}
