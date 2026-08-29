# Lambda Containers Demonstration

Source: https://notes.kodekloud.com/docs/AWS-Lambda/Advanced-Topics/Lambda-Containers-Demonstration/page

This tutorial guides building, pushing, and deploying an AWS Lambda function packaged as a container image using the AWS Management Console.

In this tutorial, we’ll guide you through building, pushing, and deploying an AWS Lambda function packaged as a container image, using the AWS Management Console.

## Environment Setup

Before you begin, ensure you have the following:

* A local development workstation (Windows, macOS, or Linux)
* An IDE such as [Visual Studio Code](https://code.visualstudio.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
* The [AWS CLI](https://aws.amazon.com/cli/) configured with proper credentials
* An active AWS account logged into the [AWS Management Console](https://aws.amazon.com/console/)

![The image is a slide titled "Container Demo" showing the environment setup, including AWS CLI, Visual Studio Code, Docker Desktop, and AWS Console.](https://kodekloud.com/kk-media/image/upload/v1752863070/notes-assets/images/AWS-Lambda-Lambda-Containers-Demonstration/container-demo-environment-setup-aws-docker.jpg)

## Project Structure

Create a new directory for your demo and add the following files:

| File             | Purpose                      |
| ---------------- | ---------------------------- |
| app.py           | Python Lambda handler        |
| requirements.txt | Python dependencies          |
| Dockerfile       | Container build instructions |

![The image shows a Visual Studio Code interface with a project directory open, displaying files such as app.py, Dockerfile, and an open requirements.txt file. The terminal at the bottom is set to a directory path.](https://kodekloud.com/kk-media/image/upload/v1752863071/notes-assets/images/AWS-Lambda-Lambda-Containers-Demonstration/visual-studio-code-project-directory-files.jpg)

### app.py

```python theme={null}
import sys

def handler(event, context):
    return 'Hello from KodeKloud with AWS Lambda using Python ' + sys.version + '!'
```

### requirements.txt

Leave this file empty for no external dependencies, or list any libraries your function needs.

> **lightbulb** If you require additional packages, add them to `requirements.txt` before building the image.

### Dockerfile

```dockerfile theme={null}
FROM public.ecr.aws/lambda/python:3.8
