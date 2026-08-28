# Docker Overlay Network

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Docker-Overlay-Network/page

Docker overlay networks enable seamless communication between containers across multiple hosts, covering network drivers, Swarm networks, and custom overlay creation.

Docker overlay networks provide a single, seamless virtual network across multiple Docker nodes, enabling containers on different hosts to communicate securely. This guide covers Docker’s built-in network drivers, the purpose of overlays, Swarm’s default networks, and how to create custom overlay networks.

## Revisiting Docker’s Built-In Networks

Below is a quick reference for Docker’s default network drivers:

| Driver | Use Case                             | Example Command                        |
| ------ | ------------------------------------ | -------------------------------------- |
| bridge | Container isolation on a single host | `docker run -p 8080:80 my-web-app`     |
| host   | Shares host network namespace        | `docker run --network=host my-web-app` |
| none   | No networking (full isolation)       | `docker run --network=none ubuntu`     |

### bridge

Docker’s default network driver. It creates a private bridge (usually `172.17.x.x`) on the host and connects containers to it:

```bash theme={null}
docker run -d --name web \
  -p 8080:80 \
  nginx
```

### host

Containers share the host’s network namespace—ports inside the container map directly to the host without `-p`:

```bash theme={null}
docker run -d --network=host \
  --name api-server \
  my-api-image
```

### none

Disables all networking for full isolation. Use this when you don’t need external access:

```bash theme={null}
docker run --network=none \
  --name isolated-container \
  ubuntu
```

## Why Overlay Networks?

Each Docker host has its own bridge, so containers on different machines can’t talk by default. Overlay networks use VXLAN to create a virtual layer 2 network across hosts, making them essential for:

* Multi-host container communication
* Docker Swarm service discovery
* Secure, encrypted traffic between containers

## Ingress Network in Docker Swarm

When you run `docker swarm init`, Swarm creates an **ingress** overlay network with a built-in load balancer and routing mesh:

```bash theme={null}
docker network ls
NETWORK ID     NAME        DRIVER    SCOPE
68abeefb1f2e   bridge      bridge    local
5bab4adc7d02   host        host      local
e43bd489dd57   none        null      local
mevcdh5b40zz   ingress     overlay   swarm
```

### Single Node Service Publishing

Without Swarm, you’d expose a container port like this:

```bash theme={null}
docker run -p 80:5000 my-web-server
```

With Swarm and two replicas, use `--publish`:

```bash theme={null}
docker service create \
  --replicas 2 \
  --publish 80:5000 \
  my-web-server
```

Ingress’s load balancer listens on port 80 and routes traffic to port 5000 on both replicas.

### Multi-Node Routing Mesh

In a multi-node Swarm, every node advertises the published port (80). Incoming requests on any node are automatically forwarded to an active replica, regardless of where it’s running.

<Frame>
  ![The image illustrates an ingress network setup for a Docker Swarm, showing load balancers, a routing mesh, and web containers distributed across multiple Docker hosts.](https://kodekloud.com/kk-media/image/upload/v1752873924/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Overlay-Network/docker-swarm-ingress-network-setup.jpg)
</Frame>

## Default Swarm Networks

Swarm init creates two essential networks:

| Name             | Driver  | Purpose                                                        |
| ---------------- | ------- | -------------------------------------------------------------- |
| ingress          | overlay | Publishes service ports cluster-wide via routing mesh          |
| docker\_gwbridge | bridge  | Connects each node’s Docker daemon to the Swarm’s gateway port |

```bash theme={null}
docker network ls
NETWORK ID     NAME             DRIVER    SCOPE
68abeefb1f2e   bridge           bridge    local
5bab4adc7d02   host             host      local
e43bd489dd57   none             null      local
mevcdh5b40zz   ingress          overlay   swarm
c8fb2c361202   docker_gwbridge  bridge    local
```

<Frame>
  ![The image illustrates a diagram of Docker's default networks, showing web containers connected through an ingress network and a bridge network across multiple Docker hosts in a Docker Swarm setup.](https://kodekloud.com/kk-media/image/upload/v1752873925/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Overlay-Network/docker-swarm-default-networks-diagram.jpg)
</Frame>

## Creating Custom Overlay Networks

Create your own overlay network for services or standalone containers:

```bash theme={null}
docker network create \
  --driver overlay \
  my-overlay-network
```

* `--attachable`: Allows standalone containers to join the overlay.
* `--opt encrypted`: Enables AES-encrypted VXLAN for secure application traffic.

Remove an overlay network or prune unused ones:

```bash theme={null}
docker network rm my-overlay-network
docker network prune
```

<Callout icon="triangle-alert">
  Ensure all Swarm nodes can communicate on the required ports (2377, 7946, 4789) to avoid network disruptions.
</Callout>

### Required Swarm Ports

<Frame>
  ![The image shows a table listing network ports and their descriptions, including TCP 2377 for cluster management communications, TCP and UDP 7946 for communication among nodes and network discovery, and UDP 4789 for overlay network traffic.](https://kodekloud.com/kk-media/image/upload/v1752873926/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Overlay-Network/network-ports-descriptions-table.jpg)
</Frame>

## Port Publishing Formats

| Syntax                                            | Description            |
| ------------------------------------------------- | ---------------------- |
| `-p 80:5000`                                      | Legacy short form      |
| `--publish published=80,target=5000`              | Explicit new form      |
| `-p 80:5000/udp`                                  | Legacy with protocol   |
| `--publish published=80,target=5000,protocol=udp` | New form with protocol |

```bash theme={null}
