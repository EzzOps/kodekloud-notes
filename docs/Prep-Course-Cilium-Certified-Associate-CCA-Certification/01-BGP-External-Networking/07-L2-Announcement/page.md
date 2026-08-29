# L2 Announcement

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/L2-Announcement/page

Explains Cilium L2 announcement allowing cluster nodes to reply to ARP for service IPs on a flat Layer 2 network so external hosts reach services with per-service failover.

This lesson explains Cilium's L2 announcement feature: how it lets cluster nodes respond to ARP for service IPs on a flat Layer‑2 network so external hosts on the same broadcast domain can reach cluster services without BGP.

How it works at a glance:

* When a Service is assigned an IP on the local L2 subnet (for example, 172.16.1.250), hosts on that subnet may ARP for that IP.
* With L2 announce enabled, Cilium elects a node to claim the service IP via an ARP reply using the node’s MAC.
* The external sender directs traffic to the node’s MAC; that node forwards traffic into the cluster to the service endpoints.
* Different services can be announced by different nodes, enabling per‑service placement and failover without running BGP.

<Frame>
  <img alt="A network diagram titled &#x22;L2Announce&#x22; showing two nodes with services (db-service 172.16.1.250 and backend-service 172.16.1.251), each node's IP/MAC details, and users connected to the 172.16.1.0/24 subnet." />
</Frame>

When to use L2 announce

* Use L2 announce when cluster nodes and external clients share the same L2 broadcast domain (same VLAN/subnet).
* Do not use L2 announce to advertise services across routed networks or different subnets — use BGP-based advertisement for routed domains.

> **lightbulb** Enable L2 announce only when your nodes and external clients are on the same broadcast domain. If your network is routed across subnets, use BGP-based advertisement instead.

## Benefits and tradeoffs

* Benefits: Simple to configure for flat networks, no router adjacency or BGP required, per-service assignment and automatic failover via leases.
* Tradeoffs: Works only within the same L2 domain; not suitable for multi‑subnet/routed environments.

## Enabling L2 announce

Prerequisite: kube-proxy replacement must be enabled in Cilium (required for L2 announcement).

Example Cilium Helm values (or equivalent installation manifest changes):

```yaml theme={null}
