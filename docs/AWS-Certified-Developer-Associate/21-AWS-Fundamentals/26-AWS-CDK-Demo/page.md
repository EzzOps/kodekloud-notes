# AWS CDK Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/AWS-Fundamentals/AWS-CDK-Demo/page

Learn to use AWS CDK for creating and managing AWS resources, including S3 bucket infrastructure, through installation, project initialization, deployment, and cleanup.

In this guide, you'll learn how to use the AWS Cloud Development Kit (CDK) to create and manage AWS resources. We'll cover installing prerequisites, initializing a CDK project, exploring generated files, and then deploying, verifying, and cleaning up a simple S3 bucket infrastructure.

***

## Prerequisites

Before you begin with AWS CDK, ensure that [Node.js](https://nodejs.org/) is installed on your machine. Node.js comes with NPM (Node Package Manager), which is required to install the AWS CDK CLI tool.

After installing Node.js, run these commands to install and verify the AWS CDK CLI:

```bash theme={null}
aws sts get-caller-identity
```

```bash theme={null}
npm install -g aws-cdk
```

```bash theme={null}
cdk --version
```

Ensure Node.js is installed correctly by referring to the [Node.js documentation](https://nodejs.org/en/docs/). The site usually detects your operating system and provides the appropriate download options.

![The image shows the Node.js download page, offering options to download the LTS and Current versions for Windows (x64). It also mentions available security releases.](https://kodekloud.com/kk-media/image/upload/v1752858090/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/nodejs-download-page-lts-current.jpg)

***

## Installing the AWS CDK CLI

Once Node.js and NPM are installed, you can install the AWS CDK CLI with:

```bash theme={null}
npm install -g aws-cdk
```

Then, verify your installation by running:

```bash theme={null}
cdk --help
```

You should see a list of available commands such as:

* `cdk list` (or `cdk ls`): List all stacks in the app.
* `cdk synth` (or `cdk synthesize`): Generate the CloudFormation template.
* `cdk bootstrap`: Deploy the CDK toolkit stack into your AWS environment.
* `cdk deploy`: Deploy your stack(s) to your AWS account.
* `cdk destroy`: Remove the deployed stack(s).
* `cdk diff`: Compare your local template with the deployed stack.

***

## Initializing a New CDK Project

To quickly get started with a new project, initialize a boilerplate application with:

```bash theme={null}
cdk init app --language python
```

If you prefer a sample project template that includes a demo application, you can run:

```bash theme={null}
cdk init sample-app --language python
```

This command creates multiple files and directories to jumpstart your CDK project:

* **Python Virtual Environment:** Isolates project dependencies.
* **Activation Script:** A file like `source.bash` (or equivalent for Mac/Linux) to activate the virtual environment.
* **requirements.txt:** Lists third-party dependencies (typically including `aws-cdk-lib` and `constructs`).

Example `requirements.txt` content:

```text theme={null}
aws-cdk-lib==2.101.0
constructs>=10.0.0,<11.0.0
```

* **README:** Contains instructions for installing dependencies and running commands:

```bash theme={null}
python -m venv .venv
cdk synth
pytest
```

* **cdk.json:** Contains project configuration. For example:

```json theme={null}
{
  "app": "python app.py",
  "watch": {
    "include": [
      "**"
    ],
    "exclude": [
      "README.md",
      "cdk*.json",
      "requirements*.txt",
      "source.bat",
      "**/__init__.py",
      "python/__pycache__",
      "tests"
    ]
  },
  "context": {
    "@aws-cdk/aws-lambda:recognizeLayerVersion": true,
    "@aws-cdk/core:checkSecretUsage": true,
    "@aws-cdk/core:target-partitions": [
      "aws",
      "aws-cn"
    ]
  }
}
```

* **app.py:** Initializes your CDK application and instantiates a stack:

```python theme={null}
#!/usr/bin/env python3

import aws_cdk as cdk
from cdk.cdk_stack import CdkStack

app = cdk.App()
CdkStack(app, "CdkStack")
app.synth()
```

* **Stack File (e.g., `cdk/cdk_stack.py`):** Initially defines resources like an SQS queue and an SNS topic with a subscription:

```python theme={null}
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        queue = sqs.Queue(
            self, "CdkQueue",
            visibility_timeout=Duration.seconds(300),
        )
        
        topic = sns.Topic(
            self, "CdkTopic"
        )
        
        topic.add_subscription(subs.SqsSubscription(queue))
```

> **lightbulb** In this demo, we will comment out the SQS/SNS implementation to focus on creating an S3 bucket.

***

## Configuring the Python Virtual Environment

Set up your Python virtual environment and install the necessary packages:

1. **Create and Activate the Virtual Environment:**

   ```bash theme={null}
   python -m venv .venv
   ```

   On Windows, activate with:

   ```bat theme={null}
   .venv\Scripts\activate.bat
   ```

   On Mac/Linux, use:

   ```bash theme={null}
   source .venv/bin/activate
   ```

2. **Install Dependencies:**

   ```bash theme={null}
   pip install -r requirements.txt
   ```

Once these steps are completed, you're ready to work on your CDK project.

***

## Editing the CDK Stack for an S3 Bucket

For this demo, we'll modify the CDK stack to create an S3 bucket. First, update the import statements to include AWS S3 (and optionally AWS KMS if you need encryption):

```python theme={null}
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
