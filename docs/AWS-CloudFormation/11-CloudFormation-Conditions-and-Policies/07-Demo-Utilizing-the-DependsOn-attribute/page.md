# Demo Utilizing the DependsOn attribute

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/Demo-Utilizing-the-DependsOn-attribute/page

Explains using CloudFormation DependsOn to enforce resource creation order, illustrated with an S3 bucket and bucket policy, and discusses when to prefer implicit dependencies and avoid overuse.

In this lesson you'll learn how to use the CloudFormation `DependsOn` attribute to enforce an explicit creation order between resources. The sample template ensures a public-read bucket policy is attached only after the corresponding Amazon S3 bucket has been created. While CloudFormation usually infers correct ordering, explicit dependencies are required in some situations (for example, when a bucket policy references a bucket name supplied by a parameter or when using custom resources). Without `DependsOn`, you can see errors like "bucket does not exist" if the policy is applied before the bucket is available.

> **lightbulb** CloudFormation typically determines creation order automatically when resources reference each other using intrinsic functions (`!Ref`, `!GetAtt`, etc.). Use `DependsOn` only when that implicit dependency is insufficient—such as when a policy references a bucket by name or ARN built from parameters or strings.

Below is an example CloudFormation YAML template showing mappings, parameters, a condition to detect production, and the Resources section that includes an S3 bucket and a bucket policy. The bucket policy explicitly depends on the bucket to guarantee ordering.

Mappings and parameters used to customize the stack:

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

  InputDeveloperName:
    Type: String
```

Condition used to detect the production environment:

```yaml theme={null}
Conditions:
  IsProd: !Equals
    - !FindInMap [DevMap, !Ref InputDeveloperName, Env]
    - "Production"
```

Resources — S3 bucket and bucket policy. Note the logical ID `MyS3Bucket` is referenced by `DependsOn` in the bucket policy:

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

  MyS3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    DependsOn: MyS3Bucket
    Properties:
      Bucket: !Ref InputBucketName
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: PublicReadGetObject
            Effect: Allow
            Principal: "*"
            Action:
              - s3:GetObject
            Resource: !Sub "arn:aws:s3:::${InputBucketName}/*"
```

Why use `DependsOn` here?

* Implicit dependencies: CloudFormation infers ordering when a resource references another resource's logical ID via intrinsic functions (for example, `!Ref MyS3Bucket` or `!GetAtt MyS3Bucket`). In those cases, explicit `DependsOn` is not needed.
* When implicit links are missing: If both the bucket and the policy use the same parameter value (for example, `InputBucketName`) or a constructed ARN/string, CloudFormation may not infer a relationship between the resources. The policy can end up being created before the bucket. Adding `DependsOn: MyS3Bucket` ensures the bucket is created (or updated) first and prevents errors where the policy references a non-existent bucket.

> **warning** Avoid overusing `DependsOn`. Adding many explicit dependencies can unnecessarily serialize resource creation, making stack creations and updates slower. Also take care to avoid creating circular dependencies.

Quick reference table — template sections in this example:

| Template Section | Purpose                                  | Example                                                                          |
| ---------------- | ---------------------------------------- | -------------------------------------------------------------------------------- |
| Mappings         | Static lookups used by the template      | `DevMap` mapping for developer -> environment                                    |
| Parameters       | Values supplied when creating the stack  | `InputBucketName`, `InputDeveloperName`                                          |
| Conditions       | Conditional logic to detect environments | `IsProd` checks mapped environment equals "Production"                           |
| Resources        | The actual AWS resources created         | `MyS3Bucket` (S3 bucket) and `MyS3BucketPolicy` (Bucket policy with `DependsOn`) |

Best practice summary:

* Prefer implicit dependencies via intrinsic functions when possible.
* Use `DependsOn` when resources must be created in a strict order but do not have intrinsic references (e.g., resource name/ARN provided via a parameter).
* Keep dependency graphs simple to avoid long-running updates and circular references.

Links and references:

* [CloudFormation — Learn KodeKloud course](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [Amazon S3 — Learn KodeKloud course](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)

That’s the basic pattern: give the dependent resource a `DependsOn` attribute listing the logical name(s) of resources it must wait for. In this example, `MyS3BucketPolicy` will only be applied after `MyS3Bucket` has been successfully created.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/ecb4c447-e6e0-4e0f-80df-c024ff3a5fef)
