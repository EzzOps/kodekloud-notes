# Troubleshoot VPN Gateway

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-VPN-Gateway/Troubleshoot-VPN-Gateway/page

A checklist to diagnose and resolve common Azure VPN Gateway connectivity, performance, and configuration issues using diagnostics, packet captures, and validation steps.

This guide provides a concise, methodical checklist to diagnose and resolve common Azure VPN Gateway issues — from connectivity failures to performance bottlenecks. Follow the steps in order and collect evidence (logs, packet captures, and metrics) so you can identify the root cause quickly.

## Quick summary

* Start with throughput and connectivity measurements.
* Collect diagnostics (Network Watcher, packet capture, gateway logs).
* Validate configuration: GatewaySubnet, UDRs, NSGs, PSKs, peer IPs, and IKE/IPsec parameters.
* Check gateway health, metrics, and SKU limits.

## Validation checklist (step-by-step)

1. Validate VPN throughput
   * Compare observed throughput against the published limits for your VPN Gateway SKU. If the measured bandwidth is substantially lower than the SKU limit, the gateway SKU may be the bottleneck.
   * Measure throughput using a performance tool such as iperf3 across the tunnel (from an on-prem host to an Azure VM) or use Azure Network Watcher diagnostics.
   * Example iperf3 commands:
   ```bash theme={null}
   # On the Azure VM (server)
   iperf3 -s -p 5201

   # On the on-premises host (client)
   iperf3 -c <azure-vm-ip> -p 5201 -P 4
   ```
   * When comparing results, allow for encryption overhead (IPsec) and any intermediate NAT or link constraints.

2. Use Azure Network Watcher for diagnostics
   * Network Watcher can test connectivity, run path and connection troubleshooting, and capture packets for deeper analysis.
   * Useful commands:
   ```bash theme={null}
   # Test connectivity between a source VM and a destination IP/port
   az network watcher test-connectivity --source-resource <source-resource-id> --dest-address <dest-ip> --dest-port <port> -g <resource-group> -l <location>

   # Start packet capture on a NIC
   az network watcher packet-capture create --resource-group <rg> --vm <vm-name> --name <capture-name> --filters '[{"protocol":"Any"}]'
   ```
   * Use packet captures to identify where traffic is dropped or malformed (local VM NIC, gateway, or transit).

3. Enable and analyze VPN gateway diagnostic logs
   * Turn on VPN Gateway diagnostics and route logs to a Log Analytics workspace, Storage account, or Event Hub to retain connection negotiation, tunnel activity, and error messages.
   * Example (enable diagnostics via Azure CLI):
   ```bash theme={null}
   az monitor diagnostic-settings create \
     --resource <vpn-gateway-resource-id> \
     --name "vpn-diagnostics" \
     --workspace <log-analytics-workspace-id> \
     --logs '[{"category":"GatewayDiagnosticLog","enabled":true},{"category":"TunnelDiagnosticLog","enabled":true}]'
   ```
   * Search logs for repeated retries, PSK mismatches, IKE negotiation failures, or specific error codes that indicate parameter mismatches.

4. Check GatewaySubnet, UDRs, and NSGs
   * Ensure the VNet contains a correctly named and sized `GatewaySubnet`. The recommended size is at least `/27` for most gateway deployments; follow current Azure guidance for your gateway type.
   * Avoid attaching restrictive NSGs or non-default UDRs to the `GatewaySubnet` unless you understand the exact impact. Custom routes or overly restrictive security rules can block IKE/IPsec traffic.
   * Required traffic typically includes:
     * UDP 500 (IKE)
     * UDP 4500 (NAT-T for IPsec)
     * ESP (IP protocol 50) where applicable
   * Verify that none of these are being blocked by on-prem or Azure-side firewalls or routes.

> **lightbulb** Do not apply restrictive NSGs or non-default UDRs to the GatewaySubnet unless absolutely required—this is a common source of VPN failures.

5. Verify on-premises VPN device compatibility
   * Confirm your on-premises device and firmware are on Microsoft’s list of validated VPN devices, or that the device supports the IKE/IPsec parameters you plan to use.
   * Use vendor sample configurations as a baseline and apply Azure-specific samples where available.

6. Check gateway health and metrics
   * In the Azure portal, review the VPN gateway resource for health status, active tunnels, public IP bindings, and per-tunnel throughput. Azure shows gateway health and any internal probe failures.
   * Use metrics to identify trends (CPU, throughput, packet drops) and time windows for failures.
   * Example CLI to get gateway details:
   ```bash theme={null}
   az network vpn-gateway show --name <gateway-name> -g <resource-group>
   ```

7. Verify shared keys and peer IP configuration
   * A mismatch in the pre-shared key (PSK) or an incorrect peer IP address will prevent the tunnel from establishing.
   * Confirm the Connection resource in Azure and the on-prem device use the identical PSK and peer IP.
   * If dynamic IPs are used on-prem, verify the Azure side expects that configuration (e.g., use Azure VPN Client for point-to-site scenarios, or use a dynamic VPN device configuration that supports changing peer IPs).

8. Match IKE / IPsec parameters, including PFS
   * IKE version (IKEv1 vs IKEv2), encryption algorithms, hashing algorithms, DH groups, lifetimes, and Perfect Forward Secrecy (PFS) settings must be compatible on both sides.
   * If one side enforces PFS or requires a specific DH group and the other side does not, the tunnel negotiation will fail. Confirm both sides use the same proposals and lifetimes or use compatible profiles.

By following these systematic checks you will be able to pinpoint and resolve most Azure VPN Gateway issues.

<Frame>
  <img alt="The image is a list of steps for VPN validation and troubleshooting, including actions such as validating VPN throughput, utilizing Network Watcher, and verifying shared keys." />
</Frame>

Since the VPN gateway in this scenario is not yet deployed, plan to enable diagnostics immediately after deployment. Specifically:

* Enable gateway diagnostics and send logs to a Log Analytics workspace.
* Check gateway health and metrics once the gateway is up and tunnels are negotiated.
* Confirm where to configure the PSK (the Azure Connection resource) and validate negotiated parameters during tunnel establishment (logs and packet captures will show IKE negotiation and proposal details).

When deploying a VPN gateway you may also see an option for active-active mode. Active-active provides high availability through multiple active tunnels and can improve resiliency for multi-site topologies. Evaluate active-active if you require:

* Multi-tunnel redundancy
* Higher aggregate throughput (consult SKU limits and supported configurations)
* Resilience to single-instance failure

Common symptoms and targeted checks

| Symptom                   | Primary checks                                                 | Suggested action                                                            |
| ------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Tunnel never establishes  | PSK mismatch, wrong peer IP, incompatible IKE/IPsec parameters | Verify PSK and peer IP, compare IKE/IPsec proposals and lifetimes           |
| Low throughput            | Gateway SKU limits, encryption overhead, MTU issues            | Measure with iperf3, check SKU throughput, review MTU and fragmentation     |
| Intermittent drops        | UDRs/NSGs blocking traffic, transient on-prem link issues      | Inspect GatewaySubnet routes/NSGs, capture packets to see where drops occur |
| Negotiates but no traffic | Traffic blocked (ESP/UDP ports), incorrect routes              | Ensure UDP 500/4500 and ESP allowed, validate route tables on both sides    |

## Links and references

* [Azure VPN Gateway documentation](https://learn.microsoft.com/azure/vpn-gateway/)
* [Network Watcher documentation](https://learn.microsoft.com/azure/network-watcher/)
* [Azure Monitor / Diagnostic settings](https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostic-settings)
* [Validated VPN devices and sample configurations](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpn-devices)

This concludes the lesson — follow the checklist, collect diagnostic artifacts (logs, packet captures, metrics), and escalate to Microsoft support with artifacts if you cannot resolve the issue locally.

<Frame>
  <img alt="The image lists eight steps related to VPN and Azure network troubleshooting and validation, including using Network Watcher and verifying shared keys and VPN peer IPs." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f28862d8-b736-4ae4-9003-0efa45de8cd9/lesson/6db21c13-fd30-4540-8c24-a3d1e5128647)
