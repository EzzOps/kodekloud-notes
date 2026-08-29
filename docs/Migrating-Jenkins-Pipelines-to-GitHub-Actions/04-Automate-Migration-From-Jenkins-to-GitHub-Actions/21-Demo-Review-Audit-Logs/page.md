# Demo Review Audit Logs

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Review-Audit-Logs/page

Guide to interpreting GitHub Actions Importer audit logs from Jenkins audits, showing converted workflows, transformer results, generated artifacts, redactions, and conversion troubleshooting.

This guide explains how to interpret the audit output produced by the GitHub Actions Importer when it audits a Jenkins server. The Importer produces an audit directory (default `tmp/audit/`) containing logs (`tmp/audit/log`) and the primary `audit.log`. Use these artifacts to verify what was inspected, which pipeline elements were auto-converted, and which require manual attention or custom transformers.

## Quick CSV summary (excerpt)

Below is an excerpt of the CSV summary the tool generates (the full file is larger — \~100 lines):

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

## What audit.log records

* The audit log tracks the Importer tool’s operations while it inspects Jenkins jobs and evaluates possible conversions to GitHub Actions. It is an audit — not an automatic, guaranteed migration.
* The Importer:
  * Fetches Jenkins job listings and individual `config.xml` files via the Jenkins API.
  * Retrieves Jenkinsfiles from SCM (e.g., GitHub) using the repository API when jobs reference them.
  * Posts declarative pipeline job definitions to the Jenkins Pipeline Model Converter endpoint (`/pipeline-model-converter/toJson`) to obtain a standardized JSON representation that’s easier to analyze.
  * Attempts to locate transformer modules for pipeline elements and logs which transformers are found or missing.
* Use `tmp/audit/` to inspect generated artifacts (YAML, JSON, Jenkinsfiles), error output, and the `audit.log` for debugging.

## Representative, cleaned log excerpt (key steps)

```text theme={null}
I, [2025-05-21T18:19:51.860944 #1] INFO  -- : Using GitHub Features: Defaults
I, [2025-05-21T18:19:51.860996 #1] INFO  -- : Auditing 'http://139.84.149.83:8080/'
I, [2025-05-21T18:19:51.943207 #1] INFO  -- : request: GET http://139.84.149.83:8080/api/json?tree=jobs%5Bname%2Curl%2CfullName%5D
I, [2025-05-21T18:19:52.016101 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:52.061601 #1] INFO  -- : Thread collection size: 2
I, [2025-05-21T18:19:52.062590 #1] INFO  -- : request: GET http://139.84.149.83:8080/job/ci-pipeline-poll-scm/config.xml
I, [2025-05-21T18:19:52.063607 #1] INFO  -- : request: GET http://139.84.149.83:8080/job/Generate%20ASCII%20Artwork/config.xml
I, [2025-05-21T18:19:52.256241 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:52.547983 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:52.555698 #1] INFO  -- : request: GET http://139.84.149.83:8080/job/scripted-pipeline/config.xml
I, [2025-05-21T18:19:52.645484 #1] INFO  -- : request: GET REDACTED://api.github.com/repos/jenkins-demo-org/solar-system/contents/Jenkinsfile?ref=main
I, [2025-05-21T18:19:52.645994 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:52.663528 #1] INFO  -- : request: GET http://139.84.149.83:8080/job/solar-system-ci-pipeline/config.xml
I, [2025-05-21T18:19:52.746582 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:52.751625 #1] INFO  -- : request: GET REDACTED://api.github.com/repos/jenkins-demo-org/solar-system/contents/Jenkinsfile?ref=main
I, [2025-05-21T18:19:53.093094 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:53.094439 #1] INFO  -- : request: POST http://139.84.149.83:8080/pipeline-model-converter/toJson
I, [2025-05-21T18:19:53.152165 #1] INFO  -- : response: Status 200
I, [2025-05-21T18:19:58.457422 #1] INFO  -- : response: Status 200
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::Defaults]: Failed to locate transformer
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::RunsOn]: Located transformer for 'label'
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::Container]: Located transformer for 'docker'
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::StepTransformer]: Located transformer for 'sh'
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::StepTransformer]: Failed to locate transformer for 'dependencyCheck'
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::StepTransformer]: Located transformer for 'publishHTML'
DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::StepTransformer]: Located transformer for 'junit'
root@jenkins in /
>
```

## Key observations from the excerpt

* The Importer calls the Jenkins API (`/api/json`) to list jobs, then fetches each job's `config.xml`.
* When a Jenkins job references a Jenkinsfile in GitHub, the Importer fetches the Jenkinsfile from the GitHub API (masked as `REDACTED://...` in logs).
* The Pipeline Model Converter (`/pipeline-model-converter/toJson`) is used to convert declarative pipeline definitions to JSON for easier transformation.
* The log contains transformer lookup results (located vs failed). Located transformers will attempt an automatic conversion to a GitHub Actions construct; missing ones need manual handling or new transformers.

<Callout icon="lightbulb">
  If a step was converted incorrectly or not converted at all, consult the audit log for the HTTP calls, transformer lookups, and any redactions. These entries help decide whether to create a custom transformer or edit the generated workflow manually.
</Callout>

## Transformer results — summary

Use the following summary to understand which Jenkins constructs the Importer can map automatically and which commonly fail (plugin-specific behaviors).

| Located transformers (examples)                                                                                                                                                                                                                                                                            | Failed-to-locate transformers (examples)                                                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - `RunsOn`: `label` → maps node/label usage<br />- `Container`: `docker` → maps container/docker usage<br />- `StepTransformer`: `sh` → maps shell/script steps<br />- `StepTransformer`: `publishHTML` → maps HTML publishing steps<br />- `StepTransformer`: `junit` → maps JUnit test result publishing | - `Defaults`: `label` (in some contexts)<br />- `Container`: `label`<br />- `StepTransformer`: `dependencyCheck`<br />- `StepTransformer`: `dependencyCheckPublisher`<br />- `StepTransformer`: `catchError`<br />- `StepTransformer`: `withDockerRegistry`<br />- `Options`: `retry`<br />- `Concurrency`: `org.jenkinsci.plugins.workflow.job.properties.Pipeline` |

* Located transformers indicate constructs that the tool can map directly to a GitHub Actions equivalent, reducing manual effort.
* Missing transformers often correspond to Jenkins plugins or advanced Pipeline properties that require either:
  * Manual translation into Actions logic, or
  * Development of a custom transformer to handle the plugin-specific behavior.

## Files generated under tmp/audit/

After auditing and attempting conversions the tool writes output to `tmp/audit/`. Example files from the log:

| Path (example)                                                                  | Description                                        |
| ------------------------------------------------------------------------------- | -------------------------------------------------- |
| `tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml`     | Generated GitHub Actions workflow (auto-converted) |
| `tmp/audit/ci-pipeline-poll-scm/config.json`                                    | Pipeline model JSON from Pipeline Model Converter  |
| `tmp/audit/ci-pipeline-poll-scm/jenkinsfile`                                    | Retrieved Jenkinsfile (if present in SCM)          |
| `tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml` | Generated workflow for another job                 |
| `tmp/audit/scripted-pipeline/error.txt`                                         | Conversion error/details for scripted pipeline     |
| `tmp/audit/solar-system-ci-pipeline/config.json`                                | Model for the `solar-system` job                   |
| `tmp/audit/solar-system-ci-pipeline/jenkinsfile`                                | Jenkinsfile for `solar-system` (from GitHub)       |
| `tmp/audit/workflow_usage.csv`                                                  | CSV summary of actions and runners used            |
| `tmp/audit/audit_summary.md`                                                    | Human-readable audit summary                       |
| `tmp/audit/log/valet-20250521-181951.log`                                       | Raw importer log for this run                      |

### Secrets and redaction

The audit process detects and redacts secrets. Look for WARN entries like:

```text theme={null}
W, [2025-05-21T18:20:20.571659 #1] WARN -- : Secrets redacted in file(s):
W, [2025-05-21T18:20:20.571857 #1] WARN -- : tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
W, [2025-05-21T18:20:20.571952 #1] WARN -- : tmp/audit/Generate_ASCII_Artwork/config.json
W, [2025-05-21T18:20:20.572034 #1] WARN -- : tmp/audit/ci-pipeline-poll-scm/config.json
W, [2025-05-21T18:20:20.572133 #1] WARN -- : tmp/audit/solar-system-ci-pipeline/config.json
W, [2025-05-21T18:20:20.572213 #1] WARN -- : tmp/audit/log/valet-20250521-181951.log
```

These warnings indicate where sensitive values were redacted in the generated outputs. Review redacted files carefully to confirm credentials, tokens, or other secrets were handled correctly during conversion.

## Next steps / recommendations

* Inspect artifacts under `tmp/audit/<job>/`:
  * `config.json` — review the pipeline model the importer used to decide mappings.
  * `jenkinsfile` — confirm the Jenkinsfile the importer fetched from SCM.
  * `.github/workflows/*.yml` — review the autogenerated workflow and identify missing or incorrect steps.
* Prioritize work using the audit outputs:
  * Jobs with many located transformers are easier to convert.
  * Jobs with multiple failed transformers will require manual edits or new transformers.
* For missing transformations:
  * Implement a custom transformer that maps the Jenkins construct to one or more GitHub Actions steps, or
  * Manually edit the generated workflow YAML to replace plugin-specific steps (e.g., `dependencyCheck`, `withDockerRegistry`) with appropriate Actions, containers, or scripts.
* When conversions are unclear:
  * Check `tmp/audit/<job>/error.txt` (if present) for conversion errors and stack traces.
  * Consult `audit.log` for debugging details (HTTP requests, transformer lookups, and debug messages).

## Links and references

* Jenkins: [https://learn.kodekloud.com/user/courses/jenkins](https://learn.kodekloud.com/user/courses/jenkins)
* GitHub Actions: [https://learn.kodekloud.com/user/courses/github-actions](https://learn.kodekloud.com/user/courses/github-actions)
* Jenkins Pipeline Model Converter (documentation): [https://plugins.jenkins.io/pipeline-model-definition/](https://plugins.jenkins.io/pipeline-model-definition/)
* GitHub API (repos/contents): [https://docs.github.com/en/rest/repos/contents](https://docs.github.com/en/rest/repos/contents)

If you need help mapping a specific Jenkins step or plugin to a GitHub Action, include the relevant `config.json`, `jenkinsfile`, and the fragment of the generated workflow YAML and I can suggest a conversion strategy.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/db2f7ebb-1ed6-4c13-a991-97e253d69d8e" />
</CardGroup>
