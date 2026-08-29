# Demonstration 2 Create 2 Stage Pipeline

Source: https://notes.kodekloud.com/docs/AWS-CodePipeline-CICD-Pipeline/Creating-a-CICD-pipeline-with-AWS-CodePipeline/Demonstration-2-Create-2-Stage-Pipeline/page

Set up a two-stage CI/CD pipeline on AWS using CodeCommit for source control and CodeDeploy for deployment of a sample web application.

In this guide, you’ll set up a simple two-stage CI/CD pipeline on AWS using CodeCommit for source control and CodeDeploy for deployment. We’ll deploy a sample web application to an EC2 instance following the [AWS CodePipeline simple tutorial](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-simple-codepipeline.html).

![The image shows a demonstration slide with an infinity loop labeled "Source" and "Deploy," alongside an AWS CodeCommit icon.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862686/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/infinity-loop-source-deploy-aws-codecommit.jpg)

![The image contains a URL link to an AWS CodePipeline tutorial page. It also includes a copyright notice for KodeKloud.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862686/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codepipeline-tutorial-kodekloud.jpg)

***

## 1. Create a CodeCommit Repository

1. Sign in to the AWS Management Console and open **CodeCommit**.
2. Ensure your region is set (we’re using **us-west-2**).

> **lightbulb** Always match the region across CodeCommit, CodeDeploy, and EC2 to avoid cross-region issues.

3. Click **Create repository**, name it **MyDemoRepo**, and confirm.

![The image shows the AWS Management Console home page, displaying recently visited services and a welcome section with links to getting started, training, and new features.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862688/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-management-console-home-page.jpg)

![The image shows the AWS CodeCommit interface for creating a new repository, with fields for repository name, description, and optional settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862689/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codecommit-new-repository-interface.jpg)

Once the repo is ready, note the clone instructions:

![The image shows an AWS CodeCommit interface with a repository named "MyDemoRepo" successfully created. It displays connection steps and prerequisites for accessing the repository.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862690/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codecommit-mydemorepo-interface.jpg)

***

## 2. Clone the Repository Locally

On your laptop or workstation:

```bash theme={null}
