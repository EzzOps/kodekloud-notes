# Setup ECR

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodeBuild-and-ECR/Setup-ECR/page

Guides creating and using an AWS Elastic Container Registry repository and steps to authenticate, tag, and push Docker images from local machines or CI pipelines.

Welcome — in this lesson we create an Amazon ECR (Elastic Container Registry) repository and review how to prepare images for pushing from your local machine or a CI pipeline.

Before you begin, sign in to the AWS Management Console and confirm you are operating in the correct AWS region used by this lesson: `eu-central-1` (Frankfurt).

In the Console search bar, type "ECR" and select Elastic Container Registry. ECR provides Docker-compatible container image repositories hosted in AWS (similar to Docker Hub, but managed inside your AWS account).

1. Click Get started.
2. Choose the repository visibility. Most organization images should be kept private — leave the default Private repository.
3. Give the repository a name. In this lesson we use `cryptoproject`.
4. Leave the remaining settings at their defaults. (Enabling "Scan on push" is recommended for production images; see the warning below.)
5. Click Create repository.

<Frame>
  <img alt="The image shows the &#x22;Create repository&#x22; page on the Amazon Elastic Container Registry (ECR) console, displaying options for setting visibility, repository name, and image scan settings." />
</Frame>

Once the repository is created it appears in your account and will store all images for this application. Locate the repository URI in the repository details — this fully qualified endpoint is used to tag and push images. Example format:

`<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<REPOSITORY_NAME>`

For example: `012345678901.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject`

<Frame>
  <img alt="The image shows an AWS Elastic Container Registry (ECR) interface with a private repository named &#x22;cryptoproject&#x22; displayed. The repository details include its URI, creation date, and encryption type." />
</Frame>

Commands to authenticate Docker to ECR, tag a local image, and push it to your ECR repository. Replace the placeholders with values from your account:

```bash theme={null}
