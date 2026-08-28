# Inbound rule configuration for SSH access
{
    "Type": "SSH",
    "Protocol": "TCP",
    "PortRange": "22",
    "Source": "0.0.0.0/0"
}
```

In this configuration, the rule allows SSH (TCP port 22) access from any IP address (0.0.0.0/0). Remember that security groups only support "allow" rules. Outbound rules follow a similar format but apply to traffic leaving the instance.

The diagram below shows a user interface section for configuring these inbound rules specifically for SSH:

<Frame>
  ![The image shows a section of a user interface for configuring inbound rules, specifically for SSH access, with details like protocol, port range, and source. It includes an icon and is labeled "Inbound and Outbound Rules."](https://kodekloud.com/kk-media/image/upload/v1752865906/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-NACLs-and-SecGroups/inbound-outbound-rules-ssh-config.jpg)
</Frame>

### Automatic Traffic Exceptions in Security Groups

Certain traffic types are automatically permitted by security groups, ensuring essential communication is not interrupted. These include:

* Amazon DNS servers
* Amazon DHCP traffic
* EC2 instance metadata service
* ECS task metadata endpoints
* Windows license activation traffic
* Amazon Time Sync Service
* Reserved IP addresses used by the default VPC router

The image below lists these exceptions:

<Frame>
  ![The image lists services for which security groups do not filter traffic, including Amazon DNS, DHCP, EC2 instance metadata, ECS task metadata endpoints, Windows license activation, Amazon Time Sync Service, and reserved IP addresses for the default VPC router.](https://kodekloud.com/kk-media/image/upload/v1752865908/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-NACLs-and-SecGroups/security-groups-traffic-exceptions.jpg)
</Frame>

<Callout icon="lightbulb">
  You do not need to create explicit rules for the above protocols; they are automatically allowed by AWS to ensure critical services run smoothly.
</Callout>

***

This comprehensive guide has provided an in-depth look at how NACLs and security groups function, highlighting their individual roles and how they synergize to secure your AWS infrastructure effectively.

For further reading and advanced configuration tips, be sure to check out the [AWS Documentation](https://aws.amazon.com/documentation/) and related resources.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/6b2d9e18-1714-499c-83d4-4d1f7ff29e66/lesson/9452bc36-c9f9-4287-8108-dbfac0da78ae" />
</CardGroup>


# Network Firewall

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Security/Network-Firewall/page

This article explores AWS Network Firewall, a managed service that secures VPCs by filtering traffic and providing granular control and deep inspection features.

In this lesson, we explore AWS Network Firewall, a fully managed service that secures your Virtual Private Cloud (VPC) by filtering incoming and outgoing traffic. By leveraging granular control and deep inspection features, AWS Network Firewall ensures that only authorized traffic is allowed in or out of your VPC.

<Callout icon="lightbulb">
  When deploying AWS Network Firewall, always configure dedicated Firewall Endpoints within exclusive subnets. Avoid sharing these subnets with other resources to ensure comprehensive protection.
</Callout>

## Firewall Endpoints and Subnet Configuration

To safeguard your VPC and its subnets, it is crucial to create dedicated Firewall Endpoints. These endpoints act as the primary points for traffic inspection. You must allocate a specific subnet for your firewall deployment because placing a Firewall Endpoint in a subnet with other resources could compromise their protection.

<Frame>
  ![The image is a diagram illustrating a network firewall setup within a Virtual Private Cloud (VPC), showing private and firewall subnets across two availability zones, connected to a central firewall endpoint.](https://kodekloud.com/kk-media/image/upload/v1752865909/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Network-Firewall/vpc-network-firewall-setup-diagram.jpg)
</Frame>

In the diagram above, you can observe that separate subnets have been deployed across various availability zones to serve as Firewall Endpoints. Reserving an exclusive subnet for these endpoints ensures that your other VPC resources remain effectively protected.

## Key Features of AWS Network Firewall

AWS Network Firewall offers a range of robust features designed to enhance your network security:

* **Centralized Rule Management:** Simplify administration with rule groups that ensure consistent policies across multiple VPCs.
* **Granular Traffic Control:** Define detailed rules based on IP addresses, ports, protocols, and other traffic attributes.
* **Deep Packet Inspection & Intrusion Detection:** Identify and block advanced threats at both network and application layers.
* **Comprehensive Logging:** Maintain detailed logs of network and firewall activity for security analysis, compliance, and troubleshooting.
* **Rule Synchronization:** Seamlessly synchronize rules across multiple firewall instances, ideal for complex network architectures and multi-VPC environments.

<Frame>
  ![The image lists five features of a network firewall: Simplified Rule Management, Granular Control, Advanced Threat Protection, Logging and Monitoring, and Rule Synchronization. Each feature is represented with an icon and a number.](https://kodekloud.com/kk-media/image/upload/v1752865910/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Network-Firewall/network-firewall-features-list.jpg)
</Frame>

## Traffic Flow Process

When AWS Network Firewall is enabled, traffic within your VPC is directed through a carefully managed inspection process:

* **Inbound Traffic:** Traffic from the Internet Gateway is first routed to the dedicated Firewall Endpoint in the firewall subnet. After being inspected and validated against the firewall rules, it is forwarded to the subnet hosting your resources.
* **Outbound Traffic:** Similarly, outbound traffic from your resources is sent to the Firewall Endpoint for inspection before exiting the VPC.

It is essential to configure your route tables properly to ensure that traffic passes through the Firewall Endpoint. Without this configuration, inbound or outbound traffic might bypass the firewall inspection.

<Callout icon="triangle-alert">
  Improper routing configuration can lead to traffic bypassing the firewall inspection, potentially exposing your network to security risks.
</Callout>

## Deployment Models

AWS Network Firewall supports two primary deployment models to suit different network architectures:

1. **VPC Deployment:** Protects resources within a single VPC by directing traffic from the Internet Gateway to the Firewall Endpoint and then to the target subnet.
2. **Transit Gateway Deployment:** Provides centralized protection across multiple VPCs or on-premises networks by connecting them through an AWS Transit Gateway, eliminating the need for deploying individual firewalls for each VPC.

## Rules Engines: Stateless vs. Stateful

AWS Network Firewall employs two distinct rules engines that allow you to tailor traffic inspection based on your security needs:

* **Stateless Rules Engine:** Analyzes each packet independently without considering the traffic context. This engine processes rules in a user-defined order—similar to network ACLs—to determine if packets should be allowed or dropped.
* **Stateful Rules Engine:** Inspects packets within the context of their ongoing traffic flow. It recognizes the request-response pattern, supports complex rules, and logs traffic details. The engine processes pass rules first, followed by drop rules, and finally alert rules. It functions similarly to VPC security groups and is compatible with Suricata IPS.

<Frame>
  ![The image illustrates the flow of network traffic through firewall stateless and stateful engines, showing how packets are inspected and either dropped or passed based on rules.](https://kodekloud.com/kk-media/image/upload/v1752865911/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Network-Firewall/network-traffic-firewall-flow-diagram.jpg)
</Frame>

By leveraging either stateless or stateful inspection—or even a combination of both—you can customize AWS Network Firewall to meet your specific security requirements, ensuring efficient and comprehensive VPC protection.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/6b2d9e18-1714-499c-83d4-4d1f7ff29e66/lesson/bac7948a-5ef0-4a45-9dab-7be5f97df50d" />
</CardGroup>
