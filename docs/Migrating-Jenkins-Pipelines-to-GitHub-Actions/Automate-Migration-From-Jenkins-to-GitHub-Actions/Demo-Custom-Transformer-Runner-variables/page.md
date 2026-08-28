# Output:
# Pull request: 'https://github.com/jenkins-demo-org/solar-system/pull/1'
```

Pull request and converted workflow

The generated workflow keeps the original environment, runners, and converted jobs. The OWASP job contains the dependency-check action and a subsequent upload-artifact step to collect reports.

<Frame>
  <img alt="A screenshot of a GitHub pull request page titled &#x22;Convert ci-pipeline-poll-scm to GitHub Actions&#x22; showing a green &#x22;All checks have passed&#x22; panel with multiple successful &#x22;Solar System CI / unit-testing&#x22; checks and a green &#x22;Merge pull request&#x22; button." />
</Frame>

Excerpt of the generated workflow (converted OWASP job)

```yaml theme={null}
Dependency_Scanning_OWASP_Dependency_Check:
  name: Dependency Scanning - OWASP Dependency Check
  runs-on:
    - ubuntu-latest
  needs: Installing_Dependencies
  steps:
    - name: checkout
      uses: actions/checkout@v4.1.0
    - name: OWASP Dependency Check
      continue-on-error: true
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: test
        path: "."
        format: ALL
        out: reports
        args: "--failOnCVSS 9"
    - name: Upload Artifacts
      uses: actions/upload-artifact@v4.1.0
      with:
        if-no-files-found: ignore
        name: Dependency Check HTML Report
        path: "reports"
```

Execute the workflow and read logs

When the action runs it triggers dependency-check, which generates multiple formats (XML, HTML, JSON, CSV, SARIF, JUnit). The action receives the `--format`, `--out`, and `--failOnCVSS` settings from the `with.args` we provided.

Sample logs (trimmed):

```bash theme={null}
[INFO] Analysis Complete (4 seconds)
[INFO] Writing XML report to: /github/workspace/reports/dependency-check-report.xml
[INFO] Writing HTML report to: /github/workspace/reports/dependency-check-report.html
[INFO] Writing JSON report to: /github/workspace/reports/dependency-check-report.json
[INFO] Writing CSV report to: /github/workspace/reports/dependency-check-report.csv
[INFO] Writing SARIF report to: /github/workspace/reports/dependency-check-report.sarif
[INFO] Writing JUNIT report to: /github/workspace/reports/dependency-check-report-junit.xml

# Upload Artifacts
Uploaded bytes 209207
Finished uploading artifact content to blob storage!
SHA256 hash of uploaded artifact .zip is [SECRET_REDACTED]
Finished artifact upload
```

Handling failures and ensuring artifact upload

If dependency-check finds vulnerabilities above the `--failOnCVSS` threshold the process exits non-zero and the step fails. By adding `continue-on-error: true` to the dependency-check step, the job will continue and the `upload-artifact` step will still run so you can download the reports for inspection.

Example error when threshold is exceeded:

```text theme={null}
Error:
One or more dependencies were identified with vulnerabilities that have a CVSS score greater than or equal to '2.0':
package-lock.json?formidable (pkg:npm/formidable@2.1.2): GHSA-75v8-2h7p-7m2m (3.1), CVE-2025-46653 (6.9)
See the dependency-check report for more details.
```

Because `continue-on-error: true` is set, the Upload Artifacts step still runs and uploads the reports for inspection.

<Frame>
  <img alt="Screenshot of a GitHub Actions workflow run for the jenkins-demo-org/solar-system repo. The run &#x22;Update ci-pipeline-poll-scm.yml&#x22; shows Failure because the &#x22;Dependency Scanning - OWASP Dependency Check&#x22; job failed while steps like Installing Dependencies and NPM scanning succeeded." />
</Frame>

<Callout icon="lightbulb">
  Using `continue-on-error: true` for the dependency-check step lets subsequent steps (for example, uploading artifacts) run even if dependency-check exits non-zero. If you prefer the job to fail on vulnerabilities, omit `continue-on-error` (or set it to `false`) and make the upload conditional (for example, `if: failure()` or use `if: always()` for unconditional uploads depending on your policy).
</Callout>

Final notes and verification

* After merging the generated PR, your repository will contain the converted GitHub Actions workflow. The OWASP dependency check will run as a job, produce multiple report formats, and upload them as artifacts.
* To have the job fail on vulnerability findings, keep the required `--failOnCVSS` value and remove `continue-on-error`.
* To always collect reports regardless of findings, keep `continue-on-error: true` and upload artifacts afterward.
* The example transformer is intentionally simple: it extracts `--format` and `--failOnCVSS` and hard-codes `project`, `path`, and `out`. Extend the transformer to pull additional parameters (project name, report directory, credentials, etc.) from other Jenkins arguments as needed.

<Frame>
  <img alt="Screenshot of a GitHub Actions page for the jenkins-demo-org/solar-system repo showing the &#x22;ci-pipeline-poll-scm&#x22; workflow and three recent workflow runs on the main branch. The left sidebar shows workflow navigation and management options like Caches, Runners, and Usage metrics." />
</Frame>

That's the complete flow: parse Jenkins `additionalArguments`, implement a custom transformer that emits a GitHub Actions step using `dependency-check/Dependency-Check_Action@main`, ensure reports are written to a defined `out` directory, and upload those reports as artifacts even if the scanner step flags vulnerabilities.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/cbdf13a1-838d-4b48-9287-736900d42e56" />
</CardGroup>


# Demo Custom Transformer Runner variables

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-Runner-variables/page

How to use a custom transformer to map CI/CD runner labels and centralize environment variable mappings when migrating pipelines to GitHub Actions

In this lesson you will learn how to use a custom transformer to translate source CI/CD runner labels into equivalent GitHub Actions runners and to centralize environment variable mappings. This is useful when migrating pipelines (for example, from Jenkins) that reference self-hosted agents or custom labels so they run on GitHub-hosted runners like `ubuntu-latest`.

<Frame>
  <img alt="A blue-to-teal gradient presentation slide with the title &#x22;Custom Transformer — runner variables&#x22; centered. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

What the transformer provides

* A `runner` helper to map a source runner label to one or more GitHub Actions runner labels.
* `env` helpers to centralize environment variables or map them to repository secrets.

Common runner mapping examples

| Source label | GitHub Actions label(s)          | Notes                                           |
| ------------ | -------------------------------- | ----------------------------------------------- |
| `linux`      | `ubuntu-latest`                  | Single-label mapping (string)                   |
| `big-agent`  | `["self-hosted", "xl", "linux"]` | Multiple labels (array) for self-hosted runners |

Example mappings (Ruby syntax):

```ruby theme={null}
runner "linux", "ubuntu-latest"

runner "big-agent", ["self-hosted", "xl", "linux"]
```

* First parameter: source CI/CD runner label (string).
* Second parameter: GitHub Actions label(s), either a string or an array of strings.

Dry-run the importer to preview generated workflows
Run a one-time dry-run of the importer to produce the converted workflow files (trimmed output shown):

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers ss-pipeline-transformer.rb
