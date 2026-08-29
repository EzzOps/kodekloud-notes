# Skip transforming certain nodes already handled elsewhere
transform "retry" do |item|
  next nil if item.dig("arguments", 0, "value", "value") == 2
end

transform "junit" do |item|
  # Skip transformation if junit result file is already handled (example)
  next nil if item.dig("arguments", 0, "value", "value") == "test-results.xml"
end

transform "catchError" do |item|
  # If this catchError wraps "npm test" (inside a sh child), skip
  next nil if item.dig("children", 0, "arguments", 0, "value", "value") == "npm test"

  # Extract coverage command from children -> sh -> arguments -> script
  coverage_cmd = item.dig("children", 0, "arguments", 0, "value", "value") || "npm run coverage"

  [
    {
      "name" => "Install dependencies",
      "run" => "npm install --no-audit",
      "shell" => "bash"
    },
    {
      "name" => "Check Code Coverage",
      "continue-on-error" => true,
      "run" => coverage_cmd,
      "shell" => "bash"
    }
  ]
end
```

## Running the importer dry-run

Use the `gh actions-importer` tool in `dry-run` mode to test extraction and transformation without writing the final workflows.

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers helper-transformer.rb
```

Example (abridged) dry-run output showing the parsed `catchError` and the output file produced:

```text theme={null}
JSON for identifier: {"name"=>"catchError", "arguments"=>[{"key"=>"buildResult","value"=>{"isLiteral"=>true,"value"=>"SUCCESS"}},{"key"=>"message","value"=>{"isLiteral"=>true,"value"=>"Oops. It will be fixed in future releases"}},{"key"=>"stageResult","value"=>{"isLiteral"=>true,"value"=>"UNSTABLE"}},{"children"=>[{"name"=>"sh","arguments"=>[{"key"=>"script","value"=>{"isLiteral"=>true,"value"=>"npm run coverage"}}]}]}]}
Output file(s):
  tmp/dry-run/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
```

## Resulting GitHub Actions job (excerpt)

The generated Code Coverage job includes checkout, dependency installation, the coverage step with `continue-on-error: true`, and artifact upload for the HTML report.

```yaml theme={null}
jobs:
  Code_Coverage:
    name: Code Coverage
    runs-on:
      - ubuntu-latest
    container:
      image: node:24
    needs: Unit_Testing
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: Install dependencies
        run: npm install --no-audit
        shell: bash
      - name: Check Code Coverage
        continue-on-error: true
        run: npm run coverage
        shell: bash
      - name: Upload Artifacts
        uses: actions/upload-artifact@v4.1.0
        with:
          if-no-files-found: ignore
          name: Code Coverage HTML Report
          path: coverage/lcov-report
```

## Pull request diff (abridged)

The transformer replaced the untranslated `catchError` block in the PR diff with two explicit steps that install dependencies and run the coverage command with `continue-on-error`.

```diff theme={null}
@@ -105,20 +105,13 @@ jobs:
   steps:
   - name: checkout
     uses: actions/checkout@v4.1.0
-#  # This item has no matching transformer
-#
-#  - catchError:
-#    - key: buildResult
-#      value:
-#        isLiteral: true
-#        value: SUCCESS
-#    - key: message
-#      value:
-#        isLiteral: true
-#        value: Oops! it will be fixed in future releases
-#    - key: stageResult
-#      value:
-#        isLiteral: true
-#        value: UNSTABLE
+  - name: Install dependencies
+    run: npm install --no-audit
+    shell: bash
+  - name: Check Code Coverage
+    continue-on-error: true
+    run: npm run coverage
+    shell: bash
   - name: Upload Artifacts
     uses: actions/upload-artifact@v4.1.0
```

## What happened when the workflow ran

* A new workflow run was triggered after merging the PR.
* The Code Coverage job executed the two transformed steps:
  * The `npm install --no-audit` step completed.
  * The `npm run coverage` step failed the coverage threshold (exit code non-zero).
* Because `continue-on-error: true` was set, the job continued and downstream jobs also ran.
* The coverage HTML report was uploaded as an artifact and is available for download from the run.

<Frame>
  <img alt="A screenshot of a GitHub Actions workflow run showing the pipeline summary on the left, a visualization of jobs at the top, and an Annotations panel listing errors (Code Coverage failed and two canceled runs). Below is an Artifacts list with reports like &#x22;Code Coverage HTML Report&#x22; and &#x22;Dependency Check HTML Report.&#x22;" />
</Frame>

You can download the artifact (Code Coverage HTML Report) and inspect it locally:

<Frame>
  <img alt="A dark‑theme Windows File Explorer window showing the contents of a &#x22;Code Coverage HTML Report.zip&#x22; with a list of HTML, CSS, JS and PNG files (e.g., app.js.html, base.css, index.html). The left navigation pane shows drives and folders and the right preview area says &#x22;Select a file to preview.&#x22;" />
</Frame>

## Code coverage failure (abridged)

This is an example of the coverage output that caused the coverage command to exit non-zero:

```console theme={null}
11 passing (825ms)

ERROR: Coverage for lines (79.06%) does not meet global threshold (90%)
-------------------------------------------------------
File | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
-------------------------------------------------------
All files | 79.54 | 33.33 | 70 | 79.06 |
app.js | 79.54 | 33.33 | 70 | 79.06 | 23,49-50,58,62-67
-------------------------------------------------------
Error: Process completed with exit code 1.
```

> **lightbulb** Using `continue-on-error: true` in the converted step mirrors Jenkins `catchError` semantics: it allows the workflow to continue and still upload artifacts even when the coverage command fails. Note that GitHub Actions will mark that step as successful for continuation, so consider also surfacing the failure via annotations, test result upload, or a PR comment if you want to preserve visibility of the failure state.

## Mapping summary

| Jenkins element                        |                                                               GitHub Actions equivalent | Notes                                                                                                   |
| -------------------------------------- | --------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------- |
| `catchError { sh 'npm run coverage' }` | Two steps: `npm install --no-audit` + `npm run coverage` with `continue-on-error: true` | Extracts inner `sh` command and wraps in `continue-on-error` to emulate Jenkins behavior.               |
| `publishHTML`                          |                                                            `actions/upload-artifact@v4` | Importer handles this conversion automatically and uploads coverage HTML (e.g. `coverage/lcov-report`). |

Example of a JSON-like transformer output is represented in the `helper-transformer.rb` implementation above.

## References

* Jenkins `catchError` step documentation: [https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/#catcherror-catch-error-mark-build-as-failed-until-unstable](https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/#catcherror-catch-error-mark-build-as-failed-until-unstable)
* GitHub Actions `continue-on-error`: [https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob\_idstepscontinue-on-error](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepscontinue-on-error)
* actions/upload-artifact: [https://github.com/actions/upload-artifact](https://github.com/actions/upload-artifact)

## Summary

* We added a custom transformer that:
  * Detects a `catchError` node and extracts the inner shell command (defaults to `npm run coverage`).
  * Emits two GitHub Actions steps: an installation step and a coverage step with `continue-on-error: true`.
* The importer still converts `publishHTML` to `actions/upload-artifact` automatically, preserving HTML reports as artifacts.
* This keeps the pipeline behavior consistent: coverage failures do not block downstream jobs while reports remain available for inspection.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/0044ba0c-5480-4569-b99b-4b4a61d94af3)


# Demo Custom Transformer Docker Build

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-Docker-Build/page

Describes a custom transformer that converts Jenkins sh docker build commands into GitHub Actions steps, replacing hard-coded values with repository variables and outlining registry authentication handling.

Let's create a custom transformer that recognizes and converts the embedded Docker build command inside Jenkins `sh` steps into a proper GitHub Actions step.

<Frame>
  <img alt="A blue-green gradient slide with the centered title &#x22;Custom Transformer Docker Build.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

Overview

* Source: Jenkins pipeline builds and pushes a Docker image, then scans it with Trivy.
* Goal: Convert the `docker build` command embedded in `sh` into a native GitHub Actions step and replace hard-coded values with repository/workflow variables.

Relevant Jenkinsfile stages (cleaned and complete)

```groovy theme={null}
stage('Code Coverage') {
    agent {
        docker {
            image 'node:24'
            args '-u root:root'
        }
    }
    steps {
        catchError(buildResult: 'SUCCESS', message: 'Oops! it will be fixed in future releases', stageResult: 'UNSTABLE') {
            sh 'npm run coverage'
        }
        publishHTML([
            allowMissing: true,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'coverage/lcov-report',
            reportFiles: 'index.html',
            reportName: 'Coverage Report'
        ])
    }
}

stage('Build Publish Image') {
    steps {
        sh 'docker build -t siddharth67/solar-system:$GIT_COMMIT .'
        withDockerRegistry(credentialsId: 'docker-hub-credentials', url: "") {
            sh 'docker push siddharth67/solar-system:$GIT_COMMIT'
        }
    }
}

stage('Trivy Vulnerability Scanner') {
    steps {
        sh '''trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json'''
        sh '''trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json'''
        publishHTML([
            allowMissing: true,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: './',
            reportFiles: 'trivy-image-CRITICAL-results.html',
            reportName: 'Trivy Report'
        ])
    }
}
```

Problem seen in the dry-run conversion

* The `docker build` was inside an `sh` step and was not converted into a proper GitHub Actions `run` step.
* The `withDockerRegistry` block had no matching transformer, so it was left commented out in the generated workflow.

Example of the dry-run output for the Build Publish Image job (trimmed):

```yaml theme={null}
if-no-files-found: ignore
name: Code Coverage HTML Report
path: coverage/lcov-report

Build_Publish_Image:
  name: Build Publish Image
  runs-on:
    - ubuntu-latest
  needs: Code_Coverage
  steps:
    - name: checkout
      uses: actions/checkout@v4.1.0
