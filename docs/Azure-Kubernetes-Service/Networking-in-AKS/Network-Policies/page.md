# Create a VNet with a /16 CIDR block (up to 65,534 addresses)
az network vnet create \
  --resource-group MyResourceGroup \
  --name VNet1 \
  --address-prefixes 10.2.0.0/16
```

<Callout icon="lightbulb">
  Use IP address management (IPAM) tools or Azure’s built-in features to plan non-overlapping CIDR blocks across multiple VNets.
</Callout>

## Subnets

A **subnet** segments your VNet’s address space into smaller networks, enabling you to group and isolate resources like VMs or AKS nodes.

Example CLI:

```bash theme={null}
# Create two /24 subnets within VNet1
az network vnet subnet create \
  --resource-group MyResourceGroup \
  --vnet-name VNet1 \
  --name SubnetA \
  --address-prefixes 10.2.1.0/24

az network vnet subnet create \
  --resource-group MyResourceGroup \
  --vnet-name VNet1 \
  --name SubnetB \
  --address-prefixes 10.2.2.0/24
```

<Callout icon="triangle-alert">
  Subnets within the same VNet must not have overlapping CIDR ranges.
</Callout>

## Network Security Groups (NSGs)

A **Network Security Group (NSG)** acts as a virtual firewall at the subnet or NIC level. NSGs include inbound and outbound rules to allow or deny traffic based on source/destination IP, port, and protocol.

Example CLI:

```bash theme={null}
# Create an NSG and attach it to SubnetA
az network nsg create \
  --resource-group MyResourceGroup \
  --name MyNSG

az network vnet subnet update \
  --resource-group MyResourceGroup \
  --vnet-name VNet1 \
  --name SubnetA \
  --network-security-group MyNSG
```

<Callout icon="lightbulb">
  Azure NSGs include default rules permitting VNet-to-VNet traffic and outbound internet traffic. Customize NSGs to enforce your security policies.
</Callout>

## Route Tables & User-Defined Routes (UDRs)

A **Route Table** is a set of routes that control packet forwarding within a VNet. Azure populates it with:

* **System routes** (default Azure routes)
* **BGP routes** (learned via ExpressRoute or VPN)
* **User-Defined Routes (UDRs)**

UDRs let you override default routing—for instance, to direct traffic through a firewall appliance.

Example CLI:

```bash theme={null}
# Create a route table
az network route-table create \
  --resource-group MyResourceGroup \
  --name MyRouteTable

# Add a UDR to route all internet-bound traffic via a virtual appliance
az network route-table route create \
  --resource-group MyResourceGroup \
  --route-table-name MyRouteTable \
  --name InternetRoute \
  --address-prefix 0.0.0.0/0 \
  --next-hop-type VirtualAppliance \
  --next-hop-ip-address 10.2.1.4

# Associate the route table with SubnetA
az network vnet subnet update \
  --resource-group MyResourceGroup \
  --vnet-name VNet1 \
  --name SubnetA \
  --route-table MyRouteTable
```

## VNet Peering

To enable low-latency, high-bandwidth connectivity between VNets (within or across regions), configure **VNet Peering**.

Example CLI:

```bash theme={null}
# Peer VNet1 with VNet2
az network vnet peering create \
  --name VNet1-to-VNet2 \
  --resource-group MyResourceGroup \
  --vnet-name VNet1 \
  --remote-vnet /subscriptions/.../resourceGroups/MyResourceGroup/providers/Microsoft.Network/virtualNetworks/VNet2 \
  --allow-vnet-access
```

<Frame>
  ![The image shows a diagram of three virtual networks (VNet1, VNet2, VNet3), each containing two subnets with network security groups and other components.](https://kodekloud.com/kk-media/image/upload/v1752869496/notes-assets/images/Azure-Kubernetes-Service-Azure-Networking-Fundamentals/virtual-networks-diagram-subnets-security-groups.jpg)
</Frame>

## Quick Reference

| Component   | Description                                        | CLI Example                                                                                                                                                                |
| ----------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VNet        | Private IP address space                           | `az network vnet create --resource-group RG --name VNet1 --address-prefixes 10.2.0.0/16`                                                                                   |
| Subnet      | Subdivision of a VNet                              | `az network vnet subnet create --resource-group RG --vnet-name VNet1 --name SubnetA --address-prefixes 10.2.1.0/24`                                                        |
| NSG         | Virtual firewall                                   | `az network nsg create --resource-group RG --name MyNSG`                                                                                                                   |
| Route Table | Collection of system, BGP, and user-defined routes | `az network route-table create --resource-group RG --name MyRouteTable`                                                                                                    |
| Route       | Custom path (UDR)                                  | `az network route-table route create --resource-group RG --route-table-name MyRouteTable --name InternetRoute --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance` |

## Links and References

* [Azure Virtual Networks](https://docs.microsoft.com/azure/virtual-network/virtual-networks-overview)
* [CIDR Notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
* [Azure Network Security Groups](https://docs.microsoft.com/azure/virtual-network/network-security-groups-overview)
* [Azure Route Tables & UDRs](https://docs.microsoft.com/azure/virtual-network/virtual-networks-udr-overview)
* [Virtual Network Peering](https://docs.microsoft.com/azure/virtual-network/virtual-network-peering-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/96320ff1-0141-4a5f-ab22-ed42e7995612/lesson/557470cd-bffb-49db-9376-30ca8743e3ab" />
</CardGroup>


# Network Policies

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Networking-in-AKS/Network-Policies/page

This article explains the use of Kubernetes Network Policies in Azure Kubernetes Service for controlling pod traffic and addressing limitations of Azure Network Security Groups.

Modern container networking demands more than subnet-level filtering. While Azure Network Security Groups (NSGs) can secure inbound and outbound traffic—including Azure CNI–provisioned pods—their reliance on static IPs makes them ill-suited for dynamic Kubernetes pods. NSG rules tied to pod IPs break when pods restart, and NSGs can’t filter by Kubernetes labels (for example, blocking traffic from `secure` pods to `unsecure` pods). Kubernetes Network Policies fill this gap by enabling label-based, pod-to-pod traffic controls.

## Limitations of Azure NSGs in AKS

* Pod IPs are ephemeral; NSG rules must be constantly updated.
* NSGs cannot reference Kubernetes constructs like namespaces or labels.
* Fine-grained policy (e.g., “allow traffic only from pods with label `app=frontend`”) requires a native Kubernetes mechanism.

## Kubernetes Network Policies

A `NetworkPolicy` is a native Kubernetes API object for controlling pod traffic. You define policies in YAML, selecting pods by labels and specifying allowed ingress and egress flows.

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: demo-policy
  namespace: demo
spec:
  podSelector:
    matchLabels:
      role: server
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
  egress:
  - to:
    - ipBlock:
        cidr: 10.2.0.0/22
      ports:
      - port: 80
```

| Policy Type | Description                                  |
| ----------- | -------------------------------------------- |
| Ingress     | Controls incoming traffic to selected pods   |
| Egress      | Controls outgoing traffic from selected pods |

<Callout icon="lightbulb">
  When at least one `NetworkPolicy` selects a pod, all other traffic is denied by default. Be sure to explicitly allow the flows your application requires.
</Callout>

For more details, see [NetworkPolicy | Kubernetes Concepts](https://kubernetes.io/docs/concepts/services-networking/network-policies/).

## Azure Network Policy Engine

Azure’s built-in network policy engine runs as a DaemonSet on every node. It watches `NetworkPolicy` objects and enforces rules using:

* **Linux nodes**: iptables + Linux bridge
* **Windows nodes** (preview): Host Networking Service (HNS) ACLs

This engine integrates with Azure CNI and the Azure Policy Manager.

<Frame>
  ![The image illustrates Azure Network Policies within a Kubernetes cluster, showing components like secure and unsecure labels, Linux Kernel, IP Tables, Bridge, Azure CNI, and Azure Policy Manager.](https://kodekloud.com/kk-media/image/upload/v1752869497/notes-assets/images/Azure-Kubernetes-Service-Network-Policies/azure-network-policies-kubernetes-diagram.jpg)
</Frame>

Azure Network Policies are the default in AKS for both Linux and Windows (Windows support is preview). You can also install the Azure policy engine on self-managed AKS clusters running on Azure VMs.

## Calico Network Policies

Calico by Tigera is an open-source networking and network security solution. It implements the Kubernetes `NetworkPolicy` API and extends it with additional features:

* GlobalNetworkPolicy for cross-namespace rules
* NetworkSets and ServiceSets for object grouping
* Integrated logging and compliance profiles

You can deploy Calico on AKS as a first-party add-on. Key differences between Azure and Calico network policies include supported platforms, networking modes, compliance features, and observability.

<Frame>
  ![The image is a comparison table of Azure and Calico policies, detailing capabilities such as supported platforms, networking options, compliance, features, support, and logging.](https://kodekloud.com/kk-media/image/upload/v1752869498/notes-assets/images/Azure-Kubernetes-Service-Network-Policies/azure-calico-policies-comparison-table.jpg)
</Frame>

<Callout icon="triangle-alert">
  If you choose Calico, Microsoft support engineers may not diagnose issues stemming from Calico components. For troubleshooting, refer to the [Calico documentation](https://docs.projectcalico.org/).
</Callout>

## Troubleshooting Network Policies

To view policy enforcement logs for either engine:

```bash theme={null}
kubectl logs -n kube-system <network-policy-pod>
```

Replace `<network-policy-pod>` with the DaemonSet pod name (e.g., `azure-npm-daemonset` or `calico-node-xxxxx`).

## Links and References

* [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Azure CNI Networking](https://docs.microsoft.com/azure/aks/configure-azure-cni)
* [Calico Documentation](https://docs.projectcalico.org/)
* [Azure NSG Overview](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/96320ff1-0141-4a5f-ab22-ed42e7995612/lesson/5d356f44-3b56-4562-91df-e9f7092252bd" />
</CardGroup>
