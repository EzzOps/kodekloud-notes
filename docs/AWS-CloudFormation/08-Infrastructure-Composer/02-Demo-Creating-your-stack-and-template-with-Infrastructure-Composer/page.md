# Demo Creating your stack and template with Infrastructure Composer

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Infrastructure-Composer/Demo-Creating-your-stack-and-template-with-Infrastructure-Composer/page

Guide showing how to use AWS CloudFormation Infrastructure Composer to visually create an S3 bucket, export the generated template, and deploy a CloudFormation stack

In this walkthrough you'll use AWS CloudFormation's Infrastructure Composer to visually design a resource, export the generated template, and create a CloudFormation stack. This is useful when you prefer a drag-and-drop experience to build CloudFormation templates (YAML or JSON), inspect the output, and then deploy it.

Key concepts covered:

* Use Infrastructure Composer to add an S3 bucket visually
* Inspect and edit the generated CloudFormation template
* Export the template to CloudFormation and deploy the stack
* Understand deletion behavior for S3 buckets created by CloudFormation

First, start creating a stack in the CloudFormation console and choose the "Build from Infrastructure Composer" option.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Create stack&#x22; page showing the &#x22;Prerequisite - Prepare template&#x22; section with the &#x22;Choose an existing template&#x22; option selected and an alternate &#x22;Build from Infrastructure Composer&#x22; option. The browser window shows tabs at the top and the Windows taskbar along the bottom." />
</Frame>

## 1. Add resources in Infrastructure Composer

When Infrastructure Composer launches, you’ll see the visual canvas. Use the search box to find the resource you want to add (for example, type “S3”), then drag an S3 bucket onto the canvas.

Select the resource to open the resource properties in the right-hand sidebar. There you can:

* Change the logical ID (for example, from the default “bucket” to `MyS3BucketSpecial`)
* Enable features like static website hosting
* Override the bucket name to supply a specific globally unique name

<Callout icon="lightbulb">
  S3 bucket names must be unique across the entire AWS global namespace and must follow [S3 bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html). If you supply a custom bucket name, ensure it’s globally unique.
</Callout>

In this demonstration a custom bucket name was used: `eden-kodekloud-vbnc-bkt`. Infrastructure Composer fills in reasonable defaults for security and encryption, such as blocking public access and enabling server-side encryption. You can preview and edit the generated template before exporting.

## 2. Example generated template (YAML)

Below is the CloudFormation YAML that Infrastructure Composer created for the S3 bucket and an attached bucket policy that denies non-HTTPS requests:

```yaml theme={null}
Resources:
  MyS3BucketSpecial:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-vbnc-bkt
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyId: alias/aws/s3
      PublicAccessBlockConfiguration:
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  MyS3BucketSpecialBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref MyS3BucketSpecial
      PolicyDocument:
        Version: "2012-10-17"
        Id: RequireEncryptionInTransit
        Statement:
          - Sid: DenyUnencryptedTransport
            Effect: Deny
            Principal: "*"
            Action: "s3:*"
            Resource:
              - !Sub "arn:aws:s3:::${MyS3BucketSpecial}"
              - !Sub "arn:aws:s3:::${MyS3BucketSpecial}/*"
            Condition:
              Bool:
                aws:SecureTransport: "false"
```

You can switch the template view to JSON if you prefer, run template validation, or make direct edits in the template editor. When satisfied, click **Create template** to export it to CloudFormation.

When you confirm the export, Infrastructure Composer stores the template in an S3 bucket. You can select an existing bucket or let Composer use the suggested bucket.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation Infrastructure Composer showing a &#x22;Continue to CloudFormation&#x22; modal that says the template will be put in an existing S3 bucket and offers &#x22;Cancel&#x22; or &#x22;Confirm and continue to CloudFormation&#x22; buttons. The blurred background shows the Infrastructure Composer canvas and resources sidebar." />
</Frame>

## 3. Create the CloudFormation stack

Provide a stack name (for example, `ICDemoStack`) and proceed through the CloudFormation create-stack workflow. Review parameters, options, tags, and IAM capabilities as you normally would.

<Frame>
  <img alt="Screenshot of the AWS CloudFormation &#x22;Create stack&#x22; console on the &#x22;Specify stack details&#x22; step, with the stack name field filled as &#x22;iCDemoStack.&#x22; The left sidebar shows CloudFormation navigation and the parameters section reports no parameters defined." />
</Frame>

Submit the stack and monitor progress on the CloudFormation console’s Events tab.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing the &#x22;Stacks&#x22; view. The right pane displays an ICDEmoStack selected with its Events tab open and status &#x22;CREATE_IN_PROGRESS.&#x22;" />
</Frame>

## 4. Confirm resource creation

After the stack completes, the S3 bucket is available in the S3 console. In the example shown, the bucket `eden-kodekloud-vbnc-bkt` is present and initially empty.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the bucket &#x22;eden-kodekloud-vbnc-bkt&#x22; with the Objects tab open; the bucket is empty and displays options like Upload, Create folder, Actions, and metadata/permissions tabs." />
</Frame>

Because this bucket contains no objects, deleting the CloudFormation stack will remove the bucket cleanly. If the bucket contains objects, stack deletion can fail unless you handle object removal (see the warning below).

<Callout icon="warning">
  If an S3 bucket contains objects, CloudFormation stack deletion will fail for the bucket resource unless you explicitly handle object removal (for example with a Lambda-backed custom resource or an S3 lifecycle/configuration that empties the bucket). Always ensure you understand retention and deletion behavior before removing stacks that include S3 buckets.
</Callout>

## Resources created by this example

| Resource Type         | Logical ID                    | Purpose                                                              |
| --------------------- | ----------------------------- | -------------------------------------------------------------------- |
| AWS::S3::Bucket       | MyS3BucketSpecial             | Stores objects; has server-side encryption and public access blocked |
| AWS::S3::BucketPolicy | MyS3BucketSpecialBucketPolicy | Denies unencrypted (non-HTTPS) requests to the bucket                |

## Summary

Using Infrastructure Composer you can:

* Visually design resources and relationships
* Preview and edit the generated CloudFormation YAML/JSON
* Export the template to CloudFormation for deployment
* Monitor stack creation and validate resulting AWS resources

Links and references:

* [Infrastructure Composer — CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/infrastructure-composer.html)
* [S3 bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html)
* [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/563043d1-772f-4d1f-a812-f0a96dafa94f/lesson/b20c3614-45f3-464a-a7c1-6e9e724c4113" />
</CardGroup>
