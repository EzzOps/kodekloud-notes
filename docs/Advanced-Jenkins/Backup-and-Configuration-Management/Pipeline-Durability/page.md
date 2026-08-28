# Install GitHub CLI on Debian/Ubuntu
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update \
  && sudo apt install gh -y
```

Install the GitHub Actions Importer extension:

```bash theme={null}
gh extension install github/gh-actions-importer
```

View the importer help:

```bash theme={null}
gh actions-importer -h
```

Sample (truncated) output:

```text theme={null}
Options:
  -?, -h, --help  Show help and usage information

Commands:
  update      Update to the latest version of GitHub Actions Importer.
  version     Display the version of GitHub Actions Importer.
  configure   Start an interactive prompt to configure credentials used to authenticate with your CI server(s).
  audit       Plan your CI/CD migration by analyzing your current CI/CD footprint.
  forecast    Forecast GitHub Actions usage from historical pipeline utilization.
  dry-run     Convert a pipeline to a GitHub Actions workflow and output its yaml file.
  migrate     Convert a pipeline and push a branch + create a pull request (see docs).
```

## Authenticate with `gh`

Log in and connect `gh` to your GitHub account:

```bash theme={null}
gh auth login
```

Follow the interactive prompts:

* Select `GitHub.com`.
* Use `HTTPS` for Git operations.
* Authenticate via browser (device/web flow).

After authorizing in the browser, `gh` will be linked to your account and allow the extension to push branches and create PRs.

<Frame>
  <img alt="A GitHub OAuth authorization page showing a list of organizations with checkmarks for requested access and buttons to &#x22;Cancel&#x22; or &#x22;Authorize github.&#x22; Several org icons and names are visible in the middle of the dark-themed screen." />
</Frame>

## Configure GitHub Actions Importer credentials

Run the importer’s interactive configuration to store credentials used during migration:

```bash theme={null}
gh actions-importer configure
```

When prompted, provide:

* GitHub Personal Access Token (classic) — include `workflow` scope (and `repo` if needed).
* Jenkins username and Jenkins API token.
* Base URLs for GitHub (`https://github.com`) and your Jenkins instance.

How to get tokens

* Generate a GitHub token: Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic). See GitHub docs: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
* Generate a Jenkins API token: User → Configure → Add new API token in Jenkins. See Jenkins docs: [https://www.jenkins.io/doc/book/managing/creating-api-tokens/](https://www.jenkins.io/doc/book/managing/creating-api-tokens/). Copy tokens immediately — Jenkins shows API tokens only once.

<Frame>
  <img alt="A screenshot of a Jenkins user configuration page for the account &#x22;siddharth,&#x22; showing fields for Full Name and Description and an API Token section with a token labeled &#x22;github importer.&#x22; The left sidebar lists navigation items (Status, Builds, Configure, etc.) and Save/Apply buttons are visible at the bottom." />
</Frame>

The `configure` command writes environment variables used by the importer (`JENKINS_USERNAME`, `JENKINS_ACCESS_TOKEN`, `GITHUB_TOKEN`, etc.), so subsequent commands can access Jenkins and GitHub.

## Update the importer image

Before running conversions, update the importer container image:

```bash theme={null}
gh actions-importer update
```

Expected output:

```text theme={null}
Updating ghcr.io/actions-importer/cli:latest...
ghcr.io/actions-importer/cli:latest up-to-date
```

## Audit and forecast (optional)

* `gh actions-importer audit` enumerates discovered Jenkins jobs and reports conversion readiness.
* `gh actions-importer forecast` estimates GitHub Actions runtime usage based on historical builds (Jenkins may need plugins to expose build history).

Example audit:

```bash theme={null}
gh actions-importer audit jenkins --output-dir tmp/audit
```

This walkthrough skips audit/forecast and proceeds to converting a job using `dry-run`.

## Dry-run: convert a Jenkins job to a workflow YAML

Use `dry-run` to convert a single Jenkins job and write the generated workflow YAML to a directory. Replace the `--source-url` with your Jenkins job URL:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url "http://64.227.187.25:8080/job/Generate%20ASCII%20Artwork/" \
  --output-dir tmp/dry-run
```

Authentication errors example:

```text theme={null}
There was an error extracting the Jenkins pipeline (http://64.227.187.25:8080/job/Generate%20ASCII%20Artwork/)
Message: Unable to fetch pipeline configuration for 'Generate ASCII Artwork'
Unable to authenticate. Please verify the `JENKINS_ACCESS_TOKEN` and `JENKINS_USERNAME` variables are set to values that have access to the jobs being converted.
(GET 401) Unauthorized: http://64.227.187.25:8080/job/Generate%20ASCII%20Artwork/config.xml
```

If you see authentication failures, re-generate or re-enter the Jenkins API token with `gh actions-importer configure` and retry.

Example of the generated workflow YAML from `dry-run` (excerpt):

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  workflow_dispatch:
env:
  # TimestamperBuildWrapper was not converted because the behavior is available by default in GitHub Actions and/or it is not configurable
jobs:
  build:
    runs-on:
      - ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: run command
        shell: bash
        run: |-
          # Build a message by invoking ADVICESLIP API
          curl -s https://api.adviceslip.com/advice > advice.json
          cat advice.json
          # Test to make sure the advice message has more than 5 words.
          cat advice.json | jq -r .slip.advice > advice.message
          [ $(wc -w < advice.message) -gt 5 ] && echo "Advice has more than 5 words" || (echo "Advice - $(cat advice.message) has 5 words or less" && exit 1)
          # Deploy
          sudo apt-get install cowsay -y
          export PATH="$PATH:/usr/games:/usr/local/games"
          cat advice.message | cowsay -f $(ls /usr/share/cowsay/cows | shuf -n 1)
```

This output shows:

* The importer created a workflow named `Generate_ASCII_Artwork`.
* It uses `workflow_dispatch` (manual run) and a `build` job on `ubuntu-latest`.
* The job includes `actions/checkout` and shell commands ported from the original Jenkins job.

## Migrate: create a branch and pull request in GitHub

To push the generated workflow into a repository and open a PR, use `migrate`. Provide the Jenkins source URL and the GitHub target repository:

```bash theme={null}
gh actions-importer migrate jenkins \
  --source-url "http://64.227.187.25:8080/job/Generate%20ASCII%20Artwork/" \
  --target-url "https://github.com/your-org/your-repo" \
  --output-dir tmp/migrate
```

Successful example output:

```text theme={null}
[...]
Logs: 'tmp/migrate/log/actions-importer-20220916-014033.log'
Pull request: 'https://github.com/your-org/your-repo/pull/1'
```

What `migrate` does:

* Creates a branch.
* Commits `.github/workflows/<workflow>.yml`.
* Opens a pull request in the target repository.

Representative diff created by the importer (excerpt):

```diff theme={null}
+ name: Generate_ASCII_Artwork
+ on:
+   workflow_dispatch:
+ env:
+   # TimestamperBuildWrapper was not converted because the behavior is available by default in
+   # GitHub Actions and/or it is not configurable
+ jobs:
+   build:
+     runs-on:
+       - ubuntu-latest
+     steps:
+       - name: checkout
+         uses: actions/checkout@v4.1.0
+       - name: run command
+         shell: bash
+         run: |-
+           # Build a message by invoking ADVICESLIP API
+           curl -s https://api.adviceslip.com/advice > advice.json
+           ...
```

Review the PR, make any necessary changes (see next section), and then merge the PR to add the workflow to the repository.

## Adjust the workflow if needed and run

Common adjustments after conversion:

* Remove or populate an empty `env:` block (empty `env:` can trigger YAML validation errors).
* Add triggers such as `push:` if you want the workflow to run automatically on push events.
* Install missing packages with `apt-get update` before `apt-get install` to avoid cache errors.
* Replace `sudo apt-get install cowsay -y` with an `apt-get update` + `apt-get install -y cowsay` sequence.

Example corrected workflow used in this walkthrough:

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  push:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0

      - name: run command
        shell: bash
        run: |
          # Build a message by invoking ADVICESLIP API
          curl -s https://api.adviceslip.com/advice > advice.json
          cat advice.json
          # Test to make sure the advice message has more than 5 words.
          cat advice.json | jq -r .slip.advice > advice.message
          [ $(wc -w < advice.message) -gt 5 ] && echo "Advice has more than 5 words" || (echo "Advice - $(cat advice.message) has 5 words or less" && exit 1)
          # Deploy
          sudo apt-get update
          sudo apt-get install -y cowsay
          export PATH="$PATH:/usr/games:/usr/local/games"
          cat advice.message | cowsay -f $(ls /usr/share/cowsay/cows | shuf -n 1)
```

After merging and committing the final YAML:

* Trigger the workflow by pushing changes or using the Actions UI to run a `workflow_dispatch`.
* Monitor the run logs in the Actions tab.

<Frame>
  <img alt="A screenshot of the Jenkins web interface showing a job page titled &#x22;Generate ASCII Artwork&#x22; with permalinks, job details, and a left-side menu (Status, Build Now, Configure, etc.). The page uses a dark theme and displays recent build history." />
</Frame>

<Frame>
  <img alt="Screenshot of a GitHub Actions page for a repository, showing the &#x22;All workflows&#x22; view with two workflow runs for Generate_ASCII_Artwork — one queued update and one failed run. The interface is in dark mode." />
</Frame>

Example run log excerpt (shows API response and cowsay output):

```text theme={null}
{"slip": {"id": 13, "advice": "If you're feeling tired or anxious, a pint of water will almost always make you feel better."}}
Advice has more than 5 words
...
Setting up cowsay (3.03+dfsg2-8) ...
...
/ If you're feeling tired or anxious, a \
| pint of water will almost always make |
\ you feel better.                       /
 ----------------------------------------
        \
         \   ,__,
             (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     |
```

## Summary / Checklist

* Install `gh` and add the `gh-actions-importer` extension.
* Authenticate `gh` and configure the importer (`gh actions-importer configure`) with GitHub and Jenkins credentials.
* Use `gh actions-importer dry-run` to preview the generated workflow YAML before pushing changes.
* Use `gh actions-importer migrate` to create a branch and open a PR with `.github/workflows/<workflow>.yml`.
* Review and adjust triggers, `env`, package installation steps, and replace any plugin-specific Jenkins steps with suitable Actions.
* Recreate Jenkins secrets as GitHub Secrets — the importer does not migrate secrets.

<Callout icon="warning">
  The importer cannot convert scripted Jenkins pipelines, Jenkins credentials/secrets, or steps that depend on custom/unknown plugins. Plan to re-create secrets in GitHub and manually validate plugin-dependent steps in the resulting workflow.
</Callout>

## Links and references

* GitHub CLI: [https://cli.github.com/](https://cli.github.com/)
* GitHub Actions Importer: [https://github.com/github/gh-actions-importer](https://github.com/github/gh-actions-importer)
* Create a GitHub Personal Access Token (classic): [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
* Jenkins API tokens: [https://www.jenkins.io/doc/book/managing/creating-api-tokens/](https://www.jenkins.io/doc/book/managing/creating-api-tokens/)

That’s it — the GitHub Actions Importer streamlines converting declarative Jenkins pipelines and many freestyle jobs into GitHub Actions workflows, but expect to review and fine-tune converted workflows and recreate secrets in GitHub.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/ad83e116-9585-4ed4-9510-3e34ad12a386" />
</CardGroup>


# Pipeline Durability

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Backup-and-Configuration-Management/Pipeline-Durability/page

Explains Jenkins Pipeline durability modes, trade-offs between resumability and performance, configuration scopes, and recommendations for choosing maximum survivability or performance optimized

What is pipeline durability?

Pipeline durability in Jenkins determines how much in-memory execution state a Pipeline persists to disk during its run. This persisted state enables a Pipeline to resume after an unexpected Jenkins restart (resumability), but writing more state to disk increases disk I/O and can impact performance for Pipelines with many steps. Durability settings let you balance resumability against runtime throughput.

<Callout icon="lightbulb">
  Pipeline durability affects whether a Pipeline can recover after an unclean shutdown. Choose settings based on the criticality of the job: production deployments typically favor durability, high-throughput workloads may favor performance.
</Callout>

Why this matters (SEO keywords): Jenkins pipeline durability, resumable pipelines, pipeline speed vs durability, Jenkins restart recovery.

Durability options

| Mode                    | Description                                                                                                                                        | When to use                                                                                             |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `PERFORMANCE_OPTIMIZED` | Minimizes disk I/O for better performance. May lose state on unclean shutdowns and the Pipeline cannot resume.                                     | High-throughput feature branches or short-lived jobs where occasional restart loss is acceptable.       |
| `SURVIVABLE_NON_ATOMIC` | Middle-ground. Preserves more state than performance-optimized while attempting to reduce I/O.                                                     | Typical development workflows that need some resiliency without the full cost of maximum survivability. |
| `MAX_SURVIVABILITY`     | Most conservative: persists the most state to disk, giving the best chance of resuming after an unclean shutdown. Slower due to frequent disk I/O. | Critical pipelines (production deployments, infrastructure changes, long-running jobs).                 |

Where to change durability settings

You can configure durability in three scopes: global (affects all Pipelines by default), per-pipeline job, and per-branch for multibranch or organization folders.

| Scope                | How to change                                                                                          | Notes                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| Global               | Manage Jenkins → System → Pipeline Speed / Durability                                                  | Sets the default for new and existing Pipelines unless overridden.                                    |
| Multibranch / Branch | Multibranch project or Organization folder → Configuration → Branch pipeline speed/durability override | Useful to set `main`/`master` to `MAX_SURVIVABILITY` and feature branches to `PERFORMANCE_OPTIMIZED`. |
| Pipeline job         | Pipeline job configuration → Pipeline Speed / Durability                                               | Job-level setting overrides the global default.                                                       |

Global setting

Change the default for all Pipelines in Jenkins via: Manage Jenkins → System → Pipeline Speed / Durability. The global default is `MAX_SURVIVABILITY`, but you can change it to `PERFORMANCE_OPTIMIZED` or `SURVIVABLE_NON_ATOMIC` as needed.

<Frame>
  <img alt="A screenshot of the Jenkins documentation page titled &#x22;How Do I Set Speed/Durability Settings?&#x22; showing numbered configuration options and explanatory text. A dark-themed site layout is visible with a &#x22;User Handbook&#x22; navigation sidebar on the left." />
</Frame>

The global default can be changed from the dropdown in the System configuration.

<Frame>
  <img alt="A screenshot of a Jenkins &#x22;Manage Jenkins > System&#x22; configuration page in dark mode showing the &#x22;Pipeline Speed / Durability&#x22; section with a dropdown open listing durability options (highlighting &#x22;Maximum survivability/durability but slowest&#x22;). The page also shows sections for Copyartifact upstream build selection, access keys, and Save/Apply buttons." />
</Frame>

Multibranch / branch-level setting

For multibranch projects or organization folders, you can override durability per branch. A common pattern is to set `main` or `master` to `MAX_SURVIVABILITY` while using `PERFORMANCE_OPTIMIZED` for short-lived feature branches.

<Frame>
  <img alt="A dark-themed web UI showing a &#x22;Gitea-Organization › Configuration&#x22; page with pipeline branch speed/durability override settings and dropdowns. At the bottom are &#x22;Save&#x22; and &#x22;Apply&#x22; buttons." />
</Frame>

Pipeline job-level setting

You can also set durability per Pipeline job in the Pipeline configuration UI. This setting overrides the global default for that specific job — useful when individual jobs have differing resiliency requirements.

Example: durability test Pipeline

This simple Pipeline writes a number to a file once per second for 600 iterations. It's designed to demonstrate resumability behavior under different durability settings.

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('For Loop - Durability Test') {
            steps {
                script {
                    sh 'touch numbers.txt'
                    for (int i = 0; i < 600; i++) {
                        sh "echo ${i + 1} >> numbers.txt"
                        sleep 1
                    }
                }
            }
        }
    }
}
```

Run the job with MAX\_SURVIVABILITY

With the job set to Maximum survivability, Jenkins persists enough state for the Pipeline to resume after an unclean restart. Start the build, kill the Jenkins process, then restart Jenkins — the Pipeline should continue from where it left off.

Pipeline dashboard while running:

<Frame>
  <img alt="A dark-themed Jenkins pipeline dashboard screenshot showing a job page for &#x22;durability-test&#x22; with a small pipeline stage diagram (Start → For Loop → End), permalinks, and a build history panel at the bottom left." />
</Frame>

Example sequence for killing the Jenkins controller (run on the controller):

```bash theme={null}
