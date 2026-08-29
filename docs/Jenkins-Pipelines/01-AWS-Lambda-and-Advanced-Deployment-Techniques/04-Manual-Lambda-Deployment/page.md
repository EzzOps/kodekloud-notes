# Manual Lambda Deployment

Source: https://notes.kodekloud.com/docs/Jenkins-Pipelines/AWS-Lambda-and-Advanced-Deployment-Techniques/Manual-Lambda-Deployment/page

Guide to manually package a Node.js Express app, upload ZIP to S3, and update an existing AWS Lambda function, including handler setup and testing via Function URL.

In this guide you'll manually deploy a Node.js Express application to AWS Lambda (Node.js 20.x). We will package the app, upload the ZIP to S3, and update an existing Lambda function. In a follow-up lesson we'll automate this with [Jenkins Pipelines](https://learn.kodekloud.com/user/courses/jenkins-pipelines).

Below are the AWS objects created for this deployment and their purposes.

|   Resource Type | Name / Identifier          | Purpose                                   |
| --------------: | -------------------------- | ----------------------------------------- |
|       S3 Bucket | solar-system-lambda-bucket | Store the deployment ZIP for Lambda       |
| Lambda Function | solar-system-function      | The existing function we will update      |
|    Function URL | (Lambda Function URL)      | Public endpoint to verify UI and behavior |

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the &#x22;General purpose buckets&#x22; list with two buckets: &#x22;solar-system-jenkins-reports-bucket&#x22; and &#x22;solar-system-lambda-bucket&#x22; in the US East (Ohio) us-east-2 region. The page shows creation dates, IAM Access Analyzer links, and controls like &#x22;Create bucket.&#x22;" />
</Frame>

We will create a ZIP archive of the minimal application artifacts, upload it to the S3 bucket above, and use `aws lambda update-function-code` to point the Lambda function to that S3 object. The Lambda function already exists; we will update it instead of creating a new function.

<Frame>
  <img alt="A screenshot of the AWS Lambda console showing a function's Code properties and Runtime settings, including package size (9.9 MB), SHA256 hash, and last modified timestamp. It lists the runtime as Node.js 20.x, handler app.handler, and architecture x86_64." />
</Frame>

Key Lambda details:

* Runtime: Node.js 20.x
* Handler: app.handler (project uses app.js)
* Current package size: \~10 MB

The packaged application contains server-side JavaScript plus static assets (HTML, CSS, images). Example static HTML snippet found in the repo:

```html theme={null}
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Solar System - Sidd</title>
    <link rel="icon" type="image/x-icon" href="https://gitlab.com/sidd-larth/solar-system/-/raw/main/images/favicon.ico">
    <style>
      #planetImage {
        background: url('https://gitlab.com/sidd-larth/solar-system/-/raw/main/images/solar-system.png');
        background-repeat: no-repeat;
        background-size: cover;
        position: static;
        animation: spin 20s linear infinite;
        width: 30vw;
      }
    </style>
  </head>
  <body>
  </body>
</html>
```

Important: the deployed Lambda currently has MongoDB credentials stored as plaintext environment variables.

<Frame>
  <img alt="A screenshot of the AWS Lambda console for a function named &#x22;solar-system-function,&#x22; open to the Configuration → Environment variables tab showing keys like MONGO_PASSWORD, MONGO_URI, and MONGO_USERNAME with their values. The page also shows navigation tabs, action buttons (Throttle, Copy ARN, Actions), and the left-side configuration menu." />
</Frame>

<Callout icon="warning">
  Do not store sensitive secrets in plain environment variables for production. Use a secrets manager and grant the Lambda execution role least privilege.
</Callout>

<Callout icon="lightbulb">
  For production deployments, avoid hardcoding sensitive values. Use [AWS Secrets Manager](https://docs.aws.amazon.[SECRET_REDACTED].html) or [AWS Systems Manager Parameter Store (SSM)](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) and grant the Lambda role least privilege to retrieve secrets.
</Callout>

The Lambda function is exposed with a Function URL (you can view and test this in the Lambda console).

<Frame>
  <img alt="A screenshot of the AWS Lambda console on the Configuration > Function URL tab, showing a public function URL with Auth type &#x22;NONE&#x22;, Invoke mode &#x22;BUFFERED&#x22;, and CORS settings. The left sidebar lists other configuration sections like Triggers, Permissions, and Environment variables." />
</Frame>

Preparing the local workspace and packaging the app

<Frame>
  <img alt="A dark-themed browser view of a code repository page (dasher-org/solar-system) showing the file list, recent commits, branches and repository stats. The page displays filenames like Dockerfile, app.js and README.md along with commit messages and timestamps." />
</Frame>

Project details and Node.js serverless setup:

* The app uses serverless-http to wrap an Express app for Lambda.
* The handler export should be: module.exports.handler = serverless(app)
* If running locally with app.listen, those lines must be commented/removed for Lambda.

Example package.json dependencies (serverless-http included):

```json theme={null}
{
  "nyc": {
    "check-coverage": true,
    "lines": 90
  },
  "dependencies": {
    "@babel/traverse": "^7.23.2",
    "cors": "^2.8.5",
    "express": "^4.18.2",
    "mocha-junit-reporter": "^2.2.1",
    "mongoose": "5.13.20",
    "nyc": "^15.1.0",
    "serverless-http": "^3.2.0"
  },
  "devDependencies": {
    "chai": "*",
    "chai-http": "*",
    "mocha": "*"
  }
}
```

Relevant excerpt from app.js showing serverless-http usage and MongoDB env var consumption:

```javascript theme={null}
const path = require('path');
const fs = require('fs');
const express = require('express');
const os = require('os');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');
const serverless = require('serverless-http');

const app = express();

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '/')));
app.use(cors());

mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
}, function(err) {
  if (err) {
    console.error('MongoDB connection error:', err);
  }
});

// If running locally, the app might have these lines:
// app.listen(3000, () => { console.log("Server successfully running on port - " + 3000); })
// module.exports = app;

// For Lambda we must export the serverless handler:
module.exports.handler = serverless(app);
```

Deployment checklist (high-level)

1. Clone the repository and install dependencies.
2. Apply any app changes to verify deployment (e.g., bump a visible version string).
3. Remove or comment local server start code (app.listen) and ensure the Lambda handler export is present.
4. Zip the minimal files required by Lambda (app files, package.json, index.html, node\_modules).
5. Upload the ZIP to S3.
6. Update the Lambda function using the S3 object via AWS CLI.
7. Retrieve and test the Function URL.

Recommended shell commands (run from a workspace/sandbox):

```bash theme={null}
