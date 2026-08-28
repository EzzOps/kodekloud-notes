# service-definition.yml
version: "3.8"
services:
  web:
    image: "simple-webapp:latest"
    ports:
      - "80:80"
  database:
    image: "mongo:5.0"
    volumes:
      - db-data:/data/db
  cache:
    image: "redis:alpine"
    deploy:
      replicas: 2

volumes:
  db-data:
```

<Callout icon="lightbulb">
  Declarative definitions allow you to scale, update, and rollback services with a single command: `docker stack deploy -c service-definition.yml my_stack`.
</Callout>

## Key Features of Docker Swarm

### 1. Simplified Setup and Maintenance

Swarm is built directly into Docker Engine, so there’s no extra software to install. With the Docker CLI you can:

* Initialize a new cluster: `docker swarm init`
* Join nodes to the cluster: `docker swarm join --token <token> <manager-ip>:2377`
* Promote or demote managers: `docker node promote <node>`

<Frame>
  ![The image lists features of Docker Swarm, such as simplified setup and scaling, alongside a diagram showing a Docker Swarm setup with manager and worker nodes.](https://kodekloud.com/kk-media/image/upload/v1752873930/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-Architecture/docker-swarm-features-setup-diagram.jpg)
</Frame>

### 2. Scalability and Load Balancing

You can scale services on demand using:

```bash theme={null}
docker service scale web=10
```

Swarm’s internal load balancer distributes requests across all healthy containers. If you need an external load balancer, point it at any manager or worker node.

<Frame>
  ![The image illustrates the features of Docker Swarm, highlighting aspects like simplified setup, scaling, and load balancing, alongside a diagram showing an external load balancer connected to Docker hosts with web services.](https://kodekloud.com/kk-media/image/upload/v1752873932/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-Architecture/docker-swarm-features-diagram.jpg)
</Frame>

### 3. Rolling Updates and Self-Healing

Swarm performs rolling updates by default, updating one container at a time:

```bash theme={null}
docker service update \
  --image simple-webapp:2.0 \
  --update-parallelism 2 \
  --update-delay 10s \
  web
```

If a container crashes or fails health checks, Swarm automatically replaces it to match the desired state.

<Callout icon="triangle-alert">
  Always test updates in a staging environment before applying to production. Use `--rollback` to revert quickly if an update misbehaves.
</Callout>

### 4. Secure Networking and Service Discovery

Node-to-node communication is secured with mutual TLS. Overlay networks let containers on different hosts communicate as if they were on the same LAN. Built-in DNS routing ensures each service name resolves to the correct VIP or container IP.

<Frame>
  ![The image describes features of Docker Swarm, including simplified setup, scaling, and service discovery, alongside a diagram showing a manager node with a DNS server and worker nodes with web services.](https://kodekloud.com/kk-media/image/upload/v1752873934/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-Architecture/docker-swarm-features-diagram-2.jpg)
</Frame>

## Summary and Next Steps

In this article, we covered the core architecture and features that make Docker Swarm a powerful container orchestration solution. You learned about:

* Cluster components and node roles
* Declarative service definitions
* Key features: setup, scaling, updates, and networking

Next, dive into practical guides on:

* Setting up a multi-node Swarm cluster
* Deploying production-grade services
* Advanced networking patterns

## Links and References

* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Docker Compose File Reference](https://docs.docker.com/compose/compose-file/)
* [Docker Networking Guide](https://docs.docker.com/network/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/6b6f6d6a-9fe3-424a-bf00-c93d04a2010e" />
</CardGroup>


# Swarm High Availability Quorum

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Swarm-High-Availability-Quorum/page

This article discusses Docker Swarms high availability, quorum requirements, and the Raft consensus algorithm for managing cluster state and fault tolerance.

In a Docker Swarm cluster, **manager nodes** are the control plane where the Swarm is initialized. Manager responsibilities include:

* Maintaining the cluster’s desired state
* Scheduling and orchestrating containers
* Adding or removing nodes
* Monitoring health and distributing services

Relying on a single manager is risky: if it goes down, there’s no orchestrator. Deploying multiple managers increases resilience but introduces the risk of conflicting decisions. Docker Swarm avoids this by electing one manager as the **leader**, which alone makes scheduling decisions. All managers—including the leader—must agree on changes via a consensus protocol before they’re committed.

<Frame>
  ![The image illustrates a Docker Swarm architecture with three manager nodes, including a leader, and three worker nodes, all labeled as Docker Hosts.](https://kodekloud.com/kk-media/image/upload/v1752873935/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-High-Availability-Quorum/docker-swarm-architecture-nodes.jpg)
</Frame>

Even the leader must replicate its decisions to a majority of managers to avoid split-brain scenarios. Docker implements this using the [Raft consensus algorithm](https://en.wikipedia.org/wiki/Raft_\(computer_science\)).

## Distributed Consensus with Raft

Raft ensures that one leader is elected and all state changes are safely replicated:

1. Each manager starts with a random election timeout.
2. When a timeout expires, that node requests votes from its peers.
3. Once it gathers a majority, it becomes leader.
4. The leader sends periodic heartbeats to followers.
5. If followers miss heartbeats, they trigger a new election.

When the leader receives a request to change the cluster (e.g., add a worker or create a service), it:

1. Appends the change as an entry in its Raft log.
2. Sends the log entry to each follower.
3. Waits for a majority of acknowledgments.
4. Commits the change across all Raft logs.

This process guarantees consistency even if the leader fails mid-update.

<Frame>
  ![The image illustrates the RAFT distributed consensus algorithm, showing a series of nodes with captain hats and databases, with an instruction being passed and acknowledged.](https://kodekloud.com/kk-media/image/upload/v1752873935/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-High-Availability-Quorum/raft-consensus-algorithm-nodes.jpg)
</Frame>

## Quorum and Fault Tolerance

A **quorum** is the minimum number of managers required to make decisions. For *n* managers:

```text theme={null}
quorum = ⌊n/2⌋ + 1
```

Fault tolerance is the number of manager failures the cluster can sustain:

```text theme={null}
fault_tolerance = ⌊(n - 1) / 2⌋
```

| Managers (n) | Quorum (⌊n/2⌋+1) | Fault Tolerance (⌊(n-1)/2⌋) |
| -----------: | ---------------: | --------------------------: |
|            3 |                2 |                           1 |
|            5 |                3 |                           2 |
|            7 |                4 |                           3 |

<Frame>
  ![The image explains the concept of quorum in a distributed system, showing a table of managers, majority, and fault tolerance, along with a formula for calculating quorum. It also includes Docker recommendations and illustrations of Docker-themed characters.](https://kodekloud.com/kk-media/image/upload/v1752873936/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-High-Availability-Quorum/quorum-distributed-system-docker.jpg)
</Frame>

Docker recommends no more than **seven** managers per Swarm. More managers do not improve performance or scalability and only increase coordination overhead.

<Callout icon="lightbulb">
  Always keep an odd number of managers (3, 5, or 7) to prevent split-brain scenarios during network partitions.
</Callout>

## Best Practices for Manager Distribution

1. Use an **odd number** of managers (3, 5, or 7).
2. Spread managers across distinct failure domains (data centers or availability zones).
3. For seven managers, a **3–2–2** distribution across three sites ensures that losing any single site still leaves a quorum.

<Frame>
  ![The image illustrates a distribution of managers across three sites (A, B, and C) with a table showing the number of managers, majority, and fault tolerance. It highlights a best practice of distributing seven managers in a 3-2-2 configuration.](https://kodekloud.com/kk-media/image/upload/v1752873938/notes-assets/images/Docker-Certified-Associate-Exam-Course-Swarm-High-Availability-Quorum/manager-distribution-3-2-2-config.jpg)
</Frame>

## Failure Scenarios and Recovery

Imagine a Swarm with three managers and five workers hosting a web application. The quorum is two managers. If two managers go offline:

* The remaining manager can **no longer** perform cluster changes (no new nodes, no service updates).
* Existing services continue to run, but self-healing and scaling are disabled.

### Recovering Quorum

1. Bring failed managers back online. Once you restore at least one, the cluster regains quorum.
2. If you cannot recover old managers and only one remains, force a new cluster:
   ```bash theme={null}
   docker swarm init --force-new-cluster
   ```
   This single node becomes the manager, and existing workers resume running services.
3. Re-add additional managers:
   ```bash theme={null}
   # Promote an existing node to manager
   docker node promote <NODE>

   # Or join a new manager
   docker swarm join --token <MANAGER_TOKEN> <MANAGER_IP>:2377
   ```

That covers high availability, quorum calculation, Raft consensus, and best practices for Docker Swarm manager nodes. Good luck!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/e278e002-ec39-4895-8486-bce0f49c984d" />
</CardGroup>
