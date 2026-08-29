# VPC Peering

Source: https://notes.kodekloud.com/docs/AWS-Networking-Fundamentals/Transit-Networks/VPC-Peering/page

VPC Peering establishes a private network connection between two VPCs, enabling communication as if on the same network.

In AWS, each Virtual Private Cloud (VPC) is an isolated network boundary. By default, resources in one VPC cannot reach resources in another VPC without an explicit link.

![The image illustrates the behavior of Virtual Private Clouds (VPCs) acting as network boundaries, showing two VPCs with a boundary between them.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863431/notes-assets/images/AWS-Networking-Fundamentals-VPC-Peering/vpc-network-boundaries-illustration.jpg)

## What Is VPC Peering?

VPC Peering establishes a private network connection between two VPCs, allowing instances to communicate as if they were on the same network. You can peer:

* VPCs within the same AWS Region
* VPCs across different regions (Inter-Region Peering)
* VPCs in separate AWS accounts

![The image illustrates VPC Peering between two AWS accounts, each containing a Virtual Private Cloud (VPC).](../../../../images/kodekloud.com/kk-media/image/upload/v1752863432/notes-assets/images/AWS-Networking-Fundamentals-VPC-Peering/vpc-peering-aws-accounts-diagram.jpg)

> **lightbulb** Once peered, you must update route tables; peering alone doesn’t modify routing.

## Pricing Overview

| Charge Type            | Details                                                            |
| ---------------------- | ------------------------------------------------------------------ |
| Peering Connection     | No setup fee or hourly rate                                        |
| Intra-AZ Data Transfer | Free (within the same Availability Zone over a peering connection) |
| Inter-AZ Data Transfer | Standard cross-AZ rates apply                                      |

## Establishing a VPC Peering Connection

Assume two VPCs with non-overlapping CIDR blocks:

* **VPC1**: `10.1.0.0/16`
* **VPC2**: `10.2.0.0/16`

Steps to create the peering link:

1. **Request Peering**
   * AWS Console: VPC dashboard → Peering Connections → Create Peering Connection
   * AWS CLI:
     ```bash theme={null}
     aws ec2 create-vpc-peering-connection \
       --vpc-id vpc-01234567 --peer-vpc-id vpc-089abcdef
     ```
2. **Accept Peering**
   * Console or CLI (`accept-vpc-peering-connection`) by the peer VPC owner.
3. **Verify Connection**
   * Status changes to `active` in the Peering Connections list—but routing is still pending.

![The image illustrates a VPC peering process between two virtual private clouds (VPC 1 and VPC 2) with IP ranges 10.1.0.0/16 and 10.2.0.0/16, showing the sending and accepting of a peering request.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863433/notes-assets/images/AWS-Networking-Fundamentals-VPC-Peering/vpc-peering-process-ip-ranges-diagram.jpg)

## Configuring Route Tables

After peering is active, add routes in each VPC’s route table:

VPC1 route table

```text theme={null}
Destination     Target
10.2.0.0/16     pcx-0a1b2c3d4e5f6g7h
```

VPC2 route table

```text theme={null}
Destination     Target
10.1.0.0/16     pcx-0a1b2c3d4e5f6g7h
```

This ensures traffic flows over the peering link instead of the internet gateway.

![The image illustrates a VPC peering connection between two virtual private clouds (VPC 1 and VPC 2) with their respective IP ranges and routing tables.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863434/notes-assets/images/AWS-Networking-Fundamentals-VPC-Peering/vpc-peering-connection-ip-ranges-routing.jpg)

> **triangle-alert** VPC Peering is non-transitive. If VPC1 peers with VPC2, and VPC2 peers with VPC3, VPC1 cannot reach VPC3 through VPC2. Each pair requires its own peering connection.

## Transitive Peering Is Not Supported

* VPC1 ↔ VPC2
* VPC2 ↔ VPC3
* **No** indirect VPC1 ↔ VPC3 communication

## Summary

![The image is a summary slide about VPC Peering, highlighting three points: network connection between VPCs, connection across regions and AWS accounts, and cost details regarding data transfer.](../../../../images/kodekloud.com/kk-media/image/upload/v1752863435/notes-assets/images/AWS-Networking-Fundamentals-VPC-Peering/vpc-peering-summary-network-connection.jpg)

* VPC Peering connects two VPCs privately.
* Peerings can span regions and AWS accounts.
* No cost for the connection itself; data transfer pricing applies.
* Each VPC pair requires its own peering link—no transit routing.

## Links and References

* [AWS VPC Peering Guide](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)
* [AWS Networking Fundamentals](https://aws.amazon.com/architecture/networking-and-content-delivery/)
* [AWS CLI Reference: create-vpc-peering-connection](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-vpc-peering-connection.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-networking-fundamentals/module/056227a0-6523-43a5-942e-4082adfaadf7/lesson/d389e18e-3934-4fa9-b14e-eabf8f1ca6af)
