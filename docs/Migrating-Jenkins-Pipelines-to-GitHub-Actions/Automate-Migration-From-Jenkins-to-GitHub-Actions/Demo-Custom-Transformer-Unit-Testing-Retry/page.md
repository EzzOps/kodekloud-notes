# ss-pipeline-transformer.rb
# Example transformer that converts Jenkins 'sh' trivy commands into GH Actions steps.
transform "sh" do |item|
  script = item.dig("arguments", 0, "value", "value").to_s.strip
  next nil unless script.downcase.start_with?("trivy image")

  # Extract image reference
  image_match = script.match(/trivy image (\S+)/i)
  image_ref = image_match ? image_match[1] : nil
  next nil unless image_ref

  # Extract other flags (fault-tolerant)
  severity = script.match(/--severity\s+(\S+)/i)&.captures&.first || "CRITICAL"
  format   = script.match(/--format\s+(\S+)/i)&.captures&.first || "json"
  output   = script.match(/-o\s+(\S+)/i)&.captures&.first || "trivy-results.json"
  exit_code = (script.match(/--exit-code\s+(\d+)/i)&.captures&.first || "1").to_i
  quiet = script.include?("--quiet") || script.include?("--quiet=true")

  # Normalize the image reference if it matches the original pattern
  if image_ref.include?("siddharth67/solar-system") || image_ref.include?("siddharth67/solar-system:$GIT_COMMIT")
    normalized_image_ref = "${{ vars.DOCKERHUB_USERNAME }}/${{ vars.IMAGE_NAME }}:${{ github.sha }}"
  else
    normalized_image_ref = image_ref
  end

  # Decide template-based output (we want HTML directly)
  # Use the Trivy action with template format and set the output to an HTML file
  trivy_output_html = output.end_with?(".html") ? output : "trivy-results.html"

  [
    {
      "name" => "Trivy Security Scan",
      "uses" => "aquasecurity/trivy-action@v0.30.0",
      "with" => {
        "image-ref" => normalized_image_ref,
        "severity"  => severity,
        "format"    => "template",
        "template"  => "@$HOME/.local/bin/trivy-bin/contrib/html.tpl",
        "output"    => trivy_output_html,
        "exit-code" => exit_code,
        "hide-progress" => quiet
      }
    },
    {
      "name" => "Upload Scan Report",
      "if" => "${{ always() }}",
      "uses" => "actions/upload-artifact@v4",
      "with" => {
        "name" => "Trivy Report",
        "path" => trivy_output_html
      }
    }
  ]
end
```

When the transformer runs as part of the migration tool, it replaces the Jenkins `sh` Trivy commands with the two GitHub Actions steps shown below.

## Generated GitHub Actions job (migrated)

Example of the generated job after running the transformer:

```yaml theme={null}
Trivy_Vulnerability_Scanner:
  name: Trivy Vulnerability Scanner
  runs-on:
    - ubuntu-latest
  needs: Build_Publish_Image
  steps:
    - name: checkout
      uses: actions/checkout@v4.1.0
    - name: Trivy Security Scan
      uses: aquasecurity/trivy-action@v0.30.0
      with:
        image-ref: "${{ vars.DOCKERHUB_USERNAME }}/${{ vars.IMAGE_NAME }}:${{ github.sha }}"
        severity: CRITICAL
        format: template
        template: "@$HOME/.local/bin/trivy-bin/contrib/html.tpl"
        output: trivy-results.html
        exit-code: 1
        hide-progress: true
    - name: Upload Scan Report
      if: "${{ always() }}"
      uses: actions/upload-artifact@v4
      with:
        name: Trivy Report
        path: trivy-results.html
```

After the migrated workflow runs:

* The Trivy action installs the Trivy binary, runs the scan, and writes `trivy-results.html`.
* If no CRITICAL vulnerabilities are found, the job succeeds and the report is uploaded.
* If CRITICAL vulnerabilities are found, the action exits with code `1` (job fails), but the upload step still runs because of `if: ${{ always() }}` so you can download the report.

<Frame>
  <img alt="A browser screenshot of a Trivy scan results page for &#x22;siddharth67/solar-system&#x22; showing &#x22;alpine&#x22; and &#x22;node-pkg&#x22; with &#x22;No Vulnerabilities found&#x22; and &#x22;No Misconfigurations found.&#x22; A small download notification for &#x22;Trivy Report.zip&#x22; is visible in the top-right." />
</Frame>

## Best practices & tips

* Keep `exit-code` small integer values (`0` or `1`) to clearly control job success/failure.
* Use `format: template` + `template:` to generate user-friendly HTML directly from the action.
* Use variables for image references in migrated workflows: `${{ vars.DOCKERHUB_USERNAME }}`, `${{ vars.IMAGE_NAME }}`, and `${{ github.sha }}` improve portability.
* Always upload scan reports with `if: ${{ always() }}` so artifacts are available regardless of job status.
* Consult the action docs for advanced inputs and templates: [https://github.com/aquasecurity/trivy-action](https://github.com/aquasecurity/trivy-action)
* For artifact uploads, see `actions/upload-artifact`: [https://github.com/actions/upload-artifact](https://github.com/actions/upload-artifact) and GitHub Expressions docs: [https://docs.github.com/en/actions/learn-github-actions/expressions#always](https://docs.github.com/en/actions/learn-github-actions/expressions#always)

## Summary

* The Jenkins `trivy image` + `trivy convert` pipeline can be mapped directly to `aquasecurity/trivy-action` in GitHub Actions to simplify the workflow and avoid manual conversions.
* A custom transformer can detect `trivy` shell commands and emit equivalent action steps while normalizing image references and preserving behavior (severity, exit-code, quiet).
* Upload reports using `actions/upload-artifact@v4` with `if: ${{ always() }}` so you can inspect results even on failures.

This approach keeps the original pipeline intent intact while producing a cleaner, maintainable workflow native to GitHub Actions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/24ef3b09-e929-467f-9424-1586f820f703" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/807211cc-a4ed-4974-98a5-a850cdeaee5f" />
</CardGroup>


# Demo Custom Transformer Unit Testing Retry

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-Unit-Testing-Retry/page

Guide to adding a custom transformer that preserves Jenkins retry behavior when migrating unit test stages to GitHub Actions, ensuring dependencies are installed and tests retried.

In this guide you'll learn how to create a custom transformer that preserves Jenkins `retry` semantics when migrating pipelines to GitHub Actions. The migrated Unit Testing job originally failed because the Jenkins `options { retry(2) }` identifier had no transformer, and the migrated workflow ran `npm test` before installing dependencies—so Mocha wasn't available.

This article covers:

* why the failure happened,
* how to implement a `retry` transformer that wraps test execution with a retry action,
* how to avoid duplicate `sh` and `junit` steps,
* and how to validate the migration with dry-runs.

Problematic test run (excerpt)

```bash theme={null}
Run npm test
npm test
shell: bash --noprofile --norc -e -o pipefail {0}
env:
  MONGO_URI: mongodb+srv://supercluster.d83jj.mongodb.net/superData
  MONGO_USERNAME: superuser
  MONGO_PASSWORD:

> Solar System@6.7.6 test
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit

sh: 1: mocha: not found

Error: Process completed with exit code 127.
```

Why this happened

* The Jenkinsfile contained `options { retry(2) }` in the Unit Testing stage, but the importer did not include a transformer for `retry`, so that option was dropped (or commented out) with no equivalent in the generated workflow.
* The migrated job executed `npm test` without a preceding `npm install` step, so dependencies (Mocha) were missing and tests failed.

Jenkins Unit Testing stage (snippet)

```groovy theme={null}
stage('Unit Testing') {
    agent {
        docker {
            image 'node:24'
            args '-u root:root'
        }
    }
    options {
        retry(2)
    }
    steps {
        sh 'npm test'
        junit allowEmptyResults: true, stdioRetention: '', testResults: 'test-results.xml'
    }
}
```

Migrated job (excerpt from generated GitHub Actions YAML where `retry` had no transformer)

```yaml theme={null}
container:
  image: node:24
