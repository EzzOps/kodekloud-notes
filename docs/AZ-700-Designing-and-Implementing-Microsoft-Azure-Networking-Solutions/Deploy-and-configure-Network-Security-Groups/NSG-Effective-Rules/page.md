# NSG Effective Rules

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-and-configure-Network-Security-Groups/NSG-Effective-Rules/page

Explains how Azure subnet and NIC network security groups combine to produce effective NIC rules, how denies override allows, and how to view and troubleshoot those rules.

Network security groups (NSGs) control network traffic to and from Azure resources. When NSGs are applied at both the subnet and network interface (NIC) levels, Azure evaluates each NSG independently and then combines the results to produce the effective rules that govern traffic for that NIC. The “effective rules” are the net, enforceable set of permissions for traffic to or from a VM’s NIC.

## Key concepts (quick summary)

* Azure evaluates subnet-level NSG and NIC-level NSG separately, then intersects their results.
* For traffic to be allowed, at least one rule in *each* NSG must permit the traffic (this can be a user-defined allow or a system default allow).
* If either NSG explicitly denies or implicitly denies (no allow rule), the traffic is blocked.

## Traffic evaluation order

Understanding the order helps reason about how Azure checks packets, though the final result is always the intersection of both NSGs.

| Traffic direction  | Evaluation order     |
| ------------------ | -------------------- |
| Inbound (to VM)    | Subnet NSG → NIC NSG |
| Outbound (from VM) | NIC NSG → Subnet NSG |

Note: The above order affects how you trace which rule matched first in logs or diagnostics, but it does not change the rule intersection logic — both NSGs must allow traffic.

## Common scenarios (what the effective decision becomes)

| Subnet NSG                       | NIC NSG | Effective result                                        |
| -------------------------------- | ------- | ------------------------------------------------------- |
| Allow                            | Allow   | Allowed                                                 |
| Allow                            | Deny    | Denied                                                  |
| Deny                             | Allow   | Denied                                                  |
| No explicit allow (default deny) | Allow   | Denied (unless a default allow exists for that traffic) |

<Callout icon="lightbulb">
  Remember: effective rules reflect the combined outcome of both subnet and NIC NSGs. A single deny in either NSG blocks the traffic even if the other NSG allows it.
</Callout>

## Why effective rules matter

* They simplify troubleshooting: instead of manually inspecting priorities and rules across multiple NSGs, you can view the NIC’s effective rules to see the exact rule set that applies.
* They clarify conflicts: effective rules show when an allow in one NSG gets overridden by a deny in the other.
* They help validate security posture: you can confirm which traffic is permitted or blocked at the NIC level before troubleshooting connectivity or implementing new rules.

## How to inspect effective rules

You can view effective NSG rules in the Azure Portal or via CLI/PowerShell:

* Azure Portal: Navigate to the VM → Networking → click the NIC → “Effective security rules” (or use the “Network Interface” resource and select Effective security rules).
* Azure CLI example:
  * Use `az network nic show-effective-nsg --name <nic-name> --resource-group <rg>` (refer to Azure CLI docs for exact flags).
* Azure PowerShell example:
  * Use `Get-AzEffectiveNetworkSecurityGroup -NetworkInterfaceName <nic-name> -ResourceGroupName <rg>` (refer to Azure PowerShell docs for exact usage).

## Troubleshooting tips

* Check both NSGs (subnet and NIC) for explicit denies or high-priority rules that might block traffic.
* Confirm the effective rules in the portal to quickly identify which rule(s) matched.
* Remember default NSG rules exist (e.g., Azure platform rules); these can allow or deny traffic if no custom rules match.
* When testing, ensure the rule priorities and source/destination ranges are correct and that you’re inspecting the same direction (inbound vs outbound) as the failing traffic.

## Next steps

* Learn how to create and manage NSG rules to control traffic precisely.
* Use effective rules to validate and iterate on security configurations before and after deployment.

## Links and references

* [Azure NSG overview](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)
* [How to view effective network security groups in Azure Portal](https://learn.microsoft.com/azure/virtual-network/tutorial-filter-network-traffic#view-effective-security-rules)
* [Azure CLI documentation](https://learn.microsoft.com/cli/azure/network/nic#az-network-nic-show-effective-nsg)
* [Azure PowerShell documentation](https://learn.microsoft.com/powershell/module/az.network/get-azeffectivenetworksecuritygroup)

CardGroup and Card components can be used to surface specific quick links, examples, or playbooks for your team’s runbooks if desired.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f311416f-4844-43ee-bc18-4ad6b6f0b71a/lesson/1dac44cc-b2fb-4973-bc78-1908b2498d83" />
</CardGroup>
