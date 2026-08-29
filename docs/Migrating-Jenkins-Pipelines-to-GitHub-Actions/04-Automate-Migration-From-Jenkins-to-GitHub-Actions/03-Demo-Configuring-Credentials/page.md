# Build a message by invoking ADVICESLIP API
curl -s https://api.adviceslip.com/advice > advice.json
cat advice.json

# Test to make sure the advice message has more than 5 words.
jq -r .slip.advice < advice.json > advice.message
if [ $(wc -w < advice.message) -gt 5 ]; then
  echo "Advice has more than 5 words"
else
  echo "Advice - $(cat advice.message) has 5 or fewer words"
fi

# Deploy (example)
echo "$m_username"
sudo apt-get update && sudo apt-get install -y cowsay
echo "$PATH"
export PATH="$PATH:/usr/games:/usr/local/games"
```

Notes:

* Use `jq` to extract structured JSON fields reliably.
* Avoid printing secrets to logs in production — the example echoes the secret only for demonstration.

***

## Re-run the audit

After saving the new multi-branch job and the updated job with a secret binding, we re-ran the audit to refresh the report and capture the new job and secret binding.

Run the audit:

```bash theme={null}
gh actions-importer audit jenkins --output-dir tmp/audit
```

Trimmed terminal session showing the audit run and redaction:

```bash theme={null}
root@jenkins:/home# gh actions-importer audit jenkins --output-dir tmp/audit
# ... tool runs ...
[2025-05-22 09:25:57] tmp/audit/workflow_usage.csv
[2025-05-22 09:25:57] tmp/audit/audit_summary.md
[2025-05-22 09:26:18] Secrets redacted in file(s):
[2025-05-22 09:26:18] tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
[2025-05-22 09:26:18] tmp/audit/Generate_ASCII_Artwork/config.json
[2025-05-22 09:26:18] tmp/audit/multi-branch-pipeline/main/config.json
[2025-05-22 09:26:18] tmp/audit/multi-branch-pipeline/uat/config.json
[2025-05-22 09:26:18] tmp/audit/multi-branch-pipeline/config.json
Redacting secrets: |---------------------------------------|
root@jenkins:/home# (took 46s)
```

The updated audit summary now includes the new multi-branch job and the secret binding detection:

```markdown theme={null}
Summary for [Jenkins instance](http://139.84.149.83:8080/)

- GitHub Actions Importer version: **1.3.22397 (b4d19e0745a2d2c3db575188f98101dd1f9b4a53)**
- Performed at: **5/22/25 at 09:25**

## Pipelines

Total: **5**

- Successful: **2 (40%)**
- Partially successful: **2 (40%)**
- Unsupported: **1 (20%)**
- Failed: **0 (0%)**

### Job types

Supported: **4 (80%)**

- flow-definition: **2**
- project: **1**
- org.jenkinsci.plugins.workflow.multibranch: **1**

Unsupported: **1 (20%)**
...
```

Summary table: Before vs After (high level)

| Metric                  | Before (5/21/25 18:19) | After (5/22/25 09:25)                             |
| ----------------------- | ---------------------- | ------------------------------------------------- |
| Total pipelines         | 4                      | 5                                                 |
| Successful              | 1 (25%)                | 2 (40%)                                           |
| Partially successful    | 2 (50%)                | 2 (40%)                                           |
| Unsupported             | 1 (25%)                | 1 (20%)                                           |
| Multi-branch discovered | No                     | Yes (org.jenkinsci.plugins.workflow\.multibranch) |

***

## Generated GitHub Actions workflow and secret mapping

The import tool redacted secrets and generated workflow YAML for the Jenkins jobs it can map. It detected the `m_username` secret and mapped it to a repository/organization-level secret in the generated workflow. You (or a repo administrator) must create that secret in GitHub (repo/org/environment level) so the workflow can use it at runtime.

Example generated workflow snippet (secrets must be created in GitHub prior to running the workflow):

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
        run: |
          # Build a message by invoking ADVICESLIP API
          curl -s https://api.adviceslip.com/advice > advice.json
          cat advice.json
          # Test to make sure the advice message has more than 5 words.
          jq -r .slip.advice < advice.json > advice.message
          if [ $(wc -w < advice.message) -gt 5 ]; then
            echo "Advice has more than 5 words"
          else
            echo "Advice - $(cat advice.message) has 5 or fewer words"
          fi
          # Deploy
          echo "$m_username"
          sudo apt-get update && sudo apt-get install -y cowsay
```

Important: The tool maps many Jenkins credential types to appropriate GitHub Actions equivalents and creates references in the generated workflows, but it does not create the repository/org secrets for you — you must create those secrets manually in GitHub.

> **lightbulb** The audit tool maps many Jenkins credential types to GitHub Actions equivalents, but referenced secrets must be created in GitHub (repo/org/environment level) before the workflow runs.

***

That's it for this lesson — the updated audit summary and generated artifacts reflect the newly added multi-branch pipeline and the secret binding added to the existing job.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/f4511dc3-eab1-404a-84d8-fd3e5fa2badd)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/7e623f64-8ef5-4b23-968f-3c6ce69b7a3a)


# Demo Configuring Credentials

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Configuring-Credentials/page

Explains how to create and securely store GitHub personal access and Jenkins API tokens and configure the GitHub Actions Importer to authenticate with both services.

In this lesson you will configure the credentials required to authenticate the GitHub Actions Importer CLI with a Jenkins CI server. Follow the steps below to create and securely store the tokens, then configure the importer so it can access both GitHub and Jenkins.

## Prerequisites

Install the GitHub Actions Importer extension and verify the help output:

```bash theme={null}
gh extension install github/gh-actions-importer
gh actions-importer -h
```

Sample help output:

```text theme={null}
Options:
 -?, -h, --help Show help and usage information

Commands:
 update      Update to the latest version of GitHub Actions Importer.
 version     Display the version of GitHub Actions Importer.
 configure   Start an interactive prompt to configure credentials used to authenticate
             with your CI server(s).
 audit       Plan your CI/CD migration by analyzing your current CI/CD footprint.
 forecast    Forecast GitHub Actions usage from historical pipeline utilization.
 dry-run     Convert a pipeline to a GitHub Actions workflow and output its yaml file.
 migrate     Convert a pipeline to a GitHub Actions workflow and open a pull request
             with the changes.
 list-features List the available feature flags for GitHub Actions Importer.
```

## Which credentials are required?

You need two credentials so the importer can access both GitHub and Jenkins:

|                                                          Credential | Purpose                                                                     | Example environment variable                                             |
| ------------------------------------------------------------------: | --------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
|        GitHub personal access token (classic) with `workflow` scope | Authenticate the importer to create or read workflows and related repo data | `GITHUB_PAT`                                                             |
| Jenkins API token for the Jenkins user account used by the importer | Authenticate API calls to your Jenkins instance                             | `JENKINS_API_TOKEN`, used with `JENKINS_USERNAME` and `JENKINS_BASE_URL` |

## Create a GitHub personal access token (classic)

1. In GitHub, go to Settings → Developer settings → Personal access tokens → Classic.
2. Click **Generate new token (classic)**.
3. Give it a descriptive name (for example, `jenkins-importer-token-2`) and select the `workflow` scope.
4. Generate the token and copy it to a secure location. Do not commit this token to source control.

<Frame>
  <img alt="A dark-themed GitHub Developer Settings screen showing the &#x22;New personal access token (classic)&#x22; form with the note set to &#x22;jenkins-importer-token-2&#x22;, a 30-day expiration, and various repo/workflow scopes selected." />
</Frame>

Example placeholder (store securely; never post real tokens publicly):

```text theme={null}
