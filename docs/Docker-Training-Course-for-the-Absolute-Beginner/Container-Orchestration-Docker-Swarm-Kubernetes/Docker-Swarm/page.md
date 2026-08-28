# Docker Swarm

Source: https://notes.kodekloud.com/docs/Docker-Training-Course-for-the-Absolute-Beginner/Container-Orchestration-Docker-Swarm-Kubernetes/Docker-Swarm/page

This article provides an introduction to Docker Swarm, covering its setup and service deployment for container orchestration.

In this article, we provide a quick introduction to Docker Swarm, a powerful container orchestration tool. While Docker Swarm comprises many detailed concepts that could fill an entire course, this overview covers the essential details to get you started.

## What is Docker Swarm?

Docker Swarm allows you to combine multiple Docker hosts into a single cluster. Within the swarm cluster, the manager node orchestrates the distribution of your services (or application instances) across different hosts, ensuring high availability and effective load balancing. To set up Docker Swarm, ensure you have several hosts with Docker installed. Designate one host as the manager (sometimes known as the master or swarm manager) and the others as worker nodes.

## Initializing the Swarm

Once your hosts are ready, begin by initializing the Docker Swarm on the manager node using the following command:

```bash theme={null}
docker swarm init --advertise-addr <manager-ip>
```

When you run this command, Docker Swarm outputs a join command for the worker nodes. For example, the output might look like this:

```bash theme={null}
root@osboxes:/root/simple-webapp-docker # docker swarm init --advertise-addr 192.168.1.12
Swarm initialized: current node (0j76dum2r56p1xfn4u1pls2c) is now a manager.
To add a worker to this swarm, run the following command:
    docker swarm join --token SWMTKN-1-35va8b3fi5krpdkefqxgtmulw3z828daucri7y526ne0sgu-2ee3g7q1g9d5j632a1yvmc4t 8.1.12:2377
To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

<Callout icon="lightbulb">
  Copy and execute the join command provided on each worker node to add them to your swarm.
</Callout>

## Deploying Services Using Docker Swarm

Traditionally, you might deploy an application instance (such as a web server) using the `docker run` command. However, running `docker run` individually on each worker node is impractical for large clusters. It requires manual intervention for deployment, load balancing, and monitoring.

Docker Swarm addresses these challenges by orchestrating containers through Docker services. Docker services let you run one or more instances (replicas) of an application across your cluster nodes.

For example, to deploy multiple instances (replicas) of your web server application across worker nodes, execute the following command on the manager node:

```bash theme={null}
docker service create --replicas=3 -p 8080:80 --network frontend my-web-server
```

<Callout icon="triangle-alert">
  Always execute the `docker service create` command on the manager node. Worker nodes should not run service creation commands.
</Callout>

## Conclusion

This high-level overview of Docker Swarm introduced key concepts, such as initializing the swarm and deploying services using Docker's orchestration features. Docker Swarm simplifies the management of containerized applications across a cluster, making it a robust choice for container orchestration.

For those interested in exploring alternative container orchestration platforms, a high-level overview of Kubernetes can provide further insights.

***

For more details and advanced configurations, consider exploring additional resources:

* [Docker Swarm Mode Documentation](https://docs.docker.com/engine/swarm/)
* [Getting Started with Docker](https://docs.docker.com/get-started/)

Happy orchestrating!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner/module/8e0fd79f-1dee-4c31-ae6b-5ce9cd1861e8/lesson/d270b199-cbd0-4bc4-91d1-8889e8a5ed83" />
</CardGroup>
