# 1. Sign in and select subscription
Connect-AzAccount
Get-AzSubscription
Select-AzSubscription -SubscriptionName "LAB-01"

# 2. Retrieve the circuit into a variable and inspect key properties
$erCircuit = Get-AzExpressRouteCircuit `
    -Name "Lab-ER-Circuit" `
    -ResourceGroupName "Lab-RG"

# Display important properties to verify current state
$erCircuit | Select-Object Name, ResourceGroupName, ProvisioningState, ServiceProviderProvisioningState, Sku

# 3. Reapply the configuration (this triggers a reset/reapply)
Set-AzExpressRouteCircuit -ExpressRouteCircuit $erCircuit

# 4. Verify the circuit state after the operation
Get-AzExpressRouteCircuit -Name "Lab-ER-Circuit" -ResourceGroupName "Lab-RG" |
    Select-Object Name, ProvisioningState, ServiceProviderProvisioningState, Sku
```

## What to inspect after running the command

Check these properties to determine whether the issue was resolved or if the provider side still reports a problem:

| Property                           | Meaning                                | Example values                                  |
| ---------------------------------- | -------------------------------------- | ----------------------------------------------- |
| `ProvisioningState`                | Azure-side provisioning status         | `Succeeded`, `Updating`, `Failed`               |
| `ServiceProviderProvisioningState` | Service provider's provisioning status | `Provisioned`, `Provisioning`, `NotProvisioned` |
| `Sku`                              | Circuit SKU and bandwidth              | e.g. `Standard_Metered`                         |

Always compare both `ProvisioningState` and `ServiceProviderProvisioningState`—a successful Azure-side state with a provider-side `NotProvisioned` or `Failed` usually indicates the issue is with the connectivity provider.

<Callout icon="warning">
  Resetting/reapplying an ExpressRoute configuration may cause a brief disruption in traffic. Ensure you have appropriate permissions (for example, Network Contributor or Owner) and perform this during an approved maintenance window when required. For built-in role details, see [https://learn.microsoft.com/azure/role-based-access-control/built-in-roles](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles).
</Callout>

## Troubleshooting tips

* Permission errors: Confirm your role assignments and that your account has access to the target subscription and resource group.
* Persistent failed state: Inspect related resources such as peerings, authorizations, and provider-side status. Collect the circuit's service key and provisioning details.
* If provider-side issues persist, open a support request with Microsoft Azure and include the circuit service key and recent provisioning logs: [https://learn.microsoft.com/azure/azure-supportability/create-technical-support-request](https://learn.microsoft.com/azure/azure-supportability/create-technical-support-request)

## Quick reference links

* ExpressRoute overview: [https://learn.microsoft.com/azure/expressroute/expressroute-introduction](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
* Az PowerShell install: [https://learn.microsoft.com/powershell/azure/install-az-ps](https://learn.microsoft.com/powershell/azure/install-az-ps)
* Set-AzExpressRouteCircuit (cmdlet reference): [https://learn.microsoft.com/powershell/module/az.network/set-azexpressroutecircuit](https://learn.microsoft.com/powershell/module/az.network/set-azexpressroutecircuit)
* Azure support: [https://learn.microsoft.com/azure/azure-supportability/create-technical-support-request](https://learn.microsoft.com/azure/azure-supportability/create-technical-support-request)

Notes:

* If the `Set-AzExpressRouteCircuit` command does not progress, capture the cmdlet output and any error details for support.
* Reapplying the configuration preserves the existing resource configuration while re-triggering Azure-side provisioning logic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6190597d-0e7a-4ffd-ac5d-afe70f482a27/lesson/07537780-a32b-40bd-ae70-b7f97ed2837e" />
</CardGroup>


# Troubleshooting Network Performance

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Troubleshooting-ExpressRoute-Connections/Troubleshooting-Network-Performance/page

Guidance for diagnosing and fixing Azure network performance issues using tools like AzCTK, tests for bandwidth latency packet loss and steps to isolate root causes

This guide explains how to diagnose and remediate network performance issues in Azure. It covers recommended tools, how to run end-to-end tests with the Azure Connectivity Toolkit (AzCTK), how to interpret results, and practical checks to narrow down root causes.

## Recommended tools

Use these Azure-native and community tools for monitoring and diagnosing connectivity, throughput, and latency issues:

* Azure Network Watcher — packet capture, topology, connection troubleshoot: [https://learn.microsoft.com/azure/network-watcher/network-watcher-monitoring-overview](https://learn.microsoft.com/azure/network-watcher/network-watcher-monitoring-overview)
* Azure CLI — scripting and automation for Azure resources: [https://learn.microsoft.com/cli/azure/](https://learn.microsoft.com/cli/azure/)
* Azure PowerShell — manage Azure resources from PowerShell: [https://learn.microsoft.com/azure/powershell/](https://learn.microsoft.com/azure/powershell/)
* Azure Connectivity Toolkit (AzCTK) — a PowerShell toolkit for end-to-end network diagnostics: [https://github.com/microsoft/Azure-Connectivity-Toolkit](https://github.com/microsoft/Azure-Connectivity-Toolkit)

AzCTK is particularly useful for automated, repeatable tests of TCP connectivity, packet loss, latency, and multi-session bandwidth.

## AzCTK overview and common cmdlets

AzCTK provides cmdlets that replicate real-world TCP behavior across different session counts and window sizes. Useful cmdlets include:

| Cmdlet                     | Purpose                                                      |
| -------------------------- | ------------------------------------------------------------ |
| `Get-LinkPerformance`      | Multi-stage TCP performance tests (bandwidth, loss, latency) |
| `Get-LinkDiagnostics`      | Path diagnostics and connectivity checks                     |
| `Test-Link` (if available) | Quick reachability and basic throughput checks               |

Key AzCTK features:

* End-to-end packet loss and latency tests.
* Single-thread and multi-thread bandwidth tests (multiple concurrent sessions).
* Ability to vary TCP window sizes to emulate different client behaviors.
* Installable as a PowerShell module for automation and scripting.

<Frame>
  <img alt="The image describes AzCTK features, including end-to-end packet loss and latency tests, simulating single/multi-thread bandwidth tests, and an installable PowerShell module for ease of use." />
</Frame>

The screenshot above shows a sample multi-stage test output with bandwidth, packet loss, and latency reported for different session counts and stages. Reviewing these metrics across stages helps identify capacity constraints, device misconfigurations, or endpoint limitations.

## Example: running a Get-LinkPerformance test

Run a basic multi-stage performance test:

```powershell theme={null}
Get-LinkPerformance -RemoteHost 127.0.0.1 -TestSeconds 10
```

This triggers a series of TCP tests (no-load ping, single-session, multi-session, varying window sizes) over the specified duration. Example (trimmed) output:

```powershell theme={null}
E:\> Get-LinkPerformance -RemoteHost 127.0.0.1 -TestSeconds 10
6/30/2017  4:50:18 PM - Stage 1 of 6: No Load Ping Test...
6/30/2017  4:50:56 PM - Stage 2 of 6: Single Thread Test...
6/30/2017  4:51:22 PM - Stage 3 of 6: 6 Thread Test...
6/30/2017  4:51:49 PM - Stage 4 of 6: 16 Thread Test...
6/30/2017  4:52:15 PM - Stage 5 of 6: 16 Thread Test with 1Mb window...
6/30/2017  4:52:22 PM - Stage 6 of 6: 32 Thread Test...
Testing Complete!

Name                          Bandwidth           Loss       P50
----                          ---------           ----       ---
No Load                       N/A                 0%         1.87ms
1 Session                     6.79 Gbits/sec      0%         0.92ms
6 Sessions                    8.39 Gbits/sec      0%         1.94ms
16 Sessions                   7.50 Gbits/sec      0%         4.34ms
16 Sessions with 1Mb window   7.33 Gbits/sec      0%         19.405ms
32 Sessions                   7.17 Gbits/sec      0%         8.335ms
```

### Interpreting the core metrics

| Metric               | Meaning                                     | Action if high/abnormal                                                    |
| -------------------- | ------------------------------------------- | -------------------------------------------------------------------------- |
| Bandwidth            | Observed throughput in the test scenario    | Compare against link/VM limits; check NIC/VM SKU and NIC teaming           |
| Loss                 | Percentage of packets lost during the test  | Investigate QoS, MTU mismatches, network saturation, or device-level drops |
| P50 (median latency) | Median round-trip latency (50th percentile) | Check routing, device CPU saturation, or asymmetric paths                  |

## Troubleshooting checklist

When results show elevated loss, reduced bandwidth, or increased latency, validate configuration and capacity across all layers:

* Azure networking:
  * NSGs and UDRs for unintended rules.
  * Load Balancer configuration and health probes.
  * VM size and NIC capabilities (maximum bandwidth, Accelerated Networking).
* On-premises network:
  * Routers, switches, firewalls for queueing or drops.
  * MTU settings and VLAN configurations.
* Connectivity circuits:
  * ExpressRoute or VPN circuit health and advertised BGP routes.
* Endpoints:
  * Server NIC drivers, OS TCP stack tuning, CPU/memory saturation.

Run tests from both endpoints (on-premises → Azure and Azure → on-premises). Vary session counts and TCP window sizes to isolate whether the bottleneck is in the network or on the endpoints.

## Installation and quick start

Install AzCTK from the PowerShell Gallery and import it into your session:

```powershell theme={null}
