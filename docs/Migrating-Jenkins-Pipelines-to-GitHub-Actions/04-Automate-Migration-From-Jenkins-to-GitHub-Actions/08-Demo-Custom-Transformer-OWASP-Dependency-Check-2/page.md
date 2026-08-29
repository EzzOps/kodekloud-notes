# Demo Custom Transformer OWASP Dependency Check 2

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-OWASP-Dependency-Check-2/page

Shows building a custom transformer that converts Jenkins OWASP Dependency Check stages into GitHub Actions steps, parsing additionalArguments to set format and failOnCVSS and upload reports

This lesson shows how to build a custom transformer that converts an OWASP Dependency-Check Jenkins stage into an equivalent GitHub Actions step. The transformer:

* Parses the Jenkins plugin configuration to find `additionalArguments`.
* Extracts key flags such as `--format` and `--failOnCVSS`.
* Emits a GitHub Actions step that runs the `dependency-check/Dependency-Check_Action` and uploads generated reports.

Goal: produce a GitHub Actions job step that runs dependency-check, writes reports to `reports/`, and uploads those artifacts.

Desired GitHub Actions step (excerpt)

```yaml theme={null}
jobs:
  depchecktest:
    runs-on: ubuntu-latest
    name: depcheck_test
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Build project with Maven
        run: mvn clean install
      - name: Depcheck
        uses: dependency-check/Dependency-Check_Action@main
        id: Depcheck
        with:
          project: "test"
          path: "."
          format: "HTML"
          out: "reports" # default; no need to specify unless overriding
          args: >
            --failOnCVSS 7
            --enableRetired
      - name: Upload Test results
        uses: actions/upload-artifact@master
        with:
          name: Depcheck report
          path: ${{ github.workspace }}/reports
```

What data do we get from Jenkins?

The Dependency-Check plugin configuration appears as a structured hash. The important field is `additionalArguments` (a multi-line string). Example:

```ruby theme={null}
{
  "name" => "dependencyCheck",
  "arguments" => [
    {
      "key" => "additionalArguments",
      "value" => {
        "isLiteral" => true,
        "value" => "
                             --scan './'
                             --out './'
                             --format 'ALL'
                             --disableYarnAudit --prettyPrint --failOnCVSS 9"
      }
    },
    {
      "key" => "nvdCredentialsId",
      "value" => {
        "isLiteral" => true,
        "value" => "owasp-dependency-check"
      }
    },
    {
      "key" => "odcInstallation",
      "value" => {
        "isLiteral" => true,
        "value" => "OWASP-DepCheck-10"
      }
    }
  ]
},
{
  "name" => "dependencyCheckPublisher",
  "arguments" => [
    {
      ...
    }
  ]
}
```

What we need to parse from `additionalArguments`

| Flag           | Purpose                                                  | Regex used to extract                | Default if missing |
| -------------- | -------------------------------------------------------- | ------------------------------------ | ------------------ |
| `--format`     | Which report format(s) to generate (e.g., `HTML`, `ALL`) | `/--format\s+['"]?([^'"\s]+)['"]?/i` | `ALL`              |
| `--failOnCVSS` | CVSS threshold that makes dependency-check exit non-zero | `/--failOnCVSS\s+(\d+(?:\.\d+)?)/i`  | `9`                |

Transformer scaffolding and environment

Add or reuse your transformer (example filename: `ci-pipeline-transformer.rb`). You can set up a runner and environment variables for the transformer runtime. Example runner/env config:

```ruby theme={null}
runner "us-west-1-ubuntu-22", "ubuntu-latest"

env "MONGO_USERNAME", "superuser"
env "MONGO_PASSWORD", secret("mongo_db_password")
env "MONGO_DB_CREDS", nil
```

Transformer implementation

The transformer locates the `additionalArguments` string, applies regular expressions to extract `--format` and `--failOnCVSS`, and builds the step hash for GitHub Actions. Defaults are applied if values are absent.

```ruby theme={null}
transform "dependencyCheck" do |item|
  # Extract additional arguments (string)
  additional_args = item["arguments"].find { |arg| arg["key"] == "additionalArguments" }["value"]["value"]

  # Parse key parameters from additional arguments
  # Accept quoted or unquoted format values
  format = additional_args.match(/--format\s+['"]?([^'"\s]+)['"]?/i)&.captures&.first || "ALL"
  # Accept integer or decimal CVSS thresholds
  fail_on_cvss = additional_args.match(/--failOnCVSS\s+(\d+(?:\.\d+)?)/i)&.captures&.first || "9"

  {
    "name" => "OWASP Dependency Check",
    # Ensure that, even if the check fails, we continue to the artifact upload step
    "continue-on-error" => true,
    "uses" => "dependency-check/Dependency-Check_Action@main",
    "with" => {
      "project" => "test",
      "path" => ".",
      "format" => format,
      "out" => "reports",
      "args" => "--failOnCVSS #{fail_on_cvss}"
    }
  }
end
```

Skip the publisher stage

Jenkins' `dependencyCheckPublisher` can be omitted for GitHub Actions because the dependency-check action writes the reports directly. Return `nil` in the transformer to skip that identifier:

```ruby theme={null}
transform "dependencyCheckPublisher" do |item|
  next nil
end
```

Run a dry-run import

Validate the transformation with a dry-run using the importer tool:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers ss-pipeline-transformer.rb
```

When you run a real migration, the tool can create a pull request in the target repo:

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/jenkins-demo-org/solar-system \
  --output-dir tmp/migrate \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --custom-transformers ss-pipeline-transformer.rb
