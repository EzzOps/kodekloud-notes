# Display the running kubelet process showing CNI options
ps -aux | grep kubelet

# List CNI plugin executables
ls /opt/cni/bin

# List CNI configuration files
ls /etc/cni/net.d
```

> **lightbulb** If multiple configuration files exist in the directory, kubelet selects the first file in alphabetical order. A common configuration file is `10-bridge.conf`.

## Example Bridge Configuration

Below is an example bridge configuration file (`10-bridge.conf`) that complies with the CNI standard:

```json theme={null}
{
  "cniVersion": "0.2.0",
  "name": "mynet",
  "type": "bridge",
  "bridge": "cni0",
  "isGateway": true,
  "ipMasq": true,
  "ipam": {
    "type": "host-local",
    "subnet": "10.22.0.0/16",
    "routes": [
      { "dst": "0.0.0.0/0" }
    ]
  }
}
```

To view its content, run:

```bash theme={null}
cat /etc/cni/net.d/10-bridge.conf
```

This configuration file includes several key components:

* The `"bridge"` parameter specifies the name of the bridge interface (in this case, `cni0`).
* The `"isGateway"` option determines whether the bridge network should have an IP address to function as a gateway.
* The `"ipMasq"` option configures IP masquerading (NAT rules) for outgoing traffic.
* The `"ipam"` section sets up IP Address Management. Here, `"host-local"` management is used where the `"subnet"` field defines the IP range for the pods (e.g., `10.22.0.0/16`), and the `"routes"` array sets the default routing.

> **triangle-alert** Be cautious when modifying the IPAM settings, as incorrect configuration can lead to network conflicts or unreachable pods.

Alternatively, you can switch the IPAM type to `"dhcp"` if you prefer to use an external DHCP server for IP address allocation.

That concludes our lesson on how Kubernetes integrates with CNI to manage container networking. For more detailed information, consider exploring [Kubernetes Documentation](https://kubernetes.io/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/35623c9b-b30e-4a5d-a868-cc9f30de96d2/lesson/45ea49fa-d481-43f1-bf04-868de47af9e8)


# Cluster Networking

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Container-Orchestration-Networking/Cluster-Networking/page

This article provides a guide on configuring networking for master and worker nodes in a Kubernetes cluster, detailing network settings and port configurations.

Welcome to this comprehensive guide on configuring networking for both master and worker nodes within a Kubernetes cluster. In this article, we detail the necessary network settings and port configurations required for optimal cluster communication and performance.

## Node Configuration

In a Kubernetes cluster, each node must have at least one network interface that is configured with:

* A unique IP address.
* A unique hostname.
* A distinct MAC address.

It is particularly important to ensure these settings are correctly applied if virtual machines (VMs) have been cloned from existing ones.

## Essential Port Configurations

Proper communication between Kubernetes components relies on opening specific network ports. Below is a list of the critical ports that must be accessible:

* **Port 6443:**\
  The Kubernetes API server, running on the master node, listens on this port. It must be open for:
  * Worker nodes.
  * The `kubectl` command-line tool.
  * External users.
  * Other control plane components.

* **Port 10250:**\
  The kubelet service runs on both the master and worker nodes and listens on this port for managing node-level operations.

* **Port 10259:**\
  The kube-scheduler service uses this port to operate smoothly.

* **Port 10257:**\
  The kube-controller-manager service requires this open port for its functions.

* **Ports 30000 to 32767:**\
  These ports are used by worker nodes to expose services to external users.

* **Port 2379:**\
  The etcd server, which handles key-value storage for the cluster, listens on this port.\
  If you are running multiple master nodes, ensure that **port 2380** is also open to facilitate communication between etcd clients.

> **lightbulb** For a full list of required ports, please refer to the [official Kubernetes documentation](https://kubernetes.io/docs/).

## Network Security Considerations

When setting up your Kubernetes cluster, make sure that the following elements are included in your network security configuration:

* **Firewall Settings:** Ensure that appropriate ports are allowed.
* **iptables Rules:** Confirm that the necessary rules enable smooth communication between components.
* **Cloud Network Security Groups:** For clusters hosted on cloud platforms such as GCP, Azure, or AWS, verify that relevant security groups permit the required ports.

If any component exhibits communication issues, a primary troubleshooting step should be to review and adjust your port configuration settings.

By adhering to these guidelines, you can establish a secure and well-functioning networking environment within your Kubernetes cluster.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/35623c9b-b30e-4a5d-a868-cc9f30de96d2/lesson/e3e489b3-9441-4d74-8398-ea7454d42894)
