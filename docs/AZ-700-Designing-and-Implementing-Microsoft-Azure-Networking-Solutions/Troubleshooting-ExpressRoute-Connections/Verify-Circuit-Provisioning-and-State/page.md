# Show the circuit and inspect the peerings section
az network express-route show \
  --name MyCircuit \
  --resource-group MyResourceGroup \
  -o json | jq '.peerings'
```

Check each peering object for:

* `provisioningState` or `status` = `Provisioned`

* `ipv4Routes?` and IP address fields (primary/secondary) for Private peering

* `peeringType`, `vlanId`, `peerASN`

* PowerShell

```powershell theme={null}
# Retrieve the ExpressRoute circuit and expand the Peerings property
(Get-AzExpressRouteCircuit -Name 'MyCircuit' -ResourceGroupName 'MyResourceGroup') |
  Select-Object -ExpandProperty Peerings
```

Inspect the returned objects for `ProvisioningState`, `PeeringType`, `PeerASN`, `VlanId`, and IP configuration properties.

## Quick reference table

| Check               | Portal location               | CLI / PowerShell                              | Expected                                          |                                                  |
| ------------------- | ----------------------------- | --------------------------------------------- | ------------------------------------------------- | ------------------------------------------------ |
| Peerings exist      | Circuit → Peerings            | \`az network express-route show ...           | jq '.peerings'\`                                  | `Private`, `Microsoft`, `Public` (as applicable) |
| Provisioning state  | Peerings list                 | `jq '.provisioningState'`                     | `Provisioned`                                     |                                                  |
| Private peering IPs | Peering details               | Inspect `properties.ipConfigurations` in JSON | `Primary` and `Secondary` IPs present and correct |                                                  |
| VLAN and ASN        | Peering details               | `vlanId`, `peerASN` fields                    | Match service provider values                     |                                                  |
| BGP status          | Peering details / Router logs | Router and provider logs                      | BGP session established                           |                                                  |

Note: In the table above, any JSON or object-like values are shown as code to avoid parsing issues (for example, `properties.ipConfigurations`).

## Troubleshooting tips

* If a peering is missing:
  * Confirm the peering was created on the correct ExpressRoute circuit and in the correct resource group.
  * Verify you selected the correct peering type (Private, Microsoft, Public) when creating the peering.

* If a peering's provisioning state is not `Provisioned` or is stuck:
  * Verify VLAN ID and peer ASN are configured correctly both in Azure and by your connectivity provider.
  * Confirm primary/secondary IP address pairs match the provider's assigned addresses.
  * Ensure required route filters, service keys, or other provider-specific settings have been applied.

* If BGP does not establish:
  * Validate BGP authentication (if used), peer ASNs, and BGP passwords on both sides.
  * Review edge-router logs and any notifications from your connectivity provider for session negotiation errors.
  * Confirm prefix advertisements and route filters are correctly applied.

* If you see inconsistent or unexpected IP settings in the portal vs. provider documentation:
  * Do not change values unilaterally—coordinate changes with the connectivity provider to avoid mismatched configurations.

<Callout icon="warning">
  Do not change VLAN IDs, peer ASNs, or IP assignments without confirming with your connectivity provider—these values must match exactly on both sides to establish BGP and avoid outages.
</Callout>

## Example inspection of Azure CLI JSON output

When you run the Azure CLI command above, a peering object in the JSON might include fields such as:

* `peeringType`
* `peerASN`
* `vlanId`
* `ipConfigurations` (contains `primaryIPv4` and `secondaryIPv4` for Private peering)
* `provisioningState`

Use `jq` or equivalent JSON parsing tools to extract and compare these values programmatically as part of validation scripts.

## Links and references

* [Azure ExpressRoute overview](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
* [Azure CLI documentation](https://learn.microsoft.com/cli/azure/)
* [Get-AzExpressRouteCircuit](https://learn.microsoft.com/powershell/module/az.network/get-azexpressroutecircuit)

By following these checks and using the portal and CLI examples above, you can quickly validate ExpressRoute peering configuration and identify common provisioning issues.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6190597d-0e7a-4ffd-ac5d-afe70f482a27/lesson/8ac98c84-a85f-4045-bf3f-596ec84035db" />
</CardGroup>


# Verify Circuit Provisioning and State

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Troubleshooting-ExpressRoute-Connections/Verify-Circuit-Provisioning-and-State/page

Guide to verify Azure ExpressRoute circuit provisioning and operational state using Azure PowerShell and the Azure portal, with checks and troubleshooting steps.

Verifying circuit provisioning and operational state is an essential first step when troubleshooting [ExpressRoute](https://learn.microsoft.com/azure/expressroute/). This guide shows how to check the provisioning status with [Azure PowerShell](https://learn.microsoft.com/azure/developer/powershell/) and how to confirm the same information in the [Azure portal](https://portal.azure.com).

Prerequisites:

* You must have the Az PowerShell module installed and be authenticated (`Connect-AzAccount`).
* Confirm you have permission to read the ExpressRoute circuit resource in the target subscription and resource group.

Use the `Get-AzExpressRouteCircuit` command and specify the resource group and circuit name:

```powershell theme={null}
Get-AzExpressRouteCircuit `
    -ResourceGroupName "Lab-Network-RG" `
    -Name "Lab-ER-Circuit"
```

Key properties to inspect in the command output:

| Property                           | Expected value | Notes                                                                                              |
| ---------------------------------- | -------------- | -------------------------------------------------------------------------------------------------- |
| `ProvisioningState`                | `Succeeded`    | Confirms the resource deployment completed successfully.                                           |
| `CircuitProvisioningState`         | `Enabled`      | Indicates the ExpressRoute circuit is enabled on the Azure side.                                   |
| `ServiceProviderProvisioningState` | `Provisioned`  | Shows the service provider has completed their provisioning (only relevant when using a provider). |

If any of the above states do not match the expected values, the problem is likely at provisioning or with the service provider. Typical next steps are to check the provider's provisioning console/status, verify ordering/billing, and if needed, open a support request with the provider or Microsoft.

Example output (values redacted where appropriate):

```powershell theme={null}
Name                           : Lab-ER-Circuit
ResourceGroupName              : Lab-Network-RG
Location                       : westus
Id                             : /subscriptions/3e45ff24-22aa-56ea-d219-0b/resourceGroups/Lab-Network-RG/providers/Microsoft.Network/expressRouteCircuits/Lab-ER-Circuit
Etag                           : W/"#############################"
ProvisioningState              : Succeeded
Sku                            : {
                                  "Name": "Standard_UnlimitedData",
                                  "Tier": "Standard",
                                  "Family": "UnlimitedData"
                                }
CircuitProvisioningState       : Enabled
ServiceProviderProvisioningState: Provisioned
ServiceProviderNotes           :
ServiceProviderProperties      : {
                                  "ServiceProviderName": "*****",
                                  "PeeringLocation": "******",
                                  "BandwidthInMbps": 200
                                }
ServiceKey                     : ****************
Peerings                       : []
Authorizations                 : []
```

<Callout icon="lightbulb">
  If any of these states are not as expected, the issue is likely at the provisioning or service-provider level. Common next steps are to verify the provider's provisioning status, confirm billing/ordering, and open a support request with the provider or Microsoft if needed.
</Callout>

Portal verification

* Open the Azure portal and navigate to your ExpressRoute circuit resource.
* On the Overview blade you will see the circuit’s Provisioning and service provider status.
* If the portal shows mismatched states, capture screenshots and correlate timestamps with your provider’s status information before escalating.

<Frame>
  <img alt="The image shows a dashboard view of an Azure ExpressRoute circuit, displaying details like resource group, provider, circuit status (enabled), provider status (provisioned), and other configuration settings." />
</Frame>

Troubleshooting checklist

* Confirm the Azure-side states (`ProvisioningState`, `CircuitProvisioningState`) are as expected.
* Verify the service provider’s provisioning and circuit activation status.
* Ensure the circuit’s `ServiceKey` and peering details match what the provider has on record.
* Check for any pending authorizations or missing peering configurations.
* If everything appears correct and traffic still isn't flowing, open a support request with Microsoft and/or your service provider and provide the command output and portal screenshots.

Links and references

* [ExpressRoute overview (Microsoft Docs)](https://learn.microsoft.com/azure/expressroute/)
* [Get-AzExpressRouteCircuit (PowerShell)](https://learn.microsoft.com/powershell/module/az.network/get-azexpressroutecircuit)
* [Azure PowerShell documentation](https://learn.microsoft.com/azure/developer/powershell/)
* [Azure portal](https://portal.azure.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6190597d-0e7a-4ffd-ac5d-afe70f482a27/lesson/68f35dd5-5e69-4fed-8c84-b33fccef22bb" />
</CardGroup>
