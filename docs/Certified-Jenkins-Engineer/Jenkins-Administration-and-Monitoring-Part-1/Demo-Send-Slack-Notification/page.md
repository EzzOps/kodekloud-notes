# Demo Send Slack Notification

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-1/Demo-Send-Slack-Notification/page

This guide enhances a Jenkinsfile to send Slack notifications based on build outcomes, creating a reusable Groovy helper for team alerts.

In this guide, you’ll enhance the `Jenkinsfile` in the **solar-system** repository to send Slack notifications based on build outcomes. By the end, you’ll have a reusable Groovy helper and a DRY pipeline that alerts your team of successes, instabilities, and failures.

## 1. Create a Feature Branch

Start by branching off from `main`:

```bash theme={null}
git checkout -b feature/enabling-slack
Switched to a new branch 'feature/enabling-slack'
```

## 2. Generate the Slack Step

Open **Pipeline Syntax** in Jenkins:

1. Select **Slack Send**.
2. Configure your channel (e.g., `#dasher-notifications`).
3. Set a default message and a hex color for “Build Started.”

<Frame>
  ![The image shows a Jenkins Pipeline Syntax page where a user is configuring a Slack message to be sent to a specific channel named "dasher-notifications."](https://kodekloud.com/kk-media/image/upload/v1752870655/notes-assets/images/Certified-Jenkins-Engineer-Demo-Send-Slack-Notification/jenkins-pipeline-slack-message-dasher.jpg)
</Frame>

You can pick a hex code to reflect status:

<Frame>
  ![The image shows a Jenkins pipeline syntax configuration screen for sending Slack messages, with fields for channel, message, and color settings. The color is set to a hex code, and there are options for advanced settings and workspace credentials.](https://kodekloud.com/kk-media/image/upload/v1752870655/notes-assets/images/Certified-Jenkins-Engineer-Demo-Send-Slack-Notification/jenkins-pipeline-slack-configuration.jpg)
</Frame>

Pipeline syntax will produce:

```groovy theme={null}
slackSend botUser: true,
          channel: '#dasher-notifications',
          color: '#439FE0',
          message: "Build Started: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
```

<Callout icon="lightbulb">
  Ensure you have [configured your Slack App and credentials](/docs/slack-integration#setup) in Jenkins **Manage Credentials** before using `slackSend`.
</Callout>

## 3. Why Reuse Is Better

Adding identical `slackSend` calls under every stage’s `post` block quickly becomes unwieldy:

```groovy theme={null}
pipeline {
  /* ... */
  stages {
    stage('Upload - AWS S3') {
      steps { /* ... */ }
      post {
        success {
          slackSend botUser: true,
                    channel: '#dasher-notifications',
                    color: '#47ec05',
                    message: "Upload S3 succeeded: ${env.BUILD_NUMBER}"
        }
        failure {
          slackSend botUser: true,
                    channel: '#dasher-notifications',
                    color: '#ec2805',
                    message: "Upload S3 failed: ${env.BUILD_NUMBER}"
        }
      }
    }
    // more stages...
  }
}
```

<Frame>
  ![The image shows a Jenkins interface with options for setting post-stage or build conditions, including checkboxes for various build statuses.](https://kodekloud.com/kk-media/image/upload/v1752870657/notes-assets/images/Certified-Jenkins-Engineer-Demo-Send-Slack-Notification/jenkins-post-stage-build-conditions.jpg)
</Frame>

## 4. Define a Reusable Slack Method

At the top of your `Jenkinsfile`, add:

```groovy theme={null}
def slackNotification(String buildStatus = 'STARTED') {
    buildStatus = buildStatus ?: 'SUCCESS'

    // Map status to color
    def color = buildStatus == 'SUCCESS'  ? '#47ec05' :
                buildStatus == 'UNSTABLE' ? '#d5ee0d' :
                                            '#ec2805'

    // Construct message
    def msg = "${buildStatus}: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
    slackSend color: color, message: msg
}
```

### Build Status Color Mapping

| Build Status | Hex Color |
| ------------ | --------- |
| SUCCESS      | #47ec05   |
| UNSTABLE     | #d5ee0d   |
| FAILURE      | #ec2805   |

## 5. Update the Pipeline

Use a single `post { always { ... } }` block:

```groovy theme={null}
pipeline {
    agent any
    tools {
        // e.g., nodejs '12.x'
    }
    stages {
        stage('Installing Dependencies') {
            steps {
                sh 'npm install --no-audit'
            }
        }
        stage('Code Coverage') {
            steps {
                catchError(buildResult: 'SUCCESS', message: 'Coverage step failed but allowed') {
                    sh 'npm run coverage'
                }
            }
        }
        // additional stages...
    }
    post {
        always {
            slackNotification(currentBuild.result)
        }
        cleanup {
            sh 'rm -rf solar-system-gitops-argocd'
        }
        junit allowEmptyResults: true, testResults: 'test-results.xml'
    }
}
```

Commit and push:

```bash theme={null}
git add Jenkinsfile
git commit -m "feat: enable Slack notifications"
git push -u origin feature/enabling-slack
```

Trigger a build to see the consolidated Slack notification:

<Frame>
  ![The image shows a Jenkins pipeline interface for a project named "solar-system," displaying various stages of the build process, including dependency scanning, unit testing, and deployment. Each stage is marked with a status indicator, and the integration testing stage is highlighted.](https://kodekloud.com/kk-media/image/upload/v1752870658/notes-assets/images/Certified-Jenkins-Engineer-Demo-Send-Slack-Notification/jenkins-pipeline-solar-system-build.jpg)
</Frame>

## 6. Demonstrate Failure

Add a failing step to confirm a red alert:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Fail Fast') {
            steps {
                sh 'echo "Simulating failure"; exit 1'
            }
        }
    }
    post {
        always {
            slackNotification(currentBuild.result)
        }
    }
}
```

Push and rebuild. The Slack notification color should switch to red on failure.

<Callout icon="triangle-alert">
  Never hardcode sensitive tokens in your `Jenkinsfile`. Use [Jenkins Credentials Binding](/docs/credentials-binding) for secure handling.
</Callout>

## 7. Next Steps

To reuse `slackNotification` across multiple repositories, extract it into a [Shared Library](https://www.jenkins.io/doc/book/pipeline/shared-libraries/). This centralizes common pipeline logic and keeps your `Jenkinsfile` lean.

***

## Links and References

* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Slack Plugin for Jenkins](https://plugins.jenkins.io/slack/)
* [Jenkins Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
* [JUnit Plugin](https://plugins.jenkins.io/junit/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/2dad0443-4a98-459f-9722-83f412c970b5" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/833ee576-11b7-4cbe-872e-bf91c4d3f93c" />
</CardGroup>
