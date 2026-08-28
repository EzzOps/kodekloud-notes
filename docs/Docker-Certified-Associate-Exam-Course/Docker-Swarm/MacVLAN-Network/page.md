# docker-compose.yml
version: "3"
services:
  web:
    image: simple-webapp
  database:
    image: mongodb
  messaging:
    image: redis:alpine
```

Launch all services together:

```bash theme={null}
docker-compose up
```

This approach centralizes configuration but is limited to a single host.

## 2. Introducing Docker Swarm and Stacks

Docker Swarm enables clustering multiple Docker engines into a single, fault-tolerant Swarm cluster. Instead of `docker run`, you create services:

```bash theme={null}
docker service create --name web simple-webapp
docker service create --name database mongodb
docker service create --name messaging redis:alpine
```

With Docker Stack, you can use your Compose file to deploy across the Swarm:

```bash theme={null}
docker stack deploy --compose-file docker-compose.yml mystack
```

<Callout icon="lightbulb">
  Docker Stack uses the same Compose file format (v3+), so you can reuse your existing `docker-compose.yml` with minimal changes.
</Callout>

## 3. Containers, Services, and Stacks

* **Container**: A running instance of an image, isolated with its dependencies.
* **Service**: A scalable set of containers of the same image, distributed across Swarm nodes.
* **Stack**: A collection of related services that define an application.

<Frame>
  ![The image illustrates a hierarchical structure of a stack, showing the relationship between stacks, services, and containers using a pyramid and a diagram.](https://kodekloud.com/kk-media/image/upload/v1752873927/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Stack/stack-services-containers-diagram.jpg)
</Frame>

## 4. Example: Voting Application

We’ll deploy a simple voting app with Redis, PostgreSQL, vote service, result service, and a worker.

### 4.1 Single-Host Deployment with Docker Compose

```yaml theme={null}
version: "3"
services:
  redis:
    image: redis
  db:
    image: postgres:9.4
  vote:
    image: voting-app
  result:
    image: result
  worker:
    image: worker
```

```bash theme={null}
docker-compose up
```

All services run on your local Docker host.

### 4.2 Multi-Node Deployment with Docker Stack

Assume a Swarm with one manager and two workers. Enhance the Compose file with a `deploy` section for Swarm-specific settings.

#### 4.2.1 Replicas

Scale services by defining replica counts:

```yaml theme={null}
version: "3"
services:
  redis:
    image: redis
    deploy:
      replicas: 1
  db:
    image: postgres:9.4
    deploy:
      replicas: 1
  vote:
    image: voting-app
    deploy:
      replicas: 2
  result:
    image: result
    deploy:
      replicas: 1
  worker:
    image: worker
    deploy:
      replicas: 1
```

Deploy the stack:

```bash theme={null}
docker stack deploy --compose-file docker-compose.yml voting
```

#### 4.2.2 Placement Constraints

Ensure critical services run only on manager nodes:

```yaml theme={null}
  db:
    image: postgres:9.4
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
```

#### 4.2.3 Resource Limits

Protect node resources by setting CPU and memory limits:

```yaml theme={null}
  vote:
    image: voting-app
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "0.01"
          memory: 50M
```

#### 4.2.4 Health Checks

Automatically monitor container health:

```yaml theme={null}
  vote:
    image: voting-app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 1m30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "0.01"
          memory: 50M
```

| Field          | Description                                                          |
| -------------- | -------------------------------------------------------------------- |
| `test`         | Command run inside the container to check health (e.g., `curl`).     |
| `interval`     | Time between health checks (e.g., `1m30s`).                          |
| `timeout`      | Maximum time to wait before marking a check as failed (e.g., `10s`). |
| `retries`      | Number of consecutive failures before marking unhealthy (e.g., `3`). |
| `start_period` | Grace period before starting health checks (e.g., `40s`).            |

## 5. Common Stack Commands

| Command                                            | Description                           |
| -------------------------------------------------- | ------------------------------------- |
| `docker stack deploy --compose-file <file> <name>` | Deploy or update a stack              |
| `docker stack ls`                                  | List all stacks                       |
| `docker stack services <stack_name>`               | List services within a specific stack |
| `docker stack ps <stack_name>`                     | List tasks (containers) for a stack   |
| `docker stack rm <stack_name>`                     | Remove an entire stack                |

<Callout icon="triangle-alert">
  Removing a stack stops and removes all associated services and containers. Use with caution in production environments.
</Callout>

## References

* [Docker Stack Deploy](https://docs.docker.com/engine/reference/commandline/stack_deploy/)
* [Compose File Reference](https://docs.docker.com/compose/compose-file/)
* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Docker Healthcheck Documentation](https://docs.docker.com/engine/reference/builder/#healthcheck)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/bc1a4ebd-aacc-4af8-a070-1f9f81d1903c" />
</CardGroup>


# MacVLAN Network

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/MacVLAN-Network/page

This guide explains how to create a MACVLAN network in Docker, detailing its modes and comparing Docker's network drivers.

Containers typically use network namespaces for isolation, but some legacy applications require direct attachment to the physical LAN. Docker’s MACVLAN driver assigns each container its own MAC address on a virtual interface, making the container appear as a standalone host on your network. This guide covers how to create a MACVLAN network, the available modes, and a comparison of Docker’s built-in network drivers.

## Why Use MACVLAN?

* Direct Layer 2 connectivity with your physical network
* Unique MAC addresses for each container
* Support for legacy applications requiring their own IP on the LAN

<Callout icon="lightbulb">
  Before you begin, ensure the parent interface (`eth0` in these examples) is active and not part of another bridge. You may need to bring it up with `ip link set eth0 up`.
</Callout>

## 1. Creating a MACVLAN Network

Use the `macvlan` driver when creating a Docker network:

```bash theme={null}
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  my_macvlan_net
```

Parameters:

* `-d macvlan`\
  Selects the MACVLAN driver.
* `--subnet` / `--gateway`\
  Defines the IP range and default gateway on the physical LAN.
* `-o parent=eth0`\
  Binds Docker’s MACVLAN to the host interface `eth0`.
* `my_macvlan_net`\
  Your custom network name.

## 2. MACVLAN Modes

MACVLAN supports two primary modes for segmenting and isolating traffic:

| Mode                    | Description                                             | Use Case                                               |
| ----------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| Bridge (`bridge`)       | Creates a Layer 2 bridge on the parent interface.       | Simple flat network where all containers share a VLAN. |
| 802.1Q Trunk (`802.1q`) | Tags traffic on a VLAN subinterface (e.g., `eth0.100`). | Segmented VLAN routing and filtering per container.    |

<Callout icon="triangle-alert">
  Your physical switch must support 802.1Q tagging, and the parent interface must be configured as a trunk port to carry multiple VLANs.
</Callout>

## 3. Summary of Docker Network Drivers

Here’s a quick reference table comparing Docker’s built-in network drivers:

| Driver  | Description                                                                           | Typical Use Case                              |
| ------- | ------------------------------------------------------------------------------------- | --------------------------------------------- |
| none    | Disables all networking for the container.                                            | Security testing, isolated workloads          |
| host    | Shares the host’s network namespace; removes network isolation.                       | High-performance scenarios, monitoring tools  |
| bridge  | Default driver; creates a local L2 bridge on a single host.                           | Single-host deployments, simple microservices |
| overlay | Creates an L3 overlay across multiple hosts (requires a key-value store backend).     | Multi-host Swarm services, cross-node traffic |
| macvlan | Assigns unique MAC addresses for L2 connectivity, available in bridge and VLAN modes. | Legacy apps, direct LAN access                |
| ipvlan  | Operates at L2 but routes at host level for higher scalability in dense networks.     | Large-scale deployments with many endpoints   |

## 4. Next Steps

Once your MACVLAN network is created, you can launch containers on it:

```bash theme={null}
docker run -d --network my_macvlan_net --name webserver nginx
```

Each container will receive an IP from your defined subnet and appear as a physical host on the LAN.

## Links and References

* [Docker Network Drivers](https://docs.docker.com/network/)
* [Linux VLAN Documentation](https://www.kernel.org/doc/Documentation/networking/vlan.txt)
* [Kubernetes CNI MACVLAN Plugin](https://github.[SECRET_REDACTED])

That concludes this lesson on Docker MACVLAN networks. Advanced multi-VLAN and trunking scenarios will be covered in a future guide.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/05f49e5b-7ee1-451e-9ea3-f11c3f1508a3" />
</CardGroup>
