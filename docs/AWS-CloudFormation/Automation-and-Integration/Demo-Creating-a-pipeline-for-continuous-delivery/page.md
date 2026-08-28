# Validate CloudFormation template
aws cloudformation validate-template --template-body file://template.yaml

# Run cfn-lint
cfn-lint template.yaml
```

Deploy examples (using change sets)

* Create a change set:

```bash theme={null}
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name pipeline-change-set \
  --template-body file://template.yaml \
  --parameters ParameterKey=Env,ParameterValue=prod
```

* Execute the change set after review:

```bash theme={null}
aws cloudformation execute-change-set \
  --change-set-name pipeline-change-set \
  --stack-name my-stack
```

<Callout icon="lightbulb">
  CodePipeline supports native [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) actions such as "Create/Update Stack" and "Create Change Set". For advanced validation or parameter generation you can add CodeBuild or Lambda steps that call the CloudFormation API before applying changes.
</Callout>

Key benefits of combining CodePipeline with CloudFormation

* Automated, auditable deployments of infrastructure changes with versioned artifacts.
* Validation and test stages to catch errors before infrastructure is modified.
* Safe deployment patterns using change sets and manual approvals to reduce risk.
* Integration with IAM and CloudWatch for secure, monitored operations and safe rollbacks.

Best practices and recommended patterns

* Use change sets in pipelines to preview and review resource changes before execution.
* Keep templates modular (nested stacks or modules) and store artifacts in S3 with unique versions.
* Run cfn-lint and unit tests in a build stage (CodeBuild) to catch syntactic and semantic issues early.
* Add a manual approval stage for production deployments and use separate pipelines/environments for dev/staging/prod.
* Restrict pipeline service roles with least privilege to limit the blast radius of a compromised pipeline.

<Callout icon="warning">
  Ensure pipeline roles and CloudFormation execution roles have least-privilege IAM policies. Incorrect permissions can cause failed deployments or unintended privilege escalation. Also plan artifact retention and S3 bucket encryption to meet compliance requirements.
</Callout>

References and further reading

* [AWS CodePipeline documentation](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* [AWS CloudFormation documentation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* cfn-lint: [https://github.com/aws-cloudformation/cfn-lint](https://github.com/aws-cloudformation/cfn-lint)

This lesson covered how to model a CodePipeline that validates and deploys CloudFormation templates, along with practical tips: use change sets, store artifacts safely, add validation stages, and restrict IAM permissions to maintain secure, auditable continuous delivery.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/3ad06612-9246-4700-953b-662d3eace39b/lesson/95ed6012-aee2-4500-af82-099e53fba4f9" />
</CardGroup>


# Demo Creating a pipeline for continuous delivery

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Automation-and-Integration/Demo-Creating-a-pipeline-for-continuous-delivery/page

Guide to build a CodePipeline that deploys a CloudFormation template from S3 to provision an EC2 instance.

This walkthrough shows how to build a simple continuous-delivery pipeline that deploys a CloudFormation template stored in S3. The pipeline uses CodePipeline as the orchestrator and CloudFormation as the deploy provider. End result: CodePipeline pulls a ZIP artifact from S3, CloudFormation extracts the template inside the ZIP, and CloudFormation creates the resources (an EC2 instance in this demo).

What you'll do in this demo:

* Create an S3 bucket (with versioning enabled) to store CloudFormation artifacts.
* Upload a zipped CloudFormation template to S3.
* Create an IAM role CloudFormation can assume to provision resources.
* Create a CodePipeline that uses the S3 artifact as Source and CloudFormation as Deploy.
* Verify the resulting CloudFormation stack and EC2 instance.

Step-by-step details follow.

## 1 — Create an S3 bucket for pipeline artifacts

Create a dedicated bucket to hold CloudFormation templates/artifacts. CodePipeline benefits from object versioning so it can reference specific object versions for each release.

<Frame>
  <img alt="A screenshot of the AWS S3 &#x22;Create bucket&#x22; console showing the &#x22;General purpose&#x22; bucket type selected and a bucket name field filled with &#x22;eden-kodekloud-kjhl-templa&#x22;. The page also shows an option to copy settings from an existing bucket and a &#x22;Choose bucket&#x22; button." />
</Frame>

Enable versioning on the bucket before using it as a pipeline source.

<Frame>
  <img alt="A screenshot of the Amazon S3 &#x22;Create bucket&#x22; console showing the Bucket Versioning section with the &#x22;Enable&#x22; option selected. The Tags (optional) section is visible below along with the console header and navigation." />
</Frame>

After creating the bucket, open it and confirm it is empty (ready for upload).

<Frame>
  <img alt="A screenshot of the Amazon S3 console for the bucket &#x22;eden-kodekloud-kjhl-templates,&#x22; showing the Objects tab with a message saying there are no objects. The UI displays controls like Upload, Create folder, Actions, Copy S3 URI, and a search/filter field." />
</Frame>

## 2 — Prepare and upload the CloudFormation artifact

For this demo we use a minimal CloudFormation template that creates a single EC2 instance. Save this content as simple-ec2.yaml:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.small
      ImageId: ami-0eb9d6fc9fab44d24
```

Zip the template (for example: simple-ec2.zip). The pipeline Source artifact will be the ZIP file uploaded to S3.

<Frame>
  <img alt="A Windows File Explorer window in dark mode showing the &#x22;cf-project&#x22; folder. The right pane lists CloudFormation-related YAML/JSON files (e.g., simple-ec2, s3-bucket, cfn-init) while the left pane shows common folders and navigation." />
</Frame>

Upload the ZIP to your S3 bucket. After upload you should see the file listed, e.g. simple-ec2.zip.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing a successful upload to the bucket s3://eden-kodekloud-kjhl-templates. The file &#x22;simple-ec2.zip&#x22; (304.0 B) is listed in the Files and folders pane with status &#x22;Succeeded.&#x22;" />
</Frame>

## 3 — Create an IAM role CloudFormation can assume

CloudFormation needs an execution role to create resources on your behalf. Create an IAM role with a trust policy allowing CloudFormation to assume the role, and attach the required policies (for this demo we attach CloudFormation and EC2 full access).

Open IAM and create a new role:

* Trusted entity: AWS service
* Use case: CloudFormation

<Frame>
  <img alt="A screenshot of the AWS IAM &#x22;Create role&#x22; page showing the Trusted entity type options with &#x22;AWS service&#x22; selected. The browser tabs and Windows taskbar are also visible." />
</Frame>

Proceed to Add permissions and attach the managed policies needed for CloudFormation to create EC2 instances (example policies: AWSCloudFormationFullAccess, AmazonEC2FullAccess).

<Frame>
  <img alt="A screenshot of the AWS IAM &#x22;Create role&#x22; console showing the &#x22;Use case&#x22; section with CloudFormation selected as the service/use case. The page shows the CloudFormation radio option, a dropdown for Service or use case, and Cancel/Next buttons." />
</Frame>

Search and select the appropriate managed policies.

<Frame>
  <img alt="A screenshot of the AWS IAM console on the &#x22;Create role&#x22; -> &#x22;Add permissions&#x22; step, showing the &#x22;Permissions policies&#x22; list with a search for &#x22;CloudFo&#x22; and several AWS-managed policies (like AWSCloudFormation) listed. The browser window and taskbar are visible at the top and bottom of the screen." />
</Frame>

Give the role a descriptive name (for example: PipelineForCFAndEC2) and an optional description. The role trust policy should allow CloudFormation to assume it; example trust policy:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudformation.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create the role when permissions and trust are configured.

<Frame>
  <img alt="A browser screenshot of the AWS Management Console showing the IAM &#x22;Create role&#x22; page where a role name &#x22;PipelineForCFAn...&#x22; is being entered and a description about CloudFormation is visible. The left panel shows the step progress (Select trusted entity → Add permissions → Name, review, and create)." />
</Frame>

## 4 — Create the CodePipeline

Open CodePipeline and create a new pipeline (use the wizard and select “Build a custom pipeline”). Choose a name (for example PipelineCF) and decide how to handle the service role (let CodePipeline create a service role or provide an existing role).

<Frame>
  <img alt="A screenshot of the AWS CodePipeline &#x22;Create new pipeline&#x22; page showing the Service role section with &#x22;New service role&#x22; selected and a role name filled in (AWSCodePipelineServiceRole-us-east-2-PipelineCF). The page also displays an option to let CodePipeline create the role, an &#x22;Advanced settings&#x22; panel, and navigation buttons (Previous, Next)." />
</Frame>

Configure pipeline stages:

* Source
  * Provider: Amazon S3
  * Bucket: the bucket you created
  * Object key: the S3 object key for simple-ec2.zip (the ZIP you uploaded)
* Skip Build and Test stages if not required
* Deploy
  * Provider: AWS CloudFormation
  * Region: the region where you want resources created (example: us-east-2)
  * Action mode: Create/Replace stack (or Create stack when creating a new stack)
  * Stack name: choose a name (e.g., DemoStackPipeline)
  * Template file: path inside the ZIP to the template (format: SourceArtifact::simple-ec2.yaml)
  * Role: choose the IAM role you created for CloudFormation (PipelineForCFAndEC2)

Specifying TemplatePath as SourceArtifact::simple-ec2.yaml instructs CloudFormation to extract simple-ec2.yaml from the source ZIP artifact and use it as the stack template.

When you review and create the pipeline, CodePipeline will automatically start the first release: it downloads the ZIP from S3, extracts the template, and triggers CloudFormation.

<Frame>
  <img alt="A screenshot of the AWS CodePipeline &#x22;Create new pipeline&#x22; confirmation screen showing pipeline details: StackName &#x22;DemoStackPipeline&#x22;, TemplatePath &#x22;SourceArtifact::simple-ec2.yaml&#x22;, the IAM Role ARN, automatic rollback enabled and automatic retry disabled. The browser and Windows taskbar are visible around the console." />
</Frame>

Monitor the pipeline execution in CodePipeline. Both Source and Deploy stages should show success if everything is configured correctly.

<Frame>
  <img alt="A screenshot of the AWS CodePipeline console showing a pipeline named &#x22;PipelineCF&#x22; with Source and Deploy stages (both actions succeeded). The top bar shows controls like Edit, Stop execution, Create trigger, Clone pipeline and an orange &#x22;Release change&#x22; button." />
</Frame>

## 5 — Verify the deployment

* Open CloudFormation and confirm the stack listed with the Stack name you specified.
* Open EC2 and verify an instance exists and is in the running state, matching the properties in simple-ec2.yaml.

If the pipeline completed successfully and CloudFormation created the stack and EC2 instance, the end-to-end pipeline is functioning: CodePipeline pulled the ZIP from S3, CloudFormation used the template inside the ZIP, and resources were provisioned.

## Quick reference: AWS resources used

| Resource       | Purpose                                                   | Example/Notes                                                     |
| -------------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| S3 bucket      | Store zipped CloudFormation templates/artifacts           | Enable versioning for Source artifact tracking                    |
| IAM role       | CloudFormation execution role (assumed by CloudFormation) | Attach AWSCloudFormationFullAccess and AmazonEC2FullAccess (demo) |
| CodePipeline   | Orchestrates Source → (Build) → Deploy stages             | Source: Amazon S3; Deploy: CloudFormation                         |
| CloudFormation | Creates and manages the stack/resources                   | Template path: SourceArtifact::simple-ec2.yaml                    |

## Tips and troubleshooting

* Ensure S3 bucket versioning is enabled so CodePipeline can reference object versions reliably.
* Confirm the Template file path inside the ZIP matches the TemplatePath you configure in CodePipeline (format: SourceArtifact::file.yaml).
* If stack creation fails, check CloudFormation events and logs for missing permissions or invalid parameters.

<Callout icon="lightbulb">
  Enable S3 bucket versioning before using the bucket as a pipeline source so CodePipeline can reference and track specific object versions.
</Callout>

<Callout icon="warning">
  AMI IDs (ImageId) are region-specific. If the AMI in the template is not available in your target region, the CloudFormation stack will fail. Use a region-appropriate AMI or implement a parameterized AMI lookup.
</Callout>

## Links and references

* [AWS CloudFormation User Guide](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [AWS CodePipeline User Guide](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Amazon S3 Versioning](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY].html)
* [IAM Roles for Amazon CloudFormation](https://docs.aws.amazon.com/[AWS_SECRET_ACCESS_KEY]-iam-template.html)

That’s it — you now have a continuous-delivery pipeline that deploys a CloudFormation template stored in S3.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/3ad06612-9246-4700-953b-662d3eace39b/lesson/8da48c60-b5e8-4429-983c-1feb9daac8e4" />
</CardGroup>
