# Extending development environment 01

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-07/Extending-development-environment-01/page

Learn to replicate your production CI/CD pipeline for a development branch using Google Cloud Build and GKE.

Welcome back! In this tutorial, you’ll learn how to replicate your production CI/CD pipeline for a **development** branch using Google Cloud Build and GKE. By the end, you’ll have:

* A dedicated `development` Git branch
* A customized `cloudbuild.yaml` for development
* A Cloud Build trigger that reacts to pushes on `development`
* Verification steps to confirm your `-dev` image lands in Container Registry

***

## 1. Create and Switch to the `development` Branch

First, make sure your local `main` branch is up to date:

```bash theme={null}
