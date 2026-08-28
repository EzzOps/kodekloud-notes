# Scaling Rolling Updates and Rollbacks

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Scaling-Rolling-Updates-and-Rollbacks/page

This guide covers scaling services, performing rolling updates, and executing rollbacks in Docker Swarm.

In this guide, you’ll learn how to scale your services, perform seamless rolling updates, and execute rollbacks in Docker Swarm. We’ll run all commands on the manager node while Swarm orchestrates tasks on worker nodes.

***

## Table of Contents

1. [Deploying a Service](#deploying-a-service)
2. [Scaling Service Replicas](#scaling-service-replicas)
3. [Rolling Updates](#rolling-updates)
   * [Default Update Behavior](#default-update-behavior)
   * [Introducing an Update Delay](#introducing-an-update-delay)
   * [Parallel Updates](#parallel-updates)
4. [Inspecting Update & Rollback Configuration](#inspecting-update--rollback-configuration)
5. [Handling Update Failures](#handling-update-failures)
6. [Rolling Back a Service](#rolling-back-a-service)
7. [References](#references)

***

## Deploying a Service

By default, creating a service launches a single replica. Here’s how to deploy a simple web service listening on port 80:

```bash theme={null}
docker service create \
  --name web \
  --publish 80:80 \
  web:latest
```

<Callout icon="lightbulb">
  Ensure the `web:latest` image is available locally or on your registry before creating the service.
</Callout>

***

## Scaling Service Replicas

Adjust the replica count of an existing service with `docker service update --replicas`.

Scale **up** to three replicas:

```bash theme={null}
docker service update \
  --replicas 3 \
  web
```

Scale **down** to one replica:

```bash theme={null}
docker service update \
  --replicas 1 \
  web
```

Docker Swarm will automatically add or remove tasks on the worker nodes to match your desired state.

***

## Rolling Updates

Rolling updates replace containers one batch at a time, ensuring zero downtime.

### Default Update Behavior

After tagging your new image (e.g., `web:2.0`), trigger the rolling update:

```bash theme={null}
docker service update \
  --image web:2.0 \
  web
```

Swarm will:

* Stop one container
* Deploy a new one
* Wait for it to pass health checks
* Repeat until all replicas are updated

### Introducing an Update Delay

Pause between updating each batch with `--update-delay`:

```bash theme={null}
docker service update \
  --image web:3.0 \
  --update-delay 30s \
  web
```

This adds a 30-second wait after each batch to monitor stability.

### Parallel Updates

Increase throughput by updating multiple tasks simultaneously using `--update-parallelism`:

```bash theme={null}
docker service update \
  --image web:2.1 \
  --update-parallelism 2 \
  web
```

This example updates up to two replicas at once, balancing speed and reliability.

***

## Inspecting Update & Rollback Configuration

Use `docker service inspect` to review how your service handles updates and rollbacks:

```bash theme={null}
docker service inspect web --format '{{json .UpdateStatus}}'
```

Key fields in the output:

| Configuration     | Description                                                     |
| ----------------- | --------------------------------------------------------------- |
| Parallelism       | Number of tasks updated simultaneously                          |
| Delay             | Time to wait between update batches                             |
| Failure Action    | Behavior when an update fails (`pause`, `continue`, `rollback`) |
| Monitoring Period | Duration Swarm waits for a task to become healthy               |

***

## Handling Update Failures

By default, Swarm **pauses** on the first failure. Change this with `--update-failure-action`:

```bash theme={null}
docker service update \
  --image web:2.2 \
  --update-failure-action rollback \
  web
```

| Failure Action | Description                                      |
| -------------- | ------------------------------------------------ |
| pause          | Halt the update on error (default)               |
| continue       | Ignore failures and proceed to next batch        |
| rollback       | Revert immediately to the previous image/version |

<Callout icon="triangle-alert">
  Using `continue` can leave your cluster in a mixed-version state. Test thoroughly before choosing this option in production.
</Callout>

***

## Rolling Back a Service

If an update introduces instability, quickly revert to the last known good state:

```bash theme={null}
docker service update \
  --rollback \
  web
```

This command restores the previous image and update configuration across all replicas.

***

## References

* [Docker Service Commands](https://docs.docker.[AWS_SECRET_ACCESS_KEY]/)
* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Docker Rolling Updates](https://docs.docker.com/engine/swarm/manage-services/update-services/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/ce95610a-9d07-46eb-82eb-9b149da9521f" />
</CardGroup>
