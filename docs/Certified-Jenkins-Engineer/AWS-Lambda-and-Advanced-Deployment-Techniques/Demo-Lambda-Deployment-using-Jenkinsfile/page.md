# Demo Lambda Deployment using Jenkinsfile

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/AWS-Lambda-and-Advanced-Deployment-Techniques/Demo-Lambda-Deployment-using-Jenkinsfile/page

This article provides a tutorial on automating AWS Lambda deployments using Jenkins, covering environment setup, code modifications, and CI/CD pipeline integration.

In this hands-on tutorial, we automate AWS Lambda deployments with Jenkins. By customizing our Lambda function code, packaging artifacts, uploading to Amazon S3, and triggering updates via the AWS CLI, we'll achieve a seamless CI/CD pipeline.

## 1. Clearing Existing Environment Variables

First, in the AWS Lambda console, navigate to your function named **solar-system-function**. Under **Configuration**, click **Edit**, remove all environment variables, and hit **Save**. We'll inject these values dynamically in Jenkins.

<Frame>
  ![The image shows an AWS Lambda console page for a function named "solar-system-function," displaying its overview, configuration options, and function details.](https://kodekloud.com/kk-media/image/upload/v1752870255/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/aws-lambda-solar-system-function.jpg)
</Frame>

<Callout icon="lightbulb">
  Removing environment variables here ensures that Jenkins controls all runtime settings securely.
</Callout>

## 2. Preparing the Local Workspace

On your build VM or local machine, clean up any existing sandbox and checkout the latest code from the `solar-system` repository:

<Frame>
  ![The image shows a Visual Studio Code interface with a Jenkinsfile open, displaying stages for a CI/CD pipeline. Below, there's a terminal session connected to a remote server.](https://kodekloud.com/kk-media/image/upload/v1752870256/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/visual-studio-code-jenkinsfile-cicd.jpg)
</Frame>

```bash theme={null}
cd ~
rm -rf sandbox
cd ~/solar-system
git fetch origin
git checkout main
git pull
```

You should see the new `Jenkinsfile` and updated files ready:

| File                            | Changes                           |
| ------------------------------- | --------------------------------- |
| Jenkinsfile                     | +328 insertions, updated pipeline |
| index.html                      | +30 additions                     |
| integration-testing-ec2.sh      | minor revision                    |
| package-lock.json, package.json | dependency updates                |
| zap\_ignore\_rules              | new rules                         |

## 3. Adding the Lambda Deployment Stage

In `Jenkinsfile`, add a new stage under `stages` called **Lambda - S3 Upload & Deploy**. This stage triggers only on the `main` branch, modifies `app.js` to work in Lambda, creates a zip package, uploads it to S3, and then updates the Lambda function code:

```groovy theme={null}
stage('Lambda - S3 Upload & Deploy') {
    when { branch 'main' }
    steps {
        withAWS(credentials: 'aws-s3-ec2-lambda-creds', region: 'us-east-2') {
            sh '''
                echo "----- Before Modification -----"
                tail -5 app.js

                echo "----- Modifying app.js for Lambda -----"
                sed -i "/app\\.listen(3000/s/^\\/\\///" app.js
                sed -i "s|module.exports = app;|//module.exports = app;|g" app.js
                sed -i "s|//module.exports.handler|module.exports.handler|g" app.js

                echo "----- After Modification -----"
                tail -5 app.js
            '''

            sh '''
                echo "----- Creating deployment package -----"
                zip -qr solar-system-lambda-${BUILD_ID}.zip app* package* index.html node*
                ls -ltr solar-system-lambda-${BUILD_ID}.zip
            '''

            s3Upload(
                file: "solar-system-lambda-${BUILD_ID}.zip",
                bucket: 'solar-system-lambda-bucket'
            )
        }

        sh '''
            echo "----- Updating Lambda function code -----"
            aws lambda update-function-code \
                --function-name solar-system-function \
                --s3-bucket solar-system-lambda-bucket \
                --s3-key solar-system-lambda-${BUILD_ID}.zip
        '''
    }
}
```

<Callout icon="lightbulb">
  Ensure the AWS credentials you reference (`aws-s3-ec2-lambda-creds`) have `s3:PutObject` and `lambda:UpdateFunctionCode` permissions.
</Callout>

## 4. Bumping the Frontend Version

Increment the frontend version number in `index.html` (near line 66) to `v5.0` to reflect new changes:

<Frame>
  ![The image shows a code editor with HTML and CSS code for styling a button and an input field. The editor interface includes a file explorer on the left and a terminal at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752870257/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/code-editor-html-css-button-input.jpg)
</Frame>

After updating, save the file.

## 5. AWS CLI Reference

For more details on the `update-function-code` command, consult the AWS CLI reference:

[Lambda update-function-code](https://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-code.html)

<Frame>
  ![The image shows a webpage from the AWS CLI Command Reference, specifically detailing the "update-function-code" command for AWS Lambda, including its description and usage instructions.](https://kodekloud.com/kk-media/image/upload/v1752870259/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/aws-cli-update-function-code-lambda.jpg)
</Frame>

| Parameter       | Description                            | Example                     |
| --------------- | -------------------------------------- | --------------------------- |
| --function-name | Name of the Lambda function            | solar-system-function       |
| --s3-bucket     | S3 bucket holding deployment package   | solar-system-lambda-bucket  |
| --s3-key        | Key (path) to the zip in the S3 bucket | solar-system-lambda-123.zip |

## 6. Committing and Pushing Changes

Stage and commit your updates, then push to the `main` branch. This action triggers the Jenkins pipeline automatically:

<Frame>
  ![The image shows a Jenkins pipeline interface with various stages of a deployment process, including building a Docker image, vulnerability scanning, and deploying to AWS. It prompts the user to decide whether to deploy to production.](https://kodekloud.com/kk-media/image/upload/v1752870260/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/jenkins-pipeline-deployment-process.jpg)
</Frame>

```bash theme={null}
git add Jenkinsfile index.html
git commit -m "Add Lambda deployment stage and bump frontend version"
git push origin main
```

Follow any manual approval prompts in Jenkins to proceed.

## 7. Validating the Deployment in S3

After the build completes, verify that the new ZIP artifact appears in your S3 bucket:

<Frame>
  ![The image shows an Amazon S3 bucket interface with two zip files named "solar-system-lambda-2.zip" and "solar-system-lambda.zip," both 9.9 MB in size. The files are listed with details such as last modified date and storage class.](https://kodekloud.com/kk-media/image/upload/v1752870261/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/amazon-s3-bucket-zip-files.jpg)
</Frame>

## 8. Troubleshooting: Missing Environment Variables

If you encounter an **Internal Server Error**, it often indicates missing environment variables. Check CloudWatch logs to debug:

<Frame>
  ![The image shows an AWS CloudWatch log screen displaying an error message related to a Mongoose connection issue, indicating that the URI parameter must be a string but received "undefined".](https://kodekloud.com/kk-media/image/upload/v1752870262/notes-assets/images/Certified-Jenkins-Engineer-Demo-Lambda-Deployment-using-Jenkinsfile/aws-cloudwatch-mongoose-error-log.jpg)
</Frame>

In `app.js` you’ll find:

```javascript theme={null}
// app.js (excerpt)
const mongoose = require('mongoose');
// ...
mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
}, (err) => {
  if (err) {
    console.error("MongoDB Connection Error:", err);
  } else {
    console.log("MongoDB Connection Successful");
  }
});
```

Here, `process.env.MONGO_URI`, `MONGO_USERNAME`, and `MONGO_PASSWORD` must be supplied by Jenkins.

<Callout icon="triangle-alert">
  Without proper environment variables, your Lambda function will fail to connect to MongoDB.
</Callout>

## 9. Next Steps: Injecting Environment Variables via Jenkins

To address missing credentials, update your `pipeline` block in `Jenkinsfile`. Add an `environment` section with secure credential bindings:

```groovy theme={null}
pipeline {
    agent any

    environment {
        MONGO_URI          = credentials('mongo-db-uri')
        MONGO_USERNAME     = credentials('mongo-db-username')
        MONGO_PASSWORD     = credentials('mongo-db-password')
        SONAR_SCANNER_HOME = tool 'sonarqube-scanner-610'
        GITEA_TOKEN        = credentials('gitea-api-token')
    }

    stages {
        // … existing stages … 
        stage('Lambda - S3 Upload & Deploy') { … }
    }
}
```

By following these steps, you’ll ensure your AWS Lambda deployments are automated, secure, and maintainable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7e65cc00-b745-498e-8351-c294cbe958ec/lesson/cb882b28-99c4-43f0-9edb-5db9eff82bed" />
</CardGroup>
