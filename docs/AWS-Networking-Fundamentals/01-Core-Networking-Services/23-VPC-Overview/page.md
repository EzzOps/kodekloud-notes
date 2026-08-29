# VPC Overview

Source: https://notes.kodekloud.com/docs/AWS-Networking-Fundamentals/Core-Networking-Services/VPC-Overview/page

A Virtual Private Cloud (VPC) is an isolated network segment within AWS for launching resources in a logically separated environment.

A Virtual Private Cloud (VPC) is your isolated network segment within AWS. It lets you launch AWS resources in a logically separated environment, complete with custom IP ranges, subnets, routing rules, and security controls—just like running your own data center without the physical infrastructure.

## What Is a VPC?

A VPC is an isolated virtual network in AWS where you can launch resources such as EC2 instances. Within each VPC, you configure:

* IP address ranges using CIDR blocks
* Subnets for grouping resources across Availability Zones
* Route tables to control traffic flow
* Security Groups (instance-level, stateful firewalls)
* Network ACLs (subnet-level, stateless firewalls)
* Gateways for Internet, VPC-to-VPC, or on-premises connectivity

<Frame>
  ![The image explains what a Virtual Private Cloud (VPC) is, highlighting components like subnetting, routing, and firewalls. It includes a network diagram and a list of features related to VPCs.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863374/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/vpc-network-diagram-subnetting-routing-firewalls.jpg)
</Frame>

## Regional Isolation

Each VPC exists entirely within a single AWS Region and cannot span multiple regions. By default, resources in VPC A (us-east-1) are isolated from resources in VPC B (us-east-2) unless you establish explicit connectivity.

<Frame>
  ![The image illustrates AWS Cloud regions "us-east-1" and "us-east-2," each containing a separate VPC (Virtual Private Cloud). It highlights that a VPC is specific to a single region.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863378/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/aws-cloud-regions-vpc-illustration.jpg)
</Frame>

## VPC as a Network Boundary

Out of the box, VPCs are completely isolated:

* No Internet access until you attach an **Internet Gateway**
* No communication between VPCs until you configure **VPC Peering** or a **Transit Gateway**
* No on-premises connectivity until you set up **VPN** or **AWS Direct Connect**

<Callout icon="lightbulb">
  You can attach an Internet Gateway to multiple public subnets, but each VPC supports only one Internet Gateway.
</Callout>

## IP Addressing: CIDR Blocks

When creating a VPC, assign a primary IPv4 CIDR block between `/16` and `/28`:

* Example: `192.168.0.0/16` (65,536 addresses)
* Add secondary IPv4 CIDR blocks as needed
* Enable IPv6 using a `/56` block (up to five per VPC, adjustable on request)

<Frame>
  ![The image is a diagram explaining a Virtual Private Cloud (VPC) with a CIDR block of 192.168.0.0/16, including options for secondary IPv4 and IPv6 CIDR blocks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863379/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/vpc-diagram-cidr-blocks-ipv4-ipv6.jpg)
</Frame>

<Callout icon="triangle-alert">
  Plan your CIDR ranges carefully to avoid overlap with other VPCs or on-premises networks.
</Callout>

## Default vs. Custom VPCs

AWS offers two VPC types:

| Feature           | Default VPC                                      | Custom VPC                             |
| ----------------- | ------------------------------------------------ | -------------------------------------- |
| Creation          | Automatically created in every region            | Manually created by you                |
| CIDR block        | `172.31.0.0/16`                                  | You choose (`/16`–`/28` for IPv4)      |
| Subnets           | One public `/20` subnet per AZ                   | Public/private subnets per your design |
| Internet Gateway  | Attached with a 0.0.0.0/0 route by default       | Requires manual attachment & routing   |
| Security Controls | Default SG and NACL allow all traffic by default | Configure SGs & NACLs from scratch     |

<Frame>
  ![The image is a diagram illustrating multiple regions, each containing a Virtual Private Cloud (VPC) labeled as "Default."](../../../../images/kodekloud.com/kk-media/image/upload/v1752863380/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/vpc-default-regions-diagram.jpg)
</Frame>

<Frame>
  ![The image is a diagram showing two types of Virtual Private Clouds (VPCs) within a region: a default VPC and a custom VPC, both represented in separate boxes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863381/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/vpc-diagram-default-custom-boxes.jpg)
</Frame>

<Frame>
  ![The image illustrates a comparison between a default and a custom Virtual Private Cloud (VPC) within a region, featuring icons and labels for each type.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863383/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/vpc-comparison-default-custom-illustration.jpg)
</Frame>

## Default VPC Configuration

Every AWS Region includes one Default VPC with these built-in settings:

* **CIDR block**: `172.31.0.0/16` (65,536 IPs)
* **Subnets**: One default `/20` subnet per AZ
  * e.g., `172.31.16.0/20`, `172.31.32.0/20`, etc.
* **Internet Gateway**: Attached by default with a `0.0.0.0/0` route
* **Security Group**: Default SG allowing all outbound traffic
* **Network ACL**: Default NACL allowing all inbound and outbound traffic

<Frame>
  ![The image illustrates a default VPC setup, showing an internet gateway attached to the VPC, routes directing all traffic to the gateway, and public subnets in two availability zones accessible from the internet.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863384/notes-assets/images/AWS-Networking-Fundamentals-VPC-Overview/default-vpc-setup-internet-gateway.jpg)
</Frame>

## Summary

* VPCs isolate your AWS resources within a single Region.
* Define IP ranges with CIDR blocks (IPv4 `/16`–`/28`, optional IPv6 `/56`).
* Default VPCs are pre-configured for fast deployment; Custom VPCs give you full control.
* Default VPCs use `172.31.0.0/16`, provide one `/20` subnet per AZ, and include Internet access by default.
* Security Groups and NACLs enforce instance- and subnet-level traffic rules, respectively.

## Links and References

* [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/)
* [AWS Networking Services](https://aws.amazon.com/products/networking/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-networking-fundamentals/module/406e4440-01a6-45f6-ab45-e14485d333c3/lesson/19a57528-02b5-4093-8418-feb2b8cb3dfd" />
</CardGroup>
