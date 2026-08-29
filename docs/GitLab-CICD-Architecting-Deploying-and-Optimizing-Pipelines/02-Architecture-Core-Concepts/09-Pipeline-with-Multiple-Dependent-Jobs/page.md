# Pipeline with Multiple Dependent Jobs

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Pipeline-with-Multiple-Dependent-Jobs/page

This guide explains configuring a CI pipeline with build, test, and deploy stages while managing job dependencies and sharing artifacts.

In this guide, we'll explore how to configure a CI pipeline with three distinct stages—**build**, **test**, and **deploy**—and ensure they execute in the correct order while sharing artifacts.

## Initial Pipeline Configuration

Here’s a basic GitLab CI configuration defining three jobs:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

build_job_1:
  stage: build
  before_script:
    - gem install cowsay
    - sleep 30s
  script:
    - cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt

test_job_2:
  stage: test
  script:
    - sleep 10s
    - grep -i "dragon" dragon.txt

deploy_job_3:
  stage: deploy
  script:
    - cat dragon.txt
    - echo "deploying ... ..."
```

> **triangle-alert** Relying on fixed `sleep` intervals can lead to fragile pipelines. Instead, use proper job dependencies and artifacts to synchronize stages.

## Job Breakdown

| Job Name       | Stage  | Purpose                                        |
| -------------- | ------ | ---------------------------------------------- |
| build\_job\_1  | build  | Installs `cowsay` and generates `dragon.txt`   |
| test\_job\_2   | test   | Searches for “dragon” in the generated file    |
| deploy\_job\_3 | deploy | Displays ASCII art and prints a deploy message |

* **build\_job\_1** installs the `cowsay` gem, pauses for 30 seconds, then writes ASCII art into `dragon.txt`.
* **test\_job\_2** pauses for 10 seconds before verifying the file contains the keyword “dragon.”
* **deploy\_job\_3** outputs the contents of `dragon.txt` and echoes a deploy message.

> **lightbulb** By default, GitLab CI jobs run in parallel on separate runners and do not share the same workspace.

## Observed Failures

Because **test\_job\_2** and **deploy\_job\_3** often start before **build\_job\_1** finishes, they encounter missing files:

```bash theme={null}
$ sleep 10s
grep: dragon.txt: No such file or directory
ERROR: Job failed: exit code 1
```

```bash theme={null}
$ cat dragon.txt
cat: dragon.txt: No such file or directory
ERROR: Job failed: exit code 1
```

Meanwhile, **build\_job\_1** succeeds:

```bash theme={null}
$ gem install cowsay
Successfully installed cowsay-3.0.3
1 gem installed
$ sleep 30s
$ cowsay -f dragon "Run for cover, I am a DRAGON....RAWR!" > dragon.txt
```

## Why Jobs Fail

* Each job runs on a separate runner with its own workspace.
* There’s no file sharing by default.
* The execution order is not guaranteed without explicit dependencies.

## Next Steps

In the next section, we’ll introduce the `needs` keyword and artifacts settings to:

1. Ensure **build\_job\_1** completes before **test\_job\_2**.
2. Share `dragon.txt` as an artifact for downstream jobs.
3. Execute **deploy\_job\_3** only after the test stage passes.

## References

* [GitLab CI/CD pipelines](https://docs.gitlab.com/ee/ci/pipelines/)
* [GitLab Artifacts](https://docs.gitlab.com/ee/ci/pipelines/job_artifacts.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/e14d87da-6664-49e3-9535-0ee88e3f3efd)
