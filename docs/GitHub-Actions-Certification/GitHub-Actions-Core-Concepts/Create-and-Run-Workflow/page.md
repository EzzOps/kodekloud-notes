# Create and Run Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-Core-Concepts/Create-and-Run-Workflow/page

Automate your CI/CD pipeline by defining workflows that build, test, and deploy your code on every push using GitHub Actions.

Automate your CI/CD pipeline by defining workflows that build, test, and deploy your code on every push. In this tutorial, you’ll set up a simple GitHub Actions workflow from scratch using the GitHub.dev editor and VS Code’s Actions extension.

| Step | Description                                           |
| ---- | ----------------------------------------------------- |
| 1    | Create a new GitHub repository                        |
| 2    | Open it in the GitHub.dev online editor (VS Code Web) |
| 3    | Install the GitHub Actions extension                  |
| 4    | Author your first workflow file                       |
| 5    | Commit, push, and trigger the workflow                |
| 6    | View, debug, and fix issues in your workflow runs     |

## Step 1: Create a New Repository

1. Sign in to GitHub and click **New**.
2. Name the repository `actions-1`, set it to **Public**, and initialize with a README.
3. Click **Create repository** to finish.

<Frame>
  ![The image shows a GitHub page for creating a new repository, with fields for the repository name, description, visibility options, and initialization settings.](https://kodekloud.com/kk-media/image/upload/v1752876121/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-new-repository-creation-page.jpg)
</Frame>

## Step 2: Open in Visual Studio Code (GitHub.dev)

In your repo’s URL, replace `github.com` with `github.dev` to launch the VS Code–style online editor:

```text theme={null}
https://github.dev/your-username/actions-1
```

<Frame>
  ![The image shows a GitHub repository page with the name "actions-1" and an initial commit. The repository is public and has no stars, forks, or releases.](https://kodekloud.com/kk-media/image/upload/v1752876122/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-repo-actions-1-initial-commit.jpg)
</Frame>

<Callout icon="lightbulb">
  GitHub.dev provides the full VS Code keybindings and interface in your browser—no local install required.
</Callout>

## Step 3: Install the GitHub Actions Extension

1. Open the **Extensions** pane (⇧⌘X or Ctrl+Shift+X).
2. Search for **GitHub Actions** and install the official extension.
3. Enjoy syntax validation, autocompletion, and inline error checking for `.yml` workflows.

<Frame>
  ![The image shows a code editor with a README.md file open, discussing GitHub Actions, alongside a sidebar displaying a list of GitHub Actions extensions.](https://kodekloud.com/kk-media/image/upload/v1752876123/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/code-editor-readme-github-actions.jpg)
</Frame>

<Frame>
  ![The image shows the GitHub Actions extension page in Visual Studio Code, detailing its features and options to disable or uninstall it.](https://kodekloud.com/kk-media/image/upload/v1752876124/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-actions-extension-vscode-features.jpg)
</Frame>

## Step 4: Create the Workflow File

In the Explorer, add a `.github/workflows` folder and create `firstexample.yml`:

<Frame>
  ![The image shows a GitHub.dev interface with a file explorer open, displaying a YAML file and a README file. There are options to continue working in GitHub Codespaces or clone the repository locally.](https://kodekloud.com/kk-media/image/upload/v1752876125/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-dev-file-explorer-yaml-readme.jpg)
</Frame>

Paste the following workflow definition:

```yaml theme={null}
name: My First Workflow
on: push

jobs:
  first_job:
    runs-on: ubuntu-latest
    steps:
      - name: Welcome message
        run: echo "My first GitHub Actions Job"
      - name: List files
        run: ls
      - name: Read file
        run: cat README.md
```

Save the file—VS Code will validate the YAML against the Actions schema.

<Frame>
  ![The image shows a Visual Studio Code interface with a YAML file open, displaying a problem message about an expected scalar value. The file is part of a GitHub repository, and the problem is highlighted in the "Problems" tab.](https://kodekloud.com/kk-media/image/upload/v1752876126/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/visual-studio-code-yaml-problem-message.jpg)
</Frame>

## Step 5: Commit and Push the Workflow

```bash theme={null}
git add .github/workflows/firstexample.yml
git commit -m "Add first workflow"
git push
```

Because the workflow triggers on `push`, GitHub will immediately enqueue a run.

## Step 6: View the Workflow Run

1. On GitHub, select the **Actions** tab.
2. Locate **My First Workflow** in the list.
3. Explore starter workflows for other languages or cloud deployments.

<Frame>
  ![The image shows a GitHub Actions setup page with options for configuring workflows, including deployment to various cloud services like Azure, Amazon ECS, and Google Cloud.](https://kodekloud.com/kk-media/image/upload/v1752876127/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-actions-workflow-setup-cloud.jpg)
</Frame>

Click your workflow to see its status:

<Frame>
  ![The image shows a GitHub Actions interface with a failed workflow run named "first workflow" and a job called "first\_job" that completed with an error.](https://kodekloud.com/kk-media/image/upload/v1752876128/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-actions-failed-workflow-first-job.jpg)
</Frame>

## Step 7: Inspect and Debug the Job

Open the job logs to review each step. You’ll see setup messages followed by your custom commands:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a failed job named "first\_job," displaying setup details and logs.](https://kodekloud.com/kk-media/image/upload/v1752876129/notes-assets/images/GitHub-Actions-Certification-Create-and-Run-Workflow/github-actions-failed-job-logs.jpg)
</Frame>

<Callout icon="triangle-alert">
  By default, the runner does **not** check out your repository. Without your code present, the `ls` and `cat` commands will fail.
</Callout>

## Fixing the Checkout Step

To resolve missing files, insert the official checkout action at the top of your steps:

```yaml theme={null}
steps:
  - name: Checkout repository
    uses: actions/checkout@v3
  # ...rest of your steps
```

This ensures your workflow has access to the project files before running commands.

## What's Next?

* Explore advanced [GitHub Actions triggers](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows).
* Integrate matrix builds, secrets, and environment variables.
* Deploy to cloud services using official actions for AWS, Azure, or GCP.

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [actions/checkout@v3](https://github.com/actions/checkout)
* [VS Code Marketplace: GitHub Actions Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/54711be0-66e6-461b-b935-f77d78a5e000/lesson/deb475d7-08a5-40d0-b9c8-39322683c5dd" />
</CardGroup>
