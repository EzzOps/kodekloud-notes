# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explain-Virtual-Network-Service-Endpoints/Introduction/page

Explains Azure Virtual Network Service Endpoints, benefits, supported services, how to enable them on subnets, configuration examples, and comparison with Azure Private Endpoints.

This lesson explains Azure Virtual Network Service Endpoints and shows how to add them to a subnet.

Azure Virtual Network Service Endpoints enable resources inside your virtual network (VMs, App Services, AKS nodes, etc.) to connect to specific Azure platform services—such as Storage, SQL Database, and Cosmos DB—over the Microsoft Azure backbone. This keeps traffic off the public internet, reduces exposure, and lets you lock down service access to particular subnets.

What you will learn:

* What a Service Endpoint is and how it works
* How to add Service Endpoints to a subnet

<Frame>
  <img alt="The image shows a slide titled &#x22;Learning objectives&#x22; with two points: understanding what a Service Endpoint is and adding Service Endpoints to a subnet." />
</Frame>

By the end of this lesson you’ll be able to securely access Azure platform services from within your virtual network and restrict those services to chosen subnets.

> **lightbulb** Service Endpoints extend your VNet identity to supported Azure services so you can apply service-level network restrictions (for example, firewall rules or resource-level access) scoped to one or more subnets.

## What is a Service Endpoint?

A Service Endpoint is a virtual network-level feature that provides secure, direct connectivity from a subnet to specific Azure platform services over the Azure backbone network. When a Service Endpoint is enabled on a subnet, traffic between resources in that subnet and the Azure service stays on Microsoft’s network rather than traversing the public internet.

Core characteristics:

* Uses the Azure backbone for traffic between your VNet and supported Azure services.
* Lets you configure service-level firewall rules to allow traffic only from selected subnets.
* Is configured per-subnet and per-service type (for example, `Microsoft.Storage`).

## Why use Service Endpoints?

* Improved security: traffic does not leave the Microsoft network.
* Access control: restrict Azure service access to specific subnets or VNets.
* Simplicity: minimal changes to application code; works with existing public endpoints but enforces subnet-based access control.
* Lower latency and improved reliability compared to internet paths.

> **warning** Service Endpoints do not assign private IPs to Azure services. If you need private connectivity with private IP addresses (for full network isolation), use Azure Private Endpoint instead.

## Supported services (examples)

| Azure Service        | Typical Use Case                                        |
| -------------------- | ------------------------------------------------------- |
| Microsoft.Storage    | Secure access to Storage Accounts from VMs and services |
| Microsoft.Sql        | Restrict Azure SQL Database access to VNets/subnets     |
| Microsoft.KeyVault   | Limit Key Vault access to application subnets           |
| Microsoft.DocumentDB | Cosmo DB network restrictions                           |

For a complete and up-to-date list of supported services, see the official Azure documentation: [Virtual network service endpoints documentation](https://learn.microsoft.com/azure/virtual-network/virtual-network-service-endpoints-overview).

## How to add a Service Endpoint to a subnet

You can enable Service Endpoints using the Azure portal, Azure CLI, PowerShell, or an ARM/Terraform template. Enabling is done at the subnet level and is scoped to one or more service types.

Examples:

* Azure CLI

```bash theme={null}
