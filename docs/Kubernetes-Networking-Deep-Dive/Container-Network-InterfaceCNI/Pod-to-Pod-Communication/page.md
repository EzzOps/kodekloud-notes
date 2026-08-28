# Namespace selector with expressions
namespaceSelector:
  matchExpressions:
    - key: environment
      operator: In
      values: ["prod", "staging"]

# Pod selector with labels
podSelector:
  matchLabels:
    app: frontend
```

For IP-based rules, you can exclude subnets:

```yaml theme={null}
ipBlock:
  cidr: 172.17.0.0/16
  except:
    - 172.17.1.0/24
```

### Layer 4 Ports and Protocols

Control ports and protocols (requires Kubernetes v1.25+ for port ranges):

```yaml theme={null}
- to:
    - podSelector:
        matchLabels:
          app: database
  ports:
    - port: 5432
      protocol: TCP
      endPort: 5434
```

* `port`: Single port or starting port of a range
* `protocol`: TCP or UDP (defaults to TCP)
* `endPort`: End of port range (optional)

## Default Policies

By default, all ingress and egress traffic is allowed. You can enforce a “deny all” or “allow all” baseline by using an empty `podSelector: {}`.

<Callout icon="lightbulb">
  An empty `podSelector: {}` matches every pod in the namespace.
</Callout>

### Ingress Defaults

```yaml theme={null}
# Deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
# Allow all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-allow-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - {}
```

### Egress Defaults

```yaml theme={null}
# Deny all egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
    - Egress
---
# Allow all egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-allow-egress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - {}
```

You may combine Ingress and Egress in a single policy or separate them.

## Benefits of Network Policies

* Granular security controls by workload
* Isolation in multi-tenant clusters
* Compliance with [GDPR](https://gdpr.eu), [HIPAA](https://www.hhs.gov/hipaa/), [PCI DSS](https://www.pcisecuritystandards.org/)
* Reduced attack surface by blocking unused paths
* Consistent enforcement across applications

<Frame>
  ![The image lists the benefits of network policies, including enhanced security, workload isolation, compliance, reduced attack surface, and consistency, each with an icon.](https://kodekloud.com/kk-media/image/upload/v1752880286/notes-assets/images/Kubernetes-Networking-Deep-Dive-Network-Policies-Overview/network-policies-benefits-security-isolation.jpg)
</Frame>

## Limitations

Network Policies operate at layers 3 & 4 and have some constraints:

* Cannot enforce a common gateway (service mesh can)
* No built-in TLS termination or deep packet inspection
* Cannot restrict host-level traffic or localhost loops
* No native allow/deny event logging
* Label-based only—cannot target Service objects
* No Layer 7 (HTTP/gRPC) filtering

<Frame>
  ![The image outlines the limitations of network policies, listing six specific tasks they cannot perform, such as forcing traffic through a gateway and handling TLS-related activities. It features a diagram with icons connected to a "Limitation" label.](https://kodekloud.com/kk-media/image/upload/v1752880288/notes-assets/images/Kubernetes-Networking-Deep-Dive-Network-Policies-Overview/network-policies-limitations-diagram.jpg)
</Frame>

## CNI-Specific Enhancements

Several CNI providers extend Kubernetes Network Policies with advanced capabilities:

| CNI Plugin     | Advanced Features                                           |
| -------------- | ----------------------------------------------------------- |
| Project Calico | Global policies, BGP routing, NetworkSets                   |
| Cilium         | Layer 7 HTTP/gRPC filtering, eBPF datapath, Hubble insights |
| Istio          | Service mesh policies, mTLS, ingress/egress gateways        |

<Frame>
  ![The image displays logos and names of various CNI (Container Network Interface) network policies, including Project Calico, Cilium, and Istio.](https://kodekloud.com/kk-media/image/upload/v1752880289/notes-assets/images/Kubernetes-Networking-Deep-Dive-Network-Policies-Overview/cni-network-policies-logos-calico-cilium-istio.jpg)
</Frame>

## Next Steps

You now understand native Kubernetes Network Policies—how to control ingress and egress by pod, namespace, IP block, ports, and ranges. In the next lesson, we’ll apply these concepts in a real-world scenario.

## References

* [Kubernetes NetworkPolicy Documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Project Calico](https://projectcalico.org)
* [Cilium](https://cilium.io)
* [Istio](https://istio.io)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5eea49e6-caea-4e84-88a0-268ea6f263af/lesson/7c0a7521-1366-4036-ab35-f93c414d71b1" />
</CardGroup>


# Pod to Pod Communication

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Container-Network-InterfaceCNI/Pod-to-Pod-Communication/page

This guide covers verifying Cilium, deploying pods, inspecting interfaces, and testing pod communication in a Kubernetes cluster.

Cilium’s CNI plugin provides transparent pod-to-pod connectivity, including support for DNS A records for pod hostnames. This guide walks through verifying Cilium, deploying pods, inspecting veth interfaces, and testing direct IP and DNS-based communication in a Kubernetes cluster.

## 1. Verify Cilium Status

First, confirm that Cilium and its components are up and running:

```bash theme={null}
cilium status
```

You should see output similar to:

```bash theme={null}
Cilium:            OK
Operator:          OK
Envoy DaemonSet:   disabled (using embedded mode)
Hubble Relay:      disabled
ClusterMesh:       disabled

Deployment          cilium-operator      Desired: 1/1, Ready: 1/1, Available: 1/1
DaemonSet           cilium               Desired: 2/2, Ready: 2/2, Available: 2/2
Containers:         cilium (Running)
                    cilium-operator (Running)
Cluster Pods:       2/2 managed by Cilium
Helm chart version: cilium
Image versions:     cilium: quay.io/cilium/cilium:v1.15.3
                    cilium-operator: quay.io/cilium/operator-generic:v1.15.3
```

<Callout icon="lightbulb">
  If `Envoy DaemonSet` is disabled, Cilium is using its embedded proxy mode. For full L7 gateway features, enable the Envoy DaemonSet.
</Callout>

## 2. Deploy Pods and Observe Interface Creation

Apply a manifest (`pods.yaml`) to spin up three simple pods in the default namespace:

```bash theme={null}
kubectl apply -f pods.yaml
```

On your control‐plane node, tail the Cilium daemon logs to watch endpoint creation:

```bash theme={null}
journalctl -u cilium -f
```

You should observe entries like:

```bash theme={null}
level=info msg="Create endpoint request" addressing="&{10.0.1.207 ee7b43f3-... default}" containerID=b1c311eadc2... interface=eth0 subsys=daemon
level=info msg="New endpoint" ciliumEndpointName=default/pod1 ipv4=10.0.1.207 endpointID=1704 subsys=endpoints
```

## 3. Inspect the Pod Interface and Network Namespace

On the node hosting **pod1**, list the CNI veth pair created by Cilium:

```bash theme={null}
ip addr | grep -A1 lxc
```

Example output:

```bash theme={null}
21: lxc7356c0cd4e00@if20: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 900
    link/ether 82:61:ee:60:27:3a brd ff:ff:ff:ff:ff:ff link-netns cni-ba760e87-7617-b4a3-197f-9baf33fa823d
```

Enter the network namespace and inspect `eth0`:

```bash theme={null}
ip netns exec cni-ba760e87-7617-b4a3-197f-9baf33fa823d ip addr show eth0
```

Result:

```bash theme={null}
20: eth0@if21: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 900
    inet 10.0.1.207/32 scope global eth0
```

This IP matches the address reported in the Cilium logs.

## 4. Delete and Recreate a Pod

Delete **pod1** and observe endpoint cleanup:

```bash theme={null}
kubectl delete pod pod1
```

Cilium logs will include:

```bash theme={null}
level=info msg="Delete endpoint by containerID request" containerID=b1c311eacd... endpointID=1704 subsys=daemon
level=info msg="Removed endpoint" ciliumEndpointName=default/pod1 endpointID=1704 subsys=endpoint
```

Verify the veth interface is removed:

```bash theme={null}
ip addr | grep lxc7356c0cd4e00
```

Recreate **pod1**:

```bash theme={null}
kubectl apply -f pods.yaml
kubectl get pods -w
```

Watch for regeneration:

```bash theme={null}
level=info msg="Rewrote endpoint BPF program" ciliumEndpointName=default/pod1 endpointID=3389 subsys=endpoint
```

## 5. Test Pod-to-Pod Connectivity by IP

Retrieve the pod IPs:

```bash theme={null}
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}: {.status.podIP}{"\n"}{end}'
```

| Pod  | IP         |
| ---- | ---------- |
| pod1 | 10.0.1.249 |
| pod2 | 10.0.1.14  |
| pod3 | 10.0.0.245 |

From **pod1**, ping **pod2** (same node):

```bash theme={null}
kubectl exec -it pod1 -- ping -c 4 10.0.1.14
```

Ping **pod3** (remote node):

```bash theme={null}
kubectl exec -it pod1 -- ping -c 4 10.0.0.245
```

And curl an HTTP server on **pod3** (port 80):

```bash theme={null}
kubectl exec -it pod1 -- curl -vvv 10.0.0.245:80
```

## 6. Pod-to-Pod Communication via DNS A Records

Check the pod’s DNS settings:

```bash theme={null}
kubectl exec -it pod1 -- cat /etc/resolv.conf
```

```text theme={null}
search default.svc.cluster.local svc.cluster.local cluster.local
nameserver 10.96.0.10
options ndots:5
```

Cilium automatically creates DNS A records in the format:

```text theme={null}
<ip-with-dashes>.<namespace>.pod.cluster.local
```

For example, to ping **pod3** by DNS:

```bash theme={null}
kubectl exec -it pod1 -- ping -c 4 10-0-0-245.default.pod.cluster.local
```

Or curl by name:

```bash theme={null}
kubectl exec -it pod1 -- curl -vvv http://10-0-0-245.default.pod.cluster.local:80
```

<Callout icon="triangle-alert">
  Pod IPs are ephemeral. DNS A records tied to pod IPs can break when the pod restarts. For stable discovery, use a [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/).
</Callout>

## 7. Summary of Commands

| Task                             | Command                                           |
| -------------------------------- | ------------------------------------------------- |
| Verify Cilium status             | `cilium status`                                   |
| Deploy pods                      | `kubectl apply -f pods.yaml`                      |
| Tail Cilium logs                 | `journalctl -u cilium -f`                         |
| Show veth interfaces             | `ip addr \| grep -A1 lxc`                         |
| Enter pod namespace              | `ip netns exec <netns> ip addr show eth0`         |
| Delete a pod                     | `kubectl delete pod pod1`                         |
| Test connectivity by IP          | `kubectl exec -it pod1 -- ping -c 4 <pod IP>`     |
| Test connectivity via DNS record | `kubectl exec -it pod1 -- ping -c 4 <dns record>` |

## Links and References

* [Cilium Documentation](https://docs.cilium.io/)
* [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/)
* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Linux Network Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)
* [Kubernetes DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5eea49e6-caea-4e84-88a0-268ea6f263af/lesson/4907e379-345a-457a-a53f-3869a820d06a" />
</CardGroup>
