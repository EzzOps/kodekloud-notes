# Additional imports (e.g., for encryption) can be added as required.
```

Then update the stack definition to include the S3 bucket:

```python theme={null}
class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create a basic S3 bucket.
        bucket = s3.Bucket(self, "My-kodekloud-cdk-bucket")
```

<Callout icon="lightbulb">
  Remember that bucket names must be globally unique. The CDK will append extra characters to ensure uniqueness.
</Callout>

For advanced configurations such as encryption using a KMS key, you might use:

```python theme={null}
bucket = s3.Bucket(self, "MyEncryptedBucket",
    encryption=s3.BucketEncryption.KMS
)

# To verify, you can access the encryption key:
# assert(bucket.encryption_key instanceof kms.Key)
```

In this demo, however, we use the basic bucket configuration.

***

## Synthesizing the CloudFormation Template

To generate the CloudFormation templates from your CDK app, run:

```bash theme={null}
cdk synth
```

This command synthesizes templates that detail the AWS resources like the S3 bucket and any related policies. A sample snippet of the generated output might be:

```text theme={null}
> cdk synth
Resources:
  MykodekloudcdkbucketB75EFD9A:
    Type: AWS::S3::Bucket
    UpdateReplacePolicy: Retain
    DeletionPolicy: Retain
    Metadata:
      aws:cdk:path: CdkStack/My-kodekloud-cdk-bucket/Resource
    CDKMetadata:
      Type: AWS::CDK::Metadata
      Properties:
        Analytics: v2:deflate64:...
```

***

## Configuring AWS Credentials

Before deploying, configure your AWS CLI credentials since the AWS CDK utilizes them for resource deployment. Run:

```bash theme={null}
aws configure
```

You will be prompted to enter your AWS Access Key ID, AWS Secret Access Key, default region, and output format. For example:

```text theme={null}
AWS Access Key ID [********************SQ5B]: AKIA4IAWSJ5UJ5XRRTMAI
AWS Secret Access Key [********************aRv]: <your-secret-key>
Default region name [us-east-1]:
Default output format [json]:
```

<Callout icon="triangle-alert">
  It is best practice to create a dedicated IAM user with limited permissions for CDK deployments in production. Avoid using full administrative privileges.
</Callout>

The following screenshots illustrate the process of creating an IAM user and generating access keys:

<Frame>
  ![The image shows the AWS IAM console where a user is specifying details to create a new user, including a field for the username and options for providing access to the AWS Management Console.](https://kodekloud.com/kk-media/image/upload/v1752858091/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/aws-iam-console-create-user.jpg)
</Frame>

<Frame>
  ![The image shows an AWS IAM console screen for creating a user, with details like user name, permissions summary, and an option to add tags. The "Create user" button is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752858093/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/aws-iam-create-user-console.jpg)
</Frame>

<Frame>
  ![The image shows an AWS console screen for creating an access key, with options for different use cases like CLI, local code, and third-party services.](https://kodekloud.com/kk-media/image/upload/v1752858095/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/aws-console-access-key-creation.jpg)
</Frame>

***

## Validating the Deployment with CDK Diff

Before deploying your changes, run a diff to compare your local template with what is currently deployed:

```bash theme={null}
cdk diff
```

The output will indicate which resources are set to be created, modified, or deleted. Since the S3 bucket hasn't been deployed yet, the diff output should reflect that a new S3 bucket will be created.

***

## Bootstrapping and Deploying the CDK Application

Certain environments require bootstrapping before deployment. If you encounter an error such as:

```text theme={null}
Error: CdkStack: SSM parameter /cdk-bootstrap/hnb659fds/version not found. Has the environment been bootstrapped? Please run 'cdk bootstrap'
```

Run the bootstrap command:

```bash theme={null}
cdk bootstrap
```

After successful bootstrapping, deploy your stack with:

```bash theme={null}
cdk deploy
```

During deployment, you will see messages indicating synthesis progress, publishing steps, and CloudFormation resource creation. An example output might include:

```text theme={null}
CdkStack: deploying... [1/1]
CdkStack: creating CloudFormation changeset...
...
Deployment time: 33.21s
Stack ARN:
arn:aws:cloudformation:us-east-1:841860927337:stack/CdkStack/b0a6b4c0-6bd7-11ee-9353-0a5897cc66
```

Once the deployment is complete, verify the S3 bucket in the AWS Management Console by refreshing the Buckets page.

<Frame>
  ![The image shows an Amazon S3 bucket interface with no objects listed, and options to upload or manage files.](https://kodekloud.com/kk-media/image/upload/v1752858096/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/amazon-s3-bucket-interface-empty.jpg)
</Frame>

Also, inspect the CloudFormation console to ensure the stack was deployed correctly:

<Frame>
  ![The image shows an AWS CloudFormation console with a list of stacks, their statuses, and creation times. One stack has a "DELETE\_FAILED" status, while others are marked "CREATE\_COMPLETE."](https://kodekloud.com/kk-media/image/upload/v1752858099/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/aws-cloudformation-stacks-statuses.jpg)
</Frame>

<Frame>
  ![The image shows an AWS CloudFormation console with a stack named "CdkStack" that has completed creation. It lists resources like "My-kodekloud-cdk-bucket" and "CDKMetadata" with a status of "CREATE\_COMPLETE."](https://kodekloud.com/kk-media/image/upload/v1752858100/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/aws-cloudformation-cdkstack-complete.jpg)
</Frame>

***

## Verifying the Deployed Template

After deployment, run the diff again to ensure that your deployed state matches your local configuration:

```bash theme={null}
cdk diff
```

Expected output:

```text theme={null}
Stack CdkStack
There were no differences
Number of stacks with differences: 0
```

This confirms that the deployed environment is in sync with your CDK application.

***

## Destroying the Stack

When you're finished with your demo, you can clean up your AWS environment by destroying the stack:

```bash theme={null}
cdk destroy
```

You'll be prompted to confirm deletion:

```text theme={null}
Are you sure you want to delete: CdkStack (y/n)? y
CdkStack: destroying... [1/1]
```

After destruction, confirm in the AWS console that both the CloudFormation stack and the S3 bucket have been removed.

<Frame>
  ![The image shows an Amazon S3 dashboard with a list of buckets, their regions, access settings, and creation dates.](https://kodekloud.com/kk-media/image/upload/v1752858102/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK-Demo/amazon-s3-dashboard-buckets-list.jpg)
</Frame>

***

## Conclusion

This guide provided an overview of using AWS CDK to manage AWS resources. You learned how to install and set up AWS CDK, initialize a Python project, modify the CDK stack to create an S3 bucket, deploy your infrastructure using CloudFormation, verify your deployment, and finally clean up resources.

Happy building with AWS CDK!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/6d3acaeb-020a-4e1e-9bd0-5fc6c50eb164/lesson/0591c752-a231-4bac-8bca-6023f4d25f5d" />
</CardGroup>


# AWS CDK

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/AWS-Fundamentals/AWS-CDK/page

This article explores the AWS Cloud Development Kit, an infrastructure-as-code tool that simplifies resource management on AWS using familiar programming languages.

In this article, we explore the AWS Cloud Development Kit (CDK)—an innovative infrastructure-as-code tool that streamlines resource management on AWS. Unlike AWS CloudFormation, which uses JSON or YAML templates, AWS CDK enables you to define infrastructure using familiar programming languages such as Python, JavaScript, Java, and .NET. This approach leverages the rich ecosystem of libraries, packages, and testing frameworks to create more dynamic, robust, and maintainable scripts.

When you build a CDK application, you work with constructs. These constructs are pre-configured blueprints that follow AWS best practices, simplifying resource provisioning. Under the hood, AWS CDK translates your high-level code into CloudFormation templates. For instance, running the command `cdk synth` generates the corresponding CloudFormation template, and executing `cdk deploy` deploys the stack to AWS.

Moreover, AWS CDK supports a wide range of programming languages, allowing you to choose the one that best aligns with your team's expertise.

<Frame>
  ![The image is a diagram illustrating the process of using AWS CDK to create CloudFormation templates from a CDK app, which are then deployed to AWS. It shows the flow from constructs in the CDK app to stacks in AWS CloudFormation, with programming languages like TypeScript, JavaScript, Java, .NET, and Python indicated at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752858103/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK/aws-cdk-cloudformation-diagram.jpg)
</Frame>

## Key Features and Benefits

1. **Declarative Infrastructure**: Define your infrastructure in a clear and declarative manner through code. This makes deployments transparent, repeatable, and predictable.
2. **Code Reusability**: Leverage a rich library of pre-built constructs and share custom components with the community, reducing duplication of effort.
3. **Automated Synthesis**: Automatically generate CloudFormation templates from your application code, ensuring consistency across deployments.
4. **Environment Agnosticism**: Write your infrastructure code once and deploy it seamlessly across different environments using parameterized configurations.

<Frame>
  ![The image lists five features: Declarative Approach, Component Reusability, AWS Construct Library, Automated Synthesis, and Environment Agnosticism, each represented with an icon.](https://kodekloud.com/kk-media/image/upload/v1752858104/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK/features-declarative-reusability-aws-icons.jpg)
</Frame>

<Callout icon="lightbulb">
  AWS CDK integrates seamlessly with various AWS services, enabling the construction of powerful and automated CI/CD pipelines for efficient infrastructure management.
</Callout>

AWS CDK not only simplifies resource provisioning but also integrates with other AWS services to support comprehensive CI/CD pipelines. For example, you might update your CDK application and commit changes to AWS CodeCommit, triggering a pipeline in [AWS CodePipeline (CI/CD Pipeline)](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline). Within this pipeline, tasks such as running `cdk synth` to generate CloudFormation templates, executing unit tests, building artifacts, and ultimately deploying AWS resources are automated.

<Frame>
  ![The image illustrates a CDK Pipeline workflow using AWS services, including AWS CodeCommit, AWS CodePipeline, AWS CodeBuild, AWS CloudFormation, and a CloudFormation stack with S3, EC2, VPC, and RDS.](https://kodekloud.com/kk-media/image/upload/v1752858105/notes-assets/images/AWS-Certified-Developer-Associate-AWS-CDK/cdk-pipeline-aws-services-workflow.jpg)
</Frame>

This integrated approach enhances the overall lifecycle management of your infrastructure and maximizes the effectiveness of AWS services in your CI/CD workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/6d3acaeb-020a-4e1e-9bd0-5fc6c50eb164/lesson/4c7d5ca2-3efc-4d3c-966a-936a59f8848e" />
</CardGroup>
