# NACLs Demo

Source: https://notes.kodekloud.com/docs/AWS-Networking-Fundamentals/Core-Networking-Services/NACLs-Demo/page

This tutorial explores configuring Network ACLs in AWS and their differences from security groups, focusing on traffic filtering at the subnet level.

In this tutorial, we’ll explore how to configure **Network ACLs (NACLs)** in AWS and see how they differ from **security groups**. Security groups are *stateful* and apply at the instance level, whereas NACLs are *stateless* and operate at the subnet level. You’ll learn how to test and modify NACL rules to filter traffic in and out of your subnet.

## Table of Contents

1. [Overview of Security Groups vs NACLs](#overview-of-security-groups-vs-nacls)
2. [1. Preparing the Security Group](#1-preparing-the-security-group)
3. [2. Verifying Subnet Membership](#2-verifying-subnet-membership)
4. [3. Inspecting the Default Network ACL](#3-inspecting-the-default-network-acl)
5. [4. Testing Initial Connectivity](#4-testing-initial-connectivity)
6. [5. Restricting Inbound NACL Rules to SSH Only](#5-restricting-inbound-nacl-rules-to-ssh-only)
7. [6. Allowing HTTP and HTTPS Traffic](#6-allowing-http-and-https-traffic)
8. [7. Demonstrating Stateless Behavior](#7-demonstrating-stateless-behavior)
9. [8. Using Explicit Deny Rules](#8-using-explicit-deny-rules)
10. [Conclusion](#conclusion)
11. [References](#references)

## Overview of Security Groups vs NACLs

| Feature          | Security Groups     | Network ACLs (NACLs)       |
| ---------------- | ------------------- | -------------------------- |
| Statefulness     | Stateful            | Stateless                  |
| Scope            | Instance-level      | Subnet-level               |
| Rule Types       | Allow only          | Allow & Deny               |
| Evaluation Order | All rules evaluated | First-match by rule number |

<Callout icon="lightbulb">
  Use security groups for fine-grained, instance-level controls and NACLs for broader subnet-level filtering.
</Callout>

***

## 1. Preparing the Security Group

Before testing NACL behavior, make sure your EC2 security group is wide open so it won’t block any traffic.

1. In the AWS Management Console, go to **EC2** → **Instances**, select your servers.
2. Under **Security** → **Security Groups**, click **Change security groups**.
3. Attach the `webserver-sg` security group to both instances.
4. Edit **Inbound** and **Outbound** rules to allow all traffic (All protocols, All ports, Source/Destination `0.0.0.0/0`).

<Frame>
  ![The image shows an AWS EC2 Management Console with two running instances, "server-2" and "server1," both of type t2.micro. The details of "server1" are displayed, including security group information and inbound rules.](https://kodekloud.com/kk-media/image/upload/v1752863275/notes-assets/images/AWS-Networking-Fundamentals-NACLs-Demo/aws-ec2-management-console-instances.jpg)
</Frame>

<Frame>
  ![The image shows an AWS EC2 Management Console screen displaying details of a security group named "webserver-sg," including its inbound and outbound rules. The outbound rules section is highlighted, showing a rule allowing all traffic to destination 0.0.0.0/0.](https://kodekloud.com/kk-media/image/upload/v1752863276/notes-assets/images/AWS-Networking-Fundamentals-NACLs-Demo/aws-ec2-security-group-outbound-rules.jpg)
</Frame>

***

## 2. Verifying Subnet Membership

Both instances must reside in the same subnet to observe NACL behavior:

1. Select your instance in **EC2** → **Networking** tab.
2. Copy the **Subnet ID** (e.g., `subnet-e1683`).

Repeat for the second instance to confirm they share the same Subnet ID.

***

## 3. Inspecting the Default Network ACL

Navigate to **VPC** → **Security** → **Network ACLs**. Select the default ACL for your VPC and review its inbound rules:

* **Rule 100**: Allow all traffic (All protocols, All ports, `0.0.0.0/0`)
* **Rule \***: Deny all traffic

Because rule 100 catches all traffic first, the deny rule never applies.

<Frame>
  ![The image shows the AWS Management Console displaying the Network ACLs section, listing various ACLs with details such as associated subnets and inbound rules. The selected ACL has inbound rules allowing and denying all traffic from any source.](https://kodekloud.com/kk-media/image/upload/v1752863277/notes-assets/images/AWS-Networking-Fundamentals-NACLs-Demo/aws-management-console-network-acls.jpg)
</Frame>

***

## 4. Testing Initial Connectivity

With the security group and default NACL wide open, verify connectivity:

```bash theme={null}
