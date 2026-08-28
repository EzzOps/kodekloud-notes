# Internet Gateway Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Networking-Fundamentals/Internet-Gateway-Demo/page

This lesson teaches how to convert a private subnet into a public subnet for Internet accessibility of EC2 instances.

In this lesson, you will learn how to convert a private subnet into a public subnet so that any EC2 instance deployed within becomes accessible from the Internet. We will create a VPC, a subnet, and then attach an Internet Gateway—all from scratch.

## Create a VPC

First, log into the AWS Management Console and navigate to the VPC page. Create a new VPC using the IPv4 CIDR block 10.0.0.0/16. (Assigning an IPv6 CIDR block is optional for this exercise.)

<Frame>
  ![The image shows the AWS Management Console interface for creating a VPC, with options to configure VPC settings such as name tag, IPv4 CIDR block, and tenancy.](https://kodekloud.com/kk-media/image/upload/v1752859153/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-management-console-vpc-creation.jpg)
</Frame>

## Create a Subnet

Next, create a subnet within the newly created VPC. Name this subnet "public subnet" and assign it the CIDR block 10.0.1.0/24.

<Frame>
  ![The image shows an AWS Management Console screen displaying details of a Virtual Private Cloud (VPC) named "vpcdemo," including its state, CIDR block, and associated resources.](https://kodekloud.com/kk-media/image/upload/v1752859155/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-management-console-vpcdemo-details.jpg)
</Frame>

After creating the subnet, deploy an EC2 instance into it. By default, an instance launched into this subnet will not have Internet access.

<Frame>
  ![The image shows an AWS VPC Management Console screen with a notification indicating a subnet has been successfully created. The subnet is listed as "public-subnet" and is in the "Available" state.](https://kodekloud.com/kk-media/image/upload/v1752859156/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-vpc-management-console-public-subnet.jpg)
</Frame>

## Launch an EC2 Instance

1. Open the EC2 page in a new tab and click on **Launch Instance**.
2. Name the instance (e.g., "my public server") and select the Amazon Linux AMI.
3. Choose the default instance type (t2.micro – covered by the free tier) and select an existing key pair for SSH access.

<Frame>
  ![The image shows an AWS EC2 instance launch configuration screen, where a user is selecting an Amazon Machine Image (AMI) and configuring instance details like the instance type and security group.](https://kodekloud.com/kk-media/image/upload/v1752859157/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-ec2-instance-launch-configuration.jpg)
</Frame>

Under **Network Settings**, edit the configuration to select the VPC you created earlier. With only one subnet available (the public subnet), select it and enable **Auto-assign Public IP** so that the instance receives a public IP address.

<Frame>
  ![This image shows the AWS EC2 instance launch configuration page, detailing key pair, network settings, and a summary of the instance specifications.](https://kodekloud.com/kk-media/image/upload/v1752859159/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-ec2-instance-launch-configuration-2.jpg)
</Frame>

Next, configure the security group. The default security group allows SSH (port 22) from any IP (0.0.0.0/0). Optionally, you can add an ICMP rule to allow ping traffic. Proceed to launch the instance.

<Frame>
  ![The image shows an AWS EC2 instance setup screen, detailing security group configurations and instance summary information. It includes options for creating a security group and setting inbound security rules for SSH access.](https://kodekloud.com/kk-media/image/upload/v1752859160/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-ec2-instance-setup-security-group.jpg)
</Frame>

<Frame>
  ![The image shows an AWS EC2 instance launch configuration screen, detailing security group rules, storage options, and a summary of the instance settings.](https://kodekloud.com/kk-media/image/upload/v1752859161/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-ec2-instance-launch-configuration-3.jpg)
</Frame>

Wait a few moments until the instance is initialized. Then, check the instance list to confirm that the server is running and has been assigned a public IP address.

<Frame>
  ![The image shows an AWS EC2 management console with a success message indicating the launch of an instance, along with various next step options like creating billing alerts and connecting to the instance.](https://kodekloud.com/kk-media/image/upload/v1752859162/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-ec2-console-instance-launch-success.jpg)
</Frame>

Review the instances view to verify that the instance is running and note its public IP address. Even though a public IP is assigned, the instance remains unreachable from the Internet by default.

<Frame>
  ![The image shows an AWS EC2 management console with details of two instances, one terminated and one running, including instance IDs, types, and public IP addresses.](https://kodekloud.com/kk-media/image/upload/v1752859163/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-ec2-management-console-instances.jpg)
</Frame>

Test network connectivity by pinging or attempting to SSH into the instance. For example, run the following commands in your terminal:

```bash theme={null}
ping 54.159.89.36
ssh -i aws-demo.pem ec2-user@54.159.89.36
```

<Callout icon="lightbulb">
  Both the `ping` and `ssh` commands will hang or time out because the subnet is private and lacks the necessary Internet routing configuration.
</Callout>

## Attach an Internet Gateway

To enable Internet connectivity, you must create and attach an Internet Gateway to your VPC.

1. Return to the VPC page and click on the Internet Gateway section.
2. Create a new Internet Gateway and give it a name (e.g., "my-internet-gateway").
3. Attach the newly created Internet Gateway to your VPC.

<Frame>
  ![The image shows an AWS console page for creating an internet gateway, with fields for entering a name tag and optional tags.](https://kodekloud.com/kk-media/image/upload/v1752859164/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-console-internet-gateway-creation.jpg)
</Frame>

<Frame>
  ![The image shows an AWS Management Console screen displaying details of an internet gateway with ID "igw-0ba052187bca5e574" that is attached to a VPC. The gateway is tagged with the name "my-igw."](https://kodekloud.com/kk-media/image/upload/v1752859165/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-management-console-internet-gateway.jpg)
</Frame>

Even after attaching the Internet Gateway, the instance remains unreachable because the route table of the subnet has not been updated. Re-run the `ping` command to confirm the connection still fails.

## Update the Route Table

Next, update the route table to direct traffic destined for the Internet through the Internet Gateway. Follow these steps:

1. Check the subnet's route table using the "Route Table" tab in the VPC console. You will notice that only a local route exists.
2. Edit the default route table or create a new custom route table (e.g., "public route table") associated with your VPC.
3. Associate the route table with the public subnet.
4. Add a default route (0.0.0.0/0) that directs all Internet-bound traffic to the Internet Gateway.

<Frame>
  ![The image shows an AWS Management Console screen displaying details of a route table within a VPC, including route destinations and their statuses.](https://kodekloud.com/kk-media/image/upload/v1752859166/notes-assets/images/AWS-Certified-Developer-Associate-Internet-Gateway-Demo/aws-management-console-route-table-vpc.jpg)
</Frame>

After saving the changes, the routing configuration enables Internet access for the EC2 instance. Test the connectivity again by running:

```bash theme={null}
