# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Enable-Cross-VNet-Connectivity/Introduction/page

Guide to Azure Virtual Network peering, setup options, gateway sharing, and best practices.

Enabling cross-VNet connectivity in Azure lets you link separate virtual networks so resources can communicate privately and securely without traversing the public Internet. This module explains how to connect virtual networks (VNets) using VNet peering, the different peering types, configuration options, and scenarios where a shared gateway is useful.

## Learning objectives

By the end of this module you'll be able to:

* Describe what VNet peering is and why it's used
* Differentiate between regional peering and global peering
* Create a peering connection and choose the right peering options
* Understand permissions required for peering
* Configure gateway sharing across multiple VNets for on-premises connectivity

## Why use VNet peering?

VNet peering connects two virtual networks so they can exchange traffic over Azure’s private backbone. Benefits include:

* Low-latency, high-bandwidth connectivity between VNets
* Traffic stays on Microsoft’s network (no public Internet exposure)
* Simple routing between resources in peered VNets
* Supports hub-and-spoke topologies when combined with gateway sharing

> **lightbulb** VNet peering is ideal for scenarios that require fast, private network communication between services in different VNets—such as microservices split across VNets, cross-subscription applications, or multi-region deployments.

## Types of peering

| Peering type     | Scope                                                         | Use case                                           | Notes                                                                |
| ---------------- | ------------------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------- |
| Regional peering | VNets in the same Azure region                                | Low-latency communication within a region          | Typically lower latency and no additional regional egress charges    |
| Global peering   | VNets in different Azure regions (even different geographies) | Cross-region app communication, DR, geo-redundancy | May incur additional data transfer costs and slightly higher latency |

## Key peering options and what they do

When you create a peering, you’ll choose several options that affect traffic flow and gateway usage:

* Allow virtual network access: Enables traffic between the peered VNets.
* Allow forwarded traffic: Permits forwarded traffic from a network virtual appliance (NVA) in one VNet to reach resources in the peered VNet.
* Allow gateway transit (Use remote gateways / Allow gateway transit): Controls whether a VNet can use a gateway (VPN or ExpressRoute) in the peered VNet.
* Use remote gateways: Let a spoke VNet use the hub VNet’s gateway—only applicable when the hub has a gateway and the hub peering allows gateway transit.

> **warning** Peering is non-transitive: if VNet A is peered with VNet B and VNet B is peered with VNet C, A and C are not automatically peered. For hub-and-spoke, enable gateway transit on the hub and configure spokes to use the remote gateway.

## Permissions and requirements

* You need the appropriate role (for example, Network Contributor or Owner) on both VNets to create peering connections.
* VNets must have non-overlapping IP address spaces.
* Peering across subscriptions is supported, but both subscriptions must be associated with the same Azure Active Directory tenant (unless using Cross-subscription peerings with proper access).

## Steps to create a VNet peering

Below is a concise workflow you can follow in the Azure Portal, Azure CLI, or Azure PowerShell.

1. Decide which VNets to peer and validate non-overlapping address spaces.
2. On the first VNet, create a peering:
   * Name the peering (e.g., `vnetA-to-vnetB`)
   * Select the remote VNet (by subscription and resource)
   * Select options: Allow virtual network access, Allow forwarded traffic (if using NVAs), Allow gateway transit (if sharing a gateway)
3. On the second VNet, create a corresponding peering back to the first VNet (this establishes the two-way connection).
4. Verify peering status and update network security groups (NSGs) and route tables if necessary.

Example Azure CLI commands:

```bash theme={null}
