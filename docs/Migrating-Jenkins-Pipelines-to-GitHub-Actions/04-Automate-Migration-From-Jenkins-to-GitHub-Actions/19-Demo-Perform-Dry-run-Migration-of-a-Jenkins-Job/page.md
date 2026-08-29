# run dry-run
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/folder-1/job/folder-2/job/pipeline-project-2 \
  --output-dir tmp/dry-run

[2025-05-22 10:36:34] Logs: 'tmp/dry-run/log/valet-20250522-103634.log'
[2025-05-22 10:36:35] Output file(s):
tmp/dry-run/folder-1/folder-2/pipeline-project-2/.github/workflows/pipeline-project-2.yml

root@jenkins in /home took 23s
```

## Generated workflow (abridged)

After the dry-run, the importer created a GitHub Actions workflow YAML. The converter successfully mapped `echo` statements to `run` steps and injected a `checkout` step. Jenkins `sleep` calls did not have a built-in transformer and are emitted as commented placeholders:

```yaml theme={null}
name: folder-1/folder-2/pipeline-project-2
on:
  workflow_dispatch:

jobs:
  First_Stage:
    name: First Stage
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: echo message
        run: echo Starting the first stage...
      # This item has no matching transformer
      # - sleep:
      #   - key: time
      #     value:
      #       isLiteral: true
      #       value: 5
      - name: echo message
        run: echo First stage completed.
  Second_Stage:
    name: Second Stage
    runs-on: ubuntu-latest
    needs: First_Stage
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: echo message
        run: echo Starting the second stage...
      # This item has no matching transformer
      # - sleep:
      #   - key: time
      #     value:
      #       isLiteral: true
      #       value: 2
      - name: echo message
        run: echo Second stage completed.
```

## What the importer did (summary)

| Jenkins construct     | Result in converted workflow                                                 | Action required                                         |
| --------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------- |
| `echo`                | Converted to `- run: echo ...` steps                                         | No action needed                                        |
| `checkout` (implicit) | Added via `actions/checkout@v4.1.0`                                          | No action needed                                        |
| `sleep`               | Emitted as commented placeholder (`# This item has no matching transformer`) | Create a custom transformer or manually update workflow |

The dry-run log reveals these internal steps: the importer fetched the job's `config.xml`, converted XML to an intermediate JSON representation, applied configured transformers, and emitted workflow YAML. Transformers were found for `echo` but not for `sleep`, so `sleep` entries appear as comments.

<Callout icon="lightbulb">
  The importer emits commented placeholders for Jenkins constructs that lack matching transformers. To retain or convert such steps (for example, `sleep`), create a custom transformer that maps the Jenkins keyword/function to an equivalent GitHub Actions step (for instance, `run: sleep 5`). Custom transformers let you tailor conversions for team-specific pipeline usage.
</Callout>

<Callout icon="warning">
  Before running a full `migrate`:

  * Validate the dry-run output under `tmp/dry-run` and manually review any commented placeholders.
  * Add or author transformers for unsupported keywords if you need automated conversions.
  * Only push or open PRs after confirming the generated workflows are functionally equivalent.
</Callout>

## Next steps

1. Implement custom transformers for unsupported Jenkins constructs (e.g., `sleep` → `run: sleep <time>`).
2. Re-run the dry-run to verify the new transformers produce the desired workflow YAML.
3. When satisfied, perform a full `migrate` to apply workflows to your target GitHub repository or open PRs.

## Links and references

* [GitHub CLI (gh)](https://cli.github.com/)
* GitHub Actions workflows documentation: [https://docs.github.com/actions](https://docs.github.com/actions)
* If you need a starting point for custom transformers, consult your `actions-importer` plugin docs or source repository for transformer templates.

That's all for this lesson — use the dry-run to iterate safely until all steps convert cleanly.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/a65b1d88-434f-41e3-8d2f-6e8a0644cbf9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/7d298231-8e0e-49ff-8121-9d257ffd0f5e" />
</CardGroup>


# Demo Perform Dry run Migration of a Jenkins Job

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Perform-Dry-run-Migration-of-a-Jenkins-Job/page

Demonstrates performing a dry-run conversion of a Jenkins job into a GitHub Actions workflow using the GitHub Actions Importer CLI, showing logs, output YAML, credentials, and key options

In this lesson you'll perform a dry-run migration of a Jenkins job into a GitHub Actions workflow using the GitHub Actions Importer CLI. A dry run converts a Jenkins job (or pipeline) into an equivalent GitHub Actions workflow and writes the output files to a directory you specify. It does not open a pull request or modify any repositories — it only generates the converted workflow and logs the conversion process so you can inspect and iterate locally.

What you will learn:

* How to run a `dry-run` for a Jenkins job.
* Where to find logs and the generated workflow file.
* How to supply credentials and control conversion behavior.
* Key flags and options to customize the dry-run output.

## 1. Run the dry-run command

Use the `gh` plugin for the GitHub Actions Importer to perform a dry run. Replace `--source-url` with the URL of the Jenkins job you want to convert and set `--output-dir` to the directory where the converted files should be written.

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url "http://jenkins.example.com/job/Generate%20ASCII%20Artwork/" \
  --output-dir tmp/dry-run
```

When the command completes it prints the location of the log file and any generated output file(s). Example compact output:

```bash theme={null}
[2025-05-22 10:10:51] Logs: 'tmp/dry-run/log/valet-20250522-101051.log'
[2025-05-22 10:10:51] Output file(s):
   tmp/dry-run/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
```

## 2. Inspect the logfile

A detailed logfile is produced in the output directory. The log shows the importer requesting the job's `config.xml`, locating transformers for Jenkins features, and writing the workflow YAML. This helps you identify any gaps in the conversion or steps that may need manual adjustment.

Example excerpt from the logfile:

```text theme={null}
