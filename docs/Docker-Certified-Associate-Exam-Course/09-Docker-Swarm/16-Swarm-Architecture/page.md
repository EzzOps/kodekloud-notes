# Swarm Architecture

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Swarm-Architecture/page

This article explains Docker Swarm architecture, its components, features, and how to manage container orchestration for high availability and scalability.

Running containers on a single Docker host is convenient for development or testing, but in production it introduces a single point of failure. If that host goes down, all your services become unavailable. Docker Swarm solves this by clustering multiple Docker hosts into one logical unit, providing high availability, load balancing, and seamless scaling.

## Swarm Cluster Components

A Swarm cluster groups physical or virtual machines—on-premises or in the cloud—into a unified environment. Every node runs Docker Engine and joins the cluster either as a manager or a worker.

| Node Type | Responsibilities                                             | Commands                                    |
| --------- | ------------------------------------------------------------ | ------------------------------------------- |
| Manager   | Maintains desired state, schedules tasks, serves the API     | `docker node ls`<br />`docker node promote` |
| Worker    | Executes tasks assigned by managers, runs service containers | `docker node ls`<br />`docker node demote`  |

<Callout icon="lightbulb">
  By default, manager nodes can handle workloads in addition to management tasks. To dedicate a manager solely to orchestration, use `docker node update --availability drain <node>`.
</Callout>

When you deploy an application, you submit a service definition to a manager. The manager translates it into tasks and distributes them across worker nodes, which then run the required containers.

## Declarative Service Definitions

Docker Swarm uses declarative YAML files—similar to Docker Compose—to define multi-service applications. Store these files in version control to track changes and facilitate CI/CD workflows:

```yaml theme={null}
