# Networking Deep Dive Docker

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Networking/Networking-Deep-Dive-Docker/page

This article explores Docker networking, including modes, network namespaces, and how to connect containers and expose services.

In this lesson, we explore Docker networking, covering built-in modes and Linux network namespaces. You’ll learn how Docker uses a bridge network, veth pairs, and iptables NAT to connect containers and expose services.

## Docker Networking Modes

Docker offers several network modes on a single host (e.g., host IP `192.168.1.10` on `eth0`):

| Mode   | Behavior                                           | Example                           |
| ------ | -------------------------------------------------- | --------------------------------- |
| none   | No network interfaces except loopback              | `docker run --network none nginx` |
| host   | Shares the host’s network stack directly           | `docker run --network host nginx` |
| bridge | Default: containers attach to the `docker0` bridge | `docker run nginx`                |

**none**\
The container only has a loopback interface and cannot send or receive external traffic.

**host**\
Containers share the host network namespace directly.

> **triangle-alert** Using `--network host` removes network isolation. Ports in the container map directly to the host and may conflict with other services.

**bridge**\
The default mode creates a `docker0` bridge with a `172.17.0.0/16` subnet. Containers receive an IP on this network.

List Docker networks and host interfaces:

```bash theme={null}
docker network ls
ip link show
```

You’ll see an interface named `docker0`:

```bash theme={null}
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST> mtu 1500 qdisc noqueue state DOWN 
    link/ether 02:42:88:56:50:83 brd ff:ff:ff:ff:ff:ff
```

Inspect its IP address:

```bash theme={null}
ip addr show docker0
```

## Docker and Network Namespaces

Each container runs in its own Linux network namespace. To view Docker namespaces on the host:

```bash theme={null}
sudo ip netns
