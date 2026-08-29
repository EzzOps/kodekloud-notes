# Installation Configuration Steps

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Installation-Configuration-Steps/page

Guide to installing and configuring the GitHub Actions Importer gh extension to plan, test, and migrate Jenkins pipelines into GitHub Actions workflows.

This guide walks through installing and configuring the GitHub Actions Importer extension for the GitHub CLI. The extension helps migrate Jenkins pipelines into GitHub Actions workflows by providing planning, testing, and migration commands integrated into `gh`.

Prerequisites

* A Jenkins account or organization containing the pipelines you plan to migrate.
* Permission to create a Jenkins personal API token (a Jenkins user or admin with token creation rights).
* A GitHub account with permission to create a personal access token (classic) for the destination GitHub user or organization.
* An environment capable of running Linux-based containers (Docker) and with the [GitHub CLI](https://cli.github.com) installed.

Table: Required credentials and recommended scopes

| Credential                             | Purpose                                | Recommended scopes / notes                                           |
| -------------------------------------- | -------------------------------------- | -------------------------------------------------------------------- |
| GitHub personal access token (classic) | Push workflows, create repos if needed | `repo` scope; add org-level scopes if migrating into an organization |
| Jenkins personal API token             | Read jobs and pipelines                | Token must belong to a user with read access to relevant jobs        |
| Jenkins username                       | Used with Jenkins API token            | Ensure it corresponds to the token owner                             |

What the extension does

* The GitHub Actions Importer is distributed as an extension for the [GitHub CLI](https://cli.github.com). Extensions add custom `gh` commands that guide planning, testing, and migrating Jenkins jobs into GitHub Actions workflows.

Installation

1. Install the extension with `gh`:

```bash theme={null}
gh extension install github/gh-actions-importer
```

Example output after a successful install:

```bash theme={null}
› gh extension install github/gh-actions-importer
✓ Installed extension github/gh-actions-importer
```

Verify the extension

* Confirm the extension is installed and view available commands:

```bash theme={null}
gh actions-importer -h
```

Sample help output:

```text theme={null}
Description:
    GitHub Actions Importer helps you plan, test, and automate your migration to GitHub Actions.

Please share your feedback @ https://gh.io/ghaimporterfeedback

Options:
    -?, -h, --help  Show help and usage information

Commands:
    update          Update to the latest version of GitHub Actions Importer.
    version         Display the current version.
    configure       Configure credentials and endpoints for CI providers.
    plan            Analyze and plan migration for your Jenkins jobs.
    migrate         Run a migration operation (test or actual).
```

Configuration

* Configure the extension to store the credentials and endpoints it needs to access GitHub and Jenkins:

```bash theme={null}
gh actions-importer configure
```

* The command is interactive. Select the CI provider(s) to configure (choose Jenkins) and provide the following:

  * GitHub personal access token (classic) — required to push workflows or create repositories.
  * Base URL of the GitHub instance — use `https://github.com` for GitHub.com or your Enterprise URL for GitHub Enterprise Server.
  * Jenkins personal API token — the token generated for the Jenkins user.
  * Jenkins username — the account that owns the Jenkins API token.
  * Base URL of the Jenkins instance — e.g., `https://jenkins-url.com`.

Example interactive session (secrets masked):

```bash theme={null}
❯ gh actions-importer configure
✔ Which CI providers are you configuring?: Jenkins
Enter the following values (leave empty to omit):
✔ Personal access token for GitHub: ***********************
✔ Base url of the GitHub instance: https://github.com
✔ Personal access token for Jenkins: ***********************
✔ Username of Jenkins user: siddharth
✔ Base url of the Jenkins instance: https://jenkins-url.com
Environment variables successfully updated.
```

* When complete, these settings are stored in your local `gh` configuration so subsequent `gh actions-importer` commands can authenticate to the configured Jenkins and GitHub instances.

<Callout icon="lightbulb">
  Ensure your GitHub personal access token has the necessary scopes (for example, `repo` and any required organization permissions). For Jenkins, use an API token tied to a user with sufficient access to read the jobs and pipelines you plan to migrate.
</Callout>

<Callout icon="warning">
  Do not expose personal access tokens or Jenkins API tokens in logs, screenshots, or shared files. Treat these tokens like passwords and rotate them immediately if they are accidentally exposed.
</Callout>

Commands overview

* After configuration, start with:

| Command                         | Purpose                                            |
| ------------------------------- | -------------------------------------------------- |
| `gh actions-importer configure` | Store credentials/endpoints for Jenkins and GitHub |
| `gh actions-importer plan`      | Analyze Jenkins jobs and produce a migration plan  |
| `gh actions-importer migrate`   | Execute a migration (dry-run or actual)            |
| `gh actions-importer update`    | Update the extension to the latest version         |
| `gh actions-importer version`   | Show the extension version                         |

Next steps

* Run `gh actions-importer plan` to analyze your Jenkins instance and generate a migration plan.
* Audit your Jenkins jobs and configurations before migrating—review job triggers, secrets, and any environment-specific steps.
* Test migrations using the extension’s dry-run/migrate options before applying changes to production repositories.

Links and references

* [GitHub CLI](https://cli.github.com)
* [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions)
* [Jenkins](https://learn.kodekloud.com/user/courses/jenkins)
* [GitHub Docs: Personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/0ddbc4de-c775-42d5-8599-83b7ec9ca54a" />
</CardGroup>
