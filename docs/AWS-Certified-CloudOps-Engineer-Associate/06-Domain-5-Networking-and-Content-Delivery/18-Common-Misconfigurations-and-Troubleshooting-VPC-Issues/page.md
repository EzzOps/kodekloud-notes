# Common Misconfigurations and Troubleshooting VPC Issues

Source: https://notes.kodekloud.com/docs/AWS-Certified-CloudOps-Engineer-Associate/Domain-5-Networking-and-Content-Delivery/Common-Misconfigurations-and-Troubleshooting-VPC-Issues/page

Guides common AWS VPC misconfigurations and step by step troubleshooting for connectivity issues involving public IPs, route tables, Internet and NAT gateways, security groups, and network ACLs.

Welcome. This lesson explains the most common AWS VPC misconfigurations and practical troubleshooting steps. VPCs combine several components—VPCs, subnets, Internet Gateways (IGWs), route tables, IP addressing, security groups, Network ACLs (NACLs), NAT gateways, and VPC endpoints—so connectivity issues often come from misconfigurations across these layers. Read the checklist and examples below to quickly identify and fix connectivity problems.

Overview of typical problem areas

| Resource / Area        | Common Misconfiguration                                                     | Quick impact                                  |
| ---------------------- | --------------------------------------------------------------------------- | --------------------------------------------- |
| Public IP assignment   | Instances launched without auto-assigned public IPv4 or an Elastic IP (EIP) | No direct internet access from public subnets |
| Route tables           | Missing 0.0.0.0/0 route or incorrect target                                 | No outbound internet traffic                  |
| Security groups        | Overly restrictive rules or wrong direction allowed                         | Traffic blocked at instance level             |
| Network ACLs (NACLs)   | Missing both inbound and outbound rules (stateless)                         | Return packets dropped                        |
| Internet Gateway (IGW) | Not created or not attached to the VPC                                      | No internet connectivity for public subnets   |
| NAT gateway            | Placed in private subnet or missing routes from private subnets             | Private instances cannot access the internet  |

1. Instances launched without a public IP
   An instance in a public subnet still needs a public IPv4 address (or an EIP) to access the internet directly. If an instance has only a private IP and the subnet has no auto-assign setting enabled, it cannot reach the internet even when the route table points to an IGW.

Fixes:

* Enable "Auto-assign public IPv4 address" for the subnet, or
* Assign an Elastic IP (EIP) to the instance when launching (or attach one later).

2. Route table misconfiguration (missing default route)
   Public subnets require a default route for non-local traffic (0.0.0.0/0) that points to the internet gateway. Without that entry, only VPC-local traffic (the "local" route) will work.

Example route table entries:

```text theme={null}
Destination        Target
10.10.0.0/16       local
0.0.0.0/0          igw-0abc1234
```

Best practice: Do not route RFC1918 private address ranges to the IGW. Private address ranges should stay internal or be routed through a NAT gateway for outbound internet access.

3. Firewall rules: security groups vs NACLs
   Understand the difference and where to apply rules:

* Security groups (stateful): You only need to allow the outbound or inbound direction for a connection; return traffic is automatically permitted.
* Network ACLs (stateless): You must define both inbound and outbound rules for the same traffic to succeed.

Example security group rules allowing common web access:

```text theme={null}
Type       Protocol   Port Range   Source
HTTP       TCP        80           0.0.0.0/0
HTTPS      TCP        443          0.0.0.0/0
SSH        TCP        22           <your-admin-ip>/32
```

> **lightbulb** Security groups are stateful and simpler to manage for instance-level access control. NACLs are stateless—if you use them, add matching inbound and outbound allow rules for the same ports and CIDR ranges.

4. Internet Gateway (IGW) not created or not attached
   A VPC must have an IGW attached to provide direct internet access for public subnets. Common mistakes:

* Forgetting to create an IGW.
* Creating an IGW but not attaching it to the correct VPC.
* Pointing the route table to an incorrect IGW ID.

Validate that:

* The IGW exists and is attached to the intended VPC.
* The route table for public subnets has a 0.0.0.0/0 target that matches the IGW ID.

5. NAT gateway placement and routing for private subnets
   Private subnets need a NAT gateway to access the internet for updates, package downloads, and other outbound-only needs. Typical mistakes include:

* Placing the NAT gateway in a private subnet (incorrect). NAT gateways must be created in a public subnet that has a route to the IGW and an Elastic IP assigned.
* Failing to add a private-subnet route that sends 0.0.0.0/0 to the NAT gateway.

Correct private-subnet route example:

```text theme={null}
Destination        Target
10.10.0.0/16       local
0.0.0.0/0          nat-0def5678
```

> **warning** NAT gateways must reside in a public subnet and require an Elastic IP. For high availability, deploy a NAT gateway in each Availability Zone and configure private-subnet route tables so instances use the NAT gateway in the same AZ. A NAT gateway placed in a private subnet will not provide outbound internet access.

<Frame>
  <img alt="A network diagram of a default VPC with two availability zones, showing a private subnet and a public subnet and a NAT gateway placed incorrectly in the private subnet. The caption explains that NAT gateways must be in a public subnet (with a route to an Internet Gateway) for outbound Internet traffic." />
</Frame>

Additional notes and best practices

* Security groups: open only required ports and restrict sources (avoid 0.0.0.0/0 for management ports like SSH/RDP).
* NACLs: if used, ensure matching inbound and outbound allow rules for each required port/protocol.
* IGW: there is one IGW per VPC—ensure route tables reference the correct IGW ID.
* NAT gateways: assign an Elastic IP and place them in public subnets; deploy one per AZ for resilience.
* Route tables: each subnet can be explicitly associated with a route table—verify subnet-to-route-table associations.

Troubleshooting checklist

| Check                | How to verify                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Public IP or EIP     | Confirm instance has public IPv4 or an EIP if it’s in a public subnet.                                      |
| Route to IGW/NAT     | Inspect the subnet's associated route table for a 0.0.0.0/0 route to igw-... (public) or nat-... (private). |
| IGW attached         | Verify the IGW exists and is attached to the VPC.                                                           |
| Security group rules | Review inbound/outbound rules on the instance security group.                                               |
| NACL rules           | If NACLs are enabled, check both inbound and outbound rules for required ports.                             |
| NAT placement        | Ensure NAT gateway is in a public subnet with an EIP and that private subnet routes point to it.            |
| AZ resiliency        | For production, run a NAT gateway in each AZ and route private subnets to the same-AZ NAT gateway.          |

References and further reading

* [Amazon VPC User Guide (AWS)](https://docs.aws.amazon.com/vpc/latest/userguide/)
* [NAT Gateways (AWS)](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
* [Internet Gateways (AWS)](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
* [Security Groups for Your VPC (AWS)](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
* [Network ACLs (ACLs) (AWS)](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)

Follow the checklist order above when diagnosing connectivity problems—checking public IPs, routes, IGW/NAT placement, and firewall rules in that sequence will resolve the majority of issues quickly.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-certified-sysops-administrator-associate/module/fd99c412-5efc-46e2-99ce-bb9c581fec27/lesson/af565c2e-6ecd-42af-88d9-10ee132ac101)
