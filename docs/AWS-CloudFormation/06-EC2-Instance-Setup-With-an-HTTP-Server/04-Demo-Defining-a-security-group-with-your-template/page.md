# Demo Defining a security group with your template

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/EC2-Instance-Setup-With-an-HTTP-Server/Demo-Defining-a-security-group-with-your-template/page

Adding a security group to a CloudFormation template and attaching it to an EC2 instance to allow public HTTP access while troubleshooting VPC and update issues

In this lesson you'll add a Security Group to a CloudFormation template and attach it to an EC2 instance so the instance accepts HTTP (port 80) traffic from the public internet. This walk-through covers the minimal resource definitions, how to reference the security group from the instance, a common VPC-related error and how to fix it, and the CloudFormation update steps to apply the change.

## 1. Starting point — minimal EC2 instance

Here is the minimal EC2 Instance resource already in the template:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0eb9d6fc9fab44d24
```

When the instance launches without an explicit security group, it may use the account's default security group. To allow HTTP access from the internet, add a security group resource to the same template and then attach it to the instance.

This follows the same pattern used when adding other resources (for example, an S3 bucket and a corresponding bucket policy): define the new resource, then reference it where needed.

```yaml theme={null}
Resources:
  MyS3Bucket:
    Metadata:
      Purpose: "Creating an s3 bucket"
      Reviewed: "02-07-2025"
      Owner: "John Doe"
      Contact: "johndoe@mail.com"

  MyPublicReadPolicy:
    Condition: IsProd
    DependsOn: MyS3Bucket
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref MyS3Bucket
      PolicyDocument: {}
```

## 2. Define a Security Group with an ingress rule for HTTP

Add a Security Group resource that allows inbound HTTP traffic. SecurityGroup ingress rules are defined in the SecurityGroupIngress list; each rule is an object with fields describing protocol, ports, and source.

```yaml theme={null}
Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP access
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
```

Key fields used in the ingress rule:

| Field      | Description                        | Example     |
| ---------- | ---------------------------------- | ----------- |
| IpProtocol | Protocol to allow (tcp, udp, icmp) | `tcp`       |
| FromPort   | Starting port in the allowed range | `80`        |
| ToPort     | Ending port in the allowed range   | `80`        |
| CidrIp     | IPv4 CIDR range for the source     | `0.0.0.0/0` |

<Callout icon="lightbulb">
  A security group is a virtual firewall for your instance. Use SecurityGroupIngress to open inbound ports (like HTTP) and SecurityGroupEgress to restrict or allow outbound traffic.
</Callout>

## 3. Attach the Security Group to the EC2 instance

Reference the security group logical name using intrinsic function !Ref and add it to the EC2 instance via SecurityGroupIds:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0eb9d6fc9fab44d24
      SecurityGroupIds:
        - !Ref MySecurityGroup
```

## 4. Common error: security group and instance must be in the same VPC

If CloudFormation reports an error about the security group reference format or the instance update fails, the most common cause is that the Security Group is being created in a different VPC than the instance. To ensure the Security Group is created in the correct VPC, add the VpcId property to the security group (copy the VPC ID from your EC2 instance details):

```yaml theme={null}
Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP access
      VpcId: vpc-0f5d3d6445abf20b5
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
```

## 5. Combined minimal template

A minimal combined snippet that creates the instance and the security group in the same VPC:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0eb9d6fc9fab44d24
      SecurityGroupIds:
        - !Ref MySecurityGroup

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP access
      VpcId: vpc-0f5d3d6445abf20b5
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
```

Validate and lint your CloudFormation template (for example with cfn-lint or the CloudFormation console validator), then update the stack.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Update stack&#x22; page showing options to replace an existing template and to specify a template source (Amazon S3 URL or upload a file). The browser window displays the DemoStack in the us-east-2 console with the system taskbar visible at the bottom." />
</Frame>

Upload the updated template file, step through the update wizard, and submit the change.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Specify stack details&#x22; step for updating a stack (DemoStack), showing a message that there are no parameters defined in the template. The left shows the update step list and navigation buttons (Cancel, Previous, Next) are at the bottom right." />
</Frame>

CloudFormation may need to replace the instance to attach the new security group. Monitor the stack events until the update completes.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing the &#x22;Stacks&#x22; page with one stack named &#x22;DemoStack.&#x22; The stack entry is timestamped and marked with the status &#x22;UPDATE_COMPLETE_CLEANUP_IN_PROGRESS.&#x22;" />
</Frame>

When the update finishes, CloudFormation may have terminated the previous instance and launched a fresh instance that has the new security group attached. Wait for the instance to reach the running state and finish initialization.

<Frame>
  <img alt="A screenshot of the AWS EC2 Instances console showing two instances listed — one terminated and one running (both t3.micro) with the &#x22;Launch instances&#x22; button visible. The console is in the us-east-2 (United States — Ohio) region." />
</Frame>

## 6. Verify the Security Group inbound rule

Open the EC2 console → Network & Security → Security Groups, locate the security group created by the stack, and inspect the Inbound rules. You should see an IPv4 HTTP rule (TCP port 80) with source 0.0.0.0/0.

<Frame>
  <img alt="A screenshot of the AWS EC2 console open to a Security Group details page, showing the Inbound rules tab with a single IPv4 HTTP rule and its security group rule ID. The left sidebar shows EC2 navigation options." />
</Frame>

Once verified, your EC2 instance is reachable over HTTP. To harden or extend the configuration you can:

* Add additional ingress rules (HTTPS on 443, SSH on 22 with a restricted CIDR).
* Define SecurityGroupEgress rules to restrict outbound traffic.
* Use CloudFormation parameters or mappings to make the VpcId and CIDR ranges configurable.

## Links and references

* [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [Amazon EC2 security groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
* [cfn-lint — CloudFormation linter](https://github.com/aws-cloudformation/cfn-lint)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/e8be47ac-5e51-4463-8b8c-dc5552940b10/lesson/95f9fce5-c446-43a1-9c35-0e2b24a35f2b" />
</CardGroup>
