# Demo Applying a condition to a public read policy

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/Demo-Applying-a-condition-to-a-public-read-policy/page

Explains adding a CloudFormation Condition to attach a public-read S3 bucket policy only when deployment environment is Production, omitting it for Development and Test

In this lesson we add a Condition to a CloudFormation stack so a public-read S3 bucket policy is applied only when the stack is deployed for Production. The objective is simple: allow objects to be publicly readable only when the environment resolves to "Production" and omit the policy for Development or Test deployments.

Below is a minimal, clear CloudFormation template that defines parameters, a mapping used to derive each developer's environment, a Condition that checks for Production, and two resources: an S3 bucket and a bucket policy that is only created when the condition evaluates to true.

CloudFormation template

```yaml theme={null}
AWSTemplateFormatVersion: "2010-09-09"

Parameters:
  InputDeveloperName:
    Type: String
    AllowedValues:
      - Arno
      - Alice
    Description: "Developer name used to look up the environment."

  InputBucketName:
    Type: String
    Description: "Name of the S3 bucket to attach the policy to."

Mappings:
  DevMap:
    Arno:
      Env: "Production"
    Alice:
      Env: "Development"

Conditions:
  IsProd: !Equals
    - !FindInMap [DevMap, !Ref InputDeveloperName, Env]
    - "Production"

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName

  MyPublicReadPolicy:
    Condition: IsProd
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref InputBucketName
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: "PublicReadForProduction"
            Effect: Allow
            Principal: "*" 
            Action: "s3:GetObject"
            Resource: !Sub "arn:aws:s3:::${InputBucketName}/*"
```

How it works (step‑by‑step)

* Parameters
  * InputDeveloperName: selects the developer key used to look up the environment in the mapping.
  * InputBucketName: the target bucket name that both the bucket resource and the policy reference.
* Mapping
  * DevMap associates developer names with an Env value. In this example, Arno → Production, Alice → Development.
* Condition
  * IsProd uses FindInMap to fetch the Env for the selected developer and Equals to check if it is "Production".
* Resources and Condition behavior
  * MyS3Bucket: always created with the provided InputBucketName.
  * MyPublicReadPolicy: annotated with Condition: IsProd so CloudFormation only creates this bucket policy when IsProd evaluates to true. If false, the resource is not created at all.

Resources and purpose

| Resource Type         | Purpose                                     | Example / Notes                          |
| --------------------- | ------------------------------------------- | ---------------------------------------- |
| Parameter             | Choose developer to map to environment      | `InputDeveloperName` (Arno, Alice)       |
| Mapping               | Map developer → environment                 | `DevMap` (Arno: Production)              |
| Condition             | Check if resolved environment is Production | `IsProd`                                 |
| AWS::S3::Bucket       | Create the bucket                           | `MyS3Bucket`                             |
| AWS::S3::BucketPolicy | Grant public-read when Production           | `MyPublicReadPolicy` (Condition: IsProd) |

Deployment examples

* Deploy for Production (Arno):

```bash theme={null}
aws cloudformation create-stack \
  --stack-name demo-prod-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=InputDeveloperName,ParameterValue=Arno ParameterKey=InputBucketName,ParameterValue=my-prod-bucket
```

* Deploy for Development (Alice) — policy will NOT be created:

```bash theme={null}
aws cloudformation create-stack \
  --stack-name demo-dev-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=InputDeveloperName,ParameterValue=Alice ParameterKey=InputBucketName,ParameterValue=my-dev-bucket
```

Security and operational considerations

* The bucket policy in this example grants `s3:GetObject` to Principal `"*"`, making objects publicly readable. Only apply this to buckets you explicitly intend to expose.
* Account-level or bucket-level S3 Block Public Access settings can override bucket policies and prevent public access even when a policy allows it. Verify Block Public Access settings if you expect objects to be public.
* Using a resource-level Condition is often safer than creating a resource and attempting to toggle its permissions at runtime.

> **lightbulb** Using a resource-level Condition means the resource is not created if the condition is false. This is safer than creating the resource and trying to toggle its permissions at runtime.

> **warning** Be cautious: public-read policies can expose sensitive data. Confirm that the bucket contains only intended public assets and that logging, monitoring, and lifecycle policies are in place.

References and further reading

* AWS CloudFormation Conditions: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html)
* S3 Bucket Policy examples: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
* Amazon S3 Block Public Access: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/block-public-access.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/block-public-access.html)

Keep in mind

* You can safely include conditional resources in stacks you frequently deploy to non-production environments: when the condition is false, CloudFormation simply omits the resource.
* Confirm that your mapping keys (e.g., developer names) and parameter values are always kept in sync so the Condition resolves deterministically.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/a16e051a-1051-4dc1-8721-e4b0f25d3645)
