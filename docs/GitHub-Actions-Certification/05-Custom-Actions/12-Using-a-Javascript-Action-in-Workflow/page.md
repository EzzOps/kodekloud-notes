# .github/workflows/pr-thank-you.yml
name: PR Thank You Comment

on:
  pull_request:
    types: [opened]

jobs:
  pr-action:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Post PR Comment with Giphy
        uses: siddharth-7/docker-action-pr-giphy-comment@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key: ${{ secrets.GIPHY_API }}
```

### Permissions Reference

| Permission             | Purpose                 |
| ---------------------- | ----------------------- |
| `issues: write`        | Post comments on issues |
| `pull-requests: write` | Manage PR comments      |

Commit and push your branch, then open a pull request:

<Frame>
  ![The image shows a GitHub interface for creating a pull request, with options to leave a comment and assign reviewers. The "Create pull request" button is highlighted at the bottom.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876088/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-pull-request-interface-highlighted-button.jpg)
</Frame>

## 4. Observe the Workflow Run

Once the PR is created, GitHub Actions will trigger the workflow automatically:

<Frame>
  ![The image shows a GitHub pull request page for creating a file named "pr-thank-you.yml" with details about the branch, checks, and merge status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876089/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-pull-request-pr-thank-you.jpg)
</Frame>

Monitor progress under the **Actions** tab:

<Frame>
  ![The image shows a GitHub Actions page with a workflow named "pr-thank-you.yml" in progress. The sidebar lists options like Caches, Deployments, and Runners.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876090/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-actions-pr-thank-you-workflow.jpg)
</Frame>

After success, the action posts a thank-you GIF comment on the pull request.

## 5. Behind the Scenes: Docker Build Logs

Each run of a container action rebuilds the Docker image. Example build output:

```bash theme={null}
#1 [internal] load .dockerignore
#1 DONE 0.0s
#2 [internal] load build definition from Dockerfile
#2 DONE 0.0s
#3 [internal] load metadata for docker.io/library/alpine:3.10
#3 DONE 0.0s
#6 [1/4] FROM docker.io/library/alpine:3.10
#6 DONE 0.1s
#9 [4/4] RUN chmod +x /entrypoint.sh
#9 DONE 0.3s
```

And the execution command:

```bash theme={null}
/usr/bin/docker run --name 2c046f464a14829b2e7791b519b_32bdb \
  --label 461ce --workdir /github/workspace -m -1 \
  --input_github_token="INPUT_GITHUB_TOKEN" \
  -e "GIPHY_API" -e "GITHUB_SHA"="GITHUB_SHA" \
  -v "/var/run/docker.sock":"/var/run/docker.sock" \
  --rm docker-action-pr-giphy-comment:main
```

<Callout icon="triangle-alert">
  Rebuilding the Docker image each run adds latency. For faster CI workflows, consider authoring a [JavaScript action](https://docs.github.com/actions/creating-actions/creating-a-javascript-action) that executes without a container build.
</Callout>

## References

* [GitHub Actions: Workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
* [Giphy Developer Portal](https://developers.giphy.com/)
* [Creating a JavaScript Action](https://docs.github.com/actions/creating-actions/creating-a-javascript-action)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/428391ee-45d0-4e9c-9e06-78d0c5ff7657/lesson/cf5b432a-57ef-4df9-bca1-a55049d352a5" />
</CardGroup>


# Using a Javascript Action in Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Custom-Actions/Using-a-Javascript-Action-in-Workflow/page

This guide explains how to integrate a JavaScript custom action into a GitHub Actions workflow for posting comments on pull requests.

In this guide, you’ll learn how to extend an existing GitHub Actions workflow by integrating a JavaScript custom action from the GitHub Marketplace. We’ll start with a Docker-based PR comment action and then add the JavaScript version to post a “Thank You” GIF on every new pull request.

## 1. Review the Original Docker-Based Workflow

The `pr-thank-you.yml` workflow below triggers on pull request **opened** events and uses a Docker action to post a Giphy comment:

```yaml theme={null}
on:
  pull_request:
    types:
      - opened

jobs:
  pr-action:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Post Docker Action PR Comment
        uses: sidd-harth-7/docker-action-pr-giphy-comment@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key: ${{ secrets.GIPHY_API_KEY }}
```

<Callout icon="lightbulb">
  Be sure your workflow has `issues: write` and `pull-requests: write` permissions so the action can post comments on PRs.
</Callout>

## 2. Identify the JavaScript Action on Marketplace

Search the GitHub Marketplace for the JavaScript version of the Giphy PR comment action. In this example, the identifier is:

```text theme={null}
sidd-harth-7/js-action-pr-giphy-comment@1.0.0-alpha
```

<Frame>
  ![The image shows a GitHub Marketplace page for a GitHub Action called "KodeKloud Giphy PR Comment," which is a sample action for demo purposes. It includes details like the version, a link to use the latest version, and contributor information.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876092/notes-assets/images/GitHub-Actions-Certification-Using-a-Javascript-Action-in-Workflow/github-marketplace-kodekloud-giphy-action.jpg)
</Frame>

## 3. Update Your Workflow to Include the JavaScript Action

Open `pr-thank-you.yml` and add a new step for the JavaScript action immediately after the Docker action:

```yaml theme={null}
on:
  pull_request:
    types:
      - opened

jobs:
  pr-action:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Post Docker Action PR Comment
        uses: sidd-harth-7/docker-action-pr-giphy-comment@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key: ${{ secrets.GIPHY_API_KEY }}

      - name: Post JavaScript Action PR Comment
        uses: sidd-harth-7/js-action-pr-giphy-comment@1.0.0-alpha
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key: ${{ secrets.GIPHY_API_KEY }}
```

| Feature             | Docker Action                                      | JavaScript Action                                     |
| ------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| Workflow Step Name  | Post Docker Action PR Comment                      | Post JavaScript Action PR Comment                     |
| Action Reference    | `sidd-harth-7/docker-action-pr-giphy-comment@main` | `sidd-harth-7/js-action-pr-giphy-comment@1.0.0-alpha` |
| Startup Performance | Slower (builds container)                          | Faster (runs natively on Node.js)                     |
| Version Pinning     | `@main`                                            | `@1.0.0-alpha`                                        |

## 4. Commit Changes and Open a Pull Request

Save your updated workflow on a branch, commit with a descriptive message, push the branch, and then create a pull request. This will trigger both actions on your new PR:

<Frame>
  ![The image shows a GitHub interface with a commit changes dialog open, where a user is updating a file named "pr-thank-you.yml" with a commit message.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876093/notes-assets/images/GitHub-Actions-Certification-Using-a-Javascript-Action-in-Workflow/github-commit-changes-dialog-pr-thank-you.jpg)
</Frame>

## 5. Monitor Workflow Runs and Logs

1. Go to the **Actions** tab in your repository.
2. Select the latest run of the “PR Thank You” workflow.
3. Expand the `pr-action` job to review logs for both the Docker and JavaScript steps.

<Frame>
  ![The image shows a GitHub Actions page with a list of workflow runs for a repository named "solar-system." Each entry displays details like the workflow name, status, and time of execution.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876094/notes-assets/images/GitHub-Actions-Certification-Using-a-Javascript-Action-in-Workflow/github-actions-solar-system-workflows.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub Actions workflow run summary, indicating a successful execution of a job named "pr-action" that includes building a Docker container and posting a JavaScript action PR comment with a Giphy GIF.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876095/notes-assets/images/GitHub-Actions-Certification-Using-a-Javascript-Action-in-Workflow/github-actions-pr-action-docker-summary.jpg)
</Frame>

Both actions will post separate “Thank You” GIF comments on your pull request, demonstrating how you can mix and reuse Docker and JavaScript actions from the GitHub Marketplace.

***

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [GitHub Marketplace](https://github.com/marketplace)
* [Creating a JavaScript Action](https://docs.github.com/actions/creating-actions/creating-a-javascript-action)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/428391ee-45d0-4e9c-9e06-78d0c5ff7657/lesson/a22a8257-8ba4-4389-aabe-e58089399d64" />
</CardGroup>
