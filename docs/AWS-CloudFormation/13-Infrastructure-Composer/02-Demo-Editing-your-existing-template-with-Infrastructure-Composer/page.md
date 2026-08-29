# Demo Editing your existing template with Infrastructure Composer

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Infrastructure-Composer/Demo-Editing-your-existing-template-with-Infrastructure-Composer/page

Demonstrates editing, validating, and updating an existing AWS CloudFormation template using Infrastructure Composer’s visual and code editor, staging templates to S3 and applying stack updates.

In this demo lesson you'll learn how to edit an existing AWS CloudFormation template directly from the CloudFormation console using Infrastructure Composer (the visual Infrastructure as Code editor), validate the template, and update the stack. This walkthrough shows how to:

* Open the stack in the console and launch Infrastructure Composer
* Edit the template on the visual canvas or in the code view (YAML/JSON)
* Validate and transfer the edited template to S3 for CloudFormation to use
* Update the stack and confirm outputs

Why this matters: Infrastructure Composer streamlines template changes by combining a visual canvas with direct code editing and built-in validation—helpful for quick updates, minor fixes, or collaborating with teammates.

What you'll need:

* An existing CloudFormation stack you can update
* Appropriate IAM permissions to update stacks and create S3 objects

When you select a stack and choose Update stack → Make changes → Edit in Infrastructure as Code (Infrastructure Composer), the console opens a visual canvas where you can inspect and modify resources and the template.

<Frame>
  <img alt="Screenshot of the AWS CloudFormation console on the &#x22;Update stack&#x22; page. It shows the &#x22;Prerequisite - Prepare template&#x22; options (Use existing template selected) and a step-by-step navigation sidebar." />
</Frame>

Infrastructure Composer provides:

* A zoomable canvas to visualize resource relationships
* A code (template) view to edit YAML or JSON directly
* Built-in validation to check syntax and basic schema before applying changes

Template example (YAML)
Below is the CloudFormation YAML that was loaded into Infrastructure Composer for this demo. It demonstrates common template sections: Mappings, Parameters, Conditions, Resources, and Outputs. This is the same template used in the walkthrough (outputs reflect the demo edits):

```yaml theme={null}
Mappings:
  DevMap:
    Arno:
      Field: Quality assurance
      Env: Testing/development
    Alice:
      Field: Backend developer
      Env: Production

Parameters:
  InputBucketName:
    Type: String
    Description: Please enter in your desired s3 bucket name
  InputDeveloperName:
    Type: String
    Description: Developer name
    AllowedValues:
      - Arno
      - Alice

Conditions:
  IsProd: !Equals
    - !FindInMap
      - DevMap
      - !Ref InputDeveloperName
      - Env
    - Production

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

Outputs:
  BucketArn:
    Description: ARN
    Value: !GetAtt MyS3Bucket.Arn

  DeveloperBucketLabel:
    Description: Developer name and bucket name
    Value: !Join
      - ' - '
      - - !Ref InputDeveloperName
        - !Ref InputBucketName
```

Editing and validation

* Switch to the template (code) view to make direct edits in YAML or to convert to JSON.
* Use the built-in validator before applying changes to ensure the template is syntactically correct.
* In the demo, output descriptions were simplified: BucketArn → "ARN" and DeveloperBucketLabel → "Developer name and bucket name".

If you prefer JSON, Infrastructure Composer can display the template in JSON view. Here is the equivalent snippet of the S3 bucket in JSON:

```json theme={null}
{
  "Resources": {
    "MyS3Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "PublicAccessBlockConfiguration": {
          "BlockPublicAcls": true,
          "BlockPublicPolicy": true,
          "IgnorePublicAcls": true,
          "RestrictPublicBuckets": true
        }
      }
    }
  },
  "Metadata": {}
}
```

When you’re done editing and validation passes, click Update template (or Continue) to move forward. Infrastructure Composer stages the edited template in an S3 transfer bucket so CloudFormation can access the artifact during the stack update.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation Infrastructure Composer showing a &#x22;Continue to CloudFormation&#x22; dialog that explains an S3 bucket (cf-templates-1tsn8nwbdamjj-us-east-2) will be created to hold the template. The dialog offers a field to change the transfer bucket name and buttons to cancel or confirm and continue to CloudFormation." />
</Frame>

> **lightbulb** Infrastructure Composer uploads the edited template to an Amazon S3 transfer bucket (created automatically) so AWS CloudFormation can use it for the update. You can change the transfer bucket name if needed, but keeping the default is usually simplest.

Continuing the update

* After confirming the transfer bucket, CloudFormation continues the update flow.
* The console will return you to the stack parameter step; existing parameter values are preserved unless you change them.
* Verify or change parameter values as needed before submitting the update.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Specify stack details&#x22; step showing parameters for InputBucketName (eden-kodekloud-bncv-bkt) and InputDeveloperName (Alice). The left sidebar shows CloudFormation navigation (Stacks, StackSets, Exports) and the bottom has Previous/Next buttons." />
</Frame>

Submit the update. CloudFormation will apply the changes—this usually takes a short time. Once complete, the stack status reflects the update result.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Stacks&#x22; console showing one stack named &#x22;DemoStack&#x22; with status &#x22;UPDATE_COMPLETE&#x22; and a creation timestamp. Action buttons like Delete, Update stack, Stack actions and Create stack are visible at the top." />
</Frame>

Verify outputs
Open the stack, switch to the Outputs tab, and confirm the updated descriptions and output values are present. In the demo you should see the updated BucketArn and the DeveloperBucketLabel that joins developer name and bucket name.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing the &#x22;DemoStack&#x22; Outputs tab. It lists outputs including a BucketArn (an S3 bucket ARN) and a DeveloperBucketLabel with the developer name and bucket name." />
</Frame>

Note on transfer S3 buckets
Because Infrastructure Composer stages edited templates in an S3 transfer bucket, you may see an extra template bucket in your S3 console (in addition to any buckets created by your stack). This is expected: Composer needs a place to store the template artifact handed off to CloudFormation.

<Frame>
  <img alt="Screenshot of the Amazon S3 console showing the &#x22;General purpose buckets&#x22; view. It lists three buckets in the US East (Ohio) us‑east‑2 region with their names, IAM Access Analyzer links, creation dates, and a &#x22;Create bucket&#x22; button." />
</Frame>

Reverting to the original template
If you need to restore the original template:

1. Choose Update stack → Replace current template → Upload a template file.
2. Provide the original template file. Uploading the original will reset the stack template to its previous contents.

Quick reference — CloudFormation template sections

| Section    | Purpose                                           | Example from demo                           |
| ---------- | ------------------------------------------------- | ------------------------------------------- |
| Mappings   | Static lookup data used by the template           | DevMap maps developer name to Env and Field |
| Parameters | Values supplied at stack create/update time       | InputBucketName, InputDeveloperName         |
| Conditions | Conditional logic that controls resource creation | IsProd condition based on mapping           |
| Resources  | Actual AWS resources created or updated           | MyS3Bucket (AWS::S3::Bucket)                |
| Outputs    | Values returned after stack operations            | BucketArn, DeveloperBucketLabel             |

Summary
Use Infrastructure Composer to visually edit templates or make direct code changes, validate the template, and let Composer stage the edited template to S3 for CloudFormation to use. Then continue the CloudFormation update flow to apply changes, confirm parameters, and verify outputs. This workflow is ideal for quick edits, iterative template tweaks, or using a visual canvas to understand resource relationships.

Links and references

* AWS CloudFormation documentation: [https://docs.aws.amazon.com/cloudformation/](https://docs.aws.amazon.com/cloudformation/)
* Amazon S3 documentation: [https://docs.aws.amazon.com/s3/](https://docs.aws.amazon.com/s3/)
* Learn more about Infrastructure as Code and CloudFormation in AWS learning resources.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/563043d1-772f-4d1f-a812-f0a96dafa94f/lesson/686268bf-2405-4257-91f6-71fadbc37032)
