# Migrating Jenkins Pipeline to GitHub Action

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Backup-and-Configuration-Management/Migrating-Jenkins-Pipeline-to-GitHub-Action/page

Guide to migrating declarative Jenkins pipelines and many freestyle jobs to GitHub Actions using the gh-actions-importer, covering installation, authentication, dry-run conversions, PR creation, and workflow adjustments.

This guide shows how to migrate declarative Jenkins pipelines (and many freestyle jobs) to GitHub Actions using the GitHub Actions Importer (`gh-actions-importer`). The importer automates most conversion steps and can open a pull request in your repository with the generated workflow.

What you'll accomplish

* Configure the importer to authenticate to both Jenkins and GitHub.
* Preview conversions with `dry-run`.
* Create a branch and pull request in GitHub with `migrate`.
* Review and adjust the workflow, then run it in GitHub Actions.

## Prerequisites

| Requirement                            | Purpose / Notes                                                                                             |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Jenkins account/organization           | Source of pipelines/jobs to migrate.                                                                        |
| Jenkins user with API access           | Needed to create a Jenkins API token (for `JENKINS_ACCESS_TOKEN`).                                          |
| GitHub account with repo permissions   | Required to push branches, create PRs, and create workflows in the target repository.                       |
| Container runtime (Docker or Podman)   | The importer runs in a container when invoked by the `gh` extension.                                        |
| GitHub CLI (`gh`)                      | Install from [https://cli.github.com/](https://cli.github.com/) and use to install the importer.            |
| GitHub Personal Access Token (classic) | Token must include `workflow` scope and `repo` as needed so the importer can create workflow files and PRs. |

## Limitations

| Limitation                     | Impact                                                                                 |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| Scripted Jenkins pipelines     | Not supported — only declarative pipelines and many freestyle jobs are convertible.    |
| Jenkins credentials/secrets    | Not migrated; create corresponding GitHub Secrets manually.                            |
| Custom/unknown Jenkins plugins | Steps reliant on such plugins may not convert correctly and require manual adjustment. |

<Frame>
  <img alt="A screenshot of the GitHub Docs page for GitHub Actions (dark theme) showing guidance on migrating from Jenkins, with a left navigation menu and main content listing prerequisites and limitations. Browser tabs and window UI are visible along the top." />
</Frame>

Note: Keep access tokens secure — store them in a secrets manager or environment variables, not in plaintext inside repositories.

> **lightbulb** You will use the GitHub CLI (`gh`) plus the `gh-actions-importer` extension. The importer runs locally and calls both Jenkins and GitHub APIs, so it requires credentials for both systems (`JENKINS_USERNAME`, `JENKINS_ACCESS_TOKEN`, and a GitHub Personal Access Token with `workflow` scope).

## Install GitHub CLI and the Importer extension

Install GitHub CLI on Debian/Ubuntu (run as root or with `sudo`):

```bash theme={null}
