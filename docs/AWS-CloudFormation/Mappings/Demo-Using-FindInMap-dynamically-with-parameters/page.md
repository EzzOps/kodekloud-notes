# Demo Using FindInMap dynamically with parameters

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Mappings/Demo-Using-FindInMap-dynamically-with-parameters/page

Demonstrates using AWS CloudFormation Mappings with FindInMap and Ref to dynamically set S3 bucket tags based on a selected parameter

This lesson demonstrates how to use CloudFormation Mappings together with nested intrinsic functions (!FindInMap and !Ref) so map keys can be selected dynamically based on a parameter. This pattern prevents hard-coded keys and lets resource properties (for example, S3 bucket tags) adapt to user input at stack creation or update time.

Overview

* Create a Mappings block (DevMap) that stores developer-specific metadata (profession and environment).
* Define Parameters for the S3 bucket name and the developer selection.
* Use !FindInMap together with !Ref to dynamically select mapping entries based on the chosen developer.
* Tag the S3 bucket with Developer, Environment and Profession values derived from the mapping.

<Callout icon="lightbulb">
  Ensure the top-level keys in Mappings (for example: Arno, Alice) exactly match the AllowedValues for the InputDeveloperName parameter (case-sensitive). The mapping keys are referenced dynamically via `!Ref InputDeveloperName`.
</Callout>

CloudFormation template example (clean, complete fragment)

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
    Description: "Select a developer"
    AllowedValues:
      - Arno
      - Alice

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Developer
          Value: !Ref InputDeveloperName
        - Key: Environment
          Value: !FindInMap [ DevMap, !Ref InputDeveloperName, Env ]
        - Key: Profession
          Value: !FindInMap [ DevMap, !Ref InputDeveloperName, Field ]
    Metadata:
      Purpose: "Creating an s3 bucket"
      Reviewed: "02-07-2025"
      Owner: "John Doe"
```

Why this works

* Mappings are static name/value pairs inside the template. They are ideal for mapping environment- or user-specific values without embedding conditional logic in many places.
* !Ref InputDeveloperName returns the parameter value selected by the user.
* !FindInMap accepts the mapping name, a top-level key (here provided by `!Ref InputDeveloperName`), and a sub-key to return the correct value.

Step-by-step explanation

1. Define a Mappings block (DevMap) with top-level keys for each developer (Arno, Alice). Each key contains attributes such as Field and Env.
2. Add an InputDeveloperName parameter constrained by AllowedValues to the same keys used in the mapping to ensure valid lookups.
3. In the resource tags:
   * Use `!Ref InputDeveloperName` to set the Developer tag directly.
   * Use `!FindInMap [ DevMap, !Ref InputDeveloperName, Env ]` to obtain the Environment value for the selected developer.
   * Use `!FindInMap [ DevMap, !Ref InputDeveloperName, Field ]` to obtain the Profession/Field value.
4. When the stack is updated with a different InputDeveloperName, CloudFormation evaluates `!Ref` and `!FindInMap` and applies the mapped values to the resource properties.

Quick mapping reference

| Developer | Env                 | Field             |
| --------- | ------------------- | ----------------- |
| Arno      | Testing/development | Quality assurance |
| Alice     | Production          | Backend developer |

Testing the template (update flow)

1. Update the existing stack in the CloudFormation console.
2. Choose "Make a direct update" and replace the template with the updated version above.
3. Set the parameters:
   * InputBucketName: your desired bucket name (e.g., eden-kodekloud-bncv-bkt)
   * InputDeveloperName: choose Arno or Alice
4. Submit the update. CloudFormation will apply tags derived from the mapping for the selected developer.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Stacks&#x22; console showing one stack named &#x22;DemoStack&#x22; with status &#x22;UPDATE_COMPLETE&#x22; and a timestamp. The &#x22;Update stack&#x22; dropdown is open, showing options to &#x22;Create a change set&#x22; or &#x22;Make a direct update.&#x22;" />
</Frame>

Select the template file and change the InputDeveloperName parameter to the desired value (for example, Arno or Alice), then submit the update.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Update stack&#x22; page showing form fields. The form shows InputBucketName set to &#x22;eden-kodekloud-bncv-bkt&#x22; and an InputDeveloperName dropdown listing &#x22;Arno&#x22; and &#x22;Alice.&#x22;" />
</Frame>

Validate the result: inspect the S3 bucket properties and check the Tags section. You should see:

* Developer: the selected parameter (Alice or Arno)
* Environment: value from the mapping via `!FindInMap`
* Profession: value from the mapping via `!FindInMap`

For example, choosing Arno will result in Environment = Testing/development and Profession = Quality assurance.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the properties for a bucket named &#x22;eden-kodekloud-bncv-bkt.&#x22; It lists metadata such as Status: Active, aws:cloudformation:stack-name: DemoStack, Developer: Arno, and Environment: Testing/development." />
</Frame>

Best practices and gotchas

* Keep mapping keys and AllowedValues synchronized and case-sensitive.
* Use Mappings for static cross-environment or per-user values; use Parameters for values you expect to change per deploy.
* Avoid duplicating values across the template—centralize them in Mappings to make maintenance easier.

Links and References

* [AWS CloudFormation Mappings documentation](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [AWS CloudFormation intrinsic functions reference](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference.html)
* [AWS S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)

Summary

* Use `!FindInMap` combined with `!Ref` to select mapping values dynamically based on parameters.
* This approach avoids hard-coding and centralizes environment- or user-specific configuration in one place.
* Always ensure mapping keys exactly match the parameter AllowedValues to prevent lookup failures.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/4e0caf18-41ee-4499-8c83-b0dc280c537a/lesson/054a5779-4cce-4b65-9c8d-cf52ac7bdec9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/4e0caf18-41ee-4499-8c83-b0dc280c537a/lesson/978f4cf6-66c9-4d8b-b7f0-f87f39188816" />
</CardGroup>
