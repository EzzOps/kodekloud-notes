# Use rules at Workflow Level

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Use-rules-at-Workflow-Level/page

Learn to implement workflow-level rules in GitLab CI/CD for dynamic variable setting and pipeline filtering based on branch patterns and file changes.

GitLab CI/CD lets you define `rules` at both the job and workflow levels. While job-level rules determine whether an individual job runs, **workflow-level rules** control if the entire pipeline is created. This approach helps you:

* Dynamically set variables.
* Match branch patterns using regex.
* Filter pipelines by file changes.

In this guide, you’ll learn how to implement workflow-level rules with real examples.

***

## Prerequisites

1. Create a new GitLab project under your `demos` group.
2. Name it `generic-project` (public) and initialize with a `README.md`.
3. Open **CI/CD > Editor** to configure your pipeline.

<Frame>
  ![The image shows a GitLab interface for creating a new project, offering options to create a blank project, create from a template, import a project, or run CI/CD for an external repository.](https://kodekloud.com/kk-media/image/upload/v1752877045/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Use-rules-at-Workflow-Level/gitlab-new-project-interface.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab interface for creating a new blank project, with fields for project name, URL, and visibility settings.](https://kodekloud.com/kk-media/image/upload/v1752877046/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Use-rules-at-Workflow-Level/gitlab-new-project-interface-2.jpg)
</Frame>

***

## 1. Initial Pipeline Configuration

Add a minimal `.gitlab-ci.yml` to ensure your project has a pipeline:

<Frame>
  ![The image shows a GitLab Pipeline Editor interface with an option to configure a CI/CD pipeline by creating a .gitlab-ci.yml file. The sidebar includes project management options like issues, merge requests, and pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877047/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Use-rules-at-Workflow-Level/gitlab-pipeline-editor-cicd-config.jpg)
</Frame>

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts

deploy-job:
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

By default, no variables are set and the pipeline always runs. Let’s introduce workflow-level `rules` to change that.

***

## 2. Rule 1: Run Only on `main`

Trigger the pipeline **only** for pushes to `main`, and set `DEPLOY_VARIABLE` to `PRODUCTION`:

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      variables:
        DEPLOY_VARIABLE: "PRODUCTION"

deploy-job:
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

When you push to `main`:

```bash theme={null}
$ echo "Deploying application..."
Deploying application...
$ echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
Application successfully deployed to PRODUCTION environment
```

***

## 3. Rule 2: Merge Requests from `feature/*`

Only run pipelines on merge requests whose source branch matches `feature/*`. Use the predefined variable `CI_MERGE_REQUEST_SOURCE_BRANCH_NAME`:

<Frame>
  ![The image shows a GitLab documentation page listing predefined CI/CD variables for merge request pipelines, including their names, GitLab version, runner compatibility, and descriptions.](https://kodekloud.com/kk-media/image/upload/v1752877049/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Use-rules-at-Workflow-Level/gitlab-ci-cd-variables-documentation.jpg)
</Frame>

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      variables:
        DEPLOY_VARIABLE: "PRODUCTION"
    - if: '$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME =~ /^feature\// && $CI_PIPELINE_SOURCE == "merge_request_event"'
      variables:
        DEPLOY_VARIABLE: "TESTING"

deploy-job:
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

Push to `feature/my-awesome-feature` and create an MR:

<Frame>
  ![The image shows a GitLab interface for creating a new merge request, with fields for title, description, assignee, and reviewer.](https://kodekloud.com/kk-media/image/upload/v1752877050/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Use-rules-at-Workflow-Level/gitlab-merge-request-interface.jpg)
</Frame>

*No pipeline runs yet* because we haven’t introduced file-change filters.

***

## 4. Rule 3: File-Change Filtering

Use the `changes:` keyword to trigger pipelines only when certain files are modified. For example, run MR pipelines only if `README.md` changes:

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      variables:
        DEPLOY_VARIABLE: "PRODUCTION"
    - if: '$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME =~ /^feature\// && $CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - README.md
      variables:
        DEPLOY_VARIABLE: "TESTING"

deploy-job:
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

Update `README.md` in your feature branch and push. Now you’ll see a new pipeline:

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface with two pipeline entries, one running and one passed, along with user avatars and pipeline details.](https://kodekloud.com/kk-media/image/upload/v1752877052/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Use-rules-at-Workflow-Level/gitlab-ci-cd-pipeline-interface.jpg)
</Frame>

The job log confirms the `TESTING` variable:

```text theme={null}
$ echo "Deploying application..."
Deploying application...
$ echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
Application successfully deployed to TESTING environment
```

***

## Summary of Workflow-Level Rules

| Rule  | Trigger                                       | Variable   | Description                                       |
| ----- | --------------------------------------------- | ---------- | ------------------------------------------------- |
| **1** | `CI_COMMIT_BRANCH == "main"`                  | PRODUCTION | Only build on `main`                              |
| **2** | MR event & source branch matches `feature/*`  | TESTING    | Run on feature-branch merge requests              |
| **3** | Same as Rule 2 **and** `changes: [README.md]` | TESTING    | Only when `README.md` is updated in the MR branch |

***

<Callout icon="triangle-alert">
  The first matching rule wins. If no rule matches, the pipeline won’t be created—no jobs will run.
</Callout>

***

## Final `.gitlab-ci.yml` Example

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: '$CI_COMMIT_TITLE =~ /-draft$/'
      when: never
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

deploy-job:
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

<Callout icon="lightbulb">
  Customize your `rules` with `when: manual`, `allow_failure`, or file filters to match your team’s workflow.
</Callout>

***

## Links and References

* [GitLab CI/CD documentation](https://docs.gitlab.com/ee/ci/)
* [Predefined CI/CD variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)
* [Rules keyword reference](https://docs.gitlab.com/ee/ci/yaml/#rules)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/b8f75a88-d4e2-45c3-9c77-7105ad3986e2" />
</CardGroup>
