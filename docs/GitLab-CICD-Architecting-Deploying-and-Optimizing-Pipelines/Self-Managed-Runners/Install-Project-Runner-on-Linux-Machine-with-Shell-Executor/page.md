# Download the latest GitLab Runner binary
sudo curl -L --output /usr/local/bin/gitlab-runner \
  https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

# Make it executable
sudo chmod +x /usr/local/bin/gitlab-runner

# Create a dedicated service user
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# Install and start GitLab Runner as a service
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo gitlab-runner start
```

Register the group runner using the token you copied:

```bash theme={null}
gitlab-runner register \
  --url https://gitlab.com \
  --token <YOUR_REGISTRATION_TOKEN>
```

When prompted:

* **Enter a name for the runner**: `aws-docker-runner`
* **Enter an executor**: `docker`
* **Enter the default Docker image**: `ruby:2.7`

<Callout icon="lightbulb">
  You can customize the default image per job in your `.gitlab-ci.yml` using the `image:` keyword.
</Callout>

## 3. Check Runner Status in GitLab

After registration, GitLab lists the runner under **Group > CI/CD > Runners**, but it will show **“Never contacted”** until the service connects.

<Frame>
  ![The image shows a GitLab interface displaying details of a runner with a Docker executor configured with AWS. The runner has never contacted the instance and is associated with a group called "demos-group."](https://kodekloud.com/kk-media/image/upload/v1752877415/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Group-Runner-on-Linux-Machine-with-Docker-Executor/gitlab-runner-docker-aws-demos-group.jpg)
</Frame>

On your Linux host, verify both shell and Docker runners are registered:

```bash theme={null}
gitlab-runner list

# Sample output:
Runtime platform                                arch=amd64 os=linux pid=123610 revision=c72a09b6 version=16.8.0
ConfigFile=/etc/gitlab-runner/config.toml
Executor=shell   Token=glrt-3iCBsGsPFN6WBGmaps5B  URL=https://gitlab.com
Executor=docker  Token=glrt-hnyKQKHcCoxosWLEssKc  URL=https://gitlab.com
```

Once the runner service starts successfully, the status will update to **online** in GitLab.

## 4. Review the Runner Configuration

Open `/etc/gitlab-runner/config.toml` to inspect both runners:

```toml theme={null}
concurrent = 1
check_interval = 0

[[runners]]
  name      = "nodejs-runner"
  url       = "https://gitlab.com"
  id        = 32418121
  token     = "glrt-3iCBsGsPFN6WBGmaps5B"
  executor  = "shell"
  cache_dir = "/home/gitlab-runner/builds"

[[runners]]
  name     = "aws-docker-runner"
  url      = "https://gitlab.com"
  id       = 32418122
  token    = "glrt-hnyKQKHcCoxosWLEssKc"
  executor = "docker"

  [runners.cache]
    MaxUploadedArchiveSize = 0

  [runners.docker]
    tls_verify                   = false
    image                        = "ruby:2.7"
    privileged                   = false
    disable_entrypoint_overwrite = false
    oom_kill_disable             = false
    disable_cache                = false
    volumes                      = ["cache"]
    shm_size                     = 0
    network_mtu                  = 0
```

## 5. Verify Runner in a Project

The group runner is now available to every project in the `demos` group.

1. Open a project (e.g., **Solar System**).
2. Navigate to **Settings > CI/CD > Runners**.
3. Optionally disable shared runners to ensure jobs use your group runner exclusively.

<Frame>
  ![The image shows a GitLab CI/CD settings page, displaying options for managing project and shared runners, with details about available runners and their configurations.](https://kodekloud.com/kk-media/image/upload/v1752877416/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Group-Runner-on-Linux-Machine-with-Docker-Executor/gitlab-ci-cd-settings-runners.jpg)
</Frame>

Jobs tagged with `docker`, `aws`, and `linux` will now execute on your Docker-based group runner.

***

## 6. Links and References

* [GitLab Runner Documentation](https://docs.gitlab.com/runner/)
* [Docker Executor for GitLab Runner](https://docs.gitlab.com/runner/executors/docker.html)
* [Managing Runners in GitLab](https://docs.gitlab.com/ee/ci/runners/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/270646a2-73ad-4be3-90c9-9b4448aa8517/lesson/419528d7-51eb-4511-963c-99216880b4a1" />
</CardGroup>


# Install Project Runner on Linux Machine with Shell Executor

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Self-Managed-Runners/Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/page

This tutorial explains setting up a self-managed GitLab Runner on Linux using the Shell executor for a NodeJS application.

In this tutorial, you’ll learn how to set up a self-managed GitLab Runner on a Linux VM using the Shell executor. We’ll use a simple NodeJS application (`runner-demo`) that runs unit tests against MongoDB.

## Table of Contents

* [1. Import the `runner-demo` Project](#1-import-the-runner-demo-project)
* [2. Define the CI/CD Pipeline](#2-define-the-cicd-pipeline)
* [3. Disable Shared Runners (and Observe a Stuck Pipeline)](#3-disable-shared-runners-and-observe-a-stuck-pipeline)
* [4. Register a New Project Runner](#4-register-a-new-project-runner)
* [5. Install GitLab Runner on Linux VM](#5-install-gitlab-runner-on-linux-vm)
* [6. Register the Runner with GitLab](#6-register-the-runner-with-gitlab)
* [7. Verify Runner in the GitLab UI](#7-verify-runner-in-the-gitlab-ui)
* [8. Examine `config.toml`](#8-examine-configtoml)
* [9. Explore Available Executors](#9-explore-available-executors)
* [10. List Registered Runners Locally](#10-list-registered-runners-locally)
* [References and Further Reading](#references-and-further-reading)

***

## 1. Import the runner-demo Project

First, create or import a GitLab project named `runner-demo` in your group. Make the project **public** to simplify access.

<Frame>
  ![The image shows a GitLab interface for importing a project, with fields for entering a Git repository URL, project name, and other details. The sidebar includes options like Projects, Groups, and Issues.](https://kodekloud.com/kk-media/image/upload/v1752877417/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-import-project-interface.jpg)
</Frame>

This project contains a NodeJS app that connects to MongoDB and executes unit tests.

<Callout icon="lightbulb">
  Ensure your MongoDB URI, username, and password are secured via CI/CD variables or a secrets manager—avoid hardcoding sensitive credentials.
</Callout>

***

## 2. Define the CI/CD Pipeline

In the root of `runner-demo`, add a file named `.gitlab-ci.yml`:

```yaml theme={null}
workflow:
  name: Project Level Runner Demo

variables:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: SuperPassword

stages:
  - test

unit_testing:
  stage: test
  cache:
    key:
      files:
        - package-lock.json
      prefix: node-modules
    policy: pull-push
    paths:
      - node_modules
  before_script:
    - npm install
  script:
    - npm test
```

This pipeline defines a single `unit_testing` job:

| Stage | Job Name      | Actions                                |
| ----- | ------------- | -------------------------------------- |
| test  | unit\_testing | Installs dependencies, runs `npm test` |

***

## 3. Disable Shared Runners and Observe a Stuck Pipeline

GitLab projects default to using shared runners. To demonstrate a self-managed runner, disable them:

1. Navigate to **Settings > CI/CD > Runners**.
2. Toggle **Shared runners** off.

<Frame>
  ![The image shows the CI/CD settings page in GitLab, displaying options for configuring project and shared runners. It includes a list of available runners and settings for enabling shared runners for a project.](https://kodekloud.com/kk-media/image/upload/v1752877419/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-cicd-settings-runners.jpg)
</Frame>

Commit and push your `.gitlab-ci.yml` to the `main` branch. The new pipeline will queue but remain **stuck**:

<Frame>
  ![The image shows a GitLab interface displaying a pipeline with a pending status. The sidebar includes options like "Issues," "Merge requests," and "Pipelines."](https://kodekloud.com/kk-media/image/upload/v1752877420/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-pipeline-pending-status.jpg)
</Frame>

The `unit_testing` job stays pending due to no active runners:

<Frame>
  ![The image shows a GitLab job interface with a message indicating that a job is pending and hasn't started due to a lack of active runners. There's an option to cancel the job.](https://kodekloud.com/kk-media/image/upload/v1752877420/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-job-pending-no-runners.jpg)
</Frame>

<Callout icon="triangle-alert">
  Until you register a runner, all CI/CD jobs will remain in a pending state. Make sure to add a project-level runner or re-enable shared runners.
</Callout>

***

## 4. Register a New Project Runner

In **Settings > CI/CD > Runners > Project Runners**, click **New runner**. Select **Linux** as the operating system and add a tag to scope job assignment (e.g., `NodeJS`).

<Frame>
  ![The image shows a GitLab interface for creating a new project runner, with options to select the operating system (Linux, macOS, Windows) and containers (Docker, Kubernetes). There is also a section for adding tags to specify jobs for the runner.](https://kodekloud.com/kk-media/image/upload/v1752877421/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-new-project-runner-interface.jpg)
</Frame>

Use the **NodeJS** tag to target your `unit_testing` job:

<Frame>
  ![The image shows a GitLab interface for creating a new runner, with options to select the operating system and containers, and a section for adding tags to specify jobs the runner can execute.](https://kodekloud.com/kk-media/image/upload/v1752877422/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-new-runner-interface.jpg)
</Frame>

Optionally, configure:

* Runner description
* Maximum job timeout
* Protection & pausing settings

<Frame>
  ![The image shows a GitLab interface for configuring a new runner, with options for tags, runner description, and various settings like pausing and protection.](https://kodekloud.com/kk-media/image/upload/v1752877423/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Install-Project-Runner-on-Linux-Machine-with-Shell-Executor/gitlab-new-runner-configuration.jpg)
</Frame>

Click **Create runner** to display the registration token and commands.

***

## 5. Install GitLab Runner on Linux VM

On your Linux VM (e.g., Ubuntu), execute the following steps:

```bash theme={null}
