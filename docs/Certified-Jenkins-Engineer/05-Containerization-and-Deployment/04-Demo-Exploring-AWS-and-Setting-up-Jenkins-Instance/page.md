# Demo Exploring AWS and Setting up Jenkins Instance

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Containerization-and-Deployment/Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/page

This article covers setting up a Jenkins deployment instance using AWS services, including configuring IAM and SSH credentials for automated deployments.

In this lesson, we begin the deployment phase of our CI/CD pipeline using AWS services—EC2, S3, and Lambda. You’ll see how to prepare your AWS environment, install necessary Jenkins plugins, and configure both AWS and SSH credentials to automate deployments.

## Reviewing the EC2 Instance

Navigate to the EC2 Instances dashboard in the AWS Console. You should see a single instance named **dev-deploy** in the **running** state.

<Frame>
  ![The image shows an AWS EC2 console with details of a running instance named "dev-deploy," including its instance ID, public and private IP addresses, and instance type (t2.micro).](../../../../images/kodekloud.com/kk-media/image/upload/v1752870503/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/aws-ec2-console-dev-deploy-instance.jpg)
</Frame>

This VM already has Docker installed. To verify, SSH into the instance and run:

```bash theme={null}
sudo docker ps
```

```text theme={null}
CONTAINER ID   IMAGE                                                   NAMES
f0f9299ee8fe   siddharth67/solar-system:7d1e24920bd455706b179c6724d5566d797634   solar-system
0.0.0.0:3000->3000/tcp
```

We’ll use this EC2 host to deploy our feature-branch Docker images.

## Setting Up AWS IAM Credentials

Create an IAM user (`jenkins-user`) with full access to EC2, S3, and Lambda. Attach these managed policies:

| Policy Name           | Service | Access Level |
| --------------------- | ------- | ------------ |
| AmazonEC2FullAccess   | EC2     | Full         |
| AmazonS3FullAccess    | S3      | Full         |
| AWSLambda\_FullAccess | Lambda  | Full         |

<Frame>
  ![The image shows an AWS Identity and Access Management (IAM) console screen, displaying user details and permissions policies for a user named "jenkins-user," with policies like AmazonEC2FullAccess, AmazonS3FullAccess, and AWSLambda\_FullAccess attached.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870504/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/aws-iam-console-jenkins-user-policies.jpg)
</Frame>

Once created, AWS will display the **Access Key ID** and **Secret Access Key**.

<Frame>
  ![The image shows an AWS Identity and Access Management (IAM) console, specifically the security credentials section for a user, displaying details like console sign-in, multi-factor authentication, and access keys.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870505/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/aws-iam-console-security-credentials.jpg)
</Frame>

<Callout icon="triangle-alert">
  Keep your **Access Key ID** and **Secret Access Key** safe—do not commit them to source control.
</Callout>

Finally, review your user details to confirm MFA and key status:

<Frame>
  ![The image shows an AWS Identity and Access Management (IAM) console page, displaying details for a user, including multi-factor authentication settings and an active access key.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870506/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/aws-iam-console-user-details.jpg)
</Frame>

## Installing the AWS Steps Plugin in Jenkins

To enable AWS API calls in your pipelines, install the **Pipeline: AWS Steps** plugin:

1. In Jenkins, go to **Manage Jenkins** → **Manage Plugins** → **Available**.
2. Search for **Pipeline: AWS Steps**, select it, and click **Install without restart**.
3. Restart Jenkins when prompted.

<Frame>
  ![The image shows a webpage from Jenkins, detailing features of a plugin that adds pipeline steps to interact with AWS's API. It includes a list of features and links to related resources.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870506/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/jenkins-plugin-aws-api-features.jpg)
</Frame>

Here are a few example steps you can use in your `Jenkinsfile`:

| Step              | Description                           | Example                                                             |
| ----------------- | ------------------------------------- | ------------------------------------------------------------------- |
| s3DoesObjectExist | Check if an object exists in a bucket | `exists = s3DoesObjectExist(bucket: 'my-bucket', path: 'file.txt')` |
| s3FindFiles       | List files in an S3 bucket            | `files = s3FindFiles(bucket: 'my-bucket', glob: 'path/to/*.ext')`   |

<Callout icon="lightbulb">
  After plugin installation, always restart Jenkins to load new pipeline steps.
</Callout>

## Configuring AWS Credentials in Jenkins

Next, store your IAM keys in Jenkins:

1. Go to **Manage Jenkins** → **Manage Credentials** → **(global)** → **Add Credentials**.
2. Select **Kind: AWS Credentials**.
3. Enter an **ID** (e.g., `aws-s3-ec2-lambda`), paste your **Access Key ID** and **Secret Access Key**, then save.

<Frame>
  ![The image shows a Jenkins interface where AWS credentials are being configured, including fields for an Access Key ID and a Secret Access Key.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870507/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/jenkins-aws-credentials-configuration.jpg)
</Frame>

Jenkins will validate these credentials automatically:

<Frame>
  ![The image shows a Jenkins interface displaying AWS credentials, including an Access Key ID and a concealed Secret Access Key, with a note about access to six availability zones.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870510/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/jenkins-aws-credentials-interface.jpg)
</Frame>

## Adding SSH Credentials for EC2

To deploy Docker images over SSH, install the **SSH Agent** plugin:

1. Go to **Manage Jenkins** → **Manage Plugins** → **Available**.
2. Search for **SSH Agent** and install.

Then add your EC2 key:

1. Navigate to **Manage Jenkins** → **Manage Credentials** → **(global)** → **Add Credentials**.
2. Choose **SSH Username with private key**.
3. Specify an **ID** (e.g., `aws-devops-deploy-ec2`), **Username** (`ubuntu`), and paste your private key.
4. Save.

<Frame>
  ![The image shows a Jenkins interface for adding new credentials, with a dropdown menu displaying options like "Username with password" and "SSH Username with private key."](../../../../images/kodekloud.com/kk-media/image/upload/v1752870511/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/jenkins-add-credentials-interface.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins interface for managing global credentials, specifically for adding an SSH username with a private key. The fields include ID, description, username, and options for entering a private key and passphrase.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870512/notes-assets/images/Certified-Jenkins-Engineer-Demo-Exploring-AWS-and-Setting-up-Jenkins-Instance/jenkins-global-credentials-ssh.jpg)
</Frame>

***

With AWS Steps and SSH Agent plugins installed, AWS IAM and SSH credentials configured, you’re ready to add a pipeline stage that connects to your EC2 instance and deploys Docker images.

## Links and References

* [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
* [Jenkins Plugin: Pipeline AWS Steps](https://plugins.jenkins.io/pipeline-aws/)
* [Jenkins Plugin: SSH Agent](https://plugins.jenkins.io/ssh-agent/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/e16e4b93-31c4-479b-96b8-f0d26cde31cd/lesson/136f41da-5da5-4057-ac72-4911deb3fe54" />
</CardGroup>
