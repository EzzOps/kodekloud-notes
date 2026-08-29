# Not recommended: IP address may change on restart
mysql.connect(
    host='172.17.0.3',
    user='root',
    password='password',
    database='mydb'
)

# Recommended: use container name for stable resolution
mysql.connect(
    host='mysql',
    user='root',
    password='password',
    database='mydb'
)
```

## Service Discovery in Docker Swarm

In Swarm mode, every service is assigned a DNS entry matching its service name. Load balancing is handled automatically across all replicas.

```bash theme={null}
# Create an API server with 2 replicas
docker service create \
  --name api-server \
  --replicas 2 \
  api-server-image

# Create a web frontend
docker service create \
  --name web \
  web-image
```

The `web` service can connect to `api-server` simply by its name:

```bash theme={null}
curl http://api-server:8080/health
```

Requests to `api-server` are distributed across its replicas.

## Using a Custom Overlay Network

DNS-based service discovery only works on user-defined networks. The default `bridge` and `ingress` networks do not support inter-service name resolution. Create an overlay network to enable DNS resolution across multiple swarm nodes:

```bash theme={null}
# 1. Create a custom overlay network
docker network create \
  --driver overlay \
  app-network

# 2. Deploy services on the overlay network
docker service create \
  --name api-server \
  --replicas 2 \
  --network app-network \
  api-server-image

docker service create \
  --name web \
  --network app-network \
  web-image
```

Now, `api-server` resolves to one of its replicas whenever any service on `app-network` queries its name.

<Callout icon="lightbulb">
  Always attach your services to a user-defined overlay network for reliable DNS-based service discovery in Swarm.
</Callout>

## Network Comparison

| Network Type         | DNS Resolution Between Services | Scope                       |
| -------------------- | ------------------------------- | --------------------------- |
| Default `bridge`     | No                              | Single host only            |
| Ingress              | Routing mesh only               | Cluster-wide load balancing |
| User-defined overlay | Yes                             | Multi-host overlay          |

## Links and References

* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Docker Networking](https://docs.docker.com/network/)
* [Service Discovery in Swarm](https://docs.docker.com/engine/swarm/services/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/b28d1a0b-e491-46b3-a5c6-f81ce9ab2f3c" />
</CardGroup>


# Swarm Service Types

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Swarm-Service-Types/page

This guide explains Docker Swarm service modes, detailing replicated and global services, their deployment, and use case comparisons.

In Docker Swarm, services define how containers are deployed and managed across a cluster. Swarm supports two primary service modes: **replicated** and **global**. This guide explains each mode, shows how to deploy them, and compares their use cases.

## Replicated Service

A *replicated* service launches a specified number of identical tasks (containers). This is the default mode in Swarm.

<Callout icon="lightbulb">
  If you omit `--replicas`, Swarm defaults to 1 replica. You can also explicitly set `--mode replicated` if you prefer.
</Callout>

To deploy five replicas of a web service:

```bash theme={null}
docker service create \
  --name web \
  --replicas 5 \
  nginx:latest
```

Verify the service mode and replica count:

```bash theme={null}
docker service inspect web \
  --format '{{json .Spec.Mode}}'
```

Sample output:

```json theme={null}
{"Replicated":{"Replicas":5}}
```

Key points for replicated services:

* Tasks are spread evenly across available nodes.
* Scale up or down by updating `--replicas`.
* Ideal for stateless applications like web servers or APIs.

## Global Service

A *global* service ensures exactly one task runs on every node in the Swarm.

<Callout icon="triangle-alert">
  Do **not** specify `--replicas` with global services. Use only `--mode global`.
</Callout>

To deploy a monitoring agent on all nodes:

```bash theme={null}
docker service create \
  --name agent \
  --mode global \
  my-monitoring-agent:1.0
```

Global mode behavior:

* New nodes automatically receive one task.
* When a node leaves, its task is removed and not rescheduled.
* Perfect for logging, monitoring, and security daemons.

## Comparison Table

| Service Type | Replica Count    | Scheduling Behavior                | Common Use Case                  |
| ------------ | ---------------- | ---------------------------------- | -------------------------------- |
| Replicated   | User-defined (N) | Distributes tasks evenly           | Scalable web apps, microservices |
| Global       | One per node     | Runs exactly one task on each node | Agents for logging, monitoring   |

## References

* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [docker service create](https://docs.docker.com/engine/reference/commandline/service_create/)
* [docker service inspect](https://docs.docker.com/engine/reference/commandline/service_inspect/)
* [Docker Blog: Introduction to Swarm Mode](https://www.docker.com/blog/docker-swarm-mode-introduction/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/fbc7044c-ddc3-4458-ab2a-3d4db24d7090" />
</CardGroup>
