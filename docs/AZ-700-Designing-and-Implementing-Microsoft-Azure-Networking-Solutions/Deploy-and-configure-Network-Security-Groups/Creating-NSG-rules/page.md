# SSH into a VM that is a member of the ASG
ssh kodekloud@172.191.36.135

# Check the storage blob endpoint with a header request
curl -I https://cskodekloudaz01.blob.core.windows.net/vision/note.jpeg

# Check access to an external site (example)
curl -I https://www.microsoft.com
```

Expected outcomes:

* From a VM that is allowed to access Storage:

```bash theme={null}
HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: 12345
...
```

* From a VM blocked from Internet or Storage:

```bash theme={null}
curl: (28) Failed to connect to www.microsoft.com port 443: Connection timed out
```

This confirms that NSG rules referencing the ASG permit only the intended VMs to reach the storage service while others remain blocked.

## Quick reference table

|               Resource | Purpose                                  | Example                                                  |
| ---------------------: | ---------------------------------------- | -------------------------------------------------------- |
|                    ASG | Logical group of NICs for NSG rules      | `ASG-storage-servers`                                    |
|      NSG rule (source) | Use ASG as source instead of IPs         | Source: `ASG-storage-servers`                            |
| NSG rule (destination) | Use built-in service tags as destination | Destination: `Storage`                                   |
|          NIC-level NSG | Optional; evaluated with subnet NSG      | Disassociate if you want subnet NSG to be sole evaluator |

<Callout icon="lightbulb">
  Application Security Groups simplify NSG management by letting you add or remove VMs from logical groups instead of repeatedly editing IP-based rules. Reuse ASGs across multiple NSGs to enforce consistent, layered network security policies.
</Callout>

## References

* Azure Application Security Groups documentation: [https://learn.microsoft.com/azure/virtual-network/application-security-groups](https://learn.microsoft.com/azure/virtual-network/application-security-groups)
* Azure Network Security Groups documentation: [https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)

Now proceed to the next topic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f311416f-4844-43ee-bc18-4ad6b6f0b71a/lesson/8a3904d2-0c99-4395-baea-7ffddaa6aae4" />
</CardGroup>


# Creating NSG rules

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-and-configure-Network-Security-Groups/Creating-NSG-rules/page

Guide to creating and managing Azure Network Security Group rules, covering rule components, service tags, portal walkthroughs, subnet versus NIC evaluation, and outbound rule examples.

In this lesson we'll learn how to create Network Security Group (NSG) rules in Azure, how each component of a rule works, and how rules from multiple NSGs are evaluated together. This guide keeps the original step sequence and diagrams while improving clarity and SEO for quick reference.

Key concepts covered:

* What to specify when creating NSG rules
* Service tags and why to use them
* Portal walkthrough: create NSG, add inbound/outbound rules
* Subnet vs NIC NSGs and Effective security rules
* Practical outbound example using service tags

## NSG rule components (at a glance)

| Component            | Purpose                                                                                                     | Example / Notes                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Service              | Pick a well-known service to auto-populate ports (RDP, SSH, HTTPS, etc.) or choose `Custom` to enter a port | `SSH` → TCP `22`                      |
| Port ranges          | Single ports, ranges, or multiple non-contiguous values separated by commas                                 | `22`, `80-90`, `22-30,45,55`          |
| Priority             | Numeric value evaluated in ascending order; lower number = higher precedence                                | `100` (higher precedence than `200`)  |
| Source / Destination | IP ranges, Service Tags, Application Security Groups, or `Any`                                              | `10.1.0.0/24`, `Service Tag: Storage` |
| Action               | Whether to `Allow` or `Deny` the matched traffic                                                            | `Allow` or `Deny`                     |

<Frame>
  <img alt="The image shows a form for adding an inbound security rule in a network security group (NSG) setup, specifying criteria like source, destination, port range, protocol, action, and rule name." />
</Frame>

<Callout icon="lightbulb">
  Lower numeric priority means higher precedence — the rule with the smallest numeric priority is evaluated first.
</Callout>

## Service tags — simplify rule maintenance

Managing IP ranges for cloud services is error-prone. Azure service tags are predefined labels that represent groups of IP address ranges used by Azure services (for example: `VirtualNetwork`, `Storage`, `Internet`, `LoadBalancer`). Use service tags in your source/destination fields to avoid maintaining large IP lists — Azure updates these tags automatically.

<Frame>
  <img alt="The image illustrates the use of service tags in a Network Security Group (NSG) to manage network traffic, showing rules to allow Azure service traffic while denying internet outbound access. It highlights actions, sources, destinations, and ports in a table format, along with benefits like predefined labels and automatic updates." />
</Frame>

## Hands-on: Azure portal walkthrough

This example uses a set of VMs in a VNet where NSGs have not yet allowed inbound SSH. By default, inbound SSH from the Internet will be blocked until you create an appropriate NSG rule.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface, specifically the network settings for a virtual machine named &#x22;vm-nsg-lab-1&#x22;. It lists details like public and private IP addresses and configurations for network security groups." />
</Frame>

Attempting to SSH directly to a VM without an NSG allowing SSH will fail:

```bash theme={null}
ssh kodeloud@172.191.36.135
