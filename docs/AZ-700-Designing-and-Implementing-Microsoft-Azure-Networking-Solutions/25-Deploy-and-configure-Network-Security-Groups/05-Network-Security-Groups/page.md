# Network Security Groups

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-and-configure-Network-Security-Groups/Network-Security-Groups/page

Explains Azure Network Security Groups, their rule properties, associations with subnets and NICs, priority evaluation, default and custom rules, and best practices for securing virtual network traffic.

Network Security Groups (NSGs) control network traffic to and from resources inside an Azure virtual network. An NSG contains an explicit list of security rules that either allow or deny inbound and outbound traffic.

It works by listing security rules that explicitly allow or deny inbound and outbound traffic.

<Frame>
  <img alt="The image shows a page for managing network security groups with options for overview, activity log, and access control, among others. It includes details about resource group, location, security rules, and associations, and emphasizes listing security rules for network traffic." />
</Frame>

You can associate an NSG with a subnet (to control traffic for multiple virtual machines) or with a virtual machine's network interface (NIC) to control traffic for a single VM. An NSG itself can be associated with multiple subnets and NICs across your subscription. Note that each subnet or NIC can have at most one NSG associated. When both a subnet and a NIC have NSGs, their rules are evaluated together and the rule with the lowest numeric priority that matches the traffic determines the outcome.

Security rules in an NSG define exactly which traffic is permitted or blocked. Azure includes several built-in default security rules that establish baseline behavior; these default rules cannot be deleted, but you can override them by adding custom rules with a higher priority (a lower numeric priority value).

Each rule is composed of properties such as priority, name, direction, protocol, source, destination, ports, and an action (Allow or Deny). Additional important rule fields include:

* Priority — an integer between 100 and 4096; lower numbers are higher priority and are evaluated before higher numbers.
* Direction — Inbound or Outbound.
* Protocol — TCP, UDP, or Any.
* Source / Destination — IP address prefixes, service tags (for Azure ranges like `Internet` or `VirtualNetwork`), or Application Security Groups (ASGs).
* Source / Destination port ranges.
* Access — Allow or Deny.
* Description — optional human-readable text.

<Frame>
  <img alt="The image shows a table of network security group (NSG) rules listing inbound and outbound security rules with properties such as priority, name, port, protocol, source, destination, and action. It provides details for rules like &#x22;RDP_Inbound&#x22; with various allow or deny actions." />
</Frame>

> **lightbulb** Priority values range from 100 to 4096; a rule with priority 100 is evaluated before one with priority 200. Because default rules exist with predefined priorities, choose custom priorities carefully so your rule takes effect as intended.

You can create custom rules to match your security requirements — for example, opening RDP on port 3389 but restricting the source to a specific IP range. Below is an example [Azure CLI](https://learn.microsoft.com/cli/azure/) command that creates a rule allowing RDP from a single IP address:

```bash theme={null}
az network nsg rule create \
  --resource-group MyResourceGroup \
  --nsg-name MyNSG \
  --name Allow-RDP \
  --priority 1000 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 203.0.113.4/32 \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 3389
```

Beyond defaults, use service tags and Application Security Groups to simplify management at scale and to avoid hard-coding many IP addresses. Test your rules carefully, and always follow the principle of least privilege — allow only what’s necessary.

Now that you understand how NSG rules work and how they are structured, this article continues with practical configuration examples and best practices for designing NSG rule sets.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f311416f-4844-43ee-bc18-4ad6b6f0b71a/lesson/33278938-ca60-4e5e-934e-11f47f5474c2)
