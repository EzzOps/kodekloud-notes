# (Optional) Install the Serverless Framework CLI globally
npm install -g serverless
```

> **lightbulb** The `serverless-http` library wraps your Express application into a handler function that AWS Lambda can invoke.

***

## 3. Do we need to modify the application code (`app.js`) for AWS Lambda?

Yes. Wrap your Express app using `serverless-http` and export the handler:

```javascript theme={null}
const express = require('express');
const serverless = require('serverless-http');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello, AWS Lambda!');
});

module.exports.handler = serverless(app);
```

![The image shows a webpage from Copilot, explaining how to build AWS Lambda functions using Node.js and Express. It details the use of module.exports, handler, and serverless(app) for adapting applications to AWS Lambda.](https://kodekloud.com/kk-media/image/upload/v1752870282/notes-assets/images/Certified-Jenkins-Engineer-Demo-Using-GenAI-to-Generate-Steps-for-Lambda-Deployment/aws-lambda-nodejs-express-guide.jpg)

***

## 4. What is the AWS CLI command to update a Lambda function’s code?

If your function already exists, run:

```bash theme={null}
aws lambda update-function-code \
  --function-name my-node-app \
  --zip-file fileb://my-node-app.zip \
  --publish
```

Or update from an S3 bucket:

```bash theme={null}
aws lambda update-function-code \
  --function-name my-node-app \
  --s3-bucket my-bucket \
  --s3-key my-node-app.zip
```

***

## 5. How can we retrieve the Function URL configuration via AWS CLI?

To fetch the function URL settings after deployment:

```bash theme={null}
aws lambda get-function-url-config \
  --function-name my-node-app
```

***

With these steps, you now have a clear roadmap:

* Integrate `serverless-http` into your Node.js app and export a Lambda handler.
* Zip your application code and dependencies.
* Use AWS CLI commands within a Jenkins pipeline to deploy and update your Lambda function.
* Retrieve and test the Function URL configuration with a simple CLI call.

In the next session, we’ll manually execute these commands to confirm the deployment before fully automating the workflow using our Jenkins pipeline.

## Links and References

* [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [serverless-http on npm](https://www.npmjs.com/package/serverless-http)
* [Serverless Framework Documentation](https://www.serverless.com/framework/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7e65cc00-b745-498e-8351-c294cbe958ec/lesson/a5f77f54-e283-4475-85c8-ebd291ace6b7)


# Automating Jenkins using CLI and APIs

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Automation-and-Security/Automating-Jenkins-using-CLI-and-APIs/page

Automating Jenkins tasks via CLI and REST API enhances efficiency and consistency in CI/CD pipelines, integrating seamlessly into automation workflows.

Automating Jenkins tasks via the CLI and REST API delivers repeatability, consistency, and efficiency to your CI/CD pipelines. While the web UI is great for manual interactions, scripting with the Jenkins CLI (SSH or JAR) and the REST API enables you to integrate Jenkins seamlessly into your automation workflows.

## Table of Contents

1. [Jenkins CLI over SSH](#jenkins-cli-over-ssh)\
   1.1 [Enable SSH Endpoint](#enable-ssh-endpoint)\
   1.2 [List Available Commands](#list-available-commands)\
   1.3 [Trigger a Job via SSH](#trigger-a-job-via-ssh)
2. [Jenkins CLI Client (jenkins-cli.jar)](#jenkins-cli-client-jenkins-clijar)
3. [Jenkins REST API](#jenkins-rest-api)\
   3.1 [Install a Plugin](#install-a-plugin)\
   3.2 [Authentication Methods](#authentication-methods)
4. [References](#references)

***

## Jenkins CLI over SSH

Jenkins includes a built-in CLI accessible over SSH. This approach avoids additional HTTP calls and works even behind strict firewalls.

### Enable SSH Endpoint

By default, SSH is disabled. You can reveal the SSH endpoint with:

```bash theme={null}
curl -Lv https://JENKINS_URL/login 2>&1 | grep -i 'x-ssh-endpoint'
