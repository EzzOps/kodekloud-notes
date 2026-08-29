# Demo Using a CloudFormation template to provision a basic EC2 Instance

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/EC2-Instance-Setup-With-an-HTTP-Server/Demo-Using-a-CloudFormation-template-to-provision-a-basic-EC2-Instance/page

Guide to creating and deploying a minimal AWS CloudFormation template that provisions a basic EC2 t3.micro instance and validates it before stack creation

In this lesson you'll create a minimal AWS CloudFormation template that provisions a single EC2 instance. The goal is to demonstrate the bare minimum properties required to launch an instance, validate the template locally, and deploy it through the CloudFormation console.

Before you start, open the EC2 console in the AWS region you want to use. AMI IDs are region-specific, so for reproducibility while following this lesson it's easiest to use the same region shown in the screenshots because the AMI ID used below will only work in that region.

<Callout icon="lightbulb">
  AMI IDs are unique per region. If you change regions, find and use the matching AMI ID for that region (use the EC2 AMIs page to search by name).
</Callout>

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch an instance&#x22; page showing the Amazon Linux 2023 AMI details (architecture, AMI ID, publish date, username) on the left. On the right is a Summary panel with number of instances, virtual server type (t3.micro) and a &#x22;Launch instance&#x22; button." />
</Frame>

Keep that EC2 page open (or copy the AMI ID) because you will need the ImageId value when writing the CloudFormation template.

Create a new file named `ec2-instance.yaml` in your CloudFormation project (for example, open the project in Visual Studio Code).

If your project already contains other templates, you might have existing Mappings and Parameters. Below is a corrected, minimal example showing how Mappings and Parameters are structured. This example is optional and not required for the minimal EC2 template that follows:

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
    Description: "Developer name used for tagging"
    AllowedValues:
      - Arno
      - Alice
```

Key elements required in the minimal EC2 template:

* The top-level Resources block
* A logical resource name (here: MyInstance)
* Resource Type: `AWS::EC2::Instance`
* Required properties: `InstanceType` and `ImageId`

Table: Minimal CloudFormation resource elements for an EC2 instance

|    Element | Purpose                                     | Example                   |
| ---------: | ------------------------------------------- | ------------------------- |
|  Resources | Container for all stack resources           | `Resources:`              |
| Logical ID | Template-local name for the resource        | `MyInstance:`             |
|       Type | Resource type identifier                    | `AWS::EC2::Instance`      |
| Properties | Resource properties (required and optional) | `InstanceType`, `ImageId` |

Below is a minimal CloudFormation template that creates a `t3.micro` EC2 instance using a specific AMI ID (example AMI ID shown in the screenshot). Replace the `ImageId` value with the correct AMI ID for the region you are using.

```yaml theme={null}
AWSTemplateFormatVersion: '2010-09-09'
Description: "Minimal template to create an EC2 instance"

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0eb9d6fc9fab44d24
```

Save the file as `ec2-instance.yaml`.

Validate the template locally (recommended) with cfn-lint. If you have cfn-lint installed, run:

```bash theme={null}
cfn-lint ec2-instance.yaml
```

If cfn-lint reports no errors, the template is ready to upload to the CloudFormation console.

Now open the CloudFormation console and create a new stack. Choose to upload a local template file (select the `ec2-instance.yaml` you just saved) and proceed through the stack creation steps.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Create stack&#x22; console showing the &#x22;Prerequisite - Prepare template&#x22; and &#x22;Specify template&#x22; sections. It displays options like &#x22;Choose an existing template&#x22; or &#x22;Build from Infrastructure Composer&#x22; and template sources such as &#x22;Amazon S3 URL&#x22;, &#x22;Upload a template file&#x22;, and &#x22;Sync from Git&#x22;." />
</Frame>

When prompted, give the stack a name (for example, `demo-stack`) and continue with the default options. Because this minimal template does not define Parameters, the CloudFormation console will display "No parameters" on the Specify stack details step.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Create stack&#x22; page on the console, showing the &#x22;Specify stack details&#x22; step with a Stack name field containing &#x22;Demo&#x22;. The Parameters section below indicates &#x22;No parameters&#x22; defined in the template." />
</Frame>

Submit the stack creation. Monitor the CloudFormation Events tab to track resource creation progress. When the stack reaches `CREATE_COMPLETE`, open the EC2 console and view Instances to confirm the instance is running.

You should see the instance launched with the instance type and AMI/platform defined in the template. By default, CloudFormation places the instance into your account's default VPC and default security group unless you specify otherwise. If you want to control placement, add `SubnetId` or `AvailabilityZone` to the resource's Properties.

<Frame>
  <img alt="A screenshot of the AWS EC2 console Instances page (us-east-2) showing a single t3.micro instance in &#x22;Running&#x22; state with its status check listed as &#x22;Initializing.&#x22; The EC2 navigation sidebar and the Launch instances/Actions controls are visible." />
</Frame>

<Callout icon="warning">
  This minimal template does not configure SSH key pairs, security groups, or user data. For production or remote access, add a KeyName, security group rules, and UserData to install or configure software at launch. Leaving defaults may expose the instance to restricted access — always follow security best practices.
</Callout>

Next steps you can add to the template (optional):

* Add a KeyPair: `KeyName` property for SSH access.
* Create or reference Security Groups to allow HTTP/SSH traffic.
* Add `UserData` to bootstrap software (e.g., install and start a web server).
* Add Tags for cost allocation and resource identification.
* Specify `SubnetId` or `AvailabilityZone` to control placement.

Useful links and references:

* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [EC2 AMIs and Images - AWS Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
* [cfn-lint GitHub repository](https://github.com/aws-cloudformation/cfn-lint)

That's the simplest CloudFormation approach to provision a basic EC2 instance. From here you can extend the template to include keys, networking, user data, tags, and more to match your deployment requirements.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/e8be47ac-5e51-4463-8b8c-dc5552940b10/lesson/53bc8fd6-dcca-4e57-ab18-0b8c46f67e5f" />
</CardGroup>
