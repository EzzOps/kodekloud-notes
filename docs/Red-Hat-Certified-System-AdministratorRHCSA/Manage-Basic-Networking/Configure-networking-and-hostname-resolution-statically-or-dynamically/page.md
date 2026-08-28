# Configure networking and hostname resolution statically or dynamically

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Basic-Networking/Configure-networking-and-hostname-resolution-statically-or-dynamically/page

This guide covers configuring networking and hostname resolution in Linux, including static and dynamic methods for IP addresses, gateways, and DNS settings.

Welcome to this comprehensive guide on configuring networking and hostname resolution in Linux—both statically and dynamically. Every device connected to a network requires an IP address (e.g., 192.168.0.5 or 10.0.0.9). In addition, internet connectivity demands proper gateway and DNS resolver settings. For instance, when accessing google.com, the typical process is:

1. The device queries a DNS resolver to obtain google.com's IP address (e.g., 203.0.113.9).
2. With the resolved IP, the device sends data to its gateway.
3. The gateway forwards the data hop-by-hop until it reaches the destination.

These settings—IP addresses, gateways, DNS resolvers, network routes, and so forth—can be configured dynamically (typically using DHCP) or statically (via manual configuration).

<Callout icon="lightbulb">
  On Red Hat-based systems (such as Red Hat Enterprise Linux or CentOS), the configuration files and tools may vary slightly compared to other Linux distributions.
</Callout>

***

## Identifying Your Network Interface

Before modifying any settings, it is important to identify the correct network interface. Start by listing all network interfaces with the following command:

```bash theme={null}
ip link show
```

A sample output might look like this:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
    group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT
    group default qlen 1000
    link/ether 08:00:27:6b:d7:87 brd ff:ff:ff:ff:ff:ff
3: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    group default qlen 1000
    link/ether 52:54:00:9c:e8:04 brd ff:ff:ff:ff:ff:ff
[aaron@LFCS-CentOS ~]$
```

In this example, the first non-loopback interface is **enp0s3**. To see the IP addresses assigned to these interfaces, you can run:

```bash theme={null}
ip address show
```

Alternatively, use the abbreviated command:

```bash theme={null}
ip a
```

The loopback adapter typically has the IP address 127.0.0.1 (localhost), while the physical adapter (enp0s3) might have an IP like 192.168.1.79/24. Note that the CIDR notation ("/24") designates the network prefix length, meaning 24 bits are fixed and only the remaining 8 bits are available for device addressing. For example, with a /16 configuration, the first 16 bits are fixed (e.g., 192.168), and the last two octets can vary.

A detailed sample output from `ip address show` is:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noop state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:6b:d7:87 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.79/24 brd 192.168.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2449sec preferred_lft 2449sec
    inet6 fe80::a00:27ff:fe6b:d787/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 52:54:00:9c:e8:04 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
       valid_lft forever preferred_lft forever
[aaron@LFCS-CentOS ~]$
```

Note that physical network interfaces typically start with "e" (e.g., enp0s3) and wireless interfaces generally start with "w".

***

## Understanding IPv6 Addresses

The output above also displays IPv6 addresses. For example, the IPv6 address on enp0s3 appears as:

```bash theme={null}
inet6 fe80::a00:27ff:fe6b:d787/64 scope link noprefixroute
```

IPv6 addresses are 128 bits long. The "/64" indicates that the first 64 bits are reserved as the network prefix, leaving the remaining bits for the device's interface identifier.

***

## Viewing the Routing Table

The routing table dictates how network traffic is directed. To review the system’s routing table, use:

```bash theme={null}
ip route show
```

Or the shorter version:

```bash theme={null}
ip r
```

A typical routing table output might be:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ ip r
default via 192.168.1.1 dev enp0s3 proto dhcp metric 100
192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.79 metric 100
192.168.122.0/24 dev virbr0 proto kernel scope link src 192.168.122.1 linkdown
[aaron@LFCS-CentOS ~]$
```

This output confirms that the default gateway is 192.168.1.1. To check the DNS resolver settings, display the contents of the `/etc/resolv.conf` file:

```bash theme={null}
cat /etc/resolv.conf
```

A sample output might be:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ cat /etc/resolv.conf
