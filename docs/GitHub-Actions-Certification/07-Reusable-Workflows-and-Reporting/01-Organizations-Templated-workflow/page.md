# 1. Create directory and enter it
mkdir actions-runner && cd actions-runner

# 2. Download the runner package
curl -L -o actions-runner-linux-x64-2.315.0.tar.gz \
  https://github.com/actions/runner/releases/download/v2.315.0/actions-runner-linux-x64-2.315.0.tar.gz

# 3. (Optional) Verify checksum
echo "6362646b67613c6981db76f4d25e68e463a9af2cc8d16e31bfeabe39153606a0 actions-runner-linux-x64-2.315.0.tar.gz" \
  | shasum -a 256 -c

# 4. Extract
tar xzf actions-runner-linux-x64-2.315.0.tar.gz

# 5. Configure (replace URL and token)
./config.sh \
  --url https://github.com/enterprises/kodekloud-training-enterprise \
  --token BDEPF64QGNY4SWJQPXUFF363GDQT42

# 6. Start the runner
./run.sh
```

During setup, assign this runner to your **default enterprise runner group** and add a label such as `enterprise`.

Once up, you’ll see logs like:

<Frame>
  ![The image shows a terminal window on the KodeKloud platform, displaying a GitHub Actions self-hosted runner registration process with successful connection and runner settings prompts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876273/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/kodekloud-github-actions-runner-registration.jpg)
</Frame>

***

## 6. Verify Runner Registration

Back in the enterprise’s **Runners** list, your new self-hosted runner appears with labels and an idle status:

<Frame>
  ![The image shows a GitHub Actions settings page for an enterprise account, displaying options for managing runners, including a self-hosted Linux runner.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876274/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-actions-enterprise-settings-runners.jpg)
</Frame>

Switch to the organization’s **Runner groups** view to confirm it’s available there too:

<Frame>
  ![The image shows a GitHub settings page for managing runner groups, with options for repository and workflow access, and a list of runners including an "enterprise-linux-runner" that is currently idle.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876275/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-settings-runner-groups-management.jpg)
</Frame>

***

## 7. Create a New Repository and Workflow

1. Disable the organization’s default runner for public repos to enforce enterprise runners.
2. Go to **Repositories > New repository** in your organization:

<Frame>
  ![The image shows a GitHub settings page for an organization, specifically focusing on "Runner groups" for managing access to shared organization runners. It includes options to create a new runner group and displays existing groups with their details.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876277/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-settings-runner-groups-management-2.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub organization page with a list of repositories and a dropdown menu for creating new repositories or organizations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876278/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-organization-repositories-dropdown-menu.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub interface for creating a new repository, with options to set the repository name, visibility, and initialize with a README file.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876279/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-new-repository-interface.jpg)
</Frame>

3. Initialize with a README and clone locally:

```bash theme={null}
git clone git@github.com:kodekloud-training-organization/demo-repo.git
cd demo-repo
```

4. Add a workflow at `.github/workflows/demo.yaml`:

```yaml theme={null}
name: Exploring GitHub Enterprise Action Features

on:
  push:
  workflow_dispatch:

jobs:
  demo_job:
    runs-on: self-hosted
    steps:
      - name: Hello
        run: echo "Hello GitHub Enterprise!!"

      - name: External Call using cURL
        run: curl -v http://httpbin.org/ip
```

5. Commit and push:

```bash theme={null}
git add .
git commit -m "Add demo workflow for enterprise runner"
git push
```

***

## 8. Review Workflow Execution

Navigate to the repository’s **Actions** tab. You should see `demo_job` queued and running on your self-hosted enterprise runner:

<Frame>
  ![The image shows a GitHub Actions interface with a job named "demo\_job" that has successfully completed. It includes details about the runner and setup steps.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876280/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-actions-demo-job-successful.jpg)
</Frame>

***

## Next Steps

In **Part 2**, we’ll cover how to move runners between groups and update labels directly from the GitHub UI.

***

## Links and References

* [GitHub Actions Runner Groups](https://docs.github.com/en/enterprise-server@latest/admin/configuration/using-runner-groups-in-an-enterprise)
* [Self-Hosted Runners Documentation](https://docs.github.com/actions/hosting-your-own-runners)
* [GitHub Enterprise Server](https://docs.github.com/en/enterprise-server)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/9b181319-216b-42b5-8069-9d56650f2d53/lesson/7ccb09f7-911c-454c-99a8-cf5f1ff9fac9" />
</CardGroup>


# Organizations Templated workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Organizations-Templated-workflow/page

This guide explains how to create and use organization-wide starter workflows for GitHub Actions to enhance consistency and reduce duplication.

In this guide, you’ll discover how to define and consume organization-wide starter workflows for GitHub Actions. By centralizing your CI/CD logic in a special `.github` repository, teams can pick prebuilt workflow templates across all repos—boosting consistency and cutting down duplication.

<Frame>
  ![The image shows a GitHub Docs page about creating starter workflows for organizations, with an overview and navigation menu on the left.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876311/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-docs-starter-workflows-overview.jpg)
</Frame>

## 1. Define a Starter Workflow Template

To publish a reusable workflow:

1. Create a **public** repository named `.github` at the root of your organization.
2. Inside `.github`, add a folder called `workflow-templates`.
3. Add a workflow YAML file (for example, `org-ci-starter.yml`).
4. Add a matching metadata file named `org-ci-starter.properties.json`.

<Callout icon="lightbulb">
  The metadata JSON controls how your template appears in the workflow picker.

  * `name` and `description` define the display text.
  * `iconName` lets you specify an optional SVG icon.
  * `categories` and `filePatterns` help users find the right template.
</Callout>

Table: Starter Template Files

| File Path                                               | Purpose                      | Example Filename                 |
| ------------------------------------------------------- | ---------------------------- | -------------------------------- |
| `.github/workflow-templates/{template}.yml`             | Workflow definition          | `org-ci-starter.yml`             |
| `.github/workflow-templates/{template}.properties.json` | Display metadata             | `org-ci-starter.properties.json` |
| (Optional) `.github/workflow-templates/{icon}.svg`      | Custom icon for the template | `kode-kloud-icon.svg`            |

Example workflow (`.github/workflow-templates/org-ci-starter.yml`):

```yaml theme={null}
name: Octo Organization CI
on:
  push:
    branches: [ $default-branch ]
  pull_request:
    branches: [ $default-branch ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
```

Example metadata (`.github/workflow-templates/org-ci-starter.properties.json`):

```json theme={null}
{
  "name": "Octo Organization Workflow",
  "description": "CI starter workflow for Go projects.",
  "iconName": "Example-icon",
  "categories": ["Go"],
  "filePatterns": ["package.json$", "Dockerfile", "\\.md$"]
}
```

***

## 2. Create Your GitHub Organization

If you don’t already have an organization, set one up:

1. Click your profile photo → **Your organizations**.
2. Select **New organization**, choose the **Free** plan.
3. Enter an organization name and contact email.
4. Complete account verification and accept the terms.
5. Skip adding members initially—you can invite collaborators later.

<Frame>
  ![The image shows a GitHub settings page for a personal account, indicating that the user is not a member of any organizations. There are options for account settings and transforming the account into an organization.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876312/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-settings-personal-account-options.jpg)
</Frame>

<Frame>
  ![The image shows a comparison of three GitHub pricing plans: Free, Team, and Enterprise, detailing their features and costs.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876314/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-pricing-plans-comparison.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub page for setting up an organization, with fields for organization name, contact email, and account verification.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876316/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-organization-setup-page.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub account verification page with a large green checkmark indicating successful verification. Below, there are options for add-ons and terms of service acceptance.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876317/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-account-verification-success-checkmark.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub page for adding members to the "kodekloud-training-organization," with options to search by username or email and buttons to complete setup or skip the step.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876319/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-add-members-kodekloud-training.jpg)
</Frame>

Once your organization is ready, you’ll land on its settings dashboard:

<Frame>
  ![The image shows the settings page of a GitHub organization named "kodekloud-training-organization," displaying options for general settings, profile picture, and social accounts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876320/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/kodekloud-training-organization-settings-page.jpg)
</Frame>

***

## 3. Set Up the `.github` Repository

Within your organization:

1. Click **New repository** → Enter **.github** as the name.
2. Set **Visibility** to Public.
3. Initialize with a README (optional) and click **Create repository**.

<Frame>
  ![The image shows a GitHub interface for creating a new repository under the "kodekloud-training-organization" with options to set the repository name, description, visibility, and initialization settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876322/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-new-repository-kodekloud-training.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub page for creating a new repository, with options to set the repository as public or private, add a README file, and choose a license. The "Create repository" button is visible at the bottom.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876323/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-create-repository-page-options.jpg)
</Frame>

Next, create the `workflow-templates/` folder in the `.github` repo—either via the web editor or locally:

<Frame>
  ![The image shows a GitHub documentation page about creating starter workflows, with instructions and a YAML code snippet.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876325/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-starter-workflows-documentation-yaml.jpg)
</Frame>

Add your template files, for example:

<Frame>
  ![The image shows a GitHub repository interface in a code editor, displaying a file named "nodejs-ci-starter-workflow.yml" within a ".github" directory.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876326/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-repo-code-editor-nodejs-workflow.jpg)
</Frame>

After committing, the repo structure should resemble:

<Frame>
  ![The image shows a GitHub repository page for "kodekloud-training-organization/.github" with folders and files like "workflow-templates" and "README.md" displayed. It also includes options for adding files and viewing repository details.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876328/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-repo-kodekloud-training-files.jpg)
</Frame>

***

## 4. Example: Node.js CI Starter Workflow

Create `.github/workflow-templates/nodejs-ci-starter-workflow.yml`:

```yaml theme={null}
name: KodeKloud Demo Organization NodeJS CI
on:
  push:
    branches: [ $default-branch ]
  pull_request:
    branches: [ $default-branch ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      - name: Setup Node.js (20.x)
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
      - name: Install Dependencies
        run: npm install
      - name: Run Tests
        run: npm test --if-present
      - name: Generate Coverage
        run: npm run coverage --if-present
```

Add metadata at `.github/workflow-templates/nodejs-ci-starter-workflow.properties.json`:

```json theme={null}
{
  "name": "KodeKloud Demo Organization NodeJS CI",
  "description": "Starter workflow for Node.js projects.",
  "iconName": "kode-kloud-icon",
  "categories": ["NPM Config"]
}
```

You may also upload an SVG icon (e.g., `kode-kloud-icon.svg`) to the same folder.

***

## 5. Consume the Starter Workflow

In any new or existing repo under your org:

1. Click **New repository**, initialize with a README if desired.
2. Navigate to the **Actions** tab.

<Frame>
  ![The image shows a GitHub interface for creating a new repository, with options to set the repository name, visibility, and initialize with a README file.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876329/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-new-repository-interface.jpg)
</Frame>

Below GitHub’s built-in suggestions, you’ll see your organization’s starter templates:

<Frame>
  ![The image shows a GitHub Actions setup page, suggesting workflows for a repository, including a simple workflow and a NodeJS CI starter workflow by KodeKloud.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876330/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-actions-workflows-nodejs-setup.jpg)
</Frame>

You can also filter by deployment, security, CI, and more:

<Frame>
  ![The image shows a GitHub Actions interface with various deployment and security workflow options, such as deploying Node.js to Azure and Amazon ECS, and performing CodeQL analysis.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876332/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-actions-deployment-security-workflows.jpg)
</Frame>

Click **Configure** on your Node.js CI starter. GitHub will generate the YAML and replace `$default-branch` (e.g., `main`):

```yaml theme={null}
name: KodeKloud Demo Organization NodeJS CI
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      - name: Setup Node.js (20.x)
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
      - name: Install Dependencies
        run: npm install
      - name: Run Tests
        run: npm test --if-present
      - name: Generate Coverage
        run: npm run coverage --if-present
```

Customize steps or add new jobs, then commit to kick off the workflow.

***

## 6. Configure Runners for Organization Repos

If your workflow remains queued, verify runner access:

1. In the repo: **Settings > Actions > Runners**—you may see none configured.

<Frame>
  ![The image shows a GitHub repository settings page for configuring runners, indicating that no runners are currently configured.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876333/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-repo-settings-no-runners.jpg)
</Frame>

2. At the org level: **Settings > Actions > Runners**. The default runner group might exclude public repos.

<Frame>
  ![The image shows a GitHub organization settings page for "kodekloud-training-organization," specifically focusing on the "Runners" section under GitHub Actions. It displays options for managing self-hosted and GitHub-hosted runners, with a standard GitHub-hosted runner listed.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876334/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-organization-settings-runners-actions.jpg)
</Frame>

3. Edit the default group to allow all repositories (including public).

<Frame>
  ![The image shows a GitHub settings page for an organization, specifically focusing on configuring runner groups for GitHub Actions. It includes options for group name, repository access, and workflow access.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876335/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-settings-runner-groups-actions.jpg)
</Frame>

Once configured, GitHub-hosted runners will pick up jobs:

<Frame>
  ![The image shows a GitHub Actions workflow run for a Node.js project, where the "build" job has failed. The interface displays the setup steps and logs related to the job execution.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876337/notes-assets/images/GitHub-Actions-Certification-Organizations-Templated-workflow/github-actions-nodejs-build-failed.jpg)
</Frame>

<Callout icon="triangle-alert">
  If no runners are permitted, workflows will remain queued indefinitely. Always verify your runner group settings after creating or migrating repositories.
</Callout>

***

## Links and References

* [GitHub Actions Starter Workflows](https://docs.github.com/actions/learn-github-actions/starter-workflows)
* [Creating a GitHub Organization](https://docs.github.com/organizations)
* [Managing Self-hosted Runners](https://docs.github.com/actions/hosting-your-own-runners)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/25ac82cb-c1dd-45d8-929f-7c0bd0ec0a95" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/2427a5f3-4e9e-4b49-9944-f592476c5657" />
</CardGroup>
