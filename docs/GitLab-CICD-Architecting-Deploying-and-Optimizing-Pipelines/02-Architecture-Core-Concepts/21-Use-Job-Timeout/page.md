# Use Job Timeout

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Use-Job-Timeout/page

Learn to set job-level timeouts in GitLab CI/CD to prevent long-running jobs from blocking pipelines and consuming resources.

In this guide, you’ll learn how to set a job-level timeout in GitLab CI/CD. Long-running or stalled jobs—caused by script errors, network issues, or unresolved dependencies—can block pipelines and consume resources. By defining a timeout, any job that exceeds the allotted time is automatically terminated.

## Sample Pipeline Without Timeout

Here’s a basic pipeline that deploys an application but uses a `sleep` command to simulate a long-running step:

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  variables:
    DEPLOY_VARIABLE: PRODUCTION

deploy-job:
  resource_group: production
  script:
    - echo "Deploying application..."
    - sleep 30s
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

> **lightbulb** A stalled or infinite loop in `script` can cause your pipeline to hang. Always test long-running commands locally before adding them to CI.

## Why Use Job-Level Timeouts?

* Prevent rogue or hung jobs from consuming runner resources
* Ensure faster pipeline feedback and fail-fast behavior
* Avoid billing surprises on shared or cloud runners

> **triangle-alert** Defining too-short a timeout may lead to unexpected job failures. Choose a duration that accommodates normal execution time plus a buffer.

## Adding a Timeout to a Job

To configure a timeout, add the `timeout` keyword to any job. GitLab supports human-readable durations in a variety of formats:

```yaml theme={null}
build:
  script: ./build.sh
  timeout: 3 hours 30 minutes

test:
  script: rspec
  timeout: 3h 30m

lint:
  script: ./lint.sh
  timeout: 3600 seconds
```

### Supported Duration Formats

| Format            | Examples               |
| ----------------- | ---------------------- |
| Hours and minutes | `3 hours 30 minutes`   |
| Compact (h/m/s)   | `3h30m`, `45m`, `10s`  |
| Full words        | `1 hour`, `90 seconds` |
| Combined units    | `1h 15m`, `2h5m30s`    |

For more details, see [GitLab CI/CD Timeout Settings](https://docs.gitlab.com/ee/ci/yaml/#timeout).

## Example: Forcing a Fast Failure

If you want your `deploy-job` to be canceled after 10 seconds, add `timeout: 10s`:

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  variables:
    DEPLOY_VARIABLE: PRODUCTION

deploy-job:
  resource_group: production
  timeout: 10s
  script:
    - echo "Deploying application..."
    - sleep 300s
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

When the job exceeds 10 seconds, the runner will terminate it and you’ll see:

```text theme={null}
ERROR: Job failed: execution took longer than 10 seconds
```

## Final Pipeline Configuration

Below is the complete pipeline configured with a 10-second timeout for `deploy-job`:

```yaml theme={null}
workflow:
  name: Exploring GitLab CI Concepts
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  variables:
    DEPLOY_VARIABLE: PRODUCTION

deploy-job:
  resource_group: production
  timeout: 10s
  script:
    - echo "Deploying application..."
    - sleep 360s
    - echo "Application successfully deployed to $DEPLOY_VARIABLE environment"
```

Choose a timeout value that aligns with your job’s expected duration to maintain pipeline reliability and resource efficiency.

## Links and References

* [GitLab CI/CD Pipeline Configuration](https://docs.gitlab.com/ee/ci/yaml/)
* [Job Timeout Settings](https://docs.gitlab.com/ee/ci/yaml/#timeout)
* [GitLab Runner Executors](https://docs.gitlab.com/runner/executors/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/de774bf8-c5bc-4aab-8960-b188dc87e248)
