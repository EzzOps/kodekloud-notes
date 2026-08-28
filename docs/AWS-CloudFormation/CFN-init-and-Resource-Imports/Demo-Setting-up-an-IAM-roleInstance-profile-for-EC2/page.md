# Ensure the helper scripts are present; then run cfn-init
/opt/aws/bin/cfn-init -v --stack <STACK_NAME> --resource MyInstance --region <REGION>

# Signal the stack that initialization finished (use return code from cfn-init)
/opt/aws/bin/cfn-signal -e $? --stack <STACK_NAME> --resource MyInstance --region <REGION>
```

Notes on cfn-hup

* cfn-hup is a daemon that polls CloudFormation for metadata changes. When it detects changes, it can invoke configured hooks to re-run cfn-init or other commands to apply updates.
* To use cfn-hup you must:
  * Configure its .conf and .hooks files (these are often created by cfn-init).
  * Ensure the instance role has permission to call CloudFormation APIs.
* cfn-hup is optional but useful when you want instances to pick up metadata changes without replacing or manually updating instances.

Summary

* cfn-init automates instance bootstrapping using AWS::CloudFormation::Init metadata in your CloudFormation template.
* Pair cfn-init with cfn-signal for lifecycle signaling and with cfn-hup for dynamic metadata updates.
* Verify helper scripts (aws-cfn-bootstrap) are installed on your AMI and that IAM permissions for S3 and CloudFormation are in place.

Links and References

* [AWS CloudFormation init (cfn-init)](https://docs.aws.amazon.[SECRET_REDACTED]-init.html)
* [cfn-hup daemon](https://docs.aws.amazon.[SECRET_REDACTED]-hup.html)
* [cfn-signal reference](https://docs.aws.amazon.[SECRET_REDACTED]-signal.html)
* [CloudFormation helper scripts (aws-cfn-bootstrap)](https://docs.aws.amazon.[SECRET_REDACTED]-helper-scripts-reference.html)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
* [Amazon EC2 Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/026ceaf9-07b6-4964-b49d-7190c136ea2b/lesson/f491e815-3d1b-4ed8-8d92-df381b726899" />
</CardGroup>


# Demo Setting up an IAM roleInstance profile for EC2

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CFN-init-and-Resource-Imports/Demo-Setting-up-an-IAM-roleInstance-profile-for-EC2/page

Guide to creating an IAM role and instance profile so EC2 instances can run cfn-init and retrieve CloudFormation metadata and configuration.

In this demo you'll learn how to create an IAM role and instance profile so an EC2 instance running cfn-init can retrieve CloudFormation stack metadata and configuration. This is a short, practical guide covering why the role is needed, what permissions to attach, and how to create the role using the AWS Console.

Why this matters

* cfn-init runs on the EC2 instance and must call CloudFormation APIs to fetch metadata and configuration.
* EC2 instances cannot store IAM credentials directly. Instead, an instance assumes an IAM role that is associated with the instance through an instance profile.
* Without the correct IAM role/instance profile, cfn-init will not be able to retrieve configuration data and therefore cannot install or configure software as defined in your CloudFormation template.

What we’ll create

* An IAM role trusted by the EC2 service (ec2.amazonaws.com).
* A permissions policy allowing read access to CloudFormation stack metadata (AWSCloudFormationReadOnlyAccess).
* (Console note) The AWS Console creates a matching instance profile for the role automatically. If you use CloudFormation or the CLI to create your role, you might need to create an AWS::IAM::InstanceProfile resource explicitly.

Step-by-step (Console)

1. Open the IAM console, choose Roles → Create role. Select the trusted entity type "AWS service" and choose EC2 as the use case.

<Frame>
  <img alt="A screenshot of the AWS IAM &#x22;Create role&#x22; page on the &#x22;Select trusted entity&#x22; step, with the &#x22;AWS service&#x22; option selected among other choices like AWS account, Web identity, and SAML 2.0. The browser window and system taskbar are also visible." />
</Frame>

2. Click Next to open the Permissions step. For cfn-init’s typical needs, attach the managed policy AWSCloudFormationReadOnlyAccess so the instance can read stack metadata from CloudFormation.

<Frame>
  <img alt="A screenshot of the AWS IAM &#x22;Create role&#x22; console focused on the &#x22;Permissions policies&#x22; step, showing a search for &#x22;AWSCloudF&#x22; and two matching AWS-managed policies: AWSCloudFormationFullAccess and AWSCloudFormationReadOnlyAccess. The UI includes navigation steps, filter options, and Next/Previous buttons." />
</Frame>

3. Click Next, then give the role a descriptive name (for example: MyCFN or MyCFNInstanceRole) and an optional description. Click Create role.

<Frame>
  <img alt="A screenshot of the AWS IAM console on the &#x22;Create role&#x22; page showing Role details with the role name &#x22;MyCFN&#x22; and a description that says &#x22;Allows EC2 instances to call AWS services on your behalf.&#x22; The left sidebar highlights Step 3: &#x22;Name, review, and create.&#x22;" />
</Frame>

4. After creation, verify the success message and note the exact role name. You will reference this role when attaching it to EC2 instances (via the console, API, or CloudFormation).

<Frame>
  <img alt="A browser screenshot of the AWS Identity and Access Management (IAM) console on the Roles page showing a green success banner &#x22;Role MyCFNInstanceRole created.&#x22; The main panel highlights &#x22;Roles Anywhere&#x22; features like accessing AWS from non-AWS workloads, X.509 standard, and temporary credentials." />
</Frame>

Quick reference

| Item             | Purpose                              | Example                          |
| ---------------- | ------------------------------------ | -------------------------------- |
| Trusted entity   | Allows EC2 to assume the role        | ec2.amazonaws.com                |
| Managed policy   | Grants CloudFormation read access    | AWSCloudFormationReadOnlyAccess  |
| Role name        | Reference when attaching to instance | MyCFNInstanceRole                |
| Instance profile | Allows EC2 to use the role           | Created automatically by Console |

Notes and common additions

<Callout icon="lightbulb">
  The AWS Console will create an instance profile with the same name as the role automatically when you create a role for [EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2). If you create roles programmatically or with [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation), you may need to create an AWS::IAM::InstanceProfile resource and associate the role explicitly.
</Callout>

<Callout icon="warning">
  AWSCloudFormationReadOnlyAccess allows cfn-init to read [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) metadata. If your cfn-init configuration needs to download artifacts from [S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) or access other AWS services, add the appropriate [S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) or service-specific permissions to the role (least-privilege principle recommended).
</Callout>

Conclusion

You now have an IAM role and instance profile that EC2 instances can assume for cfn-init to fetch CloudFormation metadata and perform instance setup. Keep the role name noted so you can attach it to your EC2 instance or reference it from your CloudFormation template.

Links and references

* [AWS Identity and Access Management (IAM)](https://learn.kodekloud.com/user/courses/aws-iam)
* [Amazon EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [Amazon S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/026ceaf9-07b6-4964-b49d-7190c136ea2b/lesson/a53f545e-59b4-470a-ac74-c42b24f7b7cc" />
</CardGroup>
