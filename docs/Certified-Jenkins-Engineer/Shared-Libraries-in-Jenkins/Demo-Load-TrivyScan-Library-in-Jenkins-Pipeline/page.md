# You should see:
# vars
```

## 2. Create a Feature Branch

Work on a dedicated branch to isolate your changes:

```bash theme={null}
git checkout -b feature/trivy-scan
```

## 3. Review the Hardcoded Trivy Stage

In many pipelines, you’ll find a stage like this in the application’s `Jenkinsfile`:

```groovy theme={null}
stage('Trivy Vulnerability Scanner') {
  steps {
    sh '''
      trivy image my-org/app:$GIT_COMMIT \
        --severity LOW,MEDIUM,HIGH \
        --exit-code 0 \
        --quiet \
        --format json -o trivy-medium.json

      trivy image my-org/app:$GIT_COMMIT \
        --severity CRITICAL \
        --exit-code 1 \
        --quiet \
        --format json -o trivy-critical.json
    '''
  }
  post {
    always {
      // report conversion steps...
    }
  }
}
```

<Callout icon="triangle-alert">
  Hardcoding scanner commands in every `Jenkinsfile` is hard to maintain. Any change in flags or output formats would need updates in all pipelines.
</Callout>

## 4. Create the `TrivyScan.groovy` in `vars/`

Inside your shared-library’s `vars/` folder, add a new file:

```bash theme={null}
cd vars
touch TrivyScan.groovy
```

## 5. Define the `vulnerability` Function

Open `vars/TrivyScan.groovy` and add a method that accepts the Docker image name:

```groovy theme={null}
def vulnerability(String imageName) {
    sh """
      echo "🔒 Scanning image: ${imageName}"
      trivy image ${imageName} \
        --severity LOW,MEDIUM,HIGH \
        --exit-code 0 \
        --quiet \
        --format json -o trivy-medium.json

      trivy image ${imageName} \
        --severity CRITICAL \
        --exit-code 1 \
        --quiet \
        --format json -o trivy-critical.json
    """
}
```

<Callout icon="lightbulb">
  We use triple-double-quotes (`"""…"""`) in Groovy to allow `${imageName}` interpolation inside the shell script block.
</Callout>

## 6. Add the `reportsConverter` Function

Extend the same file with report conversion logic:

```groovy theme={null}
def reportsConverter() {
    sh '''
      trivy convert \
        --format template --template "@usr/local/share/trivy/templates/html.tpl" \
        --output trivy-medium.html trivy-medium.json

      trivy convert \
        --format template --template "@usr/local/share/trivy/templates/html.tpl" \
        --output trivy-critical.html trivy-critical.json

      trivy convert \
        --format template --template "@usr/local/share/trivy/templates/junit.tpl" \
        --output trivy-medium.xml trivy-medium.json

      trivy convert \
        --format template --template "@usr/local/share/trivy/templates/junit.tpl" \
        --output trivy-critical.xml trivy-critical.json
    '''
}
```

## 7. Commit and Push Your Changes

Save, commit, and push the new shared-library logic:

```bash theme={null}
git add vars/TrivyScan.groovy
git commit -m "feat: add TrivyScan shared library (vulnerability + reportsConverter)"
git push --set-upstream origin feature/trivy-scan
```

## 8. Consume the Shared Library in a Pipeline

In your application’s `Jenkinsfile`, load the library and call the functions:

```groovy theme={null}
@Library('shared-libraries@feature/trivy-scan') _

pipeline {
  agent any
  stages {
    stage('Security Checks') {
      steps {
        TrivyScan.vulnerability("my-org/app:${env.GIT_COMMIT}")
        TrivyScan.reportsConverter()
      }
    }
  }
}
```

Now your security scan is centralized, versioned, and easy to update!

## References

* [Jenkins Shared Library Documentation][jenkins-shared-library]
* [Trivy – A Simple and Comprehensive Vulnerability Scanner][trivy-docs]
* [Jenkins Pipeline Syntax][jenkins-pipeline]

[jenkins-shared-library]: https://www.jenkins.io/doc/book/pipeline/shared-libraries/

[trivy-docs]: https://github.com/aquasecurity/trivy

[jenkins-pipeline]: https://www.jenkins.io/doc/book/pipeline/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/b0fefde6-7fea-44da-9509-27007d27869f/lesson/41e1b0c6-546b-4077-a721-248cb87bc549" />
</CardGroup>


# Demo Load TrivyScan Library in Jenkins Pipeline

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Shared-Libraries-in-Jenkins/Demo-Load-TrivyScan-Library-in-Jenkins-Pipeline/page

This tutorial explains how to integrate a TrivyScan shared library into a Jenkins pipeline for automated vulnerability scanning and report generation.

In this tutorial, you’ll learn how to integrate a custom TrivyScan shared library into your Jenkins pipeline to automate vulnerability scanning and report generation. We will walk through the following steps:

1. Define TrivyScan methods in your shared library
2. Configure the global pipeline library in Jenkins
3. Override the default library version using a feature branch
4. Invoke the `vulnerability` and `reportsConverter` methods inside a declarative pipeline
5. Wrap library calls in `script` blocks to comply with pipeline syntax
6. View generated reports and Slack notifications

***

## 1. Define TrivyScan Methods in Your Shared Library

Create `vars/TrivyScan.groovy` in your shared library repository with two methods:

* **vulnerability**: Runs Trivy image scans with different severity thresholds
* **reportsConverter**: Converts JSON scan results into HTML and JUnit XML

```groovy theme={null}
// vars/TrivyScan.groovy

def vulnerability(String imageName) {
    sh """
        echo "Scanning image: ${imageName}"
        trivy image ${imageName} \
            --severity LOW,MEDIUM,HIGH \
            --exit-code 0 --quiet \
            --format json -o trivy-image-MEDIUM-results.json

        trivy image ${imageName} \
            --severity CRITICAL \
            --exit-code 1 --quiet \
            --format json -o trivy-image-CRITICAL-results.json
    """
}

def reportsConverter() {
    sh """
        # Convert to HTML reports
        trivy convert --format template \
            --template "@/usr/local/share/trivy/templates/html.tpl" \
            --output trivy-image-MEDIUM-results.html trivy-image-MEDIUM-results.json

        trivy convert --format template \
            --template "@/usr/local/share/trivy/templates/html.tpl" \
            --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json

        # Convert to JUnit XML reports
        trivy convert --format template \
            --template "@/usr/local/share/trivy/templates/junit.tpl" \
            --output trivy-image-MEDIUM-results.xml trivy-image-MEDIUM-results.json

        trivy convert --format template \
            --template "@/usr/local/share/trivy/templates/junit.tpl" \
            --output trivy-image-CRITICAL-results.xml trivy-image-CRITICAL-results.json
    """
}
```

Commit and push on a feature branch:

```bash theme={null}
git checkout -b featureTrivyScan
git add vars/TrivyScan.groovy
git commit -m "Add TrivyScan shared library methods"
git push origin featureTrivyScan
```

***

## 2. Configure Jenkins Global Pipeline Library

In Jenkins, go to **Manage Jenkins** → **Configure System** → **Global Pipeline Libraries** and add or update your library:

| Property                       | Value                         |
| ------------------------------ | ----------------------------- |
| Name                           | dasher-trusted-shared-library |
| Default version                | main                          |
| Allow default version override | ☑️ Enabled                    |

<Frame>
  ![The image shows a Jenkins configuration screen for managing global trusted pipeline libraries, with options to set the library name, default version, and other settings.](https://kodekloud.com/kk-media/image/upload/v1752871101/notes-assets/images/Certified-Jenkins-Engineer-Demo-Load-TrivyScan-Library-in-Jenkins-Pipeline/jenkins-global-pipeline-libraries-config.jpg)
</Frame>

Enabling version override allows pipelines to specify a branch or tag in the `@Library` annotation.

***

## 3. Load a Specific Library Version in Your Jenkinsfile

At the very top of your `Jenkinsfile`, reference the feature branch:

```groovy theme={null}
@Library('dasher-trusted-shared-library@featureTrivyScan') _
```

This makes the `trivyScan` methods available to your pipeline.

***

## 4. Invoke TrivyScan Methods in a Declarative Pipeline

Below is a sample Declarative Pipeline that:

* Builds a Docker image
* Runs Trivy scans
* Converts scan results to HTML and JUnit
* Publishes the reports

```groovy theme={null}
@Library('dasher-trusted-shared-library@featureTrivyScan') _

pipeline {
    agent any

    environment {
        GIT_COMMIT = "${env.GIT_COMMIT}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image"
                sh 'docker build -t myrepo/solar-system:${GIT_COMMIT} .'
            }
        }

        stage('Trivy Vulnerability Scanner') {
            steps {
                script {
                    trivyScan.vulnerability("myrepo/solar-system:${GIT_COMMIT}")
                }
            }
            post {
                always {
                    script {
                        trivyScan.reportsConverter()
                    }
                    publishHTML([
                        allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true,
                        reportDir: '.', reportFiles: 'trivy-image-*.html', reportName: 'Trivy HTML Reports'
                    ])
                    publishHTML([
                        allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true,
                        reportDir: '.', reportFiles: 'trivy-image-*.xml', reportName: 'Trivy JUnit Reports'
                    ])
                }
            }
        }
    }
}
```

<Callout icon="lightbulb">
  In Declarative Pipelines, any method calls on shared library objects must be wrapped inside a `script {}` block to avoid syntax errors.
</Callout>

***

## 5. View Pipeline Output and Reports

Once you push your branch, Jenkins will trigger a build. In the **Console Output**, look for `trivy image ...` commands:

```bash theme={null}
echo "Scanning image: myrepo/solar-system:c9dc5eb9b28174642a87fb0e2c8f92845fa4b1d"
trivy image myrepo/solar-system:c9dc5eb9b28174642a87fb0e2c8f92845fa4b1d --severity LOW,MEDIUM,HIGH --exit-code 0 --quiet --format json -o trivy-image-MEDIUM-results.json
trivy image myrepo/solar-system:c9dc5eb9b28174642a87fb0e2c8f92845fa4b1d --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json
...
```

In **Pipeline Artifacts**, you’ll find both HTML and XML reports:

<Frame>
  ![The image shows a Jenkins interface displaying artifacts from a build pipeline, including a pipeline log and Trivy vulnerability reports.](https://kodekloud.com/kk-media/image/upload/v1752871102/notes-assets/images/Certified-Jenkins-Engineer-Demo-Load-TrivyScan-Library-in-Jenkins-Pipeline/jenkins-build-pipeline-artifacts.jpg)
</Frame>

***

## 6. Verify Slack Notifications

If you also have a Slack notifications shared library on this branch, you should see build alerts in your channel:

<Frame>
  ![The image shows a Slack workspace with a channel named "#dasher-notifications" displaying Jenkins build notifications, indicating both successful and failed builds. The interface includes various tabs and options for managing channels and direct messages.](https://kodekloud.com/kk-media/image/upload/v1752871103/notes-assets/images/Certified-Jenkins-Engineer-Demo-Load-TrivyScan-Library-in-Jenkins-Pipeline/slack-workspace-dasher-notifications.jpg)
</Frame>

<Callout icon="triangle-alert">
  Make sure your Slack token and channel are configured securely in Jenkins credentials to prevent unauthorized access.
</Callout>

***

## Links and References

* [Jenkins Pipeline Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
* [Trivy: A Simple and Comprehensive Vulnerability Scanner](https://github.com/aquasecurity/trivy)
* [publishHTML Plugin](https://plugins.jenkins.io/publish-html/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/b0fefde6-7fea-44da-9509-27007d27869f/lesson/3f7f8cfc-1218-43a6-aa38-314efd16d24b" />
</CardGroup>
