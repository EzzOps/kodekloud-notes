# Default VPC Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/AWS-Fundamentals/Default-VPC-Demo/page

This guide reviews default VPC setups and pre-configured settings provided by AWS for new accounts, ideal for developers and cloud enthusiasts.

In this lesson, we review the default VPC setups and examine the pre-configured settings that AWS automatically provides when you create a new account. This guide is ideal for developers and cloud enthusiasts looking to understand how AWS simplifies network access and deployment.

First, navigate to the VPC section in the AWS Management Console. You can locate it by selecting it from your recently visited services or by searching for "VPC" in the console search bar. Although you might be working in the Northern Virginia region, note that the default configuration is consistent across all regions.

For a brand new AWS account, you will see one default VPC along with a few extra security groups that could be present.

<Frame>
  ![The image shows the AWS Management Console, specifically the VPC dashboard, displaying various resources and settings related to virtual private clouds in the US East region.](https://kodekloud.com/kk-media/image/upload/v1752858162/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-vpc-dashboard-us-east.jpg)
</Frame>

## Default VPC Details

Take a closer look at this default VPC. It is in an "available" state with the CIDR block set as 172.31.0.0/16. Additionally, the "default VPC" flag is enabled. Clicking on the VPC confirms the CIDR block and the default status.

<Frame>
  ![The image shows an AWS VPC management console with details of a specific VPC, including its ID, state, and configuration settings. The VPC is marked as available with DNS hostnames and resolution enabled.](https://kodekloud.com/kk-media/image/upload/v1752858164/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-vpc-management-console-details.jpg)
</Frame>

Next, switch to another region (for example, Ohio) and navigate to the VPC section. You will observe that there is exactly one VPC with the same CIDR block (172.31.0.0/16) marked as default. This confirms that AWS creates a default VPC with an identical configuration in every region.

## Exploring the Default VPC Subnets

Return to the Northern Virginia region and inspect the default VPC contents by checking its subnets. Identify the VPC ID (ending in ACB5) and then visit the Subnets section to find six subnets.

<Frame>
  ![The image shows the AWS VPC Management Console displaying a list of subnets, their statuses, and associated details like VPC, IPv4 CIDR, and availability zones.](https://kodekloud.com/kk-media/image/upload/v1752858166/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-vpc-management-console-subnets.jpg)
</Frame>

These six subnets exist because AWS provisions one default subnet per availability zone (for example, 1A, 1B, 1C, 1D, 1E, and 1F) within the region. To visualize the layout, reference the resource map in the VPC page, which clearly displays the six subnets aligned with their respective availability zones.

<Frame>
  ![The image shows an AWS VPC management console with details of a virtual private cloud, including subnets, route tables, and network connections. It also features a resource map illustrating relationships between these components.](https://kodekloud.com/kk-media/image/upload/v1752858167/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-vpc-management-console-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  The default VPC also features a route table that manages traffic flow and an Internet Gateway configured for internet access.
</Callout>

## Examining Subnet Configuration

Explore one of the subnets by navigating to its details page. You will notice that the subnet is configured to auto-assign public IPv4 addresses. This configuration ensures that any EC2 instance launched within the subnet will automatically receive a public IP address for internet connectivity.

<Frame>
  ![The image shows the AWS VPC Management Console displaying a list of subnets with details such as Subnet ID, state, and VPC information. The selected subnet's detailed information is shown below, including its IPv4 CIDR and availability zone.](https://kodekloud.com/kk-media/image/upload/v1752858168/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-vpc-management-console-subnets-2.jpg)
</Frame>

Once you create an AWS account, you can immediately deploy servers with internet access by utilizing the default VPC and its associated subnets.

## Launching an Instance in the Default VPC

To demonstrate this, navigate to the EC2 page and launch a new instance with the default configurations. For this demo, use the Amazon Linux image and select a T2 micro instance type. During the process, create a new key pair (for example, "aws-demo") and download the PEM file.

<Frame>
  ![The image shows a dialog box in the AWS Management Console for creating a key pair, with options to specify the key pair name, type, and private key file format.](https://kodekloud.com/kk-media/image/upload/v1752858169/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-key-pair-creation-dialog.jpg)
</Frame>

When launching the instance, ensure the following:

* The instance is assigned to the default VPC (usually the only option).
* A specific subnet is selected if required.
* The auto-assign public IPv4 address option is enabled to ensure the instance obtains internet connectivity.

<Frame>
  ![The image shows an AWS EC2 management console where a user is configuring network settings and reviewing instance details before launching an instance.](https://kodekloud.com/kk-media/image/upload/v1752858170/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-ec2-management-console-network-settings.jpg)
</Frame>

After launching, move to the Instances section to confirm that your instance is running. You will see both a private IP address (from the default CIDR block) and a public IP address.

<Frame>
  ![The image shows an AWS Management Console displaying details of a running EC2 instance, including its instance ID, public and private IP addresses, and instance type.](https://kodekloud.com/kk-media/image/upload/v1752858172/notes-assets/images/AWS-Certified-Developer-Associate-Default-VPC-Demo/aws-ec2-instance-details-console.jpg)
</Frame>

<Callout icon="triangle-alert">
  Always safeguard your key pair file and avoid sharing it publicly. It is essential for secure SSH access to your instances.
</Callout>

## Connecting to Your EC2 Instance

To connect to your instance via SSH, use the downloaded key pair. On your local machine, run the following command (replacing \<PUBLIC\_IP\_ADDRESS> with the actual public IP):

```bash theme={null}
ssh -i aws-demo.pem ec2-user@<PUBLIC_IP_ADDRESS>
```

Below is an example of the terminal output after a successful connection (note that the IP address and the key fingerprint will differ):

```plaintext theme={null}
Microsoft Windows [Version 10.0.19045.3324]
(c) Microsoft Corporation. All rights reserved.

C:\Users\sanje\Documents\scratch\aws-demo>ssh -i aws-demo.pem ec2-user@34.201.6.109
The authenticity of host '34.201.6.109 (34.201.6.109)' can't be established.
ECDSA key fingerprint is SHA256:faOCPuuMP2Fvn9aHeAeW56Eei94znaTnFefIDRd1mE.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '34.201.6.109' (ECDSA) to the list of known hosts.

Amazon Linux 2023

https://aws.amazon.com/linux/amazon-linux-2023
```

Once connected, you can verify internet connectivity by pinging an external DNS server (such as Google’s). This proves that resources launched in the default VPC have the necessary internet access.

## Summary

This demonstration highlights the advantages of using AWS's default VPC:

* Automatic deployment of a default VPC across every region.
* Provisioning of default subnets for multiple Availability Zones.
* Pre-configured Internet Gateway and route table for immediate internet access.
* Simplified server deployments with minimal networking configuration.

Understanding these default settings is crucial when comparing custom VPCs with AWS’s automated default configurations, particularly for quick-start deployments.

For further reading on AWS network architecture, consider exploring the [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) and other related resources.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/6d3acaeb-020a-4e1e-9bd0-5fc6c50eb164/lesson/1ab4b167-1caf-481c-b980-41f9dff3244d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/6d3acaeb-020a-4e1e-9bd0-5fc6c50eb164/lesson/b88867cb-f435-4301-9e9e-60125d0dd13b" />
</CardGroup>
