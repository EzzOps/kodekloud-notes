# No response or connection refused because inbound SSH is not allowed by default
```

### Create an NSG

1. In the Azure portal, go to **Network Security Groups** → **Create**.
2. Provide a name (for example, `NSGLab01`) and the target region (e.g., `East US`), then click **Review + create** and complete creation.
3. Open the NSG resource to inspect default rules.

Default inbound rules include (examples):

| Default Rule                    | Priority | Purpose                                             |
| ------------------------------- | -------- | --------------------------------------------------- |
| `AllowVNetInbound`              | 65000    | Allows traffic within the virtual network           |
| `AllowAzureLoadBalancerInbound` | 65001    | Allows load balancer health probes                  |
| `DenyAllInbound`                | 65500    | Denies other inbound traffic not explicitly allowed |

Default outbound rules typically include:

* `AllowVNetOutbound`
* `AllowInternetOutbound`
* `DenyAllOutbound` (catch-all)

These defaults explain why VMs inside the same VNet can communicate, but inbound Internet traffic is blocked unless explicitly allowed.

### Associate the NSG

* Associate your new NSG to the target subnet (or to a NIC for per-VM interface control). In this walkthrough, the NSG is associated with the subnet containing the VMs.

### Add an inbound rule for SSH

1. Go to the NSG → **Inbound security rules** → **Add**.
2. Configure:
   * Source: `Any` (or restrict to a specific IP, `My IP`, a service tag, or an Application Security Group)
   * Source port ranges: `*` (or specify if needed)
   * Destination: `Any`
   * Service: `SSH` (auto-populates TCP port `22`)
   * Action: `Allow`
   * Priority: `100` (lower number = higher precedence)
   * Name: `AllowAny_SSH_Inbound`
   * Optional: add a description
3. Click **Add**.

> **warning** Opening SSH (port 22) to `Any` exposes the VM to the Internet. Restrict the Source to known IPs or use Just-in-Time VM access where possible.

A caution symbol may appear in the portal indicating the rule is open to the Internet — use that as a reminder to minimize attack surface.

<Frame>
  <img alt="The image shows the inbound security rules for a network security group in Microsoft Azure. It lists several rules with priorities, names, ports, protocols, sources, destinations, and actions (allow or deny)." />
</Frame>

After adding the rule, you should be able to SSH to the VMs in that subnet:

```bash theme={null}
ssh kodeloud@172.191.36.135
# SSH server fingerprint prompt:
# The authenticity of host '172.191.36.135 (172.191.36.135)' can't be established.
# ED25519 key fingerprint is SHA256:vdKNh1gNzy8gUjET7o7oJz+sVIl/TQxmTtrRV6kwBQ.
# Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
# kodeloud@vm-nsg-lab-1's password:
# Last login: Sun Aug 24 19:08:57 on pts/0
```

Because the rule was applied at the subnet level, all VMs in that subnet inherit the SSH access.

## Effective security rules and NIC-level NSGs

You can apply NSGs at both the subnet and network interface (NIC) levels. Traffic must be allowed by every applicable NSG for the flow to succeed; a `Deny` at either level blocks traffic.

* Example workflow:
  1. Create a second NSG and assign it to the NIC of `VM3`.
  2. If SSH is allowed at the subnet level but denied at the NIC NSG, SSH to that VM will fail.

To inspect the combined effect of subnet + NIC NSGs:

* Go to the VM → **Networking** → select the NIC → **Effective security rules**. This displays aggregated inbound/outbound rules and which rule ultimately allows or denies traffic.

<Frame>
  <img alt="The image shows a screenshot of the Microsoft Azure portal displaying a list of virtual machines, including details such as name, subscription, resource group, location, status, operating system, size, public IP address, and number of disks." />
</Frame>

<Frame>
  <img alt="The image shows a Microsoft Azure portal indicating that a deployment named &#x22;CreateNetworkSecurityGroupBladeV2&#x22; is complete. It provides options to view deployment details, go to the resource, and manage cost alerts." />
</Frame>

<Frame>
  <img alt="The image shows the network settings of a virtual machine in Microsoft Azure portal, detailing network interfaces and IP configurations alongside various networking options and settings." />
</Frame>

<Frame>
  <img alt="The image shows the &#x22;Effective security rules&#x22; interface for a network security group in Microsoft Azure, displaying inbound and outbound rules with details about priorities, source and destination ports, protocols, and access status." />
</Frame>

## Outbound example using service tags (deny Internet, allow Storage)

This example demonstrates how to block general Internet outbound access while allowing Azure Storage access by using service tags.

From the VM, a curl to a blob returns binary content (use `--output` or `-o` to save instead of printing binary to terminal):

```bash theme={null}
# On the VM:
curl https://cskodekloudaz01.blob.core.windows.net/vision/note.jpeg
# Warning: Binary output can mess up your terminal. Use "--output -" to tell
# Warning: <FILE> to save to a file.
```

To block Internet outbound but allow Storage:

1. In the NSG attached to the VM/subnet, add an outbound Deny rule:
   * Source: `Any`
   * Destination: `Service Tag` → `Internet`
   * Destination port ranges: `*`
   * Action: `Deny`
   * Priority: `200`
   * Name: `Deny_Internet`
2. This will override the default `AllowInternetOutbound` (priority 65001) because `200` is a smaller number and thus has higher precedence.

<Frame>
  <img alt="The image shows the Azure portal interface, specifically the network settings for a virtual machine, where an outbound security rule is being configured. The rule involves setting parameters like source, destination, protocol, and port ranges." />
</Frame>

After adding the deny rule, outbound Internet access from the VM is blocked:

```bash theme={null}
# On the VM:
curl https://www.microsoft.com
# curl: (7) Failed to connect to www.microsoft.com port 443: Connection refused
```

To permit Storage access while Internet is denied:

1. Add an outbound Allow rule:
   * Source: `Any`
   * Destination: `Service Tag` → `Storage`
   * Destination port ranges: `443,80` (or the ports you need)
   * Action: `Allow`
   * Priority: `100` (higher precedence than `Deny_Internet`)
   * Name: `Allow_Storage`

You may specify multiple ports or CIDR ranges separated by commas (for example, `10.1.1.0/24,10.1.2.0/24`) if you prefer IP-based rules.

After adding the Allow Storage rule:

```bash theme={null}
# On the VM:
curl --output note.jpeg https://cskodekloudaz01.blob.core.windows.net/vision/note.jpeg
# (File downloads to note.jpeg)
curl https://www.microsoft.com
# curl: (7) Failed to connect to www.microsoft.com port 443: Connection refused
```

Service tags make this simpler because `Storage` includes all necessary Azure storage IP ranges; you don't need to keep a manual list of IPs.

## Summary

* Use predefined Services for common ports or `Custom` for custom ports. You can specify single ports, ranges, and comma-separated lists for complex needs.
* Priority numbers are evaluated ascending; lower numeric values take precedence.
* NSGs may be applied at both Subnet and NIC levels. Traffic must be allowed by all applicable NSGs—any deny blocks the flow.
* Prefer Service Tags to reference Azure services (Storage, Internet, VirtualNetwork, etc.) to reduce administrative overhead and rely on Azure-managed IP updates.
* Always minimize exposure when allowing management ports (SSH/RDP). Restrict sources or use Just-in-Time access where possible.

## Links and References

* [Azure Network Security Groups documentation](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)
* [Azure service tags documentation](https://learn.microsoft.com/azure/virtual-network/service-tags-overview)
* [Just-in-Time VM access (Azure Security Center)](https://learn.microsoft.com/azure/security-center/security-center-just-in-time)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f311416f-4844-43ee-bc18-4ad6b6f0b71a/lesson/97004db6-a2b6-4f47-8a82-dbfe47002090)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-and-configure-Network-Security-Groups/Introduction/page

Guide to deploying and configuring Azure Network Security Groups, explaining default rules, effective rule calculation, custom rules, service tags, and application security groups

Deploy and configure Network Security Groups (NSGs) in Azure to control traffic flow to and from resources connected to Virtual Networks. NSGs are a fundamental building block for network security in Azure—think of them as traffic controllers that evaluate and permit or deny traffic based on rules you define.

What you'll learn in this lesson:

* The core concept of NSGs and why they are critical for cloud network access control.
* The default inbound and outbound rules that come with every NSG and the rationale behind them.
* How Azure determines the final, effective rule set when NSGs are applied at both subnet and NIC (network interface) levels.
* How to author custom rules to enforce specific security requirements.
* How service tags simplify rule creation for Azure-managed IP ranges.
* How Application Security Groups (ASGs) let you group VMs logically and use those groups within NSG rules.

<Frame>
  <img alt="The image is a slide titled &#x22;Learning Objectives&#x22; with three main points: understanding NSGs and network access control, identifying default NSG rules, and learning how effective rules are calculated at subnet and NIC levels." />
</Frame>

> **lightbulb** Before you start: familiarity with Azure Virtual Networks, subnets, and basic VM networking concepts will help you apply NSGs effectively. For detailed platform documentation, see the [Azure Network Security Groups overview](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview).

Why this matters for security and operations:

* NSGs provide fine-grained control over traffic at the subnet and NIC level, enabling least-privilege network access.
* Default rules provide safety and connectivity out of the box but may not meet your security posture—understanding them prevents accidental exposure.
* Combining NSGs with service tags and ASGs improves manageability and scalability as your environment grows.

Topics at a glance

| Topic                              | What you'll get                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| NSG fundamentals                   | Clear conceptual explanation and usage patterns for Azure NSGs                   |
| Default NSG rules                  | Which default rules exist and why Azure includes them                            |
| Effective rules calculation        | How rules at subnet + NIC are combined to produce the final permit/deny decision |
| Custom rules                       | How to craft priority and direction for secure traffic controls                  |
| Service tags                       | How to reference Azure services by tag instead of IP addresses                   |
| Application Security Groups (ASGs) | How to group VMs and apply NSG rules to groups rather than individual NICs       |

By the end of this lesson you'll understand NSGs both conceptually and practically, and you will be ready to design and deploy NSGs that meet your security requirements while keeping operational overhead manageable.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f311416f-4844-43ee-bc18-4ad6b6f0b71a/lesson/3e8b35be-b141-489c-9acb-2bc9664471bd)
