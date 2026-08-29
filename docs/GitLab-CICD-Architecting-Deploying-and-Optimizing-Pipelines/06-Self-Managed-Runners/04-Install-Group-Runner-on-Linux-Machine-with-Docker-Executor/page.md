# Before: minimal Alpine image
FROM node:18-alpine3.11

# After: standard Debian-based Node.js
FROM node:18

WORKDIR /usr/app
COPY package*.json ./
RUN npm install
COPY . .
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder
EXPOSE 3000
CMD ["npm", "start"]
```

Commit to a feature branch to trigger the pipeline. You’ll see the Container Scanning job in the `containerization` stage.

![The image shows a GitLab CI/CD pipeline interface for a NodeJS project, displaying various stages such as pre, test, containerization, and dev-deploy, with job statuses indicated by checkmarks and icons.](https://kodekloud.com/kk-media/image/upload/v1752877399/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-cicd-nodejs-pipeline.jpg)

After completion, open the Container Scanning log to view the summary table or raw output.

![The image shows a GitLab interface displaying a job log with details about a pipeline run, including a highlighted security warning related to a CVE vulnerability.](https://kodekloud.com/kk-media/image/upload/v1752877400/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-job-log-pipeline-cve-warning.jpg)

Additional deployment jobs will follow.

![The image shows a GitLab CI/CD pipeline interface for a NodeJS project, displaying various stages and jobs such as code quality checks, testing, containerization, and deployment. Each job has a status indicator, with some marked as successful and others needing attention.](https://kodekloud.com/kk-media/image/upload/v1752877401/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-cicd-nodejs-pipeline-2.jpg)

## 7. Inspecting the Reports

### 7.1 JSON Vulnerability Report

The `gl-container-scanning-report.json` artifact lists vulnerabilities in structured JSON:

```json theme={null}
{
  "vulnerabilities": [
    {
      "id": "de666e5aa0b170e90b8d7018c398ba76c577c",
      "severity": "Low",
      "location": {
        "dependency": {
          "package": {
            "name": "apt",
            "version": "2.6.1"
          },
          "image": "docker.io/siddharth67/solar-system:1165883818"
        }
      },
      "identifiers": [
        { "type": "cve", "name": "CVE-2011-3374" }
      ],
      "description": "apt-key in apt, all versions, do not correctly validate gpg keys, leading to a potential MITM attack."
    }
  ]
}
```

![The image shows a GitLab documentation page about JSON report formats and CycloneDX Software Bill of Materials related to container scanning. It includes navigation links and text explaining the report formats and integration.](https://kodekloud.com/kk-media/image/upload/v1752877402/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-json-report-cyclonedx-bom.jpg)

### 7.2 CycloneDX SBOM

The SBOM artifact follows the CycloneDX spec:

```json theme={null}
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "component": {
    "type": "container",
    "name": "docker.io/siddharth67/solar-system",
    "version": "1.1.1"
  },
  "tools": [
    { "vendor": "aquasecurity", "name": "trivy", "version": "0.48.3" }
  ]
}
```

![The image shows a GitLab documentation page about CycloneDX Software Bill of Materials, security dashboards, and vulnerabilities databases. It includes a sidebar with navigation options related to security and scanning features.](https://kodekloud.com/kk-media/image/upload/v1752877403/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-cyclonedx-software-bom.jpg)

***

## Links and References

* [GitLab Container Scanning Documentation](https://docs.gitlab.com/ee/user/application_security/container_scanning/)
* [Trivy Scanner on GitLab](https://docs.gitlab.com/ee/user/application_security/trivy/)
* [OWASP CycloneDX Specification](https://cyclonedx.org/)
* [GitLab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)

You now have a fully configured Container Scanning pipeline with vulnerability reports and SBOM output. Integrate additional scanners (Dependency, SAST, DAST) as needed based on your security requirements.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/d56895c9-c00b-41c8-9500-1081bdce8e40)


# Install Group Runner on Linux Machine with Docker Executor

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Self-Managed-Runners/Install-Group-Runner-on-Linux-Machine-with-Docker-Executor/page

This guide explains how to install and configure a group-level GitLab runner on a Linux machine using Docker.

Enable all projects in a GitLab group to share a single runner powered by Docker. This guide walks you through creating a **group-level runner**, registering it on a Linux host, and verifying its status.

## Table of Contents

1. [Create a Group-Level Runner](#1-create-a-group-level-runner)
2. [Register the Runner on Your Linux Host](#2-register-the-runner-on-your-linux-host)
3. [Check Runner Status in GitLab](#3-check-runner-status-in-gitlab)
4. [Review the Runner Configuration](#4-review-the-runner-configuration)
5. [Verify Runner in a Project](#5-verify-runner-in-a-project)
6. [Links and References](#6-links-and-references)

***

## 1. Create a Group-Level Runner

1. Sign in to GitLab and navigate to your target group (e.g., `demos`).
2. In the left sidebar, select **CI/CD > Runners**.
3. Under **Group runners**, click **New group runner**.
4. Enter the runner details:

   | Field               | Value                             |
   | ------------------- | --------------------------------- |
   | Runner description  | Docker executor with AWS on Linux |
   | Tags                | `docker`, `aws`, `linux`          |
   | Maximum job timeout | 10 minutes                        |

![The image shows a GitLab interface for creating a group runner, with options for configuring containers, tags, and runner settings. The "Runner description" field is being filled with "Docker Execu".](https://kodekloud.com/kk-media/image/upload/v1752877413/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Group-Runner-on-Linux-Machine-with-Docker-Executor/gitlab-group-runner-configuration.jpg)

5. Click **Create runner**. GitLab will display a **registration token**—copy it for the next step.

![The image shows a GitLab interface for creating a new group runner, with options to add tags, configure settings, and set a maximum job timeout. The "Create runner" button is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752877414/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Group-Runner-on-Linux-Machine-with-Docker-Executor/gitlab-create-group-runner-interface.jpg)

> **triangle-alert** Keep your registration token secure. Anyone with this token can register additional runners to your group.

## 2. Register the Runner on Your Linux Host

If GitLab Runner is not yet installed, install and start it as a system service:

```bash theme={null}
