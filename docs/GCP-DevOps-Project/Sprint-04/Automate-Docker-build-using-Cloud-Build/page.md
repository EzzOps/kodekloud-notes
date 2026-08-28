# Automate Docker build using Cloud Build

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-04/Automate-Docker-build-using-Cloud-Build/page

Streamline Docker image builds using Google Cloud Build and Artifact Registry through automated configurations and monitoring.

Effortlessly streamline your Docker image builds by leveraging Google Cloud Build and storing the results in Google Artifact Registry. In this tutorial, you'll learn how to:

* Create a feature branch for isolation
* Configure a `cloudbuild.yaml` for automated builds
* Set up and verify a Cloud Build trigger
* Monitor builds in the Cloud Build dashboard
* Inspect Docker images in Artifact Registry

***

## 1. Create a New Git Branch

First, ensure you’re working in a dedicated feature branch. This keeps your `main` branch clean and allows safe testing of CI/CD changes.

```bash theme={null}
