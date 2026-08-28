# Demo Service in Swarm Basic Operations

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Demo-Service-in-Swarm-Basic-Operations/page

This article covers basic operations for managing services in Docker Swarm, including creation, scaling, updates, and self-healing features.

Docker Swarm lets you manage containerized applications as services rather than individual containers. A **service** in Swarm mode ensures your desired state—replicas, load balancing, rolling updates, and self-healing—are always maintained.

## Table of Contents

1. [Verify Cluster Status](#1-verify-cluster-status)
2. [Create Your First Service](#2-create-your-first-service)
3. [Inspect Tasks and Service Details](#3-inspect-tasks-and-service-details)
4. [View Service Logs](#4-view-service-logs)
5. [Self-Healing Demonstration](#5-self-healing-demonstration)
6. [Remove the Service](#6-remove-the-service)
7. [Scale Services](#7-scale-services)
8. [Rolling Updates](#8-rolling-updates)
9. [Rollback](#9-rollback)
10. [Quick Command Reference](#10-quick-command-reference)

***

## 1. Verify Cluster Status

Ensure your 6-node Swarm is healthy and managers/workers are all **Ready**:

```bash theme={null}
docker node ls
```

Sample output:

```text theme={null}
ID                            HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS  ENGINE VERSION
kvbhteg486wmj881wp5vkqx53 *  managerone     Ready   Active       Leader          19.03.8
u81imabedhzsu4cawtoz6jh32    managerthree   Ready   Active       Reachable       19.03.8
s2zymqdbtfal66imydx31rlno    managertwo     Ready   Active       Reachable       19.03.8
38oehht7y9bsfs7kcoeji2cvah   workerone      Ready   Active       Active          19.03.8
k4gcc5ooc0mn8xl3f6bm2bp2d    workerthree    Ready   Active       Active          19.03.8
1pqddmhc2f0y79vq9najr841d    workertwo      Ready   Active       Active          19.03.8
```

<Callout icon="lightbulb">
  Always confirm that at least one manager node is in **Leader** status before proceeding.
</Callout>

***

## 2. Create Your First Service

Deploy a simple HTTP server using the `httpd:alpine` image on port 80:

```bash theme={null}
docker service create \
  --name first-service \
  -p 80:80 \
  httpd:alpine
```

Verify that the service is up:

```bash theme={null}
docker service ls
```

Expected output:

```text theme={null}
ID             NAME            MODE         REPLICAS  IMAGE            PORTS
njoes31daltz   first-service   replicated   1/1       httpd:alpine     *:80->80/tcp
```

***

## 3. Inspect Tasks and Service Details

List the tasks (containers) for `first-service`:

```bash theme={null}
docker service ps first-service
```

For a detailed, human-friendly overview:

```bash theme={null}
docker service inspect first-service --pretty
```

Key excerpt:

```text theme={null}
Name:           first-service
Service Mode:   Replicated
 Replicas:      1
Image:          httpd:alpine@sha256:...
Ports:
 Published:     80/TCP → 80/TCP
```

***

## 4. View Service Logs

Stream logs to troubleshoot or verify startup:

```bash theme={null}
docker service logs first-service
```

***

## 5. Self-Healing Demonstration

Swarm automatically replaces failed tasks to maintain the desired replica count.

1. On a worker, find and remove the container:
   ```bash theme={null}
   docker container ls
   docker rm -f <container_id>
   ```
2. Back on a manager, confirm Swarm recreated it:
   ```bash theme={null}
   docker service ps first-service
   ```

<Callout icon="lightbulb">
  Swarm will detect that the replica count is below the desired state and launch a new task immediately.
</Callout>

***

## 6. Remove the Service

Clean up by removing the service and all its tasks:

```bash theme={null}
docker service rm first-service
docker service ls
```

***

## 7. Scale Services

Run multiple replicas behind Swarm’s built-in load balancer to ensure zero downtime.

### a. Create a Service with Three Replicas

```bash theme={null}
docker service create \
  --name second-service \
  -p 80:80 \
  --replicas 3 \
  httpd:alpine
```

Verify:

```bash theme={null}
docker service ls
docker service ps second-service
```

### b. Scale Up to Five Replicas

```bash theme={null}
docker service update --replicas 5 second-service
```

### c. Scale Down to Three Replicas

```bash theme={null}
docker service update --replicas 3 second-service
```

***

## 8. Rolling Updates

Perform seamless image upgrades without stopping traffic.

1. View current image:
   ```bash theme={null}
   docker service inspect second-service --pretty | grep -i Image
   ```
2. Update to a new tag (e.g., `httpd:2`):
   ```bash theme={null}
   docker service update --image httpd:2 second-service
   ```
3. Monitor rollout:
   ```bash theme={null}
   docker service ls
   docker service ps second-service
   ```

<Callout icon="triangle-alert">
  During rolling updates, verify your application’s health checks to avoid cascading failures.
</Callout>

***

## 9. Rollback

If an update misbehaves, revert immediately:

```bash theme={null}
docker service update --rollback second-service
docker service inspect second-service --pretty | grep -i Image
```

***

## 10. Quick Command Reference

| Operation          | Command                                               |
| ------------------ | ----------------------------------------------------- |
| Verify cluster     | `docker node ls`                                      |
| Create service     | `docker service create --name <svc> -p 80:80 <image>` |
| List services      | `docker service ls`                                   |
| Inspect service    | `docker service inspect <svc> --pretty`               |
| View service tasks | `docker service ps <svc>`                             |
| Stream logs        | `docker service logs <svc>`                           |
| Remove service     | `docker service rm <svc>`                             |
| Scale service      | `docker service update --replicas <n> <svc>`          |
| Rolling update     | `docker service update --image <image:tag> <svc>`     |
| Rollback           | `docker service update --rollback <svc>`              |

***

## Links and References

* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Service Commands](https://docs.docker.[AWS_SECRET_ACCESS_KEY]/)
* [Rolling Updates](https://docs.docker.com/engine/swarm/how-swarm-mode-works/swarm-task-states/#rolling-updates)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/e6322da9-a312-4d22-965b-1e5f190178ca" />
</CardGroup>
