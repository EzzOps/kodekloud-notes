# Bring Your Own IP

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Configure-Public-IP-Addresses/Bring-Your-Own-IP/page

Describes Azure BYOIP enabling organizations to migrate and manage existing public IPv4/IPv6 address ranges through validation, provisioning and commissioning to preserve DNS, whitelists and reputation.

Bring Your Own IP (BYOIP) in Azure is an advanced networking capability that lets organizations migrate their existing public IPv4 or IPv6 address ranges into Azure. This is particularly useful for multi-cloud or hybrid environments, preserving DNS, firewall whitelists, and any reputation or compliance tied to your public addresses.

Why use BYOIP in Azure?

* You already control public IPv4/IPv6 address ranges used by websites, applications, corporate offices, or partner integrations.
* Those addresses may be whitelisted by partners, embedded in DNS, or associated with a reputation/trust profile.
* Migrating workloads without BYOIP would typically require updating DNS, asking partners to update firewall rules, and re-establishing IP reputation.

With BYOIP, you can bring your existing public IP ranges into Azure and use them for Azure resources. This keeps external configurations intact and maintains continuity for users and partners.

## How BYOIP works in Azure

Azure implements BYOIP with a secure three-stage process: validation, provisioning, and commissioning. Each stage is designed to protect ownership and prevent accidental prefix hijacking.

| Stage         | Purpose                                                                       | Typical actions / outcomes                                                                                                                                        |
| ------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validation    | Prove you own or are authorized to use the IP prefix                          | Provide origin validation (ROA / RPKI or other supported proofs) and cryptographic proof-of-possession so Azure can confirm your authority to announce the prefix |
| Provisioning  | Create a managed container in Azure for the brought-in prefix                 | Create a custom IP prefix resource in your subscription to allocate addresses internally. Prefix is provisioned but not advertised to the global Internet         |
| Commissioning | Put the prefix into global routing so external traffic reaches Azure services | Stop any prior advertisements, then commission the prefix in Azure so it’s advertised to the global Internet                                                      |

Think of the process like land and building permissions: validation proves you own the land, provisioning constructs the building and keeps the doors closed, and commissioning opens the doors to visitors.

<Frame>
  <img alt="The image outlines a three-step process for &#x22;Bring Your Own IP&#x22; involving validation, provisioning, and commissioning in managing custom IP prefix ranges. It includes a flowchart showing interactions between external controls, Azure API, and internal operations." />
</Frame>

### 1. Validation

* Azure must verify you legitimately own or are authorized to use the IP prefix being brought in.
* Common methods include Route Origin Authorization (ROA) / RPKI proofs or other Azure-supported validation methods to demonstrate authority to originate the prefix on the Internet.
* You will also provide cryptographic proof-of-possession (for example, a certificate or public key) that Azure can verify to ensure only legitimate owners can claim the addresses.

Analogy: this step is like proving ownership of a parcel of land before building on it. It prevents others from claiming or using IPs they don’t own.

### 2. Provisioning

* After successful validation, you create a custom IP prefix object in Azure (via the portal, PowerShell, or CLI). This represents your brought-in IP range inside Azure.
* The prefix is provisioned so you can allocate addresses to resources within your subscription, but Azure does not yet advertise the prefix to the Internet.
* You can assign IPs internally and perform testing without affecting external routing.

Analogy: provisioning is like building on the land but keeping the doors closed until you’re ready to welcome visitors.

### 3. Commissioning

* When ready to receive external traffic, you commission the prefix. Azure begins advertising the prefix to global BGP so traffic reaches your Azure-hosted services.
* Before commissioning, ensure any previous advertisements of those IPs from other providers or on-premises locations are stopped to avoid routing conflicts.

Analogy: commissioning is the moment you open the doors — users and partners can reach your services using the same IP addresses they always used.

## Key benefits

* Preserve existing public IP addresses so you don’t need to change DNS entries or ask partners to update firewall rules.
* Maintain reputation, trust, and compliance associated with your IP ranges.
* Simplify multi-cloud or hybrid migrations by keeping public addressing consistent across environments.

## Operational considerations and best practices

* Plan the cutover carefully: make sure the prefix is no longer advertised from other locations before commissioning in Azure to avoid route leaks or intermittent connectivity.
* Coordinate with upstream providers, registries, and partners, especially if you use ROAs/RPKI for origin validation.
* BYOIP is intended only for public address ranges that you legally control. Azure’s validation and proof-of-possession processes are designed to prevent IP hijacking and unauthorized claims.
* Keep an audit trail of validation artifacts and communications with registries to help troubleshoot validation or routing issues.

<Callout icon="lightbulb">
  Before commissioning a brought-in prefix, stop advertising it from any other network location. Failing to do so can cause routing conflicts or unpredictable traffic paths.
</Callout>

## Summary

Bring Your Own IP (BYOIP) in Azure lets organizations migrate public IP address ranges into Azure to preserve DNS, partner whitelists, reputation, and compliance. The three-stage workflow—validation, provisioning, and commissioning—ensures proof of ownership and safe transition into Azure’s global routing fabric.

## Links and references

* Azure documentation: [https://learn.microsoft.com/azure/virtual-network/](https://learn.microsoft.com/azure/virtual-network/) by searching for "Bring your own IP"
* RPKI / ROA overview: [https://www.ripe.net/analyse/internet-measurements/rpki](https://www.ripe.net/analyse/internet-measurements/rpki)
* General BGP concepts: [https://en.wikipedia.org/wiki/Border\_Gateway\_Protocol](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)

This concludes our discussion of Public IP addresses and Bring Your Own IP in Azure.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/d1f14b43-f5eb-48e5-a79d-22d1469571be/lesson/69281d62-9d99-4233-a61d-5301d5644c55" />
</CardGroup>
