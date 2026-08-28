# Demo Setup Github repo according to DevOps best practice 02

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-01/Demo-Setup-Github-repo-according-to-DevOps-best-practice-02/page

This lesson covers enabling branch protection on GitHub and establishing a workflow using feature branches and pull requests.

Welcome back! In this lesson, we'll walk through enabling branch protection on GitHub and establish a workflow using feature branches and pull requests.

## Enabling Branch Protection

<Callout icon="lightbulb">
  Enabling branch protection helps maintain code quality and prevents direct pushes to critical branches.
</Callout>

1. In your repository, navigate to **Settings** > **Branches**.
2. Click **Add branch protection rule**.
3. Set **Branch name pattern** to `main`.
4. Enable **Require a pull request before merging**.
5. Uncheck **Require approvals** if you're working solo.
6. Scroll down and click **Create**.

| Branch Protection Option            | Description                                      | Status   |
| ----------------------------------- | ------------------------------------------------ | -------- |
| Require pull request before merging | Enforce all changes to go through a pull request | Enabled  |
| Require approvals                   | Mandate review approvals before merging          | Disabled |

<Frame>
  ![The image shows a GitHub settings page for creating a new branch protection rule, with options to require pull requests and approvals before merging into the main branch.](https://kodekloud.com/kk-media/image/upload/v1752875399/notes-assets/images/GCP-DevOps-Project-Demo-Setup-Github-repo-according-to-DevOps-best-practice-02/github-settings-branch-protection-rule.jpg)
</Frame>

Once created, your protected rule appears in the list:

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Branches" section, where the default branch is set to "main" and branch protection rules are being managed.](https://kodekloud.com/kk-media/image/upload/v1752875400/notes-assets/images/GCP-DevOps-Project-Demo-Setup-Github-repo-according-to-DevOps-best-practice-02/github-repo-settings-branches-main.jpg)
</Frame>

## Working with Feature Branches

<Callout icon="triangle-alert">
  Avoid committing directly to `main`. Always use a dedicated feature branch for your changes.
</Callout>

First, verify your current branch in VS Code:

```bash theme={null}
git branch
* main
```

### Creating a Feature Branch

Switch to a new branch for your task:

```bash theme={null}
git checkout -b feature/task-02
git branch
* feature/task-02
  main
```

### Updating the README

1. Open `README.md`.
2. Change the heading from `####` to `#` for an H1 title.
3. Preview your changes to confirm the update.

### Staging and Committing

Stage and commit the revision:

```bash theme={null}
git add README.md
git status
