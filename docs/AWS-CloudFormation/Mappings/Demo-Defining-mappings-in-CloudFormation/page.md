# Demo Defining mappings in CloudFormation

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Mappings/Demo-Defining-mappings-in-CloudFormation/page

Guide demonstrating how to define and use CloudFormation mappings with !FindInMap for static lookups, examples, and best practices for maintainable templates

Welcome to this demo on defining mappings in AWS CloudFormation. In this lesson you'll learn what mappings are, why they matter, and how to declare and reference them using Fn::FindInMap (the short form: !FindInMap). Mappings are ideal for storing fixed lookup tables and other static configuration values so you don't hard-code them across your template.

Mappings store static key-value pairs inside a CloudFormation template and provide a deterministic lookup mechanism. Use them for environment-specific values, region-specific AMI IDs, or any configuration that varies by a known key but remains static for a given deployment.

Below is an example template that defines two input Parameters and a Mappings block. The mapping keys correspond to the allowed values for the InputDeveloperName parameter.

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name
  InputDeveloperName:
    Type: String
    AllowedValues:
      - Arno
      - Alice

Mappings:
  DevMap:
    Arno:
      Field: "Quality Assurance"
    Alice:
      Field: "Backend Developer"

Resources:
  # Your resources go here
```

How this works:

* Place the Mappings section near the top of the template (it’s common to declare Parameters and Mappings before Resources for readability).
* Give the mapping a name (in this example: DevMap).
* Under that name, define top-level keys (here: Arno and Alice).
* For each key, include one or more named values (here: Field with a string value).
* Because the mapping keys match the allowed parameter values for InputDeveloperName, you can reference the mapping based on the selected parameter value.

Example: injecting a mapped value into a resource property

```yaml theme={null}
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: DeveloperRole
          Value: !FindInMap [ DevMap, !Ref InputDeveloperName, Field ]
```

In this example, the Tag DeveloperRole will be set to the Field value mapped to the provided InputDeveloperName (either "Quality Assurance" or "Backend Developer").

Best practices and tips:

* Use mappings for static configuration (region, environment, role, AMI IDs) to keep templates DRY and easier to maintain.
* Keep mapping keys synchronized with Parameter AllowedValues when you want controlled, predictable lookups.
* Prefer !FindInMap for lookups instead of long conditionals or repeated parameters.

| Feature    | Use case                                                       | Example                                       |
| ---------- | -------------------------------------------------------------- | --------------------------------------------- |
| Mappings   | Static lookups keyed by known values                           | Region-to-AMI mapping, developer role lookup  |
| Parameters | User-supplied inputs or constrained values                     | Bucket names, allowed developer names         |
| Conditions | Deploy resources conditionally based on parameters or mappings | Create resources only in certain environments |

<Callout icon="lightbulb">
  If you run cfn-lint you may see a message like "Mapping 'DevMap' is defined but not used." This is expected until you reference the mapping with !FindInMap in your template. Running a dry validation (aws cloudformation validate-template) or using a lint rule that checks references can help confirm correct usage.
</Callout>

References and further reading:

* [AWS CloudFormation intrinsic functions: Fn::FindInMap](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference-findinmap.html)
* [CloudFormation template anatomy and best practices](https://docs.aws.amazon.[SECRET_REDACTED]-anatomy.html)
* [cfn-lint GitHub repository](https://github.com/aws-cloudformation/cfn-lint)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/4e0caf18-41ee-4499-8c83-b0dc280c537a/lesson/6064fecc-859b-4c11-99f3-15f7d54fea7d" />
</CardGroup>
