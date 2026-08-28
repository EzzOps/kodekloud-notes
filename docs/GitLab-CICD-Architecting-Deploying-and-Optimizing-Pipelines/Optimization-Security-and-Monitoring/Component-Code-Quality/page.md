# Define a reusable scripts list
.default_scripts: &default_scripts
  - ./default-script1.sh
  - ./default-script2.sh

job1:
  script:
    - *default_scripts       # Reuse the list of default scripts
    - ./job-script.sh
```

| Feature           | Syntax  | Description                            |
| ----------------- | ------- | -------------------------------------- |
| Anchor definition | `&name` | Assigns a name to a block              |
| Anchor reference  | `*name` | Inserts the content of the named block |

## Merging Entire Job Configurations

You can reuse a full job template by defining it as a hidden job and then merging it into other jobs:

```yaml theme={null}
.job_template: &job_configuration
  image: ruby:2.6
  services:
    - postgres
    - redis

test1:
  <<: *job_configuration
  script:
    - echo "Running test1"

test2:
  <<: *job_configuration
  script:
    - echo "Running test2"
```

Here, `test1` and `test2` inherit `image: ruby:2.6` and the two services from the hidden `.job_template`.

## Combining Multiple Anchors

You can break a job template into smaller anchors—for example, separate anchors for `script`, `services`, or `tags`—and then merge only the pieces you need:

```yaml theme={null}
.job_template: &job_configuration
  script:
    - echo "Test project"
  tags:
    - dev

.postgres_services:
  services: &postgres_configuration
    - postgres
    - ruby

.mysql_services:
  services: &mysql_configuration
    - mysql
    - ruby

test_postgres:
  <<: *job_configuration
  services: *postgres_configuration
  tags:
    - postgres

test_mysql:
  <<: *job_configuration
  services: *mysql_configuration
```

In this example, `test_postgres` inherits the base `script` and `tags`, then overrides `services`.

## Real-World Pipeline: Reusing Deployment Configuration

Both `k8s_dev_deploy` and `k8s_stage_deploy` share:

* `alpine:3.7` as the job image
* No dependencies
* Identical `before_script` steps to install `kubectl` and `gettext`

Define a hidden job template with an anchor:

```yaml theme={null}
.prepare_deployment_environment: &kubernetes_deploy_job
  image:
    name: alpine:3.7
  dependencies: []
  before_script:
    - wget "https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - \
       https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
    - chmod +x ./kubectl
    - mv ./kubectl /usr/bin/kubectl
    - apk add --no-cache gettext
    - envsubst -V
```

### Dev Deploy Job

```yaml theme={null}
k8s_dev_deploy:
  <<: *kubernetes_deploy_job
  stage: dev-deploy
  needs:
    - docker_push
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - kubectl version -o yaml
    - kubectl config get-contexts
    - kubectl get nodes
    - export INGRESS_IP=$(kubectl -n ingress-nginx \
        get services ingress-nginx-controller \
        -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - echo $INGRESS_IP
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI=$MONGO_URI \
        --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
        --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
        --save-config --dry-run=client -o yaml | kubectl apply -f -
```

### Stage Deploy Job

```yaml theme={null}
k8s_stage_deploy:
  <<: *kubernetes_deploy_job
  stage: stage-deploy
  when: manual
  script:
    - temp_kube_config_file=$(printenv KUBECONFIG)
    - cat $temp_kube_config_file
    - kubectl config get-contexts
    - kubectl config use-context demos-group/solar-system:kk-gitlab-agent
    - kubectl get po -A
    - export INGRESS_IP=$(kubectl -n ingress-nginx \
        get services ingress-nginx-controller \
        -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - echo $INGRESS_IP
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI=$MONGO_URI \
        --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
        --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
        --save-config --dry-run=client -o yaml | kubectl apply -f -
```

Now both deployment jobs inherit the same `image`, `dependencies`, and `before_script` steps without duplication.

<Frame>
  ![The image shows a GitLab interface displaying the "Environments" section with active environments for "development" and "staging," including deployment details and options to open or stop them.](https://kodekloud.com/kk-media/image/upload/v1752877327/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Anchors-Reuse-Configuration-Deployment-Jobs/gitlab-environments-development-staging.jpg)
</Frame>

## Visualizing the Pipeline

On the **CI/CD > Pipelines** page or the **Visualization** tab, confirm that:

* `k8s_dev_deploy` runs immediately after `docker_push` thanks to `needs:`
* `k8s_stage_deploy` is manual (`when: manual`)
* Both jobs share the anchored configuration

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a NodeJS project, displaying stages like containerization, dev-deploy, and stage-deploy with their respective jobs.](https://kodekloud.com/kk-media/image/upload/v1752877327/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Anchors-Reuse-Configuration-Deployment-Jobs/gitlab-cicd-nodejs-pipeline.jpg)
</Frame>

## Further Reading & References

* [GitLab CI/CD YAML Anchors](https://docs.gitlab.com/ee/ci/yaml/#anchors-and-aliases)
* [GitLab Pipeline Configuration](https://docs.gitlab.com/ee/ci/pipelines/)
* [Kubernetes Official Documentation](https://kubernetes.io/docs/)

That’s how you can use YAML anchors in GitLab CI/CD to keep your deployment jobs DRY and maintainable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/62acf9ad-5d44-430a-a7a0-6dfb8fd2ecee" />
</CardGroup>


# Component Code Quality

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Component-Code-Quality/page

Optimize CI/CD workflows with GitLab’s Code Quality analysis to enhance source code quality by detecting issues and ensuring high-quality changes.

Optimize your CI/CD workflow by integrating GitLab’s Code Quality analysis. This component scans your source code for complexity, duplication, style issues, and maintainability risks—helping your team merge only high-quality changes.

<Frame>
  ![The image shows a GitLab documentation page about "Code Quality," detailing its features, tiers, and usage for analyzing source code quality and complexity. The sidebar and main content provide navigation and information on related topics.](https://kodekloud.com/kk-media/image/upload/v1752877340/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-code-quality-documentation.jpg)
</Frame>

## Why Code Quality Matters

* Detects potential bugs and anti-patterns early
* Tracks complexity and duplication over time
* Enforces coding standards and style guidelines
* Integrates seamlessly with merge requests for inline review

## How It Works

GitLab’s built-in Code Quality template leverages the open-source [Code Climate](https://codeclimate.com/) engine plus additional scanners. It produces a JSON (or HTML) report consumed by GitLab to annotate merge requests and pipeline views.

<Frame>
  ![The image shows a webpage from Code Climate listing supported programming languages for maintainability checks, including Ruby, Python, PHP, JavaScript, and others. It also mentions support for third-party plugins.](https://kodekloud.com/kk-media/image/upload/v1752877341/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/code-climate-supported-languages.jpg)
</Frame>

<Callout icon="lightbulb">
  Verify your project’s language is supported by Code Climate before enabling the component.
</Callout>

## Feature Comparison by GitLab Tier

Different GitLab subscriptions unlock advanced Code Quality capabilities:

| GitLab Tier | Key Features                                       |
| ----------- | -------------------------------------------------- |
| Free        | Basic maintainability and style checks             |
| Premium     | Custom scanner configuration, report artifacts     |
| Ultimate    | Quality dashboard, advanced analytics, MR insights |

<Frame>
  ![The image shows a GitLab documentation page detailing features available per tier (Free, Premium, Ultimate) for code quality. It includes a table listing features like configuring scanners and generating report artifacts, with a sidebar for navigation.](https://kodekloud.com/kk-media/image/upload/v1752877342/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-code-quality-features-table.jpg)
</Frame>

### Merge Request Inline Reports

Once enabled, Code Quality issues surface directly in the Merge Request widget—categorized by severity and file location.

<Frame>
  ![The image shows a GitLab documentation page about the "Merge request widget" for code quality analysis. It includes a list of code quality issues with their severity levels and file locations.](https://kodekloud.com/kk-media/image/upload/v1752877343/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-merge-request-widget-code-quality.jpg)
</Frame>

For example, a simple JavaScript function:

```javascript theme={null}
function init() {
  return 'foo';
  debugger;
}
```

Code Climate flags the unused `debugger;` statement as an issue.

## 1. Enable Code Quality in Your CI Configuration

Add the official GitLab CI/CD component at the top of your `.gitlab-ci.yml`:

```yaml theme={null}
include:
  - component: gitlab.com/gitlab-components/code-quality/code-quality@1.0
```

GitLab CI/CD components are reusable jobs and templates. Browse the [CI/CD Catalog][catalog-docs] (beta) to discover 99 components.

<Frame>
  ![The image shows a GitLab documentation page about the CI/CD Catalog, detailing its tiers, offerings, and status, along with instructions on how to view and publish component projects.](https://kodekloud.com/kk-media/image/upload/v1752877345/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-cicd-catalog-documentation.jpg)
</Frame>

In the Pipeline Editor, search for **code-quality**:

```yaml theme={null}
workflow: …
stages: …
variables: …
unit_testing: …
docker_build: …
