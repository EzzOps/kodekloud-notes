# EFS Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Storage/EFS-Demo/page

Guide showing how to create and configure Amazon EFS, set mount targets and security groups, and mount the same file system on two EC2 instances for shared access.

This guide demonstrates how to create an Amazon Elastic File System (EFS), configure mount targets and security groups, and mount the same EFS file system on two EC2 instances (server1 and server2) located in different Availability Zones (AZs). The result is shared, concurrent read/write access from multiple instances.

Environment: a simple VPC with two subnets across two AZs and two EC2 instances (server1 and server2), each in a separate AZ.

<Frame>
  <img alt="A screenshot of the AWS EC2 Instances console showing two running t2.micro instances (server1 and server2), each with 2/2 status checks passed and public IPv4 addresses listed." />
</Frame>

Overview

* Create an EFS file system and configure options (storage class, encryption, lifecycle, throughput, performance).
* Add mount targets in the VPC subnets for all AZs used by your EC2 clients.
* Configure security groups to permit NFS (TCP/2049) traffic from EC2 instances to EFS mount targets.
* Install amazon-efs-utils on each EC2 instance and mount the file system.
* Verify shared file visibility and make mounts persistent across reboots.

Creating the EFS file system (step-by-step)

1. Open the Amazon EFS console and choose Create file system. Use Quick create for defaults or Customize to set options manually.
2. Provide a name (for example: efsdemo).
3. Choose a storage class:
   * Regional: redundant across AZs (recommended for HA)
   * One Zone: lower cost, single AZ
4. Optionally enable automatic backups and configure lifecycle management to transition older files to Infrequent Access (IA) to save cost.
5. Choose encryption options (at-rest via AWS KMS) if required.
6. Choose throughput and performance modes to match your workload (bursting vs provisioned throughput; General Purpose vs Max I/O).

<Frame>
  <img alt="A screenshot of the Amazon Web Services console showing “Performance settings” for a file system, with throughput mode options like Enhanced, Bursting, Elastic (Recommended), and Provisioned. The page also displays encryption and transition-to-Infrequent-Access settings." />
</Frame>

EFS options summary

|              Setting | Purpose                   | Considerations                                      |
| -------------------: | ------------------------- | --------------------------------------------------- |
|        Storage class | Regional or One Zone      | Regional gives AZ redundancy; One Zone lowers cost  |
| Lifecycle management | Transition to IA          | Save cost for infrequently accessed files           |
|           Encryption | At-rest via KMS           | Required for compliance or security needs           |
|      Throughput mode | Bursting / Provisioned    | Choose based on predictable throughput requirements |
|     Performance mode | General Purpose / Max I/O | Use Max I/O for highly parallel workloads           |

Mount targets and security groups

* Select the VPC where your EC2 instances run. Create mount targets in each AZ/subnet where clients will mount the file system for redundancy and low-latency access.
* Assign a security group to the mount targets that permits NFS traffic (TCP port 2049) from your EC2 instances. A recommended pattern is:
  * Create an EFS security group (efs-sg)
  * Allow inbound TCP/2049 from the EC2 instances security group

Example security group setup: an EFS security group (efs-sg) that allows inbound NFS from the EC2 instances security group.

<Frame>
  <img alt="Screenshot of the AWS EC2 Security Groups console showing a selected security group named &#x22;efs-sg.&#x22; The group (sg-0a985...) has one inbound rule allowing all traffic from another security group (ec2-instances)." />
</Frame>

When configuring mount targets, the console displays the created entries (Availability Zone, Subnet ID, IP, Security groups). Verify that the mount target security group permits incoming TCP/2049 from the EC2 instances' SG.

<Frame>
  <img alt="A screenshot of the Amazon Web Services console on the &#x22;Network access&#x22; step for creating an Amazon EFS file system, showing VPC selection and mount target configuration. It lists availability zones, subnet IDs, IP address settings, and security groups (efs-sg) for mount targets." />
</Frame>

Create the file system and wait for state = Available. Note the File system ID (for example: fs-08de7b8e04f984697) — you will use this when mounting.

<Frame>
  <img alt="A screenshot of the Amazon Elastic File System (EFS) console showing details for a file system named &#x22;efsdemo&#x22; (fs-08de7b8e04f984697). The General panel shows General Purpose performance, Elastic throughput, automatic backups enabled, state &#x22;Available,&#x22; and a metered size of 6.00 KiB." />
</Frame>

Prepare EC2 instances and install amazon-efs-utils
On each EC2 instance (server1 and server2), create the mount directory and install amazon-efs-utils (provides the mount helper and utilities). Run the commands below with sudo privileges; pick the package manager appropriate for your distribution.

Example commands (run on each instance):

```bash theme={null}
sudo mkdir -p /efsdemo
