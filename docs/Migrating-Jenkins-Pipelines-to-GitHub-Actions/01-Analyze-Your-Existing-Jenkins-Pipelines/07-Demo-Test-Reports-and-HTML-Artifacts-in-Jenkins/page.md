# Download the agent jar from the controller
curl -sO http://139.84.149.70:8080/jnlpJars/agent.jar

# Store the agent secret in a file (replace with the real secret, securely)
echo "REPLACE_WITH_AGENT_SECRET" > secret-file

# Start the agent using the secret stored in a file
java -jar agent.jar -url http://139.84.149.70:8080/ -secret @secret-file -name "us-west-1-ubuntu-22" -webSocket -workDir "/home/jenkins-agent"
```

<Callout icon="warning">
  Never commit agent secrets, API tokens, or other credentials into source control. Use credential managers, secret stores, or environment-specific secret injection. Limit token scope and expiry.
</Callout>

After starting the agent it should connect and report a single executor, its remote root directory, and labels. Jobs targeting the agent label will run on this node.

<Frame>
  <img alt="A dark-themed Jenkins node configuration page for the agent &#x22;us-west-1-ubuntu-22,&#x22; showing fields like Description, Number of executors (1), Remote root directory (/home/jenkins-agent), Labels, and Save/Apply buttons. The left sidebar lists agent actions (Delete Agent, Configure, Build History, etc.) and a Build Executor Status panel." />
</Frame>

## Security and credentials

* Authentication: Jenkins own user database (internal user store).
* Current UI user: `Siddharth`.
* API tokens in use to authenticate automation (e.g., tokens named `gh-1`).

<Frame>
  <img alt="A screenshot of the Jenkins web interface on the &#x22;Security&#x22; settings page, showing API token management (a token labeled &#x22;gh-1&#x22; and an &#x22;Add new Token&#x22; button) and password/confirm password fields with Save/Apply buttons. The dark-themed layout includes a left navigation menu with items like Status, Builds, Account, and Security." />
</Frame>

### Credentials stored in Jenkins

Several credentials are scoped in Jenkins credential stores and referenced by pipelines:

|                                Credential | Use                                     |
| ----------------------------------------: | --------------------------------------- |
|    `mongo-db-credentials` (user/password) | Used in unit tests and coverage stages  |
| `mongo-db-username` / `mongo-db-password` | Test DB access                          |
|                  `docker-hub-credentials` | Pushing Docker images                   |
|                 OWASP DepCheck credential | Used by Dependency-Check where required |

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Credentials&#x22; administration page showing a list of stored credentials (e.g., mongo-db-credentials, mongo-db-username, mongo-db-password, docker-hub-credentials) and credential stores scoped to the system. The UI is in dark theme with navigation breadcrumbs at the top." />
</Frame>

When migrating pipelines to GitHub Actions (or another CI), plan to:

* Re-create necessary secrets in the target CI secrets store.
* Avoid copying credentials verbatim—rotate tokens where possible.
* Map Jenkins credentials to corresponding environment names (e.g., `DOCKERHUB_TOKEN`, `MONGO_USER`, `MONGO_PASS`).

<Callout icon="lightbulb">
  Tip: Inventory every credential referenced by jobs (check pipeline scripts and Freestyle build steps). Use a spreadsheet or small manifest to record each credential name, where it’s used, required scope, and a recommended replacement in the target CI.
</Callout>

## Summary and next steps

* The controller is a standard Jenkins installation with one connected agent (and one offline agent at audit time).
* Key tools and plugins (Node.js installer, Dependency-Check, Docker) are in use; some plugins show available updates.
* Credentials and API tokens exist and will need to be re-created in the target CI. Do not migrate secrets directly—use secure secret tooling and rotate credentials after migration.
* Next: inspect each project in turn, run representative builds to validate behavior, then begin mapping pipeline steps to GitHub Actions workflows or the target CI solution.

## Links and references

* Jenkins Agents & Remoting: [https://www.jenkins.io/doc/book/using/agents/](https://www.jenkins.io/doc/book/using/agents/)
* Jenkins JNLP agent details: [https://www.jenkins.io/doc/book/managing/nodes/](https://www.jenkins.io/doc/book/managing/nodes/)
* OWASP Dependency-Check: [https://owasp.org/www-project-dependency-check/](https://owasp.org/www-project-dependency-check/)
* Jenkins Plugins: [https://www.jenkins.io/doc/book/managing/plugins/](https://www.jenkins.io/doc/book/managing/plugins/)
* Secure secret management: GitHub Actions Secrets — [https://docs.github.com/actions/security-guides/encrypted-secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/89003f1c-027f-459f-af5c-d9f03642bfa1" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/b31417fe-5d54-4a7d-94e6-a2e48bde80e6" />
</CardGroup>


# Demo Test Reports and HTML Artifacts in Jenkins

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Demo-Test-Reports-and-HTML-Artifacts-in-Jenkins/page

Demonstrates enabling JUnit test results and publishing HTML coverage and security reports from a Jenkins pipeline, including Trivy and OWASP Dependency Check integration.

This lesson shows how to enable JUnit test reports and publish HTML artifacts (coverage and security reports) from a Jenkins pipeline. In a previous pipeline run the coverage, dependency, and vulnerability-reporting steps were producing HTML outputs, but the publish/archive steps were commented out — so the reports never appeared in the Jenkins UI.

Below are the key details, the fixed Jenkinsfile fragment (with report publishing enabled), console excerpts, and screenshots illustrating the published reports.

## Problem summary

* Unit tests, coverage, and vulnerability scans were executed, but Jenkins did not display the results because the JUnit archive and HTML publish steps were commented out.
* Tools involved:
  * Trivy (image vulnerability scanner) — produces JSON and can convert it to HTML.
  * OWASP Dependency Check — produces XML and HTML reports.
  * Istanbul/nyc — produces coverage HTML (lcov-report).
  * Test runner — should produce JUnit XML results.

Example console excerpt from the previous run (showing Trivy converting JSON to HTML):

```text theme={null}
nodejs-22-6-0 — Use a tool from a predefined Tool Installation <1s
Fetches the environment variables for a given tool in a list of 'FOO=bar' strings suitable for the withEnv step. <1s
trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json — Shell Script 39s
trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json — Shell Script <1s
```

## Fixed Jenkinsfile fragment

Below is a consolidated Jenkinsfile fragment with the publish/archive steps uncommented and adjusted. It focuses on Unit Tests, Code Coverage (Istanbul), Build/Push, Trivy scanning, and OWASP Dependency Check publishing.

```groovy theme={null}
pipeline {
    agent any
    environment {
        GIT_COMMIT = "${env.GIT_COMMIT}"
    }
    stages {
        stage('Unit Tests') {
            steps {
                sh 'npm test'
                // Archive JUnit-style test results (adjust pattern to match your test runner output)
                junit 'test-results/**/*.xml'
            }
        }

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
                // Publish coverage HTML report produced by Istanbul/nyc
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'coverage/lcov-report',
                    reportFiles: 'index.html',
                    reportName: 'Code Coverage'
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
                // Scan the built image and output JSON results
                sh '''
                    trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json
                '''
                // Convert JSON to an HTML report using the provided template
                sh '''
                    trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json
                '''
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'trivy-image-CRITICAL-results.html',
                    reportName: 'Trivy Image Scan'
                ])
            }
        }

        stage('Security - Dependency Scans') {
            parallel {
                stage('NPM Dependency Audit') {
                    steps {
                        sh '''
                            npm audit --audit-level=critical || true
                        '''
                    }
                }

                stage('OWASP Dependency Check') {
                    steps {
                        dependencyCheck additionalArguments: """
                            --scan './'
                            --out './'
                            --format 'ALL'
                            --disableYarnAudit
                            --prettyPrint --failOnCVSS 9
                        """, nvdCredentialsId: 'owasp-dependency-check', odcInstallation: 'OWASP-DepCheck-10'
                        dependencyCheckPublisher failedTotalCritical: 1, pattern: 'dependency-check-report.xml', stopBuild: true
                        publishHTML([
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: './',
                            reportFiles: 'dependency-check-jenkins.html',
                            reportName: 'OWASP Dependency Check'
                        ])
                    }
                }
            }
        }
    }
}
```

After committing these changes to the main branch, a new build was triggered and the pipeline completed successfully — including the publishing of HTML reports.

<Frame>
  <img alt="Screenshot of a Jenkins Blue Ocean pipeline run for &#x22;ci-pipeline-poll-scm&#x22; showing pipeline stages and progress. The Dependency Scanning (including OWASP) completed successfully while Code Coverage shows a warning, and a list of completed dependency-scan steps is shown below." />
</Frame>

## What Jenkins published

* JUnit test results were archived and shown in the Tests page (Blue Ocean and classic UI).
* Istanbul (nyc) coverage HTML report was published under `coverage/lcov-report/index.html`.
* Trivy produced a JSON results file that was converted into an HTML report and published.
* OWASP Dependency Check HTML report was published and made available under Artifacts.

Console excerpt for the Code Coverage stage:

```text theme={null}
Code Coverage - 19s
> Check out from version control
> Checks if running on a Unix-like node
> docker inspect -f . "$JD_TO_RUN" — Shell Script
> nodejs-22-6-0 — Use a tool from a predefined Tool Installation
> Fetches the environment variables for a given tool in a list of 'FOO=bar' strings suitable for the withEnv step.
> npm run coverage — Shell Script
> Publish HTML reports
```

Open the Tests page (Blue Ocean) or the classic UI to view detailed test results (test counts, durations, and per-test metadata). For this run all tests passed (11 tests total).

<Frame>
  <img alt="A screenshot of the Jenkins CI web interface showing a test results page marked &#x22;Passed&#x22; with a left-hand navigation menu of reports and pipeline options. The main panel displays a test case about checking a liveness endpoint and a button to add a description." />
</Frame>

### Published artifacts (example locations)

| Report type                   | File / Path                         | Description                                                        |
| ----------------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| OWASP Dependency Check (HTML) | `dependency-check-jenkins.html`     | Full dependency scanning report and vulnerability summary.         |
| Code Coverage (Istanbul)      | `coverage/lcov-report/index.html`   | Per-file code coverage with highlighted missed lines/branches.     |
| Trivy (image scan)            | `trivy-image-CRITICAL-results.html` | Image vulnerability summary converted from Trivy JSON output.      |
| JUnit test results            | `test-results/**/*.xml`             | JUnit-style XML results used by Jenkins to display test summaries. |

<Frame>
  <img alt="A Jenkins Dependency-Check HTML report for project &#x22;ci-pipeline-poll-scm #27&#x22; showing scan information, totals for dependencies and vulnerabilities, and a summary table. It lists a vulnerable package (formidable@2.1.2) with details like severity, CVE counts and file path." />
</Frame>

The OWASP Dependency Check report in this run highlighted some medium severity findings. Because the pipeline is configured with `--failOnCVSS 9` (or the corresponding publisher threshold), the build only fails on critical CVSS >= 9 — medium findings do not fail the pipeline.

<Frame>
  <img alt="A browser screenshot of a code coverage report (Istanbul) showing coverage for app.js, with statements ~79.54%, branches 33.33%, functions 70% and lines ~79.06%. The page lists file metrics in a table under &#x22;All files.&#x22;" />
</Frame>

The Istanbul coverage report provides file-level details (for example, `app.js` shown at \~80% coverage) with marked statements and branches that need additional tests.

Console excerpt for the Trivy stage showing JSON output and conversion to HTML:

```text theme={null}
Trivy Vulnerability Scanner - 12s
> nodejs-22-6-0 — Use a tool from a predefined Tool Installation <1s
> Fetches the environment variables for a given tool in a list of 'FOO=bar' strings suitable for the withEnv step. <1s
> trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json — Shell Script 11s
> trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json — Shell Script <1s
> Publish HTML reports <1s
```

## Tips and best practices

* Ensure your test runner produces JUnit XML. Configure the `junit` step to match the test output path (e.g. `test-results/**/*.xml`).
* For HTML publishing, always confirm `reportDir` and `reportFiles` point to the generated files. Use `allowMissing: true` to avoid breaking builds when a report is not generated.
* Set security thresholds deliberately. In CI you may want to fail only on high/critical severity and publish informational reports for lower severities.
* Consider archiving both raw JSON/XML outputs and the converted HTML so you can reprocess raw outputs later.

<Callout icon="lightbulb">
  When publishing HTML reports from Jenkins, use `allowMissing: true` to avoid failing the build if a report is not produced. Also verify `reportDir` and `reportFiles` paths match the files generated by your tools.
</Callout>

These published artifacts improve visibility into test outcomes, coverage gaps, and security issues directly from the Jenkins build. If you plan to migrate to GitHub Actions, the GitHub Actions Importer can help transfer these stages and artifacts to workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/f7a27e44-1736-499d-b19b-fb4194b86f28" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/25b0c0f5-b536-4cdd-a2e4-97b466a130a7" />
</CardGroup>
