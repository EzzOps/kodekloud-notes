# Create a Docker Action

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Custom-Actions/Create-a-Docker-Action/page

Learn to create a Docker-based GitHub Action that posts a random Giphy Thank You GIF on pull request events.

In this tutorial, learn how to develop a custom Docker-based GitHub Action that automatically posts a random “Thank You” GIF from Giphy whenever someone opens a pull request. This CI/CD integration covers:

* Triggering on `pull_request` events
* Fetching a random GIF via the Giphy REST API
* Commenting on the pull request with the GitHub REST API

We’ll securely store API keys in GitHub Secrets and encapsulate the entire implementation in a Docker container.

## Table of Contents

1. [Giphy REST API](#1-giphy-rest-api)
2. [GitHub REST API for Comments](#2-github-rest-api-for-comments)
3. [Creating the Repository](#3-creating-the-repository)
4. [Configuring GitHub Secrets](#4-configuring-github-secrets)
5. [Project Structure Overview](#5-project-structure-overview)
6. [Dockerfile Configuration](#6-dockerfile-configuration)
7. [Entrypoint Script](#7-entrypoint-script)
8. [Action Metadata (`action.yml`)](#8-action-metadata-actionyml)
9. [Test Workflow Setup](#9-test-workflow-setup)
10. [Opening a Pull Request](#10-opening-a-pull-request)
11. [Verifying the Workflow](#11-verifying-the-workflow)
12. [Reviewing the Bot Comment](#12-reviewing-the-bot-comment)
13. [Links and References](#13-links-and-references)

***

## 1. Giphy REST API

Use the Giphy **[Random GIF endpoint](https://developers.giphy.com/docs/api/endpoint#random)** to retrieve a random “thank you” GIF. Store your GIPHY API key in GitHub Secrets and reference it in the action:

```http theme={null}
GET https://api.giphy.com/v1/gifs/random?api_key=<GIPHY_API_KEY>&tag=thank%20you&rating=g
```

A sample JSON response:

```json theme={null}
{
  "data": {
    "images": {
      "original": {
        "url": "https://media1.giphy.com/media/l119IDMNbVsKgyf5u/giphy.gif"
      },
      "downsized": {
        "url": "https://media1.giphy.com/media/l119IDMNbVsKgyf5u/200w_d.gif"
      }
    }
  }
}
```

Extract the GIF URL from `.data.images.downsized.url` using [`jq`](https://stedolan.github.io/jq/).

***

## 2. GitHub REST API for Comments

To comment on a PR, call GitHub’s **[Create an issue comment](https://docs.github.com/rest/issues/comments#create-an-issue-comment)** endpoint. Issues and pull request comments use the same API.

![The image shows a GitHub documentation page for the REST API, specifically focusing on managing issues, with links to various related actions like listing, creating, and updating issues.](https://kodekloud.com/kk-media/image/upload/v1752876036/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-rest-api-managing-issues.jpg)

| HTTP Method | Endpoint                                                                     | Purpose             |
| ----------- | ---------------------------------------------------------------------------- | ------------------- |
| POST        | `https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments` | Create a PR comment |

Example `curl` command:

```bash theme={null}
curl -s -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments \
  -d '{"body":"Thank you for this contribution! 🎉"}'
```

***

## 3. Creating the Repository

Initialize a new public repository named `docker-action-pr-giphy-comment` with a `README.md`:

![The image shows a GitHub page for creating a new repository, with fields for the repository name, description, and options for public or private settings.](https://kodekloud.com/kk-media/image/upload/v1752876037/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-new-repository-creation-page.jpg)

After creation, you’ll see the initial commit:

![The image shows a GitHub repository page titled "docker-action-pr-giphy-comment" with an initial commit and a README file. The repository has no stars, forks, or releases.](https://kodekloud.com/kk-media/image/upload/v1752876039/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-repo-docker-action-readme.jpg)

***

## 4. Configuring GitHub Secrets

Store sensitive information under **Settings > Secrets and variables > Actions**:

![The image shows a GitHub repository settings page where a new secret is being added under "Actions secrets." The secret is named "GIPHY\_API\_KEY."](https://kodekloud.com/kk-media/image/upload/v1752876040/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-repo-settings-add-secret-giphy-api-key.jpg)

> **lightbulb** You will add:

  * `GIPHY_API_KEY` for the Giphy API
  * Use the built-in `GITHUB_TOKEN` for commenting on PRs

***

## 5. Project Structure Overview

Your repository should contain the following files:

![The image shows a code editor with a project directory open, displaying files like action.yml, Dockerfile, and entrypoint.sh in a GitHub repository. The README.md file is open in the editor pane.](https://kodekloud.com/kk-media/image/upload/v1752876041/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/code-editor-github-repo-files.jpg)

| File                         | Purpose                            |
| ---------------------------- | ---------------------------------- |
| `Dockerfile`                 | Defines the container environment  |
| `entrypoint.sh`              | Handles the action logic           |
| `action.yml`                 | Action metadata and inputs         |
| `.github/workflows/test.yml` | Workflow to test the action on PRs |

***

## 6. Dockerfile Configuration

Create a lightweight container with required utilities:

```dockerfile theme={null}
FROM alpine:3.10
