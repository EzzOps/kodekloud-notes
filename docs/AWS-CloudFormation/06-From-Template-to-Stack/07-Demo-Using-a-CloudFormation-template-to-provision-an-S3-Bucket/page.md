# Demo Using a CloudFormation template to provision an S3 Bucket

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/From-Template-to-Stack/Demo-Using-a-CloudFormation-template-to-provision-an-S3-Bucket/page

Guide to provision an Amazon S3 bucket by uploading a CloudFormation YAML template to create a stack via the AWS Management Console, including validation, console steps, and verification

This guide shows how to provision an Amazon S3 bucket by moving a CloudFormation template into a CloudFormation stack using the AWS Management Console. It includes a minimal YAML template, validation tips, step-by-step console instructions, and verification steps to confirm the bucket was created.

Resources:

* CloudFormation overview and console: [https://learn.kodekloud.com/user/courses/aws-cloud-formation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* Amazon S3 overview and console: [https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* CloudFormation linter (cfn-lint): [https://github.com/aws-cloudformation/cfn-lint](https://github.com/aws-cloudformation/cfn-lint)

## Minimal CloudFormation template (YAML)

Create a file named `s3-bucket.yml` with the following contents:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-xcvt-bkt
```

This template defines a single S3 bucket resource using the logical ID `MyS3Bucket`. The BucketName property sets the physical S3 bucket name created by the stack.

## Before creating the stack — validation and best practices

Follow these quick checks before uploading the template to CloudFormation:

* Save the template file locally (e.g., `s3-bucket.yml`).
* Validate the template with a linter to catch syntax and resource issues early:

```bash theme={null}
cfn-lint s3-bucket.yml
```

* Use concise, unique stack names to help identify resources later (e.g., `demo-stack`).
* Confirm the bucket name follows S3 naming rules and is globally unique.

Checklist:

| Task                       | Command / Action                               |
| -------------------------- | ---------------------------------------------- |
| Save template locally      | `s3-bucket.yml`                                |
| Lint template              | `cfn-lint s3-bucket.yml`                       |
| Confirm unique bucket name | Choose a globally unique name (S3 requirement) |
| Upload template            | Use the CloudFormation console or CLI          |

## Create the stack in the AWS Management Console

1. Open the AWS Management Console and navigate to CloudFormation.
2. Click **Create stack**.
3. Under **Prepare template**, select **Upload a template file** and choose your `s3-bucket.yml`. CloudFormation accepts both JSON and YAML templates.
4. Click **Next**.
5. Provide a stack name (for example, `demo-stack`), accept the defaults, and submit to create the stack.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Create stack&#x22; workflow, showing the &#x22;Specify stack details&#x22; page. The Stack name field is filled with &#x22;DemoStack&#x22; and the left stepper highlights Step 2." />
</Frame>

Note: When you upload a template through the console, CloudFormation automatically stores the uploaded template content in an internal S3 location (you will typically see a `cf-templates` bucket appear in your S3 console for these uploads).

## Monitor stack creation

After submission, CloudFormation begins creating the stack. Use the Events tab to monitor progress and surface any errors. When creation completes successfully, the stack status will change to `CREATE_COMPLETE`.

* Refresh the CloudFormation console to update the stack status and events.
* The Stack info pane shows the stack ID, creation time, and current status.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console. It shows a stack named &#x22;DemoStack&#x22; with status &#x22;CREATE_COMPLETE&#x22; and overview details like the Stack ID and created time." />
</Frame>

## Verify the provisioned S3 bucket

1. Open the stack and go to the Resources tab.
   * The logical ID in the template (`MyS3Bucket`) appears here along with the resource type (`AWS::S3::Bucket`).
   * The Physical ID is the actual S3 bucket name created (`eden-kodekloud-xcvt-bkt` in this example). Click the Physical ID to open the bucket in the S3 console.

2. Check the S3 console to confirm the new bucket exists. You will usually see:
   * The bucket created by your stack (the physical ID shown in CloudFormation).
   * A `cf-templates` bucket prefixed bucket used by CloudFormation to store uploaded templates (created automatically for console uploads).

<Frame>
  <img alt="A screenshot of the AWS S3 web console on the &#x22;General purpose buckets&#x22; tab. It shows two S3 buckets listed (cf-templates... and eden-kodekloud...), their region (US East Ohio), creation dates, and actions like &#x22;Create bucket.&#x22;" />
</Frame>

> **lightbulb** When you upload a template through the CloudFormation console, CloudFormation creates and uses a `cf-templates` S3 bucket in your account to store the uploaded template. This is expected behavior for console uploads.

Back in CloudFormation, the Resources tab shows the S3 resource with status `CREATE_COMPLETE` and provides a direct link to the physical S3 bucket created by the stack.

<Frame>
  <img alt="Screenshot of the AWS CloudFormation console showing the &#x22;DemoStack&#x22; stack. The Resources tab lists an S3 bucket resource named &#x22;MyS3Bucket&#x22; with status CREATE_COMPLETE." />
</Frame>

## Summary and next steps

* Create a simple CloudFormation template that defines an S3 bucket.
* Validate the template locally (for example, with cfn-lint) before uploading.
* Upload the template through the CloudFormation console, provide a stack name, and create the stack.
* CloudFormation creates the S3 bucket defined in the template and an internal `cf-templates` bucket to store the uploaded template.
* Use the CloudFormation Events and Resources tabs to verify creation and to navigate directly to the S3 bucket.

Further reading:

* [AWS CloudFormation Documentation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [Amazon S3 Documentation](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [cfn-lint on GitHub](https://github.com/aws-cloudformation/cfn-lint)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/d0ac0bcf-be2c-4c53-a2f7-8f59a760e9de/lesson/b429afcb-1ea8-4e85-9932-e53be0ed498a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/d0ac0bcf-be2c-4c53-a2f7-8f59a760e9de/lesson/4bf7b7f4-9662-4bf9-bf8f-735d7161276e)
