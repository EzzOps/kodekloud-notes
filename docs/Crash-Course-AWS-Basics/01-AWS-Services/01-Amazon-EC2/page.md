# Amazon EC2

Source: https://notes.kodekloud.com/docs/Crash-Course-AWS-Basics/AWS-Services/Amazon-EC2/page

Step-by-step guide to launching an Amazon EC2 instance and connecting via SSH, including AMI selection, instance type, key pairs, security groups, storage, and lifecycle actions.

This guide walks through launching a basic Amazon EC2 instance and connecting to it via SSH. It covers selecting an AMI, picking an instance type, configuring key pairs and security groups, checking instance details, and connecting from your workstation.

Start by opening the AWS Console and searching for "EC2". Make sure you are working in the desired AWS region — resources are region-specific. This demo uses US East (N. Virginia), but the same steps apply in any region.

1. Launch the EC2 instance
2. Configure authentication (key pair)
3. Configure networking and security groups
4. Review storage and launch
5. Verify instance details and metrics
6. SSH into the instance
7. Stop or terminate to avoid charges

Select "Launch instance" to start the instance-creation wizard.

<Frame>
  <img alt="A screenshot of the Amazon Web Services EC2 console (US East - N. Virginia) showing resource summaries, account attributes, service health, and availability zone details. The main panel includes a prominent &#x22;Launch instance&#x22; button and lists items like instances, volumes, snapshots, and security groups." />
</Frame>

You can also start from the Instances page using the "Launch instances" button. The wizard leads you through each configuration step.

## 1. Name and choose an AMI

Give the instance a friendly name tag (for example: "web-server") so it’s easy to identify later.

Choose an AMI (Amazon Machine Image) to define the operating system and any preinstalled software. AMIs can be:

* Amazon-provided (official images)
* Community-provided
* Marketplace images

For this demo we choose an Ubuntu AMI (Ubuntu 22.04 LTS, 64-bit x86). Remember AMI IDs vary by region — verify the AMI details before launching.

<Frame>
  <img alt="Screenshot of the AWS EC2 &#x22;Launch Instance&#x22; console showing an AMI search for &#x22;ubuntu&#x22;, instance type options (t2.micro selected) and the summary panel with configuration details and a &#x22;Launch instance&#x22; button." />
</Frame>

## 2. Select an instance type

Pick an instance type to define vCPU, memory, and network performance. For simple demos or free-tier usage, `t2.micro` or `t3.micro` (1 vCPU, 1 GiB RAM) are common choices.

## 3. Configure key pair (SSH authentication)

Configure a key pair for SSH access. Key pairs are the recommended, secure method for authenticating to EC2 instances.

* If you already have a key pair, select it.
* Otherwise, create a new key pair and download the private key file (`.pem`). For this demo we created `ec2-demo.pem`.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the &#x22;Create key pair&#x22; dialog for an EC2 instance, with the key pair name set to &#x22;ec2-demo&#x22; and options for RSA/ED25519 and .pem/.ppk formats. The &#x22;Create key pair&#x22; button is visible and ready to be clicked." />
</Frame>

<Callout icon="lightbulb">
  Keep your private key file secure. After downloading, restrict permissions (for example: `chmod 400 ec2-demo.pem`) so SSH will accept the key.
</Callout>

## 4. Networking and security groups

Choose the VPC and subnet (default VPC is common for simple setups). Configure security groups to control inbound/outbound traffic. Security groups act as a stateful firewall.

Common rules for a public web server:

* SSH: TCP 22 (restrict source to your IP if possible)
* HTTP: TCP 80 (0.0.0.0/0 for public access)
* HTTPS: TCP 443 (0.0.0.0/0 for public access)

For this demo we created a security group that allows SSH. Prefer restricting SSH to your client IP (for example `203.0.113.5/32`) rather than opening to the whole Internet.

<Frame>
  <img alt="A screenshot of the AWS EC2 instance launch/configuration page showing security group rules (SSH allowed from 0.0.0.0/0), storage configuration (8 GiB gp2 root volume) and instance summary. The right panel shows a summary with the &#x22;Launch instance&#x22; button." />
</Frame>

<Callout icon="warning">
  Allowing SSH from `0.0.0.0/0` exposes your instance to the entire Internet. Restrict SSH to your IP whenever possible.
</Callout>

## 5. Storage options

By default a root EBS volume (for example 8 GiB) is attached. Defaults are typically safe for demos; you can adjust size, volume type (gp2/gp3), and encryption as needed.

<Frame>
  <img alt="A screenshot of the AWS EC2 console showing an instance summary for a web-server (instance ID i-0cc486a7972a8a004). The instance is running (t2.micro) with public IPv4 3.88.49.107 and various networking/details listed." />
</Frame>

Launch the instance when ready. The Instances page shows the new instance in a "pending" state while it boots, then "running" when ready.

## 6. View instance details and settings

Click the instance ID to see fields such as:

* Instance ID
* Public IPv4 address / Public DNS
* Private IPv4 address
* AMI used
* Key pair name
* Attached security group(s)

A quick table for commonly checked fields:

| Field           | Why it matters                                       | Example                                   |
| --------------- | ---------------------------------------------------- | ----------------------------------------- |
| Instance ID     | Unique identifier for the EC2 instance               | `i-0cc486a7972a8a004`                     |
| Public IPv4     | Use for SSH or public access (if in a public subnet) | `3.88.49.107`                             |
| Public DNS      | Alternate way to connect (resolves to the public IP) | `ec2-3-88-49-107.compute-1.amazonaws.com` |
| Key pair        | Shows which key is allowed for SSH auth              | `ec2-demo`                                |
| Security groups | Controls inbound/outbound traffic                    | `launch-wizard-5 (sg-01c42ae4a41e45f7e)`  |

Under the Security tab you can inspect inbound and outbound rules. Security groups are stateful — return traffic is automatically allowed.

<Frame>
  <img alt="A screenshot of the AWS EC2 Security Groups page showing details for security group &#x22;launch-wizard-5&#x22; (sg-01c42ae4a41e45f7e). The inbound rules list shows an SSH (TCP port 22) rule open to 0.0.0.0/0." />
</Frame>

The Networking tab shows attached network interfaces, private/public IPs, and any Elastic IPs.

<Frame>
  <img alt="A screenshot of the AWS EC2 console showing an instance's details with the Storage tab selected. The Storage panel lists the root EBS device (/dev/sda1) as an attached 8 GiB volume and the instance state is Running." />
</Frame>

The Monitoring tab displays CloudWatch metrics (CPU, network, disk, status checks). Small or newly launched instances may show "No data available" until metrics are populated.

<Frame>
  <img alt="A screenshot of the AWS EC2 console on the Monitoring tab for an instance, showing multiple metric widgets (CPU utilization, network in/out, disk reads/writes, status checks) that display &#x22;No data available.&#x22; The left sidebar shows EC2 navigation items like Instances, Images, Elastic Block Store, and Network & Security." />
</Frame>

You can use the Actions menu from the Instances list to change networking, adjust security groups, or manage instance state (Stop, Reboot, Terminate).

<Frame>
  <img alt="A screenshot of the AWS EC2 console showing a selected running instance named &#x22;web-server&#x22; with its details pane and action menus open. The panel shows instance type (t2.micro), instance ID, and a public IPv4 address." />
</Frame>

## 7. Connect via SSH

Requirements:

* The private key file you downloaded (for example `ec2-demo.pem`)
* The instance Public IPv4 or Public DNS
* Correct username for the AMI (common defaults: `ubuntu` for Ubuntu, `ec2-user` for Amazon Linux, `centos` for CentOS)

Example connection steps from your terminal:

```bash theme={null}
