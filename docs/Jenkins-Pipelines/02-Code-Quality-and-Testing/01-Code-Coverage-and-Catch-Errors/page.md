# Install dependencies
npm install
npm init -y
npm install express serverless-http

# Package the application
zip -r my-node-app.zip index.js node_modules

# Update Lambda function using a local zip file
aws lambda update-function-code --function-name my-function --zip-file fileb://my-node-app.zip

# Alternatively, update using an S3 bucket
aws s3 cp my-node-app.zip s3://my-bucket/my-node-app.zip
aws lambda update-function-code --function-name my-function --s3-bucket my-bucket --s3-key my-node-app.zip

# Retrieve function URL configuration
aws lambda get-function-url-config --function-name my-function
```

For a brief modification of your application code to ensure Lambda compatibility, you can use:

```javascript theme={null}
const express = require('express');
const serverless = require('serverless-http');

const app = express();

app.get('/', (req, res) => {
  res.send('Hello, AWS Lambda!');
});

module.exports.handler = serverless(app);
```

Additionally, to adjust the `app.js` file if needed, you might run:

```bash theme={null}
# Example commands to comment out local server startup code
sed -i 's/app\.listen(3000/\/\/ app.listen(3000/' app.js
sed -i 's/module.exports = app;/\/\/ module.exports = app;/' app.js
```

<Callout icon="lightbulb">
  In the next session, these commands will be executed manually to validate the deployment process. Subsequent automation will be implemented using a Jenkins pipeline.
</Callout>

Thank you for following this lesson on using GenAI to streamline Lambda deployment via a Jenkins pipeline.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-pipelines/module/78297356-097c-4793-b690-bc83f9aba3f0/lesson/2cbd5829-628c-411e-a118-0cc8bafd50c7" />
</CardGroup>


# Code Coverage and Catch Errors

Source: https://notes.kodekloud.com/docs/Jenkins-Pipelines/Code-Quality-and-Testing/Code-Coverage-and-Catch-Errors/page

This tutorial demonstrates adding a Jenkins pipeline stage for code coverage while handling errors gracefully.

In this tutorial, we demonstrate how to add a new stage to your Jenkins pipeline for running code coverage while gracefully catching errors. By updating your Jenkinsfile, you can ensure that even if the code coverage fails to meet the required threshold, the build continues to subsequent stages.

## Original Unit Testing Stage

For reference, here is the original unit testing stage from your Jenkinsfile:

```groovy theme={null}
stage('Unit Testing') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'mongo-db-credentials', passwordVariable: 'MONGO')]) {
            sh 'npm test'
        }
    }
}
```

```bash theme={null}
root@jenkins-controller-1 in solar-system on feature/enabling-cicd via v20.16.0
```

Since code coverage also requires MongoDB credentials, we update the command to use `npm run coverage` in a new stage.

## Pipeline Behavior with Code Coverage Failure

After committing your changes, a new pipeline (e.g. build #17) is triggered where the code coverage stage might fail if the coverage percentage is below the global threshold (e.g. 79% instead of 90%). The following image shows a Jenkins pipeline interface for the "solar-system" project with a failed code coverage step:

<Frame>
  ![The image shows a Jenkins pipeline interface for a project named "solar-system" with a failed code coverage step. The pipeline includes stages like installing dependencies, dependency scanning, unit testing, and code coverage.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879598/notes-assets/images/Jenkins-Pipelines-Code-Coverage-and-Catch-Errors/jenkins-pipeline-solar-system-failed.jpg)
</Frame>

Examining the logs reveals that the build fails due to insufficient coverage. To handle such errors and proceed to the next stages, use the `catchError` step.

## Using catchError to Handle Failures

The `catchError` step can catch exceptions and allow you to specify a custom message, as well as setting the build status to success while marking the specific stage as unstable. Here is a basic snippet demonstrating how to use `catchError`:

```groovy theme={null}
catchError {
    sh 'might fail'
}
step([$class: 'Mailer', recipients: 'admin@somewhere'])
```

You can also use `catchError` within a node block:

```groovy theme={null}
node {
    catchError {
        sh 'might fail'
    }
    step([$class: 'Mailer', recipients: 'admin@somewhere'])
}
```

<Callout icon="lightbulb">
  In the `catchError` block, you have the option to customize the error message and control both the build and stage results.
</Callout>

## Updated Code Coverage Stage in Jenkinsfile

Below is the updated "Code Coverage" stage, where the code coverage command is wrapped within a `catchError` block. This configuration marks the stage as unstable while allowing the build to succeed. Additionally, an HTML report is published after running the coverage command.

```groovy theme={null}
stage('Code Coverage') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'mongo-db-credentials', passwordVariable: 'MONGO_PASSWORD', usernameVariable: 'MONGO_USERNAME')]) {
            catchError(buildResult: 'SUCCESS', message: 'Oops! it will be fixed in future releases', stageResult: 'UNSTABLE') {
                sh 'npm run coverage'
            }
        }
        publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'coverage/lcov-report', reportFiles: 'index.html', reportName: 'Code Coverage HTML Report', reportTitles: '', useWrapperFileDirectly: true])
    }
}
```

```bash theme={null}
root@jenkins-controller-1 in solar-system on 🐳 feature/enabling-cicd via 🎈 v20.16.0
>
```

After running `npm run coverage`, the log output shows a failure due to low coverage:

```bash theme={null}
+ npm run coverage

> Solar System@6.7.6 coverage
> nyc --reporter cobertura --reporter text --reporter json-summary mocha app-test.js --timeout 10000 --exit

Server successfully running on port - 3000

(node:94566) [DEP1700] DeprecationWarning: The URL mongodb://supercluster-shard-00-01.d83jj.mongodb.net:27017,supercluster-shard-00-02.d83jj.mongodb.net:27017,supercluster-shard-00-00.d83jj.mongodb.net:27017/?authSource=admin&replicaSet=atlas-11b0vt-shard-0&ssl=true is invalid. Future versions of Node.js will throw an error.

Fetching Planet Details
  ✔ it should fetch a planet named Mercury (252ms)
  ✔ it should fetch a planet named Venus (249ms)
  ✔ it should fetch a planet named Earth (280ms)
  ✔ it should fetch a planet named Mars (255ms)
  ✔ it should fetch a planet named Jupiter (234ms)
  ✔ it should fetch a planet named Saturn (248ms)
  ✔ it should fetch a planet named Neptune (247ms)

Testing Other Endpoints
  ✔ it should fetch OS Details
  ✔ it should fetch Live Status
```

<Callout icon="triangle-alert">
  Even though the `npm run coverage` command outputs an error message for failing the coverage threshold, the catchError block ensures that the build proceeds and the stage is marked as unstable.
</Callout>

## Dashboard and HTML Coverage Report

After the changes, a new build is triggered. The dashboard now displays the build status accordingly. For example, the dashboard below shows the list of recent builds for the "solar-system" project, including each build's status, run number, commit ID, branch, message, duration, and completion time:

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of recent builds for the "solar-system" project, including their status, run number, commit ID, branch, message, duration, and completion time.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879600/notes-assets/images/Jenkins-Pipelines-Code-Coverage-and-Catch-Errors/jenkins-dashboard-solar-system-builds.jpg)
</Frame>

The HTML report generated during the coverage stage is stored in the workspace and published. You can click the report link in the Classic UI or view it in Blue Ocean.

Below is a snippet from the log that shows the archiving of the HTML report:

```text theme={null}
[htmlPublisher] Archiving HTML reports...
[htmlPublisher] Archiving at BUILD level /var/lib/jenkins/workspace/lar-system_feature_enabling-cidc/coverage/lcov-report to /var/lib/jenkins/jobs/Gitea-Organization/jobs/solar-system/branches/feature-enabling-cidc/do7qr/builds/18/htmlreports/Code_20Coverage_20HTML_20Report
[htmlPublisher] Copying recursive using current thread
```

Additionally, you can view the detailed code coverage for the "app.js" file in the following report:

<Frame>
  ![The image shows a code coverage report for a file named "app.js," indicating 79.54% statement coverage, 33.33% branch coverage, 70% function coverage, and 79.06% line coverage.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879600/notes-assets/images/Jenkins-Pipelines-Code-Coverage-and-Catch-Errors/code-coverage-report-app-js.jpg)
</Frame>

## Conclusion

By configuring the pipeline to use the `catchError` step, you ensure that code coverage errors do not block the overall build process. The stage is marked as unstable, and crucial reports, such as the HTML coverage report, remain available for further analysis. This approach not only minimizes build disruptions but also provides detailed insights into code quality and testing coverage.

For more on Jenkins pipelines and CI/CD best practices, check out the following resources:

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

Thank you for reading this guide on configuring code coverage with error handling in Jenkins pipelines.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-pipelines/module/bcd4711c-8a69-4218-a65c-113fd7a7a88d/lesson/50b67087-7e45-4a3f-a5cf-894697291ace" />
</CardGroup>
