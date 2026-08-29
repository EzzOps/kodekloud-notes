# excerpt from values.yaml
bgpControlPlane:
  # -- Enables the BGP control plane.
  enabled: true
  # -- SecretsNamespace is the namespace which BGP support will retrieve secrets from.
```

Upgrade the Cilium release and restart relevant components so the changes take effect:

```bash theme={null}
# (example; use your release name/context as appropriate)
helm upgrade cilium cilium/cilium -f values.yaml --namespace kube-system

# Restart the operator and agents to pick up the change
kubectl rollout restart deploy cilium-operator -n kube-system
kubectl rollout restart ds cilium -n kube-system
```

Label the nodes where BGP should run
In this demo BGP runs only on worker1 and worker2. Add a label that the cluster config will match on (e.g. bgp=true):

```bash theme={null}
kubectl label node worker1 bgp=true
kubectl label node worker2 bgp=true

# Verify labels
kubectl get nodes --show-labels
```

Cilium BGP CRDs — what to create and why
You will create three Cilium CRD resources. Create files for each and apply them in the order shown below.

Summary table of the CRDs:

| Resource               | Purpose                                                                    | Example filename       |
| ---------------------- | -------------------------------------------------------------------------- | ---------------------- |
| CiliumBGPAdvertisement | Define what prefixes to advertise (PodCIDR, Service IPs, route attributes) | bgp-advertisement.yaml |
| CiliumBGPPeerConfig    | Configure peer-level BGP parameters (timers, ebgp-multihop, families)      | bgp-peer-config.yaml   |
| CiliumBGPClusterConfig | Enable BGP instances on a set of selected nodes and define peers           | bgp-config.yaml        |

1. bgp-advertisement.yaml — which prefixes and attributes to advertise

```yaml theme={null}
apiVersion: cilium.io/v2alpha1
kind: CiliumBGPAdvertisement
metadata:
  name: bgp-advertisements
  labels:
    advertise: bgp
spec:
  advertisements:
    - advertisementType: "PodCIDR"
      attributes:
        communities:
          standard: [ "65000:99" ]
        localPreference: 99
    - advertisementType: "Service"
      service:
        addresses:
          - ClusterIP
          - ExternalIP
          - LoadBalancerIP
        selector:
          matchExpressions:
            # this selector will not match any services (it is shown as an example); to select all services omit the selector or use an empty selector
            - { key: somekey, operator: NotIn, values: ['never-used-value'] }
```

Notes:

* The first entry advertises each node’s PodCIDR and attaches route attributes (communities, local preference).
* The second entry advertises service addresses for services matched by the selector. The example selector intentionally matches nothing; to advertise all services omit the selector or use an empty selector. In production prefer a controlled selector to avoid leaking internal service IPs.

2. bgp-peer-config.yaml — peer-level timers, multihop and address families

```yaml theme={null}
apiVersion: cilium.io/v2alpha1
kind: CiliumBGPPeerConfig
metadata:
  name: cilium-peer
spec:
  timers:
    holdTimeSeconds: 9
    keepAliveTimeSeconds: 3
  ebgpMultihop: 5
  families:
    - afi: ipv4
      safi: unicast
```

Notes:

* keepAlive (3s) and holdTime (9s) must match the external router configuration.
* ebgpMultihop permits a TTL > 1 for eBGP sessions when peers are not directly connected.
* This demo uses only IPv4 unicast.

3. bgp-config.yaml — cluster-level config enabling BGP instances on selected nodes

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
    - name: "instance-64000"
      localASN: 64000
      peers:
        - name: "router1"
          peerASN: 65000
          peerAddress: 5.5.5.5
          peerConfigRef:
            name: "cilium-peer"
```

Notes:

* nodeSelector chooses nodes labeled with bgp=true.
* localASN is the ASN used by the node’s BGP instance (here 64000). For eBGP your peer ASN should differ (here 65000).
* peerConfigRef binds this peer to the peer settings defined earlier.

Apply the resources
Apply the three manifests in the following order:

```bash theme={null}
kubectl apply -f bgp-advertisement.yaml
kubectl apply -f bgp-peer-config.yaml
kubectl apply -f bgp-config.yaml
```

Validate BGP peering and routes
Use the Cilium CLI and other tools to validate peers, sessions, and routes.

List BGP peers (shows session state and route counts):

```bash theme={null}
cilium bgp peers
```

Example output:

```text theme={null}
Node        Local AS  Peer AS  Peer Address  Session State  Uptime   Family        Received  Advertised
worker1     64000     65000    5.5.5.5       established    11m5s    ipv4/unicast  10        8
worker2     64000     65000    5.5.5.5       established    11m3s    ipv4/unicast  3         8
```

* Session State "established" means the BGP neighborship is up.
* Received & Advertised columns show route counts from/to the peer.

Show routes advertised by the cluster (IPv4 unicast):

```bash theme={null}
cilium bgp routes advertised ipv4 unicast
```

Example output (truncated):

```text theme={null}
Node      VRouter  Peer     Prefix           Nexthop             Age    Attrs
worker1   64000    5.5.5.5  10.0.1.0/24      192.168.211.128     11m24s [{Origin: i} {AsPath: 64000} {Nexthop: 192.168.211.128} {Communities: 65000:99}]
worker2   64000    5.5.5.5  10.0.2.0/24      192.168.44.128      11m24s [{Origin: i} {AsPath: 64000} {Nexthop: 192.168.44.128} {Communities: 65000:99}]
# plus service IPs (per service address types) appear here as /32 prefixes
```

Router-side verification (example using Bird)
On your external router, confirm it has learned the Pod and service routes. Example Bird command and sample result:

```bash theme={null}
sudo birdc show route table master4
```

Example relevant lines:

```text theme={null}
10.0.1.0/24           unicast [worker1 00:18:02.463 from 192.168.211.128] * (100/?)[AS64000i]
    via 192.168.223.2 on ens33
10.0.2.0/24           unicast [worker2 00:18:04.466 from 192.168.44.128] * (100/?)[AS64000i]
    via 192.168.223.2 on ens33
172.19.255.121/32     unicast [worker2 ...]  (and also from worker1)  # external LB IP learned from both nodes
```

* When the router learns the same service IP from multiple nodes, it can use ECMP (equal-cost multipath) for load distribution.

Troubleshooting — inspect Cilium agent logs
If peers aren’t establishing, inspect the cilium-agent logs on the node running the BGP control plane and filter for bgp-control-plane entries:

```bash theme={null}
# find a cilium agent pod for the node you want to inspect
kubectl get pods -n kube-system -o wide | grep -i cilium

# show logs and filter for bgp-control-plane messages
kubectl logs <cilium-agent-pod-name> -n kube-system | grep bgp-control-plane
```

Sample log snippets indicating BGP initialization and peer events:

```text theme={null}
time="..." level=info msg="Cilium BGP Control Plane Controller now running..." subsys=bgp-control-plane
time="..." level=info msg="Registering BGP instance" instance=instance-64000 subsys=bgp-control-plane
time="..." level=info msg="Adding peer" instance=instance-64000 peer=router1 reconciler=Neighbor subsys=bgp-control-plane
time="..." level=info msg="Peer Up" Key=5.5.5.5 State=BGP_FSM_OPENCONFIRM Topic=Peer asn=64000 subsys=bgp-control-plane
```

Best practices and tips

<Callout icon="lightbulb">
  * Choose ASNs, BGP timers and ebgp-multihop values consistent with your physical network and external router configuration.
  * Use selectors in CiliumBGPAdvertisement to control which services are announced; avoid advertising all service IPs in production unless intentionally required.
  * Monitor route advertisements and BGP session health with the Cilium CLI and your router tooling (e.g., Bird, FRR).
</Callout>

Wrap-up

* You enabled Cilium’s BGP control plane, configured node-level BGP instances, established a peer to an external router, and advertised Pod CIDRs and service IPs.
* With these announcements your physical network can natively route traffic to nodes and support ECMP for service IPs advertised by multiple nodes.

Links and references

* [Cilium Documentation — BGP](https://docs.cilium.io/en/stable/)
* [Cilium CLI reference](https://docs.cilium.io/en/stable/reference/cli/)
* [BIRD Internet Routing Daemon](https://bird.network.cz/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [BGP — Wikipedia](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/3c2d3813-735e-4827-ae62-df13c6e51351" />
</CardGroup>


# Demo Egress Gateway

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/Demo-Egress-Gateway/page

Guide to configuring and testing a Cilium egress gateway in Kubernetes, demonstrating centralized SNAT egress, VXLAN forwarding, egress policies, and packet capture verification

This guide demonstrates how to configure an egress gateway in a Cilium-enabled Kubernetes cluster and how to inspect traffic flows before and after enabling it. You'll see how pods are SNAT'd by default, how to enforce egress via a chosen node, and how Cilium forwards traffic (often using VXLAN encapsulation) to the egress node.

What we'll demonstrate

* Default behavior: pod egress is SNAT'd to the node IP.
* Enabling Cilium egress gateway and applying a CiliumEgressGatewayPolicy.
* Capturing traffic to confirm egress from a single gateway node and inspecting VXLAN encapsulation.

Environment overview

|       Component | Description                                                                                                  |
| --------------: | ------------------------------------------------------------------------------------------------------------ |
|         Cluster | 3 nodes: 1 control-plane, 2 workers                                                                          |
|      Networking | Each node attached to a router on a separate subnet; router used for packet captures                         |
| Cilium features | kube-proxy replacement enabled, eBPF masquerade enabled, Cilium version with egress gateway support (v1.17+) |

<Callout icon="lightbulb">
  Prerequisites: Cilium must be installed with kube-proxy replacement enabled (kubeProxyReplacement), eBPF masquerade (bpf.masquerade) turned on, and a Cilium release that supports the egress gateway feature. Confirm your cluster networking and node labeling permissions before proceeding.
</Callout>

Cluster pod listing (example)

```bash theme={null}
user1@control-plane:~$ kubectl get pod -o wide
NAME                       READY  STATUS   RESTARTS  AGE    IP           NODE     NOMINATED NODE   READINESS GATES
app1-75c78488c4-d9xw8      1/1    Running  0         3h54s  10.0.2.182   worker2  <none>           <none>
app1-75c78488c4-dbf66      1/1    Running  0         3h54s  10.0.2.126   worker2  <none>           <none>
app1-75c78488c4-dq2dw      1/1    Running  0         3h54s  10.0.1.40    worker1  <none>           <none>
app1-75c78488c4-g521f      1/1    Running  0         3h54s  10.0.1.234   worker1  <none>           <none>
...
user1@control-plane:~$
```

Verify outbound connectivity from a pod (example)

```bash theme={null}
user1@control-plane:~$ kubectl exec -it app1-75c78488c4-dq2dw -- bash
app1-75c78488c4-dq2dw:~# ping -c 3 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=125 time=16.7 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=125 time=15.5 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=125 time=15.9 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
rtt min/avg/max/mdev = 15.495/16.039/16.739/0.519 ms
app1-75c78488c4-dq2dw:~# exit
```

Default behavior (no egress gateway)

* Flow: pod IP → node → router → internet. The node performs SNAT, so the router and external services see the node IP as the source address, not the pod IP.
* If pods run on multiple worker nodes, external services observe different source IPs depending on the node used.

Example router tcpdump showing node IP as source

```bash theme={null}
user1@router:~$ sudo tcpdump -i ens39 -nnv host 8.8.8.8
tcpdump: listening on ens39, link-type EN10MB (Ethernet), snapshot length 262144 bytes
02:09:23.781495 IP (tos 0x0, ttl 62, id 49799, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.211.128 > 8.8.8.8: ICMP echo request, id 2, seq 16, length 64
02:09:23.798489 IP (tos 0x0, ttl 127, id 62091, offset 0, flags [none], proto ICMP (1), length 84)
    8.8.8.8 > 192.168.211.128: ICMP echo reply, id 2, seq 16, length 64
...
```

Node interface example (worker1)

```bash theme={null}
user1@worker1:~$ ip addr show ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:a4:4a:15 brd ff:ff:ff:ff:ff:ff
    inet 192.168.211.128/24 brd 192.168.211.255 scope global ens33
        valid_lft forever preferred_lft forever
```

Explanation diagram:

<Frame>
  <img alt="A simple Kubernetes network diagram showing a control-plane and two worker nodes, each with an ens33 interface IP and a pod CIDR (worker1: 10.0.1.0/24, worker2: 10.0.2.0/24), all connected via a central router with additional interface IPs and external DNS 8.8.8.8." />
</Frame>

How the egress gateway changes traffic flow

* Cilium egress gateway centralizes outbound traffic from selected pods through one or more chosen node(s). Those egress node(s) perform SNAT so the external source IP is the chosen egress IP.
* Internally, Cilium forwards traffic from source nodes to the egress gateway node. In overlay networks (common with Cilium), this forwarding is encapsulated (VXLAN or similar). The egress node decapsulates, performs SNAT, and sends traffic to the internet.

Enable required Cilium options

1. kube-proxy replacement (ensure kubeProxyReplacement is enabled in values):

```yaml theme={null}
kubeProxyReplacement: "true"
```

2. eBPF masquerade (native BPF SNAT):

```yaml theme={null}
bpf:
  masquerade: true
```

3. Enable egress gateway support (depends on Cilium version and values layout). After editing Helm values, upgrade and restart Cilium:

```bash theme={null}
