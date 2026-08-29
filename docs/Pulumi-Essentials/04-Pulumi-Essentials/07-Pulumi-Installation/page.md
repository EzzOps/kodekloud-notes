# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
```

When you run this program, Pulumi deploys an S3 bucket with a name based on the internal identifier "my-bucket". AWS will append a unique suffix to ensure the bucket name's uniqueness.

## Deploying the Pulumi Configuration

To deploy the infrastructure defined in your Python code, run the following command in your terminal:

```bash theme={null}
pulumi up
```

During the deployment process, Pulumi inspects your configuration and provides a preview of the changes. The output might look similar to this:

```bash theme={null}
Using cached attrs-23.1.0-py3-none-any.whl (61 kB)
Collecting typing-extensions (from parver>=0.2.1->pulumi-aws<6.0.0,>=5.0.0->-r requirements.txt (line 2))
Using cached typing_extensions-4.6.2-py3-none-any.whl (31 kB)
Installing collected packages: arpeggio, typing-extensions, six, semver, pyyaml, protobuf, grpcio, dill, attrs, pulumi, parver, pulumi-aws
Successfully installed arpeggio-2.0.0 attrs-23.1.0 dill-0.3.6 grpcio-1.51.3 parver-0.4 protobuf-4.23.2 pulumi-3.68.0 pulumi-aws-5.41.0 pyyaml-6.0 semver-2.13.0 six-1.16.0 typing-extensions-4.6.2
Finished installing dependencies
Finished installing dependencies

Your new project is ready to go!

To perform an initial deployment, run `pulumi up`
```

When prompted, Pulumi will display the resources that are about to be created. For a new project, it will show that two resources are scheduled for creation, as demonstrated below:

```bash theme={null}
C:\Users\sanje\Documents\scratch\pulumi-demo>pulumi up
Previewing update (dev)

View in Browser (Ctrl+O): https://app.pulumi.com/YourUserName/pulumi-demo/dev/previews/1132dcb8-db60
Type:          pulumi:pulumi:Stack  pulumi-demo-dev
               └── aws:s3:Bucket   my-bucket
Outputs:
  bucket_name: output<string>

Resources:
    + 2 to create

Do you want to perform this update? [Use arrows to move, type to filter]
 yes
> no
```

Upon confirming by selecting "yes," Pulumi proceeds to create the stack and deploy the specified resources. The S3 bucket is assigned a unique name (e.g., "my-bucket-5d138fe") during creation.

### Deployment Output

After deploying, your terminal will display detailed output similar to the snippet below:

```bash theme={null}
[urn=urn:pulumi:dev:pulumi-demo:aws:s3/bucket:Bucket::my-bucket]
[provider=urn:pulumi:dev:pulumi-demo:pulumi:providers:aws::default_5_41_0::04ada6b54-80e4-46f7-96ec-b56ff0331ba9]
acl            : "private"
bucket         : "my-bucket-a45f21d"
forceDestroy   : false
--outputs--
bucket_name    : output<string>
Do you want to perform this update? yes
Updating (dev)
View in Browser (Ctrl+O): https://app.pulumi.com/YourUserName/pulumi-demo/dev/updates/1
Type:
+ pulumi:pulumi:Stack      pulumi-demo-dev
  └─ aws:s3:Bucket        my-bucket
Outputs:
  bucket_name: "my-bucket-5d138fe"
Resources:
  + 2 created
Duration: 4s
C:\Users\sanje\Documents\scratch\pulumi-demo>
```

You can verify the creation of the S3 bucket directly in the AWS console. Although the Pulumi configuration uses the internal name "my-bucket," AWS assigns the bucket a unique name that includes an automatically generated suffix.

## Re-running the Deployment

If you run `pulumi up` with the identical configuration:

```python theme={null}
import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
```

and then execute:

```bash theme={null}
pulumi up
```

Pulumi compares the current configuration with the deployed infrastructure. If no changes are detected, you will see output indicating that the resources are unchanged:

```bash theme={null}
Type                  Name                Plan
pulumi:pulumi:Stack   pulumi-demo-dev     2 unchanged

Do you want to perform this update? no
confirmation declined, not proceeding with the update
```

> **lightbulb** Pulumi enforces that the deployed infrastructure always aligns with the configuration declared in your code, updating resources only when discrepancies occur.

## Summary

This lesson demonstrated the process of creating, deploying, and managing an AWS S3 bucket using Pulumi and Python. By continuously running `pulumi up`, you ensure that your infrastructure remains consistent with the defined configuration. This approach provides a robust example of Infrastructure as Code, helping prevent the accidental creation of duplicate resources.

For further reading on managing cloud infrastructure with Pulumi, be sure to explore the [Pulumi Documentation](https://www.pulumi.com/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/pulumi-essentials/module/883d8d6f-c8be-44af-ac4d-ba0835d32f5d/lesson/4e991c27-8737-48e5-a28c-85adc8f1f8df)


# Pulumi Installation

Source: https://notes.kodekloud.com/docs/Pulumi-Essentials/Pulumi-Essentials/Pulumi-Installation/page

This article provides a guide on installing Pulumi and configuring it with AWS credentials on various operating systems.

Pulumi is a powerful infrastructure as code tool that simplifies cloud deployments. In this guide, you'll learn how to install Pulumi on various operating systems and configure it to work with AWS.

## Installation

### Windows

For Windows users, you have two options:

1. Download the installer directly from the [Pulumi website](https://www.pulumi.com/docs/get-started/install/).
2. Install via Chocolatey by running the following command:

```bash theme={null}
choco install pulumi
```

### macOS

macOS users can easily install Pulumi using Homebrew. Run the command below in your terminal:

```bash theme={null}
brew install pulumi/tap/pulumi
```

## Configuring AWS Credentials for Pulumi

After installing Pulumi, the next step is to set up your AWS credentials. Pulumi leverages the same AWS credentials used by the AWS CLI. You can configure your credentials using one of the following methods:

### Option 1: Using Environment Variables

Set up your AWS credentials and region by executing these commands in your terminal:

```bash theme={null}
export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
export AWS_REGION=<YOUR_AWS_REGION>  # e.g., ap-south-1
```

Then, configure Pulumi to use your AWS region:

```bash theme={null}
pulumi config set aws:region <your-region>  # e.g., 'ap-south-1'
```

### Option 2: Using the AWS CLI

Alternatively, if you prefer using the interactive configuration provided by the AWS CLI, run:

```bash theme={null}
aws configure
```

You'll be prompted to enter your AWS credentials:

```bash theme={null}
AWS Access Key ID [None]: <YOUR_ACCESS_KEY_ID>
AWS Secret Access Key [None]: <YOUR_SECRET_ACCESS_KEY>
Default region name [None]: <YOUR_AWS_REGION>
Default output format [None]:
```

After completing this, the credentials will be stored in the `.aws/credentials` file, which typically looks like this:

```plaintext theme={null}
[default]
aws_access_key_id = <YOUR_ACCESS_KEY_ID>
aws_secret_access_key = <YOUR_SECRET_ACCESS_KEY>
```

Pulumi will automatically use this configuration to authenticate with AWS.

> **lightbulb** Choose the configuration method that best fits your workflow. Environment variables offer quick setup for temporary sessions, while the AWS CLI configuration provides a persistent setup across sessions.

Happy deploying with Pulumi!

## Additional Resources

* [Pulumi Documentation](https://www.pulumi.com/docs/)
* [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/pulumi-essentials/module/883d8d6f-c8be-44af-ac4d-ba0835d32f5d/lesson/8ab53585-2454-4046-ba5a-3c5ca780c8f7)
