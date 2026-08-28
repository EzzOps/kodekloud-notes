# Template Container Scanning

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Template-Container-Scanning/page

This article explains how to implement Container Scanning in GitLab CI/CD to identify vulnerabilities in Docker images.

Container Scanning is a critical part of Software Composition Analysis (SCA), inspecting Docker images and their base layers for known vulnerabilities. GitLab CI/CD offers a free Container Scanning template—powered by Trivy by default (or GRype)—to help you keep your images secure.

<Frame>
  ![The image shows a GitLab documentation page about container scanning, detailing integration with open-source tools for vulnerability analysis. It includes navigation links on the left and an overview section in the main content area.](https://kodekloud.com/kk-media/image/upload/v1752877392/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-container-scanning-documentation.jpg)
</Frame>

## 1. Enabling Container Scanning

Add the built-in Container Scanning template to your `.gitlab-ci.yml`:

```yaml theme={null}
include:
  - template: Jobs/Build.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

container_scanning:
  variables:
    CS_DEFAULT_BRANCH_IMAGE: $CI_REGISTRY_IMAGE/$CI_DEFAULT_BRANCH:$CI_COMMIT_SHA
```

<Callout icon="lightbulb">
  By default, the `container_scanning` job runs in the `test` stage. Override `CS_DEFAULT_BRANCH_IMAGE` to scan a different image tag.
</Callout>

### 1.1 Scanning Remote Images

Override `CS_IMAGE` and log level:

```yaml theme={null}
include:
  - template: Security/Container-Scanning.gitlab-ci.yml

variables:
  SECURE_LOG_LEVEL: debug

container_scanning:
  variables:
    CS_IMAGE: example.com/user/image:tag
```

### 1.2 Authenticating to a Private Registry

If your registry requires authentication, log in during `before_script` and supply credentials as CI variables:

```yaml theme={null}
container_scanning:
  before_script:
    - apk add --no-cache python3 py3-pip
    - pip3 install awscli
    - export AWS_ECR_PASSWORD=$(aws ecr get-login-password --region us-east-1)
    - docker login -u AWS -p "$AWS_ECR_PASSWORD" <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
  include:
    - template: Security/Container-Scanning.gitlab-ci.yml
  variables:
    CS_IMAGE: <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/<image>:<tag>
    CS_REGISTRY_USER: AWS
    CS_REGISTRY_PASSWORD: "$AWS_ECR_PASSWORD"
    AWS_DEFAULT_REGION: us-east-1
```

## 2. Container Scanning CI/CD Variables

These variables control which image is scanned and how verbose the logs are:

| Variable                   | Default                                                    | Description                           |
| -------------------------- | ---------------------------------------------------------- | ------------------------------------- |
| CS\_DEFAULT\_BRANCH\_IMAGE | `$CI_REGISTRY_IMAGE/$CI_DEFAULT_BRANCH:$CI_COMMIT_SHA`     | Image tag for default branch          |
| CS\_IMAGE                  | —                                                          | Custom image:tag to scan              |
| CS\_REGISTRY\_USER         | —                                                          | Username for private registry         |
| CS\_REGISTRY\_PASSWORD     | —                                                          | Password/token for registry login     |
| SECURE\_LOG\_LEVEL         | info                                                       | Log verbosity (`debug` or `info`)     |
| CS\_ANALYZER\_IMAGE        | `$CI_TEMPLATE_REGISTRY_HOST/.../container-scanning:latest` | Analyzer container used for scanning  |
| CS\_SCHEMA\_MODEL          | —                                                          | Schema version of the scanning output |

<Frame>
  ![The image shows a GitLab documentation page detailing available CI/CD variables for container scanning, including variable names, defaults, descriptions, and associated scanners.](https://kodekloud.com/kk-media/image/upload/v1752877393/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-ci-cd-variables-container-scanning.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab documentation page about container scanning, detailing CI/CD variables and their descriptions. The sidebar on the left lists various security and scanning options.](https://kodekloud.com/kk-media/image/upload/v1752877394/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-container-scanning-docs.jpg)
</Frame>

## 3. Allowlisting Vulnerabilities

To ignore specific CVEs, add a `vulnerabilities-allowlist.yaml` in your repo:

```yaml theme={null}
generalAllowlist:
  CVE-2019-8696:
  CVE-2014-8166: cups
  CVE-2017-18248:

images:
  registry.gitlab.com/gitlab-org/security-products/dast/webgoat-8.0@sha256:
    CVE-2018-4180:
  your.private.registry:5000/centos:
    CVE-2015-1419: libxml2
    CVE-2015-1447:
```

<Callout icon="triangle-alert">
  Allowlisting will mark these CVEs as approved and they will not fail your pipeline. Use with caution!
</Callout>

<Frame>
  ![The image shows a GitLab documentation page about container scanning job log format, displaying a table of found vulnerabilities with details like status, CVE severity, package name, and version.](https://kodekloud.com/kk-media/image/upload/v1752877395/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-container-scanning-job-log.jpg)
</Frame>

## 4. CycloneDX SBOM Output

Container Scanning also generates a CycloneDX SBOM artifact (`gl-sbom-*.cdx.json`), following the OWASP standard for Software Bill of Materials.

<Frame>
  ![The image shows a GitLab documentation page about CycloneDX Software Bill of Materials and container scanning, including sections on the security dashboard and vulnerabilities database.](https://kodekloud.com/kk-media/image/upload/v1752877397/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-cyclonedx-sbom-scanning.jpg)
</Frame>

## 5. Integrating into a Full Pipeline

Below is an example `.gitlab-ci.yml` snippet that combines build, SAST, secret detection, and container scanning:

```yaml theme={null}
stages:
  - .pre
  - test
  - containerization
  - dev-deploy
  - stage-deploy

include:
  - component: gitlab.com/gitlab-components/code-quality/code-quality@1.0
  - template: Jobs/SAST.gitlab-ci.yml
  - component: gitlab.com/gitlab-components/secret-detection/secret-detection@1.0
  - template: Security/Container-Scanning.gitlab-ci.yml

variables:
  DOCKER_USERNAME: siddharth67
  IMAGE_VERSION: "$CI_PIPELINE_ID"
  DOCKER_IMAGE: $DOCKER_USERNAME/solar-system:$IMAGE_VERSION
  CS_ANALYZER_IMAGE: "$CI_TEMPLATE_REGISTRY_HOST/security-products/container-scanning:6"
  CS_SCHEMA_MODEL: 15

container_scanning:
  stage: containerization
  needs:
    - docker_push
  image: "$CS_ANALYZER_IMAGE$CS_IMAGE_SUFFIX"
  variables:
    CS_IMAGE: docker.io/$DOCKER_USERNAME/solar-system:$IMAGE_VERSION
    GIT_STRATEGY: none
    allow_failure: true
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json
      cyclonedx: "**/gl-sbom-*.cdx.json"
```

<Frame>
  ![The image shows a GitLab Pipeline Editor interface with a visual representation of a CI/CD pipeline, including stages like "pre," "test," "containerization," "dev-deploy," and "stage-deploy," each containing various tasks. The left sidebar displays navigation options such as "Merge requests," "Manage," "Plan," and "Code."](https://kodekloud.com/kk-media/image/upload/v1752877398/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-Container-Scanning/gitlab-pipeline-editor-cicd-diagram.jpg)
</Frame>

## 6. Demo: Generating Vulnerabilities

To demonstrate detection, switch your `Dockerfile` from Alpine to Debian:

```dockerfile theme={null}
