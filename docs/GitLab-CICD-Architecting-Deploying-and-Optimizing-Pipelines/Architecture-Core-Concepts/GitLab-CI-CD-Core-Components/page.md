# … plus over 100 more variables
```

<Callout icon="triangle-alert">
  Running `export` will print all environment variables, including sensitive tokens. Ensure your job logs are protected.
</Callout>

### 2.2 generic\_predefined\_variables

This job echoes commonly used variables to illustrate dynamic scripting:

```bash theme={null}
$ echo "GITLAB_USER_LOGIN = $GITLAB_USER_LOGIN"
GITLAB_USER_LOGIN = sidd-harth

$ echo "GITLAB_USER_EMAIL = $GITLAB_USER_EMAIL"
GITLAB_USER_EMAIL = barahalikar.siddharth@gmail.com

$ echo "CI_COMMIT_AUTHOR = $CI_COMMIT_AUTHOR"
CI_COMMIT_AUTHOR = Barahalikar Siddharth <barahalikar.siddharth@gmail.com>

$ echo "CI_COMMIT_BRANCH = $CI_COMMIT_BRANCH"
CI_COMMIT_BRANCH = main

$ echo "CI_PROJECT_NAME = $CI_PROJECT_NAME"
CI_PROJECT_NAME = predefined-variables

$ echo "CI_PROJECT_URL = $CI_PROJECT_URL"
CI_PROJECT_URL = https://gitlab.com/demos-group/predefined-variables

$ echo "CI_JOB_STAGE = $CI_JOB_STAGE"
CI_JOB_STAGE = test

$ echo "CI_PIPELINE_ID = $CI_PIPELINE_ID"
CI_PIPELINE_ID = 1154671161

$ echo "CI_PIPELINE_SOURCE = $CI_PIPELINE_SOURCE"
CI_PIPELINE_SOURCE = push
```

Use these variables to customize your jobs based on commit metadata and pipeline context.

### 2.3 merge\_request\_predefined\_variables

This job attempts to print merge-request–specific variables:

```bash theme={null}
$ echo "CI_MERGE_REQUEST_LABELS = $CI_MERGE_REQUEST_LABELS"
CI_MERGE_REQUEST_LABELS = 

$ echo "CI_MERGE_REQUEST_TARGET_BRANCH_NAME = $CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
CI_MERGE_REQUEST_TARGET_BRANCH_NAME = 

$ echo "CI_MERGE_REQUEST_ASSIGNEES = $CI_MERGE_REQUEST_ASSIGNEES"
CI_MERGE_REQUEST_ASSIGNEES = 

$ echo "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME = $CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"
CI_MERGE_REQUEST_SOURCE_BRANCH_NAME = 

$ echo "CI_MERGE_REQUEST_TITLE = $CI_MERGE_REQUEST_TITLE"
CI_MERGE_REQUEST_TITLE = 
```

<Callout icon="lightbulb">
  Merge request variables are only populated in pipelines triggered by Merge Requests. In direct pushes, these remain empty.
</Callout>

For more on Merge Request CI/CD variables, see the [GitLab Merge Request Variables documentation][2].

<Frame>
  ![The image shows a GitLab documentation page detailing predefined variables for merge request pipelines, including variable names, GitLab versions, runners, and descriptions. The sidebar on the left lists various sections related to CI/CD variables.](https://kodekloud.com/kk-media/image/upload/v1752876991/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Predefined-CICD-Variables/gitlab-merge-request-pipeline-variables.jpg)
</Frame>

***

## Links and References

* [GitLab Predefined CI/CD Variables][1]
* [Merge Request CI/CD Variables][2]
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)

[1]: https://docs.gitlab.com/ee/ci/variables/predefined_variables.html

[2]: https://docs.gitlab.com/ee/ci/variables/predefined_variables.html#merge-request-cicd-variables

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/6fdc7c8c-95b5-41ca-8474-3cf9c4101757" />
</CardGroup>


# GitLab CI CD Core Components

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/GitLab-CI-CD-Core-Components/page

This guide explores GitLab CI/CD components—Pipeline, Stages, Jobs, and Scripts—to automate testing, building, and deployment with a focus on configuration.

In this guide, we’ll dive into the four essential GitLab CI/CD building blocks—**Pipeline**, **Stages**, **Jobs**, and **Scripts**—and show you how they collaborate to automate testing, building, and deployment. By the end, you’ll have a clear understanding of how to configure a robust `.gitlab-ci.yml` and choose the right pipeline type for your workflow.

## CI/CD Core Components Overview

| Component | Description                                             |
| --------- | ------------------------------------------------------- |
| Pipeline  | Automated process orchestrating jobs and stages         |
| Stage     | Logical group of jobs (e.g., `build`, `test`, `deploy`) |
| Job       | Individual unit of work that runs on a runner           |
| Script    | Shell commands executed by a job                        |

## Pipeline

A **pipeline** is defined via a `.gitlab-ci.yml` file at the root of your repo and represents the blueprint for your CI/CD workflow.

<Callout icon="lightbulb">
  Ensure your `.gitlab-ci.yml` lives in the repository root; otherwise GitLab won’t detect it.\
  See [GitLab CI/CD YAML reference][gitlab-ci-yaml].
</Callout>

Key points:

* **Definition**: YAML file named `.gitlab-ci.yml`.
* **Naming**: Use `workflow:name` to assign a custom name shown in the Pipelines tab.
* **Triggers**: Pipelines start on `push`, `merge_request`, `schedule`, or manual actions.
* **Conditions**: Use `rules` to control when pipelines run.

Example: Run pipeline only on commits to `main`

```yaml theme={null}
workflow:
  name: My Awesome App Pipeline
  rules:
    - if: $CI_COMMIT_BRANCH == 'main'
```

## Jobs

A **job** is the fundamental execution unit in a pipeline:

* **Execution**: Runs on a GitLab Runner (shared or self-hosted).
* **Runner selection**: Use `tags` to pick specific runners.
* **Stage assignment**: Each job belongs to a defined stage.

Example: Selecting a specific runner

```yaml theme={null}
unit_test_job:
  stage: test
  tags:
    - saas-linux-small-amd64
```

<Callout icon="triangle-alert">
  Keep sensitive data out of `script` blocks. Use [CI/CD variables][gitlab-ci-variables] for secrets like tokens or credentials.
</Callout>

## Scripts

The `script` section lists shell commands executed by the job:

* **Sequential execution**: Commands run in order.
* **Common use cases**: Install dependencies, build code, run tests, deploy artifacts, perform security scans.
* **Before/after hooks**:
  * `before_script`: Setup steps (e.g., install Node.js, configure DB).
  * `after_script`: Cleanup tasks (e.g., remove temp files).

```yaml theme={null}
before_script:
  - echo "Setting up environment"
script:
  - npm install
  - npm test
after_script:
  - echo "Cleaning up"
```

## Example `.gitlab-ci.yml`

Here’s a complete sample that defines two stages—`test` and `deploy`—and a workflow rule:

```yaml theme={null}
workflow:
  name: My Awesome App Pipeline
  rules:
    - if: $CI_COMMIT_BRANCH == 'main'

stages:
  - test
  - deploy

unit_test_job:
  stage: test
  tags:
    - saas-linux-small-amd64
  before_script:
    - echo "Install NodeJS"
  script:
    - npm install
    - npm test
  after_script:
    - echo "Tests complete"

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production..."
```

In this configuration:

* The pipeline runs only on `main`.
* The **test** stage executes `unit_test_job` with setup, tests, and teardown.
* The **deploy** stage runs `deploy_job` after successful tests.

## Stages

**Stages** define the sequence of execution in a pipeline. Jobs within the same stage run in parallel. Common stages include:

| Stage    | Purpose                             | Example Commands               |
| -------- | ----------------------------------- | ------------------------------ |
| build    | Compile or assemble code            | `mvn package`, `docker build`  |
| test     | Execute automated tests             | `npm test`, `pytest`           |
| deploy   | Release artifacts to an environment | `kubectl apply`, `aws s3 sync` |
| security | Run vulnerability scans             | `trivy image`, `npm audit`     |

## Pipeline Types

<Frame>
  ![The image lists different types of pipelines, including Basic Pipeline, DAG Pipeline, Merge Request Pipelines, Merged Results Pipelines, Merge Trains, Parent-Child Pipelines, and Multi-Project Pipelines. Each type is displayed in a colored box with an icon.](https://kodekloud.com/kk-media/image/upload/v1752876992/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-GitLab-CI-CD-Core-Components/pipeline-types-list-icons.jpg)
</Frame>

Choose the pipeline type that best suits your project complexity and team structure:

| Pipeline Type           | Description                                                                      |
| ----------------------- | -------------------------------------------------------------------------------- |
| Basic Pipeline          | Executes all jobs in each stage concurrently, then proceeds sequentially.        |
| DAG Pipeline            | Runs jobs based on explicit dependencies for maximum parallelism and efficiency. |
| Merge Request Pipeline  | Validates new changes in merge requests before merging.                          |
| Merged Results Pipeline | Tests the merged result of a MR to catch conflicts early.                        |
| Merge Train             | Queues MRs in sequence to streamline integration.                                |
| Parent-Child Pipelines  | Splits large pipelines into parent and child configs—ideal for monorepos.        |
| Multi-Project Pipelines | Coordinates pipelines across multiple repositories for cross-team workflows.     |

***

## Links and References

* [GitLab CI/CD Documentation][gitlab-ci-docs]
* [GitLab CI/CD YAML Reference][gitlab-ci-yaml]
* [CI/CD Variables in GitLab][gitlab-ci-variables]

[gitlab-ci-docs]: https://docs.gitlab.com/ee/ci/

[gitlab-ci-yaml]: https://docs.gitlab.com/ee/ci/yaml/

[gitlab-ci-variables]: https://docs.gitlab.com/ee/ci/variables/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/90cda5c4-fd27-4580-ae35-eadb55b8e934" />
</CardGroup>
