# Example output:
b3165c10a92b
```

Inspect a container’s sandbox and namespace path:

```bash theme={null}
docker inspect 942d70e585b2 \
  --format '{{json .NetworkSettings}}'
```

```json theme={null}
{
  "Bridge": "",
  "SandboxID": "b3165c10a92b50edc4c8aa5f37273e180907ded31",
  "SandboxKey": "/var/run/docker/netns/b3165c10a92b"
}
```

When a container starts, Docker creates a veth pair:

* One end attaches to the host bridge (`docker0`).
* The other end goes inside the container namespace as `eth0`.

Host side:

```bash theme={null}
ip link show
# Example:
8: vethbb1c343@i7f: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0
    link/ether 9e:71:37:83:9f:50 brd ff:ff:ff:ff:ff:ff link-netnsid 1
```

Container side:

```bash theme={null}
ip -n b3165c10a92b addr
# Example:
7: eth0@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue 
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff 
    inet 172.17.0.3/16 brd 172.17.255.255 scope global eth0
```

Each new container repeats this process, assigning a unique IP in `172.17.0.0/16`.

<Frame>
  ![The image is a network diagram illustrating a Docker bridge network setup, showing connections between containers and the bridge interface docker0.](https://kodekloud.com/kk-media/image/upload/v1752873892/notes-assets/images/Docker-Certified-Associate-Exam-Course-Networking-Deep-Dive-Docker/docker-bridge-network-diagram.jpg)
</Frame>

## Container-to-Container and Host Communication

Containers on the same bridge can communicate by IP. The host also reaches them directly:

```bash theme={null}
curl http://172.17.0.3:80
# => Welcome to nginx!
```

<Callout icon="lightbulb">
  External clients cannot access container IPs on the bridge network without port publishing.
</Callout>

## Publishing Ports (Port Mapping)

Expose container ports to external clients with `-p hostPort:containerPort`:

```bash theme={null}
docker run -p 8080:80 nginx
```

Access via `http://192.168.1.10:8080`:

```bash theme={null}
curl http://192.168.1.10:8080
# => Welcome to nginx!
```

### Behind the Scenes: iptables NAT

Docker adds iptables NAT rules to forward traffic:

```bash theme={null}
iptables -t nat -A DOCKER -p tcp --dport 8080 \
  -j DNAT --to-destination 172.17.0.3:80
```

This ensures incoming connections on host port 8080 are redirected to the container’s port 80.

## References

* [Docker Networking](https://docs.docker.com/network/)
* [Linux Network Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)
* [iptables Documentation](https://www.netfilter.org/projects/iptables/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/ddc7602c-93a8-4a6f-900c-a5cf6f7b0716/lesson/a5690211-ec30-4129-b573-3810a715f663" />
</CardGroup>


# Networking Deep Dive Namespaces

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Networking/Networking-Deep-Dive-Namespaces/page

This tutorial explores Linux network namespaces, focusing on container network isolation and commands for creating, managing, and connecting namespaces.

In this tutorial, we take a deep dive into Linux **network namespaces**—the building blocks of container network isolation (e.g., in [Docker](https://www.docker.com/)). Think of your host as a house and each network namespace as a private room: containers inside one room cannot see interfaces or processes in another. The host, however, has a global view of all “rooms.”

<Frame>
  ![The image depicts a house-like structure with four colored sections, each containing a silhouette of a person, and the word "NAMESPACE" at the top.](https://kodekloud.com/kk-media/image/upload/v1752873894/notes-assets/images/Docker-Certified-Associate-Exam-Course-Networking-Deep-Dive-Namespaces/house-structure-namespaces-silhouettes.jpg)
</Frame>

<Callout icon="lightbulb">
  Most of these commands require root privileges or `sudo`. Ensure you have the appropriate permissions before proceeding.
</Callout>

***

## 1. Process Isolation

Inside a container’s PID namespace, a process always appears as PID 1. From the host’s root namespace, the same process has a distinct PID among all host processes:

```bash theme={null}
