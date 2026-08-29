# or monitor the CloudFormation console until the stack is removed
```

Notes about deletion:

* CloudFormation deletes the S3 bucket and EC2 instance it created unless the bucket contains objects you uploaded manually. Objects in an S3 bucket prevent its automatic deletion.
* If you created temporary access keys for this demo, deactivate and delete them to reduce security risk.

Example CLI commands to deactivate and delete an access key (replace placeholders):

```bash theme={null}
aws iam update-access-key --user-name <USER_NAME> --access-key-id <ACCESS_KEY_ID> --status Inactive
aws iam delete-access-key --user-name <USER_NAME> --access-key-id <ACCESS_KEY_ID>
```

> **warning** Be careful when deleting stacks—confirm you are deleting the correct stack and verify there are no important objects in S3 buckets. Deletion can cause irreversible data loss and objects may block the stack from being removed.

## Quick reference

| Action               | CLI command                                                                                                          | Notes                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Create stack         | `aws cloudformation create-stack --stack-name simple-s3-ec2-stack --template-body file://cli.yaml --region <region>` | Use `--region` to control where resources are created |
| Describe stack       | `aws cloudformation describe-stacks --stack-name simple-s3-ec2-stack --region <region>`                              | Check status and outputs                              |
| List stack resources | `aws cloudformation list-stack-resources --stack-name simple-s3-ec2-stack --region <region>`                         | Lists logical/physical IDs                            |
| Delete stack         | `aws cloudformation delete-stack --stack-name simple-s3-ec2-stack --region <region>`                                 | Removes resources created by the stack                |

## Links and further reading

* [AWS CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* [CloudFormation concepts](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [Amazon S3 documentation](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Amazon EC2 documentation](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

## Summary

* Author a minimal CloudFormation YAML template (`cli.yaml`) defining an S3 bucket and EC2 instance.
* Use the AWS CLI to create the stack: `aws cloudformation create-stack --stack-name ... --template-body file://cli.yaml --region <region>`.
* Verify the resources in the CloudFormation, S3, and EC2 consoles.
* Delete the stack to clean up resources and remove any temporary access keys.

That completes this demo on using CloudFormation with the AWS CLI to provision an S3 bucket and an EC2 instance.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/da18dc16-b0d4-49b1-a85d-32b98462fd6c/lesson/550122f7-b6f1-4bc2-a984-91687f69fc6b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/da18dc16-b0d4-49b1-a85d-32b98462fd6c/lesson/e221b4b8-56d0-4f1e-9310-e2b66fea3feb)


# Demo Installing and setting up AWS CLI

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/AWS-CLI/Demo-Installing-and-setting-up-AWS-CLI/page

Guide to installing and configuring the AWS CLI, creating IAM access keys and profiles, verifying installation, and following security best practices.

In this lesson we'll install and configure the AWS Command Line Interface (AWS CLI). The AWS CLI enables programmatic access to AWS services (for example, CloudFormation and many others) directly from your local machine, avoiding the need to use the AWS Management Console for repetitive or scripted tasks.

Begin by opening your browser and searching for "AWS CLI download" or visit the official AWS documentation page for installing/updating the AWS CLI:
[https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). On that page, select the installer or instructions that match your operating system.

<Frame>
  <img alt="A screenshot of the AWS documentation page titled &#x22;AWS CLI install and update instructions,&#x22; showing expandable sections for Linux, macOS, and Windows. The browser window (with tabs) and a Windows taskbar are visible at the bottom." />
</Frame>

## Quick installer summary (by OS)

| Operating System    | Recommended installer                          | Direct download URL / command                                                          |
| ------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| macOS (recommended) | Official .pkg installer                        | [https://awscli.amazonaws.com/AWSCLIV2.pkg](https://awscli.amazonaws.com/AWSCLIV2.pkg) |
| Windows             | MSI installer (interactive or msiexec)         | [https://awscli.amazonaws.com/AWSCLIV2.msi](https://awscli.amazonaws.com/AWSCLIV2.msi) |
| Linux               | Platform-specific package or bundled installer | See the AWS docs for distribution-specific commands                                    |

## macOS installation (recommended approach)

Download the official macOS installer package (.pkg) from the AWS docs or from:
[https://awscli.amazonaws.com/AWSCLIV2.pkg](https://awscli.amazonaws.com/AWSCLIV2.pkg)

Typical macOS installation locations:

* /usr/local/aws-cli
* /usr/local/bin/aws

Installation steps:

1. Download AWSCLIV2.pkg.
2. Double-click the .pkg and follow the installer prompts (Authenticate when prompted).
3. After installation, verify with aws --version.

Optional: If you prefer Homebrew, you can also install via:

```bash theme={null}
brew install awscli
```

(Refer to Homebrew docs if using that method.)

## Windows installation (MSI)

You can install interactively (GUI) or from the command line. An elevated Administrator Command Prompt or PowerShell is required for system-wide installs.

Interactive:

* Download the MSI and double-click it.
* Follow the setup wizard (Accept terms → Next → Install), handle any UAC prompts, and finish.

Command-line (interactive):

```powershell theme={null}
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

Command-line (silent install):

```powershell theme={null}
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi /qn
```

After installation completes, close the installer.

## Verify the installation

Open a terminal (macOS/Linux) or Command Prompt / PowerShell (Windows) and run:

```bash theme={null}
aws --version
```

Example output (your versions may differ):

```text theme={null}
aws-cli/2.27.50 Python/3.10.6 Windows/10 exe/AMD64
```

If a version string appears, the AWS CLI is installed and available in your PATH.

## Create access keys (IAM user)

To authenticate CLI requests, create access keys for an IAM user with the appropriate permissions:

1. Sign in to the AWS Management Console and open the IAM console: [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).
2. Select "Users" and choose the user you will use for CLI access.
3. Open the "Security credentials" tab and create a new access key.
4. Immediately copy or download the Access Key ID and Secret Access Key — you will not be able to view the secret again after closing the creation dialog.

<Frame>
  <img alt="A browser screenshot of the AWS IAM console showing a green &#x22;Access key created&#x22; confirmation banner and a panel titled &#x22;Access key best practices&#x22; with tips and buttons to download a .csv file or finish. The page also shows the IAM breadcrumb for user &#x22;arno-cf&#x22; and a small tooltip saying &#x22;Secret access key Copied.&#x22;" />
</Frame>

> **warning** Never commit or share your Access Key ID and Secret Access Key publicly. Treat them like passwords. If an access key is accidentally exposed, delete it immediately and create a new one.

You can download the .csv file from the console for secure storage. After you finish the tasks that require the key, remove the access key if it is no longer needed.

<Frame>
  <img alt="A screenshot of the AWS Identity and Access Management (IAM) console showing a user's &#x22;Access keys&#x22; page with one active access key listed and the IAM navigation pane on the left." />
</Frame>

## Configure the AWS CLI

With your Access Key ID and Secret Access Key ready, run the interactive configuration command:

```bash theme={null}
aws configure
```

You will be prompted for these values. Example interactive session (replace with your actual keys and preferred region/output):

```text theme={null}
$ aws configure
AWS Access Key ID [None]: <YOUR_AWS_ACCESS_KEY_ID>
AWS Secret Access Key [None]: <YOUR_AWS_SECRET_ACCESS_KEY>
Default region name [None]: us-east-2
Default output format [None]: yaml
```

This creates/stores credentials and settings in these files:

* macOS / Linux:
  * \~/.aws/credentials
  * \~/.aws/config
* Windows:
  * %USERPROFILE%.aws\credentials
  * %USERPROFILE%.aws\config

Table: config file locations

| Platform      | Credentials file              | Config file              |
| ------------- | ----------------------------- | ------------------------ |
| macOS / Linux | \~/.aws/credentials           | \~/.aws/config           |
| Windows       | %USERPROFILE%.aws\credentials | %USERPROFILE%.aws\config |

## Working with multiple profiles

If you manage multiple AWS accounts or roles, create named profiles:

```bash theme={null}
aws configure --profile <profile-name>
```

Then use that profile with:

* The --profile option: aws s3 ls --profile \<profile-name>
* Environment variable: export AWS\_PROFILE=\<profile-name> (macOS/Linux) or setx AWS\_PROFILE "\<profile-name>" (Windows)

> **lightbulb** If you work with multiple AWS accounts or roles, consider creating named profiles with:
  aws configure --profile \<profile-name>
  Then use that profile with --profile \<profile-name> or set AWS\_PROFILE in your environment.

## Quick tips and housekeeping

* Clear the terminal:
  * macOS/Linux: clear
  * Windows Command Prompt: CLS
* Rotate and remove keys you no longer need.
* Prefer IAM roles (EC2/ECS/STS) where possible for temporary credentials and improved security.
* Follow the principle of least privilege when assigning IAM permissions.

## Links and references

* AWS CLI official docs: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* IAM console: [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)
* IAM best practices: [https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
* CloudFormation (for examples and further lessons): [https://learn.kodekloud.com/user/courses/aws-cloud-formation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)

That’s it — the AWS CLI should now be installed and configured. Remember to secure and rotate access keys, and prefer roles and least-privilege IAM policies whenever possible.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/da18dc16-b0d4-49b1-a85d-32b98462fd6c/lesson/7a1fc605-1825-4ea3-bccf-bd4917b12197)
