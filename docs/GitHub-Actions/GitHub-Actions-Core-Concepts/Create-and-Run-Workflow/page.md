# Create and Run Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions/GitHub-Actions-Core-Concepts/Create-and-Run-Workflow/page

Learn to set up a simple GitHub Actions workflow that runs on every push, including repository creation and troubleshooting common errors.

In this guide, you’ll learn how to set up a simple GitHub Actions workflow that runs on every push. We’ll walk through creating a new repository, editing in the browser-based editor, installing the GitHub Actions extension, and troubleshooting a common error.

## 1. Initialize a New Public Repository

1. Navigate to GitHub and click **New** to create a repository.
2. Name it `actions-1`, set visibility to **Public**, and **Initialize with a README**.
3. Click **Create repository**.

<Frame>
  ![The image shows a GitHub interface for creating a new repository, with options to set the repository name, description, visibility, and initialize with a README file.](https://kodekloud.com/kk-media/image/upload/v1752876627/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-new-repository-interface.jpg)
</Frame>

## 2. Edit in the GitHub.dev Browser IDE

1. In your browser’s address bar, replace `github.com` with `github.dev` and press **Enter**.
2. Wait a few seconds for the VS Code–powered editor to load.
3. You can now edit, commit, and push files directly from the web IDE.

<Callout icon="lightbulb">
  Using **GitHub.dev** gives you instant access to a VS Code–like environment without any local setup.
</Callout>

<Frame>
  ![The image shows a GitHub.dev interface with a README.md file open, discussing GitHub Actions, and a sidebar displaying a search for "GitHub actions" in the extensions marketplace.](https://kodekloud.com/kk-media/image/upload/v1752876628/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-dev-readme-github-actions-sidebar.jpg)
</Frame>

## 3. Install the GitHub Actions Extension

For syntax highlighting, validation, and IntelliSense in YAML workflows:

1. Open the **Extensions** tab in the sidebar.
2. Search for **GitHub Actions**.
3. Click **Install** on the [GitHub Actions extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-github-actions).

<Frame>
  ![The image shows the GitHub Actions extension page in Visual Studio Code, displaying details about the extension, including its features and installation status.](https://kodekloud.com/kk-media/image/upload/v1752876630/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-actions-extension-vscode-details.jpg)
</Frame>

## 4. Create the Workflow File

1. In the file explorer, create a new folder: `.github/workflows/`.
2. Inside it, add `firstexample.yml`.

<Frame>
  ![The image shows a GitHub.dev interface with a file explorer open, displaying a .yml file and a README.md file. The interface prompts the user to sign in to GitHub to access repositories and GitHub Actions workflows.](https://kodekloud.com/kk-media/image/upload/v1752876631/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-dev-file-explorer-yml-readme.jpg)
</Frame>

3. Paste the following YAML:

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

<Callout icon="triangle-alert">
  YAML is indentation-sensitive. Ensure you use spaces (not tabs) and proper nesting to avoid validation errors like “mapping or sequence required.”
</Callout>

4. Commit and push your changes:

```bash theme={null}
git add .github/workflows/firstexample.yml
git commit -m "first workflow"
git push
```

## 5. Observe the Workflow Run

Since the workflow triggers on `push`, it runs immediately. Switch back to GitHub.com and click the **Actions** tab.

<Frame>
  ![The image shows a GitHub Actions setup page, offering options to configure workflows for deployment, such as deploying Node.js to Azure or using Terraform.](https://kodekloud.com/kk-media/image/upload/v1752876633/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-actions-workflow-setup-node-azure.jpg)
</Frame>

Refresh to see **My First Workflow** in the list.

<Frame>
  ![The image shows a GitHub Actions interface with a failed workflow run named "first workflow #1." It includes details of a job setup and logs indicating the use of Ubuntu as the operating system.](https://kodekloud.com/kk-media/image/upload/v1752876634/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-actions-failed-workflow-ubuntu.jpg)
</Frame>

Click the run to inspect:

<Frame>
  ![The image shows a GitHub Actions interface with a failed workflow run named "first workflow." It includes details about the job setup, operating system, and runner image.](https://kodekloud.com/kk-media/image/upload/v1752876635/notes-assets/images/GitHub-Actions-Create-and-Run-Workflow/github-actions-failed-workflow-first.jpg)
</Frame>

## 6. Troubleshoot: Missing Checkout Step

You’ll see this error in the logs:

```bash theme={null}
Run echo "My first GitHub Actions Job"
Run ls
Run cat README.md
cat: README.md: No such file or directory
Error: Process completed with exit code 1
```

By default, Actions runners don’t fetch your code. Add the checkout action before accessing files:

```yaml theme={null}
steps:
  - name: Checkout repository
    uses: actions/checkout@v3
  - name: Welcome message
    run: echo "My first GitHub Actions Job"
  # other steps...
```

## Workflow Components Overview

| Keyword   | Purpose                              | Example                      |
| --------- | ------------------------------------ | ---------------------------- |
| `name`    | Friendly workflow name               | `My First Workflow`          |
| `on`      | Event that triggers the workflow     | `push`, `pull_request`       |
| `jobs`    | Collection of tasks                  | `first_job`                  |
| `runs-on` | Defines the runner environment       | `ubuntu-latest`              |
| `steps`   | Ordered list of actions and commands | `actions/checkout@v3`, `run` |

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [actions/checkout@v3](https://github.com/actions/checkout)
* [GitHub Actions VS Code Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-github-actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/0ac6c98f-7100-471e-b9aa-037f25cb58d7/lesson/112a77bb-9a8b-49f3-a7b6-03e060eda049" />
</CardGroup>
