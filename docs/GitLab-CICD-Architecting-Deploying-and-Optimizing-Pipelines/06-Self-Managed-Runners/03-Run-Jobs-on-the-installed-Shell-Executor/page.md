# 1. Download the GitLab Runner binary
sudo curl -L --output /usr/local/bin/gitlab-runner \
  https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

# 2. Make it executable
sudo chmod +x /usr/local/bin/gitlab-runner

# 3. Create a runner user
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# 4. Install and start as a service
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo gitlab-runner start
```

Verify the installation:

```bash theme={null}
gitlab-runner -v
# Expected output:
# Version:      16.8.0
# Git revision: c72a09b6
# Git branch:   16-8-stable
# GO version:   go1.21.5
# Built:        2024-01-18T22:42:25+0000
# OS/Arch:      linux/amd64
```

***

## 6. Register the Runner with GitLab

Use the registration token from the project UI:

```bash theme={null}
sudo gitlab-runner register \
  --url https://gitlab.com/ \
  --token <YOUR_TOKEN>
```

Interactive prompts:

1. Confirm the GitLab URL (`https://gitlab.com/`).
2. Provide a runner name (e.g., `nodejs-runner`).
3. Enter tags (`NodeJS`).
4. Select executor: `shell`.

```bash theme={null}
Enter the GitLab instance URL (for example, https://gitlab.com/):
Verifying runner... is valid
Enter a name for the runner: nodejs-runner
Enter tags for the runner (comma-separated): NodeJS
Enter an executor: shell
Runner registered successfully.
```

***

## 7. Verify Runner in the GitLab UI

Return to **Settings > CI/CD > Runners**. You should see your new runner listed as **active**:

![The image shows a GitLab runner configuration page with details such as runner ID, status, tags, version, IP address, platform, and description.](https://kodekloud.com/kk-media/image/upload/v1752877424/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-runner-configuration-page.jpg)

You can **edit**, **pause**, or **protect** this runner from the UI.

***

## 8. Examine `config.toml`

The runner’s settings live in `/etc/gitlab-runner/config.toml`:

```toml theme={null}
concurrent = 1
check_interval = 3
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "nodejs-runner"
  url = "https://gitlab.com/"
  token = "glrt-..."
  executor = "shell"

[runners.cache]
  MaxUploadedArchiveSize = 0
```

| Setting                          | Description                             |
| -------------------------------- | --------------------------------------- |
| `concurrent`                     | Max parallel jobs (default: `1`)        |
| `check_interval`                 | Poll interval in seconds (default: `3`) |
| `session_server.session_timeout` | Web terminal session timeout (seconds)  |
| `[[runners]].executor`           | Executor type (e.g., `shell`, `docker`) |

For advanced options, see [Advanced Configuration Documentation](https://docs.gitlab.com/runner/configuration/advanced-configuration.html).

![The image shows a GitLab documentation page about advanced configuration for GitLab Runner, detailing how to modify the config.toml file and explaining configuration validation.](https://kodekloud.com/kk-media/image/upload/v1752877425/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-runner-advanced-configuration.jpg)

***

## 9. Explore Available Executors

GitLab Runner supports multiple executors. Review and choose the one that best fits your environment:

* Shell
* Docker
* Kubernetes
* SSH
* VirtualBox
* Parallels

[Executors Documentation](https://docs.gitlab.com/runner/executors/)

![The image shows a GitLab documentation page about runner executors, listing various types such as SSH, Shell, Parallels, and Docker. The sidebar includes navigation links for related topics.](https://kodekloud.com/kk-media/image/upload/v1752877426/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-runner-executors-documentation.jpg)

![The image shows a GitLab documentation page comparing different executor types, such as SSH, Shell, VirtualBox, and Docker, with various features and conditions.](https://kodekloud.com/kk-media/image/upload/v1752877427/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-executor-types-comparison.jpg)

![The image shows a GitLab documentation page detailing runner executors, with a table comparing features across different executor types like SSH, Shell, Docker, and Kubernetes.](https://kodekloud.com/kk-media/image/upload/v1752877428/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-runner-executors-comparison.jpg)

![The image shows a GitLab documentation page detailing different executors available for GitLab Runner, including their required configurations and where jobs run. The sidebar on the left lists various configuration topics.](https://kodekloud.com/kk-media/image/upload/v1752877430/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-runner-executors-documentation-2.jpg)

***

## 10. List Registered Runners Locally

On your runner VM, confirm the registration:

```bash theme={null}
gitlab-runner list
# Example output:
# Runtime platform            arch=amd64 os=linux pid=46330 revision=c72a09b6 version=16.8.0
# ConfigFile=/etc/gitlab-runner/config.toml
# Executor=shell Token=<TRUNCATED> URL=https://gitlab.com/
# nodejs-runner
```

Your self-managed Shell executor runner is now operational. In the next guide, we’ll cover running pipelines and job debugging.

***

## References and Further Reading

* [GitLab Runner Official Documentation](https://docs.gitlab.com/runner/)
* [Advanced Runner Configuration](https://docs.gitlab.com/runner/configuration/advanced-configuration.html)
* [CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)
* [GitLab CI/CD Pipeline Configuration](https://docs.gitlab.com/ee/ci/yaml/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/270646a2-73ad-4be3-90c9-9b4448aa8517/lesson/0d5d4be1-0707-44ec-9cf3-28614a5fc02a)


# Run Jobs on the installed Shell Executor

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Self-Managed-Runners/Run-Jobs-on-the-installed-Shell-Executor/page

This guide explains configuring and optimizing a CI/CD pipeline on a self-hosted GitLab Runner using the Shell executor.

In this guide, you’ll learn how to configure and optimize a CI/CD pipeline on a self-hosted GitLab Runner using the Shell executor. We’ll walk through:

1. Defining a **basic pipeline**.
2. Selecting your **self-managed runner** with tags.
3. Troubleshooting **shell-profile** issues.
4. Installing **Node.js** on the runner VM.
5. Caching **npm dependencies** between runs.
6. Customizing the runner’s **cache directory**.

***

## 1. Basic Pipeline Configuration

Begin by creating a simple `.gitlab-ci.yml` that runs unit tests against your Node.js project. This example sets up environment variables, uses stages, and caches `node_modules` to speed up subsequent runs.

```yaml theme={null}
workflow:
  name: Shell Executor Demo

variables:
  MONGO_URI:  'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: SuperPassword

stages:
  - test

unit_test:
  stage: test
  cache:
    policy: pull-push
    key:
      files:
        - package-lock.json
      prefix: node-modules
    paths:
      - node_modules
  before_script:
    - npm install
  script:
    - npm test
```

| Section         | Purpose                                    |
| --------------- | ------------------------------------------ |
| `variables`     | Secure strings for database connection     |
| `stages`        | Defines workflow steps (only `test` here)  |
| `cache`         | Speeds up `npm install` by reusing modules |
| `before_script` | Pre-test setup commands                    |
| `script`        | Actual test command                        |

***

## 2. Selecting the Self-Managed Runner

To ensure jobs land on your Shell executor, add the same tags you used during runner registration:

```yaml theme={null}
unit_test:
  tags:
    - nodejs
    - linux
    - local
  stage: test
  cache:
    policy: pull-push
    key:
      files:
        - package-lock.json
      prefix: node-modules
    paths:
      - node_modules
  before_script:
    - npm install
  script:
    - npm test
```

> **lightbulb** Runner tags must match exactly (case-sensitive). Review **Settings > CI/CD > Runners** in your project to confirm tag names.

Your project’s **CI/CD settings** should display your tagged runner:

![The image shows the CI/CD settings page of a GitLab project, with options for configuring pipelines, Auto DevOps, runners, artifacts, variables, and pipeline trigger tokens. The interface includes a sidebar with various settings categories.](https://kodekloud.com/kk-media/image/upload/v1752877431/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Run-Jobs-on-the-installed-Shell-Executor/gitlab-cicd-settings-page.jpg)

After committing these changes, GitLab will automatically trigger a new pipeline.

***

## 3. Troubleshooting Shell-Executor Profiles

If the job fails during **prepare environment**, you might see:

![The image shows a GitLab CI/CD job interface where a unit testing job has failed, with an error message related to preparing the environment.](https://kodekloud.com/kk-media/image/upload/v1752877432/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Run-Jobs-on-the-installed-Shell-Executor/gitlab-cicd-unit-test-failed.jpg)

```plaintext theme={null}
Preparing environment
Running on iac-server...
ERROR: Job failed: prepare environment: exit status 1.
Check https://docs.gitlab.com/runner/shells/index.html#shell-profile-loading
```

This usually means your shell’s logout or profile scripts are clearing the console. On the runner VM, edit `~/.bash_logout`:

```bash theme={null}
