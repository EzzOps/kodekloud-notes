# Demo Review Audit Output Files

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Review-Audit-Output-Files/page

Guide reviewing audit output files from migrating Jenkins jobs to GitHub Actions, showing generated artifacts, conversion logs, unsupported items, and migration best practices.

Let's review the output files produced by the audit command when migrating Jenkins jobs to GitHub Actions.

<Frame>
  <img alt="A blue-green gradient slide with centered white text that reads &#x22;Review Audit Output Files.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

Overview

The audit run performs the following high-level steps:

* Fetches Jenkins job configuration (`config.xml`) from the Jenkins API.
* Attempts to convert Jenkinsfiles to a JSON intermediate representation using the pipeline-model-converter.
* Generates per-job artifact directories under `tmp/audit/<job>/` containing converted GitHub Actions workflows, JSON job metadata, original Jenkinsfiles (if available), and diagnostic files (e.g., `error.txt`) when conversion fails.
* Redacts secrets in any exported output files.

The audit log below demonstrates these interactions — HTTP requests/responses, transformer activity, and the list of generated output files:

```text theme={null}
