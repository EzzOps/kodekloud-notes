# Deploy and Configure IAM Role

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/AWS-With-CDKTF/Deploy-and-Configure-IAM-Role/page

Instructions to create and configure an AWS Lambda IAM execution role including trust policy, permissions for logging, and verification steps while following least privilege

This section shows how to deploy and configure the IAM execution role that your Lambda function will assume. The role lets the Lambda service run your code securely and gives the function the permissions it needs (for example, to write logs or access other AWS services). Follow the steps below to create the trust policy and verify the role.

## Create the IAM execution role

Create an IAM role and provide an assume role (trust) policy that allows the Lambda service to assume the role:

```javascript theme={null}
const lambdaRole = new iamRole.IamRole(this, 'lambda-execution-role', {
  name: 'name-picker-execution-role',
  assumeRolePolicy: JSON.stringify({
    Version: '2012-10-17',
    Statement: [{
      Effect: 'Allow',
      Principal: { Service: 'lambda.amazonaws.com' },
      Action: 'sts:AssumeRole'
    }]
  })
});
```

This JSON trust policy grants the Lambda service permission to assume the role. Key fields in the trust policy:

* `Version` — The policy language version.
* `Statement.Effect` — `Allow` permits the action.
* `Statement.Principal` — The AWS service or principal allowed to assume the role (`lambda.amazonaws.com` here).
* `Statement.Action` — `sts:AssumeRole` is the action that allows the principal to assume the role.

| Trust policy field    | Purpose                                | Example                                 |
| --------------------- | -------------------------------------- | --------------------------------------- |
| `Version`             | Specifies the policy syntax version    | `2012-10-17`                            |
| `Statement.Principal` | Who can assume the role                | `{ "Service": "lambda.amazonaws.com" }` |
| `Statement.Action`    | The allowed action for the principal   | `sts:AssumeRole`                        |
| `Statement.Effect`    | Whether the statement allows or denies | `Allow`                                 |

The assume role policy (also called the trust policy) establishes *who* can assume the role. The role still requires an identity permissions policy to specify *what* the Lambda function can do after assuming the role.

> **lightbulb** Grant only the permissions your Lambda function needs. Start with the managed policy `service-role/AWSLambdaBasicExecutionRole` for CloudWatch Logs, then narrow permissions with a custom inline or managed policy to follow the principle of least privilege.

## Provide runtime permissions

A typical Lambda execution role needs permission to write logs to CloudWatch. You can grant this using the AWS managed policy `AWSLambdaBasicExecutionRole` or by creating a minimal custom policy that only allows the required actions.

Example: attach the AWS managed logging policy using the AWS CLI:

`aws iam attach-role-policy --role-name name-picker-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`

Alternatively, add a custom inline policy that grants only the specific permissions your function needs (for example, specific S3 or DynamoDB actions). Using managed policies is a convenient starting point; refine permissions later.

## Verify the role and trust relationship

You can inspect the role and its trust relationship in the AWS Console:

1. Open the IAM service.
2. Select “Roles”.
3. Choose the role (for example, `name-picker-execution-role`).
4. View the **Trust relationships** tab to confirm the assume role policy.
5. View the **Permissions** tab to verify attached policies (for logging and any resource access).

To summarize:

* Every Lambda function assumes an IAM execution role that contains two parts:
  * The trust policy (assume role policy) — who can assume the role (here, the Lambda service).
  * The permissions policy — what the function is allowed to do (CloudWatch logs, S3, DynamoDB, etc.).
* Start with `service-role/AWSLambdaBasicExecutionRole` to enable logging, then apply least-privilege custom policies for additional resource access.

## Links and References

* [IAM Roles for AWS Lambda - AWS Docs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)
* [AWS managed policies reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html)
* [AWS IAM documentation](https://docs.aws.amazon.com/iam/latest/UserGuide/)

That concludes this section on deploying and configuring the IAM role for your Lambda function.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/4625ff69-dbd8-42ac-9542-d0e60a85e2ae/lesson/6099b48a-109c-4a8c-88b7-3c38e290379a)
