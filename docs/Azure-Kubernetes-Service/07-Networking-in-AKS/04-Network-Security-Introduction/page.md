# Network Security Introduction

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Networking-in-AKS/Network-Security-Introduction/page

Securing Azure Kubernetes Service clusters through networking options, CNI plugins, and network policies to enhance security posture.

Securing your Azure Kubernetes Service (AKS) cluster begins with a solid network foundation. In this lesson, we’ll examine the main networking options in AKS—including CNI plugins and network policies—and how they shape your cluster’s security posture.

## Lesson Agenda

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Agenda&#x22; with three topics: Networking Options, Configuration Options, and Networking Policies, each accompanied by an icon." />
</Frame>

We’ll explore:

1. Virtual networks, subnets, Network Security Groups (NSGs), and User-Defined Routes (UDRs)
2. Kubernetes CNI vs. Azure CNI
3. Network policies in AKS

## Part 1: Virtual Networks, Subnets, NSGs, and UDRs

<Frame>
  ![The image shows a section titled "Networking Security" with a checkmark next to "Virtual Networks, Subnets, NSGs, and UDRs."](../../../../images/kodekloud.com/kk-media/image/upload/v1752869499/notes-assets/images/Azure-Kubernetes-Service-Network-Security-Introduction/networking-security-virtual-networks-checkmark.jpg)
</Frame>

In this section, we review the building blocks of Azure networking:

| Component                    | Description                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------- |
| Virtual Network (VNet)       | Provides an isolated, private network for your AKS cluster.                                       |
| Subnet                       | Segments a VNet into smaller address spaces for different workloads.                              |
| Network Security Group (NSG) | Applies inbound/outbound traffic rules at the subnet or network interface level.                  |
| User-Defined Route (UDR)     | Overrides Azure’s default system routes to direct traffic through custom appliances or firewalls. |

## Links and References

* [Azure Virtual Network Concepts](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)
* [AKS Networking Overview](https://learn.microsoft.com/azure/aks/concepts-network)
* [Network Security Groups Overview](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)
* [User-Defined Routes in Azure](https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/96320ff1-0141-4a5f-ab22-ed42e7995612/lesson/36d2cea7-cd10-474e-b627-2f4abd4b9975" />
</CardGroup>
