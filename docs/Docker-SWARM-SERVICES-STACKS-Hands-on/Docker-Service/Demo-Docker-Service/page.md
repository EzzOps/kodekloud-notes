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

Then, simply start the stack with:

```bash theme={null}
docker-compose up
```

Let’s now examine a more comprehensive example.

## The Sample Voting Application

We will use a popular voting application to illustrate a multi-service Docker setup. This sample architecture demonstrates various Docker features and best practices.

<Frame>
  ![A person stands beside a diagram of a sample voting application architecture, showing components like voting-app, result-app, in-memory DB, db, and worker.](https://kodekloud.com/kk-media/image/upload/v1752874070/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Docker-Compose-in-Depth/frame_140.jpg)
</Frame>

### Application Overview

The voting application comprises the following primary components:

* **Voting App:** A Python-based web application that lets users vote (e.g., select between cat or dog). Votes are temporarily stored in Redis.
* **Redis:** Acts as an in-memory database to hold votes temporarily.
* **Worker:** A .NET application that processes votes from Redis and updates a persistent PostgreSQL database.
* **PostgreSQL:** Stores vote counts permanently.
* **Result App:** A Node.js-based web application that reads vote data from PostgreSQL and displays the results.

<Frame>
  ![Diagram of a voting application architecture using Python, Redis, .NET, and PostgreSQL, showing components and data flow with a voting result for cats and dogs.](https://kodekloud.com/kk-media/image/upload/v1752874071/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Docker-Compose-in-Depth/frame_210.jpg)
</Frame>

This architecture clearly illustrates Docker’s versatility—enabling multi-service applications across various languages and platforms.

## Deploying the Application on a Single Docker Host

First, deploy each service using individual Docker run commands. Assume that all images have been built and are available on Docker Hub or your private registry. We will start with the data layer:

1. **Redis Instance:** Run the Redis container in detached mode and name it "redis".
2. **PostgreSQL Instance:** Run the PostgreSQL container (version 9.4) in detached mode and name it "db".

Next, launch the application services:

* **Voting App:** Run the voting app container, name it "vote", and map container port 80 to host port 5000.
* **Result App:** Run the result-app container, name it "result", and map container port 80 to host port 5001.
* **Worker Service:** Run the worker container and name it "worker".

The commands are as follows:

```bash theme={null}
docker run -d --name=redis redis
docker run -d --name=db postgres:9.4
docker run -d --name=vote -p 5000:80 voting-app
```

```bash theme={null}
docker run -d --name=result -p 5001:80 result-app
docker run -d --name=worker worker
```

### The Linking Problem

Even though all containers are running, they cannot communicate by default. For example, the voting app does not know which Redis instance to connect to, and similarly, other containers remain isolated. Container linking solves this issue.

To link the voting app to the Redis container, modify the vote container’s command to include the `--link` option:

```bash theme={null}
docker run -d --name=vote -p 5000:80 --link redis:redis voting-app
```

This command updates the `/etc/hosts` file inside the voting app container to map the hostname "redis" to the Redis container’s internal IP address. Similarly, link containers for the result app and worker:

```bash theme={null}
docker run -d --name=redis redis
docker run -d --name=db postgres:9.4
docker run -d --name=vote -p 5000:80 --link redis:redis voting-app
docker run -d --name=result -p 5001:80 --link db:db result-app
docker run -d --name=worker --link db:db --link redis:redis worker
```

In the voting app’s source code, the Redis connection might be handled like this:

```python theme={null}
def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis
```

And in the worker code, linking is used as follows:

```java theme={null}
try {
    Jedis redis = connectToRedis("redis");
    Connection dbConn = connectToDB("db");
    System.err.println("Watching vote queue");
}
```

<Callout icon="lightbulb">
  Note that container linking is now deprecated. Modern Docker networking and Swarm features provide more robust and flexible ways for container communication.
</Callout>

## Converting Docker Run Commands to a Docker Compose File

Once you are comfortable with the Docker run commands, the next step is to translate them into a Docker Compose file. This involves:

1. Defining entries for each service with the same container names as used in your Docker run commands.
2. Specifying the Docker images or build instructions.
3. Configuring port mapping using the `ports` property.
4. Including the `links` option where necessary.

Here’s a sample Compose file using images directly:

```yaml theme={null}
redis:
  image: redis
db:
  image: postgres:9.4
vote:
  image: voting-app
  ports:
    - 5000:80
  links:
    - redis
result:
  image: result-app
  ports:
    - 5001:80
  links:
    - db
worker:
  image: worker
  links:
    - redis
    - db
```

To build images from local Dockerfiles rather than pulling from a registry, replace the `image` key with a `build` key as follows:

```yaml theme={null}
redis:
  image: redis
db:
  image: postgres:9.4
vote:
  build: ./vote
  ports:
    - 5000:80
  links:
    - redis
result:
  build: ./result
  ports:
    - 5001:80
  links:
    - db
worker:
  build: ./worker
  links:
    - redis
    - db
```

Running `docker-compose up` with this file will build the images (if required) and start the containers with the defined configurations.

## Evolving Compose File Versions

Docker Compose file formats have evolved through three primary versions:

* **Version 1:** Had limitations such as no support for custom networks and no control over container startup order.
* **Version 2:** Introduced several improvements, including a dedicated `services` section, explicit version declaration (e.g., `version: '2'`), enhanced networking features, and the `depends_on` option to control the order in which services start.
* **Version 3:** Builds upon version 2 while adding support for Docker Swarm. In version 3, you declare the version at the top (e.g., `version: '3'`) and define services under the `services` section. Some options have been modified or removed; please refer to the official documentation for a detailed comparison.

Below are examples of all three versions:

```yaml theme={null}
# version: 1
redis:
  image: redis
db:
  image: postgres:9.4
vote:
  image: voting-app
  ports:
    - 5000:80
  links:
    - redis
```

```yaml theme={null}
# version: 2
version: '2'
services:
  redis:
    image: redis
  db:
    image: postgres:9.4
  vote:
    image: voting-app
    ports:
      - 5000:80
    depends_on:
      - redis
```

```yaml theme={null}
# version: 3
version: '3'
services:
  redis:
    image: redis
  db:
    image: postgres:9.4
  vote:
    image: voting-app
    ports:
      - 5000:80
```

## Docker Compose Networking

Enhance your Docker Compose setup by segregating external user traffic from internal service communication. For this scenario, we will define two distinct networks:

* **Front End Network:** Dedicated to external (user-generated) traffic.
* **Back End Network:** Facilitates internal communication between services.

In this configuration, the voting app and result app are connected to both networks, whereas Redis and PostgreSQL are attached only to the back end network.

Below is an example Compose file demonstrating this network setup (port mappings are omitted for clarity):

```yaml theme={null}
version: 2
services:
  redis:
    image: redis
    networks:
      - back-end
  db:
    image: postgres:9.4
    networks:
      - back-end
  vote:
    image: voting-app
    networks:
      - front-end
      - back-end
  result:
    image: result
    networks:
      - front-end
      - back-end
networks:
  front-end:
  back-end:
```

If additional services (such as the worker) are part of your architecture, ensure you assign them to the appropriate networks.

## Conclusion

You now have a detailed overview of Docker Compose—from using basic container linking to translating Docker run commands into a Compose file, and from exploring Compose file versions to implementing advanced networking. Put this knowledge into practice, and try building your own Compose files and networking configurations.

<Frame>
  ![A person stands beside a presentation slide titled "Coding Exercises," listing tasks related to Docker compose files and networking.](https://kodekloud.com/kk-media/image/upload/v1752874072/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Docker-Compose-in-Depth/frame_1130.jpg)
</Frame>

Happy learning, and I look forward to seeing you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/43e8db99-9bc6-4277-88b0-a6f699d2fd76/lesson/66928578-103f-4752-84d7-ecac9a33e95c" />
</CardGroup>


# Demo Docker Service

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Docker-Service/Demo-Docker-Service/page

This guide covers managing Docker services in a Swarm cluster, including creation, scaling, monitoring, and resilience against node failures.

Welcome to this guide on managing Docker services within a Swarm cluster. In this lesson, you'll learn how to create, update, scale, and monitor Docker services. We'll also highlight how running multiple containers as part of a service increases resilience against node failures.

## Verifying the Swarm Cluster

First, ensure your Swarm cluster is properly configured. In this example, our cluster consists of three nodes: one manager (master) node and two worker nodes. Run the following command on the manager node to list all nodes within the cluster:

```bash theme={null}
root@docker-master:/root # docker node ls
ID                         HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS
qp9scmbhf3cz13rxy342pywc   docker-node2   Ready   Active        Reachable
uildwhelph5pjt6vi197tsn5s   docker-master  Ready   Active        Leader
zycf5u8yudke6nfzo74grysx   docker-node1   Ready   Active        Reachable
root@docker-master:/root #
```

## Creating an NGINX Service

Next, create an NGINX service. Because the `--detach=false` flag was not specified, Docker creates the service tasks in the background:

```bash theme={null}
root@docker-master:/root # docker service create nginx
0vehhuvumc1r82u3eijwecl
Since --detach=false was not specified, tasks will be created in the background.
In a future release, --detach=false will become the default.
root@docker-master:/root #
```

<Callout icon="lightbulb">
  Docker automatically assigns a random name to the service if no name is provided.
</Callout>

## Inspecting the Service

After creating the service, list all services to see the assigned name (in this example, "hopeful\_jones"):

```bash theme={null}
root@docker-master:/root # docker service ls
ID            NAME             MODE         REPLICAS
0vehhuvumci0  hopeful_jones    replicated   0/1
```

To inspect the tasks of the service, run:

```bash theme={null}
root@docker-master:/root # docker service ps 0v
ID            NAME               IMAGE         NODE         DESIRED STATE   CURRENT STATE
v3c6kgq7sbwr  hopeful_jones.1    nginx:latest  docker-node2  Running         Running
```

If the container is still pulling the NGINX image from Docker Hub, its state might temporarily display as "Preparing":

```bash theme={null}
root@docker-master:/root # docker service ps 0v
ID            NAME               IMAGE         NODE         DESIRED STATE   CURRENT STATE
v3c6kgq7sbwr  hopeful_jones.1    nginx:latest  docker-node2  Running         Preparing about a minute ago
root@docker-master:/root #
```

You can further verify that the container is running by checking with the `docker ps` command:

```bash theme={null}
root@docker-master:/root # docker ps
CONTAINER ID      IMAGE               COMMAND                  CREATED             STATUS              PORTS    NAMES
6c4b985af166      nginx:latest        "nginx -g 'daemon …'"   10 seconds ago      Up 10 seconds       80/tcp   hopeful_jones
```

Each service receives a random name, and each task is suffixed with an incremental identifier (e.g., "hopeful\_jones.1"). The container's name is derived from the task name along with a unique task ID.

## Publishing a Port

Since NGINX serves web content, you might wish to access it via a web browser. To publish a port so that requests on the host are forwarded to the container, update the service as follows. The command below maps port 5000 on the host to port 80 on the NGINX container:

```bash theme={null}
root@docker-master:/root # docker service update --publish-add 5000:80
```

After the update, confirm the published port with:

```bash theme={null}
root@docker-master:/root # docker service ls
ID            NAME          MODE         REPLICAS  IMAGE         PORTS
0vehhuvumci0  hopeful_jones  replicated  1/1      nginx:latest  *:5000->80/tcp
```

Now, open a web browser and navigate to the host address at port 5000 to view the NGINX welcome page.

## Removing and Scaling the Service

When you’re done with the service, you can remove it by executing:

```bash theme={null}
root@docker-master:/root # docker service rm 0v
```

After removal, the service list will no longer display any active services.

To demonstrate scaling, recreate a similar service this time with multiple replicas. This showcases how Docker Swarm distributes containers across available nodes for enhanced availability:

```bash theme={null}
root@docker-master:/root # docker service create --replicas 2 --name nginx nginx
Since --detach=false was not specified, tasks will be created in the background.
In a future release, --detach=false will become the default.
root@docker-master:/root #
```

Check the status of the newly created service:

```bash theme={null}
root@docker-master:/root # docker service ls
ID                  NAME    MODE        REPLICAS  IMAGE          PORTS
fuwei5oh8r24       nginx   replicated  1/2       nginx:latest
```

Inspect the tasks to see their distribution across nodes:

```bash theme={null}
root@docker-master:/root # docker service ps nginx
ID              NAME         IMAGE          NODE            DESIRED STATE   CURRENT STATE
0949ij67fe78h  nginx.1     nginx:latest   docker-master   Running         Running 29 seconds ago
oyv6thzu1ldt   nginx.2     nginx:latest   docker-node2    Running         Running 19 seconds ago
```

Over time, both replicas should be running and accessible. Initially, one replica might start running before the other is fully up.

## Draining the Manager Node

By default, manager nodes in Docker Swarm can run service tasks. However, if you want the manager node to focus solely on control-plane activities, you can drain it so that no tasks are scheduled on it. Execute the following command on the manager node:

```bash theme={null}
root@docker-master:/root # docker node update --availability drain docker-master
```

Draining the manager node causes any tasks running on it to be shut down and redeployed on other nodes. For example, after draining, the service tasks might appear as follows:

```bash theme={null}
root@docker-master:/root # docker service ps nginx
ID                  NAME         IMAGE          NODE            DESIRED STATE   CURRENT STATE         ERROR   PORTS
blv43kjwaj7        nginx.1      nginx:latest   docker-node1    Running         Preparing 5 seconds ago         80/tcp
0949ij67fe78h      nginx.1      nginx:latest   docker-master   Shutdown        Shutdown 2 seconds ago         80/tcp
oyw6thzulldt       nginx.2      nginx:latest   docker-node2    Running         Running 3 minutes ago
```

After a short period, Docker Swarm automatically migrates tasks away from the drained manager node.

## Simulating a Node Failure

To demonstrate Docker Swarm’s self-healing capabilities, simulate a node failure by shutting down one of the worker nodes. On docker-node1, run the following command:

```bash theme={null}
root@docker-node1:/root # shutdown now
```

Once the node is shut down, Docker Swarm will automatically redeploy the affected tasks onto the other available nodes—even if this means placing both replicas on a single node. You can check the current status of running containers on the manager node with:

```bash theme={null}
root@docker-master:/root # docker ps
```

<Callout icon="lightbulb">
  This self-healing feature ensures your service remains available even if individual nodes fail.
</Callout>

***

Thank you for reading this guide on managing Docker services in a Swarm cluster. We hope you found the walkthrough helpful. Stay tuned for more advanced topics and best practices in managing containerized applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/438444ef-50af-45e0-87e2-cdba1492962f/lesson/ee60240e-5aac-4254-ad9b-9f9ba2327260" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/438444ef-50af-45e0-87e2-cdba1492962f/lesson/feef5517-50da-4d8f-8992-5183a6493afa" />
</CardGroup>
