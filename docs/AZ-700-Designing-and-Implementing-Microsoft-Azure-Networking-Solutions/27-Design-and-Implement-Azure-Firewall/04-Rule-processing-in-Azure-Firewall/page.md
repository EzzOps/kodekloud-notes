# Rule processing in Azure Firewall

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-Firewall/Rule-processing-in-Azure-Firewall/page

Explains Azure Firewall rule types and their strict processing order DNAT network and application rules with examples and use cases

Azure Firewall enforces security using an ordered collection of rule types that operate across OSI layers. Understanding the evaluation sequence is critical: destination translation (DNAT), transport-level filtering, and application-level controls are applied in a fixed order so traffic is handled predictably.

This guide explains each rule type, shows examples, and summarizes the strict precedence Azure Firewall uses when processing traffic.

## NAT rules (DNAT / SNAT)

* Purpose: Configure destination network address translation (DNAT) to publish internal services by mapping a firewall public IP and port to a private IP and port in your virtual network.
* Common use case: Publish a web server to the internet by mapping the firewall public IP on port 80 to the VM's private IP and port 80.
* Outbound flows: Azure Firewall also performs source NAT (SNAT) for outbound traffic when the private source IPs need to be translated to the firewall's public IP for internet-bound flows.
* Processing: NAT rules are always evaluated first. If a packet matches a DNAT rule, the destination is translated and the packet is forwarded using the translated destination.

Example DNAT mapping (conceptual):

```text theme={null}
Firewall PublicIP:80  ->  10.0.1.4:80 (internal web server)
```

## Network rules (Layer 3–4)

* Purpose: Control access at transport and network layers by defining allowed or denied combinations of source IP ranges, destination IPs, protocol (TCP/UDP/ICMP), and ports.
* When to use: Traditional IP/port-based filtering—e.g., allow TCP/443 from a subnet to a specific backend IP or block specific IP ranges.
* Processing: Network rules are evaluated after NAT rules. They determine whether the transport-level flow (IP/protocol/port) is allowed or denied.

Example:

* Allow TCP 443 from `10.0.0.0/24` to `10.0.1.4:443`

<Frame>
  <img alt="The image describes rule processing in Azure Firewall, highlighting NAT rules, Network rules, and Application rules with brief descriptions for each." />
</Frame>

## Application rules (Layer 7)

* Purpose: Apply application-layer filtering for HTTP/HTTPS traffic using fully qualified domain names (FQDNs), hostnames, URLs, and web categories.
* When to use: Allow/deny access based on domains or categories (for example, allow `*.microsoft.com` but block social media domains).
* Processing: Application rules are evaluated after network rules and only apply to supported HTTP/HTTPS flows that reach the firewall.

Example:

* Allow `*.microsoft.com` and block `facebook.com`, or allow only specific URL paths for outbound web requests.

## Rule processing precedence (strict order)

Azure Firewall evaluates rules in this exact sequence:

1. NAT rules — always processed first. If a DNAT rule matches, the destination is translated and the flow is forwarded using the translated endpoint.
2. Network rules — evaluated next for transport-level (IP/protocol/port) access control.
3. Application rules — evaluated last for domain- or URL-level filtering on HTTP/HTTPS flows.

This ordering ensures:

* DNAT occurs before any transport- or application-level decisions.
* Network-level allow/deny decisions can short-circuit application evaluation.
* Application-level filtering is only considered when network rules do not already allow or deny the traffic.

| Rule Type         | OSI Layer            | Typical Use Case                                             | Evaluated |
| ----------------- | -------------------- | ------------------------------------------------------------ | --------- |
| NAT (DNAT/SNAT)   | Layer 3 (DNAT) / NAT | Publish internal services; translate source IPs for outbound | First     |
| Network Rules     | Layer 3–4            | IP/port filtering, protocol enforcement                      | Second    |
| Application Rules | Layer 7              | Domain/URL filtering, web categories                         | Last      |

> **lightbulb** Rule order matters: a DNAT match can change the destination before network or application rules are evaluated, and a network rule can allow or deny traffic before application rules are considered.

Next steps

* Try a hands-on deployment of Azure Firewall and create example DNAT, network, and application rules to observe how the precedence affects actual flows.
* Reference: [Azure Firewall documentation](https://learn.microsoft.com/azure/firewall/) for configuration examples, JSON schema, and policy-based rules.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c48f6bd6-195c-4405-9c9f-614ed7beb371/lesson/c3bd8ef8-7e23-4c47-a9ba-09a2da328080)
