# Short form (YAML)
!FindInMap [MappingName, TopLevelKey, SecondLevelKey]

# Long form (YAML explicit)
Fn::FindInMap:
  - MappingName
  - TopLevelKey
  - SecondLevelKey
```

Example: define a mapping and use FindInMap to pick an AMI based on region

```yaml theme={null}
AWSTemplateFormatVersion: '2010-09-09'
Description: Example of using Fn::FindInMap

Mappings:
  RegionMap:
    us-east-1:
      AMI: ami-0abcdef1234567890
      HVM: hvm
    us-west-2:
      AMI: ami-0fedcba9876543210
      HVM: hvm2

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      # Use the current region (pseudo parameter) to look up the AMI
      ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", AMI]
      InstanceType: t2.micro
```

Arguments summary

| Argument position  | Description                                                                                         | Example                           |
| ------------------ | --------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1 (MappingName)    | The name of the mapping under the template's Mappings section                                       | RegionMap                         |
| 2 (TopLevelKey)    | The top-level key (row) to select within the mapping. Can be a literal or an intrinsic (e.g., !Ref) | !Ref "AWS::Region" or "us-east-1" |
| 3 (SecondLevelKey) | The second-level key (column/label) identifying the specific value in the selected row              | AMI                               |

Tips and common patterns

* Use !Ref "AWS::Region" (or other intrinsics) as the TopLevelKey to select region-specific entries.
* Keys and values are literal strings and case-sensitive—ensure the mapping keys match exactly.
* You can nest other intrinsic functions inside the arguments (for example, !Ref, !FindInMap cannot call other mappings but can be used alongside other intrinsics in the same template).
* Fn::FindInMap fails the stack operation if the specified mapping, or keys, do not exist—validate your mappings and test with different regions.

<Callout icon="lightbulb">
  Mappings must be declared under the template's Mappings section. Fn::FindInMap performs a static lookup at stack create/update — mapping values are part of the template and not dynamically generated outside intrinsic functions.
</Callout>

Warning: common pitfalls

<Callout icon="warning">
  If a mapping name or key is missing or misspelled, CloudFormation will fail the stack operation. Remember that mapping keys are case-sensitive and must match exactly.
</Callout>

Quick reference (one-line)

```yaml theme={null}
!FindInMap [MappingName, TopLevelKey, SecondLevelKey]
```

Links and references

* [AWS CloudFormation Fn::FindInMap documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-findinmap.html)
* [CloudFormation Intrinsic Functions overview](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
* [AWS CloudFormation Mappings section](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/4e0caf18-41ee-4499-8c83-b0dc280c537a/lesson/745550ff-7de7-4a8f-a572-55f1707a43d7" />
</CardGroup>


# Demo Accessing our mapped values

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Mappings/Demo-Accessing-our-mapped-values/page

Shows how to use CloudFormation Mappings and !FindInMap to retrieve values and apply them to resource tags using an S3 bucket example with deployment and verification steps

In this lesson we'll learn how to retrieve values from a CloudFormation Mappings block using the !FindInMap intrinsic function. Mappings are useful for storing static lookup data (for example, environment-specific settings or role-to-profession mappings) and then referencing those values elsewhere in your template.

Mappings example

```yaml theme={null}
Mappings:
  DevMap:
    Arno:
      Field: Quality assurance
    Alice:
      Field: Backend developer
```

!FindInMap — the three parts

| Argument         | Purpose                                | Example       |
| ---------------- | -------------------------------------- | ------------- |
| Mapping name     | The Mappings block name to search      | DevMap        |
| Top-level key    | The first-level key inside the mapping | Arno or Alice |
| Second-level key | The nested key whose value you want    | Field         |

Using the mapping in a resource tag
Below is a simplified Resources snippet that adds tags to an S3 bucket. The Profession tag pulls its value from the mapping using !FindInMap.

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
          Value: "Development"
        - Key: Profession
          Value: !FindInMap [DevMap, "Arno", "Field"]

    Metadata:
      Purpose: "Creating an s3 bucket"
      Reviewed: "02-07-2025"
```

Notes on the example

* The !FindInMap invocation returns the value at Mappings → DevMap → Arno → Field, which is "Quality assurance".
* The Developer tag is populated from the InputDeveloperName parameter so the developer name appears in the S3 console; Profession is taken from the mapping instead of being hard-coded in the Tags list.
* You can make the top-level key dynamic (for example, by referencing a parameter instead of hard-coding "Arno") to select different mapped values at stack creation or update time.

<Callout icon="lightbulb">
  Putting the top-level key in quotes (for example, "Arno") is optional in YAML, but quoting can prevent parsing ambiguity and improve readability.
</Callout>

Full compact template
The compact template below combines Mappings, Parameters, and the S3 resource shown above—use this as a minimal working example.

```yaml theme={null}
Mappings:
  DevMap:
    Arno:
      Field: Quality assurance
    Alice:
      Field: Backend developer

Parameters:
  InputBucketName:
    Type: String
    Description: Please enter your desired S3 bucket name
  InputDeveloperName:
    Type: String
    Description: Please enter the developer name

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
        - Key: Profession
          Value: !FindInMap [DevMap, "Arno", "Field"]

Metadata:
  Purpose: "Creating an s3 bucket"
  Reviewed: "02-07-2025"
  Owner: "John Doe"
```

Redeploying the template
To update a stack with this template:

1. In the CloudFormation console choose Update stack → Replace current template → Upload a template file → Choose file.
2. Proceed to the Specify stack details page and fill parameters such as InputBucketName and InputDeveloperName.
3. Complete the update and wait for the stack update to finish.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console with a Windows file-open dialog overlaid, showing a &#x22;cf-project&#x22; folder and a selected &#x22;s3-bucket&#x22; YAML file. The browser window in the background displays the CloudFormation stack creation UI." />
</Frame>

On the Specify stack details page, set parameters such as InputBucketName and InputDeveloperName (for this demo we selected "Arno" for the developer).

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Specify stack details&#x22; page for updating a stack, showing parameters including InputBucketName set to &#x22;eden-kodekloud-bncv-bkt&#x22; and InputDeveloperName set to &#x22;Arno.&#x22; The left sidebar shows the multi-step progress with &#x22;Specify stack details&#x22; highlighted and navigation buttons (Previous, Next) appear at the bottom." />
</Frame>

Verifying the mapped value
After the stack update completes, open the S3 bucket in the S3 console and navigate to Properties → Tags to confirm the mapping was applied. In this example:

* Developer tag shows the parameter value "Arno".
* Profession tag shows "Quality assurance" (the value resolved from DevMap → Arno → Field).

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the properties/tags for a bucket (keys like Status: Active, aws:cloudformation:stack-name: DemoStack, Developer: Arno, Environment: Development). The &#x22;Profession&#x22; tag (&#x22;Quality assurance&#x22;) is highlighted." />
</Frame>

Summary

* !FindInMap requires three arguments: mapping name, top-level key, and second-level key.
* Use Mappings to centralize static lookup data and avoid duplication across your template.
* Combine Parameters and Mappings to let users control keys (top-level lookup) while still resolving other values from a central mapping.

Links and references

* [CloudFormation Overview](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [Intrinsic function: !FindInMap](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-findinmap.html)
* [Mappings section structure](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html)
* [Update a stack (CloudFormation)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/4e0caf18-41ee-4499-8c83-b0dc280c537a/lesson/33a30cb1-053c-4ff8-85af-dc29611dd90b" />
</CardGroup>
