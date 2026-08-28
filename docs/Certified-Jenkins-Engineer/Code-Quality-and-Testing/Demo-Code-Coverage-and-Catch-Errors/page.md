# Demo Code Coverage and Catch Errors

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Code-Quality-and-Testing/Demo-Code-Coverage-and-Catch-Errors/page

This tutorial explains how to enhance a Jenkins Pipeline with code coverage metrics, error handling, and HTML report publishing.

This tutorial walks you through extending your Jenkins Pipeline to generate code coverage metrics, handle coverage failures gracefully with `catchError`, and publish an HTML coverage report. You’ll update your `Jenkinsfile`, use the Credentials Binding and HTML Publisher plugins, and ensure downstream stages always run.

## Pipeline Stages Overview

| Stage Name              | Purpose                              | Command            |
| ----------------------- | ------------------------------------ | ------------------ |
| Installing Dependencies | Install application dependencies     | `npm install`      |
| Dependency Scanning     | Run security and vulnerability scans | `npm audit`        |
| Unit Testing            | Execute unit tests                   | `npm test`         |
| Code Coverage           | Generate coverage metrics            | `npm run coverage` |

## 1. Add the Code Coverage Stage

Open your `Jenkinsfile` and duplicate the **Unit Testing** stage for coverage:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Installing Dependencies') {
      steps {
        sh 'npm install'
      }
    }
    stage('Dependency Scanning') {
      steps {
        sh 'npm audit'
      }
    }
    stage('Unit Testing') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'mongo-db-credentials',
          usernameVariable: 'MONGO_USERNAME',
          passwordVariable: 'MONGO_PASSWORD'
        )]) {
          sh 'npm test'
        }
      }
    }
    stage('Code Coverage') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'mongo-db-credentials',
          usernameVariable: 'MONGO_USERNAME',
          passwordVariable: 'MONGO_PASSWORD'
        )]) {
          sh 'npm run coverage'
        }
      }
    }
  }
}
```

Commit and push to trigger a new build.

## 2. Observe the Coverage Failure

If coverage falls below your global threshold (e.g., 90%), the pipeline will fail:

```bash theme={null}
> npm run coverage
…
ERROR: Coverage for lines (79.1%) does not meet global threshold (90%)
…
script returned exit code 1
```

<Frame>
  ![The image shows a Jenkins pipeline interface for a project named "solar-system," displaying the stages of a build process with a failure at the "Code Coverage" stage. The details below indicate a failed "npm run coverage" shell script."](https://kodekloud.com/kk-media/image/upload/v1752870465/notes-assets/images/Certified-Jenkins-Engineer-Demo-Code-Coverage-and-Catch-Errors/jenkins-pipeline-solar-system-failure.jpg)
</Frame>

## 3. Introduce catchError

Wrap the coverage command in `catchError` so the stage becomes **UNSTABLE** instead of **FAILED**, allowing later stages to run.

<Callout icon="lightbulb">
  The `catchError` step lets you control both the stage and build result. For full syntax, see the [Jenkins Pipeline Syntax reference](https://www.jenkins.io/doc/book/pipeline/syntax/#catcherror).
</Callout>

Example using the Snippet Generator or manual insertion:

```groovy theme={null}
catchError(
  buildResult: 'SUCCESS',
  stageResult: 'UNSTABLE',
  message: 'Coverage below threshold; will be fixed soon'
) {
  sh 'npm run coverage'
}
```

<Frame>
  ![The image shows a Jenkins interface with a "Snippet Generator" for creating pipeline scripts. It includes options for handling errors, with a message input field containing "Oops!" and settings for build and stage results on error.](https://kodekloud.com/kk-media/image/upload/v1752870466/notes-assets/images/Certified-Jenkins-Engineer-Demo-Code-Coverage-and-Catch-Errors/jenkins-snippet-generator-pipeline.jpg)
</Frame>

## 4. Update the Jenkinsfile

Combine `catchError` with the HTML Publisher plugin to publish coverage reports:

```groovy theme={null}
pipeline {
  agent any
  stages {
    // ... previous stages ...
    stage('Code Coverage') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'mongo-db-credentials',
          usernameVariable: 'MONGO_USERNAME',
          passwordVariable: 'MONGO_PASSWORD'
        )]) {
          catchError(
            buildResult: 'SUCCESS',
            stageResult: 'UNSTABLE',
            message: 'Coverage below threshold; will be fixed soon'
          ) {
            sh 'npm run coverage'
          }
        }
        publishHTML([
          allowMissing: true,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: 'coverage/lcov-report',
          reportFiles: 'index.html',
          reportName: 'Code Coverage HTML Report'
        ])
      }
    }
  }
}
```

Push your changes.

## 5. Verify the Results

Rerun the pipeline. The **Code Coverage** stage will be marked **UNSTABLE** and subsequent stages will still execute.

View the build history and status in the Jenkins dashboard:

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of recent build activities for a project named "solar-system" under the "Gitea-Organization." It includes details such as status, run number, commit ID, branch, message, duration, and completion time.](https://kodekloud.com/kk-media/image/upload/v1752870468/notes-assets/images/Certified-Jenkins-Engineer-Demo-Code-Coverage-and-Catch-Errors/jenkins-dashboard-solar-system-builds.jpg)
</Frame>

In the Pipeline view, stages reflect their new statuses:

<Frame>
  ![The image shows a Jenkins build pipeline interface, displaying the status of various stages such as SCM checkout, tool installation, dependency scanning, and unit testing, with some stages marked as successful and others with issues.](https://kodekloud.com/kk-media/image/upload/v1752870469/notes-assets/images/Certified-Jenkins-Engineer-Demo-Code-Coverage-and-Catch-Errors/jenkins-build-pipeline-status.jpg)
</Frame>

## 6. View the HTML Coverage Report

Click **Code Coverage HTML Report** in Jenkins to open `coverage/lcov-report/index.html`. You’ll see detailed metrics for each file—e.g., for `app.js`:

* Statement coverage: 79.54%
* Branch coverage: 33.33%
* Function coverage: 70%
* Line coverage: 79.06%

<Frame>
  ![The image shows a code coverage report for a file named "app.js," indicating 79.54% statement coverage, 33.33% branch coverage, 70% function coverage, and 79.06% line coverage.](https://kodekloud.com/kk-media/image/upload/v1752870470/notes-assets/images/Certified-Jenkins-Engineer-Demo-Code-Coverage-and-Catch-Errors/code-coverage-report-app-js.jpg)
</Frame>

You can also view this report in Blue Ocean or any HTML-compatible Jenkins plugin.

***

## Links and References

* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [HTML Publisher Plugin](https://plugins.jenkins.io/htmlpublisher/)
* [Credentials Binding Plugin](https://plugins.jenkins.io/credentials-binding/)
* [npm Documentation](https://docs.npmjs.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7214771c-8a65-4b34-94a9-43665202a4e4/lesson/3db3f706-ca2d-41b8-b1fb-a03985a93304" />
</CardGroup>
