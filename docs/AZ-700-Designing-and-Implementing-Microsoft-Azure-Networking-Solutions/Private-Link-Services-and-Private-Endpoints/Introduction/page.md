# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Private-Link-Services-and-Private-Endpoints/Introduction/page

Explains Azure Private Link, Private Endpoints and Private Link Services, their properties, end to end workflow, DNS and operational guidance for secure private connectivity

Private Link Services and Private Endpoints

In this lesson we'll explain how Azure Private Link provides private, secure connectivity to Azure platform services (such as Storage Accounts, SQL, and Web Apps) and to partner or customer-hosted services. You’ll learn what a Private Endpoint and a Private Link Service are, how connection requests are processed, and the operational details required for creating, approving, and troubleshooting Private Link connections.

What this article covers (in sequence)

* What a Private Endpoint is and why you use it
  * A Private Endpoint is a network interface (NIC) with a private IP address in your virtual network (`VNet`) that privately and securely connects to an Azure service over the Microsoft backbone network.
* What a Private Link Service is and how it’s used
  * A Private Link Service is a service fronted by a NIC in a `VNet` that exposes a service privately to other VNets or tenants via Private Endpoints.
* How Private Link works end-to-end, including approval workflows
* Key properties of a Private Endpoint: target resource and subresource (group IDs), DNS behavior, connection state, and IP/subnet details
* Operational notes for creating, approving, and troubleshooting Private Endpoint connections

<Callout icon="lightbulb">
  Private Endpoint traffic flows over the Azure backbone, providing private connectivity to platform or customer services without exposing traffic to the public internet.
</Callout>

## Why use Azure Private Link?

Azure Private Link ensures that traffic between your virtual network and the target service remains on the Microsoft network. This reduces exposure to the public internet, helps meet compliance requirements, and improves security posture for services such as:

* Azure Storage (Blobs, Files)
* Azure SQL
* Azure App Service
* Partner or customer-hosted services exposed via Private Link Service

## Private Endpoint vs Private Link Service — Quick comparison

| Concept              | Purpose                                                                                               | Common use                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Private Endpoint     | A `NIC` in your `VNet` with a private IP that maps to a target resource over Private Link             | Connect to Azure PaaS resources (e.g., storage, SQL) or to a Private Link Service exposed by another VNet/tenant |
| Private Link Service | A service fronted by a `NIC` in a `VNet` that exposes an application privately to other VNets/tenants | Publish your own service privately to consumers using Private Endpoints                                          |

## Key properties of a Private Endpoint

| Property               | What it represents                                                                                                                           |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Target resource        | The specific Azure resource (or Private Link Service) the endpoint connects to                                                               |
| Subresource / Group ID | The subresource or `groupId` on the target (for example, `blob` for Storage or `sqlServer` for SQL) that maps to the private connection      |
| DNS resolution         | The service hostname must resolve to the Private Endpoint's private IP — DNS configuration is required for name resolution inside the `VNet` |
| Connection state       | Status of the endpoint connection (e.g., `Pending`, `Approved`, `Rejected`) and whether manual approval is required                          |
| IP / Subnet            | The private IP assigned to the endpoint and the subnet it is deployed into (must allow traffic to the target)                                |

## How Private Link works (end-to-end)

1. Consumer creates a Private Endpoint in their `VNet`, specifying:
   * The target resource (or the target Private Link Service)
   * The subresource / `groupId` (if applicable)
   * A subnet and private IP for the endpoint
2. If the target requires approval, the owner receives a connection request and can approve or reject it (approval workflow)
3. Once approved, Azure provisions the network connectivity: the Private Endpoint’s `NIC` is associated with the target resource via the Microsoft backbone
4. DNS must be configured so that the service's FQDN resolves to the Private Endpoint's private IP from the consumer `VNet`
5. Client traffic flows over the Azure backbone to the service—no public internet traversal

## Typical Private Link workflow (concise steps)

* Create Private Endpoint in consumer `VNet`
* If needed, submit connection request to service owner
* Service owner approves (or rejects) request
* Configure DNS (Azure Private DNS or custom DNS) so the service hostname resolves to the private IP
* Test and validate connectivity

<Callout icon="warning">
  DNS configuration is critical: without proper DNS mapping the service hostname will resolve to a public endpoint and traffic can fail to use the Private Endpoint. Configure Azure Private DNS Zones or your custom DNS to point the service FQDN to the Private Endpoint private IP.
</Callout>

## DNS recommendations

* Use Azure Private DNS zones where possible (for example, `privatelink.blob.core.windows.net`), and link the Private DNS zone to your `VNet`.
* If you run a custom DNS solution, create records so the service FQDN resolves to the Private Endpoint private IP.
* Verify resolution from resources in the `VNet` with standard tools (e.g., `nslookup`, `dig`).

## Troubleshooting checklist

* Verify the Private Endpoint's `Connection State` (approved/connected).
* Confirm the endpoint’s private IP and subnet are correct and routeable.
* Ensure NSGs and UDRs do not block required traffic to the Private Endpoint.
* Check DNS resolution inside the `VNet` to confirm the service FQDN resolves to the private IP.
* Validate whether the target resource requires a specific `groupId` (subresource) and that the Private Endpoint is configured accordingly.

## Links and references

* [Azure Private Link documentation](https://learn.microsoft.com/azure/private-link/)
* [Azure Private Endpoint overview](https://learn.microsoft.com/azure/private-link/private-endpoint-overview)
* [Azure Private Link DNS configuration guidance](https://learn.microsoft.com/azure/private-link/private-endpoint-dns)

Use the guidance above to deploy and manage Private Link connections that keep traffic on the Azure backbone and maintain secure, private access to platform or customer-hosted services.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/dc19a21a-0949-471f-ba49-0bc6c09e7ff7/lesson/884038a3-5fee-42be-9895-5484af912e97" />
</CardGroup>
