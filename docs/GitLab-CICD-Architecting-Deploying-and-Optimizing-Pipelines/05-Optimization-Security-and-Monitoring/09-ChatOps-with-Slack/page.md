# ChatOps with Slack

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/ChatOps-with-Slack/page

This guide demonstrates integrating GitLab ChatOps into Slack for triggering CI/CD pipelines, managing issues, and reviewing job outputs.

In this guide, we’ll demonstrate how to integrate GitLab ChatOps into your Slack workspace. With GitLab ChatOps, you can trigger CI/CD pipelines, manage issues, and review job outputs—all without leaving Slack.

<Frame>
  ![The image shows a GitLab documentation page about ChatOps, detailing its integration with CI/CD jobs through chat services like Slack, and includes information on slash command integrations and workflow configuration.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877328/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-chatops-cicd-integration.jpg)
</Frame>

## Requirements

* A GitLab project with the **GitLab for Slack** app installed and configured
* Enabled slash commands in Slack (Mattermost uses different commands)

## Available Slash Commands

Use the `/gitlab help` command to list all supported GitLab ChatOps slash commands in your workspace.

<Frame>
  ![The image shows a webpage from GitLab documentation about the GitLab for Slack app, detailing installation instructions and features like slash commands and notifications.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877330/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-slack-app-installation-guide.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab documentation page detailing slash commands for the GitLab Slack app, with a list of commands and their descriptions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877331/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-slack-app-slash-commands.jpg)
</Frame>

| Slash Command                                        | Description           | Example                                                   |
| ---------------------------------------------------- | --------------------- | --------------------------------------------------------- |
| `/gitlab [alias] issue show <id>`                    | Display issue details | `/gitlab demo-group/solar-system issue show 42`           |
| `/gitlab [alias] issue new <title> <description>`    | Create a new issue    | `/gitlab demo-group/solar-system issue new "Bug" "Steps"` |
| `/gitlab [alias] issue close <id>`                   | Close an issue        | `/gitlab demo-group/solar-system issue close 42`          |
| `/gitlab [alias] run <job-name> [--branch=<branch>]` | Trigger a CI job      | `/gitlab demo-group/solar-system run test-suite`          |
| `/gitlab [alias] deploy <env> to <target-env>`       | Deploy environment    | `/gitlab demo-group/solar-system deploy staging to prod`  |

### List Commands in Slack

In your GitLab notification channel (e.g., `#gitlab-notifications`), type:

```bash theme={null}
/gitlab help
```

<Frame>
  ![The image shows a Slack workspace with a channel named "gitlab-notifications" where users and bots are interacting, including notifications about GitLab activities.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877333/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/slack-workspace-gitlab-notifications.jpg)
</Frame>

## Creating an Issue via ChatOps

You can quickly create issues directly in Slack:

1. Identify your **project alias** (group/project) set up during Slack integration.
2. Run the new-issue command:

   ```shell theme={null}
   /gitlab demos-group/solar-system issue new "Demo Title" <<Shift+Enter>>
   Trying out GitLab ChatOps commands using Slack.
   ```

<Frame>
  ![The image shows the GitLab integration settings for a Slack app, indicating that the integration is active and configured to trigger notifications when a push is made to the repository.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877334/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-slack-integration-settings.jpg)
</Frame>

<Frame>
  ![The image shows a Slack interface with a channel named "gitlab-notifications" open, displaying messages related to GitLab commands and notifications.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877335/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/slack-gitlab-notifications-interface.jpg)
</Frame>

Slack will confirm the issue creation. You can verify it in GitLab:

<Frame>
  ![The image shows a GitLab interface with an open issue titled "Demo Title" in a project named "Solar System." It includes options for creating a merge request, adding labels, and managing child and linked items.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877336/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-solar-system-issue-demo.jpg)
</Frame>

## Running CI Jobs via ChatOps

Assuming your `.gitlab-ci.yml` defines a `unit_testing` job:

```yaml theme={null}
unit_testing:
  stage: test
  extends: .prepare_nodejs_environment
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: Moca-Test-Result
    paths:
      - test-results.xml
    reports:
      junit: test-results.xml
```

Trigger this job in Slack:

```shell theme={null}
/gitlab demos-group/solar-system run unit_testing
```

If you need to run the job on a feature branch:

```shell theme={null}
/gitlab demos-group/solar-system run unit_testing --branch="feature/setting-up-gitlab-ci"
```

<Callout icon="triangle-alert">
  If escaping special characters in branch names fails, you may temporarily change your project’s default branch in GitLab.

  1. Go to **Settings > Repository > Default branch**
  2. Select your feature branch and save
</Callout>

<Frame>
  ![The image shows a GitLab repository settings page, specifically focusing on branch defaults and branch name templates. A cursor is hovering over the "Save changes" button.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877337/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-repo-settings-branch-defaults.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab repository interface with a list of files and their last commit messages. The sidebar includes options like branches, commits, and merge requests.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877339/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-ChatOps-with-Slack/gitlab-repository-interface-files-list.jpg)
</Frame>

Once the default branch is updated, rerun without `--branch`:

```shell theme={null}
/gitlab demos-group/solar-system run unit_testing
```

Back in GitLab you’ll see the new pipeline logs:

```plaintext theme={null}
Using docker image sha256:[SECRET_REDACTED] for node:17-alpine3.14 ...
$ npm install
up to date, audited 385 packages in 2s
45 packages are looking for funding
run `npm fund` for details
2 vulnerabilities (1 high, 1 critical)
...
$ npm test
> Solar System@6.7.6 test
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit
Server successfully running on port - 3000
```

You’ll also receive job-completion notifications directly in Slack, keeping you informed without context switching.

## References

* [GitLab ChatOps Documentation](https://docs.gitlab.[AWS_SECRET_ACCESS_KEY].html)
* [Slack Apps Integration Guide](https://api.slack.com/apps)
* [GitLab CI/CD Overview](https://docs.gitlab.com/ee/ci/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/2b348ddc-3550-4672-85a1-6bce061d53d7" />
</CardGroup>
