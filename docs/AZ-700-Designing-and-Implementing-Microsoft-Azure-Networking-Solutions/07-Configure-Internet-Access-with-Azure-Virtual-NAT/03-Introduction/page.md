# Example output:
# 52.172.37.47
```

3. From the management VM, SSH to the app VM using its private IP (example: `10.80.2.4`):

```bash theme={null}
ssh kodekloud@10.80.2.4
# If prompted:
# The authenticity of host '10.80.2.4' can't be established.
# ED25519 key fingerprint is SHA256:...
# Are you sure you want to continue connecting (yes/no)? yes
# kodekloud@10.80.2.4's password:
```

4. On the app VM, check the outbound IP before NAT gateway attachment (this is dynamic and can change):

```bash theme={null}
curl https://ifconfig.me
# Example output:
# 172.191.1.94
```

Create and attach the NAT gateway in the Azure Portal

* In the Azure portal, create a new NAT gateway resource in the appropriate subscription, resource group, and region.
* Choose outbound IP addresses: select either a single Public IP or a Public IP Prefix. For this demo we create a single Public IP (named `NAT app PIP`).
* You can attach the NAT gateway to a subnet during creation or attach it afterwards. In this walkthrough we create the NAT gateway first and then attach it to the app subnet.

<Frame>
  <img alt="This image shows a Microsoft Azure portal interface for creating a Network Address Translation (NAT) gateway, with fields for project and instance details such as subscription, resource group, and region." />
</Frame>

* After the NAT gateway resource is deployed, open it in the portal, go to the Subnets blade, select the app subnet, and click Save to attach the NAT gateway to that subnet.
* After attachment, most outbound traffic from VMs in that subnet will egress using the NAT gateway’s public IP(s).
* Note: VMs that already have their own public IPs will continue to egress using their assigned public IPs instead of the NAT gateway.

<Frame>
  <img alt="The image shows a Microsoft Azure portal window for creating a network address translation (NAT) gateway. A pop-up for adding a public IP address is also visible with a prompt to enter a name and select options." />
</Frame>

Verify the outbound IP from the app VM

* Back on the app VM, re-run the outbound IP check after NAT gateway attachment:

```bash theme={null}
curl https://ifconfig.me
# Example output after NAT attachment:
# 172.191.1.202
```

* In the Azure portal, open the NAT gateway resource and view the associated public IP(s). Confirm the NAT gateway public IP matches the app VM's observed outbound IP.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying outbound IP settings for a NAT gateway, including a specific public IP address." />
</Frame>

Summary

* Deploying a NAT gateway and attaching it to your subnet provides predictable, centrally managed, and scalable outbound connectivity for resources without public IPs.
* It eliminates the need for custom outbound routes for normal egress scenarios and simplifies SNAT IP management.
* If your workload needs very high concurrent outbound connections, plan for multiple public IPs or a public IP prefix to avoid SNAT port exhaustion.

> **lightbulb** A single public IP provides approximately 64k SNAT ports. If your workload opens many concurrent outbound connections, use multiple public IPs or a public IP prefix on the NAT gateway to avoid SNAT port exhaustion.

Further reading and references

* Azure NAT gateway documentation: [https://learn.microsoft.com/azure/virtual-network/nat-gateway](https://learn.microsoft.com/azure/virtual-network/nat-gateway)
* Public IP and Public IP Prefix overview: [https://learn.microsoft.com/azure/virtual-network/public-ip-address](https://learn.microsoft.com/azure/virtual-network/public-ip-address)
* Azure networking concepts: [https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)

Related topics to explore: VPN gateway, User-Defined Routes (UDRs), Azure Firewall, and Azure Load Balancer outbound rules.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/5fa34fd1-903f-422e-8fc1-12a89731ebb9/lesson/fd94e4bf-0277-4272-931f-ab6a155c3dac)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Configure-Internet-Access-with-Azure-Virtual-NAT/Introduction/page

Guide to Azure NAT Gateway explaining outbound-only internet access, when to use it versus public IPs or load balancers, and how to configure and associate it with subnets.

Welcome to the module on configuring internet access with Azure Virtual NAT Gateway.

This lesson explains how Azure NAT Gateway provides secure, scalable outbound-only internet access for resources in your Azure Virtual Network (VNet). By centralizing egress through a NAT Gateway, you avoid assigning public IPs to individual virtual machines, reduce management overhead, and achieve predictable outbound (egress) behavior that improves your security posture and simplifies auditing.

By the end of this module you will be able to:

* Describe the purpose of Azure NAT Gateway and how it enables outbound-only internet connectivity for selected subnets.
* Explain when to prefer NAT Gateway over assigning public IP addresses directly to VMs or using load balancers for egress.
* Understand how NAT Gateway and Azure Load Balancer can work together to support both inbound and outbound connectivity for applications.
* Configure and associate a NAT Gateway with one or more subnets to provide scalable, efficient outbound traffic for your workloads.

<Frame>
  <img alt="The image outlines four learning objectives related to NAT Gateway, including its purpose, ideal scenarios, interaction with load balancers, and configuration for scalable traffic." />
</Frame>

> **lightbulb** Before you proceed, ensure you have a basic understanding of Azure Virtual Networks, subnets, Network Security Groups (NSGs), and public IP addressing. For a quick primer, see the [Azure networking fundamentals](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview) documentation.

Learning objectives (mapped to outcomes and why they matter):

| Learning objective                    |                                                               What you'll be able to do | Why it matters                                                                                                       |
| ------------------------------------- | --------------------------------------------------------------------------------------: | -------------------------------------------------------------------------------------------------------------------- |
| Describe NAT Gateway purpose          |    Explain how NAT Gateway provides outbound-only internet access for specified subnets | Centralizes egress, removes need for per-VM public IPs, and supports predictable source IPs for outbound connections |
| Choose the right egress pattern       |  Decide when to use NAT Gateway vs. VM public IPs or Load Balancer for outbound traffic | Helps meet security, cost, and scalability requirements for different application architectures                      |
| Combine NAT Gateway and Load Balancer | Architect solutions that handle both inbound (load-balanced) and outbound (NAT) traffic | Enables hybrid traffic patterns—public entry points plus secure, controlled egress                                   |
| Configure and associate NAT Gateway   |     Create and attach a NAT Gateway to subnets to enable scalable outbound connectivity | Provides a repeatable, supported deployment pattern for production workloads                                         |

References and further reading:

* [Azure NAT Gateway documentation](https://learn.microsoft.com/azure/virtual-network/nat-gateway)
* [Azure Load Balancer overview](https://learn.microsoft.com/azure/load-balancer/load-balancer-overview)
* [Azure Virtual Network overview](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/5fa34fd1-903f-422e-8fc1-12a89731ebb9/lesson/e24792c1-6629-4864-89f8-86a3d3b4c786)
