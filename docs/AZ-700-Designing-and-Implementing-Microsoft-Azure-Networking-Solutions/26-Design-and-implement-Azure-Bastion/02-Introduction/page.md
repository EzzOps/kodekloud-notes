# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-implement-Azure-Bastion/Introduction/page

Overview of Azure Bastion, a managed service that provides secure browser-based RDP and SSH access to VMs over TLS without exposing VMs to the public internet.

In this lesson we focus on Azure Bastion — a managed Azure service that provides secure, seamless access to virtual machines directly through the Azure portal.

Azure Bastion enables RDP and SSH connectivity to your VMs without exposing those VMs to the public internet. It acts as a broker inside your virtual network and tunnels RDP/SSH traffic over TLS (port 443) using an HTML5-based client in the portal, removing the need for public IPs on your VMs.

## Learning objectives

By the end of this lesson you will be able to:

* Explain how Azure Bastion fits into a virtual network and how it tunnels RDP/SSH over TLS.
* Identify deployment requirements and follow basic configuration steps (for example, the required `AzureBastionSubnet` with a recommended `/26` or larger prefix).
* Connect to virtual machines via Azure Bastion from the Azure portal.
* Recognize common operational and security considerations (no inbound VM public IPs, portal-based connections, and platform-managed scaling).

> **lightbulb** Azure Bastion uses an HTML5 client over TLS (port 443) in the Azure portal, so you can connect to VMs from most modern browsers without installing any client-side RDP/SSH tools.

## What is Azure Bastion?

Azure Bastion is a PaaS service deployed into your virtual network (VNet). It provides:

* Secure RDP and SSH connectivity to VMs via the Azure portal.
* No need to open inbound ports on the VM’s network security group or assign public IPs to VMs.
* Platform-managed scaling and maintenance handled by Azure.

## How Azure Bastion works (high-level)

1. Deploy Azure Bastion into your VNet using a dedicated subnet named `AzureBastionSubnet`.
2. The Bastion host receives RDP/SSH connections from the Azure portal client over TLS (port 443).
3. Bastion brokers these connections to VMs inside the same VNet using private IP addresses.
4. No public IPs are assigned to the target VMs, reducing exposure to the public internet.

## Deployment requirements and basic configuration

The important prerequisites and configuration steps are:

* A virtual network (VNet) where Bastion will be deployed.
* A subnet named `AzureBastionSubnet` (required name).
* A recommended subnet size of `/26` or larger to allow for scale and additional hosts.
* A Bastion host requires a public IP (managed by the Bastion resource), but your VMs do not.
* Appropriate network security group (NSG) rules that allow required outbound connections from Bastion (for example, to target VMs and Azure platform services).

> **warning** Create a dedicated subnet named `AzureBastionSubnet` BEFORE deploying Bastion. Use a prefix of `/26` or larger to avoid capacity and scaling issues. Do not reuse existing subnets for Bastion.

### Quick reference table

| Requirement   | Description                             | Example                              |
| ------------- | --------------------------------------- | ------------------------------------ |
| Subnet name   | Must be `AzureBastionSubnet`            | `AzureBastionSubnet`                 |
| Subnet size   | Recommended `/26` or larger             | `10.0.0.0/26`                        |
| Client access | HTML5 client via Azure portal over TLS  | Port `443`                           |
| VM public IPs | Not required — Bastion uses private IPs | N/A                                  |
| Scaling       | Platform-managed by Azure               | Automatic scaling behind the service |

## Typical deployment flow

1. Create or select a VNet.
2. Create the `AzureBastionSubnet` with the recommended prefix.
3. Deploy the Azure Bastion resource into that subnet and assign (or allow Azure to create) a public IP for the Bastion host.
4. From the Azure portal, navigate to the VM and choose "Connect" → "Bastion" to start an RDP/SSH session through the portal.

## Benefits and operational considerations

* Security: No inbound ports to VMs, reducing attack surface.
* Simplicity: Browser-based access requires no client-side RDP/SSH tools.
* Manageability: Azure handles scaling, updates, and high availability as part of the service.
* Limitations: Ensure proper subnet sizing and consider network design when peering VNets or using custom routing/NAT solutions.

## Links and references

* [Azure Bastion documentation (Microsoft)](https://learn.microsoft.com/azure/bastion/)
* [Azure Virtual Network documentation](https://learn.microsoft.com/azure/virtual-network/)
* [Azure networking best practices](https://learn.microsoft.com/azure/architecture/best-practices/networking)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/fbd7bcc4-5539-49f4-abcb-c72fd0f106ee/lesson/feda3611-6db3-40a7-939e-5a7c4c6ea6de)
