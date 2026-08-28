# Demo Setting default values and limit choices

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Parameters/Demo-Setting-default-values-and-limit-choices/page

Explains how to use AWS CloudFormation parameters to set defaults, validate input, restrict allowed values, and reference parameters in resources like S3 buckets

In this lesson you'll learn how to define CloudFormation Parameters to accept input, set sensible defaults, and constrain user choices. Parameters act as template inputs (form fields) and support validation through Type, Default, AllowedValues, and other properties. You'll also see how to reference parameters (with !Ref or Ref) inside resources such as an S3 bucket.

Parameters are useful for:

* Reusing templates across environments (dev/stage/prod).
* Pre-filling metadata like developer names or tags.
* Restricting choices to avoid invalid configurations.

Parameters overview

A parameter entry defines the input name, its Type, and optional validation and UI hints such as Description, Default, and AllowedValues. These fields enforce validation both in the console and when you run linting tools locally.

| Parameter field       | Purpose                                                                   | Example                                    |
| --------------------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| Type                  | Determines the input data type (String, Number, AWS-specific types, etc.) | `String`                                   |
| Description           | Help text shown in the console                                            | `Please enter your desired S3 bucket name` |
| Default               | A pre-filled value shown in the console                                   | `Arno Pretorius`                           |
| AllowedValues         | Restricts the parameter to a set of valid options                         | `- Arno Pretorius`<br />`- Alice`          |
| ConstraintDescription | Message shown when validation fails                                       | `Must be one of the allowed developers`    |

Useful references:

* [AWS CloudFormation parameters](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html)
* [CloudFormation intrinsic functions (!Ref, !Sub, etc.)](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference.html)
* [cfn-lint repository (template validation tool)](https://github.com/aws-cloudformation/cfn-lint)

Simple example — referencing a parameter in an S3 bucket

Below is a minimal template that defines a parameter for the S3 bucket name and uses it in the bucket resource via !Ref:

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
```

Setting a default value

Providing a Default value pre-fills the parameter in the CloudFormation console so users don't need to type the same metadata repeatedly. Defaults are especially handy for tags such as `Developer` or `Environment`.

Example: add a developer parameter with a Default and use it in the bucket Tags via !Ref.

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

  InputDeveloperName:
    Type: String
    Default: Arno Pretorius
    Description: Name of the developer

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: !Ref InputDeveloperName
        - Key: Environment
          Value: "Development"
```

Validate your template locally before uploading:

```bash theme={null}
cfn-lint s3-bucket.yaml
```

<Callout icon="lightbulb">
  Use cfn-lint to catch syntax errors, unsupported properties, or policy issues before deploying—this can save time and reduce failed stack updates.
</Callout>

When you upload this template and choose Update stack → Replace existing template, CloudFormation will show the parameters page with the Default value pre-filled. The Default will be used unless you overwrite it in the console.

<Frame>
  <img alt="Screenshot of the AWS CloudFormation &#x22;Specify stack details&#x22; page. It shows parameter fields with InputBucketName set to &#x22;eden-kodekloud-bncv-bkt&#x22; and InputDeveloperName set to &#x22;Arno.&#x22;" />
</Frame>

Limiting choices with AllowedValues

To present a curated set of options to users (for example, a list of developers or environments), use AllowedValues. The CloudFormation console renders a dropdown containing only the specified values.

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

  InputDeveloperName:
    Type: String
    AllowedValues:
      - Arno Pretorius
      - Alice
    Description: Choose the developer responsible for this stack

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: !Ref InputDeveloperName
        - Key: Environment
          Value: "Development"
```

<Callout icon="lightbulb">
  CloudFormation often displays the first AllowedValues entry as the initially-selected value in the dropdown. Be mindful of the ordering if you rely on which option is selected by default.
</Callout>

To update the stack with the modified template, choose Update stack → Replace existing template and upload the updated file.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Update stack&#x22; page showing the stepper on the left and the &#x22;Prerequisite - Prepare template&#x22; section in the center. The &#x22;Replace existing template&#x22; option is selected among choices to use or edit the stack template." />
</Frame>

After you select an AllowedValues entry and apply the update, CloudFormation passes that value to the parameter and the resource tags reflect the chosen developer. If the S3 console doesn't immediately show the updated tags, try a hard refresh of the page.

Summary — quick takeaways

* Default: pre-fills a parameter value in the CloudFormation console to simplify deployments.
* AllowedValues: restricts a parameter to a predefined set of valid choices and produces a dropdown in the console.
* Reference parameters in resources using !Ref (or other intrinsic functions) to populate properties such as BucketName or Tags.
* Validate templates locally with tools like cfn-lint before uploading.

Final example (parameters with AllowedValues and the referenced S3 resource):

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name

  InputDeveloperName:
    Type: String
    AllowedValues:
      - Arno Pretorius
      - Alice
    Description: Choose the developer responsible for this stack

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: !Ref InputDeveloperName
        - Key: Environment
          Value: "Development"
```

Further reading and references

* [AWS CloudFormation Parameters documentation](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html)
* [CloudFormation intrinsic functions](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference.html)
* [cfn-lint (YAML/JSON CloudFormation linter)](https://github.com/aws-cloudformation/cfn-lint)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/636db37e-4a51-4bb0-bcec-7ebf488a26b8/lesson/f2135bc2-3535-4a34-a93d-0856d7fc65d7" />
</CardGroup>
