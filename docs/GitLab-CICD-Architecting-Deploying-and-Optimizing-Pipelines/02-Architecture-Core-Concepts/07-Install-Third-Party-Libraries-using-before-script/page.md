# Install Third Party Libraries using before script

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Install-Third-Party-Libraries-using-before-script/page

Learn to use before_script in GitLab CI/CD to install dependencies and manage cleanup with an example using the cowsay gem.

In this guide, you’ll learn how to leverage `before_script` and `after_script` in GitLab CI/CD pipelines to install dependencies and handle cleanup. We’ll demonstrate using the `cowsay` gem to generate fun ASCII artwork.

> **lightbulb** * A GitLab project with CI/CD enabled
  * Basic understanding of GitLab CI/CD YAML syntax
  * Docker runner or shared runners configured

***

## Table of Contents

1. [Define OS Version Jobs](#define-os-version-jobs)
2. [Generate ASCII Artwork with cowsay](#generate-ascii-artwork-with-cowsay)
3. [Pipeline Failure: Missing Dependency](#pipeline-failure-missing-dependency)
4. [Install Dependencies with before\_script](#install-dependencies-with-before_script)
5. [Successful Job Output](#successful-job-output)
6. [Summary](#summary)
7. [Links and References](#links-and-references)

***

## Define OS Version Jobs

Create lightweight jobs to display OS versions on various runners:

```yaml theme={null}
windows_job:
  tags:
    - shared-windows
  script:
    - echo "Windows OS Version"
    - systeminfo

linux_job:
  tags:
    - saas-linux-medium-amd64
  script:
    - echo "Linux OS Version"
    - cat /etc/os-release

macos_job:
  tags:
    - saas-macos-medium-m1
  script:
    - echo "macOS Version"
    - system_profiler SPSoftwareDataType
```

***

## Generate ASCII Artwork with cowsay

Define a pipeline that uses `cowsay` to output ASCII art into a file:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

ascii_job:
  script:
    - echo "Generating ASCII artwork using COWSAY"
    - cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt
    - grep -i "dragon" dragon.txt
    - cat dragon.txt
```

***

## Pipeline Failure: Missing Dependency

Running the above job on the default Ruby image fails:

```bash theme={null}
$ cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt
/usr/bin/bash: line 1: cowsay: command not found
ERROR: Job failed: exit code 1
```

The error indicates `cowsay` is not preinstalled in the base image.

***

## Install Dependencies with before\_script

To ensure `cowsay` is available, install it via `before_script`:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

ascii_job:
  image: ruby:3.1
  before_script:
    - gem install cowsay
  script:
    - echo "Generating ASCII artwork using COWSAY"
    - cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt
    - grep -i "dragon" dragon.txt
    - cat dragon.txt
  after_script:
    - echo "Cleanup after job"
```

| Keyword        | Purpose                                                     | Example                      |
| -------------- | ----------------------------------------------------------- | ---------------------------- |
| before\_script | Install dependencies or prepare environment before `script` | `- gem install cowsay`       |
| script         | Main steps of the job                                       | ASCII generation commands    |
| after\_script  | Cleanup or notifications after the job                      | `- echo "Cleanup after job"` |

> **triangle-alert** Ensure your runner can access external package sources. For air-gapped environments, pre-build a custom Docker image with required gems.

***

## Successful Job Output

With `cowsay` installed, the pipeline completes successfully:

```bash theme={null}
$ gem install cowsay
Successfully installed cowsay-0.3.0
1 gem installed

$ echo "Generating ASCII artwork using COWSAY"
Generating ASCII artwork using COWSAY

$ cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt

$ grep -i "dragon" dragon.txt
 Run for cover, I am a DRAGON....RAWR |

$ cat dragon.txt
 ________
< Run for cover, I am a DRAGON....RAWR >
 --------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

$ echo "Cleanup after job"
Cleanup after job
```

***

## Summary

By adding a `before_script` section to your GitLab CI/CD job, you can:

* Automatically install required libraries or tools
* Avoid failures due to missing dependencies
* Leverage `after_script` for cleanup and notifications

This pattern ensures robust, repeatable pipelines across all environments.

***

## Links and References

* [GitLab CI/CD Pipeline Configuration](https://docs.gitlab.com/ee/ci/yaml/)
* [cowsay RubyGem on RubyGems.org](https://rubygems.org/gems/cowsay)
* [GitLab Runners](https://docs.gitlab.com/runner/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/f727b50e-8001-4e2b-bd3f-e3338f9e39f3)
