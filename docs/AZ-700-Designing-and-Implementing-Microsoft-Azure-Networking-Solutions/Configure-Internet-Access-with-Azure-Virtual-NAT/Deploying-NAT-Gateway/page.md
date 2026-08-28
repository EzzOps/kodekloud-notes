# Deploying NAT Gateway

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Configure-Internet-Access-with-Azure-Virtual-NAT/Deploying-NAT-Gateway/page

Guide to deploying Azure NAT Gateway for predictable, secure outbound internet access from subnet resources without public IPs, including setup, configuration, and verification steps.

Deploying an Azure NAT Gateway to provide predictable, secure outbound internet access for resources that do not have their own public IP addresses.

In this guide you'll learn what a NAT gateway is, when to use it, how to create and attach one in the Azure portal, and how to verify outbound IP behavior from VMs.

Overview

* Create an Azure NAT Gateway in your chosen region — it becomes the outbound gateway for all resources in attached subnets. (NAT gateways are regional resources; assigned public IPs can be zonal or zone-redundant.)
* Assign either a static Public IP or a Public IP Prefix so outbound connections use a predictable public IP range.
* Attach the NAT gateway to one or more subnets in a virtual network. Resources in those subnets without public IPs will egress through the NAT gateway.
* Azure manages outbound routing automatically for subnets with a NAT gateway attached — you do not need user-defined routes (UDRs) unless you have explicit routing requirements.

<Frame>
  <img alt="The image is a guide for creating a NAT Gateway Resource in Azure, showing steps to set up project and instance details like subscription, region, and NAT gateway name. It also includes options for creating a NAT gateway and assigning a static IP address." />
</Frame>

Key configuration details

| Setting                       | What it controls                                                                                             | Recommendation                                                                                                                            |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Public IP vs Public IP Prefix | A single `Public IP` gives one outbound IP. A `Public IP Prefix` is a contiguous range (multiple addresses). | Use a `Public IP` for small-medium workloads. Use multiple `Public IP`s or a `Public IP Prefix` when you need many concurrent SNAT ports. |
| SNAT ports                    | Number of ephemeral ports available per public IP (affects concurrent outbound connections).                 | One public IP ≈ 64k SNAT ports. If you expect very high concurrent outbound connections, add more public IPs or use a prefix.             |
| TCP idle timeout              | How long Azure keeps idle TCP SNAT mappings. Range: `4`–`120` minutes (default `4`).                         | Increase for long-lived, idle connections (e.g., long polling). Default is fine for short-lived HTTP calls.                               |
| Scope                         | NAT gateway is regional and attached to subnets in the same VNet.                                            | Attach to subnets that should share the deterministic egress IP.                                                                          |

<Callout icon="lightbulb">
  NAT gateways are regional resources. Public IPs assigned to them can be zonal or zone-redundant — choose based on availability needs.
</Callout>

Subnet attachment rules

* A NAT gateway can be associated with multiple subnets within the same virtual network.
* A single subnet can have at most one NAT gateway attached (you cannot attach multiple NAT gateways to the same subnet).
* Virtual machines with their own assigned public IP will still egress using that VM public IP; NAT gateway affects only resources without their own public IPs.

<Frame>
  <img alt="The image shows a virtual network setup interface for configuring an Azure NAT gateway, highlighting steps like attaching the NAT gateway to a specific subnet and indicating no need for user-defined routes for outbound traffic." />
</Frame>

Practical demo: management and app VMs

Scenario

* Two VMs in the same VNet:
  * Management VM has a public IP (used as a jump host for SSH).
  * App VM does not have a public IP (initially uses dynamic Azure egress IP).
* Goal: Attach a NAT gateway to the app subnet so the app VM uses a deterministic outbound public IP.

Steps (using the management VM as a jump host)

1. SSH from your workstation to the management VM (replace the IP with your management VM public IP):

```bash theme={null}
ssh kodekloud@52.172.37.47
```

2. From the management VM, confirm its outbound public IP:

```bash theme={null}
curl https://ifconfig.me
