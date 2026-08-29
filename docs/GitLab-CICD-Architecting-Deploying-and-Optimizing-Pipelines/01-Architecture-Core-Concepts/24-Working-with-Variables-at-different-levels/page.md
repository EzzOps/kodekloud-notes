# Working with Variables at different levels

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Working-with-Variables-at-different-levels/page

This guide explains how to define and manage variables at different scopes within a GitLab CI/CD pipeline.

In this guide, you’ll learn how to define and manage variables at different scopes within a GitLab CI/CD pipeline. Proper use of variables helps you follow DRY principles, streamline maintenance, and reduce the risk of errors when updating image names, versions, or other configuration values.

<Callout icon="lightbulb">
  GitLab CI/CD supports both [custom variables](https://docs.gitlab.com/ee/ci/variables/) and [predefined variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html). Use them to parameterize your pipeline and avoid hard-coding values.
</Callout>

***

## 1. Pain Point: Hard-Coded Values in Every Job

Here’s a typical pipeline that builds, tests, and pushes a Docker image. Notice how the registry, username, image name, and version are repeated in each job:

```yaml theme={null}
docker_build:
  stage: docker
  needs:
    - build_file
  script:
    - echo "docker build -t docker.io/dockerUsername/imageName:version"
    - sleep 15s

docker_testing:
  stage: docker
  needs:
    - docker_build
  script:
    - echo "docker run -p 80:80 docker.io/dockerUsername/imageName:version"
    - sleep 10s
    - exit 1

docker_push:
  stage: docker
  needs:
    - docker_testing
  script:
    - echo "docker login --username=dockerUsername --password=s3cUrePaSsW0rd"
    - echo "docker push docker.io/dockerUsername/imageName:version"
```

Maintaining pipelines like this is error-prone. Every change to `imageName` or `version` requires edits in multiple places.

***

## 2. Variable Scopes: Global vs. Job-Level

GitLab CI/CD provides two scopes for custom variables:

| Scope      | Declaration Location         | Effective In      |
| ---------- | ---------------------------- | ----------------- |
| **Global** | top-level `variables:` block | *All* jobs        |
| **Job**    | `variables:` inside a job    | That specific job |

* Global variables can be overridden by job-level variables with the same name.
* Job-level variables are isolated to their job and not visible elsewhere.

***

## 3. Defining Global Variables

Move shared configuration into a global `variables:` block. This makes your pipeline DRY and easier to update.

```yaml theme={null}
variables:
  DEPLOY_SITE: "https://example.com/"

deploy_job:
  stage: deploy
  script:
    - deploy-script --url "$DEPLOY_SITE" --path "/"
  environment: production

deploy_review_job:
  stage: deploy
  variables:
    REVIEW_PATH: "/review"
  script:
    - deploy-review-script --url "$DEPLOY_SITE" --path "$REVIEW_PATH"
  environment: production
```

* `DEPLOY_SITE` is available to both jobs.
* `REVIEW_PATH` applies only to `deploy_review_job`.

***

## 4. Refactoring Docker Jobs with Shared Variables

First, here’s a version that still repeats variables at the job level:

```yaml theme={null}
docker_build:
  stage: docker
  needs:
    - build_file
  variables:
    USERNAME: dockerUsername
    REGISTRY: docker.io/$USERNAME
    IMAGE: ascii-artwork
    VERSION: latest
  script:
    - echo "docker build -t $REGISTRY/$IMAGE:$VERSION"

docker_testing:
  stage: docker
  needs:
    - docker_build
  variables:
    USERNAME: dockerUsername
    REGISTRY: docker.io/$USERNAME
    IMAGE: ascii-artwork
    VERSION: latest
  script:
    - echo "docker run -p 80:80 $REGISTRY/$IMAGE:$VERSION"

docker_push:
  stage: docker
  needs:
    - docker_testing
  variables:
    USERNAME: dockerUsername
    REGISTRY: docker.io/$USERNAME
    IMAGE: ascii-artwork
    VERSION: latest
    PASSWORD: s3cUrePaSsW0rd
  script:
    - echo "docker login --username=$USERNAME --password=$PASSWORD"
    - echo "docker push $REGISTRY/$IMAGE:$VERSION"
```

Each job redeclares `USERNAME`, `REGISTRY`, `IMAGE`, and `VERSION`—we can improve this.

***

## 5. Promoting Common Variables to Global Scope

Define all shared variables at the top level. Only sensitive or job-specific variables stay within the job.

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

stages:
  - build
  - test
  - docker
  - deploy

variables:
  USERNAME: dockerUsername
  REGISTRY: docker.io/$USERNAME
  IMAGE: ascii-artwork
  VERSION: latest

build_file:
  stage: build
  script: …

test_file:
  stage: test
  script: …

docker_build:
  stage: docker
  needs:
    - build_file
  script:
    - echo "docker build -t $REGISTRY/$IMAGE:$VERSION"

docker_testing:
  stage: docker
  needs:
    - docker_build
  script:
    - echo "docker run -p 80:80 $REGISTRY/$IMAGE:$VERSION"

docker_push:
  stage: docker
  needs:
    - docker_testing
  variables:
    PASSWORD: s3cUrePaSsW0rd
  script:
    - echo "docker login --username=$USERNAME --password=$PASSWORD"
    - echo "docker push $REGISTRY/$IMAGE:$VERSION"
```

Now only `PASSWORD` remains in `docker_push`, while `USERNAME`, `REGISTRY`, `IMAGE`, and `VERSION` are defined once.

***

## 6. Leveraging Predefined CI/CD Variables for Dynamic Tagging

Instead of a static `latest` tag, use `$CI_PIPELINE_ID` or `$CI_COMMIT_SHA` to uniquely tag each build:

```yaml theme={null}
variables:
  USERNAME: dockerUsername
  REGISTRY: docker.io/$USERNAME
  IMAGE: ascii-artwork
  VERSION: $CI_PIPELINE_ID
```

```yaml theme={null}
docker_build:
  stage: docker
  needs:
    - build_file
  script:
    - echo "docker build -t $REGISTRY/$IMAGE:$VERSION"
```

Every pipeline run now pushes `ascii-artwork:<pipeline_id>`, making image versions traceable.

***

## 7. Viewing Expanded Variables in Job Logs

When the pipeline runs, GitLab replaces variables with their values:

```bash theme={null}
$ echo "docker login --username=$USERNAME --password=$PASSWORD"
docker login --username=dockerUsername --password=s3cUrePaSsW0rd

$ echo "docker push $REGISTRY/$IMAGE:$VERSION"
docker push docker.io/dockerUsername/ascii-artwork:1153576211
```

Here, `$VERSION` was replaced by the numeric pipeline ID.

***

## 8. Job-Level Variables Are Isolated

Job-specific variables do not carry over to other jobs:

```yaml theme={null}
deploy_ec2:
  stage: deploy
  script:
    - echo "Username: $USERNAME, Password: $PASSWORD"
```

Log output:

```bash theme={null}
$ echo "Username: $USERNAME, Password: $PASSWORD"
Username: dockerUsername, Password:
```

`$PASSWORD` is empty because it was only defined in the `docker_push` job.

<Callout icon="triangle-alert">
  Avoid exposing sensitive variables in job logs. Use [Masked Variables](https://docs.gitlab.com/ee/ci/variables/#mask-a-cicd-variable) or [Protected Variables](https://docs.gitlab.com/ee/ci/variables/#protected-cicd-variables) to secure credentials and secrets.
</Callout>

***

## 9. Next Steps

* Explore [GitLab CI/CD Variables documentation](https://docs.gitlab.com/ee/ci/variables/).
* Learn how to [mask and protect variables](https://docs.gitlab.com/ee/ci/variables/#using-cicd-variables-in-your-pipeline).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/50b14c65-af22-4280-83e0-21f89fffcd4d" />
</CardGroup>
