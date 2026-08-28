# Demo Using Sub dynamically with parameters

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/Demo-Using-Sub-dynamically-with-parameters/page

Using CloudFormation !Sub to inject parameters into ARNs and strings for reusable environment agnostic templates and partition portability with AWS partition and cfn lint guidance

This article demonstrates how to use the CloudFormation `!Sub` substitution function to inject parameter values into ARNs and other strings, avoiding hard-coded resource names. Using `!Sub` makes templates reusable, easier to manage across environments, and helps eliminate brittle string literals.

## Why use `!Sub` instead of hard-coded names

* Keeps templates environment-agnostic and reusable.
* Lets you supply values at stack creation time via Parameters.
* Reduces copy/paste errors when reusing templates across accounts, regions, or partitions.

## Example: Hard-coded bucket name

Here is an example policy where the bucket name is hard-coded inside the ARN:

```yaml theme={null}
Resources:
  MyPublicReadPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref InputBucketName
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: "*"
            Action: "s3:GetObject"
            Resource: "arn:aws:s3:::eden-kodekloud-bncv-bkt/*"
```

The `eden-kodekloud-bncv-bkt` segment is fixed in the template. To make this template parameter-driven, replace the literal bucket name in the ARN with a `!Sub` expression that references a parameter.

## Dynamic resource ARN with `!Sub`

Use `!Sub` with a placeholder like `${InputBucketName}`. You can keep the `Bucket` property as `!Ref` (or use `!Sub` there as well). This example keeps `Bucket: !Ref` and uses `!Sub` only in the ARN:

```yaml theme={null}
Resources:
  MyPublicReadPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref InputBucketName
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: "*"
            Action: "s3:GetObject"
            Resource: !Sub "arn:aws:s3:::${InputBucketName}/*"
```

Now the `${InputBucketName}` placeholder is replaced with the value provided to the `InputBucketName` parameter when the stack is created.

## Parameters and mappings (example)

Below is an example `Mappings` and `Parameters` section that pairs a bucket parameter with a developer selection. This demonstrates how `!Sub` works together with template inputs:

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
    Description: "Please enter your desired S3 bucket name"

  InputDeveloperName:
    Type: String
    Description: "Select the developer"
    AllowedValues:
      - Arno
      - Alice
```

<Callout icon="lightbulb">
  Using `!Sub` improves template readability and reusability. You can reference parameters in any string or ARN using the same `${ParamName}` pattern, and the substitution happens at deploy time.
</Callout>

## cfn-lint warning about hard-coded partition

Tooling like [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) may warn about a hard-coded partition when an ARN includes `arn:aws:...`. That literal uses the `aws` partition and reduces portability if you plan to deploy to specialized partitions (for example, `aws-us-gov` or `aws-cn`).

To make an ARN partition-agnostic, include the `AWS::Partition` pseudo parameter inside `!Sub`:

```yaml theme={null}
Resources:
  MyPublicReadPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref InputBucketName
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: "*"
            Action: "s3:GetObject"
            Resource: !Sub "arn:${AWS::Partition}:s3:::${InputBucketName}/*"
```

This ensures the partition (`aws`, `aws-cn`, `aws-us-gov`, etc.) is chosen automatically based on where the stack is deployed.

<Callout icon="warning">
  If you do not plan to deploy to AWS GovCloud or China partitions, keeping `arn:aws:s3:::` is acceptable in many cases. Use `${AWS::Partition}` when you need true portability across partitions.
</Callout>

## Linter severities (quick reference)

| Severity         | Meaning                                     | Action                         |
| ---------------- | ------------------------------------------- | ------------------------------ |
| Red (Error)      | Will prevent deployment                     | Fix immediately                |
| Yellow (Warning) | Likely a configuration or portability issue | Evaluate and address as needed |
| Blue / Info      | Best-practice suggestion                    | Optional; follow if applicable |

## Best practices & checklist

* Replace hard-coded resource names in ARNs with `!Sub` and `${ParameterName}` to support parameterized deployments.
* Use `AWS::Partition` inside `!Sub` if you require portability across AWS partitions.
* Prefer `!Sub` for any string that includes parameters or pseudo parameters (for example, `AWS::AccountId`, `AWS::Region`, `AWS::Partition`).
* Keep `Bucket: !Ref InputBucketName` (or `Bucket: !Sub "${InputBucketName}"`) and use `!Sub` only where interpolation is required.
* Run `cfn-lint` to catch portability and formatting issues, and apply linter guidance based on your deployment targets.

## Summary

* Use `!Sub` with `${ParameterName}` to inject parameter values into ARNs and other strings.
* Add `${AWS::Partition}` inside `!Sub` when cross-partition portability is needed.
* Treat `cfn-lint` messages as guidance: prioritize errors, evaluate warnings, and apply best-practice suggestions where beneficial.

## Links and references

* [AWS CloudFormation pseudo parameters — AWS::Partition](https://docs.aws.amazon.[SECRET_REDACTED]-parameter-reference.html#cfn-pseudo-param-partition)
* [cfn-lint GitHub repository](https://github.com/aws-cloudformation/cfn-lint)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/5aa2ca92-da6c-439d-9c7f-ae7b176d59c8" />
</CardGroup>
