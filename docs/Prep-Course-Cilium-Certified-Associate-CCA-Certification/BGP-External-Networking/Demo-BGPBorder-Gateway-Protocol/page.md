# Demo BGPBorder Gateway Protocol

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/Demo-BGPBorder-Gateway-Protocol/page

Guide to enable and configure Cilium BGP control plane on Kubernetes to advertise Pod CIDRs and Service IPs to external routers for direct routing and ECMP.

In this lesson you’ll enable and configure BGP on a Cilium-based Kubernetes cluster so the cluster can advertise Pod CIDRs and Service IPs to an external router. This allows your physical network to route directly to nodes and enables ECMP when multiple nodes advertise the same service IP.

Topology overview:

<Frame>
  <img alt="A network diagram showing a control-plane and two worker nodes, each with an ens33 interface and pod CIDRs (10.0.1.0/24 and 10.0.2.0/24) connected to a central router (5.5.5.5). The worker nodes establish BGP peering with the router to advertise their networks." />
</Frame>

* 3-node cluster: control-plane, worker1, worker2.
* Each node sits on a different L2 network; all are reachable via a central router (the “outside world”).
* Router loopback: 5.5.5.5 — worker1 and worker2 will peer to that IP and advertise their Pod CIDRs and service IPs.

Overview of steps

1. Enable Cilium’s BGP control plane via Helm values.
2. Restart Cilium operator and agents to pick up the change.
3. Label nodes to select where BGP instances should run.
4. Create three Cilium CRDs in order:
   * CiliumBGPAdvertisement — defines what to advertise (PodCIDR, Service types, attributes).
   * CiliumBGPPeerConfig — peer-level settings (timers, multihop, address families).
   * CiliumBGPClusterConfig — cluster-level config (which nodes, BGP instances & peers).
5. Apply resources and validate peers, sessions and routes.
6. Inspect Cilium logs on the agent if troubleshooting is required.

Prerequisites

* A running Kubernetes cluster with Cilium installed.
* Helm access to upgrade Cilium (if needed).
* Network reachability between nodes and the external router (ensure any firewall/NAT allows BGP TCP/179 or multihop TTL as configured).

Enable the BGP control plane in Cilium
Edit your Cilium Helm values (values.yaml) and enable the BGP control plane:

```yaml theme={null}
