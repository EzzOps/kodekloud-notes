# Sample DNAT rule configuration for Spoke A VM1 and VM2
# VM1: Public IP <firewall_public_ip>:32000 -> 192.168.1.4:22
# VM2: Public IP <firewall_public_ip>:32001 -> 192.168.1.5:22
```

After deploying these rules via the Azure portal, establish SSH connections using the firewall’s public IP address and the specified port numbers:

```bash theme={null}
ssh kodekloud@<firewall_public_ip> -p 32000
```

You will be prompted for a password, and upon success, you will connect to Spoke A VM1. Repeat the process for Spoke A VM2 using port 32001.

<Frame>
  ![The image shows a Microsoft Azure portal interface where a user is adding a DNAT rule collection named "SSH-VMs" with specific rules for TCP protocols, destination ports, and translated IP addresses. The interface includes fields for rule collection type, priority, and action.](https://kodekloud.com/kk-media/image/upload/v1752882160/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Create-User-Defined-Routes-and-Network-Virtual-Appliances/azure-portal-dnat-rule-collection.jpg)
</Frame>

Additionally, you may need to configure application rules on the firewall to manage domain-based traffic. For instance, you could block all outbound web traffic by default and then allow access selectively via application rules. In one scenario, an application rule was added to permit access to [www.google.com](http://www.google.com) for one VM while denying it for another:

```bash theme={null}
# Testing web access from a VM behind the firewall
kodekloud@spoke-a-vm-1:~$ curl www.google.com
Action: Deny. Reason: No rule matched. Proceeding with default action.
```

To allow web access, adjust the Azure Firewall configuration by adding an application rule collection (e.g., named "SpokeA Domains") with a defined priority (e.g., 200) and specify:

* Source: Any (or a specific source IP)
* Protocols: HTTP, HTTPS
* Destination Type: FQDN (e.g., \*.google.com)

After applying this rule, test connectivity again. If configured correctly, one VM might access [www.google.com](http://www.google.com) while another could be restricted or allowed access to a different domain (e.g., [www.microsoft.com](http://www.microsoft.com)).

<Frame>
  ![The image shows a Microsoft Azure portal page displaying DNAT rules for a firewall policy, listing several SSH-VM rules with details like source, port, protocol, and translated addresses.](https://kodekloud.com/kk-media/image/upload/v1752882161/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Create-User-Defined-Routes-and-Network-Virtual-Appliances/azure-portal-dnat-firewall-rules.jpg)
</Frame>

Alternatively, network rules can also be used to manage communications (e.g., between spokes via the firewall) within a hub-spoke architecture.

## Conclusion

By overriding default system routes with user-defined routes and configuring both DNAT and application rules on the firewall, you can enforce tighter network controls and direct traffic through NVAs as required. This approach ensures that all network communications—whether internal or outbound—adhere to the security policies set in your Azure environment.

Happy configuring!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/cb10a3ae-53f4-4588-ad61-042af34f31ab/lesson/cadf0ff5-3fea-40ff-9791-b2c163ff8b32" />
</CardGroup>


# Define defense in depth

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/Perimeter-Security/Define-defense-in-depth/page

This article explains the defense in depth strategy in Azure, detailing multiple security layers protecting resources from potential threats.

As we explore the Azure security model, we focus on the layered approach known as defense in depth. This strategy enhances security by implementing multiple layers of protection between potential threats and your Azure resources. Below is an in-depth explanation of each layer, starting from physical security and working inward toward data protection.

<Callout icon="lightbulb">
  Implementing multiple security layers ensures that even if one layer is breached, the remaining layers continue to protect your environment.
</Callout>

## Physical Security

The physical security layer is the foundation of the Azure security model. It involves safeguarding data centers against physical threats. Microsoft data centers employ a comprehensive suite of measures—including biometric scanners, security personnel, and surveillance systems—to ensure that physical infrastructure remains secure and unauthorized access is prevented.

## Identity and Access Management

The identity and access layer is critical because it guarantees that only authorized users and services gain access to your resources. Features such as multi-factor authentication, conditional access policies, and role-based access control (RBAC) form the backbone of this security measure. By systematically regulating and verifying identities, this layer significantly strengthens your overall defense in depth strategy.

## Perimeter Security

Perimeter security focuses on protecting the edge of your network. Services like Azure Application Gateway and Azure Firewall play key roles in filtering malicious traffic before it reaches your resources. For instance, deploying Azure DDoS Protection safeguards your environment against distributed denial-of-service attacks that could disrupt service availability.

## Network Security

At the network layer, security is enhanced with measures such as segmentation and robust network policies. Tools like Network Security Groups (NSGs) and Application Security Groups (ASGs) control inbound and outbound traffic, ensuring that only authorized traffic flows between different network segments. These practices help minimize the overall attack surface.

## Compute Security

The compute security layer protects the core processing components of your environment, including virtual machines, containers, and serverless computing services. Using solutions such as Microsoft Defender for Cloud ensures that your virtual machines follow best practices—like timely system updates and effective endpoint protection—to detect and remove malicious software. This layer also covers host security and container security, which are essential for approaches involving Azure Kubernetes Service (AKS) and Azure Container Registry (ACR).

## Application Security

Application security integrates protection into the design, development, and deployment phases. Leveraging tools such as Azure DevOps and Azure App Service, you can implement secure DevOps practices (SecDevOps). This ensures that your continuous integration and deployment pipelines continuously update applications with the latest security measures.

## Data Security

Data security is central to the defense in depth strategy as it focuses on protecting data at rest and in transit. Key protective measures include encryption, auditing, and strict access controls. For example, Azure SQL Database supports Transparent Data Encryption (TDE) to secure data at rest, while Advanced Threat Protection (ATP) alerts you to anomalous activities that may signal attempted breaches. Additionally, Azure Defender for Cloud helps safeguard SQL databases and Azure Storage.

Reviewing the overall strategy reveals that each layer—from identity and access management to network, compute, and application—builds upon one another, forming a comprehensive defense in depth strategy with data security at its core.

<Callout icon="lightbulb">
  Later in the discussion, we will expand on this layered model by addressing additional aspects such as virtual network security, host security, container security, and further protective measures that enhance both the perimeter and data layers.
</Callout>

The subsequent sections will cover virtual network security, which forms the outer perimeter of your infrastructure, ensuring that every point of access to your environment is safeguarded.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/cb10a3ae-53f4-4588-ad61-042af34f31ab/lesson/31b5f406-17a8-4f6e-901b-923e00bb1bd3" />
</CardGroup>
