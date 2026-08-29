# Using stage vs stages Keyword

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Using-stage-vs-stages-Keyword/page

This article explains the use of `stage` and `stages` keywords in GitLab CI/CD for defining job execution order in pipelines.

## Introduction

In GitLab CI/CD, the `stages` keyword defines the sequence in which jobs execute. Without an explicit order, all jobs run in parallel—leading to situations where tests or deployments start before your build finishes and ultimately fail. By declaring an ordered list of stages and assigning each job to one, you ensure a reliable, sequential pipeline: build → test → deploy.

All GitLab CI/CD YAML syntax is covered in the official [GitLab docs](https://docs.gitlab.com/ee/ci/yaml/).

***

## Defining Stages in Your `.gitlab-ci.yml`

### 1. Basic `stages` Syntax

```yaml theme={null}
stages:
  - build
  - test
  - deploy
```

Each item under `stages` represents a phase of your pipeline. Jobs in the same stage run in parallel, while stages themselves execute one after another.

### 2. Assigning Jobs to Stages

```yaml theme={null}
stages:
  - build
  - test
  - deploy

compile_code:
  stage: build
  script:
    - echo "Compiling code..."

run_tests:
  stage: test
  script:
    - echo "Running tests..."

deploy_app:
  stage: deploy
  script:
    - echo "Deploying application..."
```

Here, `compile_code` runs first. If it succeeds, `run_tests` starts. Finally, `deploy_app` executes only after tests pass.

***

## Example: Full Pipeline Configuration

Below is a complete pipeline that installs a gem, generates ASCII art in a file, then tests and deploys based on that file.

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  before_script:
    - gem install cowsay
    - sleep 30s
  script:
    - >
      cowsay -f dragon "Run for cover,
      I am a DRAGON....RAWR" >> dragon.txt

test_job:
  stage: test
  script:
    - sleep 10s
    - grep -i "dragon" dragon.txt

deploy_job:
  stage: deploy
  script:
    - echo "Deploying..."
```

| Stage  | Description                                          |
| ------ | ---------------------------------------------------- |
| build  | Installs dependencies and generates `dragon.txt`     |
| test   | Executes a search for “dragon” in the generated file |
| deploy | Deploys the application after successful tests       |

* **workflow\.name**: Gives your pipeline a friendly title.
* **build\_job**: Installs `cowsay`, waits 30s, and writes ASCII art to `dragon.txt`.
* **test\_job**: Waits 10s then searches for “dragon” inside `dragon.txt`.
* **deploy\_job**: Runs only if the test stage succeeds.

> **lightbulb** Jobs must be assigned to one of the listed `stages`. Assigning a job to an undefined stage will trigger a pipeline editor warning.

***

## Exploring Pipeline Visualization

Once committed, GitLab runs the pipeline in three sequential stages. Use the **Visualize** tab in the pipeline editor to confirm the flow before pushing changes.

![The image shows a GitLab pipeline interface with three stages: build, test, and deploy. The test stage has failed due to a script failure.](https://kodekloud.com/kk-media/image/upload/v1752877053/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Using-stage-vs-stages-Keyword/gitlab-pipeline-build-test-deploy.jpg)

***

## Analyzing Job Output

### Build Job Logs

```bash theme={null}
$ gem install cowsay
Successfully installed cowsay-3.1.0
1 gem installed
$ sleep 30s
$ cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt
```

### Test Job Failure

```bash theme={null}
$ sleep 10s
grep: dragon.txt: No such file or directory
ERROR: Job failed: exit code 1
```

> **triangle-alert** Because each job runs in its own runner environment, artifacts created in `build` aren’t available in `test` by default. You must configure [artifacts](https://docs.gitlab.com/ee/ci/yaml/#artifacts) to pass files between stages.

***

## Passing Data with Artifacts

To preserve files like `dragon.txt` across stages, add an `artifacts` section to your build job:

```yaml theme={null}
build_job:
  stage: build
  script:
    - cowsay -f dragon "..." >> dragon.txt
  artifacts:
    paths:
      - dragon.txt
    expire_in: 1 hour
```

This makes the file available to all downstream jobs in the same pipeline.

***

## Monitoring Compute Minutes

GitLab’s UI shows **Pipeline Duration** and **Minutes Used**—critical metrics if you’re on a usage-limited plan. Check these under **Pipeline Details** for better cost management.

***

## Links and References

* [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
* [GitLab Artifacts Documentation](https://docs.gitlab.com/ee/ci/yaml/#artifacts)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/7bb7540d-cefa-4b16-a002-2d2e0a6d0a21)
