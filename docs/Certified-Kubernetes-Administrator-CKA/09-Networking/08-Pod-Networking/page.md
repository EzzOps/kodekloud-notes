# Pod Networking

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Networking/Pod-Networking/page

This article explains pod networking in Kubernetes, covering implementation, inter-pod communication, and the role of CNI in managing network interfaces.

Welcome to this deep dive into pod networking in Kubernetes. In this article, we explain how pod networking is implemented within a Kubernetes cluster, detailing the steps that make inter-pod communication seamless across multiple nodes.

Kubernetes clusters consist of multiple master and worker nodes with pre-configured networking that allows full node-to-node communication. We assume that all Kubernetes control plane components (e.g., kube-apiserver, etcd, and kubelet) are already set up properly. With this foundation in place, the next step is deploying your applications with a focus on robust pod-level networking.

> **lightbulb** * Each pod gets a unique IP address.
  * Every pod on a node can reach every other pod on that node using its IP address.
  * Pods across different nodes can communicate using a consistent addressing scheme.

  These requirements ensure that Kubernetes can support both local (node-level) and cross-node communications without relying on NAT rules.

## Understanding the Basics

Before deploying applications, it is crucial to address several questions:

* How are pods assigned IP addresses?
* How do these pods communicate both within a node and across nodes?
* How can services running in these pods be accessed from inside or outside the cluster?

Kubernetes leaves the implementation details for pod networking to the user, as long as the chosen solution meets the basic connectivity requirements. Many networking solutions are available; here, we demonstrate the core concepts using Linux network namespaces, bridge networks, and IP address management inspired by CNI concepts.

### Setting Up a Simple Bridge Network

Below is an example that sets up a simple bridge network and connects network namespaces:

```bash theme={null}
ip link add v-net-0 type bridge
ip link set dev v-net-0 up
ip addr add 192.168.15.5/24 dev v-net-0
ip link add veth-red type veth peer name veth-red-br
ip link set veth-red netns red
ip -n red addr add 192.168.15.1 dev veth-red
ip -n red link set veth-red up
ip link set veth-red-br master v-net-0
ip netns exec blue ip route add 192.168.1.0/24 via 192.168.15.5
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -j MASQUERADE
```

Imagine a cluster with three nodes where every node runs a combination of management and workload pods. Although node roles are flexible, the networking concepts remain consistent across nodes.

### Cluster Network Planning

Consider the following plan for a three-node cluster:

1. **External Network Configuration**: Each node has an IP in the 192.168.1.0 series (e.g., 192.168.1.11, 192.168.1.12, and 192.168.1.13).
2. **Container Network Namespaces**: Kubernetes creates unique network namespaces when containers start. These namespaces must connect to a network to allow inter-container communication.
3. **Bridge Networks on Each Node**: Create a bridge network on every node. Assign a distinct subnet to each bridge, such as:
   * Node one: 10.244.1.0/24
   * Node two: 10.244.2.0/24
   * Node three: 10.244.3.0/24

When a container is created, a virtual cable (veth pair) connects its network namespace to the node’s bridge network. One end is inserted into the container’s namespace and the other attaches to the node’s bridge. An IP address is assigned (for example, 10.244.1.2), and a route to the default gateway is configured before enabling the interface.

Below is a sample snippet from a script that connects a container to the network:

```bash theme={null}
