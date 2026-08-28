# Pod Networking

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Container-Orchestration-Networking/Pod-Networking/page

This article explores pod networking in Kubernetes, covering IP address assignment, inter-pod communication, and the use of the Container Network Interface for automation.

Welcome to this comprehensive guide on pod networking in Kubernetes. In this article, we will explore how pods are assigned unique IP addresses and how they communicate both within a single node and across multiple nodes. By understanding these fundamentals, you’ll be better prepared to deploy resilient and scalable applications on your Kubernetes clusters.

So far, you have set up several Kubernetes master and worker nodes with proper networking configurations. The nodes are fully interconnected, and firewalls or network security groups are configured to allow the necessary communication between control plane components such as kube-apiserver, etcd, and kubelets. With control plane setup complete, the next crucial step is configuring the pod network.

Before deploying applications, consider these essential questions:

* How are pods addressed?
* How do pods communicate with one another?
* How can pod services be accessed both from within the cluster and externally?

Kubernetes does not include an out-of-the-box pod networking solution but defines strict requirements that your networking implementation must meet. These requirements include:

* Each pod must receive its own unique IP address.
* Every pod on the same node must be able to reach every other pod using its IP address.
* Every pod on different nodes should communicate with each other seamlessly with no additional Network Address Translation (NAT), regardless of the underlying IP ranges.

<Frame>
  ![The image illustrates a networking model for Docker pods, emphasizing IP address assignment and inter-pod communication within and across nodes without NAT.](https://kodekloud.com/kk-media/image/upload/v1752880576/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Pod-Networking/frame_100.jpg)
</Frame>

As long as your solution automatically assigns IP addresses and provides seamless connectivity both within a node and across nodes, it satisfies Kubernetes’ requirements.

<Callout icon="lightbulb">
  Ensure your networking solution supports automatic IP assignment and connectivity without relying on manual NAT configuration.
</Callout>

## Building a Pod Network

Let’s design a basic pod network solution using core networking concepts such as routing, IP address management, namespaces, and the Container Network Interface (CNI).

Imagine a three-node cluster where all nodes, regardless of their role, participate equally in the network. The external network assigns IP addresses in the 192.168.1.x range (e.g., node 1 receives 192.168.1.11, node 2 receives 192.168.1.12, and node 3 receives 192.168.1.13). When containers are created, each one is provided with its dedicated network namespace. To enable communication among these namespaces, attach each to a local bridge network on every node.

Begin by creating a bridge network on each node and configuring it with a specific IP address. For example:

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

In this configuration, all nodes are treated equivalently since both management and workload pods rely on the same networking principles.

### Planning Pod Connectivity

Given that nodes have public IPs, assign each node’s bridge network its own private subnet. For example, you might allocate:

* Node 1: 10.244.1.0/24
* Node 2: 10.244.2.0/24
* Node 3: 10.244.3.0/24

Assign the corresponding IP addresses to each node’s bridge interface as follows:

```bash theme={null}
ip link add v-net-0 type bridge
