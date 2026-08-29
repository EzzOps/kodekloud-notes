# IAM Roles

Source: https://notes.kodekloud.com/docs/AWS-IAM/Introduction-to-AWS-Identity-and-Access-Management/IAM-Roles/page

AWS IAM roles provide secure, temporary access to resources, enabling fine-grained permissions and trust relationships while minimizing exposure risk.

AWS Identity and Access Management (IAM) roles enable secure, temporary access to AWS resources without embedding long-term credentials. By defining fine-grained permissions and trust relationships, you can enforce the principle of least privilege and reduce exposure risk.

| Component          | Description                                                                 | Example                                          |
| ------------------ | --------------------------------------------------------------------------- | ------------------------------------------------ |
| Role               | An identity with attached permissions and a trust policy                    | `S3AccessRole`                                   |
| Permissions Policy | A JSON document specifying allowed or denied actions                        | `AmazonS3ReadOnlyAccess`                         |
| Trust Policy       | Defines which principals (services, users, or accounts) can assume the role | EC2 service: `ec2.amazonaws.com`                 |
| Temporary Tokens   | Short-lived credentials issued by AWS STS                                   | `AccessKeyId`, `SecretAccessKey`, `SessionToken` |

![The image explains IAM roles, highlighting their use for access control, adherence to the principle of least privilege, creation of temporary credentials, and establishment of trust relationships.](https://kodekloud.com/kk-media/image/upload/v1752863063/notes-assets/images/AWS-IAM-IAM-Roles/iam-roles-access-control-diagram.jpg)

## How IAM Roles Enhance Security

Instead of hard-coding long-term AWS keys:

1. A principal (user or service) calls `sts:AssumeRole`.
2. AWS returns temporary credentials.
3. The principal uses these credentials to access resources.
4. Credentials expire automatically, minimizing the blast radius.

> **lightbulb** Always follow the [principle of least privilege](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege). Grant only the permissions required for the task.

### Role Assumption Flow

![The image illustrates a process for increasing security using IAM roles, showing the flow from an IAM user assuming a role, applying a policy, accessing an S3 role, and obtaining temporary keys.](https://kodekloud.com/kk-media/image/upload/v1752863064/notes-assets/images/AWS-IAM-IAM-Roles/iam-roles-security-process-diagram.jpg)

Roles can be assumed not only by IAM users but also by AWS services such as EC2, Lambda, and ECS. The permissions come from attached policies, while the trust policy specifies who can assume the role.

### AWS Components Interaction

![The image is a diagram illustrating the relationship between AWS components: EC2 Service, S3 Bucket, IAM Role, IAM Policy, and IAM User. It shows how these components interact with each other in an AWS IAM Role setup.](https://kodekloud.com/kk-media/image/upload/v1752863065/notes-assets/images/AWS-IAM-IAM-Roles/aws-ec2-s3-iam-relationship-diagram.jpg)

***

## Demo: Create an IAM Role for EC2 to Access S3

Follow these steps in the AWS Management Console or use the AWS CLI commands shown.

### Console Steps

1. **Open the IAM console**\
   [https://console.aws.amazon.com/iam](https://console.aws.amazon.com/iam)

2. **Create a new role**
   * In the navigation pane, choose **Roles** → **Create role**.
   * Under **Select trusted entity**, choose **AWS service**, then **EC2**, and click **Next**.

3. **Attach permissions**
   * Search for **AmazonS3ReadOnlyAccess** (or attach your custom policy).
   * Select it and click **Next**.

4. **Name and create**
   * Enter **Role name**: `S3AccessRole`
   * Review settings and click **Create role**.

5. **Attach the role to an existing EC2 instance**
   * Open the EC2 console, select your instance.
   * Choose **Actions** → **Security** → **Modify IAM role**.
   * Select **S3AccessRole** and click **Save**.

### AWS CLI Alternative

First, create a trust policy file (`trust-policy.json`):

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

Then run:

```bash theme={null}
