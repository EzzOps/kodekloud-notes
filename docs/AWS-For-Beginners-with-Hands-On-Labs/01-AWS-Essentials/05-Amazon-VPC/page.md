# Amazon VPC

Source: https://notes.kodekloud.com/docs/AWS-For-Beginners-with-Hands-On-Labs/AWS-Essentials/Amazon-VPC/page

Overview of Amazon VPC explaining virtual private clouds, subnets, routing, security groups, internet and NAT gateways, default VPCs, and launching EC2 instances within regional VPCs.

In this lesson we'll cover a foundational AWS networking concept: Amazon VPC (Virtual Private Cloud). A VPC is a logically isolated, virtual network in AWS that gives you full control over your cloud networking—IP address ranges, subnets, routing, and network-level security.

Key benefits of a VPC:

* Isolates resources between customers and between workloads in the same account.
* Lets you segment networks (public/private subnets) and apply fine-grained controls.
* Integrates with managed AWS networking services (Internet Gateway, NAT Gateway, Transit Gateway, VPN).

Core VPC capabilities:

* Subnetting: define IPv4/IPv6 CIDR ranges and place resources into subnets.
* Routing: configure route tables to control traffic flow.
* Firewalls: enforce traffic rules with Security Groups and Network ACLs (NACLs).
* Gateways: attach Internet Gateways, NAT Gateways, or VPN/Transit Gateways to enable external connectivity.

<Frame>
  <img alt="A slide titled &#x22;What Is a VPC?&#x22; showing a stylized network diagram of connected user nodes and a pointing hand. To the right it lists VPC components: Subnetting (IP addresses), Routing (route tables), Firewalls (NACLs and security groups), and Gateways." />
</Frame>

VPCs map closely to traditional data-center networking but are provisioned and managed via the AWS Console, CLI, or APIs. You can treat a VPC as your cloud “network” and build layered topologies—public subnets for internet-facing resources, private subnets for internal services, and dedicated routes for secure connectivity.

## VPCs are regional

* A VPC exists inside a single AWS region and cannot span regions. A VPC created in us-east-1 is separate from one created in us-east-2.
* Resources in different VPCs are isolated by default. Cross-VPC communication requires explicit configuration (VPC Peering, Transit Gateway, VPC endpoints, or VPN).

<Frame>
  <img alt="A diagram of the AWS Cloud showing two regions (us-east-1 and us-east-2), each containing its own VPC labeled VPC 1 and VPC 2. A caption notes that a VPC is specific to a single region." />
</Frame>

VPCs act as a network boundary: resources deployed into one VPC cannot reach resources in another VPC unless you create network connectivity.

<Frame>
  <img alt="A diagram of the AWS Cloud (us-east-1) showing two Virtual Private Clouds inside the region. Big X icons between them indicate they are network-isolated, illustrating that a VPC acts as a network boundary." />
</Frame>

## Default VPCs created per region

When you create an AWS account, AWS provisions a default VPC in each region with a standard, ready-to-use configuration. The default VPC is convenient for getting started because it enables Internet access for launched instances without manual network setup.

> **lightbulb** Every region in your AWS account receives a default VPC. Use it to quickly launch instances without configuring networking from scratch.

You can view VPC resources per region in the VPC Console, which shows counts for VPCs, subnets, route tables, security groups and related resources.

<Frame>
  <img alt="A screenshot of the AWS VPC Management Console showing the &#x22;Resources by Region&#x22; dashboard with counts for VPCs, subnets, route tables, security groups, and other VPC resources. The left sidebar shows VPC navigation (subnets, route tables, internet gateways) and the top has buttons for &#x22;Create VPC&#x22; and &#x22;Launch EC2 Instances.&#x22;" />
</Frame>

### Typical default VPC configuration

* CIDR block: 172.31.0.0/16 (default for the default VPC).
* Subnets: AWS creates one default subnet per Availability Zone in the region (e.g., us-east-1 typically has one in each AZ).
* Routing: A default route table and an Internet Gateway (IGW) are attached so instances in default subnets can obtain public IPs and reach the Internet (when auto-assign public IPv4 is enabled).
* Security: Default security group permits outbound traffic and limited inbound traffic; NACLs are permissive by default.

> **warning** Default VPCs are convenient but not hardened for production workloads. For production, design private subnets, tighten security groups/NACLs, and avoid placing sensitive services in default public subnets.

You can inspect the default VPC in the console to confirm the CIDR and the “default VPC” flag.

<Frame>
  <img alt="A screenshot of the AWS VPC Management Console showing a listed VPC (172.31.0.0/16) and a visual VPC resource map with multiple subnets, a route table, and an internet gateway. The left sidebar shows VPC-related navigation items like Subnets, Route tables, and Internet gateways." />
</Frame>

## Subnets and Availability Zones

Open the Subnets view for a VPC to see the subnets that AWS created (or that you created). A typical default VPC has one subnet per AZ; each subnet controls the IP addressing and can be configured to auto-assign public IPv4 addresses.

<Frame>
  <img alt="A screenshot of the AWS VPC console on the Subnets page, showing a list of subnets with their IDs, state, VPC and IPv4 CIDR blocks. The lower details pane shows properties for a selected subnet (available IPv4 addresses, availability zone, route table, network ACL, etc.)." />
</Frame>

Because default subnets are connected to an Internet Gateway and are often configured to auto-assign public IPv4, you can immediately launch Amazon EC2 instances that are reachable from the Internet.

## Launching an EC2 instance into the default VPC

When you use the EC2 Launch Instance wizard and choose the default VPC (or leave networking at default), the instance receives a public IPv4 address (if auto-assign is enabled) and becomes reachable from the Internet—subject to Security Group rules.

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch an instance&#x22; console showing the Name and tags and Application and OS Images (AMI) selection area on the left and a Summary panel on the right. The summary lists settings like 1 instance, Amazon Linux AMI, t2.micro, storage details and a &#x22;Launch instance&#x22; button." />
</Frame>

During launch, you can explicitly select the VPC and subnet (and the Availability Zone). Ensure the subnet has "Auto-assign public IPv4" enabled or override it at instance launch to assign a public IP.

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch an instance&#x22; console showing Network settings with a subnet dropdown open on the left. On the right is the Summary panel listing the AMI, instance type, storage, and a &#x22;Launch instance&#x22; button." />
</Frame>

After launching, the EC2 details show the private IP (from the subnet) and the public IPv4 address. With a public IP and Security Group rules allowing SSH (port 22), you can connect to the instance from your workstation.

<Frame>
  <img alt="A screenshot of the AWS EC2 Management Console showing an EC2 instance details pane. It shows a running instance (i-000872d9df41ab19c) with instance type t2.micro and public IPv4 34.201.6.109." />
</Frame>

Example: SSH into a launched instance (Windows CMD/PowerShell shown)

* Replace aws-demo.pem with your private key file and 34.201.6.109 with the instance's public IP.

```bash theme={null}
C:\Users\me\Downloads> ssh -i aws-demo.pem ec2-user@34.201.6.109
The authenticity of host '34.201.6.109 (34.201.6.109)' can't be established.
ECDSA key fingerprint is SHA256:fa0CPuUMP2Fvn9aHeAewW56Eei94znaTnFefIDRDg1mE.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '34.201.6.109' (ECDSA) to the list of known hosts.

      ,_        #_
  ^\_ ####_
  ~~ \_#####\           Amazon Linux 2023
  ~~   \####|
  ~~    \###\
  ~~     \#/_ ___  https://aws.amazon.com/linux/amazon-linux-2023
  ~~      V~'`->

[ec2-user@ip-172-31-6-49 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.3 ms
^C
--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
```

This confirms Internet connectivity (assuming Security Group egress rules permit outbound traffic).

## Quick reference table: VPC components and purpose

| Resource Type          | Purpose                                     | Example                                 |
| ---------------------- | ------------------------------------------- | --------------------------------------- |
| VPC                    | Isolated virtual network per region         | `172.31.0.0/16` default VPC             |
| Subnet                 | Segments within a VPC mapped to AZs         | Public subnet (auto-assign public IP)   |
| Route Table            | Controls routes for subnets                 | Route to IGW for 0.0.0.0/0              |
| Internet Gateway (IGW) | Enables Internet access for public subnets  | Attach to VPC to allow outbound traffic |
| NAT Gateway            | Allows private instances to access Internet | Private subnet → NAT in public subnet   |
| Security Group         | Stateful instance-level firewall            | Allow SSH (port 22) inbound             |
| Network ACL            | Stateless subnet-level firewall             | Additional layer of control             |

## Recap

* Amazon VPC provides isolated, configurable virtual networks inside AWS.
* Each VPC is regional and isolated by default.
* AWS creates a default VPC per region with a 172.31.0.0/16 CIDR and default subnets (one per AZ).
* To provide Internet access to instances: attach an Internet Gateway, assign public IPs at subnet or instance level, and configure Security Groups and routing appropriately.
* For production, design layered topologies (private subnets, NAT Gateways, VPC Peering/Transit Gateway, VPNs) and harden network policies.

## Links and references

* [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/)
* [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/)
* [AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)
* [AWS NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
* Learn more about EC2: [https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/cd9d5f60-422d-4fa4-82a4-6479a692689d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/9888231a-dd4c-4542-b155-d9f9e7452c29)
