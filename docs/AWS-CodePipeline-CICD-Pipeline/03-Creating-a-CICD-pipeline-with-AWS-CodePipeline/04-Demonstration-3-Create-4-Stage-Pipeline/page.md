# Create a working directory
mkdir -p ~/demo/MyDemoRepo
cd ~/demo/MyDemoRepo

# Clone via HTTPS
git clone https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MyDemoRepo .
ls
# (directory is currently empty)
```

***

## 3. Add the Sample Application

1. Download the sample app ZIP from the AWS tutorial and extract its contents.
2. You should see:

   ```text theme={null}
   MyDemoRepo/
   ├── appspec.yml
   ├── index.html
   ├── LICENSE.txt
   └── scripts/
       ├── install_dependencies
       ├── start_server
       └── stop_server
   ```

![The image shows a Windows File Explorer window open to the "SampleApp\_Linux" folder, displaying four selected items: "appspec," "index," "LICENSE," and "scripts."](https://kodekloud.com/kk-media/image/upload/v1752862691/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/windows-file-explorer-sampleapp-folder.jpg)

3. Add, commit, and push:

   ```bash theme={null}
   git add .
   git commit -m "Add initial sample application files"
   git push origin master
   ```

4. Verify the files in the AWS Console:

![The image shows an AWS CodeCommit repository interface named "MyDemoRepo" with files like "scripts," "appspec.yml," "index.html," and "LICENSE.txt" listed. The interface includes options for creating pull requests and cloning the repository URL.](https://kodekloud.com/kk-media/image/upload/v1752862693/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codecommit-mydemorepo-interface-3.jpg)

***

## 4. Create an IAM Role for EC2 (CodeDeploy Agent)

In the IAM console, go to **Roles** > **Create role**:

* **Trusted entity:** AWS service → EC2
* **Attach policies:**

  | Policy Name                   | Purpose                               |
  | ----------------------------- | ------------------------------------- |
  | AmazonEC2RoleforAWSCodeDeploy | Grants CodeDeploy agent permissions   |
  | AmazonSSMManagedInstanceCore  | Allows AWS Systems Manager operations |

![The image shows the AWS IAM Management Console with a list of permission policies related to CodeDeploy. A specific policy, "AmazonEC2RoleforAWSCodeDeploy," is selected.](https://kodekloud.com/kk-media/image/upload/v1752862694/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-iam-management-console-codedeploy-policies.jpg)

![The image shows the AWS IAM Management Console with a list of permission policies related to Amazon SSM. One policy, "AmazonSSMManagedInstanceCore," is selected.](https://kodekloud.com/kk-media/image/upload/v1752862695/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-iam-management-console-ssm-policies.jpg)

3. Name the role **EC2InstanceRole**.
4. Use this trust policy:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

After creation, you’ll see:

![The image shows the AWS Identity and Access Management (IAM) console, specifically the "Roles" section, listing various roles with their trusted entities and last activity details. A green notification bar indicates that a role named "Ec2InstanceRole" has been created.](https://kodekloud.com/kk-media/image/upload/v1752862696/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-iam-console-roles-ec2instancerole.jpg)

***

## 5. Launch an EC2 Instance

1. In the EC2 console (same region), choose **Launch Instance**.
2. Configure as follows:
   * **Name tag:** MyCodePipelineDemo
   * **AMI:** Amazon Linux 2 (Free Tier)
   * **Instance type:** t2.micro (Free Tier)
   * **Key pair:** Proceed without one (demo only)
   * **Network:** Enable auto-assign Public IP
   * **Security group:**
     * SSH (port 22) from My IP
     * HTTP (port 80) from My IP

![The image shows an AWS EC2 management console where a user is selecting an Amazon Machine Image (AMI) to launch an instance. The summary on the right details the instance configuration, including the software image, instance type, and storage.](https://kodekloud.com/kk-media/image/upload/v1752862698/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-ec2-console-select-ami-instance.jpg)

![The image shows an AWS EC2 management console where a user is configuring settings to launch an instance, including key pair, network settings, and instance summary details.](https://kodekloud.com/kk-media/image/upload/v1752862699/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-ec2-management-console-launch-instance.jpg)

![The image shows an AWS EC2 management console where a user is configuring security group rules and storage settings for launching an instance. The summary section on the right provides details about the instance type, software image, and storage volume.](https://kodekloud.com/kk-media/image/upload/v1752862700/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-ec2-instance-launch-configuration.jpg)

![The image shows an AWS EC2 management console where a user is configuring security group rules and storage settings for launching an instance. The summary section on the right provides details about the instance type, software image, and storage volume.](https://kodekloud.com/kk-media/image/upload/v1752862701/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-ec2-security-group-settings-console.jpg)

Under **Advanced details**, assign the **EC2InstanceRole** profile and click **Launch instances**.

![The image shows an AWS EC2 management console with a success message indicating the initiation of an instance launch. It also displays next steps for managing the instance, such as connecting to it or setting up billing alerts.](https://kodekloud.com/kk-media/image/upload/v1752862702/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-ec2-management-console-instance-launch.jpg)

***

## 6. Create a CodeDeploy Application & Deployment Group

### 6.1 Service Role for CodeDeploy

In IAM, choose **Roles** > **Create role**:

* **Trusted entity:** AWS service → CodeDeploy
* **Managed policy:** AWSCodeDeployRole
* **Role name:** CodeDeployRole

Use this trust policy:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "codedeploy.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

![The image shows the AWS Identity and Access Management (IAM) console, specifically the "Roles" section, listing various roles with their trusted entities and last activity dates. A notification at the top indicates that a role named "CodeDeployRole2" has been created.](https://kodekloud.com/kk-media/image/upload/v1752862704/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-iam-console-roles-notification.jpg)

### 6.2 Application & Deployment Group

1. Open **CodeDeploy** > **Applications** > **Create application**:
   * **Name:** MyDemoApplication
   * **Compute platform:** EC2/On-premises

![The image shows the AWS CodeDeploy interface for creating a new application, with fields for application name, compute platform, and tags. The "Create application" button is highlighted.](https://kodekloud.com/kk-media/image/upload/v1752862705/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codedeploy-create-application-interface.jpg)

2. Under **Deployment groups**, click **Create deployment group**:
   * **Name:** MyDemoDeploymentGroup
   * **Service role:** CodeDeployRole
   * **Deployment type:** In-place
   * **Environment configuration:** Tag instances `Name = MyCodePipelineDemo`
   * **Load balancing:** Disabled
   * **Agent configuration:** AWS Systems Manager

![The image shows an AWS CodeDeploy interface where a user is creating a deployment group for an application named "MyDemoApplication." The deployment group name is set as "MyDemoDeploymentGroup."](https://kodekloud.com/kk-media/image/upload/v1752862706/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codedeploy-my-demo-deployment-group.jpg)

![The image shows an AWS CodeDeploy configuration screen where Amazon EC2 instances are being tagged for deployment. It includes options for adding tag groups and configuring the AWS Systems Manager agent.](https://kodekloud.com/kk-media/image/upload/v1752862707/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codedeploy-ec2-tagging-configuration.jpg)

When complete, review details:

![The image shows an AWS CodeDeploy interface with details of a deployment group named "MyDemoDeploymentGroup." It includes information about the application, deployment type, and environment configuration for Amazon EC2 instances.](https://kodekloud.com/kk-media/image/upload/v1752862708/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codedeploy-mydemodeploymentgroup.jpg)

***

## 7. Create the CodePipeline

In **CodePipeline**, click **Create pipeline** and configure:

1. **Pipeline name:** MyFirstPipeline
2. **Service role:** New service role

![The image shows the AWS CodePipeline setup screen where a user is configuring pipeline settings, including naming the pipeline "MyFirstPipeline" and selecting a new service role.](https://kodekloud.com/kk-media/image/upload/v1752862709/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codepipeline-setup-myfirstpipeline.jpg)

### Source Stage

* **Provider:** AWS CodeCommit
* **Repository name:** MyDemoRepo
* **Branch name:** master

![The image shows a screenshot of the AWS CodePipeline setup interface, where a user is configuring a source provider and repository settings. Options for change detection and output artifact format are also visible.](https://kodekloud.com/kk-media/image/upload/v1752862710/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codepipeline-setup-screenshot.jpg)

### Skip Build

Choose **Skip build stage**.

### Deploy Stage

* **Action provider:** AWS CodeDeploy
* **Region:** US West (Oregon)
* **Application name:** MyDemoApplication
* **Deployment group:** MyDemoDeploymentGroup

![The image shows an AWS CodePipeline interface where a user is configuring a deployment stage using AWS CodeDeploy, selecting the region "US West (Oregon)" and specifying an application name.](https://kodekloud.com/kk-media/image/upload/v1752862711/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codepipeline-deployment-config-us-west.jpg)

Review and click **Create pipeline**. The pipeline will start automatically:

![The image shows an AWS CodePipeline interface with a pipeline named "MyFirstPipeline" that is currently in progress. The interface includes options for creating and managing pipelines.](https://kodekloud.com/kk-media/image/upload/v1752862712/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codepipeline-myfirstpipeline-progress.jpg)

***

## 8. Verify the Initial Deployment

Once **Source** and **Deploy** stages complete, get the Public IPv4 DNS of your EC2 instance:

![The image shows an AWS EC2 Management Console with details of a running instance, including its instance ID, public IPv4 address, and status.](https://kodekloud.com/kk-media/image/upload/v1752862713/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-ec2-management-console-instance-details.jpg)

Paste the address into your browser to see the welcome page:

![The image shows a web page with a blue background displaying a "Congratulations" message, indicating that an application was deployed using AWS CodeDeploy. It also provides a link to the AWS CodeDeploy documentation for further steps.](https://kodekloud.com/kk-media/image/upload/v1752862714/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codedeploy-congratulations-message.jpg)

***

## 9. Update the Application and Redeploy

1. Modify `index.html` locally. Example update:

   ```html theme={null}
   <!DOCTYPE html>
   <html>
   <head>
     <title>Updated Sample Deployment</title>
     <style>
       body { background-color: #CCFFCC; font-family: Arial, sans-serif; }
       h1 { font-size: 250%; margin-bottom: 0; }
       h2 { font-size: 175%; margin-bottom: 0; }
     </style>
   </head>
   <body>
     <div align="center"><h1>Updated Sample Deployment</h1></div>
     <div align="center"><h2>Deployed via CodePipeline, CodeCommit & CodeDeploy.</h2></div>
     <div align="center">
       <p>Learn more:</p>
       <p><a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/">CodePipeline User Guide</a></p>
       <p><a href="https://docs.aws.amazon.com/codecommit/latest/userguide/">CodeCommit User Guide</a></p>
       <p><a href="https://docs.aws.amazon.com/codedeploy/latest/userguide/">CodeDeploy User Guide</a></p>
     </div>
   </body>
   </html>
   ```

2. Commit and push:

   ```bash theme={null}
   git add index.html
   git commit -m "Update index.html for new deployment"
   git push origin master
   ```

The pipeline auto-triggers and redeploys:

![The image shows an AWS CodePipeline interface with a pipeline execution in progress. The "Source" stage has succeeded, and the "Deploy" stage is currently in progress.](https://kodekloud.com/kk-media/image/upload/v1752862716/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/aws-codepipeline-execution-source-deploy.jpg)

After deployment, refresh to view changes:

![The image shows a webpage titled "Updated Sample Deployment" with a message about using CodePipeline, CodeCommit, and CodeDeploy, along with links to user guides.](https://kodekloud.com/kk-media/image/upload/v1752862717/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-2-Create-2-Stage-Pipeline/updated-sample-deployment-codepipeline-guides.jpg)

***

## Conclusion

You’ve successfully created and tested a two-stage AWS CodePipeline using CodeCommit and CodeDeploy. In this lesson you:

* Set up and cloned a CodeCommit repository
* Added a sample web application
* Configured IAM roles for EC2 and CodeDeploy
* Launched an EC2 instance with the CodeDeploy agent
* Defined a CodeDeploy application and deployment group
* Built a Source → Deploy pipeline
* Verified initial deployment and automated updates

Up next: we’ll extend this pipeline with build and test stages for a complete four-stage CI/CD workflow.

***

## References

* [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)
* [AWS CodeCommit User Guide](https://docs.aws.amazon.com/codecommit/latest/userguide/)
* [AWS CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline/module/d0ecdc6d-aba5-4798-80c9-171edb45c9dc/lesson/dbfb753d-ea36-4927-8792-06eeb99fd2db)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline/module/d0ecdc6d-aba5-4798-80c9-171edb45c9dc/lesson/7fb38ae9-3f5e-445f-bd67-0d61501b113f)


# Demonstration 3 Create 4 Stage Pipeline

Source: https://notes.kodekloud.com/docs/AWS-CodePipeline-CICD-Pipeline/Creating-a-CICD-pipeline-with-AWS-CodePipeline/Demonstration-3-Create-4-Stage-Pipeline/page

Build a complete AWS CodePipeline CI/CD workflow with four stages  Source, Build, Test, and Deploy using AWS services for consistent deployments and faster delivery cycles.

In this walkthrough, you will build a complete AWS CodePipeline CI/CD workflow with four stages—Source, Build, Test, and Deploy—using AWS CodeCommit, CodeBuild, CodeDeploy, and EC2. Automating these steps ensures consistent, repeatable deployments and faster delivery cycles.

## Pipeline Overview

| Stage  | AWS Service | Purpose                                 |
| ------ | ----------- | --------------------------------------- |
| Source | CodeCommit  | Store application code and scripts      |
| Build  | CodeBuild   | Install dependencies and compile assets |
| Test   | CodeBuild   | Run automated tests                     |
| Deploy | CodeDeploy  | Deploy artifacts to EC2 instances       |

***

## 1. Source Stage with CodeCommit

1. Open the [AWS CodeCommit console](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html) and create a new repository named `kodekloudcpdemo`.

![The image shows the AWS CodeCommit console with an empty repositories list. The interface includes options to create, clone, and manage repositories.](https://kodekloud.com/kk-media/image/upload/v1752862718/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codecommit-console-empty-repositories.jpg)

2. Enter **Repository name** as `kodekloudcpdemo` and click **Create**.

![The image shows the AWS CodeCommit interface for creating a new repository, with fields for repository name, description, and optional settings.](https://kodekloud.com/kk-media/image/upload/v1752862719/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codecommit-new-repository-interface.jpg)

3. Clone the repo locally:

```bash theme={null}
git clone https://git-codecommit.us-east-2.amazonaws.com/v1/repos/KodeKloudCPDemo
```

4. Back in the console, click **Upload file** to add your application files (`after_install`, `application_start`, `appspec.yml`, etc.). For each file, provide an author name and email, then commit.

![The image shows a file explorer window open on a computer, displaying a list of files in a directory. In the background, there is a web page related to AWS CodeCommit with fields for committing changes.](https://kodekloud.com/kk-media/image/upload/v1752862721/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/file-explorer-aws-codecommit-window.jpg)

5. After each commit, you’ll see a success notification:

![The image shows an AWS CodeCommit interface with a repository named "KodeKloudCPDemo" and a file named "after\_install" committed to the main branch. A notification indicates a successful commit.](https://kodekloud.com/kk-media/image/upload/v1752862722/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codecommit-kodekloudcpdemo-commit.jpg)

6. When all nine files are uploaded, your repo should list them as shown:

![The image shows an AWS CodeCommit repository interface named "KodeKloudCPDemo" with a list of files such as after\_install, application\_start, and appspec.yml.](https://kodekloud.com/kk-media/image/upload/v1752862723/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codecommit-repository-kodekloudcpdemo.jpg)

***

## 2. Build Stage with CodeBuild

1. Navigate to the [AWS CodeBuild console](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html) and click **Create build project**.

![The image shows the AWS CodeBuild interface with no build projects listed. There is an option to create a new build project.](https://kodekloud.com/kk-media/image/upload/v1752862724/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codebuild-interface-no-projects.jpg)

2. Set **Project name** to `KodeKloudCPdemo`.

![The image shows the AWS CodeBuild interface for creating a new build project, with fields for project configuration such as project name and description.](https://kodekloud.com/kk-media/image/upload/v1752862725/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codebuild-new-project-interface.jpg)

3. Under **Source**, select **AWS CodeCommit**, choose `kodekloudcpdemo`, and branch `main`.

![The image shows an AWS CodeBuild configuration screen where the source provider is set to AWS CodeCommit, with a repository named "KodeKloudCPDemo" and the branch "main" selected.](https://kodekloud.com/kk-media/image/upload/v1752862726/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codebuild-codecommit-kodekloudcpdemo.jpg)

4. In **Environment**, pick:
   * Operating system: **Linux**
   * Runtime: **Standard**
   * Image: **aws/codebuild/standard:2.0**

5. Keep service role and log settings at their defaults, then click **Create build project**.

![The image shows an AWS CodeBuild interface for configuring logs, with options for CloudWatch and S3 logs.](https://kodekloud.com/kk-media/image/upload/v1752862727/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codebuild-logs-configuration-interface.jpg)

6. Confirm your project is ready:

![The image shows an AWS CodeBuild project interface for "KodeKloudCPDemo," displaying configuration details and options to start or manage builds. A green notification bar indicates the project was successfully created.](https://kodekloud.com/kk-media/image/upload/v1752862728/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codebuild-kodekloudcpdemo-interface.jpg)

> **triangle-alert** The default `buildspec.yml` uses Node.js 14, but your app requires Node.js 10. Update the `runtime-versions` accordingly to avoid build failures.

### Adjusting the Buildspec

Open `buildspec.yml` in your CodeCommit repo. Change Node.js version from 14 to 10:

```yaml theme={null}
version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: 10
    commands:
      - echo "Installing dependencies"
      - npm install
  build:
    commands:
      - echo "Building the application"
      - npm run build
artifacts:
  files:
    - '**/*'
```

Commit your changes with author metadata.

***

## 3. Prepare EC2 Instances for CodeDeploy

1. In the [EC2 console](https://docs.aws.amazon.com/ec2/index.html), click **Launch Instance**.
2. Name the instance `CodePipelineCPdemo` and choose an Ubuntu AMI.
3. Select or create a key pair.
4. Open HTTP (port 80) and HTTPS (port 443) in the security group.
5. Enable **Auto-assign Public IP**.
6. Under **Advanced Details**, attach an IAM instance profile with CodeDeploy permissions.
7. Click **Launch Instance**.

![The image shows an AWS EC2 instance launch configuration screen, where a user is selecting an Amazon Machine Image (AMI) and configuring instance details like the server type and security group.](https://kodekloud.com/kk-media/image/upload/v1752862729/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-ec2-instance-launch-configuration.jpg)

Review network settings and instance summary:

![The image shows an AWS EC2 instance launch configuration screen, detailing network settings and a summary of the instance specifications.](https://kodekloud.com/kk-media/image/upload/v1752862730/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-ec2-instance-launch-configuration-2.jpg)

Select the IAM role:

![The image shows an AWS EC2 instance launch configuration page, detailing options like purchasing, domain join directory, IAM instance profile, and a summary of the instance settings.](https://kodekloud.com/kk-media/image/upload/v1752862731/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-ec2-instance-launch-configuration-3.jpg)

Verify the instance is running before proceeding to CodeDeploy.

> **lightbulb** Ensure the IAM instance profile has `AmazonEC2RoleforAWSCodeDeploy` permissions so the CodeDeploy agent can communicate with AWS.

***

## 4. Deploy Stage with CodeDeploy

1. Go to the [AWS CodeDeploy console](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html) and click **Create application**.
2. Name it `KodeKloudCPdemo` and choose **EC2/On-premises** as the compute platform.

![The image shows an AWS CodeDeploy application interface for "KodeKloudCPDemo," with options to create a deployment group and manage application details. The interface includes navigation for various developer tools and deployment settings.](https://kodekloud.com/kk-media/image/upload/v1752862732/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codedeploy-kodekloudcpdemo-interface.jpg)

3. Create a deployment group:
   * Name: **KodeKloudCPdemo**
   * Service role: **CodeDeployDefault** (or your custom role)
   * Uncheck load balancer integration.
   * Environment: **EC2/On-premises**
   * Tag key/value matching your EC2 instance (`Name=CodePipelineCPdemo`).

![The image shows an AWS CodeDeploy setup page where a deployment group name is being entered, along with options for selecting a service role and deployment type.](https://kodekloud.com/kk-media/image/upload/v1752862733/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codedeploy-setup-deployment-group.jpg)

4. Select the EC2 instance by tag:

![The image shows an AWS CodeDeploy interface where a user is selecting Amazon EC2 instances for deployment, with a dropdown menu listing various instance options.](https://kodekloud.com/kk-media/image/upload/v1752862734/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codedeploy-ec2-instances-selection.jpg)

5. (Optional) Install or verify the CodeDeploy agent via Systems Manager, then click **Create deployment group**.

![The image shows an AWS CodeDeploy configuration screen with options for tagging and agent configuration using AWS Systems Manager. It includes settings for installing the CodeDeploy Agent.](https://kodekloud.com/kk-media/image/upload/v1752862735/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codedeploy-configuration-screen.jpg)

***

## 5. Create the Four-Stage Pipeline

1. Open the [AWS CodePipeline console](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html) and click **Create pipeline**.
2. Name it `KodeKloudCPdemo` and use the default service role.

![The image shows an AWS CodePipeline setup screen where a user is configuring pipeline settings, including the pipeline name and service role options.](https://kodekloud.com/kk-media/image/upload/v1752862737/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codepipeline-setup-screen-configure.jpg)

### Source Stage

* Provider: **AWS CodeCommit**
* Repository: `kodekloudcpdemo`
* Branch: `main`

![The image shows an AWS CodePipeline interface where a user is adding a source stage, selecting AWS CodeCommit as the source provider, and specifying repository and branch details.](https://kodekloud.com/kk-media/image/upload/v1752862738/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codepipeline-source-stage-codecommit.jpg)

### Build Stage

* Provider: **AWS CodeBuild**
* Project name: `KodeKloudCPdemo`

<Frame>
  <img alt="The image shows an AWS CodeBuild project interface with build project details and an option to start builds indicating the project was successfully created." />
</Frame>

### Deploy Stage

* Provider: **AWS CodeDeploy**
* Region: *your AWS Region*
* Application: `KodeKloudCPdemo`
* Deployment group: `KodeKloudCPdemo`

![The image shows an AWS CodePipeline interface where a user is adding a deploy stage, selecting AWS CodeDeploy as the provider, and specifying the region, application name, and deployment group.](https://kodekloud.com/kk-media/image/upload/v1752862739/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codepipeline-deploy-stage-codedeploy.jpg)

Click **Create pipeline**. The pipeline initializes and starts its first run:

![The image shows an AWS CodePipeline interface with a successful pipeline creation message for "KodeKloudCPDemo." It displays the status of the source and build stages, with the source stage marked as succeeded.](https://kodekloud.com/kk-media/image/upload/v1752862740/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codepipeline-kodekloudcpdemo-success.jpg)

***

## 6. Adding the Test Stage

Once the initial pipeline run succeeds, insert a **Test** stage between Build and Deploy:

1. Click **Edit** in the pipeline view.
2. Under the Build stage, click **Add stage**, name it **Test**, then **Add stage**.

![The image shows an AWS CodePipeline interface with successful build and deploy stages. The pipeline execution details indicate recent success in both stages.](https://kodekloud.com/kk-media/image/upload/v1752862741/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codepipeline-success-build-deploy.jpg)

3. Inside **Test**, click **Add action group** and configure:
   * Action name: `TestAction`
   * Provider: **AWS CodeBuild**
   * Input artifact: `BuildArtifact`
   * Project name: `KodeKloudCPdemo`

![The image shows an AWS CodePipeline interface where a user is editing an action, selecting AWS CodeBuild as the action provider, and specifying input artifacts and environment variables.](https://kodekloud.com/kk-media/image/upload/v1752862742/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Demonstration-3-Create-4-Stage-Pipeline/aws-codepipeline-codebuild-action-edit.jpg)

4. Save changes and click **Release change**. The pipeline will now run all four stages in sequence, ending with a green success status across Source, Build, Test, and Deploy.

***

## Summary

You have successfully built an automated four-stage CI/CD pipeline on AWS:

1. **Source**: CodeCommit
2. **Build**: CodeBuild
3. **Test**: CodeBuild
4. **Deploy**: CodeDeploy

Use this template to accelerate your deployments and enforce consistent delivery practices.

***

## Links and References

* [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [AWS CodeCommit Documentation](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)
* [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [AWS CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)
* [EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline/module/d0ecdc6d-aba5-4798-80c9-171edb45c9dc/lesson/89aad9e4-558b-4865-ad10-133ee3a6454d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline/module/d0ecdc6d-aba5-4798-80c9-171edb45c9dc/lesson/4ebbcb9e-e655-4977-a97f-4c2f4ccf920c)
