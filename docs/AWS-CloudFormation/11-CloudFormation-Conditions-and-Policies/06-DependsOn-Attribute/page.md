# DependsOn Attribute

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/DependsOn-Attribute/page

Explains AWS CloudFormation DependsOn attribute that enforces resource creation and deletion order, with a YAML example showing an S3 bucket and bucket policy dependency.

This lesson explains the AWS CloudFormation DependsOn attribute and shows a practical YAML example. DependsOn controls the creation and deletion order of resources when one resource must exist before another. Without it, CloudFormation may create resources in parallel, which can cause errors if a strict sequence is required.

<Frame>
  <img alt="A presentation slide titled &#x22;DependsOn Attribute.&#x22; It explains that DependsOn tells CloudFormation to create one resource only after another is fully created and thus controls creation order when resources rely on each other." />
</Frame>

What DependsOn does:

* Ensures one or more resources are created only after specified resources finish creation.
* Accepts either a single logical resource name or a list of logical names.
* Impacts deletion order because CloudFormation deletes resources in reverse creation order.
* Is useful when there is no direct reference relationship between dependent resources.

| Feature                | Behavior                                                                 | Example use case                                                                 |
| ---------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Accepts single or list | Use a string or an array of logical names                                | A bucket and multiple resources that must be created after it                    |
| Creation order control | Forces sequential creation where implicit dependencies are absent        | Linking a resource that relies on an external resource created in the same stack |
| Deletion order         | Resources are deleted in reverse order of creation                       | Prevents deleting a dependent resource before the resource it needs              |
| Implicit dependencies  | Referencing a resource (e.g., !Ref, !GetAtt) creates implicit dependency | Most property references already enforce ordering without DependsOn              |

For more details, see the AWS CloudFormation documentation:

* [AWS CloudFormation: Resource creation order and DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html)
* [AWS S3 documentation](https://docs.aws.amazon.com/s3/index.html)

Below is a simple CloudFormation YAML example that creates an S3 bucket and a bucket policy. The BucketPolicy resource uses DependsOn to ensure it is created only after the bucket exists.

```yaml theme={null}
Resources:
  MyBucket:
    Type: AWS::S3::Bucket

  BucketPolicy:
    Type: AWS::S3::BucketPolicy
    DependsOn: MyBucket
    Properties:
      Bucket: !Ref MyBucket
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: "*"
            Action: "s3:GetObject"
            Resource: !Sub "arn:aws:s3:::${MyBucket}/*"
```

Key points in the example:

* "MyBucket" and "BucketPolicy" are logical resource names in the same CloudFormation template.
* The Bucket property uses `!Ref` to reference the bucket name.
* The PolicyDocument grants the public principal (`"*"`) the `s3:GetObject` action for all objects in the bucket by using `!Sub` to construct the bucket ARN.

> **lightbulb** Note: CloudFormation automatically creates implicit dependencies when a resource is referenced (for example, using `!Ref` or `!GetAtt`). In many cases (including this example where `Bucket: !Ref MyBucket` is used), explicit DependsOn is unnecessary. Use DependsOn when you need to enforce ordering but there is no property reference or when you must control a precise creation/deletion sequence.

> **warning** Warning: Overusing DependsOn can make templates harder to maintain and slower to deploy because it forces sequential creation. Prefer implicit dependencies where possible. Use DependsOn sparingly—only when implicit references cannot express the required ordering.

Links and references

* [AWS CloudFormation documentation: DependsOn attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html)
* [AWS CloudFormation best practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/eed1ec00-2d5c-49f1-a5a8-0d4985ee7870)
