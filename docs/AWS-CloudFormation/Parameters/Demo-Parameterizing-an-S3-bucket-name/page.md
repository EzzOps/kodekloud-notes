# Demo Parameterizing an S3 bucket name

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Parameters/Demo-Parameterizing-an-S3-bucket-name/page

Explains how to parameterize an AWS CloudFormation template to supply an S3 bucket name via Parameters and !Ref, validate locally, and safely update stacks

This demo shows how to make an AWS CloudFormation template reusable by parameterizing the S3 bucket name. Instead of hard-coding values in the template, use CloudFormation parameters so you can supply inputs when creating or updating a stack.

* What you'll learn: how to add a parameter for a bucket name, reference it from a resource using `!Ref`, validate the template locally, and update a stack in the console.
* Useful reference: [CloudFormation parameters documentation](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html).

Why use parameters?

* Parameters let you provide input at stack creation or update time.
* They improve template reusability and avoid embedding environment-specific values.

Example: template with a hard-coded bucket name

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-xcvt-bkt
      Tags:
        - Key: Developer
          Value: "Arno Pretorius"
        - Key: Environment
          Value: "Development"

Metadata: {}
```

If a template defines no parameters, the CloudFormation console will not show any input fields when updating a stack.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Specify stack details&#x22; step for updating a stack named DemoStack, showing the Parameters panel which says &#x22;No parameters.&#x22; Navigation buttons &#x22;Cancel,&#x22; &#x22;Previous,&#x22; and &#x22;Next&#x22; are visible at the bottom." />
</Frame>

Where to place the Parameters block

* Best practice: place the `Parameters` section near the top of the template (above `Resources`) for readability and maintainability.

Add a parameter for the bucket name

* Define a parameter named `InputBucketName` that accepts a string and provides a helpful description.

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-xcvt-bkt
```

Reference the parameter in the resource

* Replace the hard-coded bucket name with a reference to the `InputBucketName` parameter using `!Ref`:

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: "Arno Pretorius"
        - Key: Environment
          Value: "Development"
```

S3 bucket naming constraints

<Callout icon="lightbulb">
  [S3 bucket names](https://docs.aws.amazon.[SECRET_REDACTED].html) must be globally unique and conform to naming rules. Typical constraints include:

  * 3–63 characters
  * Lowercase letters, numbers, hyphens, and dots allowed (no underscores)
  * Cannot be formatted as an IP address
  * Must begin and end with a letter or number

  If your bucket name contains dots, be aware of virtual-hosted–style endpoint and TLS certificate restrictions.
</Callout>

<Callout icon="warning">
  Changing `BucketName` in your template causes CloudFormation to replace the S3 bucket resource (CloudFormation cannot rename an existing bucket). Replacement deletes the old resource and creates a new one; deletion can fail if the original bucket is not empty. Take care when updating bucket names in an existing stack.
</Callout>

Validate your template locally (recommended)

* Use cfn-lint to validate the YAML template before uploading:

```bash theme={null}
cfn-lint S3-bucket.yaml
```

If validation passes, update the CloudFormation stack:

1. In the console select the stack and choose Update stack → Replace current template → Upload a template file.
2. Upload your updated template and click Next.

During the update flow, the Parameters panel will display the `InputBucketName` field and its description. This is where you provide the value that gets substituted into the template via `!Ref`.

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: "Arno Pretorius"
        - Key: Environment
          Value: "Development"
```

You can also add or override tags in the console during the Configure stack options step—here's an example of adding a tag.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Configure stack options&#x22; step, showing the Tags section with a tag key &#x22;Status&#x22; and value &#x22;Active.&#x22; The left sidebar shows the update stack workflow steps and the top bar displays the AWS navigation/header." />
</Frame>

Submit the update and monitor progress

* After submitting the update, wait for the stack to complete. On success, the stack status will show UPDATE\_COMPLETE.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation Stacks console showing one stack named &#x22;DemoStack.&#x22; The stack entry shows a timestamp and a green &#x22;UPDATE_COMPLETE&#x22; status." />
</Frame>

Verify the bucket in S3

* Open the [S3 console](https://s3.console.aws.amazon.com/s3/home) and refresh the bucket list. The bucket name you entered via the parameter will appear, and the tags defined in the template will be applied.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the Properties tab for the bucket &#x22;eden-kodekloud-bncv-bkt,&#x22; including the bucket overview (ARN, AWS Region: US East (Ohio)) and the creation date. The lower part shows the Bucket Versioning section with an Edit button." />
</Frame>

Summary

* Use CloudFormation Parameters to supply values at stack creation or update time instead of hard-coding them.
* Place `Parameters` at the top of your template (above `Resources`) for readability.
* Use `!Ref` to reference parameter values inside `Resources`.
* Validate templates locally with `cfn-lint` before deploying.
* Ensure S3 bucket names meet naming constraints and be careful: changing a bucket name forces resource replacement.

Links and references

| Resource                  | Purpose                                 | Link                                                                                                                                                                                                 |
| ------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CloudFormation parameters | Reference and details                   | [https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html) |
| S3 bucket naming rules    | Naming constraints and guidance         | [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)                                         |
| cfn-lint                  | Template validation tool                | [https://github.com/aws-cloudformation/cfn-lint](https://github.com/aws-cloudformation/cfn-lint)                                                                                                     |
| Updating stacks           | Update stack workflow in CloudFormation | [https://docs.aws.amazon.[SECRET_REDACTED]-stacks.html](https://docs.aws.amazon.[SECRET_REDACTED]-stacks.html)                           |

Extending this pattern

* Use parameters for tags, versioning settings, or names of other resources to make templates flexible and environment-agnostic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/636db37e-4a51-4bb0-bcec-7ebf488a26b8/lesson/32417087-d6d2-42cd-aae0-ed6436e610dd" />
</CardGroup>
