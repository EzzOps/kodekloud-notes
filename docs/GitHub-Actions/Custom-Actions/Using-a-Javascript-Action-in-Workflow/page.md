# Build container for action use: '/home/runner/work/_actions/sidd-harth-7/docker-action-pr-giphy-comment/main/Dockerfile'.
#1 [internal] load .dockerignore
#1 transferring context: 2B done
#1 DONE 0.0s
#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 448B done
#2 DONE 0.0s
#3 [internal] load metadata for docker.io/library/alpine:3.10
#3 DONE 0.0s
#6 [1/4] FROM docker.io/library/alpine:3.10@sha256:...
#6 DONE 0.1s
#9 [4/4] RUN chmod +x /entrypoint.sh
#9 DONE 0.3s
```

Then the container runs:

```bash theme={null}
/usr/bin/docker run --name 2d046f464e14829be2791b519b_32bdb \
  --label 461cec \
  --workdir /github/workspace \
  -e "INPUT_GITHUB_TOKEN=" \
  -e "INPUT_GIPHY_API_KEY=" \
  --rm \
  -v /home/runner/work/... \
  ...
```

<Callout icon="lightbulb">
  Continuous Docker builds can introduce latency. Consider using a [JavaScript action](/docs/actions/creating-actions/about-actions#javascript-actions) for faster startup.
</Callout>

## 5. Confirm the GIF Comment

After success, your pull request will display a “Thank you” comment with a GIF:

<Frame>
  ![The image shows a GitHub Actions workflow run summary for a repository, indicating that the "pr-action" job has succeeded.](https://kodekloud.com/kk-media/image/upload/v1752876598/notes-assets/images/GitHub-Actions-Using-a-Docker-Action-in-Workflow/github-actions-workflow-pr-action-success.jpg)
</Frame>

***

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Creating a Docker Container Action](https://docs.github.com/actions/creating-actions/creating-a-docker-container-action)
* [Giphy Developer API](https://developers.giphy.com/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/cdb7c2b7-442d-440c-a4f1-d6679733ffd8/lesson/44c1fc3e-458a-449d-9e2c-865be2da2642" />
</CardGroup>


# Using a Javascript Action in Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Custom-Actions/Using-a-Javascript-Action-in-Workflow/page

Integrate a JavaScript custom action with a Docker-based action to post GIF comments on pull requests in GitHub Actions workflows.

Integrate a JavaScript custom action alongside an existing Docker-based action to post two “thank you” GIF comments on pull requests. This guide walks through updating your workflow file to call both actions, committing the changes, and verifying the results in GitHub.

## Prerequisites

<Callout icon="lightbulb">
  * A GitHub repository with an existing workflow file (e.g., `.github/workflows/pr-thank-you.yml`)
  * `GITHUB_TOKEN` and `GIPHY_API_KEY` set in **Repository → Settings → Secrets**
  * Basic familiarity with YAML and [GitHub Actions](https://docs.github.com/actions)
</Callout>

## 1. Review the Existing Workflow

Open `.github/workflows/pr-thank-you.yml` and locate the step that invokes the Docker-based action:

```yaml theme={null}
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
      - name: Post PR Comment (Docker)
        uses: sidd-harth-7/docker-action-pr-giphy-comment@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key:  ${{ secrets.GIPHY_API_KEY }}
```

This configuration triggers whenever a pull request is opened and posts a GIF comment via the Docker action.

## 2. Add the JavaScript Action

Head over to the [GitHub Marketplace](https://github.com/marketplace) and search for the JavaScript version:\
**sidd-harth-7/js-action-pr-giphy-comment**, currently at tag `1.0.0-alpha`.

<Frame>
  ![The image shows a GitHub Marketplace page for the "KodeKloud Giphy PR Comment" action, which is a sample action for demo purposes. It includes options to use the latest version and shows contributor information.](https://kodekloud.com/kk-media/image/upload/v1752876599/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-marketplace-kodekloud-giphy-action.jpg)
</Frame>

Update your workflow to include both the Docker and JavaScript actions:

```yaml theme={null}
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
      - name: Post PR Comment (Docker)
        uses: sidd-harth-7/docker-action-pr-giphy-comment@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key:  ${{ secrets.GIPHY_API_KEY }}

      - name: Post PR Comment (JavaScript)
        uses: sidd-harth-7/js-action-pr-giphy-comment@1.0.0-alpha
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key:  ${{ secrets.GIPHY_API_KEY }}
```

| Action Type       | Version        | Purpose                            |
| ----------------- | -------------- | ---------------------------------- |
| Docker Action     | `@main`        | Builds a container and posts a GIF |
| JavaScript Action | `@1.0.0-alpha` | Executes a JS bundle to post a GIF |

## 3. Commit Changes and Open a Pull Request

Commit your updated workflow. You can commit directly or create a new branch for a pull request:

<Frame>
  ![The image shows a GitHub interface with a "Commit changes" dialog open, where a commit message is being entered for a file update. The user can choose to commit directly to a branch or create a new branch for a pull request.](https://kodekloud.com/kk-media/image/upload/v1752876600/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-commit-changes-dialog-interface.jpg)
</Frame>

Once you open the PR, GitHub Actions triggers the workflow:

<Frame>
  ![The image shows a GitHub pull request page for a project named "solar-system," with details about a pull request titled "Update pr-thank-you.yml added JS action." The pull request is open, with some checks pending and no conflicts with the base branch.](https://kodekloud.com/kk-media/image/upload/v1752876602/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-pull-request-solar-system-update.jpg)
</Frame>

## 4. Verify the Comments

After the workflow completes, check the pull request conversation. You should see two GIF comments—one from each action:

<Frame>
  ![The image shows a GitHub pull request page with comments featuring GIFs expressing gratitude for contributions.](https://kodekloud.com/kk-media/image/upload/v1752876603/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-pull-request-comments-gifs-gratitude.jpg)
</Frame>

## 5. Inspect the Workflow Run

Go to the **Actions** tab and select the latest run of your PR workflow:

<Frame>
  ![The image shows a GitHub Actions interface with a list of workflow runs, including details like event names, status, branches, and timestamps. The sidebar displays options for managing workflows, caches, deployments, and runners.](https://kodekloud.com/kk-media/image/upload/v1752876605/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-actions-workflow-runs-interface.jpg)
</Frame>

Under the `pr-action` job, you’ll see two distinct steps:

* **Docker Action**: Builds the image and posts its comment
* **JavaScript Action**: Runs the pre-built bundle and posts its comment

<Frame>
  ![The image shows a GitHub Actions workflow run page with a successful job titled "pr-action," which includes steps for building a Docker container and posting a pull request comment.](https://kodekloud.com/kk-media/image/upload/v1752876606/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-actions-pr-action-docker-workflow.jpg)
</Frame>

Finally, confirm both steps succeeded in the workflow summary:

<Frame>
  ![The image shows a GitHub Actions workflow run summary for a repository, indicating a successful job execution involving a JavaScript action for posting a PR comment with a Giphy link.](https://kodekloud.com/kk-media/image/upload/v1752876607/notes-assets/images/GitHub-Actions-Using-a-Javascript-Action-in-Workflow/github-actions-workflow-summary-success.jpg)
</Frame>

***

You’ve now successfully integrated a JavaScript custom action with your existing Docker action in the same workflow. Both can be versioned, published, and reused via the [GitHub Marketplace](https://github.com/marketplace).

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [GitHub Marketplace](https://github.com/marketplace)
* [Managing Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/cdb7c2b7-442d-440c-a4f1-d6679733ffd8/lesson/94329e6e-fd77-4d75-9b01-e00d7e61d208" />
</CardGroup>
