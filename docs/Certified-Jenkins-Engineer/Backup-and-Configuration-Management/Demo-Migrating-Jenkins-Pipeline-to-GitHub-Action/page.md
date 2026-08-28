# Demo Migrating Jenkins Pipeline to GitHub Action

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/page

This tutorial explains how to migrate Jenkins jobs to GitHub Actions workflows using the GitHub Actions Importer.

In this tutorial, you'll learn how to migrate existing Jenkins jobs into GitHub Actions workflows using the GitHub Actions Importer.

## Prerequisites

* A Jenkins account or organization with pipelines to migrate
* A Jenkins personal API token with read or admin permissions
* Docker installed (required by the importer)
* GitHub CLI (`gh`) installed and authenticated

<Frame>
  ![The image shows a GitHub documentation page about migrating from Jenkins to GitHub Actions using the GitHub Actions Importer. It includes prerequisites, limitations, and installation instructions for the CLI extension.](https://kodekloud.com/kk-media/image/upload/v1752870416/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/github-actions-migration-jenkins.jpg)
</Frame>

<Callout icon="triangle-alert">
  Some features cannot be migrated automatically:

  | Limitation                | Impact                                |
  | ------------------------- | ------------------------------------- |
  | Scripted pipelines        | Not supported—only declarative syntax |
  | Secrets & unknown plugins | Must be recreated or handled manually |
</Callout>

***

## 1. Install GitHub CLI & Importer Extension

On Ubuntu, add the GitHub CLI repository and install:

```bash theme={null}
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
  && sudo mkdir -p /etc/apt/keyrings \
  && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
     | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && sudo chmod 644 /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) \
     signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] \
     https://cli.github.com/repos/github/cli/releases/apt/ \
     $(lsb_release -cs) main" \
     | sudo tee /etc/apt/sources.list.d/github-cli.list \
  && sudo apt update \
  && sudo apt install gh -y
```

Install the GitHub Actions Importer:

```bash theme={null}
gh extension install github/gh-actions-importer
gh actions-importer -h
```

***

## 2. Authenticate with GitHub

Log in to GitHub via the CLI:

```bash theme={null}
gh auth login
```

Follow the browser prompts to authorize.

<Frame>
  ![The image shows a GitHub authorization page for the GitHub CLI, requesting access to a user's account and various organizations. There are options to cancel or authorize the application.](https://kodekloud.com/kk-media/image/upload/v1752870417/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/github-cli-authorization-page.jpg)
</Frame>

***

## 3. Configure Importer Credentials

You need two tokens:

1. **GitHub Personal Access Token (classic)**
   * Scopes: `repo`, `workflow`
   * Create under **Settings → Developer settings → Personal access tokens → Tokens (classic)**

<Frame>
  ![The image shows a GitHub page for creating a new personal access token, with options to set a note, expiration date, and select scopes for the token.](https://kodekloud.com/kk-media/image/upload/v1752870418/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/github-personal-access-token-creation.jpg)
</Frame>

2. **Jenkins API Token**
   * Go to **People → \[your user] → Configure → API Token**
   * Copy it before leaving the page

<Frame>
  ![The image shows a Jenkins dashboard with a list of build jobs, their statuses, last success and failure times, and durations. The interface includes navigation options on the left and user account details on the top right.](https://kodekloud.com/kk-media/image/upload/v1752870420/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/jenkins-dashboard-build-jobs-statuses.jpg)
</Frame>

Run the configuration command and answer prompts:

```bash theme={null}
gh actions-importer configure
```

* Choose **Jenkins**
* Enter your GitHub token & base URL (`https://github.com`)
* Enter your Jenkins token, username & base URL (e.g. `http://64.227.187.25:8080/`)

***

## 4. Update the Importer

Keep the extension up to date:

```bash theme={null}
gh actions-importer update
```

***

## 5. Audit & Forecast (Optional)

Review your Jenkins jobs before migration:

```bash theme={null}
gh actions-importer audit jenkins --output-dir tmp/audit
```

Estimate GitHub Actions runner usage (requires a Jenkins plugin):

```bash theme={null}
gh actions-importer forecast jenkins
```

<Frame>
  ![The image shows a GitHub Docs page about migrating from Jenkins with GitHub Actions Importer, detailing steps for forecasting potential build runner usage. The page includes navigation links and a sidebar with related topics.](https://kodekloud.com/kk-media/image/upload/v1752870421/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/github-actions-migrate-jenkins-docs.jpg)
</Frame>

***

## 6. Dry Run a Jenkins Job

Locate your full Jenkins job URL:

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of jobs with their statuses, last success, last failure, and duration. The interface includes options for managing Jenkins, viewing job configurations, and build executor status.](https://kodekloud.com/kk-media/image/upload/v1752870423/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/jenkins-dashboard-job-statuses.jpg)
</Frame>

Execute a dry-run to preview the workflow:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://64.227.187.25:8080/job/Generate%20ASCII%20Artwork/ \
  --output-dir tmp/dry-run
```

Inspect the generated workflow YAML:

```bash theme={null}
cat tmp/dry-run/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
```

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  workflow_dispatch:
env:
  # TimestamperBuildWrapper was not converted
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4
      - name: run command
        shell: bash
        run: |
          # Fetch a piece of advice
          curl -s https://api.adviceslip.com/advice > advice.json
          cat advice.json
          # Validate word count
          jq -r .slip.advice advice.json > advice.message
          [ $(wc -w < advice.message) -gt 5 ] \
            || (echo "Advice has 5 words or less" && exit 1)
          # Install cowsay and display
          sudo apt-get install cowsay -y
          export PATH="$PATH:/usr/games:/usr/local/games"
          cowsay -f "$(ls /usr/share/cowsay/cows | shuf -n 1)" \
            < advice.message
```

***

## 7. Migrate to GitHub Actions

Prepare your target repository (e.g., `jenkins-to-actions`):

<Frame>
  ![The image shows a GitHub repository page titled "jenkins-to-actions" with an initial commit made 16 minutes ago. The repository is public and contains a README file.](https://kodekloud.com/kk-media/image/upload/v1752870424/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/jenkins-to-actions-repo-initial-commit.jpg)
</Frame>

Run the migration:

```bash theme={null}
gh actions-importer migrate jenkins \
  --source-url http://64.227.187.25:8080/job/Generate%20ASCII%20Artwork/ \
  --target-url https://github.com/jenkins-kk-demo/jenkins-to-actions \
  --output-dir tmp/migrate
```

A pull request will be created automatically:

<Frame>
  ![The image shows a GitHub pull request page titled "Convert Generate\_ASCII\_Artwork to GitHub Actions," with details about the commit and options to merge the pull request.](https://kodekloud.com/kk-media/image/upload/v1752870426/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/github-pull-request-convert-actions.jpg)
</Frame>

Merge the PR to land the workflow in `.github/workflows/generate_ascii_artwork.yml`:

```bash theme={null}
cat .github/workflows/generate_ascii_artwork.yml
```

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  workflow_dispatch:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: run command
        shell: bash
        run: |
          curl -s https://api.adviceslip.com/advice > advice.json
          jq -r .slip.advice advice.json > advice.message
          [ $(wc -w < advice.message) -gt 5 ] \
            || (echo "Advice has 5 words or less" && exit 1)
          sudo apt-get install cowsay -y
          export PATH="$PATH:/usr/games:/usr/local/games"
          cowsay -f "$(ls /usr/share/cowsay/cows | shuf -n 1)" \
            < advice.message
```

***

## 8. Run the Workflow

Trigger the workflow manually or push to `main`:

<Frame>
  ![The image shows a GitHub Actions interface with a workflow named "Generate\_ASCII\_Artwork" that has been manually run. The interface includes options for managing workflows and running them.](https://kodekloud.com/kk-media/image/upload/v1752870427/notes-assets/images/Certified-Jenkins-Engineer-Demo-Migrating-Jenkins-Pipeline-to-GitHub-Action/github-actions-generate-ascii-artwork.jpg)
</Frame>

After completion, check the logs to see your ASCII artwork output.

***

## Links & References

* [GitHub CLI Documentation](https://cli.github.com/)
* [gh-actions-importer Repository](https://github.com/github/gh-actions-importer)
* [Jenkins Documentation](https://www.jenkins.io/doc/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/a3c3de7d-f9ef-4898-935d-fbe99c18e10c" />
</CardGroup>
