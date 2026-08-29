# 0 (no critical vulnerabilities found)
```

Your `package.json` will update under `dependencies`:

```json theme={null}
{
  "dependencies": {
    "@babel/traverse": "^7.23.2",
    "cors": "^2.8.5",
    "express": "^4.18.2",
    "mongoose": "^5.13.20",
    "nyc": "^15.1.0"
  }
}
```

Commit the changes:

```bash theme={null}
git add package.json package-lock.json
git commit -m "fix critical vulnerability in @babel/traverse"
git push
```

## 3. Verify in Jenkins

Once pushed, Jenkins triggers a new build. Both **NPM Audit** and **OWASP Dependency Check** stages should now pass:

```bash theme={null}
npm install --no-audit
npm audit --audit-level=critical && echo $?
# vulnerability summary (2 moderate, 5 high)
# + echo 0
```

## 4. Publish the HTML Report

Expose the OWASP Dependency-Check HTML report in Jenkins by using the `htmlPublisher` step.

1. Open **Snippet Generator** > **Pipeline Syntax** > **htmlPublisher**.
2. Set:
   * Report directory: `./`
   * Report files: `dependency-check-jenkins.html`
   * Report name: **Dependency Check HTML Report**
3. Copy the generated Groovy snippet.

![The image shows a Jenkins interface with the "Snippet Generator" section open, displaying options for generating a pipeline script to publish HTML reports.](https://kodekloud.com/kk-media/image/upload/v1752871050/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/jenkins-snippet-generator-pipeline-html.jpg)

![The image shows a Jenkins Pipeline Syntax configuration page with options for generating a pipeline script, including settings for HTML report handling and file inclusion.](https://kodekloud.com/kk-media/image/upload/v1752871051/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/jenkins-pipeline-syntax-configuration.jpg)

Add it to your OWASP stage:

```groovy theme={null}
stage('OWASP Dependency Check') {
  steps {
    dependencyCheck additionalArguments: '''
      --scan ./
      --out ./
      --format ALL
      --prettyPrint
    ''', odcInstallation: 'OWASP-DepCheck-10'

    dependencyCheckPublisher failedTotalCritical: 1,
                            pattern: 'dependency-check-report.xml',
                            stopBuild: true

    publishHTML(
      allowMissing: true,
      alwaysLinkToLastBuild: true,
      keepAll: true,
      reportDir: './',
      reportFiles: 'dependency-check-jenkins.html',
      reportName: 'Dependency Check HTML Report',
      useWrapperFileDirectly: true
    )
  }
}
```

Commit and push your changes:

```bash theme={null}
git commit -am "publish Dependency-Check HTML report"
git push
```

After the build completes, view the archived HTML under **Artifacts**:

```plaintext theme={null}
[htmlpublisher] Archiving HTML reports...
[htmlpublisher] Archiving at BUILD level ...
```

![The image shows a Jenkins interface displaying artifacts for a project in the "Gitea-Organization" with links to a "pipeline.log" and a "Dependency Check HTML Report."](https://kodekloud.com/kk-media/image/upload/v1752871052/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/jenkins-gitea-artifacts-pipeline-report.jpg)

> **lightbulb** By default, Jenkins enforces a strict Content Security Policy that may strip inline CSS/JS. To allow CSS in archived HTML reports, execute in the **Script Console**:

  ```java theme={null}
  System.setProperty(
    "hudson.model.DirectoryBrowserSupport.CSP",
    "sandbox allow-same-origin; default-src 'self'; img-src 'self'; style-src 'self';"
  );
  ```

  Then rebuild the job to see the styled report.

## 5. Publish JUnit XML Results

Show OWASP results in the **Test Results** tab by adding a `junit` publisher:

1. Ensure the JUnit plugin is installed.
2. In **Snippet Generator**, select **junit**.
3. Configure:
   * Test results: `dependency-check-junit.xml`
   * Allow empty results: `true`
   * Keep properties: `true`

![The image shows a Jenkins workspace interface displaying a list of files and directories with their names, sizes, and modification dates.](https://kodekloud.com/kk-media/image/upload/v1752871054/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/jenkins-workspace-file-list.jpg)

Insert this snippet before or after your existing publishers:

```groovy theme={null}
junit allowEmptyResults: true,
      keepProperties: true,
      testResults: 'dependency-check-junit.xml'
```

Full stage example:

```groovy theme={null}
stage('OWASP Dependency Check') {
  steps {
    dependencyCheck /* ... */
    dependencyCheckPublisher /* ... */

    junit(
      allowEmptyResults: true,
      keepProperties: true,
      testResults: 'dependency-check-junit.xml'
    )

    publishHTML(/* ... */)
  }
}
```

Commit and push:

```bash theme={null}
git commit -am "configure JUnit results for Dependency-Check"
git push
```

## 6. View Test Results and Reports

When the pipeline completes (it may show **unstable** if high-severity issues persist), Jenkins displays a **Test Result** tab:

![The image shows a Jenkins pipeline interface for a project named "solar-system," displaying a dependency scanning process with a warning related to JUnit-formatted test results.](https://kodekloud.com/kk-media/image/upload/v1752871055/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/jenkins-pipeline-solar-system-dependency-scan.jpg)

Click **Test Results** to inspect passes, failures, and detailed CVSS scores, impacts, and patch guidance:

![The image shows a web interface displaying an error message related to a security vulnerability in Express.js, detailing its impact, patches, and workarounds. It also includes a CVSS score and references for further information.](https://kodekloud.com/kk-media/image/upload/v1752871056/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/expressjs-security-error-message.jpg)

In the classic UI, the **Test Results** section lists failures and history:

![The image shows a Jenkins dashboard displaying test results, with 18 failures out of 2,992 tests. A list of failed tests is visible, each with details like test name, duration, and age.](https://kodekloud.com/kk-media/image/upload/v1752871057/notes-assets/images/Certified-Jenkins-Engineer-Demo-Fixing-Vulnerabilities-Publish-HTML-Report/jenkins-dashboard-test-results-failures.jpg)

Your **Dependency Check HTML Report** now renders with full CSS styling and detailed insights into library risks.

***

Thank you for following this guide! For further reading, check out:

* [npm audit documentation](https://docs.npmjs.com/cli/v9/commands/npm-audit)
* [OWASP Dependency-Check](https://jeremylong.github.io/DependencyCheck/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/73d0066f-a01f-4d13-a00c-c9baf9aae603/lesson/31525c0e-3f02-4859-b1f5-f4a92a827be2)


# Demo Install Dependencies

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Setting-up-CI-Pipeline/Demo-Install-Dependencies/page

This tutorial demonstrates integrating a Node.js install step into a Jenkins Pipeline and verifying the Node.js version.

## Demo: Install Node.js Dependencies in Your Jenkins Pipeline

In this tutorial, we’ll show you how to integrate a Node.js install step into your [Jenkins Pipeline][1], verify your Node.js version, and install project dependencies. By the end, you’ll see how Blue Ocean displays your pipeline stages and where the `node_modules` folder appears in the workspace.

### Prerequisites

> **lightbulb** Make sure the [NodeJS Plugin](https://plugins.jenkins.io/nodejs/) is installed and configured under **Manage Jenkins** → **Global Tool Configuration**.

### Pipeline Configuration

1. Open your `Jenkinsfile`.
2. Configure the Node.js tool and define two stages:
   * **VM Node Version**: Verifies `node` and `npm` versions.
   * **Installing Dependencies**: Runs `npm install --no-audit`.

| Stage Name              | Purpose                               | Command                  |
| ----------------------- | ------------------------------------- | ------------------------ |
| VM Node Version         | Check Node.js and npm versions        | `node -v`, `npm -v`      |
| Installing Dependencies | Install project dependencies with npm | `npm install --no-audit` |

```groovy theme={null}
pipeline {
    agent any

    tools {
        nodejs 'nodejs-22-6-0'
    }

    stages {
        stage('VM Node Version') {
            steps {
                sh 'node -v'
                sh 'npm -v'
            }
        }

        stage('Installing Dependencies') {
            steps {
                sh 'npm install --no-audit'
            }
        }
    }
}
```

> **triangle-alert** Using `--no-audit` skips vulnerability checks. Consider running `npm audit` or integrating a security scanner in your CI/CD pipeline for production workloads.

### Run the Pipeline

1. Commit and push your `Jenkinsfile` changes.
2. In [Blue Ocean][3], watch the pipeline execute both stages in sequence.

#### Sample Output for “Installing Dependencies”

```bash theme={null}
+ npm install --no-audit
added 365 packages in 5s
44 packages are looking for funding
run 'npm fund' for details
```

### Verify the Workspace

After the build completes, navigate to **Workspaces** in the Jenkins UI. You should see a `node_modules` directory with all installed dependencies:

![The image shows a Jenkins workspace interface displaying a list of node modules in a project directory. The interface includes navigation options like "Dashboard," "Console Output," and "Open Blue Ocean."](https://kodekloud.com/kk-media/image/upload/v1752871058/notes-assets/images/Certified-Jenkins-Engineer-Demo-Install-Dependencies/jenkins-workspace-node-modules.jpg)

***

## Links and References

* [Jenkins Pipeline][1] – Official Pipeline documentation
* [Node.js][2] – Download and documentation
* [Blue Ocean][3] – Modern Jenkins UI

[1]: https://www.jenkins.io/doc/book/pipeline

[2]: https://nodejs.org/

[3]: https://www.jenkins.io/projects/blueocean/

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/73d0066f-a01f-4d13-a00c-c9baf9aae603/lesson/b71c173b-d4ca-4877-9ee6-7b160efd86ba)
