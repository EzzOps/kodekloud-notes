# List PeerAuthentication resources in the payments namespace
kubectl get peerauthentication -n payments

# Inspect a PeerAuthentication resource to see the mode
kubectl get peerauthentication default -n payments -o yaml
```

Use `istioctl` to inspect a pod and see the applied mTLS settings and relevant policies:

```bash theme={null}
# Describe pod via istioctl to view mTLS and policy details
istioctl x describe pod payment-api-xxx -n payments
```

Verify sidecar injection (the sidecar is the istio-proxy container). A `2/2` READY indicates the application container plus the istio-proxy sidecar:

```bash theme={null}
# Confirm the sidecar is injected — look for READY = 2/2
kubectl get pods -n payments
# Example output:
# NAME             READY   STATUS
# payment-api-xxx  2/2     Running   <-- istio-proxy sidecar present
```

If you see `1/1`, no sidecar is injected and mTLS will not be applied for that pod.

## Rolling out strict mTLS safely

Follow a staged rollout to avoid outages:

1. Enable automatic sidecar injection for the target namespace(s) and restart pods so they pick up the sidecar.
2. Start with `PERMISSIVE` mode at the mesh or namespace level so both mTLS and plaintext are accepted. This allows services not yet meshed to continue communicating.
3. Monitor traffic, Istio telemetry, and logs to detect and remediate failures.
4. Once all workloads show sidecars and traffic is healthy, change the mode to `STRICT` for full enforcement.

This approach mirrors standard safe rollout patterns used for security and policy enforcement.

<Frame>
  <img alt="The image outlines steps for migrating to strict mutual TLS (mTLS) in a Kubernetes environment, including enabling sidecar injection, starting with a permissive mode, monitoring traffic, and switching to strict mode." />
</Frame>

## Quick checklist

* Ensure sidecar injection is enabled for target namespaces.
* Confirm pods show `2/2` READY (application + istio-proxy).
* Start with `PERMISSIVE` to avoid breaking traffic during migration.
* Apply `PeerAuthentication` (`STRICT`) once all workloads are meshed.
* Use `AuthorizationPolicy` to enforce service-to-service access using SPIFFE principals.
* Validate with `istioctl x describe pod` and `kubectl` commands.

<Callout icon="lightbulb">
  Enable sidecar injection for the target namespaces and validate with `kubectl get pods -n <namespace>` (look for `2/2` READY) before switching PeerAuthentication to `STRICT`.
</Callout>

## References

* Istio Service Mesh: [https://learn.kodekloud.com/user/courses/istio-service-mesh](https://learn.kodekloud.com/user/courses/istio-service-mesh)
* SPIFFE: [https://spiffe.io/](https://spiffe.io/)
* Envoy Proxy: [https://www.envoyproxy.io/](https://www.envoyproxy.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/19c3a421-318d-40c7-aeb3-45eebb398056" />
</CardGroup>


# BGPBorder Gateway Protocol

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/BGPBorder-Gateway-Protocol/page

Explains how to integrate BGP with Cilium to advertise pod and service routes for native Kubernetes routing, configuration of CRDs, and troubleshooting

In this lesson we cover how Border Gateway Protocol (BGP) integrates with Cilium so your Kubernetes cluster can advertise pod and service routes to your physical/core network. Using BGP enables native routing (no encapsulation), so external routers can reach pods and services directly without tunnel headers.

This guide explains the two routing modes relevant for BGP, how to enable Cilium's BGP control plane, which custom resources to configure, and how to troubleshoot sessions and advertised routes.

## Routing modes: Tunnel (encapsulation) vs Native routing

Tunnel mode (encapsulation)

* Pod A sends a packet to Pod B using Pod IPs (src = Pod A IP, dst = Pod B IP).
* Cilium encapsulates the packet; the outer packet uses node IPs (node1 -> node2).
* The physical network only needs to route node IPs; node2 decapsulates and forwards to Pod B.
* Because of encapsulation (e.g., VXLAN), the physical network does not need knowledge of pod CIDRs.

Example outer packet addressing:

```text theme={null}
SIP: 172.16.1.1
DIP: 172.16.2.1
```

Native routing

* Pod A sends a packet to Pod B using Pod IPs and no encapsulation is applied.
* The physical network must route pod CIDRs (for example, 192.168.1.0/24 and 192.168.2.0/24).
* One approach is to add static routes on physical routers pointing each pod CIDR to the respective node IP.
* Static routes do not scale (100 nodes → 100 static routes per router), so dynamic routing with BGP is preferred.

<Frame>
  <img alt="A diagram titled &#x22;Routing Modes&#x22; comparing Tunnel and Native Routing, showing two Kubernetes pods in separate podCIDRs (192.168.1.0/24 and 192.168.2.0/24). It illustrates BGP peering to a router with next-hop addresses 172.16.1.1 and 172.16.2.1 for the respective networks." />
</Frame>

Quick comparison

| Mode                   | Encapsulation | Physical network must know pod CIDRs? | Scalability                            |
| ---------------------- | ------------- | ------------------------------------- | -------------------------------------- |
| Tunnel (encapsulation) | Yes           | No                                    | High (no router config)                |
| Native routing         | No            | Yes (or dynamic routing)              | High with BGP; poor with static routes |

## Why use BGP with Cilium?

BGP lets Cilium form peering sessions with physical routers and automatically advertise:

* Pod CIDRs (so routers can forward packets to nodes hosting pods).
* Service IPs (ClusterIP, ExternalIP, LoadBalancerIP) when configured.

This removes manual static routes and enables native cross-network pod connectivity.

Useful references:

* [Cilium BGP integration](https://docs.cilium.io/en/stable/networking/bgp/)
* [Kubernetes networking concepts](https://kubernetes.io/docs/concepts/cluster-administration/networking/)

## Enable the BGP control plane in Cilium

To enable the BGP control plane in the Cilium configuration:

```yaml theme={null}
bgpControlPlane:
  # Enables the BGP control plane.
  enabled: true
```

After enabling, restart the Cilium operator and agents so they pick up the control plane configuration.

## Cilium BGP CRDs — what to create

Three Kubernetes custom resources are typically involved:

|               Resource | Purpose                                                                      | Example                                       |
| ---------------------: | ---------------------------------------------------------------------------- | --------------------------------------------- |
| CiliumBGPClusterConfig | Which nodes run BGP, cluster/local ASN, and peers                            | Select nodes by label and define bgpInstances |
|    CiliumBGPPeerConfig | Peer-specific settings (timers, multihop, families, advertisement selectors) | Referred by peerConfigRef                     |
| CiliumBGPAdvertisement | Which prefixes to advertise (PodCIDR, Service IPs, routes attributes)        | Controls advertisementType and attributes     |

In a typical deployment, label a subset of nodes (e.g., bgp: "true") to run the BGP control plane so you can control how many peers are formed and which interfaces are used.

Example topology: two nodes labeled bgp: "true" with node IPs 172.16.1.1 and 172.16.2.1, pod CIDRs 192.168.1.0/24 and 192.168.2.0/24, and an external router with loopback 5.5.5.5 in AS 65000. Cilium will use local ASN 64000 and peer to the router.

<Frame>
  <img alt="A network diagram titled &#x22;Enabling BGP&#x22; showing two nodes (Node 1 and Node 2) each configured with bgp:true and podCIDRs 192.168.1.0/24 and 192.168.2.0/24. Both nodes (IPs 172.16.1.1 and 172.16.2.1) peer with an external router whose loopback is 5.5.5.5 and AS is 65000." />
</Frame>

## Example resources

CiliumBGPClusterConfig

```yaml theme={null}
apiVersion: cilium.io/v2alpha1
kind: CiliumBGPClusterConfig
metadata:
  name: cilium-bgp
spec:
  nodeSelector:
    matchLabels:
      bgp: "true"
  bgpInstances:
    - name: instance-64000
      localASN: 64000
      peers:
        - name: peer-65000-r1
          peerASN: 65000
          peerAddress: 5.5.5.5
          peerConfigRef:
            name: cilium-peer
```

CiliumBGPPeerConfig (peer settings referenced above)

```yaml theme={null}
apiVersion: cilium.io/v2alpha1
kind: CiliumBGPPeerConfig
metadata:
  name: cilium-peer
spec:
  timers:
    keepAliveTimeSeconds: 3
    holdTimeSeconds: 9
  ebgpMultihop: 5
  families:
    - afi: ipv4
      safi: unicast
      advertisements:
        matchLabels:
          advertise: "bgp"
```

CiliumBGPAdvertisement — advertise PodCIDR and selected Service addresses

```yaml theme={null}
apiVersion: cilium.io/v2alpha1
kind: CiliumBGPAdvertisement
metadata:
  name: bgp-advertisements
  labels:
    advertise: bgp
spec:
  advertisements:
    - advertisementType: PodCIDR
      attributes:
        communities:
          standard: ["65000:99"]
        localPreference: 99
    - advertisementType: Service
      service:
        addresses:
          - ClusterIP
          - ExternalIP
          - LoadBalancerIP
      selector:
        matchExpressions:
          - key: somekey
            operator: NotIn
            values: ["never-used-value"]
```

Key fields explained

* timers.keepAliveTimeSeconds & holdTimeSeconds: govern BGP keepalive and hold intervals.
* ebgpMultihop: TTL for eBGP multi-hop peerings (required when peer is not directly connected).
* families: choose address families (IPv4/IPv6) and safi (e.g., unicast).
* advertisements selector: controls which Advertisement resources a BGPPeer should consult.

<Callout icon="lightbulb">
  If you rely on native routing (no encapsulation), enable PodCIDR advertisements so your physical routers learn how to reach pod networks. Use node labels (nodeSelector) to control which nodes run the BGP control plane and avoid advertising routes from every node if not required.
</Callout>

<Callout icon="warning">
  Be cautious with ebgpMultihop and route attributes. Incorrect multihop or advertisement configuration can cause session flaps or unexpected route leaks. Always validate on a staging router before applying in production.
</Callout>

## Troubleshooting with the Cilium CLI

Useful cilium CLI commands and sample outputs.

List BGP peers and session state:

```bash theme={null}
$ cilium bgp peers
Node       Local AS  Peer AS  Peer Address  Session State  Uptime    Family         Received  Advertised
worker1    64000     65000    5.5.5.5       established    2h2m54s   ipv4/unicast   10        8
worker2    64000     65000    5.5.5.5       established    2h2m57s   ipv4/unicast   3         8
```

Show available/learned routes (defaults to ipv4/unicast):

```bash theme={null}
$ cilium bgp routes available
(Defaulting to `ipv4 unicast` AFI & SAFI, please see help for more options)

Node        VRouter    Prefix                 NextHop    Age       Attrs
worker1     64000      10.0.1.0/24            0.0.0.0    2h4m14s   [{Origin: i} {Nexthop: 0.0.0.0}]
            64000      10.100.67.164/32      0.0.0.0    2h4m14s   [{Origin: i} {Nexthop: 0.0.0.0}]
            64000      10.103.112.96/32      0.0.0.0    2h4m14s   [{Origin: i} {Nexthop: 0.0.0.0}]
worker2     64000      10.0.2.0/24            0.0.0.0    2h4m14s   [{Origin: i} {Nexthop: 0.0.0.0}]
```

Show routes that Cilium has advertised to a peer:

```bash theme={null}
user1@control-plane:~$ cilium bgp routes advertised

Node       VRouter  Peer     Prefix               NextHop           Age     Attrs
worker1    64000    5.5.5.5  10.0.1.0/24          192.168.211.128   2h4m57s [{Origin: i} {AsPath: 64000} {Nexthop: 192.168.211.128} {Communities: 65000:99}]
           64000    5.5.5.5  10.100.67.164/32     192.168.211.128   2h4m57s [{Origin: i} {AsPath: 64000} {Nexthop: 192.168.211.128}]
worker2    64000    5.5.5.5  10.0.2.0/24          192.168.44.128    2h4m57s [{Origin: i} {AsPath: 64000} {Nexthop: 192.168.44.128} {Communities: 65000:99}]
```

What to check if sessions fail

* Verify node selector labels match your CiliumBGPClusterConfig.
* Check network reachability between peers (TCP/179 and any configured multi-hop TTL).
* Confirm ASNs and peerAddress values are correct.
* Inspect Cilium agent/operator logs for BGP negotiation messages.
* Validate that advertisement selectors (labels) match the CiliumBGPAdvertisement resources.

## Summary & next steps

* BGP with Cilium enables scalable native routing for PodCIDRs and service IPs.
* Enable bgpControlPlane in Cilium, label nodes to run BGP, and create CiliumBGPClusterConfig, CiliumBGPPeerConfig, and CiliumBGPAdvertisement resources.
* Use the cilium CLI to inspect peers, learned routes, and advertised prefixes.
* Test in staging before applying to production routers; validate route attributes and policies on both Cilium and your physical routers.

Further reading

* [Cilium BGP documentation](https://docs.cilium.io/en/stable/networking/bgp/)
* [Border Gateway Protocol (BGP) overview](https://www.cloudflare.com/learning/bgp/what-is-bgp/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/1921a7e1-109f-4d9d-b0d0-a54e277bbe8e" />
</CardGroup>
