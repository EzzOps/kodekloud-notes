# Demo Create Shared Library for Trivy Scan

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Shared-Libraries-in-Jenkins/Demo-Create-Shared-Library-for-Trivy-Scan/page

This tutorial guides you in creating a Jenkins Shared Library for running Trivy vulnerability scans in CI/CD pipelines.

In this tutorial, you’ll build a reusable Jenkins Shared Library to run [Trivy](https://github.com/aquasecurity/trivy) scans in your CI/CD pipelines. By isolating scanning logic in a library, you’ll eliminate duplication and enable versioned updates via Git feature branches.

## Prerequisites

| Requirement                 | Description                                           |
| --------------------------- | ----------------------------------------------------- |
| Jenkins Shared Library Repo | A Git repository to host your `vars/` functions       |
| Trivy CLI                   | Installed on your Jenkins agents or build environment |

## 1. Clone the Shared Library Repository

Start by cloning your existing shared-library project:

```bash theme={null}
git clone http://64.227.187.25:5555/dasher-org/shared-libraries.git
cd shared-libraries
ls
