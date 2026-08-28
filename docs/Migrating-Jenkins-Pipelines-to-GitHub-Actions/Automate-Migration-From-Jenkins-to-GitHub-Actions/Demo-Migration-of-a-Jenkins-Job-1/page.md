# Demo Migration of a Jenkins Job 1

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Migration-of-a-Jenkins-Job-1/page

Guide to migrating a Jenkins job into a GitHub Actions workflow using the GitHub Actions Importer CLI to generate workflows, create branches, and open pull requests.

This guide shows how to migrate a Jenkins job into a GitHub Actions workflow, create a branch in the target repository, and open a pull request with the generated workflow using the GitHub Actions Importer CLI.

What you’ll do:

* Fetch a Jenkins job config (config.xml).
* Run the importer transformers to generate a workflow.
* Push the workflow into a new branch on the target repo.
* Open a pull request so you can review and merge the changes.

Prerequisites:

* GitHub CLI with the Actions Importer extension installed (gh actions-importer).
* Access to the Jenkins job URL and any Jenkins credentials required to fetch the job.
* Write access to the target GitHub repository (or a fork).

Quick migrate command pattern

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/:owner/:repo \
  --output-dir tmp/migrate \
  --source-url <jenkins-job-url>
```

Example (replace with your repository and Jenkins job URL):

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/owner/repo \
  --output-dir tmp/migrate \
  --source-url my-jenkins-project
```

Inspect the available migrate options:

```bash theme={null}
gh actions-importer migrate jenkins --help
```

Key options at a glance

| Option                               |                                       Purpose | Example / Notes                                     |
| ------------------------------------ | --------------------------------------------: | --------------------------------------------------- |
| `-s, --source-url <source-url>`      |                    Jenkins job URL to migrate | `--source-url "http://jenkins.example/job/my-job/"` |
| `-o, --output-dir <output-dir>`      |           Directory to place any output files | `--output-dir tmp/migrate`                          |
| `-t, --jenkins-access-token <token>` |               Jenkins API token (if required) | Use when Jenkins requires authentication            |
| `--target-url <target-url>`          |     Target GitHub repo to open the PR against | `--target-url https://github.com/owner/repo`        |
| `--allow-verified-actions`           | Allow verified actions in generated workflows | Use to relax action restrictions                    |
| `--no-ssl-verify`                    |  Disable SSL verification for troubleshooting | Not recommended in production                       |

You can view the full help output from the CLI to see all available flags and advanced options.

<Callout icon="warning">
  If the Jenkins job references credentials or secrets, the importer cannot create GitHub repository secrets for you. Add the required secrets to the target repository before merging the PR.
</Callout>

Demo command used in this walkthrough

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/jenkins-demo-org/demo-repo \
  --output-dir tmp/migrate \
  --source-url "http://139.84.149.83:8080/job/Generate%20ASCII%20Artwork/"
```

What the importer does (high level)

1. Fetches the Jenkins job configuration (`config.xml`).
2. Runs transformers (for example: Shell Transformer, Secret Build Wrapper Transformer) to generate Actions workflow steps.
3. Checks out the target repository (default branch).
4. Creates a branch (e.g., `convert-generated-generate-ASCII-artwork-branch`).
5. Adds the workflow file under `.github/workflows/`, commits, and opens a pull request.

When the command completes, the CLI prints log and PR information:

```bash theme={null}
[2025-05-22 10:23:36] Logs: 'tmp/migrate/log/valet-20250522-102336.log'
[2025-05-22 10:23:40] Pull request: 'https://github.com/jenkins-demo-org/demo-repo/pull/1'
```

You should now see the newly created branch and the workflow changes in the repo.

<Frame>
  <img alt="A dark‑themed screenshot of a GitHub repository page for &#x22;demo-repo,&#x22; showing the selected branch &#x22;convert-generate-ascii-artwork-to-act...&#x22; with recent commits and files (.github/workflows, Jenkinsfile). The main pane prompts to &#x22;Add a README&#x22; and the right sidebar shows repo details like activity and no stars or forks." />
</Frame>

Review the pull request

* Open the PR created by the importer.
* The PR body will include migration notes and may list required manual actions, such as adding secrets.
* Inspect the generated workflow file and the transformed steps to confirm they match expected behavior.

Secrets in the generated workflow

The importer maps Jenkins job secrets into GitHub Actions secret references in the workflow. You must add those secrets manually to the repository (or organization) before merging.

Example secret reference in the workflow:

```yaml theme={null}
env:
  m_username: "${{ secrets.MONGO_DB_PASSWORD_M_USERNAME }}"
```

<Callout icon="lightbulb">
  Secrets referenced in the generated workflow must be added manually to the target repository (`Settings → Secrets and variables → Actions`). GitHub Actions masks secrets in logs, so secret values appear as asterisks if printed during a run.
</Callout>

Generated workflow example (from this demo)

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  workflow_dispatch:
env:
  m_username: "${{ secrets.MONGO_DB_PASSWORD_M_USERNAME }}"
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
          echo "$m_username"
          sudo apt-get install cowsay -y
          echo "$PATH"
          export PATH="$PATH:/usr/games:/usr/local/games"
          cat advice.message | cowsay -f "$(ls /usr/share/cowsay/cows | shuf -n 1)"
```

Merge and run the workflow

* After adding the required repository secrets, the PR should have no conflicts and can be merged.
* Merged workflows that use `workflow_dispatch` appear in the repository Actions tab and can be triggered manually.

<Frame>
  <img alt="A dark-themed GitHub Actions page for the repo &#x22;jenkins-demo-org/demo-repo&#x22; showing the &#x22;Generate_ASCII_Artwork&#x22; workflow with no runs and a &#x22;Run workflow&#x22; button. The left sidebar shows management items like Caches, Runners, and usage/performance metrics." />
</Frame>

Example run output highlights

The run shows standard checkout steps and the commands that were translated from the Jenkins job:

```bash theme={null}
Run actions/checkout@v4.1.0
Syncing repository: jenkins-demo-org/demo-repo
Getting Git version info
Temporarily overriding HOME='/home/runner/.../ _temp/...' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/demo-repo/demo-repo
Deleting the contents of '/home/runner/work/demo-repo/demo-repo'
Initializing the repository
...
`[AWS_SECRET_ACCESS_KEY]`
run command
Post checkout
```

The run executes the advice API call, validates the advice length, installs the `cowsay` package, and prints ASCII art produced from the advice text:

```bash theme={null}
"slip": { "id": 95, "advice": "Good advice is something a man gives when he is too old to set a bad example."}
Advice has more than 5 words
Unpacking cowsay (3.03+dfsg2-8) ...
Setting up cowsay (3.03+dfsg2-8) ...
...
/ Good advice is something a man gives \
| when he is too old to set a bad     |
\ example.                            /
 -------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

Note on secret masking

* If a workflow prints a secret, GitHub Actions masks its value in the logs (you’ll see `***`), so secrets remain hidden even if `echo` is used in a step.

Preview a migration (dry run / forecast)
If you want to preview how a Jenkins job would be converted without opening a PR, run a forecast (dry-run):

```bash theme={null}
gh actions-importer forecast jenkins --output-dir tmp/forecast
```

Production migration reminder
To run a full production migration (generate the workflow and open a PR against a real repository), run:

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/:owner/:repo \
  --output-dir tmp/migrate \
  --source-url my-jenkins-project
```

References and further reading

* GitHub Actions secrets: [https://docs.github.com/en/actions/security-guides/encrypted-secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* GitHub CLI: [https://cli.github.com/](https://cli.github.com/)

That’s everything for this demo migration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/c28a06fb-40d3-44c4-9366-42b1d83b71ae" />
</CardGroup>
