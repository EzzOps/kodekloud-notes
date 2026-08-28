# ping: second: Name or service not known
```

## Creating a User-Defined Bridge Network

User-defined bridge networks include built-in DNS and automatic name resolution. Create one with a custom subnet:

```bash theme={null}
docker network create \
  --driver bridge \
  --subnet 192.168.10.0/24 \
  kodekloudnet
```

Verify its presence:

```bash theme={null}
docker network ls
```

```bash theme={null}
$ docker network ls
NETWORK ID     NAME           DRIVER    SCOPE
cf10938f5edf   bridge         bridge    local
d4f46412e7e9   host           host      local
f22c791ef1ad   kodekloudnet   bridge    local
b5b0ab8c1665   none           null      local
```

## Running Containers on the Custom Network

Launch two containers on `kodekloudnet`:

```bash theme={null}
docker run -itd --name customfirst --net kodekloudnet centos:7
docker run -itd --name customsecond --net kodekloudnet centos:7
```

They now receive IPs within `192.168.10.0/24`, and DNS-based name resolution works:

```bash theme={null}
docker exec customfirst ping -c 4 customsecond
```

```bash theme={null}
PING customsecond (192.168.10.3): 56 data bytes
64 bytes from customsecond.kodekloudnet (192.168.10.3): icmp_seq=1 ttl=64 time=0.07 ms
...
```

## Connecting an Existing Container to a Network

By default, containers attach only to the default bridge. To connect `first` to `kodekloudnet`:

```bash theme={null}
docker network connect kodekloudnet first
```

Verify both network endpoints:

```bash theme={null}
docker inspect first \
  --format '{{json .NetworkSettings.Networks}}' | jq
```

```json theme={null}
{
  "bridge": {
    "IPAddress": "172.17.0.2"
  },
  "kodekloudnet": {
    "IPAddress": "192.168.10.4"
  }
}
```

Now ping `first` from `customfirst`:

```bash theme={null}
docker exec customfirst ping -c 2 first
```

## Disconnecting a Container from a Network

To detach a container:

```bash theme={null}
docker network disconnect kodekloudnet first
```

After disconnecting, `customfirst` will no longer reach `first` on that network.

## Removing Networks

Docker prevents removing networks with active endpoints. To delete `kodekloudnet`:

1. Stop and remove containers:
   ```bash theme={null}
   docker container stop $(docker ps -q)
   docker container rm $(docker ps -aq)
   ```
2. Remove the network:
   ```bash theme={null}
   docker network rm kodekloudnet
   ```

You can also prune all unused user-defined networks:

```bash theme={null}
docker network prune
```

<Callout icon="triangle-alert">
  `docker network prune` removes only user-defined networks without active containers. Default networks (`bridge`, `host`, `none`) are not affected.
</Callout>

***

## Links and References

* [Docker Networking Overview](https://docs.docker.com/network/)
* [Docker Network Commands](https://docs.docker.[AWS_SECRET_ACCESS_KEY]/)
* [Kubernetes Networking](https://kubernetes.io/docs/concepts/services-networking/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/ddc7602c-93a8-4a6f-900c-a5cf6f7b0716/lesson/312fe0b8-2fc3-4610-b5cd-354b89a4f521" />
</CardGroup>


# Docker Networking

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Networking/Docker-Networking/page

This guide covers Dockers networking features, including built-in networks, user-defined bridges, and container communication methods.

Docker simplifies container networking by providing built-in networks and easy-to-use commands for creating custom networks. Whether you need isolated environments or seamless inter-container communication, this guide covers everything from default networks to user-defined bridges, inspection commands, and internal mechanics.

## Built-in Docker Networks

Docker creates three networks upon installation:

| Network Name | Description                                  | Typical Use Case                         |
| ------------ | -------------------------------------------- | ---------------------------------------- |
| bridge       | Default private internal network on the host | General container communication          |
| host         | Shares host’s network namespace—no isolation | High-performance networking, host apps   |
| none         | No network interfaces except loopback        | Security-isolated or self-managed setups |

You can attach containers to any network using the `--network` flag:

```bash theme={null}
docker run --network=<network_name> ubuntu
```

***

## 1. Bridge Network

The **bridge** network is Docker’s default. Each container on this network gets an internal IP (typically in `172.17.x.x`). Containers on the same bridge can communicate directly.

### Port Mapping

Expose container ports to the host with `-p`:

```bash theme={null}
docker run -d -p 8080:80 nginx
```

This maps port **80** in the container to port **8080** on your Docker host.

<Callout icon="lightbulb">
  If you omit `-d`, the container runs in the foreground.
</Callout>

***

## 2. Host Network

Running with `--network=host` makes the container share your host’s network stack:

```bash theme={null}
docker run --network=host ubuntu
```

Key points:

* No port mapping needed
* Ports in the container are the same as on the host
* Cannot run multiple containers on the same host port

<Callout icon="triangle-alert">
  Using the host network removes isolation. Only use this when you trust the container’s network behavior.
</Callout>

***

## 3. None Network

The **none** network disables all external interfaces, leaving only the loopback:

```bash theme={null}
docker run --network=none ubuntu
```

Use this for maximum network isolation when <em>no</em> connectivity is desired.

***

## Creating a User-Defined Bridge Network

Custom bridge networks let you isolate groups of containers and define subnets:

```bash theme={null}
docker network create \
  --driver bridge \
  --subnet 182.18.0.0/16 \
  custom-isolated-network
```

List all available networks:

```bash theme={null}
docker network ls
```

Example output:

```plain theme={null}
NETWORK ID          NAME                         DRIVER    SCOPE
dba0fb9370fe        bridge                       bridge    local
4d60768bc9          custom-isolated-network      bridge    local
6de6865ce1c6        docker_gwbridge              bridge    local
e29d81be47          host                         host      local
mmrho7vb9rm         ingress                      overlay   swarm
d371b4009142        simplewebappdocker_default   bridge    local
```

<Frame>
  ![The image illustrates a user-defined network setup with Docker containers, showing IP addresses and connections between them.](https://kodekloud.com/kk-media/image/upload/v1752873891/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Networking/docker-user-defined-network-setup.jpg)
</Frame>

***

## Inspecting a Container’s Network Settings

To retrieve a container’s IP address and network details:

```bash theme={null}
docker inspect <container_id_or_name>
```

Search for the `NetworkSettings` section in the JSON output:

```json theme={null}
"NetworkSettings": {
  "Gateway": "172.17.0.1",
  "IPAddress": "172.17.0.6",
  "MacAddress": "02:42:ac:11:00:06",
  "Networks": {
    "bridge": {
      "Gateway": "172.17.0.1",
      "IPAddress": "172.17.0.6",
      "MacAddress": "02:42:ac:11:00:06"
    }
  }
}
```

<Callout icon="lightbulb">
  Use `jq` to filter output:

  ```bash theme={null}
  docker inspect <id> | jq '.[0].NetworkSettings'
  ```
</Callout>

***

## Name-Based Container Communication

Docker’s embedded DNS (at `127.0.0.11`) lets containers resolve each other by name:

```plaintext theme={null}
mysql.connect(mysql)
```

Here, `mysql` refers to the target container’s name. No static IPs required.

***

## Under the Hood: Namespaces & veth Pairs

Docker uses Linux **network namespaces** to isolate containers. Communication between a container and the host bridge relies on **veth** (virtual Ethernet) pairs:

* One end lives in the container’s namespace
* The other end attaches to the host bridge

This setup ensures both isolation and connectivity.

***

## Links and References

* [Docker Networking Overview](https://docs.docker.com/network/)
* [docker network create](https://docs.docker.com/engine/reference/commandline/network_create/)
* [Linux Network Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/ddc7602c-93a8-4a6f-900c-a5cf6f7b0716/lesson/f81b533f-0848-43d3-a6b4-93069bab2cd9" />
</CardGroup>
