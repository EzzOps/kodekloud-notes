# Using a Docker Action in Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Custom-Actions/Using-a-Docker-Action-in-Workflow/page

Learn to integrate a custom Docker container action in GitHub Actions to post a thank-you GIF on pull requests.

Learn how to integrate a reusable custom Docker container action across repositories. In this guide, we’ll invoke the **docker-action-pr-giphy-comment** action from the **solar-system** project to post a thank-you GIF on pull requests.

<Frame>
  ![The image shows a GitHub repository page for "docker-action-pr-giphy-comment," displaying files and recent commits.](https://kodekloud.com/kk-media/image/upload/v1752876081/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-repo-docker-action-pr-giphy.jpg)
</Frame>

## 1. Open the Target Repository

Navigate to your **solar-system** repository on GitHub:

<Frame>
  ![This image shows a GitHub repository page named "solar-system" with various files and folders listed, including workflows, images, and JavaScript files. The repository has no stars or forks and includes a recent pull request merge.](https://kodekloud.com/kk-media/image/upload/v1752876083/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-repo-solar-system-files.jpg)
</Frame>

## 2. Add the Giphy API Token

Your custom action fetches GIFs using the Giphy API. To configure:

1. Get an API key from the [Giphy Developer Portal](https://developers.giphy.com/).
2. In your repo, go to **Settings** > **Actions** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. Name it `GIPHY_API` and paste the API key.
5. Save.

<Frame>
  ![The image shows a GitHub repository settings page focused on "Actions secrets and variables," displaying options for managing environment and repository secrets.](https://kodekloud.com/kk-media/image/upload/v1752876084/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-repo-settings-actions-secrets.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub repository settings page where a new secret is being added under "Actions secrets," with the name "GIPHY\_API" and a secret key entered.](https://kodekloud.com/kk-media/image/upload/v1752876085/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-repo-settings-add-secret.jpg)
</Frame>

<Callout icon="lightbulb">
  Never expose your API keys in plain text. Always use GitHub Secrets for sensitive values.
</Callout>

## 3. Create the Workflow File

Checkout a branch (e.g., `main` or a feature branch) and add `.github/workflows/pr-thank-you.yml`:

<Frame>
  ![The image shows a GitHub interface where a user is creating or editing a file named "pr-thank" in the ".github/workflows" directory of a repository. The file content area is currently empty.](https://kodekloud.com/kk-media/image/upload/v1752876086/notes-assets/images/GitHub-Actions-Certification-Using-a-Docker-Action-in-Workflow/github-file-edit-pr-thank-workflows.jpg)
</Frame>

### Workflow Configuration

```yaml theme={null}
