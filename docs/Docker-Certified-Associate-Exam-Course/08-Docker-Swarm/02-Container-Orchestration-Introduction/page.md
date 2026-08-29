# Initialize a new Swarm with auto-lock enabled
docker swarm init --autolock=true

# Enable auto-lock on an existing Swarm
docker swarm update --autolock=true
```

Example output:

```text theme={null}
Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock` command and provide the following key:
SWMKEY-1-7K9wg5n85QeC4Zh7rZ0vSV0b5MteDsUvpVhG/lQnbl0
Please remember to store this key in a password manager, since without it you will not be able to restart the manager.
```

## Manager Restart and Unlocking

After a manager restart, the Swarm remains **locked**. Any attempt to run Swarm commands will result in an error:

```bash theme={null}
$ docker node ls
Error response from daemon: Swarm is encrypted and needs to be unlocked before it can be used.
Please use "docker swarm unlock" to unlock it.
```

To resume normal operation, unlock the manager:

```bash theme={null}
$ docker swarm unlock
Enter unlock key: SWMKEY-1-7K9wg5n85QeC4Zh7rZ0vSV0b5MteDsUvpVhG/lQnbl0
```

Once the manager is unlocked, it will rejoin disconnected nodes automatically.

## Quick Reference

| Command                               | Description                                   |
| ------------------------------------- | --------------------------------------------- |
| `docker swarm init --autolock=true`   | Initialize a new Swarm with auto-lock enabled |
| `docker swarm update --autolock=true` | Turn on auto-lock for an existing Swarm       |
| `docker swarm unlock`                 | Unlock a locked Swarm manager after restart   |

## Further Reading

* [Docker Swarm Security Overview](https://docs.docker.com/engine/swarm/)
* [High Availability in Docker Swarm](https://docs.docker.com/engine/swarm/swarm-mode/manager/README/)
* [Docker Swarm Autolock Deep Dive](https://docs.docker.com/engine/swarm/autolock/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/c17d7f98-d4b0-4b73-a1cc-4aa7c6e31015)


# Container Orchestration Introduction

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Container-Orchestration-Introduction/page

This article explores container orchestration and its importance for efficiently managing containerized applications at scale.

In this lesson, we’ll explore container orchestration and why it’s essential for running containerized applications at scale. Up to this point, we’ve used Docker to launch single instances of applications:

```bash theme={null}
docker run nodejs
```

While this works for development or low-traffic scenarios, it becomes cumbersome when you need to:

* Deploy multiple instances
* Monitor container health
* Automate restarts on failure
* Handle host-level outages

***

## The Challenge of Manual Scaling

Imagine your Node.js application starts receiving more traffic. You’d manually spin up additional containers:

```bash theme={null}
docker run nodejs
docker run nodejs
docker run nodejs
```

You also need to:

* Monitor each container’s CPU, memory, and response time
* Restart containers when they crash
* Migrate workloads if a Docker host fails

> **triangle-alert** Manual scripts can help automate tasks, but they often become brittle as you scale. Maintaining and debugging those scripts can turn into a full-time job.

At small scale, manual intervention is possible. But with **tens of thousands of containers**, you need a more robust, automated solution.

***

## Enter Container Orchestration

Container orchestration platforms let you define desired state and let the system handle:

* Container placement across hosts
* Health checks and automatic restarts
* Load balancing and service discovery
* Cluster auto-scaling
* Configuration management

For example, with Docker Swarm you can scale your service to 100 replicas in one command:

```bash theme={null}
docker service create --name my-node-app --replicas=100 nodejs
```

Or update an existing service:

```bash theme={null}
docker service scale my-node-app=100
```

***

## Key Features of Orchestration Platforms

| Feature                            | Description                                           |
| ---------------------------------- | ----------------------------------------------------- |
| Automatic Scaling                  | Increase or decrease replicas based on resource usage |
| Self-Healing                       | Detect failed containers and reschedule replacements  |
| Rolling Updates & Rollbacks        | Deploy changes without downtime                       |
| Service Discovery & Load Balancing | Expose services with DNS and virtual IPs              |
| Storage Orchestration              | Attach persistent volumes dynamically                 |
| Configuration & Secret Management  | Securely inject configuration and secrets             |

***

## Popular Orchestration Solutions

| Platform     | Pros                                                      | Cons                                    |
| ------------ | --------------------------------------------------------- | --------------------------------------- |
| Docker Swarm | Easy to set up; native Docker integration                 | Limited auto-scaling; smaller ecosystem |
| Apache Mesos | Highly scalable; multi-tenant support                     | Complex to configure and maintain       |
| Kubernetes   | Extensive community support; rich ecosystem; cloud-native | Steeper learning curve                  |

For a deeper dive, see [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

> **lightbulb** Kubernetes is supported by all major cloud providers (AWS, GCP, Azure) and offers a vast plugin ecosystem for networking, storage, and security.

***

## What’s Next

In upcoming lessons, we’ll walk through:

* Deploying applications with **Docker Swarm**
* Setting up a **Kubernetes** cluster
* Implementing **auto-scaling**, **rolling updates**, and **persistent storage**

***

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Documentation](https://docs.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/c7b34bd2-5dab-48b2-94a9-b69bc331dbec)
