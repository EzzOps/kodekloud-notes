# Demo Working with CFN init scripting Part 1

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CFN-init-and-Resource-Imports/Demo-Working-with-CFN-init-scripting-Part-1/page

Guide explaining how to use CloudFormation cfn-init and UserData to configure EC2 instances, install packages, enable services, and provide a minimal example template.

In this lesson you'll learn how to use CloudFormation's cfn-init helper to configure an EC2 instance (install packages, enable services, etc.) by:

* Declaring AWS::CloudFormation::Init metadata in your template, and
* Invoking cfn-init from the instance UserData during boot.

Below I walk through the essential pieces (metadata, parameters, security group, UserData) and then provide a complete, minimal CloudFormation YAML example that combines them.

> **lightbulb** Make sure the EC2 instance has an IAM instance profile that gives it permission to read stack metadata (this is typically an Instance Profile containing an IAM role you created earlier).

## How cfn-init works (high level)

* The template embeds configuration instructions under the resource's `Metadata` → `AWS::CloudFormation::Init` section.
* On instance boot, a UserData script calls `/opt/aws/bin/cfn-init` (or equivalent) to fetch the metadata from the stack and apply the configuration (install packages, write files, and start/enable services).
* cfn-init uses the instance's IAM role (Instance Profile) to retrieve stack metadata, so the instance must have the appropriate permissions.

## 1) cfn-init metadata (packages and services)

The `AWS::CloudFormation::Init` metadata describes how to configure the instance. The fragment below installs the `httpd` package using `yum` and ensures the `httpd` service is enabled and running using `sysvinit`:

```yaml theme={null}
Metadata:
  AWS::CloudFormation::Init:
    config:
      packages:
        yum:
          httpd: []
      services:
        sysvinit:
          httpd:
            enabled: true
            ensureRunning: true
```

Notes:

* `packages` instructs cfn-init to install OS packages (here using `yum` for Amazon Linux).
* `services` tells cfn-init which service manager to interact with. Use `sysvinit` for older AMIs or `systemd` for Amazon Linux 2 and most modern distributions.

## 2) Properties: instance type, AMI, security group, and instance profile

The EC2 Instance resource needs standard properties: `InstanceType`, `ImageId`, `SecurityGroupIds`, and `IamInstanceProfile`. Many templates use a region-based mapping to choose the `ImageId`.

Example parameters and mapping:

```yaml theme={null}
Parameters:
  MyVPC:
    Type: AWS::EC2::VPC::Id
    Description: Select the VPC to launch the EC2 instance in

  MyInstanceType:
    Type: String
    Default: t3.micro
    Description: EC2 instance type

  MyCFNInstanceProfile:
    Type: AWS::IAM::InstanceProfile::Name
    Description: Name of an existing IAM Instance Profile to attach to the EC2 instance

Mappings:
  RegionMap:
    us-east-2:
      AMI: ami-0eb9d6fc9fab44d24
    eu-west-1:
      AMI: ami-0b3e7dd7b2a99b08d
    us-east-1:
      AMI: ami-0150ccaf51ab55a51
```

## 3) Security group

Create a security group that allows SSH (22) and HTTP (80) access and attach it to the instance via `SecurityGroupIds`:

```yaml theme={null}
MySecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Allow SSH and HTTP access
    VpcId: !Ref MyVPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 80
        ToPort: 80
        CidrIp: 0.0.0.0/0
      - IpProtocol: tcp
        FromPort: 22
        ToPort: 22
        CidrIp: 0.0.0.0/0
```

## 4) UserData: invoke cfn-init

UserData should invoke cfn-init on instance boot to apply the `AWS::CloudFormation::Init` configuration. Encode the script with `Fn::Base64` and use `Fn::Sub` to allow CloudFormation pseudo-parameters to be expanded:

```yaml theme={null}
UserData:
  Fn::Base64: !Sub |
    #!/bin/bash
    /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource MyInstance --region ${AWS::Region}
```

Practical tips:

* The typical path for `cfn-init` on Amazon Linux is `/opt/aws/bin/cfn-init`. Ensure the AMI includes the `aws-cfn-bootstrap` package or otherwise provides `cfn-init`.
* Use the `-v` flag for more verbose output when troubleshooting.
* Wrap the script with `Fn::Sub` when embedding pseudo-parameters such as `${AWS::StackName}` so substitutions happen before the Base64 encoding.

> **warning** Confirm the AMI you use contains `cfn-init` (often provided by the `aws-cfn-bootstrap` package). Also choose the correct service manager key in metadata (`sysvinit` vs `systemd`) to match your AMI. Without the correct AMI and permissions, cfn-init will not be able to apply the configuration.

## Full minimal template (combines the pieces)

This example ties together Parameters, Mappings, the security group, and the EC2 instance with `AWS::CloudFormation::Init` metadata and UserData that runs `cfn-init`.

```yaml theme={null}
AWSTemplateFormatVersion: '2010-09-09'
Description: Minimal template demonstrating cfn-init usage to install and start httpd

Parameters:
  MyVPC:
    Type: AWS::EC2::VPC::Id
    Description: Select the VPC to launch the EC2 instance in

  MyInstanceType:
    Type: String
    Default: t3.micro
    Description: EC2 instance type

  MyCFNInstanceProfile:
    Type: AWS::IAM::InstanceProfile::Name
    Description: Name of an existing IAM Instance Profile to attach to the EC2 instance

Mappings:
  RegionMap:
    us-east-2:
      AMI: ami-0eb9d6fc9fab44d24
    eu-west-1:
      AMI: ami-0b3e7dd7b2a99b08d
    us-east-1:
      AMI: ami-0150ccaf51ab55a51

Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow SSH and HTTP access
      VpcId: !Ref MyVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0

  MyInstance:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          packages:
            yum:
              httpd: []
          services:
            sysvinit:
              httpd:
                enabled: true
                ensureRunning: true
    Properties:
      InstanceType: !Ref MyInstanceType
      ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", AMI]
      IamInstanceProfile: !Ref MyCFNInstanceProfile
      SecurityGroupIds:
        - !Ref MySecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource MyInstance --region ${AWS::Region}

Outputs:
  InstanceId:
    Description: Instance ID of the created EC2 instance
    Value: !Ref MyInstance
```

## Template components at a glance

| Template section           | Purpose                           | Example/key items                                               |
| -------------------------- | --------------------------------- | --------------------------------------------------------------- |
| Parameters                 | Inputs to the template            | `MyVPC`, `MyInstanceType`, `MyCFNInstanceProfile`               |
| Mappings                   | Region-specific AMI selection     | `RegionMap` → `AMI`                                             |
| Resources — Security Group | Network access rules              | `MySecurityGroup` (SSH, HTTP)                                   |
| Resources — EC2 Instance   | Instance configuration & metadata | `MyInstance` with `Metadata` → `AWS::CloudFormation::Init`      |
| UserData                   | Boot-time invocation of cfn-init  | `Fn::Base64` + `Fn::Sub` script calling `/opt/aws/bin/cfn-init` |

## Final checklist

* Verify the `MyCFNInstanceProfile` Instance Profile exists and grants the instance permission to read CloudFormation stack metadata.
* Confirm the chosen AMI includes `cfn-init` (or install `aws-cfn-bootstrap`) and uses the expected service manager (`sysvinit` vs `systemd`).
* Use `-v` with cfn-init for verbose logs while debugging.
* Ensure your security group allows the inbound traffic necessary for testing (SSH/HTTP in this example).

When deployed, this template causes the EC2 instance to call `cfn-init` at boot. cfn-init will read the embedded `AWS::CloudFormation::Init` instructions to install `httpd` and ensure the service is enabled and running.

## Links and references

* [AWS CloudFormation User Guide — AWS::CloudFormation::Init](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html)
* [cfn-init and aws-cfn-bootstrap (GitHub / docs)](https://github.com/aws/aws-cfn-bootstrap)
* [Amazon Linux AMI information](https://aws.amazon.com/amazon-linux-ami/)
* [CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/026ceaf9-07b6-4964-b49d-7190c136ea2b/lesson/08a7d3f9-c583-47d0-a3d1-a67288850af3)
