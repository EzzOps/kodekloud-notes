# Configure Azure Route Server

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Implement-Virtual-Network-Traffic-Routing/Configure-Azure-Route-Server/page

Explains Azure Route Server, a managed BGP service that automates route exchange between BGP devices and Azure virtual networks to simplify dynamic routing for hybrid hub and spoke architectures.

Configuring Azure Route Server

In this lesson we cover one of Azure’s most powerful — and often misunderstood — managed networking services: Azure Route Server. This service automates route exchange between BGP-capable devices and your Azure virtual network, reducing manual route table management as your cloud environment scales. By the end of this lesson you’ll understand what Azure Route Server does, when to use it, and how it simplifies routing for complex architectures.

Conceptual overview

On the left of the diagram is the on‑premises network connecting through an SD‑WAN device. On the right is a firewall device that connects to the Internet. In the center is Azure Route Server, deployed in its own dedicated subnet within the virtual network. Both the SD‑WAN device and the firewall peer with Azure Route Server using BGP (Border Gateway Protocol). Application VMs in their subnets receive routing information that Azure Route Server learned via BGP, so traffic flows to the correct next hop — back to on‑premises via SD‑WAN, out to the Internet via the firewall, or to other Azure resources.

Azure Route Server learns routes published by on‑premises devices and advertises those learned routes into the virtual network. Effective routes for each VM will show next hops such as the SD‑WAN for on‑premises traffic, the firewall for Internet bound traffic, or the VM for local traffic.

A practical example: when deploying Azure VMware Solution (AVS), AVS uses ExpressRoute and speaks BGP. If you have another ExpressRoute in a hub and there is no Global Reach between circuits, Azure Route Server can bridge routing by learning and propagating routes between them. With a BGP-capable network virtual appliance (NVA) peered to the Route Server, routes learned from AVS can be propagated to on‑premises and vice versa. In short: Azure Route Server learns BGP routes and serves all connected devices, enabling dynamic, managed route propagation across hybrid architectures.

Now let's break down the key ideas behind Azure Route Server.

<Frame>
  <img alt="The image illustrates the configuration of an Azure Route Server, showing connections between On-Premises, Internet, and app subnets through BGP, with associated routing tables. It includes an example of effective routes for a virtual machine." />
</Frame>

Key features and behavior

* Automates route exchange: Azure Route Server automates the exchange of routing information between your BGP‑capable network appliances (for example, NVAs, firewalls, SD‑WAN devices) and virtual networks. You do not need to update route tables manually when the network topology changes.
* Requires BGP support: The appliances you connect must support BGP so Azure Route Server can dynamically learn and share routes.
* Real‑time updates and failover: If a route changes — for example, a primary firewall fails and traffic must use a backup path — Azure Route Server propagates updated routing in real time so traffic continues with minimal interruption.
* Dedicated subnet: Azure Route Server must be deployed into a dedicated subnet named `RouteServerSubnet` in the virtual network. This subnet is reserved for the Route Server’s control plane.
* Enterprise networking pattern: Route Server brings dynamic BGP routing to Azure in a managed form, aligning Azure networking behavior with large on‑premises networks. This reduces manual configuration, improves route visibility and convergence, and simplifies failover and scaling.

Best practices (quick reference)

| Topic             | Recommendation                                                 | Example / Notes                                                                        |
| ----------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Subnet            | Use a dedicated subnet named `RouteServerSubnet`               | Do not place other workloads in this subnet.                                           |
| Peer devices      | Ensure NVAs and edge devices support BGP                       | Typical peers: firewalls, SD‑WAN appliances, routers.                                  |
| Route propagation | Validate advertised prefixes and ASNs                          | Avoid accidentally leaking default routes to application subnets.                      |
| High availability | Pair Route Server with HA NVAs and redundant paths             | Monitor BGP session status and route convergence times.                                |
| Use cases         | Hybrid connectivity, AVS peering, multi‑ExpressRoute scenarios | Route Server is especially useful when global reach is not available between circuits. |

> **lightbulb** Azure Route Server requires BGP‑capable peers and a dedicated subnet named `RouteServerSubnet`. Ensure your NVAs or edge devices support BGP before deployment.

How Azure Route Server fits into common architectures

* Hybrid connectivity: Learn on‑premises prefixes via BGP and advertise them to application subnets; learn Azure prefixes and advertise them back to on‑premises through BGP peers.
* Hub-and-spoke with NVAs: Place the Route Server in a hub VNet and peer NVAs to offload route management; spokes receive advertised routes without manual route table updates.
* Multi‑ExpressRoute / AVS scenarios: When multiple ExpressRoute circuits cannot directly share routes (no Global Reach), Route Server can facilitate route exchange through a BGP-capable NVA.

Summary

Azure Route Server is a managed BGP service that automates dynamic route exchange between Azure virtual networks and BGP-capable appliances. It reduces manual route table management, improves failover behavior, and enables complex hybrid topologies to converge quickly. Use Route Server when you need dynamic route propagation across NVAs, ExpressRoute/AVS environments, or multi‑site network designs.

Links and references

* [Azure Route Server documentation (Microsoft)](https://learn.microsoft.com/azure/route-server)
* [Overview of BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)
* [Azure VMware Solution (AVS)](https://learn.microsoft.com/azure/azure-vmware/)
* [Designing a hub‑and‑spoke network in Azure](https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/hub-spoke)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/3289c34c-80e6-417c-af60-54cbbcee3f01/lesson/931ebe5c-e7d2-4ceb-a01d-10a3d254e4bc)
