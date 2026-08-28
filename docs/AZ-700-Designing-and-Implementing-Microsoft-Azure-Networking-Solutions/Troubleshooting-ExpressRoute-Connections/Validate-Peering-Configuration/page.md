# Validate Peering Configuration

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Troubleshooting-ExpressRoute-Connections/Validate-Peering-Configuration/page

Guide to validating Azure ExpressRoute peerings via portal, Azure CLI and PowerShell including checks, troubleshooting steps and configuration verification for BGP, VLANs, ASNs, and IP assignments

After confirming circuit health, the next step is to validate your peering configuration. This ensures the peerings for an ExpressRoute circuit are present, properly provisioned, and ready for BGP session establishment and traffic flow.

This guide shows how to verify peerings both in the Azure portal and from the command line (Azure CLI and PowerShell). It also includes common troubleshooting steps and quick checks to help you identify configuration mismatches.

## What to verify (Quick checklist)

* Peerings (Private, Microsoft, Public) exist for the circuit.
* Each peering's provisioning state is `Provisioned`.
* Primary and secondary IP addresses for Private peering are present and correct.
* VLAN ID and peer ASN match what your connectivity provider expects.
* BGP session parameters (peer ASN, authentication, passwords) are consistent on both sides.

<Callout icon="lightbulb">
  Before making changes, record the current peering settings (VLAN, ASN, IP pairs). You can use the Azure CLI or PowerShell to export these settings for auditing or troubleshooting.
</Callout>

## Verify in the Azure portal

1. Open the Azure portal and navigate to your ExpressRoute circuit.
2. From the circuit Overview, open the "Peerings" section.
3. Confirm the configured peerings appear (for example: Private, Microsoft, Public—as applicable).
4. For each peering:
   * Check the provisioning status: it should be `Provisioned`.
   * For Private peering, confirm both primary and secondary IP addresses are populated and match your design.
   * Validate VLAN ID and peer ASN are correct for your environment.

Mismatches or missing entries commonly indicate configuration issues that will prevent BGP session establishment or traffic flow.

## Command-line checks

Use the CLI for scripted validation and quick automation-friendly checks.

* Azure CLI (recommended for scripting)

```bash theme={null}
