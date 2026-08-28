# docker-compose.yml
services:
  web:
    image: "mmumshad/simple-webapp"
  database:
    image: "mongodb"
  messaging:
    image: "redis:alpine"
  orchestration:
    image: "ansible"
```

Start your complete stack with:

```bash theme={null}
docker-compose up
```

### Deploying with Docker Swarm

When deploying on Docker Swarm, the concept is similar but offers additional flexibility. Instead of using the Docker run command, you create services for each component. For instance:

```bash theme={null}
docker service create mmumshad/simple-webapp
docker service create mongodb
docker service create redis
docker service create ansible
```

You can define the entire stack for Docker Swarm in a Compose file using version 3 format:

```yaml theme={null}
version: 3
services:
  web:
    image: "mmumshad/simple-webapp"
  database:
    image: "mongodb"
  messaging:
    image: "redis:alpine"
  orchestration:
    image: "ansible"
```

Deploy the complete stack with:

```bash theme={null}
docker stack deploy
```

This method enables you to manage your entire application configuration in one file, simplifying the process of scaling and monitoring multiple instances of your services.

***

## Understanding the Docker Stack Hierarchy

Understanding the hierarchy within Docker helps you manage resources effectively. Here's a breakdown of the Docker stack hierarchy:

* **Container:** A packaged unit of an application with all its dependencies.
* **Service:** One or more instances of the same container running on one or more nodes. For example, running several instances of a web application creates a service.
* **Stack:** A collection of interrelated services that form a complete application.

Consider the following diagram that illustrates these relationships:

<Frame>
  ![The image shows a person explaining a diagram about containers and services in a stack, with visual representations of containerized applications.](https://kodekloud.com/kk-media/image/upload/v1752874076/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Docker-Stacks/frame_140.jpg)
</Frame>

In this diagram, multiple web containers are combined to form a service, alongside a separate messaging service (Redis) with a single container and a database service running two containers. Together, these elements compose a full application stack.

<Frame>
  ![The image illustrates a hierarchical structure of stack, service, and container, with a person explaining the concept.](https://kodekloud.com/kk-media/image/upload/v1752874077/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Docker-Stacks/frame_190.jpg)
</Frame>

***

## Deploying an Application on a Multi-Node Swarm Cluster

Let’s examine a scenario where you deploy an application on a Docker Swarm Cluster with five nodes (four worker nodes and one manager node). Consider the following deployment details:

* **Redis Service:** One instance, which Docker Swarm deploys on any available worker node.
* **PostgreSQL Database:** Should reside on a manager node using placement constraints.
* **Voting Application:** Due to high traffic, this application runs two instances, and you may also run separate Result and Worker services.

The diagram below represents a sample multi-node cluster setup:

<Frame>
  ![The image shows a presentation slide about a sample application in Docker Swarm, featuring manager and worker nodes with various software icons, alongside a presenter.](https://kodekloud.com/kk-media/image/upload/v1752874079/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Docker-Stacks/frame_250.jpg)
</Frame>

Docker Swarm optimizes container placement automatically unless specific constraints are provided. You can also configure resource limits per service; for example, the Redis service might use a maximum of 5% of the CPU and 50 MB of memory per host.

***

## Configuring a Stack for Docker Swarm

Stacks in Docker Swarm are defined using YAML files similar to Docker Compose files, but they use version 3 to include swarm-specific properties under the deploy key. Below is a basic configuration example:

```yaml theme={null}
version: 3
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

### Placement Constraints

To ensure that the database service runs on a specific node (e.g., a manager node), use placement constraints:

```yaml theme={null}
version: 3
services:
  db:
    image: postgres:9.4
    deploy:
      placement:
        constraints:
          - node.hostname == node1
          - node.role == manager
```

### Limiting Resource Usage

To prevent a service from consuming excessive resources, you can set resource limits. For example, to restrict Redis resource usage:

```yaml theme={null}
version: 3
services:
  redis:
    image: redis
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '0.01'
          memory: 50M
```

<Callout icon="lightbulb">
  Keep in mind that these configurations allow for scalable deployment and resource management. For more advanced options, refer to the latest Docker documentation.
</Callout>

***

While numerous options and properties exist for configuring Docker Stacks, it’s crucial to understand the core concepts to adapt them to real-world applications. For the most current best practices and sample templates, always refer to the [Docker Documentation](https://docs.docker.com/).

Ready to put these concepts into practice? Continue to the demo section and experiment with the provided configurations to create your own stack file.

That’s it for this comprehensive guide on Docker Stacks—see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/9c0c70f2-8fd8-459d-b5fb-6c70585ad4a7/lesson/7ab62eca-09bc-4baa-bfe5-f251a0e8c329" />
</CardGroup>


# Demo Docker Swarm

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Docker-Swarm/Demo-Docker-Swarm/page

This guide covers creating and managing a Docker Swarm cluster, including initialization, adding nodes, simulating failures, and recovery methods.

Welcome to this detailed guide on creating and managing a Docker Swarm cluster. In this tutorial, you'll learn how to initialize a Docker Swarm cluster, add worker and manager nodes, simulate node failures, and recover from manager failures—all while maintaining a healthy quorum. This guide serves as an essential resource for DevOps engineers and system administrators looking to deploy resilient container orchestration with Docker Swarm.

***

## Setting Up the Swarm Cluster

In this demo, three servers are used. One server acts as the Docker master, while the other two serve as Docker nodes. Initially, each server only has Docker installed, differing only by their hostnames.

To establish the swarm cluster, identify the Docker master among the three servers and initialize the swarm. Running the following command without an advertised address causes an error because the Docker host has multiple network interfaces:

```bash theme={null}
root@DOCKER_MASTER:/root # docker swarm init
Error response from daemon: could not choose an IP address to advertise since this system has multiple addresses on different interfaces (192.168.1.9 on eth0 and 192.168.56.101 on eth1) - specify one with --advertise-addr
```

Since the master has two network interfaces, specify the IP address using the `--advertise-addr` flag. In this example, we choose to advertise the IP address 192.168.56.101:

```bash theme={null}
root@DOCKER_MASTER:/root # docker swarm init --advertise-addr 192.168.56.101
Swarm initialized: current node (uiddwelph55pjtk6vi97tsn5s) is now a manager.

To add a worker to this swarm, run the following command:
    docker swarm join --token SWMTKN-1-[SECRET_REDACTED]-5a6525x9twuwpdg8v46jj29ul 192.168.56.101:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
root@DOCKER_MASTER:/root #
```

The output provides the necessary command for adding a node to the swarm. The generated token serves as authentication for a worker node to join the cluster.

When running the command `docker node ls` on the master, only the master node appears (marked as active and the leader), since no additional nodes have been added yet.

***

## Adding Worker Nodes

To add worker nodes, follow these steps:

1. Copy the generated `docker swarm join` command.
2. Execute it on each worker server.

For example, executing the join command on a worker node produces the following confirmation:

```bash theme={null}
root@Docker_NODE1:/root # docker swarm join --token SWMTKN-1-[SECRET_REDACTED]-5a6525x9tvwwpdg 
This node joined a swarm as a worker.
```

Once a worker node successfully joins, the master node's listing will include both the master (marked with a star and labeled as Leader) and the new worker:

```bash theme={null}
root@DOCKER_MASTER:/root # docker node ls
ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
uildwelph5spjtk6vi97tsn5s *   docker-master   Ready   Active        Leader
lzd18400ditete34e5nvsdn4n    docker-node1    Ready   Active
```

Repeat the same process on the second worker node. Once both nodes are connected, `docker node ls` displays three nodes in total: one master and two workers.

***

## Removing a Node from the Cluster

If you need to remove a node, execute the following on the node you wish to leave the swarm:

```bash theme={null}
root@DOCKER_NODE2:/root # docker swarm leave
Node left the swarm.
```

<Callout icon="lightbulb">
  Keep in mind that there may be a short delay before the node's status changes from “Ready” to “Down” in the swarm listing. To completely remove a node that remains in the list, run the following command from the master node:
</Callout>

```bash theme={null}
root@DOCKER_MASTER:/root # docker node rm docker-node1
```

After removal, running `docker node ls` confirms that the node has been deleted from the swarm.

***

## Adding Manager Nodes

A Docker Swarm cluster can support multiple manager nodes, which significantly improves high availability. To add a new manager:

1. Change the hostname of the node if necessary.
2. Retrieve the manager join token by running:

```bash theme={null}
root@docker-master:/root # docker swarm join-token manager
To add a manager to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-[SECRET_REDACTED]-7jbbj8kldn4jaj2naidz9lh7 192.168.56.101:2377
```

Next, run the provided command on the intended manager node (e.g., `docker-master2`):

```bash theme={null}
root@docker-master2:/root # docker swarm join --token SWMTKN-1-[SECRET_REDACTED]-7jbbjj8kldn4jaj2naidz9lh7 192.168.56.101:2377
This node joined a swarm as a manager.
```

After adding, running `docker node ls` will show two managers: one labeled as Leader and the other as Reachable. Worker nodes will have no manager status listed.

To add an additional worker node, retrieve the worker join token with the following command:

```bash theme={null}
root@docker-master:/root # docker swarm join-token worker
```

Then, execute the join command on the worker machine.

***

## Promoting a Worker to a Manager

At times, you might need to promote an existing worker node to a manager. To do so, run the promotion command from an active manager node:

```bash theme={null}
root@docker-master:/root # docker node promote docker-node2
```

A subsequent execution of `docker node ls` confirms that `docker-node2` now shows a manager status—typically “Reachable” or “Leader”—while the remaining worker nodes continue to display a blank manager status.

***

## Simulating Node Failures and Managing Quorum

An important aspect of managing a Docker Swarm cluster is handling node failures. To simulate a manager node failure, shut down one of the manager nodes. For example, shutting down `docker-master3` will result in its status changing to “Unreachable,” as shown below:

```bash theme={null}
root@docker-master:/root # docker node ls
ID                            HOSTNAME          STATUS      AVAILABILITY  MANAGER STATUS
qp9p5cmbhf3czl3rxy342pywc    docker-master3    Ready       Active        Unreachable
uildwelph5spjtk6vi97tsn5     docker-master     Ready       Active        Leader
zycf5u8yudke6nfzo74gryssx    docker-master2   Ready       Active        Reachable
```

<Callout icon="triangle-alert">
  A Docker Swarm cluster with three managers requires a majority (at least two) to maintain quorum. If too many managers go offline, you might encounter error messages when executing management commands:
</Callout>

```bash theme={null}
Error response from daemon: rpc error: code = 2 desc = The swarm does not have a leader. It's possible that too few managers are online.
```

During a loss of quorum, running services on worker nodes remain operational, but management tasks such as adding new services or nodes will be unavailable until quorum is re-established.

***

## Recovering from a Manager Failure

If a manager failure causes the loss of quorum and it is not possible to bring all managers back online, you can force-create a new swarm cluster. Use the `--force-new-cluster` flag along with the `--advertise-addr` parameter:

```bash theme={null}
root@docker-master:/root # docker swarm init --advertise-addr 192.168.56.101 --force-new-cluster
```

After initiating a new cluster, `docker node ls` will display the master node as the only manager. You can then rejoin the worker nodes to the new cluster. Note that previously registered manager nodes will lose their status in the process.

***

## Recap

In this guide, we covered the following key points:

| Task                         | Description                                                                               | Command/Example                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Initialize Docker Swarm      | Start a swarm on the designated master node with the correct advertised IP address.       | `docker swarm init --advertise-addr 192.168.56.101`                     |
| Add Worker Node              | Use the provided worker token to join a new worker node to the swarm.                     | `docker swarm join --token <worker-token> 192.168.56.101:2377`          |
| Remove Node                  | Remove a node from the swarm gracefully and then force-remove it from the master listing. | `docker swarm leave` and `docker node rm <node>`                        |
| Add Manager Node             | Retrieve the manager join token and execute the join command on the new manager node.     | `docker swarm join-token manager`                                       |
| Promote Worker               | Promote an existing worker node to a manager to expand the managerial capacity.           | `docker node promote <worker-node>`                                     |
| Simulate and Manage Failures | Observe how the cluster behaves when manager nodes go down and manage quorum issues.      | Shutdown a manager to simulate failure and run `docker node ls`         |
| Force New Cluster Recovery   | Recover from a manager failure and lost quorum by forcing a new cluster formation.        | `docker swarm init --advertise-addr 192.168.56.101 --force-new-cluster` |

Docker Swarm is designed to ensure that services continue to run even if some nodes fail, as long as a quorum of managers is maintained. Management functions may be temporarily blocked during these failures, but running containers will persist without disruption.

Thank you for reading this guide. We hope this detailed demo enhances your understanding of managing a Docker Swarm cluster and helps you implement robust orchestration in your environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/59d6dff1-0181-4a5e-9c05-6da9e38ae605/lesson/d3a45389-334b-4c61-bb82-9e86711bf0ee" />
</CardGroup>
