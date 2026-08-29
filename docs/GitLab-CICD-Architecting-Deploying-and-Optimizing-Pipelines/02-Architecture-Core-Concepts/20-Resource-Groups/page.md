# .gitlab-ci.yml
stages:
  - test

generic_predefined_variables:
  stage: test
  script:
    - echo "GITLAB_USER_LOGIN         = $GITLAB_USER_LOGIN"
    - echo "GITLAB_USER_EMAIL         = $GITLAB_USER_EMAIL"
    - echo "CI_COMMIT_AUTHOR          = $CI_COMMIT_AUTHOR"
    - echo "CI_COMMIT_BRANCH          = $CI_COMMIT_BRANCH"
    - echo "CI_PROJECT_NAME           = $CI_PROJECT_NAME"
    - echo "CI_PROJECT_URL            = $CI_PROJECT_URL"
    - echo "CI_JOB_STAGE              = $CI_JOB_STAGE"
    - echo "CI_PIPELINE_NAME          = $CI_PIPELINE_NAME"
    - echo "CI_PIPELINE_ID            = $CI_PIPELINE_ID"
    - echo "CI_PIPELINE_SOURCE        = $CI_PIPELINE_SOURCE"

merge_request_predefined_variables:
  stage: test
  script:
    - echo "CI_MERGE_REQUEST_LABELS              = $CI_MERGE_REQUEST_LABELS"
    - echo "CI_MERGE_REQUEST_TARGET_BRANCH_NAME = $CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - echo "CI_MERGE_REQUEST_ASSIGNEES          = $CI_MERGE_REQUEST_ASSIGNEES"
    - echo "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME = $CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"
    - echo "CI_MERGE_REQUEST_TITLE              = $CI_MERGE_REQUEST_TITLE"
```

| Job Name                              | Purpose                             | Key Variables                               |
| ------------------------------------- | ----------------------------------- | ------------------------------------------- |
| generic\_predefined\_variables        | Show general GitLab CI/CD variables | `CI_COMMIT_BRANCH`, `CI_PROJECT_NAME`, etc. |
| merge\_request\_predefined\_variables | Show merge request–only variables   | `CI_MERGE_REQUEST_*`                        |

> **lightbulb** Predefined merge request variables like `CI_MERGE_REQUEST_TITLE` are only available in pipelines triggered by merge requests—not on direct pushes to branches.

## 2. Apply `rules` to Limit the Job to Merge Requests

To ensure `merge_request_predefined_variables` runs only for merge requests, add a `rules` clause that checks the pipeline source:

```yaml theme={null}
merge_request_predefined_variables:
  stage: test
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  script:
    - echo "CI_MERGE_REQUEST_LABELS              = $CI_MERGE_REQUEST_LABELS"
    - echo "CI_MERGE_REQUEST_TARGET_BRANCH_NAME = $CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - echo "CI_MERGE_REQUEST_ASSIGNEES          = $CI_MERGE_REQUEST_ASSIGNEES"
    - echo "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME = $CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"
    - echo "CI_MERGE_REQUEST_TITLE              = $CI_MERGE_REQUEST_TITLE"
```

![The image shows a GitLab documentation page about CI/CD YAML syntax, specifically focusing on using rules to include or exclude jobs in pipelines. It includes a sidebar with navigation options and a detailed explanation of how rules are evaluated.](https://kodekloud.com/kk-media/image/upload/v1752877008/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-amp-Use-rules-at-Job-level/gitlab-ci-cd-yaml-rules-docs.jpg)

> **triangle-alert** Always wrap your conditional expression in single quotes to prevent YAML parsing errors.

With this configuration, the merge-request job is included only when `CI_PIPELINE_SOURCE` equals `merge_request_event`.

***

## 3. Create a Feature Branch and Push Changes

1. Checkout a new branch (e.g., `feature-1`):\
   `git checkout -b feature-1`
2. Commit your `.gitlab-ci.yml` changes and push:\
   `git push -u origin feature-1`

In the GitLab UI, select **Start a merge request** when prompted.

![The image shows a GitLab interface for creating a new merge request, with fields for the title, description, assignee, and reviewer. The title field is filled with "added rules for merge request job."](https://kodekloud.com/kk-media/image/upload/v1752877009/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-amp-Use-rules-at-Job-level/gitlab-merge-request-interface.jpg)

Because this initial push is a branch update, the merge-request job will be excluded, and only the generic job runs:

![The image shows a GitLab interface displaying a list of CI/CD pipelines, with two pipelines marked as "Passed." The sidebar includes options for managing projects, code, and pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877010/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-amp-Use-rules-at-Job-level/gitlab-cicd-pipelines-interface.jpg)

***

## 4. Open and Inspect the Merge Request Pipeline

1. In your project, click **Create merge request** for `feature-1`.
2. Add labels such as `predefined-variables`, `testing-rules`, then submit.

![The image shows a GitLab interface for creating a new merge request, with options to assign milestones, labels, and merge options. A user is about to click the "Create merge request" button.](https://kodekloud.com/kk-media/image/upload/v1752877011/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-amp-Use-rules-at-Job-level/gitlab-create-merge-request-interface.jpg)

3. GitLab triggers a merge request pipeline, visible under **Merge requests** as **merge request**:

![The image shows a GitLab interface displaying a list of CI/CD pipelines with their statuses, including one running and two passed. The sidebar includes options like issues, merge requests, and pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877012/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-amp-Use-rules-at-Job-level/gitlab-cicd-pipelines-status-interface.jpg)

4. Open the MR pipeline. You should see only the `merge_request_predefined_variables` job ran successfully:

![The image shows a GitLab pipeline interface for a project named "Exploring Predefined Variable Pipeline," indicating a successful pipeline run with details about jobs and merge requests.](https://kodekloud.com/kk-media/image/upload/v1752877013/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-amp-Use-rules-at-Job-level/gitlab-pipeline-exploring-variable-success.jpg)

***

## 5. Review the Merge Request Job Output

```bash theme={null}
$ echo "$CI_MERGE_REQUEST_LABELS"
CI_MERGE_REQUEST_LABELS - predefined-variables,testing-rules

$ echo "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
CI_MERGE_REQUEST_TARGET_BRANCH_NAME - main

$ echo "$CI_MERGE_REQUEST_ASSIGNEES"
CI_MERGE_REQUEST_ASSIGNEES - sidd-harth

$ echo "$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"
CI_MERGE_REQUEST_SOURCE_BRANCH_NAME - feature-1

$ echo "$CI_MERGE_REQUEST_TITLE"
CI_MERGE_REQUEST_TITLE - added rules for merge request job
```

This confirms:

* Merge request variables are populated only in MR pipelines.
* The `rules` keyword controls when a job is executed.

In upcoming lessons, we’ll dive deeper into more advanced `rules` configurations and merge request integrations.

***

## Links and References

* [GitLab CI/CD Predefined Variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)
* [GitLab CI/CD `rules` Documentation](https://docs.gitlab.com/ee/ci/yaml/#rules)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

## Further Reading

| Topic            | Description                              | Link                                                                                                                |
| ---------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| GitLab Pipelines | Overview of CI/CD in GitLab              | [https://docs.gitlab.com/ee/ci/](https://docs.gitlab.com/ee/ci/)                                                    |
| Pipeline Configs | Writing effective `.gitlab-ci.yml` files | [https://docs.gitlab.com/ee/ci/yaml/](https://docs.gitlab.com/ee/ci/yaml/)                                          |
| Merge Requests   | Lifecycle and best practices             | [https://docs.gitlab.com/ee/user/project/merge\_requests/](https://docs.gitlab.com/ee/user/project/merge_requests/) |

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/8a825bb5-b3db-4030-9ef9-dd800b38510e)


# Resource Groups

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Resource-Groups/page

Resource groups in GitLab CI/CD ensure mutual exclusion for critical jobs, allowing only one job in a group to run at a time.

In GitLab CI/CD, pipelines run concurrently by default. When you need to serialize critical jobs—such as deployments—across all pipelines in a project, **resource groups** provide mutual exclusion. Only one job in a given group can run at a time; the rest queue until the resource is released.

To learn more, see the [CI/CD YAML syntax reference for `resource_group`](https://docs.gitlab.com/ee/ci/yaml/#resource_group).

## Basic Workflow Example

The example below runs `deploy-job` on the `main` branch. Without a resource group, multiple pipelines could execute the deploy concurrently.

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: $CI_COMMIT_BRANCH == 'main'
      variables:
        DEPLOY_VARIABLE: "PRODUCTION"

deploy-job:
  stage: deploy
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

## Enforcing Mutual Exclusion with Resource Groups

Add the `resource_group` keyword to ensure that jobs sharing the same group never overlap:

```yaml theme={null}
deploy-to-production:
  stage: deploy
  script:
    - deploy
  resource_group: production
```

When several pipelines reach `deploy-to-production` at the same time, only one job obtains the `production` resource. The others wait in line.

## Process Modes

Resource groups support three modes for dequeuing waiting jobs:

| Process Mode  | Description                                            |
| ------------- | ------------------------------------------------------ |
| unordered     | Default; any waiting job may start next (no guarantee) |
| oldest\_first | Jobs run in the order they were queued                 |
| newest\_first | The most recently queued job starts first              |

To update the process mode for an existing resource group, use the [GitLab CI REST API](https://docs.gitlab.com/ee/api/resource_groups.html).

### Example: Build and Deploy Across Three Pipelines

This configuration triggers three successive pipelines. Each pipeline queues its `deploy` job against `production`:

```yaml theme={null}
build:
  stage: build
  script:
    - echo "Building..."

deploy:
  stage: deploy
  script:
    - echo "Deploying..."
  environment: production
  resource_group: production
```

* **unordered**: Any of deploy-1, deploy-2, or deploy-3 may run first; others wait.
* **oldest\_first**: deploy-1 → deploy-2 → deploy-3.
* **newest\_first**: deploy-3 → deploy-2 → deploy-1.

## Demo: Simulating Long-Running Deployments

Add a sleep command to observe the queuing behavior in the GitLab UI:

```yaml theme={null}
name: Exploring GitLab CI Concepts
rules:
  - if: '$CI_COMMIT_BRANCH == main'
variables:
  DEPLOY_VARIABLE: "PRODUCTION"
  
deploy-job:
  stage: deploy
  resource_group: production
  script:
    - echo "Deploying application..."
    - sleep 300
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

1. Commit to `main` to trigger the first pipeline.
2. Manually schedule a second pipeline on `main`.

> **lightbulb** The GitLab UI pipelines list shows each pipeline’s status, name, and project navigation options.

![The image shows a GitLab interface displaying a list of CI/CD pipelines with their statuses, names, and other details. The sidebar includes navigation options like Issues, Merge requests, and Pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877015/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Resource-Groups/gitlab-cicd-pipelines-interface.jpg)

> **lightbulb** Since the production resource is occupied by the first deploy-job, the second deploy-job remains queued and waiting.

![The image shows a GitLab interface with a "deploy-job" that is currently waiting for the resource "production." There is a sidebar with project navigation options.](https://kodekloud.com/kk-media/image/upload/v1752877016/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Resource-Groups/gitlab-deploy-job-waiting-production.jpg)

3. Cancel the first pipeline (or just its deploy-job) to free the resource.

> **lightbulb** Once the first deploy-job is canceled and the production resource is freed, the queued deploy-job automatically starts.

![The image shows a GitLab interface displaying a list of CI/CD pipelines with their statuses, such as running, canceled, and passed. The sidebar includes options like issues, merge requests, and pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877017/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Resource-Groups/gitlab-cicd-pipelines-status-interface.jpg)

Resource groups let you control job concurrency precisely, ensuring critical jobs never overlap across pipelines.

***

## Links and References

* [CI/CD YAML Syntax: resource\_group](https://docs.gitlab.com/ee/ci/yaml/#resource_group)
* [GitLab CI REST API: Resource Groups](https://docs.gitlab.com/ee/api/resource_groups.html)
* [GitLab Pipelines Documentation](https://docs.gitlab.com/ee/ci/pipelines/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/4df12434-eaad-4d72-aa9d-37a416ebcb1d)
