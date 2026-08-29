# ExpressRoute FastPath

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/ExpressRoute-Advanced-Features/ExpressRoute-FastPath/page

Explains Azure ExpressRoute FastPath, a feature that bypasses the virtual network gateway to improve data-plane throughput and latency, plus prerequisites, enabling steps, and validation tips

ExpressRoute FastPath is a performance feature that optimizes data throughput and reduces latency for ExpressRoute connections between on-premises networks and Azure virtual networks. FastPath improves packet-forwarding efficiency by removing the extra data hop through the virtual network gateway for qualified traffic, letting high-volume data-plane flows reach Azure VMs and services more directly.

Why use FastPath:

* Reduced latency for data-plane traffic.
* Higher packets-per-second and connections-per-second capacity.
* Lower processing load on the virtual network gateway, improving overall data-path performance.

<Frame>
  <img alt="The image illustrates the &#x22;ExpressRoute FastPath&#x22; network architecture, depicting the flow between on-premises networks, ExpressRoute, and Azure services like server farms and virtual networks. It includes elements like gateways, control and data planes, and mentions a &#x22;No Gateway Hop&#x22; feature." />
</Frame>

## How FastPath works

Two logical planes remain in the architecture:

* Data plane (FastPath): High-throughput, low-latency path that forwards application/user data directly from on-premises into Azure virtual machines and services without traversing the virtual network gateway.
* Control plane: Routing, management, and control messages still use the virtual network gateway for configuration and topology control.

Effectively, FastPath removes an extra hop in the data path that can otherwise create a bottleneck for high-volume workloads.

## Key benefits and considerations

| Benefit / Consideration  | Details                                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Throughput & latency     | Data-plane traffic can take a more direct route into Azure VMs/services, improving throughput and reducing latency.                 |
| Control plane separation | Control-plane (management) traffic continues to use the virtual network gateway, preserving routing and orchestration behavior.     |
| Gateway load             | FastPath reduces processing load on the gateway, improving scalability for data-heavy applications.                                 |
| SKU & regional support   | Not all gateway SKUs or regions support FastPath—verify supported SKUs, gateway versions, and region limitations in the Azure docs. |

> **lightbulb** FastPath requires a gateway SKU that supports the feature. Check the Azure documentation ([https://learn.microsoft.com/en-us/azure/expressroute/expressroute-fastpath-overview](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-fastpath-overview)) for the exact SKUs and any additional prerequisites (for example, certain gateway versions, configurations, or network topologies). Enabling FastPath can affect how traffic is routed, so validate requirements before making changes in production.

## Prerequisites checklist

* Confirm your virtual network gateway SKU supports FastPath (refer to the Azure FastPath overview).
* Ensure you have access to the ExpressRoute circuit and the Connection resource inside the circuit.
* Validate topology and routing: changes can affect how traffic flows to Azure VMs and appliances.
* Test in a non-production environment before enabling in production.

## Enable FastPath — Azure Portal

1. Open the ExpressRoute circuit in the Azure Portal.
2. Locate the ExpressRoute Connection resource (the connection inside the circuit that links to your gateway).
3. Open Connection > Configuration.
4. Toggle the FastPath (or "ExpressRoute gateway bypass") checkbox and save the changes.

<Frame>
  <img alt="The image shows instructions for updating a network connection to enable FastPath in a configuration interface, highlighting options to save or discard changes." />
</Frame>

## Enable FastPath — CLI and PowerShell

You can also enable FastPath programmatically.

Azure CLI (example pattern):

```bash theme={null}
