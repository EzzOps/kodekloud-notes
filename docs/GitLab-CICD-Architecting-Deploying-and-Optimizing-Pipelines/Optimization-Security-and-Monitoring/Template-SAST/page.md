# .gitlab-ci.yml
.default_scripts: &default_scripts
  - ./default-script1.sh
  - ./default-script2.sh

job1:
  script:
    - *default_scripts
```

Or use GitLab’s custom reference tag:

```yaml theme={null}
# setup.yml
.setup:
  script:
    - echo "creating environment"

# .gitlab-ci.yml
include:
  - local: setup.yml

.teardown:
  after_script:
    - echo "deleting environment"

test:
  script:
    - !reference [.setup, script]
```

<Callout icon="lightbulb">
  YAML anchors work within the same file, while `!reference` can pull from hidden jobs or included files.
</Callout>

***

## 2. Preparing the Kubernetes Environment

Let’s define two hidden jobs: one for Node.js and one for Kubernetes deployment. We’ll attach an anchor (`&kubernetes_deploy_job`) to reuse the Kubernetes job’s `image` later.

```yaml theme={null}
variables:
  # Add global variables here…

.prepare_nodejs_environment:
  image: node:14
  script:
    - npm install

.prepare_deployment_environment: &kubernetes_deploy_job
  image:
    name: alpine:3.7
  dependencies: []
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    - chmod +x ./kubectl
    - mv ./kubectl /usr/bin/kubectl
    - apk add --no-cache gettext
    - envsubst --version
```

<Callout icon="triangle-alert">
  Make sure hidden jobs (prefixed with `.`) are not executed on their own—they only serve as references.
</Callout>

***

## 3. Two Almost-Identical Integration Tests

Consider two integration testing jobs—dev and staging. They share the same `image`, identical `before_script`, and `script` blocks:

```yaml theme={null}
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  needs:
    - k8s_stage_deploy
  before_script:
    - apk --no-cache add curl jq
  script:
    - echo "$INGRESS_URL"
    - curl -s -k "https://$INGRESS_URL/live"  | jq -r .status | grep -i live
    - curl -s -k "https://$INGRESS_URL/ready" | jq -r .status | grep -i ready

k8s_stage_deploy:
  stage: stage-deploy
  image: alpine:3.7
  needs:
    - k8s_dev_deploy
  before_script:
    - apk --no-cache add curl jq
  script:
    - echo "$INGRESS_URL"
    - curl -s -k "https://$INGRESS_URL/live"  | jq -r .status | grep -i live
    - curl -s -k "https://$INGRESS_URL/ready" | jq -r .status | grep -i ready
```

Rather than duplicating, let’s pull these blocks into new jobs via `!reference`.

***

## 4. Reusing the `image` Definition

We can reuse the `image` from `.prepare_deployment_environment` with:

```yaml theme={null}
k8s_dev_integration_testing:
  stage: dev-deploy
  image: !reference [.prepare_deployment_environment, image]
  needs:
    - k8s_dev_deploy
  before_script:
    - apk --no-cache add curl jq
  script:
    - echo "$INGRESS_URL"
    - curl -s -k "https://$INGRESS_URL/live"  | jq -r .status | grep -i live
    - curl -s -k "https://$INGRESS_URL/ready" | jq -r .status | grep -i ready

k8s_stage_integration_testing:
  stage: stage-deploy
  image: !reference [.prepare_deployment_environment, image]
  needs:
    - k8s_stage_deploy
  before_script:
    - apk --no-cache add curl jq
  script:
    - echo "$INGRESS_URL"
    - curl -s -k "https://$INGRESS_URL/live"  | jq -r .status | grep -i live
    - curl -s -k "https://$INGRESS_URL/ready" | jq -r .status | grep -i ready
```

Now, updating the base image in one place updates both jobs.

***

## 5. Reusing `before_script` and `script` Blocks

To avoid repeating `before_script` or `script`, reference the dev-integration job directly:

```yaml theme={null}
k8s_dev_integration_testing:
  stage: dev-deploy
  image: !reference [.prepare_deployment_environment, image]
  needs:
    - k8s_dev_deploy
  before_script:
    - apk --no-cache add curl jq
  script:
    - echo "$INGRESS_URL"
    - curl -s -k "https://$INGRESS_URL/live"  | jq -r .status | grep -i live
    - curl -s -k "https://$INGRESS_URL/ready" | jq -r .status | grep -i ready

k8s_stage_integration_testing:
  stage: stage-deploy
  image: !reference [.prepare_deployment_environment, image]
  needs:
    - k8s_stage_deploy
  before_script: !reference [k8s_dev_integration_testing, before_script]
  script:        !reference [k8s_dev_integration_testing, script]
```

This ensures both jobs stay in sync for setup and testing steps.

***

## 6. Full Snippet with Artifacts and Environment

For a consolidated pipeline, include artifacts and environment details alongside your reused blocks:

```yaml theme={null}
artifacts:
  reports:
    dotenv:
      - app_ingress_url.env

environment:
  name: staging
  url: "https://$INGRESS_URL"

k8s_stage_integration_testing:
  stage: stage-deploy
  image: !reference [.prepare_deployment_environment, image]
  needs:
    - k8s_stage_deploy
  before_script: !reference [k8s_dev_integration_testing, before_script]
  script:        !reference [k8s_dev_integration_testing, script]
```

***

## Conclusion

By combining standard YAML anchors (`&` / `*`) with GitLab’s custom `!reference` tags, you can effectively DRY up your CI/CD definitions. Pull in common `image`, `before_script`, or `script` sections from hidden or existing jobs—simplifying maintenance and reducing errors.

***

## Links and References

* [GitLab CI/CD Reference Tags](https://docs.gitlab.com/ee/ci/yaml/#reference)
* [GitLab CI/CD Anchors and Aliases](https://docs.gitlab.com/ee/ci/yaml/#anchors)
* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [jq JSON Processor](https://stedolan.github.io/jq/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/d5dc80da-3126-4680-87c6-a252357b9874" />
</CardGroup>


# Template SAST

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Template-SAST/page

Static Application Security Testing integrates into GitLab CI/CD to identify code vulnerabilities early, supporting various languages and manifest types before deployment.

## Overview

Static Application Security Testing (SAST) integrates directly into your GitLab CI/CD pipelines to catch code and manifest vulnerabilities early. It supports scanning source code, Kubernetes YAML, and Helm charts before deployment. While all GitLab plans can run SAST analyzers, Ultimate subscribers enjoy rich dashboards; free tiers can parse JSON reports.

<Frame>
  ![The image shows a GitLab documentation page about Static Application Security Testing (SAST), detailing its features and usage within GitLab CI/CD for detecting vulnerabilities. The sidebar includes navigation links related to application security and configuration.](https://kodekloud.com/kk-media/image/upload/v1752877405/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-sast-documentation-page.jpg)
</Frame>

## Supported Languages and Manifests

GitLab’s SAST documentation lists supported languages, frameworks, and manifest types. In JavaScript/Node.js projects, analyzers include [Semgrep](https://gitlab.com/gitlab-org/security-products/semgrep) and [NodeJsScan](https://gitlab.com/gitlab-org/security-products/nodejs-scan). Kubernetes YAML can be scanned with [KubeSec](https://gitlab.com/gitlab-org/security-products/kubesec).

<Frame>
  ![The image shows a GitLab documentation page listing various programming languages and frameworks, their corresponding analyzers for scanning, and the minimum supported GitLab version.](https://kodekloud.com/kk-media/image/upload/v1752877406/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-documentation-programming-languages.jpg)
</Frame>

## Available Analyzers

The following table summarizes core SAST analyzers:

| Analyzer   | Purpose                            | Installation / Notes             |
| ---------- | ---------------------------------- | -------------------------------- |
| NodeJsScan | Finds Node.js vulnerabilities      | `pip install njsscan==<version>` |
| Semgrep    | Pattern-based static checks        | Bundled in CI template           |
| KubeSec    | Analyzes Kubernetes manifest YAMLs | Bundled in CI template           |

<Frame>
  ![The image shows a GitLab repository page for the "kubesec analyzer," which performs SAST scanning on YAML files. It includes project details, versioning, contributing guidelines, and license information.](https://kodekloud.com/kk-media/image/upload/v1752877406/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-kubesec-analyzer-sast-yaml.jpg)
</Frame>

Each analyzer repository includes detailed scanning logic and JSON report schemas.

## Enabling SAST via CI/CD Template

GitLab’s built-in template `Jobs/SAST.gitlab-ci.yml` auto-detects languages and injects relevant jobs. To activate it:

```yaml theme={null}
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

External YAML files or local snippets can be added with the `include` keyword, streamlining long configurations and avoiding duplication.

<Frame>
  ![The image shows a GitLab documentation page about using the include keyword in CI/CD YAML configurations. It explains how to include external YAML files and lists possible inputs and additional details.](https://kodekloud.com/kk-media/image/upload/v1752877408/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-include-keyword-cicd-yaml.jpg)
</Frame>

GitLab also offers a **Browse templates** UI to select from all out-of-the-box CI/CD snippets.

<Frame>
  ![The image shows a GitLab repository interface with a list of YAML configuration files for various technologies, such as Julia, Laravel, and Python. The sidebar includes options like Issues, Merge requests, and Repository.](https://kodekloud.com/kk-media/image/upload/v1752877409/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-repo-yaml-configs-interface.jpg)
</Frame>

## Default SAST Jobs

The `Jobs/SAST.gitlab-ci.yml` template defines jobs like:

```yaml theme={null}
sast-analyzer:
  extends: sast
  allow_failure: true
  script:
    - echo "$CI_JOB_NAME is for pipeline configuration only"
    - exit 1

semgrep-sast:
  extends: sast-analyzer
  image: "$SAST_ANALYZER_IMAGE"
  variables:
    SAST_ANALYZER_IMAGE_TAG: "$SAST_ANALYZER_IMAGE_TAG"
  rules:
    - if: $SAST_DISABLED == 'true' || $SAST_DISABLED == '1'
      when: never
    - if: $SAST_EXCLUDED_ANALYZERS =~ /semgrep-sast/
      when: never
    - exists:
        - "**/*.js"
```

By default, SAST jobs run in the `test` stage and publish a JSON report at `gl-sast-report.json`:

```yaml theme={null}
sast:
  stage: test
  artifacts:
    reports:
      sast: gl-sast-report.json
  rules:
    - when: always
      allow_failure: true
    - changes:
        - "**/*.js"
        - "**/*.rb"
```

<Callout icon="lightbulb">
  All SAST jobs default to `allow_failure: true`, so pipelines won’t be blocked by detected issues.
</Callout>

## Customizing SAST Configuration

You can tweak the SAST template by setting CI variables:

```yaml theme={null}
variables:
  SCAN_KUBERNETES_MANIFESTS: "true"
```

This variable injects the `kubesec-sast` job. Additional options:

```yaml theme={null}
variables:
  SECURE_ANALYZERS_PREFIX: "$CI_TEMPLATE_REGISTRY_HOST/security-products"
  SAST_EXCLUDED_ANALYZERS: "nodejs-scan"
  SAST_EXCLUDED_PATHS: "spec,test,tmp"
```

## Adjusting the SAST Stage

To run SAST in a custom stage (for example, `.pre`):

```yaml theme={null}
stages:
  - .pre
  - test
  - deploy

include:
  - template: Jobs/SAST.gitlab-ci.yml

variables:
  SCAN_KUBERNETES_MANIFESTS: "true"

sast:
  stage: .pre
```

You can comment out unused templates:

```yaml theme={null}
