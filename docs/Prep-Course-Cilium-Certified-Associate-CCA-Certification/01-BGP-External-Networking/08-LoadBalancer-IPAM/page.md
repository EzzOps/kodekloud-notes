# Cilium Helm values (example)
kubeProxyReplacement: "strict"

l2announcements:
  enabled: true
```

After updating your Cilium configuration, restart the operator and daemonset so the new settings are applied:

```bash theme={null}
kubectl -n kube-system rollout restart deployment/cilium-operator
kubectl -n kube-system rollout restart ds/cilium
```

## Cilium L2 Announcement Policy (CiliumL2AnnouncementPolicy)

L2 announcements are controlled per service using the CiliumL2AnnouncementPolicy CRD. A policy selects which services should be announced, which nodes are eligible to respond to ARP, which network interfaces to use, and which IP types to advertise (ExternalIPs, LoadBalancer IPs, etc).

Example policy:

```yaml theme={null}
apiVersion: "cilium.io/v2alpha1"
kind: CiliumL2AnnouncementPolicy
metadata:
  name: l2announcement-policy
spec:
  serviceSelector:
    matchLabels:
      app: myapp
  nodeSelector:
    matchExpressions:
      - key: node-role.kubernetes.io/control-plane
        operator: DoesNotExist
  interfaces:
    - "^eth[0-9]+"
  externalIPs: true
  loadBalancerIPs: true
```

Key fields explained:

| Field           | Purpose                                                          | Example                                      |
| --------------- | ---------------------------------------------------------------- | -------------------------------------------- |
| serviceSelector | Selects Services by label to announce their service IPs          | `app: myapp`                                 |
| nodeSelector    | Selects the set of nodes allowed to hold leases / respond to ARP | Exclude control-plane nodes via DoesNotExist |
| interfaces      | Regex list of network interface names on which to respond to ARP | `^eth[0-9]+` matches eth0, eth1, ...         |
| externalIPs     | When true, advertise Service ExternalIPs                         | `true`                                       |
| loadBalancerIPs | When true, advertise LoadBalancer service IPs                    | `true`                                       |

Notes:

* The interfaces list accepts regular expressions applied to node interface names, giving fine control over which NICs will answer ARP.
* nodeSelector controls which nodes can acquire a lease for a given service IP; only eligible nodes will be chosen.

## Verifying configuration and runtime state

Describe the policy to inspect spec and status:

```bash theme={null}
kubectl describe ciliuml2announcementpolicy l2announcement-policy
```

Truncated sample output:

```text theme={null}
Name:                   l2announcement-policy
Namespace:
Labels:                 <none>
Annotations:            <none>
API Version:            cilium.io/v2alpha1
Kind:                   CiliumL2AnnouncementPolicy
Metadata:
  Creation Timestamp:   2025-06-03T12:57:06Z
  Generation:           1
  Resource Version:     1193
  UID:                  <uid>
Spec:
  Service Selector:     app=myapp
  Node Selector:        (matchExpressions: key=node-role.kubernetes.io/control-plane, operator=DoesNotExist)
  Interfaces:           ["^eth[0-9]+"]
  External IPs:         true
  Load Balancer IPs:    true
Status:
  <status fields showing assigned leases and nodes>
```

Cilium uses Kubernetes Lease objects to assign which node will answer ARP for each service IP. To list leases managed by Cilium:

```bash theme={null}
kubectl -n kube-system get lease
```

Sample lease output:

```text theme={null}
NAME                                      HOLDER                AGE
cilium-l2announce-default-app1-service   my-cluster-worker2    35m
cilium-l2announce-default-app2-service   my-cluster-worker     35m
```

Interpretation:

* HOLDER shows the node currently answering ARP for the service IP.
* If the holder node fails or loses eligibility, the lease will be acquired by another eligible node, which then begins responding — providing automatic failover.

## Troubleshooting tips

* Confirm nodes and external clients are on the same L2 subnet/VLAN.
* Verify the interface regex matches the actual interface name (check with ip link show).
* Ensure kube-proxy replacement is enabled (kubeProxyReplacement: "strict") before enabling l2announcements.
* Inspect Cilium logs on nodes and the cilium-operator for errors about leases or ARP handling:
  * kubectl -n kube-system logs ds/cilium
  * kubectl -n kube-system logs deployment/cilium-operator

## References

* [Cilium Documentation — L2 announcements](https://docs.cilium.io/en/stable/)
* [Kubernetes Concepts — Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Kubernetes Leases API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#lease-v1-coordination-k8s-io)

That covers the fundamentals: how Cilium L2 announcement operates on flat L2 networks, how to enable it, how to write per‑service policies, and how to verify which nodes are announcing which service IPs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/044a2c60-e7c5-42dc-8715-0385137cc255" />
</CardGroup>


# LoadBalancer IPAM

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/LoadBalancer-IPAM/page

Explains Cilium LoadBalancer IPAM, configuring IP pools, allocating external IPs for LoadBalancer Services, and methods to advertise or route those IPs to the cluster

In this lesson we cover Cilium's LoadBalancer IPAM: how Cilium can allocate external IP addresses for Kubernetes LoadBalancer Services and how to make those IPs reachable from your network.

Why this matters

* In cloud providers (for example, EKS on AWS) creating a Service of type LoadBalancer usually triggers the cloud provider to provision a load balancer and return an external IP or DNS name (for example, an [AWS ELB](https://aws.amazon.com/elasticloadbalancing/) DNS entry).
* On-premise clusters typically use components like [MetalLB](https://metallb.universe.tf/) to provide external IPs.
* Cilium’s LoadBalancer IPAM eliminates the need for separate tooling by allocating external IPs directly from configured pools and exposing them as the Service EXTERNAL-IP.

How it looks in Kubernetes
When Cilium assigns an external IP to a Service, it appears in the Service listing:

```bash theme={null}
user1@control-plane:~$ kubectl get svc
NAME              TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
kubernetes        ClusterIP      10.96.0.1      <none>        443/TCP          36d
myapp-service     LoadBalancer   10.98.13.153   10.0.10.1     80:30699/TCP     170m
```

Traffic sent to that EXTERNAL-IP will be routed to the Service and then to the pods backing it, provided the network fabric advertises or forwards that IP to the cluster.

How to configure LoadBalancer IPAM (CiliumLoadBalancerIPPool)
Create a Cilium custom resource of kind CiliumLoadBalancerIPPool describing the address ranges Cilium can use and optional selectors that control which Services may receive external IPs.

Example manifest:

```yaml theme={null}
apiVersion: cilium.io/v2alpha1
kind: CiliumLoadBalancerIPPool
metadata:
  name: blue-pool
spec:
  blocks:
    - cidr: "10.0.10.0/24"
    - cidr: "2004::0/64"
    - start: "20.0.20.100"
      stop: "20.0.20.200"
    - start: "1.2.3.4"
  serviceSelector:
    matchLabels:
      color: red
```

Spec fields explained

* apiVersion / kind / metadata.name: standard Kubernetes CR metadata.
* spec.blocks: one or more blocks from which external IPs are allocated.
* spec.serviceSelector: (optional) restricts allocation to Services matching the provided labels.

Types of blocks supported

| Block type       | Description                                                     | Example                                       |
| ---------------- | --------------------------------------------------------------- | --------------------------------------------- |
| CIDR             | A CIDR range (IPv4 or IPv6) from which Cilium will allocate IPs | `cidr: "10.0.10.0/24"`                        |
| Start/Stop range | An explicit sequential range between two addresses              | `start: "20.0.20.100"`, `stop: "20.0.20.200"` |
| Single IP        | A start-only entry to represent a single IP                     | `start: "1.2.3.4"`                            |

Service selector behavior

* If you include spec.serviceSelector, only Services that match those labels will be eligible for external IP allocation from this pool.
* In the example above, only Services labeled `color: red` will be assigned IPs from `blue-pool`.

Making the allocated external IPs reachable
Allocating an IP on the Service resource is only half the job — you must ensure external routing/forwarding directs traffic for those IPs to the cluster nodes. Common methods:

| Mechanism                       | When to use                                        | Notes                                                                |
| ------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------- |
| BGP advertisements              | Data center or network fabric supports BGP peering | Use a BGP speaker to advertise pool prefixes to upstream routers     |
| L2 announcements (ARP/NDP)      | Simple L2 networks or when BGP is not available    | Cluster nodes respond to neighbor discovery for allocated IPs        |
| Static routing (network config) | Small deployments or lab environments              | Add static routes pointing to cluster nodes or load balancer devices |

Verification and troubleshooting

* Verify the pool CR exists:
  * kubectl get ciliumloadbalancerippool -A
  * kubectl describe ciliumloadbalancerippool blue-pool
* Check Service allocation:
  * kubectl get svc myapp-service -o wide
  * kubectl describe svc myapp-service
* Confirm network reachability:
  * From outside the cluster, ping or curl the EXTERNAL-IP.
  * Use network tools on upstream routers to verify routes or BGP advertisements.
* Logs and Cilium status:
  * Check Cilium agent logs on nodes for IPAM-related messages.
  * Inspect Cilium control plane status (see Cilium documentation for cluster-specific commands).

Best practices

* Only include pool ranges that your network fabric can route to the cluster.
* Use selectors to separate pools by environment (prod/staging) or by tenant.
* Prefer advertising the entire pool prefix via BGP when possible — it simplifies routing and scales better than per-IP static routes.

Links and references

* [Cilium LoadBalancer IPAM documentation](https://docs.cilium.io/en/stable/loadbalancer_ipam/)
* [Kubernetes Service types](https://kubernetes.io/docs/concepts/services-networking/service/)
* [MetalLB project](https://metallb.universe.tf/)
* [AWS Elastic Load Balancing (ELB)](https://aws.amazon.com/elasticloadbalancing/)
* [BGP overview](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)

Important: you must ensure that external routing/forwarding is configured so traffic destined to those allocated external IPs actually reaches your cluster. Common ways to advertise or make those routes reachable include:

* BGP advertisements from the cluster (peering with a router or BGP speaker).
* L2 (ARP/NDP) announcements so the cluster responds to neighbor discovery for the IPs.

BGP and other advertisement mechanisms are commonly used to advertise those allocated external IPs to the wider network so they become reachable.

<Callout icon="lightbulb">
  When creating pools, include only ranges that your network fabric can actually route to the cluster. Otherwise external traffic won't reach the assigned IPs even though Services will show the EXTERNAL-IP.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/9d32cc1f-26d5-424a-8f19-461cab3ab72d" />
</CardGroup>
