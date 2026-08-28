# Demo Creating and Executing Automation Runbooks

Source: https://notes.kodekloud.com/docs/AWS-Certified-CloudOps-Engineer-Associate/Domain-1-Monitoring-Logging-and-Remediation/Demo-Creating-and-Executing-Automation-Runbooks/page

This article demonstrates using a CloudFormation template to create and execute automation runbooks for managing EC2 instances with SSM.

Welcome to our SSM Automation tutorial. In this lesson, Michael Forrester demonstrates how to use a CloudFormation template to launch a T2 micro EC2 instance and configure SSM automation documents. These documents later create snapshots and restart the instance. Follow along as we explore the details of the CloudFormation template, IAM role configuration, and runbook creation.

## CloudFormation Template Overview

The CloudFormation template provisions several key resources, including the EC2 instance, the instance profile, and the necessary IAM roles. The instance is configured to run the latest Amazon Linux 2 AMI and ensures that the SSM agent is properly installed and running.

<Frame>
  ![The image shows an AWS CloudFormation dashboard displaying stack details and events for "SSM-Automation-Demo," with various statuses like "CREATE\_COMPLETE" and "CREATE\_IN\_PROGRESS."](https://kodekloud.com/kk-media/image/upload/v1752859897/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Demo-Creating-and-Executing-Automation-Runbooks/aws-cloudformation-ssm-automation-dashboard.jpg)
</Frame>

Below is an excerpt of the CloudFormation template:

```yaml theme={null}
Type: String
Default: t2.micro
Description: EC2 instance type
AllowedValues:
  - t2.small
  - t3.micro
  - t3.small
Resources:
  DemoEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: '{{resolve:ssm:/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2}}'
      InstanceType: !Ref InstanceType
      IamInstanceProfile: !Ref DemoInstanceProfile
      UserData:
        Fn::Base64: |
          #!/bin/bash
          # Ensure the SSM agent is installed and running
          sudo systemctl status amazon-ssm-agent
          if [ $? -ne 0 ]; then
              sudo yum install -y amazon-ssm-agent
              sudo systemctl enable amazon-ssm-agent
              sudo systemctl start amazon-ssm-agent
          fi
          # Log installation status for verification
          echo "SSM Agent installation status:" > /tmp/ssm-install-log.txt
          sudo systemctl status amazon-ssm-agent >> /tmp/ssm-install-log.txt
Tags:
  - Key: Name
    Value: SSM-Automation-Demo-Instance

DemoInstanceProfile:
  Type: AWS::IAM::InstanceProfile
  Properties:
    Roles: !Ref DemoEC2Role
```

<Callout icon="lightbulb">
  The template includes a user data script to validate that the SSM agent is running on the instance, ensuring seamless automation execution.
</Callout>

## IAM Role Configurations

The template defines two critical IAM roles. One is for the EC2 instance (DemoEC2Role) to enable SSM managed instance functionality, and the other is the Automation Service Role, which allows the automation document to perform a series of EC2 actions.

```yaml theme={null}
AssumeRolePolicyDocument:
  Version: '2012-10-17'
  Statement:
    - Effect: Allow
      Principal:
        Service: ec2.amazonaws.com
      Action: sts:AssumeRole
ManagedPolicyArns:
  - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

AutomationServiceRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: ssm.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AmazonSSMAutomationRole
    Policies:
      - PolicyName: EC2ManagementPermissions
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - ec2:DescribeInstances
                - ec2:DescribeInstanceStatus
                - ec2:StartInstances
                - ec2:StopInstances
                - ec2:CreateSnapshot
                - ec2:DescribeSnapshots
                - ec2:CreateTags
              Resource: '*'
Outputs:
  InstanceId:
    Description: ID of the EC2 instance.
```

The CloudFormation template reiterates the tags and instance profile configuration to ensure consistency:

```yaml theme={null}
Tags:
  Key: Name
  Value: SSM-Automation-Demo-Instance
DemoInstanceProfile:
  Type: AWS::IAM::InstanceProfile
  Properties:
    Roles:
      - !Ref DemoEC2Role
DemoEC2Role:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: ec2.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
AutomationServiceRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: ssm.amazonaws.com
```

## Navigating to AWS Systems Manager

Once the instance and IAM roles are provisioned through CloudFormation, the next step is to work within AWS Systems Manager. Navigate to the Documents section under Change Management Tools to create a custom automation document.

<Frame>
  ![The image shows a webpage for AWS Systems Manager, highlighting features and benefits for managing nodes at scale. It includes navigation options on the left and sections for benefits, use cases, and resources.](https://kodekloud.com/kk-media/image/upload/v1752859898/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Demo-Creating-and-Executing-Automation-Runbooks/aws-systems-manager-webpage-features.jpg)
</Frame>

Click on Documents and choose to create a new document with the Automation type. Follow the on-screen guide to start with automation runbooks.

<Frame>
  ![The image shows an AWS interface for creating automation runbooks, featuring a "Getting started" guide with options to learn about components, review Amazon samples, and create custom runbooks.](https://kodekloud.com/kk-media/image/upload/v1752859899/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Demo-Creating-and-Executing-Automation-Runbooks/aws-automation-runbooks-interface.jpg)
</Frame>

## Designing the Automation Runbook

For this runbook, name it **StopSnapshotStartEC2Instance**. This document performs the following tasks:

* Stops the EC2 instance.
* Creates a snapshot of its root volume.
* Starts the instance.
* Verifies that the instance is in a running state.

The automation flow is visually represented using a flowchart interface.

<Frame>
  ![The image shows an AWS Management Console interface for creating a runbook in AWS Systems Manager. It features a flowchart with "Start" and "End" nodes and a sidebar with various actions and scripting options.](https://kodekloud.com/kk-media/image/upload/v1752859901/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Demo-Creating-and-Executing-Automation-Runbooks/aws-systems-manager-runbook-flowchart.jpg)
</Frame>

Switch to the code view to review and customize the runbook. A pre-configured runbook using schema version 3 is provided:

```yaml theme={null}
schemaVersion: '0.3'
description: |
  *Replace this default text with instructions or other information about your runbook.*
----
### What is Markdown?
Markdown is a lightweight markup language that converts your content with plain text formatting to structure.
## You can add headings
You can add *italics* or make the font **bold**
1. Create numbered lists
2. Add bullet points
   * Indent code samples
You can create a [link to another webpage](https://aws.amazon.com),
```

### Automation Steps Overview

The runbook includes the following automation steps:

* **Check the Instance State:** Pause to verify the current state.
* **Stop the Instance:** Initiate stopping the instance.
* **Wait for Instance Stop:** Ensure the instance has stopped.
* **Retrieve the Root Volume ID:** Identify the root volume for creating a snapshot.
* **Create the Snapshot:** Capture the snapshot of the root volume.
* **Start the Instance:** Restart the instance.
* **Verify Instance Running:** Confirm the instance is running post-automation.

Below is an excerpt that illustrates the snapshot creation step:

```yaml theme={null}
inputs:
  Service: ec2
  Api: CreateSnapshot
  VolumeId: "{{GetRootVolumeId.RootVolumeId}}"
  Description: "{{SnapshotDescription}}"
  TagSpecifications:
    - ResourceType: snapshot
      Tags:
        - Key: Name
          Value: AutoSnapshot-{{InstanceId}}
        - Key: CreatedBy
          Value: SystemsManagerAutomation
outputs:
  Name: SnapshotId
  Selector: $.SnapshotId
  Type: String
- name: StartInstance
  action: aws:changeInstanceState
  inputs:
    InstanceIds: ['{{InstanceId}}']
    DesiredState: running
- name: VerifyInstanceRunning
  inputs:
    Service: ec2
    Api: DescribeInstances
    PropertySelector: '$.Reservations[0].Instances[0].State.Name'
  outputs:
    - InstanceId
```

Additional steps manage the instance state before and after creating the snapshot:

```yaml theme={null}
InstanceIds: '{{InstanceId}}'
IncludedAllInstances: true
outputs:
  InstanceState:
    Selector: $.InstanceState[0].InstanceState.Name
    Type: String

name: StopInstance
action: aws:changeInstanceState
inputs:
  InstanceIds:
    - '{{InstanceId}}'
  DesiredState: stopped
  isEnd: false

name: WaitForInstanceStop
action: aws:waitForAwsResourceProperty
inputs:
  Service: ec2
  Api: DescribeInstances
  InstanceIds:
    - '{{InstanceId}}'
  PropertySelector: $.Reservations[0].Instances[0].State.Name
  DesiredValues:
    - stopped

name: GetRootVolumeId
action: aws:executeAwsApi
inputs:
  Service: ec2
  Api: DescribeInstances
  InstanceIds:
    - '{{InstanceId}}'
outputs:
  RootVolumeId:
    Selector: $.Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId
    Type: String

name: CreateSnapshot
action: aws:executeAwsApi
```

The user data section on the EC2 instance reinforces that the SSM agent is running:

```bash theme={null}
sudo systemctl start amazon-ssm-agent
else
    sudo systemctl restart amazon-ssm-agent
fi
