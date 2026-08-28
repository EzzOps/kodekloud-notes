# Demo Creating a condition to differentiate environments

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/Demo-Creating-a-condition-to-differentiate-environments/page

Using CloudFormation mappings and conditions to create environment-specific resources, applying a production-only public-read S3 bucket policy based on developer selection.

In this lesson you'll learn how to use CloudFormation Conditions to create environment-specific resources. We build a small mapping that ties each developer to metadata (including their environment), then use the intrinsic functions !FindInMap and !Equals to determine whether the selected developer maps to "Production". Finally, we apply that condition so a public-read S3 bucket policy is created only for production.

Why this matters: using mappings and conditions in CloudFormation lets you control which resources are created based on input parameters and predefined rules — enabling safer, environment-specific deployments and reducing the risk of accidentally exposing resources in non-production environments.

Overview

* Map developer names to metadata that includes the environment.
* Accept the bucket name and developer name via template parameters at stack creation time.
* Use a Condition to detect whether the chosen developer is in Production.
* Create the S3 bucket for all environments, and add a public-read BucketPolicy only when the Condition evaluates to true.

<Callout icon="lightbulb">
  Conditions control whether specific resources or outputs are created. If a resource has a Condition and the condition evaluates to false, CloudFormation will not create that resource.
</Callout>

## Mapping and parameters

Define a Mappings block to store per-developer metadata (including the Env key) and add Parameters to accept the bucket name and developer name:

```yaml theme={null}
Mappings:
  DevMap:
    Arno:
      Field: "Quality assurance"
      Env: "Testing/development"
    Alice:
      Field: "Backend developer"
      Env: "Production"

Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

  InputDeveloperName:
    Type: String
    Description: Select the developer/environment to use for this stack
    AllowedValues:
      - Arno
      - Alice
```

This mapping lets the template look up the Env value for the selected InputDeveloperName using !FindInMap.

Parameters reference table

| Parameter          | Type   | Purpose                                                      |
| ------------------ | ------ | ------------------------------------------------------------ |
| InputBucketName    | String | The S3 bucket name to create                                 |
| InputDeveloperName | String | Choose which developer mapping to use (controls environment) |

## Define the Condition

Add a Conditions block that sets IsProd to true only when the mapped Env equals "Production". This uses !FindInMap to look up the Env value and !Equals to compare it:

```yaml theme={null}
Conditions:
  IsProd: !Equals
    - !FindInMap [DevMap, !Ref InputDeveloperName, Env]
    - "Production"
```

How this works:

* !FindInMap \[DevMap, !Ref InputDeveloperName, Env] — fetches the Env value for the provided developer (for example, "Production" or "Testing/development").
* !Equals \[value1, value2] — returns true only when both values match exactly. Here, IsProd becomes true only when the mapped Env is "Production".

## Resources

Create an S3 bucket for every deployment, tag it with Developer and Environment, and create a BucketPolicy resource that only gets created when `IsProd` evaluates to true.

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: !Ref InputDeveloperName
        - Key: Environment
          Value: !FindInMap [DevMap, !Ref InputDeveloperName, Env]

  MyPublicReadPolicy:
    Type: AWS::S3::BucketPolicy
    Condition: IsProd
    Properties:
      Bucket: !Ref InputBucketName
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: PublicReadForGetBucketObjects
            Effect: Allow
            Principal: "*" 
            Action:
              - "s3:GetObject"
            Resource:
              - !Sub "arn:aws:s3:::${InputBucketName}/*"
```

Resource summary table

| Resource logical ID | Type                  | Created when                                                      |
| ------------------- | --------------------- | ----------------------------------------------------------------- |
| MyS3Bucket          | AWS::S3::Bucket       | Always (for any selected developer)                               |
| MyPublicReadPolicy  | AWS::S3::BucketPolicy | Only when `IsProd` evaluates to true (mapped Env == "Production") |

Notes on the policy:

* The `Condition: IsProd` property on the BucketPolicy resource ensures CloudFormation creates the policy only for production mappings.
* The policy allows public read access (s3:GetObject) to all objects in the bucket. Only enable public read where it matches your security and compliance requirements.

<Callout icon="warning">
  Be careful when making S3 buckets publicly readable. Ensure this matches your security requirements and compliance policies before enabling public access.
</Callout>

## Summary

* Use a Mappings block (DevMap) to store developer metadata including Env.
* Collect user input with Parameters for bucket name and developer selection.
* Use a Conditions block to define `IsProd` by combining !FindInMap and !Equals to test for "Production".
* Apply the condition to the BucketPolicy resource so the public-read policy is created only when the selected developer maps to Production.

This pattern allows you to control resource creation based on input parameters and mappings, helping enforce environment-specific behavior in CloudFormation templates.

Links and references

* [AWS CloudFormation — Conditions](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html)
* [AWS CloudFormation — Intrinsic Functions (!FindInMap, !Equals)](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference.html)
* [Amazon S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/3853c6e2-6fc2-4cae-95db-f847eeb51aee" />
</CardGroup>
