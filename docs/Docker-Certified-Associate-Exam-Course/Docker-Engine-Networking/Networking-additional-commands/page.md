# Inside the container (PID namespace)
ps aux
# ...
root     1   0.0  0.0   4528   828 ?   Ss   03:06  0:00 nginx

# On the host
ps aux
# ...
root   3816  1.0  0.0   4528   828 ?   Ss   06:06  0:00 nginx
```

***

## 2. Creating Network Namespaces

By default, the host’s network stack is isolated to its own namespace. To spin up isolated network domains:

```bash theme={null}
# Create two namespaces
ip netns add red
ip netns add blue

# Verify namespaces
ip netns list
# red
# blue
```

| Command                    | Description                       |
| -------------------------- | --------------------------------- |
| `ip netns add NAME`        | Create a network namespace        |
| `ip netns delete NAME`     | Remove a namespace                |
| `ip netns list`            | List existing namespaces          |
| `ip netns exec NAME <cmd>` | Run `<cmd>` inside namespace NAME |

***

## 3. Inspecting Interfaces Inside a Namespace

On the host, you’ll see all physical and virtual interfaces:

```bash theme={null}
ip link show
# 1: lo: <LOOPBACK,UP,LOWER_UP> ...
# 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
```

Within **red**, only the loopback interface exists:

```bash theme={null}
# Method 1: ip netns exec
ip netns exec red ip link show

# Method 2: shorthand
ip -n red link show

# Output:
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 ...
```

No host interfaces (like `eth0`) appear in **red**. ARP and routing tables start empty:

```bash theme={null}
ip netns exec red arp           # no entries
ip netns exec red ip route      # default only loopback
```

***

## 4. Connecting Two Namespaces with veth Pairs

To create a virtual “cable” between **red** and **blue**, use a veth pair:

```bash theme={null}
# Create veth pair
ip link add veth-red type veth peer name veth-blue

# Move each end into its namespace
ip link set veth-red  netns red
ip link set veth-blue netns blue

# Assign IPs and bring up interfaces
ip -n red  addr add 192.168.15.1/24 dev veth-red
ip -n red  link set veth-red up

ip -n blue addr add 192.168.15.2/24 dev veth-blue
ip -n blue link set veth-blue up
```

Test connectivity:

```bash theme={null}
ip -n red ping -c1 192.168.15.2
# 64 bytes from 192.168.15.2: icmp_seq=1 ttl=64 time=0.xxx ms
```

ARP tables populate automatically:

```bash theme={null}
ip -n red  arp
ip -n blue arp
# 192.168.15.1 ether 7a:9d:9b:c8:3b:7f C veth-blue
```

***

## 5. Building a Virtual Switch with a Bridge

Connecting many namespaces via direct veth pairs is impractical. Instead, create a Linux bridge on the host:

```bash theme={null}
# Create and enable bridge
ip link add v-net-0 type bridge
ip link set v-net-0 up
```

Remove the direct link in **red**:

```bash theme={null}
ip -n red link del veth-red
```

Recreate veth pairs for each namespace and attach them to the bridge:

```bash theme={null}
# red ↔ bridge
ip link add veth-red     type veth peer name veth-red-br
ip link set veth-red netns red
ip link set veth-red-br master v-net-0

# blue ↔ bridge
ip link add veth-blue    type veth peer name veth-blue-br
ip link set veth-blue netns blue
ip link set veth-blue-br master v-net-0
```

Assign IPs and bring them up:

```bash theme={null}
ip -n red  addr add 192.168.15.1/24 dev veth-red
ip -n red  link set veth-red up

ip -n blue addr add 192.168.15.2/24 dev veth-blue
ip -n blue link set veth-blue up
```

All namespaces on **v-net-0** can now communicate via the bridge.

***

## 6. Host–Namespace Connectivity

To let the host join this virtual network, assign **v-net-0** an IP in the same subnet:

```bash theme={null}
ip addr add 192.168.15.5/24 dev v-net-0
```

Now the host can ping into any namespace:

```bash theme={null}
ping -c1 192.168.15.1
# 64 bytes from 192.168.15.1: icmp_seq=1 ttl=64 time=0.xxx ms
```

***

## 7. Namespace → LAN Connectivity via Host

By default, namespaces cannot reach external LANs:

```bash theme={null}
ip -n blue ping 192.168.1.3
# Connect: Network is unreachable
```

Check **blue**’s routes:

```bash theme={null}
ip -n blue ip route
# 192.168.15.0/24 dev veth-blue proto kernel scope link
```

Add a route via the host (gateway `192.168.15.5`):

```bash theme={null}
ip -n blue ip route add 192.168.1.0/24 via 192.168.15.5
```

### Enabling NAT on the Host

<Callout icon="triangle-alert">
  Be careful when modifying `iptables` rules on production systems. Always test in a safe environment first.
</Callout>

```bash theme={null}
# Masquerade outbound traffic from your virtual subnet
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -j MASQUERADE

# Set default route in the namespace
ip -n blue ip route add default via 192.168.15.5
```

Now **blue** can reach the internet (e.g., `8.8.8.8`):

```bash theme={null}
ip -n blue ping -c1 8.8.8.8
# 64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=XX ms
```

***

## 8. Port Forwarding into a Namespace

To expose a service (e.g., HTTP on port 80) running in **blue**, use `iptables` DNAT on the host:

```bash theme={null}
iptables -t nat -A PREROUTING --dport 80 \
  -j DNAT --to-destination 192.168.15.2:80
```

Now requests to the host’s port 80 are transparently forwarded into **blue**.

***

## 9. Summary of Key Commands

| Task                       | Command Example                                                               |
| -------------------------- | ----------------------------------------------------------------------------- |
| Create namespace           | `ip netns add NAME`                                                           |
| Execute in namespace       | `ip netns exec NAME <cmd>`                                                    |
| Create veth pair           | `ip link add veth-A type veth peer name veth-B`                               |
| Create bridge              | `ip link add BRIDGE type bridge`                                              |
| Attach interface to bridge | `ip link set IFACE master BRIDGE`                                             |
| Assign IP                  | `ip -n NS addr add IP/MASK dev IFACE`                                         |
| Enable masquerading (NAT)  | `iptables -t nat -A POSTROUTING -s SUBNET -j MASQUERADE`                      |
| DNAT for port forwarding   | `iptables -t nat -A PREROUTING --dport PORT -j DNAT --to-destination IP:PORT` |

***

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [iproute2 Manual](https://man7.org/linux/man-pages/man8/ip.8.html)
* [Linux Bridge Wiki](https://wiki.linuxfoundation.org/networking/bridge)
* [Docker Networking](https://docs.docker.com/network/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/ddc7602c-93a8-4a6f-900c-a5cf6f7b0716/lesson/e5ec223b-0e3c-4a86-8fe4-ba20e8dd2d61" />
</CardGroup>


# Networking additional commands

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Networking/Networking-additional-commands/page

Manage Docker networks with commands to list, inspect, connect, disconnect, and remove networks for a cleaner environment.

Manage Docker networks beyond the basics. In this guide, you’ll learn how to list default networks, inspect their settings, connect or disconnect containers, and remove unused networks to keep your Docker environment clean.

## Table of Contents

* [Listing Default Networks](#listing-default-networks)
* [Inspecting a Network](#inspecting-a-network)
* [Connecting and Disconnecting Containers](#connecting-and-disconnecting-containers)
* [Removing Networks](#removing-networks)

***

## Listing Default Networks

Docker provides three built-in networks out of the box: `bridge`, `host`, and `none`. Use the following command to see them:

```bash theme={null}
docker network ls
```

Example output:

```text theme={null}
NETWORK ID          NAME      DRIVER    SCOPE
599dcaf4e856        bridge    bridge    local
c817f1bca596        host      host      local
e6508d3404a3        none      null      local
```

You can also get a quick overview in tabular form:

| Network Name | Driver | Scope | Description                                   |
| ------------ | ------ | ----- | --------------------------------------------- |
| bridge       | bridge | local | Default network for standalone containers     |
| host         | host   | local | Containers share the host’s network namespace |
| none         | null   | local | Containers have no network interfaces         |

<Callout icon="lightbulb">
  The **bridge** network uses the `172.17.0.0/16` subnet by default, with gateway `172.17.0.1` assigned to the `docker0` interface on the host.
</Callout>

***

## Inspecting a Network

To dive deeper into a network’s configuration—such as its IPAM settings, subnets, gateways, and attached containers—run:

```bash theme={null}
docker network inspect bridge
```

Sample output (abridged):

```json theme={null}
[
  {
    "Name": "bridge",
    "Id": "[SECRET_REDACTED]",
    "Scope": "local",
    "Driver": "bridge",
    "IPAM": {
      "Driver": "default",
      "Config": [
        {
          "Subnet": "172.17.0.0/16",
          "Gateway": "172.17.0.1"
        }
      ]
    },
    "Containers": {
      // attached container details
    }
  }
]
```

This output shows the network’s driver, IPAM configuration, and any containers currently connected.

***

## Connecting and Disconnecting Containers

You can attach a running container to additional networks or remove it from one without restarting:

```bash theme={null}
