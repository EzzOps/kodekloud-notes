# Azure Networking Fundamentals

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Networking-in-AKS/Azure-Networking-Fundamentals/page

This lesson explores Azures core networking components for secure, scalable networking in Azure Kubernetes Service.

In this lesson, we’ll explore Azure’s core networking components—Virtual Networks (VNets), CIDR addressing, subnets, Network Security Groups (NSGs), Route Tables, and User-Defined Routes (UDRs). These building blocks form the foundation of secure, scalable networking for Azure Kubernetes Service (AKS).

## Table of Contents

1. [Virtual Networks (VNets) & CIDR Notation](#virtual-networks-vnets--cidr-notation)
2. [Subnets](#subnets)
3. [Network Security Groups (NSGs)](#network-security-groups-nsgs)
4. [Route Tables & User-Defined Routes (UDRs)](#route-tables--user-defined-routes-udrs)
5. [VNet Peering](#vnet-peering)
6. [Quick Reference](#quick-reference)
7. [Links and References](#links-and-references)

## Virtual Networks (VNets) & CIDR Notation

A **Virtual Network (VNet)** provides an isolated, private IP address space in Azure. VNets support both IPv4 and IPv6; this guide focuses on IPv4.

We define address ranges using **Classless Inter-Domain Routing (CIDR)** notation, which combines an IP address with its subnet mask.

Example CLI:

```bash theme={null}
