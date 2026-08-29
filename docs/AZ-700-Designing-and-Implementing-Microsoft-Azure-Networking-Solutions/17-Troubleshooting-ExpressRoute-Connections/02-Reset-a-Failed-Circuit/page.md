# Reset a Failed Circuit

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Troubleshooting-ExpressRoute-Connections/Reset-a-Failed-Circuit/page

How to reset and reapply configuration of a failed Azure ExpressRoute circuit using Az PowerShell to resolve provisioning state issues without recreating the resource

This guide shows how to reset a failed or unknown Azure ExpressRoute circuit by reapplying its configuration with Azure PowerShell. Reapplying the circuit configuration can often resolve transient provisioning or state inconsistencies without recreating the resource.

ExpressRoute reference: [https://learn.microsoft.com/azure/expressroute/expressroute-introduction](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)

> **lightbulb** Prerequisites: install and import the Az PowerShell module if you haven't already. Use `Install-Module -Name Az -Scope CurrentUser` to install and `Import-Module Az` to load it. For installation details, see [https://learn.microsoft.com/powershell/azure/install-az-ps](https://learn.microsoft.com/powershell/azure/install-az-ps).

## When to use this procedure

* The circuit shows `Failed`, `Unknown`, or an unexpected `ProvisioningState`.
* You suspect a transient provisioning issue between Azure and the service provider.
* You want to reapply the existing ExpressRoute configuration without deleting the circuit.

## High-level steps

1. Authenticate to Azure and set the target subscription.
2. Retrieve the ExpressRoute circuit into a variable and inspect its key properties.
3. Reapply the circuit configuration using `Set-AzExpressRouteCircuit`.
4. Verify the circuit’s provisioning and provider provisioning states.

## PowerShell example

Use the sequence below to sign in, capture the circuit, reapply its configuration, and confirm the result.

```powershell theme={null}
