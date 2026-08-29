# Cloud9

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/AWS-CICD-Developer-Tools/Cloud9/page

Cloud9 is a cloud-based IDE that enables coding, collaboration, and deployment of applications directly from a web browser.

Cloud9 is a powerful cloud-based Integrated Development Environment (IDE) that enables developers to code, collaborate, and deploy applications directly from a web browser. Hosted on AWS, Cloud9 eliminates the need for local software installations, making it easy to work from anywhere with internet access.

## Key Features of Cloud9

Cloud9 is packed with features designed to streamline your development workflow:

* **Preconfigured Environments:** Get started quickly with environments tailored for popular languages and frameworks including JavaScript, Python, PHP, Ruby, Go, C++, and more.
* **Real-Time Collaboration:** Work simultaneously with team members. Cloud9 provides individual cursors for each collaborator, enhancing pair programming, troubleshooting, and feature development.
* **Seamless AWS Integration:** Enjoy native integration with AWS services, such as EC2, S3, and Lambda. Cloud9 includes a built-in terminal with a full Unix Bash shell for running commands, installing software, executing tests, and managing AWS services.

## Example: Dockerfile for a Python Application

Below is an example Dockerfile that configures a simple Python application environment. This setup is similar to how you might prepare your project within Cloud9:

```dockerfile theme={null}
FROM python:3.12.0b3-alpine3.18
COPY . /application
WORKDIR /application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

## Managing Code and Deployments

Cloud9 simplifies the process of managing code changes and deployments. When you commit changes to repositories like GitHub or AWS CodeCommit, you can immediately trigger automated pipelines using AWS CodePipeline. These pipelines typically run tests with CodeBuild and deploy applications via CodeDeploy, ensuring a smooth continuous integration and delivery process.

<Callout icon="lightbulb">
  The console session below demonstrates how code changes are tracked and pushed effectively:
</Callout>

```bash theme={null}
bash "ip-172-371-78"
Counting objects: 24, done.
remote: Counting objects: 100% (24/24), done.
remote: Compressing objects: 100% (16/16), done.
Receiving objects: 100% (24/24), done.
Resolving deltas: 100% (3/3), done.
```

## Cloud9 Infrastructure Overview

Cloud9 runs on an Amazon EC2 instance within your VPC, ensuring a secure and scalable development environment. The following diagram displays the Cloud9 architecture as it appears within an AWS VPC:

<Frame>
  ![The image lists five features: cloud-based IDE, preconfigured development environments, real-time collaboration, seamless integration with AWS, and a built-in terminal.](../../../../images/kodekloud.com/kk-media/image/upload/v1752857923/notes-assets/images/AWS-Certified-Developer-Associate-Cloud9/cloud-ide-features-list.jpg)
</Frame>

The diagram below illustrates the setup of Cloud9 within an AWS VPC, where a secure web interface connects an EC2 instance to your browser:

<Frame>
  ![The image is a diagram showing a Cloud9 setup within an AWS VPC, including a subnet and an EC2 instance, connected to a developer.](../../../../images/kodekloud.com/kk-media/image/upload/v1752857924/notes-assets/images/AWS-Certified-Developer-Associate-Cloud9/cloud9-aws-vpc-diagram.jpg)
</Frame>

## Automated Deployment Workflow

When a code change is committed, it can trigger an automated pipeline involving AWS services such as CodeCommit, CodeBuild, and CodeDeploy. This workflow ensures that your application is deployed to your compute platform seamlessly.

<Frame>
  ![The image illustrates a workflow involving a developer using Cloud9, followed by AWS CodePipeline stages: CodeCommit, CodeBuild, CodeDeploy, and finally deploying to AWS EC2.](../../../../images/kodekloud.com/kk-media/image/upload/v1752857925/notes-assets/images/AWS-Certified-Developer-Associate-Cloud9/cloud9-aws-codepipeline-workflow.jpg)
</Frame>

## Environment Templates for Faster Setup

Cloud9 offers an extensive range of preconfigured environment templates. Whether you require a simple Python setup or an advanced environment like an API server using Express in Node.js, Cloud9 provides templates to help you get started swiftly. You can even customize and save your own templates for future projects.

<Frame>
  ![The image shows a selection of templates for Cloud9 environments, featuring various programming languages and application types, all utilizing AWS Lambda for serverless execution.](../../../../images/kodekloud.com/kk-media/image/upload/v1752857926/notes-assets/images/AWS-Certified-Developer-Associate-Cloud9/cloud9-templates-aws-lambda.jpg)
</Frame>

<Callout icon="lightbulb">
  Cloud9 is a robust, cloud-based IDE that allows you to develop code, collaborate in real time, and integrate effortlessly with AWS services. With its preconfigured templates and seamless integration with AWS pipelines, Cloud9 is an ideal choice for modern cloud-based development practices.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/184641b0-93ba-48d1-a9d7-1bc2b57db724/lesson/5cdcf67c-776a-4c87-a4b9-57a947fd1e7a" />
</CardGroup>
