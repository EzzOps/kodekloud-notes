# Deploying a Load Balancer in Azure

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-Load-Balancer/Deploying-a-Load-Balancer-in-Azure/page

Guide to deploying and configuring an Azure Load Balancer via the portal, covering frontend/backend, rules, health probes, NAT, outbound connectivity, and a Standard SKU portal walkthrough.

This guide walks through deploying and configuring an Azure Load Balancer using the Azure portal. It explains the required decisions and configuration steps—frontend, backend pools, load-balancing rules, health probes, NAT rules, and outbound connectivity—then demonstrates a portal-based example using a Standard Load Balancer across availability zones.

<Callout icon="lightbulb">
  Before you begin: ensure you have an Azure subscription, a resource group, and one or more Virtual Machines (VMs) deployed in the same virtual network (or in the zones/regions you plan to cover). If you need cross-region routing, consider Azure Front Door or Traffic Manager for global scenarios.
</Callout>

Overview: high-level deployment steps

* Choose subscription, resource group, name, region, SKU, type (public/internal), and tier (regional/global).
* Configure frontend IP configuration (public or private).
* Create backend pool(s) and add VM NICs or IP addresses.
* Create health probe(s).
* Create load balancing rule(s) that map frontend IP/port to backend pool/port.
* Optionally create inbound NAT rules for VM management and outbound rules (or use NAT gateway) for internet egress.

Start by selecting your Azure subscription and resource group, and provide a unique name for the load balancer instance.

<Frame>
  <img alt="The image is a screenshot of a form in the Azure Portal for creating a load balancer, showing fields for subscription, resource group, name, region, SKU, type, and tier. A highlighted note emphasizes providing a unique name for the load balancer instance." />
</Frame>

Choose region and SKU (Basic, Standard, or Gateway Load Balancer) based on scale, features, and support requirements. Then pick the type:

* Internet-facing (public) — public front end to serve internet traffic.
* Internal — private load balancing inside a virtual network.

Finally, choose a tier: regional (single region) or global (cross-region).

Backend pools
A backend pool contains the VM NICs or IP addresses that will receive load-balanced traffic. Configure it with:

* A descriptive name.
* The virtual network containing the backend resources.
* The configuration type:
  * NIC — add VM network interfaces (recommended for managed VMs).
  * IP address — for static or external endpoints.

<Frame>
  <img alt="The image illustrates the concept of creating backend pools, showing a cloud load balancer distributing traffic to a group of virtual machines (VMs) with various IP addresses. It explains that backend pools contain IPs of VMs to direct traffic from the load balancer." />
</Frame>

When defining a backend pool:

* Name the pool clearly for easier management.
* Associate the pool with the correct virtual network/subnet.
* Select the IP configurations or NICs to include.

<Frame>
  <img alt="The image provides instructions and options for configuring backend pools, including naming the pool, choosing a virtual network, and selecting a configuration type (NIC or IP address). A configuration panel shows fields for inputting these settings." />
</Frame>

SKU comparison — quick reference

| SKU                   | Use case                                                                    | Key notes                                                                                                                                   |
| --------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic                 | Small/test deployments within a single availability set or simple scenarios | Limited features and scale; may be deprecated in some regions—check current [Azure docs](https://learn.microsoft.com/azure/load-balancer/). |
| Standard              | Production deployments, zone-redundant, greater features and scale          | Recommended for production. Supports VMs, availability sets, and scale sets within a VNet.                                                  |
| Gateway Load Balancer | Transparent proxying for NVAs/firewalls                                     | Used to insert virtual appliances into traffic path.                                                                                        |

<Frame>
  <img alt="The image describes two types of SKUs for creating backend pools: Basic SKU, which supports VMs in a single availability set or VM scale set, and Standard SKU, supporting VMs in a virtual network with a mix of VMs, availability sets, and scale sets." />
</Frame>

Load balancing rules
A load balancing rule maps a frontend IP and port to a backend pool and backend port—this is the bridge between the frontend and backend instances.

<Frame>
  <img alt="The image shows a user interface for creating load balancer rules, with a section for adding specific rule details such as IP version, protocol, and ports. On the left, there are buttons for &#x22;Rule Mapping,&#x22; &#x22;NAT Rule Integration,&#x22; and &#x22;NAT Rule Behavior.&#x22;" />
</Frame>

Key fields for a load balancing rule:

* Rule name
* Frontend IP configuration
* Frontend port → Backend port
* Protocol (TCP/UDP)
* Backend pool association
* Health probe
* Session persistence (sticky sessions)
* Idle timeout
* Floating IP (Direct Server Return, if required)

Session persistence (affinity)
Session persistence controls whether requests from the same client are consistently routed to the same backend instance. By default, Azure Load Balancer distributes using a five-tuple hash: source IP, source port, destination IP, destination port, and protocol.

Options:

* None — five-tuple hash, no persistence.
* Client IP — two-tuple (client IP + destination IP).
* Client IP and protocol — three-tuple (client IP + destination IP + protocol).

Use persistence for stateful applications (shopping carts, session-specific services).

<Frame>
  <img alt="The image illustrates &#x22;Configuring Session Persistence&#x22; options, detailing how client connections pass through the internet to a load balancer, which directs traffic to different virtual machines." />
</Frame>

Health probes
Health probes determine whether backend instances are healthy and eligible for traffic. Probe types and configuration options:

| Probe type | What it checks             | Typical configuration                            |
| ---------- | -------------------------- | ------------------------------------------------ |
| TCP        | Port open/tcp handshake    | Port, interval, unhealthy threshold              |
| HTTP       | GET request expects 200 OK | Path (e.g. `/health`), port, interval, threshold |
| HTTPS      | Secure HTTP probe          | Path, port, TLS validation, interval, threshold  |

Probe parameters include protocol, port, path (for HTTP/HTTPS), probe interval (seconds), and unhealthy threshold (consecutive failures). Associate the probe with the load balancing rule so traffic is only forwarded to healthy instances.

<Frame>
  <img alt="The image is a slide titled &#x22;Creating Health Probes – Association,&#x22; showing a form for adding a health probe with fields like name, protocol, port, path, and interval. There's also a description explaining how probes are linked to load balancer rules to manage traffic based on backend status." />
</Frame>

Outbound connectivity (Standard Load Balancer)

* Standard SKU has no default outbound SNAT to the internet. You must create an outbound rule or attach a NAT gateway for backend VMs to reach the internet.
* When an outbound rule is present, backend VM IPs are SNATed to the load balancer public IP.
* A single outbound rule can apply to multiple backend pools.

A common limitation is SNAT port exhaustion: each public IP has a finite number of ephemeral ports. For workloads requiring a very large number of concurrent outbound connections, prefer a NAT gateway (assigned to the subnet) because it offers higher, scalable SNAT port capacity.

<Callout icon="lightbulb">
  If you expect a large number of concurrent outbound connections, use a NAT gateway (associated to the VM subnet). NAT gateway provides scalable SNAT port allocation and avoids port exhaustion.
</Callout>

<Frame>
  <img alt="The image explains how to configure outbound traffic using a standard load balancer, detailing the default behavior, outbound rule requirements, frontend association, SNAT translation, and outbound port allocation, accompanied by a diagram of pools with VMs and timeout settings for outbound rules." />
</Frame>

Portal walkthrough: create a Standard Load Balancer (example)
In this example we deploy a Standard Load Balancer in East US 2 across three availability zones for zone redundancy. Begin by verifying the VMs you will add to the backend pool.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying a list of virtual machines. Each entry includes information such as name, subscription, resource group, location, status, operating system, size, and disk count." />
</Frame>

Create the load balancer:

* SKU: Standard (general purpose; use Gateway LB only for NVAs/firewalls).
* Subscription and resource group: choose appropriate ones.
* Name: e.g., `AZ-700-Web-LB`.
* Region: East US 2.

<Frame>
  <img alt="The image shows a Microsoft Azure interface for creating a load balancer, including fields for project and instance details such as subscription, resource group, name, region, SKU, type, and tier." />
</Frame>

Note: Basic SKU may not be available in some subscriptions or regions; consult the current Azure documentation for SKU availability.

Frontend configuration (example)

* Type: Public (internet-facing) for this demo.
* Frontend name: `AZ-700-LB-FE`
* IP version: IPv4
* Public IP: create `AZ-700-LB-PIP` (optionally zone-redundant)

<Frame>
  <img alt="The image shows a Microsoft Azure page where a frontend IP configuration for a load balancer is being set. There are options to select the IP version, type, and a section to add a public IP address." />
</Frame>

Backend pool (example)

* Add a backend pool and select the virtual network where your VMs reside.
* Select VM NICs (IP configurations) that should receive traffic and save.

<Frame>
  <img alt="The image shows a Microsoft Azure interface for adding IP configurations to a backend pool, with a table listing virtual machines and their details such as resource group and IP address." />
</Frame>

You can skip inbound NAT and outbound rules during initial deployment and add them later. Review + create to deploy the load balancer.

After deployment, inspect the load balancer blade to verify frontend IP configuration, backend pools, health probes, load balancing rules, and NAT rules.

<Frame>
  <img alt="The image shows a user interface of a load balancer setup on a cloud platform, with options for configuration and management, including resource group, location, and subscription details." />
</Frame>

Create a load balancing rule (example)
To load balance web traffic on port 80:

* Name: `AZ-700-web-rule`
* IP version: IPv4
* Frontend IP: `AZ-700-LB-FE`
* Backend pool: `AZ700LBBE`
* Protocol: TCP
* Frontend port: 80 → Backend port: 80
* Health probe: create an HTTP probe (path `/`, interval 5s)
* Session persistence: None (adjust if needed)
* Idle timeout & floating IP: defaults unless required otherwise

<Frame>
  <img alt="The image shows a Microsoft Azure interface for adding a load balancing rule, with options for IP version, frontend IP address, backend pool, protocol, port, health probe, session persistence, and idle timeout settings." />
</Frame>

Save the rule. You should now be able to browse to the load balancer front-end public IP and receive responses from one of the backend VMs (responses may alternate based on hashing and session persistence settings).

Find the public frontend IP via the Load Balancers list, copy it, and open it in a browser.

<Frame>
  <img alt="The image shows a Microsoft Azure portal page displaying a list of load balancers under &#x22;Load balancing and content delivery,&#x22; with details such as name, SKU, resource group, location, and subscription." />
</Frame>

The frontend IP shown is the public address clients use to reach your service.

<Frame>
  <img alt="The image shows a configuration screen for a load balancer, displaying the frontend IP address 20.12.96.233 associated with the name az700-lb-fe." />
</Frame>

If you refresh the browser you may see responses from different backend VMs (for example AZ3, AZ2) depending on the hashing algorithm and client source/port behavior.

Inbound NAT rules
Use inbound NAT rules when you need direct access to a specific VM on a specific port through the load balancer public IP. Azure recommends the newer V2 NAT format to avoid future migrations.

<Frame>
  <img alt="The image shows the Microsoft Azure portal with a &#x22;Load balancing rules&#x22; page open for a load balancer named &#x22;az700-web-lb,&#x22; displaying a rule with TCP/80 protocol linked to a backend pool and health probe." />
</Frame>

Example NAT rule to reach a VM's SSH port:

* Name: `AZ-700-LB-NAT-VM1`
* Target VM: select VM in zone 1
* Frontend IP: `AZ-700-LB-FE`
* Frontend port: `9090` (public)
* Backend port: `22` (SSH on VM)
* Protocol: TCP

<Frame>
  <img alt="This image shows a Microsoft Azure interface for adding an inbound NAT rule, including options to specify the rule's name, type, target virtual machine, and protocol. There is a warning about the retirement of Inbound NAT rule version 1 by September 30, 2027." />
</Frame>

<Frame>
  <img alt="The image shows the &#x22;Add inbound NAT rule&#x22; setup page in Microsoft Azure, where various configuration options for adding a NAT rule are being displayed, including fields for name, type, target virtual machine, and protocol." />
</Frame>

With that NAT rule in place, connecting to the load balancer public IP on port `9090` will forward to port `22` of the selected VM. From a terminal, SSH to the VM via the load balancer public IP and NAT port:

```bash theme={null}
ssh kodekloud@20.12.96.233 -p 9090
```

You will likely see a host authenticity prompt similar to:

```bash theme={null}
The authenticity of host '20.12.96.233:9090' can't be established.
ED25519 key fingerprint is SHA256:[SECRET_REDACTED].
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Answer `yes` and provide your credentials to verify inbound NAT mapping to port 22.

Testing outbound connectivity from a backend VM
If a VM in the backend pool cannot reach the internet (typical with Standard SKU and no outbound rule/NAT gateway), test with:

```bash theme={null}
curl https://www.microsoft.com
```

If the request times out, create an outbound rule and associate it with the frontend IP and the backend pool, or attach a NAT gateway to the subnet for scalable outbound SNAT.

After adding an outbound rule or NAT gateway, internet-bound requests (e.g., `apt update` or `curl`) should succeed.

Summary

* Load balancing rules map frontend IP/port to backend pool and port to distribute inbound traffic.
* Health probes ensure only healthy backend instances receive traffic.
* Inbound NAT rules map unique frontend ports to backend VM ports (useful for SSH/RDP or management).
* Standard Load Balancer requires an outbound rule (or NAT gateway) for backend VMs to access the internet; NAT gateway is recommended for high-scale outbound needs to avoid SNAT port exhaustion.

Further reading and references

* [Azure Load Balancer documentation](https://learn.microsoft.com/azure/load-balancer/)
* [NAT gateway overview](https://learn.microsoft.com/azure/virtual-network/nat-gateway)
* [Designing for high availability and redundancy in Azure](https://learn.microsoft.com/azure/architecture/resiliency/)

This completes the Azure Load Balancer deployment and configuration walkthrough.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6d9c06ee-9a3e-4b7a-be2f-6bb8314af6a2/lesson/1efb3f9d-40e0-4e86-a2fb-d7a2b9350c61" />
</CardGroup>
