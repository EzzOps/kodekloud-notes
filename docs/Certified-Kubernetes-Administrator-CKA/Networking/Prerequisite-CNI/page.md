# Create veth pair
ip link add <veth-in-host> type veth peer name <veth-in-namespace>
# Attach one end to the container’s namespace
ip link set <veth-in-namespace> netns <namespace>
# Attach the other end to the bridge
ip link set <veth-in-host> master <bridge>
# Assign IP address to the container’s interface
ip -n <namespace> addr add <IP-address>/24 dev <veth-in-namespace>
# Add default route in the container’s namespace
ip -n <namespace> route add default via <bridge-IP>
# Bring up the container’s interface
ip -n <namespace> link set <veth-in-namespace> up
```

Executing this script on each node ensures that all containers receive an IP address and are connected to their respective internal networks.

### Cross-Node Communication

One of the challenges is enabling communication between pods on different nodes. For example, if a pod with IP 10.244.1.2 on node 1 attempts to ping a pod with IP 10.244.2.2 on node 2, the ping may initially fail due to unknown routes between subnets:

```bash theme={null}
bluepod$ ping 10.244.2.2
Connect: Network is unreachable
```

To resolve this, add a route on node 1 that directs traffic for 10.244.2.2 via node 2’s external IP (e.g., 192.168.1.12):

```bash theme={null}
node1$ ip route add 10.244.2.2 via 192.168.1.12
```

After configuring the routing, the ping command should succeed:

```bash theme={null}
bluepod$ ping 10.244.2.2
64 bytes from 10.244.2.2: icmp_seq=1 ttl=63 time=0.587 ms
64 bytes from 10.244.2.2: icmp_seq=2 ttl=63 time=0.466 ms
```

Similarly, add these routes on all nodes to cover all pod subnets:

```bash theme={null}
node1$ ip route add 10.244.2.2 via 192.168.1.12
node1$ ip route add 10.244.3.2 via 192.168.1.13
node2$ ip route add 10.244.1.2 via 192.168.1.11
node2$ ip route add 10.244.3.2 via 192.168.1.13
node3$ ip route add 10.244.1.2 via 192.168.1.11
node3$ ip route add 10.244.2.2 via 192.168.1.12
```

<Callout icon="triangle-alert">
  Manually configuring routes on every host is impractical for large-scale deployments. A more scalable solution involves configuring a centralized router to manage all subnet routes and setting each node's default gateway to this router.
</Callout>

Below is an image that illustrates a Docker network setup with three nodes, each with distinct IP addresses and subnet configurations, connected via a virtual network bridge:

<Frame>
  ![The image illustrates a Docker network setup with three nodes, each having distinct IP addresses and subnet configurations, connected via a virtual network bridge.](https://kodekloud.com/kk-media/image/upload/v1752869856/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Pod-Networking/frame_420.jpg)
</Frame>

## Integrating Container Network Interface (CNI)

In our lab setup, we executed scripts manually to configure pod networking. However, in a production Kubernetes environment where thousands of pods may be created per minute, this manual approach is not feasible.

This is where the Container Network Interface (CNI) becomes essential. CNI specifies how Kubernetes should invoke a networking script each time a pod is created. To conform with CNI standards, the networking script must have:

* An "add" section to connect the container to the network.
* A "delete" section to disconnect the container, remove interfaces, and free up the IP address.

When the container runtime launches a container, it uses the CNI configuration (provided as a command-line argument) to execute the relevant script with the command "add" and pass the container’s name and namespace identifier.

Below is an example snippet that illustrates the CNI execution process:

```bash theme={null}
ip -n <namespace> link set <interface> up
ip link del <interface>
./net-script.sh add <container> <namespace>
```

## Conclusion

In this article, we covered the essential concepts behind pod networking in Kubernetes—from manual network namespace and bridge configuration to the role of CNI in automating network interface management. The techniques discussed here lay a solid foundation for understanding and troubleshooting pod networking in a Kubernetes cluster.

Stay tuned for upcoming articles where we integrate detailed CNI configurations into Kubernetes workflows and provide practical tests to reinforce your learning.

For more insight into Kubernetes networking, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/44bc9a9f-319c-40ee-babd-0f7b53a70de7/lesson/66d09e22-eaf7-4613-8515-cda836b961bd" />
</CardGroup>


# Prerequisite CNI

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Networking/Prerequisite-CNI/page

This article provides a comprehensive guide on the Container Networking Interface (CNI) and its role in simplifying container networking configuration and management.

Welcome to this comprehensive guide on the Container Networking Interface (CNI) and its vital role in container networking. In this lesson, we explore how network namespaces and standardized networking plugins simplify the configuration and management of container networks.

Network namespaces create isolated network environments on a single host. These namespaces are interconnected by a bridge network that establishes virtual interfaces (or virtual cables) for communication between namespaces. This involves assigning IP addresses, activating interfaces, and enabling NAT or IP masquerading for external connectivity. Although Docker configures its bridge networking using similar methods, it employs its own naming conventions. Other container platforms like Rocket, Mesos Containerizer, and Kubernetes address these networking challenges in a comparable way.

<Frame>
  ![The image shows a comparison of network namespace setup steps for Docker, rkt, Mesos, and Kubernetes, each with eight similar configuration steps.](https://kodekloud.com/kk-media/image/upload/v1752869857/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Prerequisite-CNI/frame_70.jpg)
</Frame>

To standardize this process and avoid duplicating efforts across multiple platforms, a dedicated program known as "bridge" was developed. This program automates the tasks required to connect a container to a bridge network. For instance, you can run the program with the container ID and network namespace as shown below:

```bash theme={null}
bridge add 2e34dcf34 /var/run/netns/2e34dcf34
```

The "bridge" program handles low-level networking configuration, freeing container runtime environments from such complexities. When container platforms like Rocket or Kubernetes spin up a new container, they invoke this bridge program—passing the container ID and namespace—to automatically set up the network.

<Callout icon="lightbulb">
  By offloading network configuration tasks to a standardized bridge program, container runtimes can focus on higher-level operations while ensuring consistent and reliable network setups via CNI-compliant plugins.
</Callout>

This brings us to an important question: if you want to develop a similar program for a different networking scenario, which commands and arguments should it support? How do you ensure compatibility with container runtimes like Kubernetes or Rocket? The solution lies in establishing a set of standards—this is where the Container Networking Interface (CNI) comes into play.

CNI defines a standard for creating and integrating network plugins with container runtime environments. These plugins are responsible for:

* Creating a network namespace for each container.
* Identifying the networks to which the container should connect.
* Configuring the network when a container is created (using the "add" command) and cleaning up when it is deleted (using the "del" command).
* Setting up necessary network details via a JSON configuration file.

On the plugin side, CNI requires support for three command-line arguments: "add", "del", and "check". These commands must accept parameters such as the container ID and network namespace. The plugin then takes over to manage IP addresses and necessary routing, ensuring that containers can communicate effectively. The output of these operations must follow a strict format for consistency.

<Frame>
  ![The image outlines the Container Network Interface (CNI) requirements and processes, including network namespace creation, plugin invocation, and IP management, with logos of rkt, Mesos, and Kubernetes.](https://kodekloud.com/kk-media/image/upload/v1752869858/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Prerequisite-CNI/frame_240.jpg)
</Frame>

When both container runtimes and network plugins adhere to CNI standards, seamless interoperability is achieved. Any CNI-compliant plugin can work with any container runtime that supports these standards. The ecosystem already includes several CNI plugins such as bridge, VLAN, IP VLAN, MAC VLAN, and even one designed for Windows. IP address management (IPAM) plugins like host-local and DHCP are also available, along with third-party solutions like Weave, Flannel, Cilium, VMware NSX, Calico, and Infoblox.

<Callout icon="triangle-alert">
  Docker uses its own networking standard known as the Container Network Model (CNM), which differs from CNI. To use CNI with Docker, you must create a container without network configuration (using the “none” option) and then manually invoke the CNI plugin to set up networking.
</Callout>

Consider the following example that demonstrates how Kubernetes handles networking with Docker:

```bash theme={null}
docker run --network=none nginx
bridge add 2e34dcf34 /var/run/netns/2e34dcf34
```

In this workflow, Kubernetes first creates a Docker container without any network configuration and then calls the CNI plugin to establish the network. This process highlights how Kubernetes efficiently leverages CNI standards to manage container networks.

For further information, explore these resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

Dive deeper into container networking and harness the power of CNI standards in your deployments. Happy networking!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/44bc9a9f-319c-40ee-babd-0f7b53a70de7/lesson/f7be59d4-427d-4dc0-bf3c-57ff689c6520" />
</CardGroup>
