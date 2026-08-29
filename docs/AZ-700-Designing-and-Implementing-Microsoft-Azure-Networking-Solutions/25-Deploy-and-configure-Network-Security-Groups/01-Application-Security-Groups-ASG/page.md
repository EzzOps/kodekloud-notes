# Application Security Groups ASG

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-and-configure-Network-Security-Groups/Application-Security-Groups-ASG/page

Explains Azure Application Security Groups for grouping network interfaces and simplifying Network Security Group rules to enforce scalable role based VM network access and security

Application Security Groups (ASGs) provide an application-centric way to manage Network Security Group (NSG) rules in Azure. Instead of writing rules that target static IP addresses, ASGs let you group network interfaces (NICs) — and by extension the virtual machines that own those NICs — and reference those groups in NSG rules. This enables dynamic, reusable, and scalable security policies.

Key benefits:

* Group NICs logically regardless of IP address or subnet.
* A NIC can belong to multiple ASGs; an ASG can be referenced by many NSGs.
* Simplifies rule maintenance when VMs scale, are replaced, or move subnets.

<Frame>
  <img alt="The image shows the network settings for a virtual machine in Microsoft Azure, displaying inbound and outbound port rules. The interface allows management of security configurations for VM communications." />
</Frame>

## How ASGs work (brief)

* Create an ASG and add NICs as members.
* Reference the ASG in NSG rules as source or destination.
* When traffic is evaluated, NSGs match against the ASG membership (not IPs).
* Use ASGs to build layered, role-based network security policies.

## Example scenario (problem to solve)

* A subnet has a broad NSG rule that allows access to a storage account — by default every VM in the subnet inherits it.
* Requirement: Only specific VMs (lab1 and lab2) should access the storage account; lab3 must be excluded.
* Without ASGs, you would manually maintain IP addresses in NSG rules — error-prone and hard to scale.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface, displaying the network settings for a virtual machine named &#x22;vm-nsg-lab-1,&#x22; including details like network interface, IP addresses, and security configuration." />
</Frame>

Solution overview:

1. Create an ASG (for example, `ASG-storage-servers`).
2. Associate the NICs for `lab1` and `lab2` with that ASG.
3. Update NSG rules to reference the ASG (instead of IP addresses).
4. Verify that `lab1`/`lab2` can access the Storage service and that `lab3` cannot.

## Step-by-step: Create ASG and enforce NSG rules

1. Create an ASG
   * In the Azure portal search for "Application security groups" → Add → provide a name such as `ASG-storage-servers`.

2. Add NICs to the ASG
   * Open the VM → Networking → Network interface → Application security groups → Add → select `ASG-storage-servers`.
   * Repeat for the second VM (`lab2`).

3. Consider NIC-level NSGs
   * If a NIC-level NSG exists, it will be evaluated together with subnet-level NSGs. To ensure consistent behavior, either disassociate the NIC-level NSG or update its rules so they don't conflict.

You can inspect the NSG and its current rules to confirm the configuration:

<Frame>
  <img alt="The image shows a Microsoft Azure interface displaying the security rules for a network security group named &#x22;nsg-lab-01,&#x22; listing both inbound and outbound rules with their details such as priority, name, port, protocol, source, destination, and action." />
</Frame>

4. Create the NSG rule referencing the ASG
   * In the NSG outbound (or inbound) rules pane, click Add and set:
     * Source: `ASG-storage-servers`
     * Destination: Service tag `Storage`
     * Destination ports: `80, 443` (or ports required by your service)
     * Protocol: `Any` (or `TCP` to restrict)
     * Action: `Allow`
     * Priority: choose a lower numeric value than an existing deny rule (e.g., `100` if a Deny is `200`)

Open the NSG outbound rules pane and click Add to configure the rule:

<Frame>
  <img alt="The image shows a network security group interface with outbound security rules listed on the left and a form to add a new outbound security rule on the right." />
</Frame>

After adding the rule, the NSG should list the new allow rule (for example `AllowStorage`) that permits traffic from your ASG to the Storage service tag on the specified ports.

<Frame>
  <img alt="The image shows a list of outbound security rules in a network security group, detailing various rules with priorities, names, ports, protocols, sources, destinations, and actions (allow or deny). A notification indicates the successful creation of a security rule named 'AllowStorage'." />
</Frame>

## Verify connectivity from the VMs

* From a VM in the ASG (`lab1` or `lab2`), you should be able to reach the storage account.
* From a VM not in the ASG (`lab3`), access should be blocked by the subnet-level deny rule or by the absence of the Allow condition.

Example commands (replace IP/hostnames with your environment values):

```bash theme={null}
