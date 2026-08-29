# Navigate to your repo folder (if not already there)
cd ~/environment/aws-microservice-project

# Check status, add and commit
git status
git add .
git commit -m "Add buildspec.yml"

# Push to the remote repository
git push origin master
```

Sample console output (illustrative):

```bash theme={null}
ec2-user@ip-172-31-x:~/environment/aws-microservice-project (master) $ git status
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   buildspec.yml

ec2-user@ip-172-31-x:~/environment/aws-microservice-project (master) $ git commit -m "Add buildspec.yml"
[master b12f6f2] Add buildspec.yml
 1 file changed, 20 insertions(+)
 create mode 100644 buildspec.yml

ec2-user@ip-172-31-x:~/environment/aws-microservice-project (master) $ git push origin master
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 75.00 KiB | 785.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/aws-microservice-project
   863f04d..b12f6f2  master -> master
```

Verify the commit in CodeCommit
Open the CodeCommit repository in the AWS Console and confirm that `buildspec.yml` appears in the repository root.

<Frame>
  <img alt="The image depicts an AWS CodeCommit interface showing a repository named &#x22;aws-microservice-project.&#x22; Various options and menus for developer tools are visible on the left sidebar." />
</Frame>

Next steps

* Create or configure a CodeBuild project (or CodePipeline) that points to this repository and has the `REPOSITORY_URI`, `AWS_ACCOUNT_ID`, and `AWS_DEFAULT_REGION` environment variables set.
* Make sure the build environment supports Docker and has privileged mode enabled.
* After a push, CodeBuild will run the `buildspec.yml` steps, build the Docker image, and push it to ECR.

Links and references

* [Amazon ECR Documentation](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* [AWS CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [AWS CLI - ecr get-login-password](https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login-password.html)
* [AWS CodeCommit User Guide](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)

That’s it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/37195f61-a068-4f6c-9ccc-0bd66b358449/lesson/7679f290-3995-4a32-aa9e-b09645f6da60" />
</CardGroup>


# Demo Work on Buildspecyaml file Part 02

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodeBuild-and-ECR/Demo-Work-on-Buildspecyaml-file-Part-02/page

Debugging an AWS CodeBuild failure to authenticate with Amazon ECR by fixing IAM permissions so builds can log in to ECR and push Docker images

In this lesson we debug a failing AWS CodeBuild run by inspecting the build logs, identifying the root cause, and applying the minimum required IAM changes so CodeBuild can authenticate to Amazon ECR and push Docker images.

## What happened (quick summary)

The build failed during the pre-build step when CodeBuild attempted to run:
`aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin <ECR_URI>`

The error in the logs shows the CodeBuild service role did not have permission to call `ecr:GetAuthorizationToken`, so authentication to ECR failed and the build exited.

## Inspecting the CodeBuild logs

Check the CodeBuild logs to find the failing step. The build downloads the source first and then executes the commands in `buildspec.yml`. Below is an excerpt from the failing run:

```text theme={null}
aws-cli/2.15.7 Python/3.11.6 Linux/4.18.0-348.el8.x86_64 exec-env/AWS_ECS_EC2

2024/02/19 03:18:00.409902 Waiting for agent ping
2024/02/19 03:18:07.349060 Phase is DOWNLOAD_SOURCE
2024/02/19 03:18:07.351164 CODEBUILD_SRC_DIR=codebuild/output/src1381929287/src/git-codecommit.eu-central-1.amazonaws.com/v1/repos/aws-microservice-project
2024/02/19 03:18:07.354431 Processing environment variables
2024/02/19 03:18:07.354452 No runtime environment selected in buildspec.
2024/02/19 03:18:07.655606 PRE_BUILD
2024/02/19 03:18:07.727964 phase shift: PRE_BUILD -> BUILD
2024/02/19 03:18:07.772743 Starting the build
2024/02/19 03:18:18.453611 Running command aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject
An error occurred (AccessDeniedException) when calling the GetAuthorizationToken operation: User: arn:aws:sts::666234783044:assumed-role/codebuild.aws-microservice-project-service-role/AWSCodeBuild-StartBuild-84e88e66-a6c7-4cf0-9cca-0cf847e17b48 is not authorized to perform: ecr:GetAuthorizationToken on resource: *
[Container] 2024/02/19 03:18:18.801288 Running command aws --version
[Container] 2024/02/19 03:18:19.311065 Phase complete: PRE_BUILD State: FAILED
[Container] 2024/02/19 03:18:19.311106 Command exited with non-zero status code: COMMAND_EXECUTION_ERROR Message: Error while executing command: aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin. Reason: exit status 1
```

## Root cause

* The CodeBuild service role (the assumed role in the log) was missing permissions to call `ecr:GetAuthorizationToken`. Without that action CodeBuild cannot obtain credentials to authenticate Docker to ECR.

## Fix: grant ECR permissions to the CodeBuild service role

Follow these steps to resolve the issue:

1. Copy the assumed role ARN from the error message (the `assumed-role/...` value).
2. Open the AWS Console → IAM → Roles.
3. Search for and select the CodeBuild service role shown in the logs.
4. Click "Attach policies".
5. Search for `container` to find ECR related managed policies.
6. Select the managed policy **AmazonEC2ContainerRegistryPowerUser** (this grants the ECR actions CodeBuild needs for build and push).
7. Click "Add permissions" to attach the policy.

<Frame>
  <img alt="This image shows an AWS IAM console where a user is attaching policies to a service role, with a list of available AWS managed permissions policies related to EC2 Container Registry." />
</Frame>

After attaching the policy, re-run the CodeBuild project (Start build) and monitor the logs. The next build should be able to authenticate to ECR and continue.

## Successful run — authentication, image build, and push

After fixing the role permissions the build logs should show successful ECR login, image creation, tagging, and push. Example successful pre-build and build lines:

```bash theme={null}
2024/02/19 03:23:01.902870 Running command aws --version
2024/02/19 03:23:02.689528 Running command aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject
WARNING: Your password will be stored unencrypted in '/root/.docker/config.json'.
Configure a credential helper to remove this warning. See https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
2024/02/19 03:23:02.826377 Running command REPOSITORY_URI=666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject
2024/02/19 03:23:02.833188 Running command COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
2024/02/19 03:23:02.842619 Running command IMAGE_TAG=$(echo $COMMIT_HASH)
2024/02/19 03:23:02.870384 Phase complete: BUILD State: SUCCEEDED
```

The build then shows Docker building the image and pushing layers to ECR. Example push output:

```text theme={null}
#9 exporting to image
#9 exporting layers 0.4 done
#9 writing image sha256:0de72c70987a46f7676443bfe6e5e5d02283ca6eaf0a4d4b28d0a4208 done
#9 naming to 666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest done
#9 DONE 0.4s
...
Running command docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
Running command echo Pushing the Docker image...
Running command docker push $REPOSITORY_URI:latest
The push refers to repository [666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject]
1af49fca580d: Preparing
b5d68cd6f062: Preparing
1af67b67162c: Preparing
ca274c4711b: Preparing
e6b364b54e: Preparing
c8b3674b54e: Preparing
1af9f76ba60b: Waiting
b5d68cd6f062: Pushed
1af67b67162c: Pushed
ca274c4711b: Pushed
e6b364b54e: Pushed
c8b3674b54e: Pushed
1af9f76ba60b: Pushed
latest: digest: sha256:8e110f19430ea193464746f8708d5d260cf5f8d8a07f1d8a7a3fe13eed896 size: 2001
```

<Frame>
  <img alt="The image shows an AWS CodeBuild interface displaying a successfully completed build project named &#x22;aws-microservice-project.&#x22; It includes build details such as status, initiator, and logs." />
</Frame>

You can verify the pushed images in the ECR console — repository tags such as `latest` and the short commit hash should appear.

<Frame>
  <img alt="The image shows an Amazon Elastic Container Registry (ECR) interface with a private repository named &#x22;cryptoproject&#x22; successfully created, displaying details like URI and creation date." />
</Frame>

## Recommended IAM permissions (least privilege guidance)

For production systems prefer least-privilege policies instead of broad managed policies. Below is a compact mapping of common ECR actions CodeBuild needs and why:

| Action                            | Use case                                          |
| --------------------------------- | ------------------------------------------------- |
| `ecr:GetAuthorizationToken`       | Get a temporary auth token to log Docker into ECR |
| `ecr:BatchCheckLayerAvailability` | Check which layers are needed during pushes       |
| `ecr:InitiateLayerUpload`         | Start uploading a layer                           |
| `ecr:UploadLayerPart`             | Upload layer chunks                               |
| `ecr:CompleteLayerUpload`         | Finalize layer upload                             |
| `ecr:PutImage`                    | Create or update an image manifest                |

Example minimal IAM policy (scope the `Resource` ARN to your repository where possible). Replace `<ACCOUNT_ID>` and `<REGION>` and `<REPOSITORY_NAME>` with your values:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRLoginAndPush",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage"
      ],
      "Resource": "arn:aws:ecr:<REGION>:<ACCOUNT_ID>:repository/<REPOSITORY_NAME>"
    },
    {
      "Sid": "AllowGetRepositoryPolicy",
      "Effect": "Allow",
      "Action": [
        "ecr:GetRepositoryPolicy",
        "ecr:DescribeRepositories"
      ],
      "Resource": "*"
    }
  ]
}
```

Notes:

* `ecr:GetAuthorizationToken` is a global call that typically requires `Resource: "*"`. You can keep that action broader while scoping the rest to specific repo ARNs if you need tighter permissions.
* If your builds use image caching or multiple repositories, include those repository ARNs as additional `Resource` entries.

## Quick checklist

* [ ] Verify the service role shown in the CodeBuild logs is the role you updated.
* [ ] Attach a managed policy (AmazonEC2ContainerRegistryPowerUser) for quick fixes, or create a scoped custom policy for least privilege.
* [ ] Re-run the build and confirm `Login Succeeded` and successful `docker push`.
* [ ] Confirm images and tags appear in the ECR console.

<Callout icon="lightbulb">
  For production environments, prefer granting least privilege. Instead of attaching a broad managed policy, consider creating a custom IAM policy that includes only the specific ECR actions CodeBuild needs (e.g., `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`, `ecr:PutImage`) and scope the resource ARNs to the specific repository.
</Callout>

## References

* Amazon ECR documentation: [https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* IAM policies and best practices: [https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

This completes the troubleshooting steps for fixing CodeBuild authentication to ECR and getting Docker image pushes working from your build pipeline.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/37195f61-a068-4f6c-9ccc-0bd66b358449/lesson/4f5a93f2-81c3-4f70-8f22-090ec5610a0b" />
</CardGroup>
