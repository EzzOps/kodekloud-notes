# Logfile created on 2025-05-22 10:10:51 +0000 by logger.rb/v1.6.0
I, [2025-05-22T10:10:51.167421 #1]  INFO -- : Using GitHub Features: Defaults
I, [2025-05-22T10:10:51.169121 #1]  INFO -- : request: GET http://139.84.149.83:8080/job/Generate%20ASCII%20Artwork/config.xml
I, [2025-05-22T10:10:51.252549 #1]  INFO -- : response: Status 200
D, [2025-05-22T10:10:51.262487 #1]  DEBUG -- : [Transformers::Jenkins::DesignerPipeline::Jobs]: Located transformer for 'hudson.tasks.Shell'
D, [2025-05-22T10:10:51.339226 #1]  DEBUG -- : [Transformers::Jenkins::DesignerPipeline::Env]: Located transformer for 'org.jenkinsci.plugins...'
I, [2025-05-22T10:10:51.341622 #1]  INFO -- : Output file(s):
I, [2025-05-22T10:10:51.352145 #1]  INFO -- :  tmp/dry-run/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
I, [2025-05-22T10:10:51.539123 #1]  INFO -- : request: GET https://api.github.com/user
I, [2025-05-22T10:10:51.836812 #1]  INFO -- : response: Status 200
I, [2025-05-22T10:10:51.838139 #1]  INFO -- : Sending telemetry with transaction id '11ebd3df-87dc-4e38-a189-ba2650ff0d4c'
```

The log confirms which built-in transformers were used (for example, shell transformer and secret build wrapper transformer) and shows the path of the generated workflow.

## 3. Open the generated workflow YAML

The dry-run writes the converted workflow YAML under the specified output directory. Review the file to validate the conversion, adjust environment mappings, secrets, or steps as needed.

Example converted workflow (trimmed and corrected for clarity):

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  workflow_dispatch:
env:
  m_username: "${{ secrets.MONGO_DB_PASSWORD_M_USERNAME }}"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: run_command
        shell: bash
        run: |-
          # Build a message by invoking ADVICESLIP API
          curl -s REDACTED://api.adviceslip.com/advice > advice.json
          cat advice.json
          # Test to make sure the advice message has more than 5 words.
          jq -r .slip.advice < advice.json > advice.message
          if [ "$(wc -w < advice.message)" -gt 5 ]; then
            echo "Advice has more than 5 words"
          else
            echo "Advice - $(cat advice.message) has 5 words or less"
          fi
          # Deploy / display
          echo "$m_username"
          sudo apt-get update -y
          sudo apt-get install cowsay -y
          echo "$PATH"
          export PATH="$PATH:/usr/games:/usr/local/games"
          cat advice.message | cowsay -f "$(ls /usr/share/cowsay/cows | shuf -n 1)"
```

Notes on the conversion:

* Jenkins environment variables are mapped into `env:` (secrets preserved as `secrets.*` where possible).
* Shell steps are converted into `run` steps using a single `bash` script block.
* Sensitive values are preserved as secret references when they could be detected.

<Callout icon="lightbulb">
  Use `dry-run` when you want a local, inspectable conversion of a Jenkins job before migrating it into a repository. It helps validate transformation choices (actions, transformers, secrets) without modifying your repos.
</Callout>

## 4. Why use dry-run instead of audit?

Both `audit` and `dry-run` can help with migration analysis, but `dry-run` is designed for safe, iterative conversions:

* Writes the converted workflow to disk for local inspection and testing.
* Produces detailed logs that indicate transformer choices and potential issues.
* Accepts overrides (credentials, allowed actions, custom transformers, features) on a per-run basis so you can simulate different migration settings.

## 5. Common options for dry-run

Run `--help` to see the full list of options:

```bash theme={null}
gh actions-importer dry-run jenkins --help
```

Key flags and what they do:

| Flag                                                | Purpose                                                                  | Example                                                       |
| --------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------- |
| `-s, --source-url <source-url>`                     | The URL of the Jenkins job to migrate (REQUIRED).                        | `--source-url "http://jenkins.example.com/job/MyJob/"`        |
| `-o, --output-dir <output-dir>`                     | Destination for the generated files (REQUIRED).                          | `--output-dir tmp/dry-run`                                    |
| `-u, --jenkins-instance-url <jenkins-instance-url>` | Jenkins instance base URL.                                               | `--jenkins-instance-url "http://jenkins.example.com"`         |
| `-n, --jenkins-username <jenkins-username>`         | Username for the Jenkins instance.                                       | `--jenkins-username siddharth`                                |
| `-t, --jenkins-access-token <jenkins-access-token>` | Access token for Jenkins.                                                | `--jenkins-access-token xxxxxxxxx`                            |
| `--github-access-token <github-access-token>`       | Access token for GitHub (used for telemetry or repo access if provided). | `--github-access-token ghp_XXXX`                              |
| `--allowed-actions <allowed-actions>`               | Comma-separated list to restrict mapped GitHub Actions.                  | `--allowed-actions actions/checkout@v4,actions/setup-node@v3` |
| `--custom-transformers <custom-transformers>`       | Paths to custom transformer files for special Jenkins steps.             | `--custom-transformers ./my_transformers.rb`                  |
| `--enable-features` / `--disable-features`          | Toggle specific GHES/feature flags used during transformation.           | `--enable-features someFeature`                               |
| `` `--yaml-verbosity <info\|minimal\|quiet>` ``     | Control the verbosity of YAML output.                                    | `--yaml-verbosity info`                                       |
| `--no-telemetry`                                    | Disable telemetry during the dry-run.                                    | `--no-telemetry`                                              |
| `--no-ssl-verify`                                   | Disable SSL certificate verification for HTTP requests.                  | `--no-ssl-verify`                                             |

Note: The full help output contains many more flags such as `--credentials-file`, `--source-file-path`, and `--github-instance-url`. Use `--help` for complete details.

## 6. Supplying credentials and overrides

You can provide Jenkins and GitHub credentials either through environment variables or by passing the corresponding CLI flags.

Example environment variables (replace placeholders with real tokens/URLs):

```bash theme={null}
export GITHUB_ACCESS_TOKEN="ghp_XXXXXXXXXXXX"
export GITHUB_INSTANCE_URL="https://github.com"
export JENKINS_ACCESS_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export JENKINS_INSTANCE_URL="http://139.84.149.83:8080/"
export JENKINS_USERNAME="siddharth"
```

Or provide them directly on the CLI:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url "http://139.84.149.83:8080/job/Generate%20ASCII%20Artwork/" \
  --output-dir tmp/dry-run \
  --jenkins-username siddharth \
  --jenkins-access-token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --github-access-token ghp_XXXXXXXXXXXX
```

Security tip: prefer environment variables or a credentials file to avoid exposing secrets in shell history.

## 7. Allowed actions, transformers, and features

* `--allowed-actions`: Restrict which GitHub Actions the importer may map Jenkins steps to. Useful to enforce an approved action list.
* `--allow-verified-actions` and `--allow-github-created-actions`: Enforce stricter policies for action selection during conversion.
* `--custom-transformers`: Provide custom conversion logic for Jenkins plugins or steps not covered by built-in transformers.
* `--enable-features` / `--disable-features`: Toggle features that influence how the importer maps Jenkins behavior to GitHub Actions capabilities.

## 8. Summary and next steps

* `gh actions-importer dry-run jenkins` converts a Jenkins job into a GitHub Actions YAML file and writes it to disk without creating PRs.
* Inspect the logfile and generated YAML to validate the conversion and identify any manual adjustments required.
* Use CLI flags or environment variables to control credentials, allowed actions, transformers, and features.
* After validating the dry-run output, proceed with a final migrate step or manually commit the generated workflow to your repo.

That's all for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/d95331a4-18de-4e10-959a-492bfa9930cd" />
</CardGroup>


# Demo Perform an Audit of Jenkins

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Perform-an-Audit-of-Jenkins/page

Guide for auditing a Jenkins instance with the GitHub Actions Importer to discover pipelines, dry-run convert them to GitHub Actions, and generate per-job outputs and migration summaries.

This guide shows how to audit a Jenkins instance using the GitHub Actions Importer. The audit will:

* Discover jobs and pipelines on a Jenkins server.
* Attempt to convert each pipeline into a GitHub Actions workflow (dry-run).
* Produce per-job output files (converted YAML, metadata, Jenkinsfile, errors) and an overall migration summary.
* Export a `workflow_usage.csv` to help estimate required Actions, secrets, and runners.

<Frame>
  <img alt="A blue-green gradient slide with the centered text &#x22;Perform an Audit of Jenkins.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

## What the audit does

* Enumerates jobs and pipelines on the configured Jenkins instance.
* Converts pipelines to equivalent GitHub Actions workflows in dry-run mode when possible.
* Writes output files per job: converted workflow YAML (if generated), `config.json` metadata, original `Jenkinsfile` (when available), error details (if any), and an overall `audit_summary.md`.
* Creates `workflow_usage.csv` with detected actions, secrets, and runners to support migration planning.

## Prerequisites — configure credentials

Before running the audit, configure authentication for both GitHub and Jenkins. The interactive `gh actions-importer configure` flow writes credentials to a local environment file.

Example interactive flow (sensitive values redacted):

```bash theme={null}
root@jenkins in /home
➜ gh actions-importer configure
✓ Which CI providers are you configuring?: Jenkins
Enter the following values (leave empty to omit):
✓ Personal access token for Github: *****************************
✓ Base url of the Github instance: https://github.com
✓ Personal access token for Jenkins: *****************************
✓ Username of Jenkins user: siddharth
✓ Base url of the Jenkins instance: http://139.84.149.83:8080/
Environment variables successfully updated.
```

The command populates `.env.local`:

```bash theme={null}
root@jenkins in /home
❯ cat .env.local
GITHUB_ACCESS_TOKEN=ghp_**********************
GITHUB_INSTANCE_URL=https://github.com
JENKINS_ACCESS_TOKEN=**********************
JENKINS_INSTANCE_URL=http://139.84.149.83:8080/
JENKINS_USERNAME=siddharth
```

Tip: Keep your tokens secure and do not commit `.env.local` to source control.

## Run the audit

Run the audit and point outputs to a directory (example: `tmp/audit`):

```bash theme={null}
root@jenkins in /home
❯ gh actions-importer audit jenkins --output-dir tmp/audit
```

Example (truncated) log output from a run:

```bash theme={null}
[2025-05-21 18:19:51] Logs: 'tmp/audit/log/valet-20250521-181951.log'
[2025-05-21 18:19:51] Auditing 'http://139.84.149.83:8080/'
[2025-05-21 18:19:58] Output file(s):=============================|
tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
tmp/audit/ci-pipeline-poll-scm/config.json
tmp/audit/ci-pipeline-poll-scm/jenkinsfile
tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
tmp/audit/Generate_ASCII_Artwork/config.json
tmp/audit/scripted-pipeline/error.txt
tmp/audit/scripted-pipeline/config.json
tmp/audit/solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml
tmp/audit/solar-system-ci-pipeline/config.json
tmp/audit/solar-system-ci-pipeline/jenkinsfile
tmp/audit/workflow_usage.csv
tmp/audit/audit_summary.md
[2025-05-21 18:20:20] Secrets redacted in file(s):
tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
tmp/audit/Generate_ASCII_Artwork/config.json
tmp/audit/ci-pipeline-poll-scm/config.json
tmp/audit/solar-system-ci-pipeline/config.json
tmp/audit/log/valet-20250521-181951.log
Redacting secrets: |-------------------------------|
```

This example completed in \~29 seconds and produced multiple files under `tmp/audit`.

## Inspect the generated directory

After the run, examine the output structure. Example `tree` output:

```bash theme={null}
root@jenkins in /home
❯ tree tmp/audit
.
└── audit
    ├── audit_summary.md
    ├── ci-pipeline-poll-scm
    │   ├── config.json
    │   └── jenkinsfile
    ├── Generate_ASCII_Artwork
    │   └── config.json
    ├── log
    │   └── valet-20250521-181951.log
    ├── scripted-pipeline
    │   ├── config.json
    │   └── error.txt
    ├── solar-system-ci-pipeline
    │   ├── config.json
    │   └── jenkinsfile
    └── workflow_usage.csv

7 directories, 10 files
```

## Audit summary and interpretation

Open `tmp/audit/audit_summary.md` for a human-readable report. It contains importer version, timestamp, counts, and a breakdown of discovered pipelines and conversion statuses.

Sample high-level summary:

| Metric                     | Value |
| -------------------------- | ----- |
| Total pipelines discovered | 4     |
| Successful                 | 1     |
| Partially successful       | 2     |
| Unsupported                | 1     |
| Failed                     | 0     |

Result definitions:

* Successful: Fully converted pipeline constructs and steps.
* Partially successful: Major constructs converted; some steps require manual fixes.
* Unsupported: Pipeline types the importer doesn't convert automatically (e.g., scripted pipelines).
* Failed: Conversion aborted due to fatal errors (network, fetch failures).

## Job types detected

The audit maps Jenkins job types to readable labels:

| Jenkins type        | Meaning                                   |
| ------------------- | ----------------------------------------- |
| `project`           | Freestyle projects                        |
| `Flow Definition`   | Declarative pipeline jobs                 |
| `Scripted pipeline` | Scripted pipelines (commonly unsupported) |

## Build steps and actions summary

The audit aggregates known vs unknown build steps and suggests mapped GitHub Actions.

Example of known vs unknown steps (excerpt):

Known steps (automatically mapped):

* sh: 12
* publishHTML: 6
* junit: 2
* hudson.tasks.Shell: 1

Unknown steps (need manual handling): 10 (32%)

* withDockerRegistry: 2
* catchError: 2
* retry: 2
* dependencyCheckPublisher: 2
* dependencyCheck: 2

Suggested Actions (example):

* actions/checkout\@v4.1.0: 15
* run: 13
* actions/upload-artifact\@v4.1.0: 6
* EnricoMi/publish-unit-test-result-action\@v2.12.0: 2

Triggers detected:

* Total triggers: 1
* Known triggers: 1 (100%) — poll-based SCM detected (can be mapped to `schedule` or `workflow_dispatch`).

Environment variables (sample):

* Total env vars: 8
  * Known: 2 (25%) — `MONGO_URI: 2`
  * Unknown: 6 (75%) — `MONGO_PASSWORD`, `MONGO_USERNAME`, `MONGO_DB_CREDS`

## Manual tasks and self-hosted runners

Actions the importer cannot automate and that require manual work:

* Provision and configure self-hosted GitHub runners if Jenkins agents/labels were used.
* Recreate repository/organization secrets in GitHub (the importer redacts secrets).
* Implement custom plugin integrations or functionality that lacks a direct GitHub Actions equivalent.

Example runner info extracted:

```text theme={null}
Self hosted runners: 14
- us-west-1-ubuntu-22 : 14
```

## Files produced per job

The importer creates a directory per job with relevant artifacts. Use the generated YAML and `config.json` as the basis for manual edits and secret/re-runner setup.

Table — example per-job outputs:

| Job                                             | Generated workflow                                                                                                                                 | Metadata                                                                     | Source / Error                                                               |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Generate\_ASCII\_Artwork                        | [Generate\_ASCII\_Artwork/.github/workflows/generate\_ascii\_artwork.yml](Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml)     | [Generate\_ASCII\_Artwork/config.json](Generate_ASCII_Artwork/config.json)   | —                                                                            |
| ci-pipeline-poll-scm (partially successful)     | [ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml](ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml)                 | [ci-pipeline-poll-scm/config.json](ci-pipeline-poll-scm/config.json)         | [ci-pipeline-poll-scm/jenkinsfile](ci-pipeline-poll-scm/jenkinsfile)         |
| solar-system-ci-pipeline (partially successful) | [solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml](solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml) | [solar-system-ci-pipeline/config.json](solar-system-ci-pipeline/config.json) | [solar-system-ci-pipeline/jenkinsfile](solar-system-ci-pipeline/jenkinsfile) |
| scripted-pipeline (unsupported)                 | —                                                                                                                                                  | [scripted-pipeline/config.json](scripted-pipeline/config.json)               | [scripted-pipeline/error.txt](scripted-pipeline/error.txt)                   |

## workflow\_usage.csv

`workflow_usage.csv` lists detected Actions, secrets, and runners for converted pipelines — useful to plan which Actions to include and which runners or secrets to configure.

Sample CSV excerpt:

```csv theme={null}
Pipeline,Action,File path
ci-pipeline-poll-scm,actions/checkout@v4.1.0,tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
ci-pipeline-poll-scm,actions/upload-artifact@v4.1.0,tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
ci-pipeline-poll-scm,EnricoMi/publish-unit-test-result-action@v2.12.0,tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
Generate_ASCII_Artwork,actions/checkout@v4.1.0,tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
solar-system-ci-pipeline,actions/checkout@v4.1.0,tmp/audit/solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml
solar-system-ci-pipeline,actions/upload-artifact@v4.1.0,tmp/audit/solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml
solar-system-ci-pipeline,EnricoMi/publish-unit-test-result-action@v2.12.0,tmp/audit/solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml

Pipeline,Secret,File path

Pipeline,Runner,File path
ci-pipeline-poll-scm,us-west-1-ubuntu-22,tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
solar-system-ci-pipeline,us-west-1-ubuntu-22,tmp/audit/solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml
```

## Logs and troubleshooting

* Detailed logs and redaction notices are under `tmp/audit/log/`.
* For unsupported or failed pipelines, inspect `error.txt` inside the job directory to identify conversion failures and required manual remediation.

## Next steps — migrate and validate

1. Review generated YAMLs under each job directory and adapt steps, paths, or environment-specific settings.
2. Recreate required secrets in GitHub repositories or organization secrets.
3. Provision self-hosted runners if needed and map runner labels to jobs.
4. Use `gh actions-importer dry-run` for individual job iterations if you want to test conversions interactively.
5. Use `workflow_usage.csv` to stockpile required Actions and identify runner needs.

For more about GitHub Actions and runners, see:

* [GitHub Actions documentation](https://docs.github.com/en/actions)
* [Jenkins documentation](https://www.jenkins.io/doc/)

<Callout icon="lightbulb">
  The audit provides a migration plan that highlights what can be auto-converted and what requires manual work. Use the per-job `config.json` and generated YAML as the authoritative reference when migrating each pipeline.
</Callout>

<Callout icon="warning">
  Scripted Jenkins pipelines are often unsupported by the importer and will appear as unsupported/failed — they require manual migration. Also, the importer redacts secrets and cannot provision self-hosted runners; you must recreate those manually in GitHub.
</Callout>

That's a summary of the audit process and how to interpret the generated artifacts. In subsequent lessons you can explore individual generated YAML files and run dry-run conversions for individual pipelines.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/8ceff64a-4fcc-43d0-b5f0-5dbe564aed33" />
</CardGroup>
