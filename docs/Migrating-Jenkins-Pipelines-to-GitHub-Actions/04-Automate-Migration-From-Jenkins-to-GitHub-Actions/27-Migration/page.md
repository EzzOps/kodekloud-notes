# Migration

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Migration/page

Guide to converting Jenkins pipelines into GitHub Actions workflows using the gh actions-importer migrate jenkins command, creating and reviewing a pull request and merging the generated workflow.

Use the `migrate` command to convert a Jenkins pipeline into an equivalent GitHub Actions workflow. The tool will create a pull request (PR) in your repository containing the generated workflow and any migration artifacts. This guide explains the command format, key options, example usage, how to review the generated PR, and what to do after merging.

## Command overview

Run the following command to start a Jenkins → GitHub Actions migration:

```bash theme={null}
gh actions-importer migrate jenkins
```

Key options:

| Flag           | Purpose                                                             | Example                                          |
| -------------- | ------------------------------------------------------------------- | ------------------------------------------------ |
| `--target-url` | Full URL of the GitHub repository where the workflow will be added. | `https://github.com/:owner/:repo`                |
| `--source-url` | URL of the Jenkins job to migrate.                                  | `http://localhost:8080/job/ci-pipeline-poll-scm` |
| `--output-dir` | Local directory for migration artifacts and logs.                   | `tmp/migrate`                                    |

Replace placeholders with your actual repository and Jenkins job URLs.

## Examples

Generic form:

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/:owner/:repo \
  --output-dir tmp/migrate \
  --source-url <your-jenkins-job-url>
```

Concrete example:

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/octo-org/octo-repo \
  --output-dir tmp/migrate \
  --source-url http://localhost:8080/job/ci-pipeline-poll-scm
```

## Expected output

If the command completes successfully, it prints where logs were written and the PR URL. Example output:

```text theme={null}
[2022-08-20 22:08:20] Logs: 'tmp/migrate/log/actions-importer-20220916-014033.log'
[2022-08-20 22:08:20] Pull request: 'https://github.com/sidd-harth-7/solar-system/pull/1'
```

Use the `Logs:` path to inspect detailed migration diagnostics and the generated artifacts.

## Reviewing the generated pull request

1. Open the PR URL printed by the command.
2. Read the PR description carefully — it contains a "Manual steps" section listing items that must be completed before the workflow will run correctly (for example, required secrets or platform-specific build tools).
3. Inspect the files changed. Typically the new workflow file(s) appear under `.github/workflows/`. Confirm workflows, job steps, environment variables, and referenced secrets match your Jenkins pipeline's intent.
4. Make any manual edits directly in the PR if needed.

Example "Manual steps" section output:

```text theme={null}
ci-pipeline-poll-scm

Ensure secret is available: ${{ secrets.mongo_db_password }}
Ensure build tool is available: nodejs
```

> **lightbulb** Create any required secrets at the repository or organization level before you merge the PR. Without those secrets, the workflow may fail when it runs.

> **warning** Never commit plaintext credentials or secrets into the repository. Use GitHub repository or organization secrets for sensitive values referenced by the workflow.

## What else to check in the PR

* Files changed: confirm the workflow YAML(s) are added under `.github/workflows/`.
* Steps: verify the sequence, build/install steps, and any scripts align with your Jenkins pipeline.
* Environment and secrets: ensure `env:` and `secrets:` usage matches available secrets, or note which secrets must be created.
* Runners and tool availability: check if the workflow expects specific runner labels or preinstalled tools (e.g., `node`, `docker`, `kubectl`) and update accordingly.

## Merging and running the workflow

1. After you finish reviewing the PR and have created any required secrets, merge the pull request to add the workflow to your repository.
2. Once merged, go to the repository's Actions tab to view workflow runs and logs.
3. Inspect the run details and the workflow job graph to validate that the migrated pipeline behaves as expected. If jobs fail, use the logs saved in the PR artifacts or the `--output-dir` logs for deeper debugging.

<Frame>
  <img alt="A slide titled &#x22;PR review&#x22; showing a numbered 1–4 checklist for reviewing, viewing, merging, and running a pull request. On the right is a screenshot of a GitHub Actions run summary with job statuses and a workflow graph." />
</Frame>

You can inspect logs and the job execution graph from the Actions tab to verify your migrated Jenkins pipelines are running as expected.

## Links and references

* [GitHub Actions documentation](https://docs.github.com/en/actions)
* [Jenkins documentation](https://www.jenkins.io/doc/)
* [GitHub CLI](https://cli.github.com/) (for `gh` command setup)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/82cf54bf-edd2-4967-b010-d3bf9959d20a)
