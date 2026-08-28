# Using needs Keyword

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Using-needs-Keyword/page

This guide explains how to enhance a GitLab CI/CD pipeline using the `needs` keyword for job sequencing and efficient failure handling.

In this guide, you’ll enhance an existing GitLab CI/CD pipeline by:

* Renaming jobs for clarity
* Introducing a dedicated Docker stage
* Controlling execution order with the `needs` keyword

By the end, you’ll understand how to build a Directed Acyclic Graph (DAG) of jobs that enforces logical progression and efficient failure handling.

## 1. Original Workflow

Here’s the starting pipeline, which builds ASCII art, runs tests, and deploys:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

stages:
  - build
  - test
  - deploy

build_job_1:
  stage: build
  before_script:
    - gem install cowsay
    - sleep 30s
  script:
    - >
      cowsay -f dragon "Run for cover,
      I am a DRAGON....RAWR!" >> dragon.txt
  artifacts:
    name: Dragon Text File
    paths:
      - dragon.txt
    when: on_success
    expire_in: 3 days

test_job_2:
  stage: test
  script:
    - echo "Running tests..."

deploy_job_3:
  stage: deploy
  script:
    - echo "Deploying to AWS EC2"
```

## 2. Renaming Jobs and Cleaning Up

Rename jobs for readability and remove the unnecessary `sleep` command:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

stages:
  - build
  - test
  - deploy

build_file:
  stage: build
  before_script:
    - gem install cowsay
  script:
    - >
      cowsay -f dragon "Run for cover,
      I am a DRAGON....RAWR" >> dragon.txt
  artifacts:
    name: Dragon Text File
    paths:
      - dragon.txt
    when: on_success
    expire_in: 3 days

test_file:
  stage: test
  script:
    - echo "Running tests..."

deploy_ec2:
  stage: deploy
  script:
    - echo "Deploying to AWS EC2"
```

At this point, the pipeline runs three sequential stages: **build**, **test**, then **deploy**.

## 3. Introducing a Docker Stage

Add a new **docker** stage with three placeholder jobs:

```yaml theme={null}
stages:
  - build
  - test
  - docker
  - deploy

build_file: &build_file
  stage: build
  before_script:
    - gem install cowsay
  script:
    - >
      cowsay -f dragon "Run for cover,
      I am a DRAGON....RAWR" >> dragon.txt
  artifacts:
    name: Dragon Text File
    paths:
      - dragon.txt
    when: on_success
    expire_in: 3 days

test_file: &test_file
  stage: test
  script:
    - echo "Running tests..."

docker_build:
  stage: docker
  script:
    - echo "docker build -t docker.io/dockerUsername/imageName:version"
    - sleep 15s

docker_testing:
  stage: docker
  script:
    - echo "docker run -p 80:80 docker.io/dockerUsername/imageName:version"
    - sleep 10s
    - exit 1

docker_push:
  stage: docker
  script:
    - echo "docker login --username=dockerUsername --password=s3cUrePaSsW0rd"
    - echo "docker push docker.io/dockerUsername/imageName:version"

deploy_ec2:
  <<: *build_file
  script:
    - echo "Deploying to AWS EC2"
```

By default, GitLab runs all three Docker jobs in parallel once the **test** stage completes.

<Callout icon="triangle-alert">
  When jobs share the same stage, GitLab CI/CD executes them in parallel. This may cause `docker_push` to run before `docker_build`, or allow failures in `docker_testing` without halting `docker_push`.
</Callout>

## 4. Docker Jobs Overview

| Job Name         | Stage  | Purpose                                      |
| ---------------- | ------ | -------------------------------------------- |
| `docker_build`   | docker | Builds the Docker image                      |
| `docker_testing` | docker | Runs container and performs health checks    |
| `docker_push`    | docker | Logs in and pushes the image to the registry |

## 5. Sequencing with `needs`

Use the `needs` keyword to enforce a DAG of dependencies and ensure correct ordering:

```yaml theme={null}
docker_build:
  stage: docker
  needs:
    - test_file
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

After committing, the UI will reflect this sequence:\
build → test → docker\_build → docker\_testing → docker\_push.\
If `docker_testing` fails, `docker_push` is automatically skipped.

Console output for `docker_testing`:

```bash theme={null}
$ echo "docker run -p 80:80 docker.io/dockerUsername/imageName:version"
docker run -p 80:80 docker.io/dockerUsername/imageName:version
$ sleep 10s
$ exit 1
ERROR: Job failed: exit code 1
```

## 6. Ignoring Stage Order

You can also launch jobs as soon as their dependencies complete, even if they’re in later stages. For example:

```yaml theme={null}
docker_build:
  stage: docker
  needs:
    - build_file
  script:
    - echo "docker build -t docker.io/dockerUsername/imageName:version"
```

Here, **docker\_build** starts immediately after **build\_file**, running in parallel with **test\_file**.

## 7. Conclusion

Using the `needs` keyword allows you to:

* Sequence jobs within the same stage
* Override default stage ordering for earlier execution
* Visualize your pipeline as a clear DAG

This gives you precise control over dependencies and failure handling in your GitLab CI/CD workflows.

## Links and References

* [GitLab CI/CD `needs` Keyword](https://docs.gitlab.com/ee/ci/yaml/#needs)
* [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/da301f46-6c42-4c5d-aa4f-26aa8f9472ac" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/1b39cf47-9ccb-448c-9d50-bb27fe48be4b" />
</CardGroup>
